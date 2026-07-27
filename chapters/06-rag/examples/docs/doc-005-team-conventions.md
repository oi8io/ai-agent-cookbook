# 萤火协作平台团队规范

## 分支命名

所有代码开发必须在 `feat` 分支完成，禁止直接在 `main` 或 `test` 上开发。

分支命名规则：

- 新功能：`feat-<简短描述>`，如 `feat-task-batch-import`
- 缺陷修复：`fix-<bug-id 或简短描述>`，如 `fix-upload-size-limit`
- 紧急修复：`hotfix-<描述>`

## Commit 格式

格式：`type(scope): message`

类型（type）：

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | 缺陷修复 |
| refactor | 重构 |
| docs | 文档更新 |
| test | 测试相关 |
| chore | 构建、依赖等杂项 |

示例：

```
feat(task): add CSV batch import for task list
fix(upload): increase attachment size limit from 10MB to 50MB
refactor(auth): extract token validation to middleware
```

## 代码审查

- 所有合并到 `main` 的 PR 必须至少 1 人 approve。
- 核心模块（认证、权限、支付）必须至少 2 人 approve。
- CI 全部通过后才能合并。
- 禁止强制推送 `main` 和 `test` 分支。

## 发布窗口

每周五 16:00 为常规发布窗口。紧急修复不受窗口限制，但需要项目负责人审批。

发布前 Checklist：

1. 所有关联任务状态已更新。
2. Changelog 已更新。
3. 发布说明已同步至「发布记录」文档。
4. 回归测试全部通过。
5. 数据库迁移脚本已准备并在预发布环境验证。

## 代码风格

- Python 遵循 PEP 8，使用 Ruff 格式化，行宽 100 字符。
- JavaScript/TypeScript 遵循 ESLint 推荐规则。
- 所有公开接口必须有 docstring。
