# AGENTS.md — Agent Protocol

> 本文件定义 AI Agent 操作本仓库的完整协议。
> Claude Code、Gemini、Codex、Copilot 及其他编码 Agent 在操作前必须先读取本文件。
> 本文件不包含课程介绍、目录结构、写作规范——这些信息应从各自的 SSOT 文件中获取。

---

## 1. Startup Flow

每次 Agent 启动或收到修改任务时，按以下顺序读取：

```
1. AGENTS.md（本文件）               — 知道规则
2. docs/status.md                    — 知道当前进度和上下文
3. README.md                         — 知道项目导航
4. docs/writing-guide.md             — 知道写作规范（仅在修改 notebook 时）
5. docs/notebook-template.md         — 知道结构模板（仅在新建 notebook 时）
```

**原则：只读你需要的信息，不要全部预加载。**

---

## 2. Pre-Modification Checklist

在对任何文件做修改之前：

- [ ] 已读 `docs/status.md`，确认当前进度和当前决策。
- [ ] 已确认目标文件属于哪个 SSOT 域（见下方 Contract）。
- [ ] 如果修改 notebook：已读 `docs/writing-guide.md`。
- [ ] 如果新建 notebook：已读 `docs/notebook-template.md`。

---

## 3. File Modification Rules

### 3.1 SSOT Map（改什么，去哪改）

| 要修改的信息 | 唯一文件 | 禁止修改的文件 |
|-------------|---------|---------------|
| 章节进度 / 状态 | `docs/status.md` | README, AGENTS |
| Notebook 结构模板 | `docs/notebook-template.md` | writing-guide, AGENTS |
| 写作规范 / 风格 | `docs/writing-guide.md` | status, AGENTS, README |
| 项目导航 / 目录树 | `README.md` | AGENTS, status |
| 路线图 | `docs/roadmap.md` | — |
| 发布工作流 | `docs/publishing-guide.md` | README |
| Agent 行为规则 | `AGENTS.md`（本文件） | — |
| 依赖 / 版本 | `pyproject.toml` | 任何 .md |
| 环境变量定义 | `.env.example` | AGENTS |
| 课程内容 | `chapters/XX-topic/notebooks/*.ipynb` | — |
| 草稿 / 调研 | `chapters/XX-topic/notes.md` | — |

### 3.2 Cascading Updates

某些修改需要同步更新多个文件。以下是完整的级联规则：

| 变更类型 | 必须同步更新 |
|---------|-------------|
| 章节状态变更（提纲→撰写中→已完成） | `docs/status.md` → `README.md` 目录表状态列 |
| 章节新增 / 重命名 / 删除 | `docs/status.md` → `README.md` 目录表 + 仓库结构图 |
| 写作规范变更 | `docs/writing-guide.md`，检查是否与 `notebook-template.md` 冲突 |
| 新增环境变量 | `.env.example`，在对应 notebook 中说明 |
| `.env.example` 新增变量 | 必须同步更新 `scripts/check_env.py` 的白名单 |

**级联原则：SSOT 先改，下游引用跟随。不允许改了 SSOT 不跟新下游。**

---

## 4. Repository Contract

以下契约对所有 Agent 具有强制约束力。

### Contract 1: Notebook is Content Truth

```
Notebook (.ipynb) = 教学内容的唯一事实源。

- 任何正文内容只存在于 notebook 中。
- 禁止在 notebook 之外创建正文文件。
- notes.md 仅允许放草稿、调研链接和临时笔记，不允许放正文。
- 章节目录禁止出现 README.md。
```

### Contract 2: status.md is State Truth

```
docs/status.md = 项目状态的唯一事实源。

- 章节进度、已完成事项、已验证事项、当前决策、下一步——只在这里维护。
- README 的目录状态列是 status.md 的只读投影，必须与 status.md 一致。
- AGENTS.md 不维护任何进度信息。
```

### Contract 3: README is Navigation Only

```
README.md = 项目导航入口。

- 提供目录表（含状态投影）、仓库结构图、写作原则摘要（≤5条）。
- 不维护进度详情、不维护写作规范全文、不维护 Notebook 结构说明。
- 所有详情通过链接指向对应 SSOT 文件。
```

### Contract 4: writing-guide.md is Style Truth

```
docs/writing-guide.md = 写作风格与代码规范的唯一事实源。

- 风格要求、禁用表达、代码要求、章节目录结构——只在这里维护。
- status.md 和 AGENTS.md 不重复写作规范。
```

### Contract 5: notebook-template.md is Structure Truth

```
docs/notebook-template.md = Notebook 结构的唯一事实源。

- 默认结构（工程笔记体）和论文体结构只在这里维护。
- writing-guide.md 只引用，不重复。
```

### Contract 6: Agent Must Not Violate Contracts

```
Agent 不得在任何情况下违反以上契约。
如果发现契约之间存在冲突，以冲突优先级表中定义的文件为准。
```

---

## 5. Definition of Done（章节完成标准）

一章从“提纲”变为“已完成”，必须通过以下所有检查项：

### A. 结构完整性

