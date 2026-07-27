"""最小 MCP Server —— 把 tool_functions 中的三个函数暴露为 MCP Tools。

启动方式：
    uv run python chapters/05-mcp/examples/mcp_server.py

使用 stdio transport，与 MCP Client 通过标准输入输出通信。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tool_functions import read_file as _read_file
from tool_functions import search_text as _search_text
from tool_functions import repo_status as _repo_status

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

mcp = FastMCP("repo-analyzer")


@mcp.tool()
async def read_file(path: str) -> list[TextContent]:
    """读取仓库中指定路径的文件内容。path 相对于仓库根目录。"""
    # 不捕获异常——FastMCP 会捕获并以 isError=True 返回给 Client。
    content = _read_file(path)
    return [TextContent(type="text", text=content)]


@mcp.tool()
async def search_text(pattern: str) -> list[TextContent]:
    """搜索仓库所有文件中包含关键词的文本行。返回匹配列表。"""
    # 不捕获异常——FastMCP 会捕获并以 isError=True 返回给 Client。
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
    mcp.run(transport="stdio")
