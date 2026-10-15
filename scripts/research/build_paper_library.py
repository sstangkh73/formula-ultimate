"""Resolve, download and catalogue the Formula Ultimate paper library (Work 145).

The curated inputs live in ``docs/research/paper_library/sources/*.json``. For each
paper this script:

1. confirms the paper's identity against arXiv or OpenAlex metadata by title
   similarity, never trusting a remembered identifier on its own;
2. collects lawful open-access PDF locations (the curated ``pdf_url``, arXiv,
   and OpenAlex open-access locations, plus a publisher ``citation_pdf_url``
   meta tag when a location returns HTML);
3. downloads the first location that returns a real PDF whose first pages
   contain the curated title words, and records SHA-256, size and URL;
4. writes ``manifest_v1.json`` and the bilingual catalog.

Every paper ends in an explicit status. PDFs are written below ``papers/``,
which is git-ignored; only metadata is meant to be committed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html
import io
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
LIBRARY_DIR = ROOT / "docs" / "research" / "paper_library"
SOURCES_DIR = LIBRARY_DIR / "sources"
MANIFEST_PATH = LIBRARY_DIR / "manifest_v1.json"
CATALOG_EN = LIBRARY_DIR / "PAPER_LIBRARY_2026-09-27.md"
CATALOG_TH = LIBRARY_DIR / "PAPER_LIBRARY_2026-09-27.th.md"
PAPERS_DIR = ROOT / "papers"

# An honest, non-browser identity: repositories that challenge browser-like
# clients (for example HAL's Anubis) serve declared tools directly.
USER_AGENT = "FormulaUltimate-PaperLibrary/1.0 (open-access research library builder; python-requests)"
ARXIV_API = "https://export.arxiv.org/api/query"
OPENALEX_API = "https://api.openalex.org/works"
CROSSREF_API = "https://api.crossref.org/works"
S2_BATCH_API = "https://api.semanticscholar.org/graph/v1/paper/batch"
ATOM = "{http://www.w3.org/2005/Atom}"

RESOLVER_VERSION = 2
TITLE_MATCH = 0.86
PDF_WORD_COVERAGE = 0.6
MAX_BYTES = 120 * 1024 * 1024
DOWNLOAD_DEADLINE_S = 240

STATUSES = (
    "downloaded",
    "no_open_access_copy",
    "identity_unconfirmed",
    "download_failed",
)
RELATIONS = ("direct", "indirect", "data")
CARRIED_FIELDS = (
    "status", "local_path", "bytes", "sha256", "download_url", "pdf_title_word_coverage",
    "attempts", "retrieved_utc", "manual_download_url", "failure_kind",
)


# ---------------------------------------------------------------- utilities


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", html.unescape(text or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^0-9a-zA-Z]+", " ", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def title_similarity(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    ratio = difflib.SequenceMatcher(None, na, nb).ratio()
    shorter, longer = sorted((na, nb), key=len)
    # A published title often extends or trims the preprint subtitle.
    if len(shorter) >= 25 and longer.startswith(shorter):
        ratio = max(ratio, 0.95)
    return ratio


def title_matches(curated: str, found: str | None, lenient: bool = False) -> bool:
    """Title identity test; lenient mode is for records fetched by an explicit DOI."""
    if not found:
        return False
    if title_similarity(curated, found) >= TITLE_MATCH:
        return True
    if lenient:
        found_words = normalize(found).split()
        return bool(found_words) and set(found_words) <= set(normalize(curated).split())
    return False


def significant_words(title: str) -> list[str]:
    stop = {
        "with", "from", "into", "using", "that", "this", "their", "over",
        "under", "through", "for", "and", "the", "via", "towards", "toward",
    }
    return [w for w in normalize(title).split() if len(w) > 3 and w not in stop]


def slugify(text: str, limit: int = 60) -> str:
    slug = normalize(text).replace(" ", "-")
    return slug[:limit].rstrip("-") or "paper"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


class Http:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.last_call: dict[str, float] = {}
        self.disabled: dict[str, str] = {}

    def _pace(self, host: str) -> None:
        if "arxiv.org" in host:
            gap = 3.1
        elif "semanticscholar" in host:
            gap = 5.0
        else:
            gap = 0.25
        waited = time.monotonic() - self.last_call.get(host, 0.0)
        if waited < gap:
            time.sleep(gap - waited)
        self.last_call[host] = time.monotonic()

    def get(self, url: str, retry_statuses: tuple[int, ...] = (429, 503), **kwargs) -> requests.Response:
        host = urllib.parse.urlparse(url).netloc
        kwargs.setdefault("timeout", 60)
        last_error: Exception | None = None
        for attempt in range(3):
            self._pace(host)
            try:
                response = self.session.get(url, **kwargs)
                if response.status_code in retry_statuses and attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                return response
            except requests.RequestException as error:  # network noise
                last_error = error
                time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"GET failed for {url}: {last_error}")


# ---------------------------------------------------------------- resolvers


def parse_arxiv_feed(text: str) -> list[dict]:
    entries = []
    root = ET.fromstring(text)
    for entry in root.findall(f"{ATOM}entry"):
        ident = (entry.findtext(f"{ATOM}id") or "").strip()
        title = " ".join((entry.findtext(f"{ATOM}title") or "").split())
        if not ident or title.lower() == "error":
            continue
        arxiv_id = re.sub(r"^https?://arxiv\.org/abs/", "", ident)
        arxiv_id = re.sub(r"v\d+$", "", arxiv_id)
        authors = [
            " ".join((a.findtext(f"{ATOM}name") or "").split())
            for a in entry.findall(f"{ATOM}author")
        ]
        published = entry.findtext(f"{ATOM}published") or ""
        entries.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "year": int(published[:4]) if published[:4].isdigit() else None,
                "venue": "arXiv",
            }
        )
    return entries


def arxiv_by_ids(http: Http, ids: list[str]) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for start in range(0, len(ids), 40):
        chunk = ids[start : start + 40]
        response = http.get(
            ARXIV_API,
            params={"id_list": ",".join(chunk), "max_results": len(chunk)},
        )
        if response.status_code != 200:
            continue
        for entry in parse_arxiv_feed(response.text):
            found[entry["arxiv_id"]] = entry
    return found


def arxiv_by_title(http: Http, title: str) -> dict | None:
    words = [w for w in normalize(title).split() if len(w) > 2][:14]
    if not words:
        return None
    query = " AND ".join(f"ti:{w}" for w in words)
    response = http.get(
        ARXIV_API, params={"search_query": query, "max_results": 5}
    )
    if response.status_code != 200:
        return None
    best, best_score = None, 0.0
    for entry in parse_arxiv_feed(response.text):
        score = title_similarity(title, entry["title"])
        if score > best_score:
            best, best_score = entry, score
    return best if best_score >= TITLE_MATCH else None


def openalex_record(work: dict) -> dict:
    locations = []
    for location in [work.get("best_oa_location")] + list(work.get("locations") or []):
        if not location:
            continue
        pdf = location.get("pdf_url")
        landing = location.get("landing_page_url")
        if location.get("is_oa") and (pdf or landing):
            locations.append({"pdf_url": pdf, "landing_url": landing})
    arxiv_id = None
    for location in work.get("locations") or []:
        landing = (location or {}).get("landing_page_url") or ""
        match = re.search(r"arxiv\.org/abs/([^\s/?#]+?)(v\d+)?$", landing)
        if match:
            arxiv_id = match.group(1)
            break
    source = ((work.get("primary_location") or {}).get("source") or {})
    return {
        "openalex_id": work.get("id"),
        "title": work.get("title") or work.get("display_name") or "",
        "authors": [(a.get("author") or {}).get("display_name", "") for a in work.get("authorships") or []],
        "year": work.get("publication_year"),
        "venue": source.get("display_name"),
        "doi": (work.get("doi") or "").replace("https://doi.org/", "") or None,
        "arxiv_id": arxiv_id,
        "oa_status": (work.get("open_access") or {}).get("oa_status"),
        "oa_url": (work.get("open_access") or {}).get("oa_url"),
        "locations": locations,
    }


def openalex_get(http: Http, url: str, **params) -> dict | None:
    """OpenAlex now meters anonymous use; a spent budget disables it for the run."""
    if http.disabled.get("openalex"):
        return None
    response = http.get(url, params=params or None, retry_statuses=(503,))
    if response.status_code == 429:
        http.disabled["openalex"] = "anonymous daily budget exhausted (HTTP 429)"
        return None
    return response.json() if response.status_code == 200 else None


def openalex_by_doi(http: Http, doi: str) -> dict | None:
    payload = openalex_get(http, f"{OPENALEX_API}/doi:{urllib.parse.quote(doi, safe='/')}")
    return openalex_record(payload) if payload else None


def openalex_by_title(http: Http, title: str, year: int | None) -> dict | None:
    payload = openalex_get(http, OPENALEX_API, search=re.sub(r"[,:;?!|()\"']", " ", title), **{"per-page": 10})
    if not payload:
        return None
    candidates = [openalex_record(work) for work in payload.get("results", [])]
    return best_title_match(title, year, candidates)


def best_title_match(title: str, year: int | None, candidates: list[dict]) -> dict | None:
    best, best_key = None, (0.0, -999)
    for record in candidates:
        score = title_similarity(title, record.get("title") or "")
        if score < TITLE_MATCH:
            continue
        closeness = -abs(int(year) - int(record["year"])) if year and record.get("year") else 0
        key = (round(score, 2), closeness)
        if key > best_key:
            best, best_key = record, key
    return best


def crossref_record(item: dict) -> dict:
    authors = []
    for author in item.get("author") or []:
        name = " ".join(x for x in (author.get("given"), author.get("family")) if x) or author.get("name", "")
        if name:
            authors.append(name)
    year = None
    for key in ("published-print", "published-online", "issued", "created"):
        parts = ((item.get(key) or {}).get("date-parts") or [[None]])[0]
        if parts and parts[0]:
            year = int(parts[0])
            break
    pdf_links = [
        link["URL"]
        for link in item.get("link") or []
        if "pdf" in (link.get("content-type") or "").lower() and link.get("URL")
    ]
    licenses = sorted({(lic.get("URL") or "") for lic in item.get("license") or [] if lic.get("URL")})
    return {
        "doi": item.get("DOI"),
        "title": " ".join(
            ": ".join(x for x in ((item.get("title") or [""])[0], (item.get("subtitle") or [""])[0]) if x).split()
        ),
        "authors": authors,
        "year": year,
        "venue": (item.get("container-title") or [None])[0],
        "type": item.get("type"),
        "pdf_links": pdf_links,
        "licenses": licenses,
    }


def crossref_by_doi(http: Http, doi: str) -> dict | None:
    response = http.get(f"{CROSSREF_API}/{urllib.parse.quote(doi, safe='/')}")
    if response.status_code != 200:
        return None
    return crossref_record(response.json()["message"])


def crossref_by_title(http: Http, title: str, year: int | None) -> dict | None:
    response = http.get(
        CROSSREF_API,
        params={
            "query.bibliographic": title,
            "rows": 8,
            "select": "DOI,title,subtitle,issued,published-print,published-online,created,author,container-title,link,license,type",
        },
    )
    if response.status_code != 200:
        return None
    candidates = [crossref_record(item) for item in response.json()["message"].get("items", [])]
    return best_title_match(title, year, candidates)


def semantic_scholar_batch(http: Http, keys: list[str]) -> dict[str, dict]:
    """One batch call per 400 identifiers keeps well inside the anonymous limit."""
    found: dict[str, dict] = {}
    for start in range(0, len(keys), 400):
        chunk = keys[start : start + 400]
        for attempt in range(6):
            http._pace("api.semanticscholar.org")
            try:
                response = http.session.post(
                    S2_BATCH_API,
                    params={"fields": "title,year,venue,authors,externalIds,openAccessPdf,isOpenAccess"},
                    json={"ids": chunk},
                    timeout=90,
                )
            except requests.RequestException:
                time.sleep(10)
                continue
            if response.status_code == 200:
                for key, record in zip(chunk, response.json()):
                    if record:
                        found[key] = {
                            "paper_id": record.get("paperId"),
                            "title": record.get("title") or "",
                            "year": record.get("year"),
                            "venue": record.get("venue"),
                            "authors": [a.get("name", "") for a in record.get("authors") or []],
                            "external_ids": record.get("externalIds") or {},
                            "open_access_pdf": ((record.get("openAccessPdf") or {}).get("url")) or None,
                        }
                break
            time.sleep(15 * (attempt + 1))
        else:
            print(f"semantic scholar batch unavailable for {len(chunk)} ids", flush=True)
    return found



# ---------------------------------------------------------------- download


def extract_first_pages_text(data: bytes) -> str | None:
    try:
        import fitz  # PyMuPDF

        with fitz.open(stream=data, filetype="pdf") as document:
            return " ".join(document[i].get_text() for i in range(min(2, document.page_count)))
    except Exception:
        pass
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        return " ".join((reader.pages[i].extract_text() or "") for i in range(min(2, len(reader.pages))))
    except Exception:
        return None


def title_word_coverage(title: str, text: str | None) -> float | None:
    if text is None:
        return None
    haystack = " " + normalize(text) + " "
    squashed = haystack.replace(" ", "")
    words = significant_words(title)
    if not words:
        return None
    hits = sum(1 for w in words if f" {w} " in haystack or w in squashed)
    return round(hits / len(words), 3)


def title_phrase_present(title: str, text: str | None) -> bool:
    """The whole title (or its part before a colon, if long) appears contiguously in the text."""
    if not text:
        return False
    squashed = normalize(text).replace(" ", "")
    whole = normalize(title).replace(" ", "")
    main = normalize(title.split(":")[0]).replace(" ", "")
    return whole in squashed or (len(main) >= 15 and main in squashed)


def pdf_links_in_page(page: str, base_url: str) -> list[str]:
    """PDF links a landing page declares, most authoritative first."""
    q, nq = "[\"']", "[^\"']"
    links: list[str] = []
    for name in ("citation_pdf_url", "bepress_citation_pdf_url", "eprints.document_url"):
        key = re.escape(name)
        for pattern in (
            f"<meta[^>]+name={q}{key}{q}[^>]+content={q}({nq}+)",
            f"<meta[^>]+content={q}({nq}+){q}[^>]+name={q}{key}{q}",
        ):
            links += re.findall(pattern, page, flags=re.IGNORECASE)
    links += re.findall(f"href={q}({nq}+?\\.pdf(?:\\?{nq}*)?){q}", page, flags=re.IGNORECASE)
    seen, ordered = set(), []
    for link in links:
        absolute = urllib.parse.urljoin(base_url, html.unescape(link))
        if absolute not in seen:
            seen.add(absolute)
            ordered.append(absolute)
    return ordered


def fetch_pdf(
    http: Http, url: str, follow_meta: bool = True, deadline_s: float = DOWNLOAD_DEADLINE_S
) -> tuple[bytes | None, str, str]:
    """Return (pdf bytes, final url, note)."""
    started = time.monotonic()
    try:
        response = http.get(url, allow_redirects=True, stream=True, timeout=(15, 45))
    except RuntimeError as error:
        return None, url, str(error)
    if response.status_code != 200:
        return None, url, f"HTTP {response.status_code}"
    chunks, size = [], 0
    try:
        for chunk in response.iter_content(1 << 16):
            chunks.append(chunk)
            size += len(chunk)
            if size > MAX_BYTES:
                return None, response.url, "exceeds size limit"
            if time.monotonic() - started > deadline_s:
                return None, response.url, f"slower than {deadline_s:g} s deadline"
    except requests.RequestException as error:
        return None, response.url, f"transfer error: {type(error).__name__}"
    data = b"".join(chunks)
    if b"%PDF" in data[:1024]:
        return data, response.url, "ok"
    content_type = response.headers.get("Content-Type", "")
    if follow_meta and "html" in content_type.lower():
        for link in pdf_links_in_page(data.decode("utf-8", "replace"), response.url)[:6]:
            if link == url:
                continue
            pdf, final, note = fetch_pdf(http, link, follow_meta=False, deadline_s=deadline_s)
            if pdf is not None:
                return pdf, final, note
    return None, response.url, f"not a PDF ({content_type or 'unknown type'})"


# ---------------------------------------------------------------- pipeline


def load_sources() -> tuple[list[dict], list[dict]]:
    categories, papers = [], []
    for path in sorted(SOURCES_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        category = payload["category"]
        category["source_file"] = path.name
        categories.append(category)
        for paper in payload["papers"]:
            paper["category"] = category["key"]
            papers.append(paper)
    return categories, papers


def verify_arxiv(http: Http, title: str, arxiv_id: str | None, cache: dict[str, dict]) -> dict | None:
    if not arxiv_id:
        return None
    arxiv_id = re.sub(r"v\d+$", "", arxiv_id)
    if arxiv_id not in cache:
        cache.update(arxiv_by_ids(http, [arxiv_id]))
    entry = cache.get(arxiv_id)
    return entry if entry and title_matches(title, entry["title"]) else None


def resolve(http: Http, papers: list[dict], previous: dict, use_openalex: bool) -> dict[str, dict]:
    """Confirm each paper's identity by title against arXiv, Crossref, Semantic Scholar (and OpenAlex)."""
    resolved: dict[str, dict] = {}
    todo = []
    for paper in papers:
        cached = previous.get(paper["id"]) or {}
        identity = cached.get("identity") or {}
        if identity.get("resolver_version") == RESOLVER_VERSION and cached.get("curated_title") == paper["title"]:
            resolved[paper["id"]] = identity
        else:
            todo.append(paper)
    if not use_openalex:
        http.disabled["openalex"] = "not requested"
    arxiv_cache = arxiv_by_ids(http, sorted({p["arxiv"] for p in todo if p.get("arxiv")}))
    for index, paper in enumerate(todo, start=1):
        identity: dict = {
            "resolver_version": RESOLVER_VERSION,
            "arxiv": None,
            "crossref": None,
            "s2": None,
            "openalex": None,
            "rejected_hints": [],
        }
        title, year = paper["title"], paper.get("year")
        if paper.get("arxiv"):
            identity["arxiv"] = verify_arxiv(http, title, paper["arxiv"], arxiv_cache)
            if identity["arxiv"] is None:
                found = arxiv_cache.get(paper["arxiv"])
                identity["rejected_hints"].append({"arxiv": paper["arxiv"], "found_title": found["title"] if found else None})
        if paper.get("doi"):
            record = crossref_by_doi(http, paper["doi"])
            if record and title_matches(title, record["title"], lenient=True):
                identity["crossref"] = record
            else:
                identity["rejected_hints"].append({"doi": paper["doi"], "found_title": record["title"] if record else None})
        if identity["crossref"] is None and not paper.get("arxiv"):
            identity["crossref"] = crossref_by_title(http, title, year)
        if use_openalex:
            doi = (identity["crossref"] or {}).get("doi") or paper.get("doi")
            record = openalex_by_doi(http, doi) if doi else openalex_by_title(http, title, year)
            if record and title_matches(title, record["title"], lenient=bool(doi)):
                identity["openalex"] = record
        if identity["arxiv"] is None and (year or 9999) >= 1991:
            identity["arxiv"] = verify_arxiv(http, title, (identity["openalex"] or {}).get("arxiv_id"), arxiv_cache)
            if identity["arxiv"] is None:
                identity["arxiv"] = arxiv_by_title(http, title)
        resolved[paper["id"]] = identity
        print(
            f"[resolve {index}/{len(todo)}] {paper['id']}: arxiv={'yes' if identity['arxiv'] else 'no'} "
            f"crossref={'yes' if identity['crossref'] else 'no'}",
            flush=True,
        )
    # One batched Semantic Scholar call adds open-access PDF locations (author copies, repositories).
    keys: dict[str, str] = {}
    for paper in todo:
        identity = resolved[paper["id"]]
        doi = (identity["crossref"] or {}).get("doi") or paper.get("doi")
        arxiv_id = (identity["arxiv"] or {}).get("arxiv_id")
        if doi:
            keys[paper["id"]] = f"DOI:{doi}"
        elif arxiv_id:
            keys[paper["id"]] = f"ARXIV:{arxiv_id}"
    if keys:
        found = semantic_scholar_batch(http, sorted(set(keys.values())))
        by_id = {p["id"]: p for p in todo}
        for pid, key in keys.items():
            record = found.get(key)
            paper = by_id[pid]
            if record and title_matches(paper["title"], record["title"], lenient=True):
                resolved[pid]["s2"] = record
                if resolved[pid]["arxiv"] is None and record["external_ids"].get("ArXiv"):
                    resolved[pid]["arxiv"] = verify_arxiv(http, paper["title"], record["external_ids"]["ArXiv"], arxiv_cache)
    return resolved


