# 调研笔记

## 2026-07-12

- MCP Python SDK 当前版本 1.28.1，使用 FastMCP + @mcp.tool() 装饰器模式。
- Server 端：`mcp.run(transport="stdio")`，无需手动管理 stdio_server 上下文。
- Client 端：`stdio_client(server_params)` + `ClientSession`，异步上下文管理器模式。
- 字段名使用 camelCase（`protocolVersion`、`serverInfo`、`inputSchema`）。
- `tools/call` 返回 `CallToolResult`，`content` 是 `TextContent` 列表。
- 注意：async tool 函数名不能与导入的 sync 函数名冲突（会覆盖导致递归）。
- 参考：https://modelcontextprotocol.io/specification
- 参考：https://github.com/modelcontextprotocol/python-sdk
