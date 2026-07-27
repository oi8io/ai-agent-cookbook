"""最小 MCP HTTP Server —— 与 mcp_server.py 相同的工具，使用 Streamable HTTP 传输。

启动方式：
    uv run python chapters/05-mcp/examples/mcp_server_http.py

默认监听 http://localhost:8000/mcp。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tool_functions import read_file as _read_file
from tool_functions import search_text as _search_text
from tool_functions import repo_status as _repo_status

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

mcp = FastMCP("repo-analyzer-http")


@mcp.tool()
async def read_file(path: str) -> list[TextContent]:
    """读取仓库中指定路径的文件内容。path 相对于仓库根目录。"""
    content = _read_file(path)
    return [TextContent(type="text", text=content)]


@mcp.tool()
async def search_text(pattern: str) -> list[TextContent]:
    """搜索仓库所有文件中包含关键词的文本行。返回匹配列表。"""
    matches = _search_text(pattern)
    if not matches:
        return [TextContent(type="text", text=f'未找到包含 "{pattern}" 的行')]
    lines = [f"{m['file']}:{m['line']}: {m['content']}" for m in matches]
    return [TextContent(type="text", text="\n".join(lines))]


@mcp.tool()
async def repo_status() -> list[TextContent]:
    """获取仓库当前状态：分支名和最新 commit。"""
    status = _repo_status()
    return [
        TextContent(
            type="text",
            text=f"分支: {status['branch']}\n最新 commit: {status['latest_commit']}",
        )
    ]


if __name__ == "__main__":
    mcp.run(transport="streamable-http", mount_path="/mcp")