def candidate_urls(paper: dict, identity: dict) -> list[str]:
    urls: list[str] = list(paper.get("pdf_urls", []))
    if paper.get("pdf_url"):
        urls.append(paper["pdf_url"])
    if identity.get("arxiv"):
        urls.append(f"https://arxiv.org/pdf/{identity['arxiv']['arxiv_id']}")
    if (identity.get("s2") or {}).get("open_access_pdf"):
        urls.append(identity["s2"]["open_access_pdf"])
    openalex = identity.get("openalex") or {}
    urls += [loc["pdf_url"] for loc in openalex.get("locations", []) if loc.get("pdf_url")]
    crossref = identity.get("crossref") or {}
    urls += crossref.get("pdf_links", [])
    doi = crossref.get("doi") or openalex.get("doi") or paper.get("doi")
    if doi:
        urls.append(f"https://doi.org/{doi}")
    urls += [loc["landing_url"] for loc in openalex.get("locations", []) if loc.get("landing_url") and not loc.get("pdf_url")]
    if paper.get("landing_url"):
        urls.append(paper["landing_url"])
    seen, ordered = set(), []
    for url in urls:
        if url and url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def local_name(paper: dict, identity: dict) -> str:
    meta = merged_metadata(paper, identity)
    authors = meta["authors"]
    first = authors[0] if authors else "anon"
    surname = (normalize(first.split(",")[0]).split(" ") or ["anon"])[-1].capitalize() or "Anon"
    year = meta["year"] or "nd"
    return f"{paper['id']}_{surname}{year}_{slugify(paper['title'], 50)}.pdf"


