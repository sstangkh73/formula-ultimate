"""Non-destructive protocol probe for the local Formula Ultimate MCP stack."""

from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client


BOX_CODE = """import cadquery as cq
result = cq.Workplane("XY").box(10, 20, 30)
"""


def tool_names(response: object) -> list[str]:
    return sorted(tool.name for tool in response.tools)


async def probe_session(
    session: ClientSession,
    call_inspect: bool,
    render_output: Path | None = None,
) -> dict[str, object]:
    initialized = await session.initialize()
    tools = await session.list_tools()
    evidence: dict[str, object] = {
        "server_name": initialized.serverInfo.name,
        "server_version": initialized.serverInfo.version,
        "tools": tool_names(tools),
    }
    if call_inspect:
        inspection = await session.call_tool("inspect", {"code": BOX_CODE})
        evidence["inspect_is_error"] = bool(inspection.isError)
        evidence["inspect_text"] = [
            item.text for item in inspection.content if hasattr(item, "text")
        ]
    if render_output:
        rendering = await session.call_tool(
            "render", {"code": BOX_CODE, "view": "isometric"}
        )
        images = [item for item in rendering.content if hasattr(item, "data")]
        if not images:
            raise RuntimeError("render returned no image content")
        image_bytes = base64.b64decode(images[0].data)
        render_output.parent.mkdir(parents=True, exist_ok=True)
        render_output.write_bytes(image_bytes)
        evidence["render_is_error"] = bool(rendering.isError)
        evidence["render_mime_type"] = images[0].mimeType
        evidence["render_bytes"] = len(image_bytes)
        evidence["render_sha256"] = hashlib.sha256(image_bytes).hexdigest().upper()
    return evidence


async def probe_stdio(
    command: str,
    arguments: list[str],
    call_inspect: bool,
    render_output: Path | None,
) -> dict[str, object]:
    parameters = StdioServerParameters(command=command, args=arguments)
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            return await probe_session(session, call_inspect, render_output)


async def probe_http(url: str) -> dict[str, object]:
    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            return await probe_session(session, False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    subparsers = parser.add_subparsers(dest="transport", required=True)

    stdio = subparsers.add_parser("stdio")
    stdio.add_argument("--command", required=True)
    stdio.add_argument("--arg", dest="arguments", action="append", default=[])
    stdio.add_argument("--inspect-box", action="store_true")
    stdio.add_argument("--render-output", type=Path)

    http = subparsers.add_parser("http")
    http.add_argument("--url", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.transport == "stdio":
        evidence = asyncio.run(
            probe_stdio(
                args.command,
                args.arguments,
                args.inspect_box,
                args.render_output,
            )
        )
    else:
        evidence = asyncio.run(probe_http(args.url))

    output = json.dumps(evidence, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
