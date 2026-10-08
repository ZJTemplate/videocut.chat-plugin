"""Check an installed wheel over stdio MCP without credentials or rendering."""

import asyncio
import json
import sys
import tempfile
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def verify(config):
    params = StdioServerParameters(
        command=sys.executable,
        args=["-I", "-m", "saycut_tools.cli", "--config", str(config), "mcp"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            assert "saycut_keeper_status" in names
            for name, args in (
                ("saycut_capabilities", {}),
                ("saycut_keeper_status", {}),
                ("saycut_list_styles", {"limit": 3}),
                ("saycut_parse_subtitles", {
                    "content": "1\n00:00:00,000 --> 00:00:02,000\nHello world.\n",
                    "format": "srt",
                }),
            ):
                result = await session.call_tool(name, args)
                assert not result.is_error, (name, result)
                assert result.structured_content is not None, name
                print("Verified:", name)
            print("MCP version:", initialized.server_info.version, "tools:", len(names))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="videocut-mcp-check-") as directory:
        root = Path(directory)
        config = root / "saycut.json"
        config.write_text(json.dumps({
            "account_enabled": True,
            "data_dir": str(root / "data"),
            "allowed_roots": [str(root)],
            "asr_backend": "disabled",
        }))
        asyncio.run(verify(config))