def download(http: Http, paper: dict, identity: dict, folder: str, previous: dict) -> dict:
    pid = paper["id"]
    cached = previous.get(pid) or {}
    if cached.get("status") == "downloaded":
        path = ROOT / cached["local_path"]
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == cached.get("sha256"):
            return {k: cached[k] for k in CARRIED_FIELDS if k in cached}
    urls = candidate_urls(paper, identity)
    confirmed = any(identity.get(k) for k in ("arxiv", "crossref", "s2", "openalex"))
    attempts = []
    if not urls:
        return {"status": "no_open_access_copy", "attempts": attempts}
    target_dir = PAPERS_DIR / folder
    for url in urls[:8]:
        data, final_url, note = fetch_pdf(http, url, deadline_s=paper.get("deadline_s", DOWNLOAD_DEADLINE_S))
        if data is None:
            attempts.append({"url": url, "result": note})
            continue
        coverage = title_word_coverage(paper["title"], extract_first_pages_text(data))
        if coverage is not None and coverage < PDF_WORD_COVERAGE:
            attempts.append({"url": url, "result": f"title words not on first pages (coverage {coverage})"})
            continue
        if coverage is None and not confirmed:
            attempts.append({"url": url, "result": "no extractable text and no resolver identity"})
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / local_name(paper, identity)
        path.write_bytes(data)
        attempts.append({"url": url, "result": "ok"})
        return {
            "status": "downloaded",
            "local_path": path.relative_to(ROOT).as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "download_url": final_url,
            "pdf_title_word_coverage": coverage,
            "attempts": attempts,
            "retrieved_utc": utc_now(),
        }
    oa_urls = open_access_indicators(paper, identity)
    if attempts and all("title words" in a["result"] for a in attempts):
        status = "identity_unconfirmed"
    elif not oa_urls:
        # Only a publisher landing page was available and it did not serve a PDF.
        status = "no_open_access_copy"
    else:
        status = "download_failed"
    result = {"status": status, "attempts": attempts}
    if status == "download_failed":
        result["manual_download_url"] = oa_urls[0]
        result["failure_kind"] = failure_kind(attempts)
    return result


