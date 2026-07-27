"""三个纯 Python 工具函数——不含任何 MCP 代码。

本地 Tool Calling（实验 3）和 MCP Server（实验 4）共享同一套函数体。
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent / "demo_repo"


def read_file(path: str) -> str:
    """读取仓库中指定路径的文件内容。

    参数 path 相对于仓库根目录。
    """
    resolved_root = REPO_ROOT.resolve()
    full_path = (REPO_ROOT / path).resolve()
    # 防止路径穿越：确保解析后的路径仍在仓库内
    if not full_path.is_relative_to(resolved_root):
        raise ValueError(f"路径超出仓库范围: {path}")
    if not full_path.is_file():
        raise FileNotFoundError(f"文件不存在: {path}")
    return full_path.read_text(encoding="utf-8")


def search_text(pattern: str) -> list[dict]:
    """搜索仓库中所有包含关键词的文本行。

    返回匹配行列表，每行包含文件路径、行号和内容。
    """
    matches = []
    for file_path in REPO_ROOT.rglob("*"):
        if not file_path.is_file():
            continue
        # 跳过 .git 目录
        if ".git" in file_path.parts:
            continue
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(lines, start=1):
            if pattern in line:
                matches.append(
                    {
                        "file": str(file_path.relative_to(REPO_ROOT)),
                        "line": line_no,
                        "content": line.strip(),
                    }
                )
    return matches


def repo_status() -> dict:
    """返回仓库当前状态：分支名、最新 commit hash 和消息。"""
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
        commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%H %s"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"branch": "unknown", "latest_commit": "git not available"}
    return {"branch": branch, "latest_commit": commit}