- [ ] **A1** Notebook JSON 合法（`json.load` 可解析）
- [ ] **A2** 所有 cell ID 唯一（无重复 `id` 字段）
- [ ] **A3** 包含所有必需节（按 notebook-template.md 对应结构）
- [ ] **A4** 标题层级正确（无跳级）
- [ ] **A5** 每节有实际内容（无空节占位）

### B. 代码质量

- [ ] **B1** 所有代码单元可顺序执行，0 异常
- [ ] **B2** 所有断言通过
- [ ] **B3** 代码包含中文注释
- [ ] **B4** 复杂 Python 语法有阅读说明注释
- [ ] **B5** 依赖全部在 `pyproject.toml` 中声明

### C. 内容质量

- [ ] **C1** 结论在章节开头给出
- [ ] **C2** 至少记录一个失败模式或边界条件
- [ ] **C3** 不包含禁用表达（见 writing-guide.md 禁用清单）
- [ ] **C4** 信息密度达标（无大段铺垫、无营销口吻）

### D. 安全与配置

- [ ] **D1** 真实模型调用默认关闭（`RUN_LIVE_LLM=0` 保护）
- [ ] **D2** 不存在硬编码 API Key
- [ ] **D3** 使用的所有环境变量已在 `.env.example` 中声明
- [ ] **D4** Notebook 源文件不保存 API 响应输出（cell output 不含 Key）

### E. 文档同步

- [ ] **E1** `docs/status.md` 已更新（章节状态 + 包含内容清单）
- [ ] **E2** `README.md` 目录表状态列已同步
- [ ] **E3** 如果新增依赖，`pyproject.toml` 和 `uv.lock` 已更新

### F. 论文体附加项

- [ ] **F1** 参考文献编号 `[1]` 至 `[N]` 连续无缺号
- [ ] **F2** 正文引用全部对应到参考文献
- [ ] **F3** 参考文献格式符合 GB/T 7714—2015
- [ ] **F4** 官方文档引用标注访问日期

---

## 6. Post-Modification Verification

每次修改 notebook 后，Agent 必须执行：

```bash
# 1. JSON 合法性
python -c "import json; json.load(open('chapters/XX-topic/notebooks/XX-topic.ipynb')); print('JSON OK')"

# 2. Cell ID 唯一性
python -c "
import json
nb = json.load(open('chapters/XX-topic/notebooks/XX-topic.ipynb'))
ids = [c['id'] for c in nb['cells']]
dups = [x for x in ids if ids.count(x) > 1]
assert not dups, f'Duplicate IDs: {set(dups)}'
print(f'OK: {len(ids)} cells, unique')
"

# 3. 顺序执行（无真实 API 调用）
uv run jupyter nbconvert --to notebook --execute --inplace \
  chapters/XX-topic/notebooks/XX-topic.ipynb
```

如果第 3 步触发真实 API 调用，说明 `RUN_LIVE_*` 保护未生效，必须修复。

---

## 7. Forbidden Actions

以下操作绝对禁止：

| 禁止操作 | 原因 |
|---------|------|
| 在章节目录创建 `README.md` | 违反 Contract 1 |
| 在 notebook 之外创建正文文件 | 违反 Contract 1 |
| 修改 notebook 后不更新 `docs/status.md` | 违反 Contract 2 |
| 在 `docs/status.md` 之外维护进度 | 违反 Contract 2 |
| 在 `docs/writing-guide.md` 之外维护写作规范 | 违反 Contract 4 |
| 提交 `.env` 文件 | 安全风险 |
| 在 notebook 中硬编码 API Key | 安全风险 |
| 先写发布稿再写 notebook | 违反工作流 |
| 把 notebook 写成命令行教程 | 违反写作规范 |
| 在 `main.py` 中添加业务逻辑 | main.py 是占位文件 |
| 在第 2 章开头引入复杂数学推导 | 违反写作规范 |
| 不关闭 `RUN_LIVE_*` 就提交 notebook | 浪费 API 额度 |

---

## 8. Output Format

Agent 完成任务后，报告必须包含：

```
## 完成摘要
- 修改了哪些文件
- 每个文件改了什么（≤1行描述）

## 验证结果
- [ ] JSON 合法
- [ ] Cell ID 唯一
- [ ] 顺序执行 0 异常
- [ ] docs/status.md 已同步
- [ ] README.md 状态列已同步（如适用）

## 未完成 / 已知问题
- （如有）
```

---

## 9. Conflict Resolution

当 Agent 发现两个 SSOT 文件描述不一致时，按以下优先级仲裁：

```
1. Notebook 正文内容 > 任何 .md 文件的描述
2. docs/status.md > README.md（进度与状态）
3. docs/writing-guide.md > 任何文件（写作规范）
4. AGENTS.md > 任何文件（Agent 操作行为）
5. pyproject.toml > 任何文件（依赖与版本）
6. .env.example > 任何文件（环境变量定义）
```

Agent 发现冲突时：**以高优先级文件为准，并主动修复低优先级文件使其一致。** 不要只报告不修复。