def open_access_indicators(paper: dict, identity: dict) -> list[str]:
    """URLs that a source asserts are free to read (curated, arXiv, Semantic Scholar, OpenAlex, CC licence)."""
    urls = list(paper.get("pdf_urls", [])) + ([paper["pdf_url"]] if paper.get("pdf_url") else [])
    if identity.get("arxiv"):
        urls.append(f"https://arxiv.org/pdf/{identity['arxiv']['arxiv_id']}")
    if (identity.get("s2") or {}).get("open_access_pdf"):
        urls.append(identity["s2"]["open_access_pdf"])
    urls += [loc.get("pdf_url") or loc.get("landing_url") for loc in (identity.get("openalex") or {}).get("locations", [])]
    crossref = identity.get("crossref") or {}
    if any("creativecommons.org" in lic for lic in crossref.get("licenses", [])):
        urls += crossref.get("pdf_links", []) or [f"https://doi.org/{crossref['doi']}"]
    return [u for u in urls if u]


def failure_kind(attempts: list[dict]) -> str:
    results = " ".join(a["result"] for a in attempts)
    if "HTTP 403" in results or "HTTP 401" in results:
        return "publisher_access_check"
    if "GET failed" in results or "transfer error" in results or "deadline" in results:
        return "host_unreachable_or_slow"
    return "no_pdf_served"


