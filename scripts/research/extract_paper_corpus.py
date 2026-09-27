from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "docs" / "research" / "paper_library" / "sources"
LIBRARY_MANIFEST = ROOT / "docs" / "research" / "paper_library" / "manifest_v1.json"
READING_ROOT = ROOT / "docs" / "research" / "paper_reviews"
READING_MANIFEST = READING_ROOT / "reading_manifest.json"
CORPUS_ROOT = ROOT / "artifacts" / "paper_review_corpus"

PUBLIC_RECORD_FIELDS = (
    "id",
    "category",
    "title",
    "authors",
    "year",
    "relation",
    "source_pdf",
    "sha256",
    "page_count",
    "pages_with_text",
    "text_coverage",
    "characters",
    "words",
    "likely_scanned",
    "page_character_counts",
    "extraction_errors",
    "keywords",
    "full_text_path",
)

SECTION_PATTERNS = {
    "abstract": re.compile(r"(?im)^\s*(?:abstract|summary)\s*$"),
    "introduction": re.compile(r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?introduction\s*$"),
    "methods": re.compile(
        r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?(?:method(?:s|ology)?|materials and methods|approach|framework)\s*$"
    ),
    "results": re.compile(r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?(?:results?|experiments?|evaluation)\s*$"),
    "discussion": re.compile(r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?discussion\s*$"),
    "limitations": re.compile(r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?limitations?\s*$"),
    "conclusion": re.compile(
        r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?(?:conclusions?|concluding remarks|discussion and conclusions?)\s*$"
    ),
    "references": re.compile(r"(?im)^\s*(?:references|bibliography)\s*$"),
}

EVIDENCE_TERMS = re.compile(
    r"(?i)\b(?:we (?:find|found|show|demonstrate|observe|report|evaluate|compare|propose)|"
    r"results? (?:show|indicate|suggest)|outperform|improv(?:e|ed|ement)|reduce[ds]?|increase[ds]?|"
    r"limitation|failure|however|significant|baseline|ablation|experiment|validated?|physical|"
    r"manufactur|robust|uncertainty|generaliz|constraint|accuracy|error|dataset|benchmark)\b"
)


@dataclass(frozen=True)
class Paper:
    paper_id: str
    category: str
    title: str
    authors: list[str]
    year: int | None
    relation: str
    why_en: str
    why_th: str
    local_path: Path
    expected_sha256: str


def normalize_authors(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(author).strip() for author in value if str(author).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return []


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_papers() -> list[Paper]:
    source_by_id: dict[str, dict] = {}
    for source_path in sorted(SOURCE_DIR.glob("*.json")):
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        category = payload["category"]["key"]
        for entry in payload["papers"]:
            source_by_id[entry["id"]] = {**entry, "category": category}

    manifest = json.loads(LIBRARY_MANIFEST.read_text(encoding="utf-8"))["papers"]
    papers: list[Paper] = []
    for paper_id, item in sorted(manifest.items()):
        if item["status"] != "downloaded":
            continue
        source = source_by_id[paper_id]
        authors = normalize_authors(source.get("authors") or item.get("metadata", {}).get("authors"))
        papers.append(
            Paper(
                paper_id=paper_id,
                category=source["category"],
                title=source["title"],
                authors=authors,
                year=source.get("year"),
                relation=source["relation"],
                why_en=source["why_en"],
                why_th=source["why_th"],
                local_path=ROOT / item["local_path"],
                expected_sha256=item["sha256"],
            )
        )
    return papers


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ").replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def page_marked_text(page_texts: list[str]) -> str:
    return "\n\n".join(
        f"[[PAGE {index}]]\n{text}" for index, text in enumerate(page_texts, start=1)
    )


def section_excerpt(full_text: str, pattern: re.Pattern[str], max_chars: int = 5000) -> str | None:
    match = pattern.search(full_text)
    if not match:
        return None
    start = match.end()
    candidates = [m.start() for p in SECTION_PATTERNS.values() for m in p.finditer(full_text, start)]
    end = min(candidates) if candidates else len(full_text)
    section = full_text[start:end].strip()
    return section[:max_chars] or None


def sentence_candidates(page_texts: list[str], limit: int = 18) -> list[dict]:
    candidates: list[tuple[int, int, str]] = []
    for page_number, text in enumerate(page_texts, start=1):
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.replace("\n", " ")):
            sentence = re.sub(r"\s+", " ", sentence).strip()
            words = sentence.split()
            if not 12 <= len(words) <= 80 or not EVIDENCE_TERMS.search(sentence):
                continue
            score = 2 * len(EVIDENCE_TERMS.findall(sentence))
            score += 2 if re.search(r"\b\d+(?:\.\d+)?\s*(?:%|ms|s|kg|N|W|kW|J|MJ|m/s|km/h)\b", sentence) else 0
            score += 1 if re.search(r"(?i)\b(?:than|versus|compared|relative to|across)\b", sentence) else 0
            candidates.append((score, page_number, sentence))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    selected: list[dict] = []
    normalized_seen: set[str] = set()
    for score, page, sentence in candidates:
        key = re.sub(r"\W+", " ", sentence.lower())[:120]
        if key in normalized_seen:
            continue
        normalized_seen.add(key)
        selected.append({"page": page, "score": score, "text": sentence})
        if len(selected) >= limit:
            break
    return selected


def keyword_counts(text: str, limit: int = 30) -> list[dict]:
    stop = {
        "about", "after", "also", "among", "because", "been", "before", "being", "between",
        "both", "could", "does", "each", "from", "have", "into", "more", "most", "other",
        "paper", "results", "show", "shown", "such", "than", "that", "their", "there", "these",
        "they", "this", "through", "using", "were", "which", "while", "with", "would",
    }
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text.lower())
    counts = Counter(word for word in words if word not in stop)
    return [{"term": term, "count": count} for term, count in counts.most_common(limit)]


def extract_one(paper: Paper) -> dict:
    actual_hash = sha256_file(paper.local_path)
    if actual_hash != paper.expected_sha256:
        raise ValueError(f"{paper.paper_id}: SHA-256 mismatch")

    reader = PdfReader(str(paper.local_path), strict=False)
    if reader.is_encrypted:
        reader.decrypt("")
    page_texts: list[str] = []
    page_chars: list[int] = []
    errors: list[dict] = []
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = normalize_text(page.extract_text() or "")
        except Exception as exc:  # extraction evidence must retain per-page failure
            text = ""
            errors.append({"page": page_number, "error": f"{type(exc).__name__}: {exc}"})
        page_texts.append(text)
        page_chars.append(len(text))

    marked = page_marked_text(page_texts)
    text_path = CORPUS_ROOT / f"{paper.paper_id}.txt"
    text_path.write_text(marked, encoding="utf-8")
    sections = {
        name: excerpt
        for name, pattern in SECTION_PATTERNS.items()
        if name != "references" and (excerpt := section_excerpt(marked, pattern))
    }
    pages_with_text = sum(chars >= 80 for chars in page_chars)
    digest = {
        "id": paper.paper_id,
        "category": paper.category,
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "relation": paper.relation,
        "prior_relevance_en": paper.why_en,
        "prior_relevance_th": paper.why_th,
        "source_pdf": paper.local_path.relative_to(ROOT).as_posix(),
        "sha256": actual_hash,
        "page_count": len(reader.pages),
        "pages_with_text": pages_with_text,
        "text_coverage": round(pages_with_text / max(1, len(reader.pages)), 4),
        "characters": sum(page_chars),
        "words": len(re.findall(r"\b\w+\b", marked)),
        "likely_scanned": pages_with_text / max(1, len(reader.pages)) < 0.75,
        "page_character_counts": page_chars,
        "extraction_errors": errors,
        "sections": sections,
        "evidence_sentences": sentence_candidates(page_texts),
        "keywords": keyword_counts(marked),
        "full_text_path": text_path.relative_to(ROOT).as_posix(),
    }
    (CORPUS_ROOT / f"{paper.paper_id}.json").write_text(
        json.dumps(digest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return digest


def public_record(record: dict) -> dict:
    result = {key: record[key] for key in PUBLIC_RECORD_FIELDS}
    result["section_headings"] = sorted(record.get("sections", {})) or record.get("section_headings", [])
    result["evidence_pages"] = sorted(
        {entry["page"] for entry in record.get("evidence_sentences", [])}
    ) or record.get("evidence_pages", [])
    return result


def write_reading_manifest(records: list[dict]) -> None:
    library = json.loads(LIBRARY_MANIFEST.read_text(encoding="utf-8"))["papers"]
    public_records = [public_record(record) for record in records]
    for record in public_records:
        source = library[record["id"]]
        metadata = source.get("metadata", {})
        record["bibliography"] = {
            "venue": metadata.get("venue"),
            "doi": metadata.get("doi"),
            "arxiv_id": metadata.get("arxiv_id"),
            "landing_url": metadata.get("landing_url"),
            "download_url": source.get("download_url"),
        }
    payload = {
        "version": 1,
        "work_item": 146,
        "scope": "Every PDF present in papers/ at extraction time",
        "paper_count": len(public_records),
        "papers": public_records,
    }
    READING_MANIFEST.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def extract_all(workers: int) -> list[dict]:
    papers = load_papers()
    CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    READING_ROOT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        records = list(executor.map(extract_one, papers))
    records.sort(key=lambda item: item["id"])
    write_reading_manifest(records)
    return records


def compact_existing_manifest() -> list[dict]:
    payload = json.loads(READING_MANIFEST.read_text(encoding="utf-8"))
    records = payload["papers"]
    write_reading_manifest(records)
    return json.loads(READING_MANIFEST.read_text(encoding="utf-8"))["papers"]


def iter_pdf_paths() -> Iterable[Path]:
    return sorted((ROOT / "papers").rglob("*.pdf"))


def validate_inventory(records: list[dict]) -> list[str]:
    errors: list[str] = []
    actual = {path.relative_to(ROOT).as_posix() for path in iter_pdf_paths()}
    recorded = {item["source_pdf"] for item in records}
    if actual != recorded:
        errors.append(f"PDF inventory mismatch: missing={sorted(actual-recorded)}, extra={sorted(recorded-actual)}")
    return errors


def validate_reports(records: list[dict]) -> list[str]:
    errors = validate_inventory(records)
    report_root = READING_ROOT / "by_paper"
    required_en = (
        "## Research question",
        "## Method and evidence",
        "## Principal findings",
        "## Limitations and transfer boundary",
        "## Connection to Formula Ultimate",
        "## Recommended project changes",
        "## Reading evidence",
    )
    required_th = (
        "## คำถามวิจัย",
        "## วิธีและหลักฐาน",
        "## ผลสำคัญ",
        "## ข้อจำกัดและขอบเขตการถ่ายโอน",
        "## ความเชื่อมโยงกับ Formula Ultimate",
        "## ข้อเสนอปรับปรุงโครงการ",
        "## หลักฐานการอ่าน",
    )
    for item in records:
        en = report_root / f"{item['id']}_review.md"
        th = report_root / f"{item['id']}_review.th.md"
        if not en.is_file() or not th.is_file():
            errors.append(f"{item['id']}: missing bilingual report pair")
            continue
        en_text = en.read_text(encoding="utf-8")
        th_text = th.read_text(encoding="utf-8")
        for heading in required_en:
            if heading not in en_text:
                errors.append(f"{en.name}: missing {heading}")
        for heading in required_th:
            if heading not in th_text:
                errors.append(f"{th.name}: missing {heading}")
        if f"English source: `{en.name}`" not in th_text:
            errors.append(f"{th.name}: missing English source declaration")
        if item["sha256"] not in en_text or item["sha256"] not in th_text:
            errors.append(f"{item['id']}: source hash not recorded in both reports")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract and validate the Formula Ultimate paper corpus")
    parser.add_argument("--extract", action="store_true", help="extract every local PDF and write reading manifest")
    parser.add_argument("--compact-manifest", action="store_true", help="remove source-text excerpts from an existing manifest")
    parser.add_argument("--validate-reports", action="store_true", help="validate report coverage and structure")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    if args.extract:
        records = extract_all(max(1, args.workers))
    elif args.compact_manifest:
        records = compact_existing_manifest()
    else:
        records = json.loads(READING_MANIFEST.read_text(encoding="utf-8"))["papers"]

    errors = validate_reports(records) if args.validate_reports else validate_inventory(records)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"Validated {len(records)} PDFs; "
        f"pages={sum(item['page_count'] for item in records)}; "
        f"words={sum(item['words'] for item in records)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
