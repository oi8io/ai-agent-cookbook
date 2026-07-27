# 萤火协作平台 API 参考

## 认证方式

所有 API 请求需要在 Header 中携带 Bearer Token：

```
Authorization: Bearer <your_api_token>
```

Token 在「个人设置 → API Token」页面生成，有效期为 30 天。

## 速率限制

- 每个 Token 每小时最多 1000 次请求。
- 超出限制后返回 HTTP 429，Response Body 包含 `retry_after` 字段（单位：秒）。
- 批量导入接口不受速率限制。

## 分页

支持分页的接口统一使用以下参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | integer | 1 | 页码，从 1 开始 |
| `page_size` | integer | 20 | 每页条数，最大 100 |
| `sort_by` | string | `updated_at` | 排序字段 |
| `order` | string | `desc` | 排序方向，可选 `asc` 或 `desc` |

## 任务列表接口

### GET /api/v1/tasks

查询当前用户可见的任务列表。

**请求示例：**

```
GET /api/v1/tasks?page=1&page_size=20&status=open
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**响应字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 任务 ID |
| `title` | string | 任务标题 |
| `status` | string | `open` / `in_progress` / `resolved` / `closed` |
| `assignee` | string | 负责人用户名 |
| `priority` | string | `low` / `medium` / `high` / `critical` |
| `created_at` | string | 创建时间（ISO 8601） |
| `updated_at` | string | 更新时间（ISO 8601） |

### POST /api/v1/tasks

创建新任务。

**请求体：**

```json
{
  "title": "修复登录页样式错乱",
  "description": "在 Safari 17 下登录按钮位置偏移",
  "priority": "high",
  "assignee": "zhangsan"
}
```

## Webhook 回调

用户可以配置 Webhook 地址，平台在任务状态变更时发送 POST 通知。

**配置方式：**「项目设置 → Webhook → 添加回调地址」。

通知体格式：

```json
{
  "event": "task.updated",
  "task_id": "TASK-1234",
  "old_status": "open",
  "new_status": "in_progress",
  "timestamp": "2026-07-10T14:30:00Z"
}
```