def merged_metadata(paper: dict, identity: dict) -> dict:
    records = [identity.get(k) or {} for k in ("crossref", "openalex", "s2", "arxiv")]

    def first(field: str):
        for record in records:
            if record.get(field):
                return record[field]
        return None

    arxiv_id = (identity.get("arxiv") or {}).get("arxiv_id") or (identity.get("openalex") or {}).get("arxiv_id")
    doi = paper.get("doi") or first("doi")
    return {
        "authors": paper.get("authors") or first("authors") or [],
        "year": paper.get("year") or first("year"),
        "venue": paper.get("venue") or first("venue"),
        "doi": doi,
        "arxiv_id": arxiv_id,
        "landing_url": paper.get("landing_url")
        or (f"https://doi.org/{doi}" if doi else None)
        or (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None)
        or paper.get("pdf_url"),
    }


def author_label(authors: list[str]) -> str:
    if not authors:
        return "—"
    surnames = [a.split(",")[0].split(" ")[-1] if " " in a else a for a in authors]
    if len(surnames) == 1:
        return surnames[0]
    if len(surnames) == 2:
        return f"{surnames[0]} & {surnames[1]}"
    return f"{surnames[0]} et al."


# ---------------------------------------------------------------- catalog


EN = {
    "title": "# Formula Ultimate Paper Library — 2026-09-27",
    "companion": "Thai companion: `PAPER_LIBRARY_2026-09-27.th.md`",
    "local": "local PDF",
    "nolocal": "no local copy",
    "manual": "open-access copy to fetch in a browser",
    "manual_heading": "Open-access papers to download by hand",
    "manual_intro": "A free copy of each paper below exists, but its host refused scripted downloads (mostly Cloudflare-style bot checks at MDPI, ACM, PNAS, Royal Society, IEEE and some university repositories), and that check was not bypassed. Open the link in a browser, save the PDF into one folder, then run `python scripts/research/build_paper_library.py --ingest <folder>`. Naming a file `<ID>.pdf` (for example `OE-003.pdf`) makes the match explicit; the title check still applies.",
    "manual_title": "Title",
    "manual_link": "Open in a browser",
    "relation": {"direct": "direct", "indirect": "indirect", "data": "data/findings"},
    "prior": "Work 102 catalog",
    "status": {
        "downloaded": "downloaded",
        "no_open_access_copy": "no open-access copy found",
        "identity_unconfirmed": "identity unconfirmed",
        "download_failed": "download failed",
    },
}
TH = {
    "title": "# คลัง paper ของ Formula Ultimate — 2026-09-27",
    "companion": "ต้นฉบับภาษาอังกฤษ: `PAPER_LIBRARY_2026-09-27.md`",
    "local": "มี PDF ในเครื่อง",
    "nolocal": "ไม่มีสำเนาในเครื่อง",
    "manual": "สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์",
    "manual_heading": "paper open access ที่ต้องดาวน์โหลดด้วยมือ",
    "manual_intro": "paper แต่ละชิ้นด้านล่างมีสำเนาฟรี แต่เซิร์ฟเวอร์ปฏิเสธการดาวน์โหลดด้วยสคริปต์ (ส่วนใหญ่เป็นการตรวจ bot แบบ Cloudflare ที่ MDPI, ACM, PNAS, Royal Society, IEEE และคลังของบางมหาวิทยาลัย) และไม่ได้พยายามข้ามการตรวจนั้น ให้เปิดลิงก์ในเบราว์เซอร์ บันทึก PDF ไว้ในโฟลเดอร์เดียวกัน แล้วรัน `python scripts/research/build_paper_library.py --ingest <folder>` การตั้งชื่อไฟล์เป็น `<ID>.pdf` (เช่น `OE-003.pdf`) ทำให้จับคู่ได้ชัดเจน โดยยังมีการตรวจชื่อเรื่องเหมือนเดิม",
    "manual_title": "ชื่อเรื่อง",
    "manual_link": "เปิดในเบราว์เซอร์",
    "relation": {"direct": "ตรง", "indirect": "อ้อม", "data": "ข้อมูล/ผลที่ใช้ได้"},
    "prior": "แค็ตตาล็อก Work 102",
    "status": {
        "downloaded": "ดาวน์โหลดแล้ว",
        "no_open_access_copy": "ไม่พบสำเนา open access",
        "identity_unconfirmed": "ยืนยันตัวตนไม่ได้",
        "download_failed": "ดาวน์โหลดไม่สำเร็จ",
    },
}


def write_catalog(categories: list[dict], papers: list[dict], manifest: dict, intro_en: str, intro_th: str) -> None:
    for language, labels, path, intro in (
        ("en", EN, CATALOG_EN, intro_en),
        ("th", TH, CATALOG_TH, intro_th),
    ):
        lines = [labels["title"], "", labels["companion"], "", intro.strip(), ""]
        lines += summary_table(categories, papers, manifest, language)
        counts = {s: sum(e["status"] == s for e in manifest["papers"].values()) for s in STATUSES}
        lines += ["", " · ".join(f"{labels['status'][s]}: **{counts[s]}**" for s in STATUSES)]
        for category in categories:
            members = [p for p in papers if p["category"] == category["key"]]
            if not members:
                continue
            heading = category["title_en"] if language == "en" else category["title_th"]
            lines += ["", f"## {heading}", ""]
            scope = category["scope_en"] if language == "en" else category["scope_th"]
            lines += [scope, ""]
            for paper in members:
                entry = manifest["papers"][paper["id"]]
                meta = entry["metadata"]
                parts = [author_label(meta["authors"]), str(meta["year"] or "n.d.")]
                if meta.get("venue"):
                    parts.append(" ".join(str(meta["venue"]).split()))
                parts.append(f"**{labels['relation'][paper['relation']]}**")
                if paper.get("prior_catalog_id"):
                    parts.append(f"{labels['prior']} {paper['prior_catalog_id']}")
                lines.append(f"### {paper['id']} — {paper['title']}")
                lines.append("")
                lines.append(" · ".join(parts))
                lines.append("")
                links = []
                if meta.get("landing_url"):
                    links.append(f"[{'source' if language == 'en' else 'แหล่ง'}]({meta['landing_url']})")
                if meta.get("arxiv_id"):
                    links.append(f"[arXiv:{meta['arxiv_id']}](https://arxiv.org/abs/{meta['arxiv_id']})")
                if entry["status"] == "downloaded":
                    local = entry["local_path"]
                    links.append(f"{labels['local']}: [`{local}`](../../../{local})")
                else:
                    links.append(f"{labels['nolocal']} ({labels['status'][entry['status']]})")
                    if entry.get("manual_download_url"):
                        links.append(f"[{labels['manual']}]({entry['manual_download_url']})")
                lines.append(" · ".join(links))
                lines.append("")
                lines.append(paper["why_en"] if language == "en" else paper["why_th"])
                lines.append("")
        manual = [p for p in papers if manifest["papers"][p["id"]].get("manual_download_url")]
        if manual:
            lines += ["", f"## {labels['manual_heading']}", "", labels["manual_intro"], ""]
            lines += [f"| ID | {labels['manual_title']} | {labels['manual_link']} |", "| --- | --- | --- |"]
            for paper in manual:
                url = manifest["papers"][paper["id"]]["manual_download_url"]
                host = urllib.parse.urlparse(url).netloc
                lines.append(f"| {paper['id']} | {paper['title'].replace('|', '/')} | [{host}]({url}) |")
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def summary_table(categories, papers, manifest, language) -> list[str]:
    if language == "en":
        head = ["| Category | Papers | Direct | Indirect | Data | Local PDF |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    else:
        head = ["| หมวด | จำนวน | ตรง | อ้อม | ข้อมูล | มี PDF |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    rows = []
    totals = [0, 0, 0, 0, 0]
    for category in categories:
        members = [p for p in papers if p["category"] == category["key"]]
        counts = [
            len(members),
            sum(p["relation"] == "direct" for p in members),
            sum(p["relation"] == "indirect" for p in members),
            sum(p["relation"] == "data" for p in members),
            sum(manifest["papers"][p["id"]]["status"] == "downloaded" for p in members),
        ]
        totals = [a + b for a, b in zip(totals, counts)]
        name = category["title_en"] if language == "en" else category["title_th"]
        rows.append(f"| {name} | " + " | ".join(str(c) for c in counts) + " |")
    total_label = "**Total**" if language == "en" else "**รวม**"
    rows.append(f"| {total_label} | " + " | ".join(f"**{c}**" for c in totals) + " |")
    return head + rows


def ingest(inbox: Path, categories: list[dict], papers: list[dict], manifest: dict) -> list[str]:
    """File PDFs a person downloaded in a browser (for pages a script may not pass).

    A file is matched by an id prefix in its name (for example ``AE-011.pdf``) or,
    failing that, by the curated title appearing as a phrase on its first pages.
    Scattered title words are not enough here: short generic titles ("Development
    of a Functional Basis for Design") share most words with unrelated papers.
    """
    folders = {c["key"]: c["folder"] for c in categories}
    by_id = {p["id"]: p for p in papers}
    pending = [p for p in papers if manifest["papers"].get(p["id"], {}).get("status") != "downloaded"]
    report = []
    for pdf in sorted(inbox.glob("*.pdf")):
        data = pdf.read_bytes()
        if b"%PDF" not in data[:1024]:
            report.append(f"{pdf.name}: skipped, not a PDF")
            continue
        text = extract_first_pages_text(data)
        match = re.match(r"([A-Z]{2,3}-\d{3})", pdf.name)
        if match and match.group(1) in by_id:
            paper = by_id[match.group(1)]
            coverage = title_word_coverage(paper["title"], text)
            if not title_phrase_present(paper["title"], text) and (coverage is None or coverage < 0.8):
                report.append(f"{pdf.name}: title of {paper['id']} not found on first pages (word coverage {coverage}); not filed")
                continue
        else:
            hits = [p for p in pending if title_phrase_present(p["title"], text)]
            if len(hits) != 1:
                report.append(f"{pdf.name}: {len(hits)} catalog titles found on first pages; rename it '<ID>.pdf'")
                continue
            paper = hits[0]
            coverage = title_word_coverage(paper["title"], text)
        entry = manifest["papers"].setdefault(paper["id"], {"curated_title": paper["title"], "identity": {}, "metadata": {}})
        target_dir = PAPERS_DIR / folders[paper["category"]]
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / local_name(paper, entry.get("identity") or {})
        target.write_bytes(data)
        pdf.unlink()
        for key in ("manual_download_url", "failure_kind"):
            entry.pop(key, None)
        entry.update(
            {
                "status": "downloaded",
                "local_path": target.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "download_url": f"manual:{pdf.name}",
                "pdf_title_word_coverage": coverage,
                "retrieved_utc": utc_now(),
            }
        )
        report.append(f"{pdf.name}: filed as {paper['id']} -> {entry['local_path']}")
    return report


def verify(manifest: dict) -> list[str]:
    """Every downloaded entry must exist locally, be a PDF and match its recorded SHA-256."""
    problems = []
    for pid, entry in manifest["papers"].items():
        if entry.get("status") != "downloaded":
            continue
        path = ROOT / entry["local_path"]
        if not path.is_file():
            problems.append(f"{pid}: missing {entry['local_path']}")
            continue
        data = path.read_bytes()
        if b"%PDF" not in data[:1024]:
            problems.append(f"{pid}: not a PDF")
        if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["bytes"]:
            problems.append(f"{pid}: SHA-256 or size differs from manifest")
    return problems


def write_manifest(manifest: dict) -> None:
    """Atomic replace with retries: Windows can briefly lock a file another process is reading."""
    temporary = MANIFEST_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for attempt in range(10):
        try:
            os.replace(temporary, MANIFEST_PATH)
            return
        except OSError:
            time.sleep(0.5 * (attempt + 1))
    raise OSError(f"could not replace {MANIFEST_PATH}")


# ---------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="download open-access PDFs")
    parser.add_argument("--only", help="comma-separated paper ids to (re)process")
    parser.add_argument("--refresh", action="store_true", help="ignore cached identities")
    parser.add_argument("--catalog-only", action="store_true", help="rewrite the catalog from the manifest")
    parser.add_argument("--openalex", action="store_true", help="also query OpenAlex (metered for anonymous use)")
    parser.add_argument("--verify", action="store_true", help="check local PDFs against the manifest and exit")
    parser.add_argument("--ingest", metavar="DIR", help="file PDFs downloaded by hand (name them '<ID>*.pdf' or leave the title to be matched)")
    args = parser.parse_args(argv)

    categories, papers = load_sources()
    ids = [p["id"] for p in papers]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        print(f"duplicate ids: {duplicates}", file=sys.stderr)
        return 2

    manifest = {"version": 1, "papers": {}}
    if MANIFEST_PATH.is_file():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    previous = {} if args.refresh else manifest.get("papers", {})
    intro = json.loads((LIBRARY_DIR / "intro.json").read_text(encoding="utf-8"))

    if args.verify:
        problems = verify(manifest)
        downloaded = sum(e.get("status") == "downloaded" for e in manifest["papers"].values())
        for line in problems:
            print(line)
        print(json.dumps({"downloaded_checked": downloaded, "problems": len(problems)}))
        return 1 if problems else 0
    if args.ingest:
        for line in ingest(Path(args.ingest), categories, papers, manifest):
            print(line)
    elif not args.catalog_only:
        selected = papers
        if args.only:
            wanted = set(args.only.split(","))
            selected = [p for p in papers if p["id"] in wanted]
            previous = {k: v for k, v in previous.items() if k not in wanted}
        http = Http()
        identities = resolve(http, selected, previous, use_openalex=args.openalex)
        folders = {c["key"]: c["folder"] for c in categories}
        for index, paper in enumerate(selected, start=1):
            identity = identities[paper["id"]]
            entry = {
                "curated_title": paper["title"],
                "category": paper["category"],
                "relation": paper["relation"],
                "identity": identity,
                "metadata": merged_metadata(paper, identity),
            }
            if args.download:
                entry.update(download(http, paper, identity, folders[paper["category"]], previous))
            else:
                old = previous.get(paper["id"], {})
                entry.update({k: old[k] for k in CARRIED_FIELDS if k in old})
                entry.setdefault("status", "download_failed" if candidate_urls(paper, identity) else "no_open_access_copy")
            manifest["papers"][paper["id"]] = entry
            print(f"[download {index}/{len(selected)}] {paper['id']}: {entry['status']}", flush=True)
            write_manifest(manifest)

    known = set(ids)
    manifest["papers"] = {k: v for k, v in manifest["papers"].items() if k in known}
    ordered = {p["id"]: manifest["papers"][p["id"]] for p in papers if p["id"] in manifest["papers"]}
    manifest.update(
        {
            "version": 1,
            "work_item": 145,
            "generated_utc": utc_now(),
            "generator": "scripts/research/build_paper_library.py",
            "papers": ordered,
        }
    )
    write_manifest(manifest)
    missing = [p["id"] for p in papers if p["id"] not in ordered]
    if missing:
        print(f"not yet processed: {missing}", file=sys.stderr)
        return 1
    write_catalog(categories, papers, manifest, intro["en"], intro["th"])
    counts = {s: sum(e["status"] == s for e in ordered.values()) for s in STATUSES}
    print(json.dumps({"papers": len(ordered), **counts}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
