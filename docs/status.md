# 当前状态

更新时间：2026-07-27

## 当前决策

1. 每章使用 notebook 作为唯一阅读入口。
2. 章节目录不再保留 `README.md`。
3. 根目录 `README.md` 只做索引。
4. `notes.md` 只放草稿、调研、临时想法。
5. `examples/` 和 `tests/` 只在需要工程化复用时添加。
6. 第 1 至 12 章以学透单项技术为主，每章选择最适合当前概念的案例。
7. 产研协作助手是第 13 章综合项目，不再要求第 3 至 12 章逐章增加产品功能。
8. 前置章节可以说明当前技术与最终项目的关系，但不为项目强行引入业务对象和状态。
9. 默认采用技术教程结构：结论与目标、背景、术语、参与者、原理、时序、渐进实验、工程边界和小结。
10. 保留论文式树形标题、统一名词、顺序引用和参考文献，不强制摘要、关键词和研究方法等论文栏目。
11. 代码用于观察底层协议；正文必须在代码前交代原因、逻辑、参与者、数据流和时序。
12. 第 8 章只讲单 Agent Planning，不引入多 Agent。
13. 核心课程在第 13 章结束；第 14 章作为独立行业扩展，不属于核心课程依赖。
14. PydanticAI 与 LangChain/LangGraph、AutoGen 等框架统一在第 11 章比较。
15. 第 9 章把 Agent Skills 与 Agent-facing CLI 作为两个独立知识点讲解，章末再说明可选组合；CLI 指面向 Agent 暴露 Web、桌面应用或业务 API 的结构化命令接口，不讲 Linux 基础命令。
16. 第 10 章独立讲 Harness Engineering，不并入 Skill / CLI 或框架章。
17. 仓库名和 Python 项目名使用 `ai-agent-cookbook`，正式书名使用
    `AI Agent Engineering Cookbook`，中文副标题为“从基础原理到生产级智能体系统”。

完整设计见 [roadmap.md](roadmap.md)。

写作规范详见 [writing-guide.md](writing-guide.md)。

## 已完成

1. 创建仓库骨架。
2. 创建 14 个章节目录。
3. 14 章均已创建 `notebooks/*.ipynb`。
4. 删除章节 `README.md`。
5. 第 1 章内容已合并到 notebook：
   `chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro.ipynb`
6. 第 1 章包含：
   - AI Agent 工程全景图（主运行链、Harness 边界、框架与供给生态）
   - Tokenization、LLM、RAG、Skills、MCP、CLI、Agent Loop 和 Harness 的职责边界
   - 模型、框架、协议、平台、算力、完整 Coding Agent 和多模态能力的七层分类
   - 20 余个代表性 Agent 框架 / SDK 的分类索引：图与状态、类型化 SDK、RAG / Pipeline、多 Agent、厂商 ADK、TypeScript 和长期记忆
   - LangGraph、CrewAI、AutoGen、AG2 与 Microsoft Agent Framework 的定位和演进说明
   - Claude Code、Codex、OpenCode 等 Coding Agent 产品的共同骨架
   - Hugging Face、阿里云百炼、火山方舟、GLM 开放平台、AutoDL、可灵和 GigaTok 的生态定位
   - 常见系统类型、工程师能力结构和课程章节导航
   - minimal planner 代码实验
   - Planner 失败模式与 Agent 工程边界
   - 上线检查项
   - 常见误区
   - 顺序引用和参考文献
7. 更新文档：
   - `README.md`
   - `docs/roadmap.md`
   - `docs/writing-guide.md`
   - `docs/publishing-guide.md`
   - `docs/notebook-template.md`
8. 第 2 章已写成可运行草稿：
   `chapters/02-llm-basics/notebooks/02-llm-basics.ipynb`
9. 第 2 章包含：
   - 结论
   - 必备概念
   - tokenization 实验
   - next-token prediction 实验
   - temperature sampling 实验
   - attention 权重实验
   - Q/K/V 对照解释
   - attention 到 next token 的生成演示
   - 逐 token 自回归生成演示
   - 训练 step / epoch / loss 演示
   - token ID、Embedding、位置编码和 Transformer 数据流
   - causal mask、prefill、decode、KV Cache
   - 用户输入编码到输出 token 的完整链路
   - 使用训练后参数连续生成 token
   - batch、checkpoint、训练阶段和模型产物
   - 按优先级裁剪上下文
   - Transformer 工程理解
   - 上下文窗口
   - 幻觉来源
   - 本章要点
10. 第 3 章产研协作助手 V0 已完成：
   `chapters/03-prompt-engineering/notebooks/03-prompt-engineering.ipynb`
11. 第 3 章当前包含：
   - 论文题目、摘要和关键词
   - 引言、研究问题和研究方法
   - Prompt 定义与生成机制
   - 指令层级与数据边界
   - Prompt 七要素协议
   - 测试驱动的提示词工程工作流
   - Prompt、代码、RAG、工具和微调的能力边界
   - GB/T 7714—2015 格式参考文献
   - Prompt 七要素模板与消息构建代码
   - 静态指令和动态输入分离
   - OpenAI-compatible API 适配层
   - 弱 Prompt / 强 Prompt 本地对照
   - Zero-shot / Few-shot 对照
   - 思维链、分析检查清单与 Self-Consistency 适用边界
   - 长上下文位置效应与 `Lost in the Middle`
   - OpenAI-compatible API 参数速查
   - Prompt Injection 攻击与输入隔离实验
   - 分步分析对需求完整度的固定回放实验
   - Prompt、JSON Mode、Strict JSON Schema 与本地校验的四层约束
   - `ProjectContext`、`Requirement` 和当前问题输入协议
   - `analysis_status`、需求摘要、范围、验收标准、风险、待确认问题和建议动作输出协议
   - JSON Schema Draft 2020-12 产研需求分析协议
   - OpenAI 与阿里云百炼的结构化输出配置差异
   - 拒答、截断、空响应、解析失败和 Schema 失败处理
   - 失败类型与恢复动作映射
   - normal、boundary、adversarial 三类评测数据
   - JSON、字段、Schema、标签、缺失项和整例六项指标
   - Prompt v1 / v2 固定回放与确定性评分器
   - Prompt Regression、修复样例和指标变化对比
   - 最低指标与 blocker 回退双重发布门禁
   - 失败类型、输入类别和严重级别统计
   - OpenAI-compatible 真实模型批量评测入口
   - 固定回放实验结果与结论边界
   - Prompt 生产版本记录与内容哈希
   - 发布流程、研究局限与结论
   - V0 能力边界：无工具、无 RAG、无历史对话、无长期记忆

## 已验证

1. 14 个 notebook JSON 合法，cell ID 均存在且在各自 notebook 内唯一。
2. 第 1 章 notebook 代码单元可顺序执行。
3. 第 1 章断言通过。
4. 旧的章节 README 引用已清理。
5. 旧的脚本入口 `minimal_planner.py` 已移除。
6. 第 2 章 notebook JSON 合法。
7. 第 2 章 notebook 代码单元可顺序执行。
8. 第 2 章断言通过。
9. 第 3 章第一部分 notebook JSON 合法。
10. 第 3 章标题层级、正文引用和参考文献编号已检查。
11. 第 3 章最终稿的 29 个代码单元可顺序执行，执行结果为 0 个异常。
12. 第 3 章真实模型调用默认关闭，Notebook 验证不会产生 API 请求。
13. 第 3 章共 89 个单元，cell ID 合法且唯一；29 个代码单元中有 28 个保存离线学习输出，不包含真实 API 响应和 Key。
14. 第 3 章参考文献编号 `[1]` 至 `[17]` 连续，正文引用已检查。
15. 第 3 章未发现重复长句和约定禁用表达。
16. 第 4 章 Function Calling 技术教程已按新路线重写：
   `chapters/04-tool-calling/notebooks/04-tool-calling.ipynb`
17. 第 4 章当前包含：
   - 三秒内可读的结论和学习目标
   - 大模型需要计算、实时数据、私有数据和外部动作的原因
   - 自然语言到程序参数的转换过程
   - Function、Tool、Tool Schema、Tool Call、Tool Result 和 Tool Calling Loop 统一定义
   - 用户、模型、应用程序和工具函数的职责边界
   - 完整 Mermaid 时序图与四份关键协议数据
   - 模型根据工具名称、说明和参数 Schema 选择工具的原理
   - Chat Completions 与 Responses API 的背景、位置和字段对照
   - 加法器最小实验：函数、Schema、Tool Call、校验、执行、Tool Result 和消息历史
   - 最小实验各代码单元独立准备输入，重启 Kernel 后可单独运行
   - 天气工具与加法工具的 DeepSeek 真实双工具调用实验
   - tool_choice、并列调用和数据依赖
   - 参数校验、工具白名单、读写操作差异、幂等、权限和工具结果注入
   - 11 类常见踩坑及请求、响应、参数、执行、关联、历史和终止排查顺序
   - 按协议、API、DeepSeek、Schema、Agent Loop 和评测分类的扩展阅读
   - 当前技术与最终产研协作助手的简短关系说明
   - `.env`、Shell 环境变量和 API Key 防泄露说明
18. 第 4 章共 59 个单元，13 个代码单元；最长代码单元 34 行。
19. 第 4 章 cell ID 合法且唯一；发布版保存离线学习输出，不包含真实 API 响应和 Key。
20. `.env.example` 不含 Key，`.env` 已被 Git 忽略。
21. `pyproject.toml` 和 `uv.lock` 已声明 `openai`、`jsonschema`、`python-dotenv` 依赖。
22. DeepSeek 已作为默认实测服务加入：支持 `DEEPSEEK_API_KEY`、`https://api.deepseek.com` 和 `deepseek-v4-flash` / `deepseek-v4-pro`。
23. 第 4 章已使用 `deepseek-v4-pro` 完成真实双工具调用：
   - 第一轮同时选择 `get_weather` 和 `add_numbers`
   - 参数分别为 `city="北京"` 与 `a=12345, b=67890`
   - 应用程序回传 2 个独立 Tool Result
   - 第二轮回答同时使用天气结果和加法结果
   - 真实 API 原始响应未保存在 Notebook 最终文件中，Key 未输出
24. 第 4 章参考文献编号 `[1]` 至 `[9]` 连续。
25. 工程基础设施整理完成（2026-07-11）：
   - `AGENTS.md` 重构为纯 Agent Protocol（启动流程、SSOT Map、Contract、DoD、禁止事项、输出格式、冲突仲裁）
   - `README.md` 去重，增加文档导航表
   - `docs/status.md` 去重，写作规范指向 `writing-guide.md`
   - `docs/writing-guide.md` 去重，结构模板指向 `notebook-template.md`
   - `docs/notebook-template.md` 补充论文体结构（原在 writing-guide.md）
   - `scripts/` 目录创建（4 个 CI 脚本骨架）
26. 第 3 章已迁移为产研协作助手 V0（2026-07-11）：
   - 旧案例已全部替换为站内消息通知需求分析
   - 固定 8 条 normal、boundary、adversarial 评测样例及稳定 ID
   - 29 个代码单元顺序执行，0 个异常，全部断言通过
   - 真实模型调用默认关闭，执行过程未发送 API 请求
27. 第 3 章 5.3 确定性评分器已完成可读性重构（2026-07-11）：
   - 增加评分流程、输入输出和通过标准的文字说明
   - 固定回放、本地准备、单条评分、批量评分和指标汇总分步展示
   - 评分器在本节重新定义解析、校验和集合比较函数，只复用正式 V0 Schema
28. 第 3 章提示技术与安全边界已补充（2026-07-11）：
   - 新增 CoT、Self-Consistency、长上下文位置效应和 API 参数说明
   - 将原输入边界实验扩展为 Prompt Injection 攻击与隔离验证
   - 新增分步分析检查清单的固定回放实验
   - 增加内容安全与 Moderation API 的后续路标
29. 第 5 章 MCP 技术教程已完成（2026-07-12）：
   `chapters/05-mcp/notebooks/05-mcp.ipynb`
30. 第 5 章包含：
   - 三秒可读的结论和学习目标
   - 多客户端重复适配的工程背景
   - Host、Client、Server、Tool、Resource、Prompt、Transport、JSON-RPC 统一定义
   - 参与者关系图与完整 Mermaid 时序图
   - 时序图显式声明全部参与者；状态图使用 ASCII ID 与基础 Mermaid 语法
   - 生命周期状态图和传输层对比
   - Tools、Resources、Prompts 三种原语的协议结构与适用场景
   - 协议消息速查表（8 个核心方法）
   - 本地 Tool Calling 与 MCP 对照实验（同一查询、同一函数实现）
   - Tool Schema 硬编码 vs tools/list 协议发现对比
   - 传输层、Server 发现、错误处理、权限和结果截断 5 项工程边界
   - 6 条常见误区
   - MCP 与 Function Calling 的层次区分和协作方式
   - MCP 热度与采用分化的客观分析
   - 检查清单：什么时候该用 MCP
   - 与产研协作助手的关系说明
31. 第 5 章共 51 个单元，8 个代码单元；全部可顺序执行，0 个异常。
32. 第 5 章 cell ID 合法且唯一；保存离线学习输出，不包含 API Key。
33. 第 5 章配套文件：
   - `chapters/05-mcp/examples/tool_functions.py` — 三个纯 Python 工具函数
   - `chapters/05-mcp/examples/mcp_server.py` — 最小 MCP Server
   - `chapters/05-mcp/examples/demo_repo/` — 模拟仓库
34. `pyproject.toml` 已新增 `mcp` 依赖。
35. 第 6 章 RAG 技术教程已按单一应用主线重构（2026-07-14）：
    `chapters/06-rag/notebooks/06-rag.ipynb` 以“萤火平台内部文档问答”为贯穿场景，使用本机 Ollama `qwen3-embedding:0.6b` 运行真实语义检索，按关键词 RAG 闭环、失败观察、Embedding、Hybrid/RRF、Rerank、Chunk、ACL、评测和生产索引逐步展开。
36. `pyproject.toml` 已新增 `chromadb`、`sentence-transformers`、`jieba`、`rank-bm25` 依赖。
37. 第 7 章 notebook JSON 合法，46 个 cell ID 唯一。
38. 第 7 章 18 个代码单元可顺序执行，0 个异常。
39. 第 7 章真实模型调用默认关闭（`RUN_LOCAL_LLM=0`），Notebook 验证不产生 API 请求。
40. 第 7 章 Context / Memory 技术教程已完成（2026-07-15）：
    `chapters/07-context-memory/notebooks/07-context-memory.ipynb`，46 个单元（28 MD + 18 CODE）。
41. `pyproject.toml` 已新增 `tiktoken` 依赖。
42. 第 7 章包含：上下文装配器、六种短期策略、Compaction 管理器、长期记忆生命周期、
    Checkpoint 恢复、SQLite 多用户数据模型、Local-first 架构、持久化选型、
    小上下文实验、生产 Trade-off、故障安全与评测，以及“大内容落盘、摘要常驻、按需回读”的设计思考。
43. 课程路线新增两个独立技术章节（2026-07-15）：
    - 第 9 章：Agent Skills 与 Agent-facing CLI
    - 第 10 章：Harness Engineering
44. 原框架、生产控制、Capstone 和行业扩展顺延为第 11 至 14 章；第 13 章当前只完成提纲和占位 notebook，未开始正文实现。
45. 第 13 章占位 notebook 已顺序执行，0 个异常，不包含真实 API 调用。
46. 第 8 章 Agent Planning 与执行循环技术教程已完成（2026-07-16）：
    `chapters/08-agent-loop/notebooks/08-agent-loop.ipynb`，67 个单元（51 MD + 16 CODE）。
47. 第 8 章包含：Planning 适用条件、ReAct 运行机制和课程归属、Plan-and-Solve、Plan 数据协议、
    DAG 依赖调度、单 Agent plan-act-observe 循环、ReAct 执行轨迹、错误分类、动态重规划、
    独立 Verifier、预算与停止条件、Checkpoint 恢复、幂等和人工介入，以及 ReWOO、Reflexion、
    Tree of Thoughts 扩展阅读。
48. 第 8 章 16 个代码单元可顺序执行，0 个异常；ReAct 轨迹、无计划失败、重规划成功、
    预算耗尽和中断恢复路径均有断言。
49. 第 8 章真实 Planner 使用现有 DeepSeek/OpenAI-compatible 配置完成过一次端到端验证；发布版以
    `RUN_LIVE_LLM=0` 重新执行，未保存真实 API 响应和 Key。
50. 第 8 章 6.7 的金额规则改为由 `check_rule(row, rule_name)` 统一判断；规则名通过
    `match/case` 分发，清洗和校验复用同一判断，未引入通用操作符规则引擎。
51. 第 8 章环境变量加载已与第 3、4 章统一：使用 `find_dotenv(usecwd=True)` 定位根目录
    `.env`，使用 `load_dotenv(..., override=False)` 保持进程环境变量优先，并输出不含 Key 的配置诊断。
52. 第 8 章 7.1 使用 `baoyu-article-illustrator` 增加重规划流程配图，明确标出
    `validate_v1` 失败、进入 `Plan Patch`、插入去重与二次校验步骤、重接审计依赖的完整路径。
53. 第 8 章 `replan_after_failure` 已补充逐段中文注释，解释错误筛选、重规划预算、
    `next(...)` 查找步骤、追加修复步骤、重接依赖、记录 Plan Patch 和计划校验。
54. 第 9 章 Agent Skills 与 Agent-facing CLI 技术教程已完成（2026-07-17）：
    `chapters/09-agent-skills-cli/notebooks/09-agent-skills-cli.ipynb`，81 个单元（55 MD + 26 CODE）。
55. 第 9 章将两个知识点分开讲解：CLI 部分包含输入输出契约、Schema 自省、JSON/NDJSON、
    退出码、OAuth、多账户、分页、dry-run、幂等、冲突、Web/API 改造和 Google Workspace CLI；
    Skill 部分包含编写、静态校验、安装、发现、显式/隐式触发、渐进加载、Script、Reference、
    Asset、Observation、Evals、迭代、版本、分发、禁用和供应链安全。
56. CLI 使用团队日历 REST 服务离线实现 `workcli`；Skill 使用独立的需求文档审查案例，安装三个
    候选 Skill，并通过现有 DeepSeek/OpenAI-compatible 配置真实验证模型路由、资源选择和最终审查。
57. 第 9 章 26 个代码单元可顺序执行，0 个异常；真实生命周期 3 次模型调用通过，三组真实触发
    评测全部通过；发布版以 `RUN_LIVE_LLM=0`、`RUN_LIVE_EVAL=0` 重新执行，未保存 API 响应和 Key。
58. 第 10 章 Agent Harness Engineering 技术教程已完成（2026-07-17，2026-07-23 补充）：
    `chapters/10-harness-engineering/notebooks/10-harness-engineering.ipynb`，68 个单元（49 MD + 19 CODE）。
59. 第 10 章按照 What、Why、Integration、How、When 展开，包含 Harness 定义与背景、职责边界、
    Brain/Hands/Session、Thread/Run/Turn/Item/Event、完整时序、Context Builder、Policy、Tool Runtime、
    Event Store、Artifact Store、Supervisor、Verifier、多 Tool Call 批次语义、跨系统事务、Saga、
    生产选型和上线检查表。
60. 第 10 章使用跨文件价格 API 迁移贯穿实验，稳定复现裸循环提前完成、大输出落盘、路径越界拒绝、
    崩溃窗口、幂等回执、预算取消、Checkpoint 恢复和独立验收。
61. 第 10 章已使用现有 DeepSeek/OpenAI-compatible 配置完成真实 Harness 验证：模型自主搜索、读取、
    修改和测试，最终 5 轮模型调用、13 次工具调用，测试通过且 `legacy_price` 引用清零。
62. 真实循环区分 API `tool_call.id` 与 Harness 稳定 `action_id`，工具通过 Receipt Store 幂等执行；
    发布版将以 `RUN_LIVE_LLM=0` 顺序执行，不保存真实 API 响应和 Key。
63. 第 11 章 Agent Frameworks 技术教程已完成（2026-07-17，2026-07-23 重构案例）：
    `chapters/11-frameworks/notebooks/11-frameworks.ipynb`，86 个单元（64 MD + 22 CODE）。
64. 第 11 章从编程模型、运行时和集成层解释框架内核，按模型驱动、工作流驱动和混合控制分类，
    对照 PydanticAI、OpenAI Agents SDK、Google ADK、Strands、LangGraph、LlamaIndex、CrewAI、
    Microsoft Agent Framework、Dify 和 Coze Studio，并选择三个代表框架深入实验。
65. 第 11 章使用“共享测试环境部署申请”统一实验，先说明合并代码、触发流水线、Runner 部署和
    生产发布的动作边界，再定义开发人员、Agent、Team Leader、Runner 和运维的权限；Agent 只读取
    PR、CI、环境证据并创建测试任务，不持有生产凭据。
66. 第 11 章保留三套可选 DeepSeek/OpenAI-compatible 真实实验入口：PydanticAI 使用
    `PromptedOutput`，LangGraph 使用 JSON Mode、本地 Pydantic 校验和有界重试，Microsoft Agent
    Framework 使用工具调用和双 Agent Workflow。旧案例曾完成真实协议验证；本次案例重构未重新
    发送外部数据，发布版仅保存 `RUN_LIVE_LLM=0` 的离线输出。
67. 第 11 章使用内存字典模拟 PR API、CI API、环境注册表、审批回调和测试部署队列，无需搭建
    GitLab、Jenkins、Kubernetes 或审批系统；统一业务内核覆盖 CI 失败、Commit 不一致、环境占用、
    数据库迁移审批、拒绝、恢复和幂等入队。
68. PydanticAI 实验验证依赖注入、工具轨迹和类型化输出；LangGraph 验证 State、条件边、
    Interrupt、Checkpoint History 和恢复；Microsoft Agent Framework 验证 Executor、Workflow、
    类型化人工请求和 Agent 串联。三者共用同一数据协议、准入函数、入队函数和验收标准。
69. 第 11 章记录了 Provider 能力矩阵、框架重试与副作用、状态迁移、多租户、隐式 Prompt、
    多 Agent Token 成本、选型 PoC 和生产 Trade-off；新增并锁定 `pydantic-ai`、`langgraph`、
    `langchain-openai` 与三个 `agent-framework-*` 最小子包依赖。
70. 第 11 章 22 个代码单元已在 `RUN_LIVE_LLM=0` 下顺序执行，0 个异常；最终 Notebook
    不保存真实 API 响应或密钥，86 个 cell ID 合法且唯一，参考文献编号 `[1]` 至 `[16]` 连续。
71. 第 10 章 7.3 已补充同一轮多 Tool Call 的执行语义（2026-07-23）：全只读批次使用
    `BEST_EFFORT_READS`，包含写入或检查的批次使用 `ORDERED_FAIL_FAST`；前序动作失败后，
    剩余调用返回 `SKIPPED_PRIOR_ACTION_FAILED`，保持每个 `tool_call.id` 都有对应 Tool Result。
72. 第 10 章生产机制已补充跨系统判断与 Saga：使用事务控制权区分本地事务和跨系统操作，
    对照单库、支付 API、Kafka、Jira + 飞书、数据库 + 文件系统，并展示订单、库存、支付和物流
    失败后的补偿时序、幂等、Pivot、补偿失败和人工接管。
73. 第 10 章修改后共 19 个代码单元，已在 `RUN_LIVE_LLM=0` 下顺序执行，0 个异常；新增断言验证
    第一个写入失败后第二个写入被跳过，纯读取失败不阻断其他读取。本次真实 DeepSeek 回归因外部
    数据发送未获单独授权而未重新执行，Notebook 保留发布版离线输出。
74. 第 12 章 Agent 生产控制技术教程已完成（2026-07-27）：
    `chapters/12-evals-guardrails/notebooks/12-evals-guardrails.ipynb`，71 个单元（52 MD + 19 CODE）。
75. 第 12 章使用本地退款处理 Agent 贯穿，包含 Trace / Span / Event、脱敏与采样、黄金数据集、
    最终答案与工具轨迹评分、回归门禁、输入/知识/工具/输出 Guardrails、直接与间接 Prompt
    Injection、fail-open / fail-closed、人工审批、参数哈希、资源版本、审批过期、幂等恢复和完整批准路径。
76. 第 12 章固定 7 条 normal、boundary、adversarial 样例，先复现越权、超额、错误状态、
    直接注入和知识文档间接注入导致的危险副作用，再验证受控版本全部通过发布门禁。
77. 第 12 章 19 个代码单元已在 `RUN_LIVE_EVAL=0` 下顺序执行，0 个异常；71 个 cell ID
    合法且唯一，参考文献编号 `[1]` 至 `[9]` 连续，发布版不保存真实 API 响应或密钥。
78. 第 14 章行业 Agent 落地扩展教程已完成（2026-07-27）：
    `chapters/14-industry-cases/notebooks/14-industry-cases.ipynb`，61 个单元（47 MD + 14 CODE）。
79. 第 14 章从业务流程、证据、决策责任、错误成本和数据闭环筛选行业场景，区分普通软件、
    单次模型调用、RAG、专用模型和 Agent，并定义 Use Case Canvas、五级上线阶梯、团队角色、
    Data Sheet、Model Card、风险台账、评测报告和 Runbook。
80. 第 14 章包含客服质检、病历管理和车险理赔受理三个案例；车险实验使用纯合成数据，
    通用模型只提取事实，领域图像模型、RAG、规则、身份系统和理赔人员分别承担专业职责。
81. 第 14 章车险实验覆盖正常、缺材料、越权、伤人、车牌冲突和 Prompt Injection 六条分支；
    越权请求在授权阶段立即终止，所有分支均不自动定责、认定欺诈、拒赔或赔付。
82. 第 14 章 14 个代码单元已在 `RUN_LIVE_LLM=0` 下顺序执行，0 个异常；61 个 cell ID
    合法且唯一，参考文献编号 `[1]` 至 `[12]` 连续，发布版不保存真实 API 响应或密钥。
78. GitHub 发布前验证已完成（2026-07-27）：
    - 14 个 Notebook 均在真实调用关闭的条件下顺序执行，0 个异常。
    - 第 6 章新增 `RUN_LIVE_EMBEDDING=0` 默认保护；离线特征回放只验证索引、检索和评测管道，
      设置为 `1` 时才调用本机 Ollama，且调用失败时不会静默降级。
    - 发布文件未发现真实 API Key；`.env`、IDE 配置、Notebook checkpoint、PyCharm 支持库和
      嵌套 Git 元数据均已排除。
83. 第 1 章 AI Agent 工程全景已重构（2026-07-27）：总览 PNG 提升为 6400×4480，
    同时提供可缩放 SVG、6400×2540 主运行链放大图和 5333×1760 框架与供给生态放大图；
    覆盖 Tokenization、LLM、RAG、Skills、Loop、Harness、MCP、CLI、AutoGen、LangGraph、
    CrewAI、Hugging Face、GigaTok、豆包、可灵、GLM、百炼、Claude Code、Codex、OpenCode、
    AutoDL 等概念与产品；框架区扩展为 Python / 数据与状态、厂商 SDK / 通用编排、
    多 Agent / TypeScript / 专项三组，并按运行主链和生态层级建立关系。
84. 第 1 章共 28 个单元（23 MD + 5 CODE），cell ID 合法且唯一；5 个代码单元已顺序执行，
    0 个异常，全部断言通过；参考文献编号 `[1]` 至 `[35]` 连续，全景图通过 Archify
    `single_svg`、`finite_svg`、`orthogonal_arrows` 和 `legend_clearance` 检查。
85. 第 1 章课程导航已与 `README.md` 和 `docs/roadmap.md` 对齐（2026-07-27）：完整列出
    01 至 14 章的正式标题，明确第 13 章闭合核心依赖、第 14 章为独立行业扩展；Agent 框架索引
    补充 OpenAI Agents SDK、Claude Agent SDK、Google ADK、Strands、LlamaIndex、Haystack、
    smolagents、Agno、BeeAI、CAMEL、Mastra、Vercel AI SDK、Letta、Langroid、MetaGPT 等项目。

## 章节状态

| 章节 | 当前状态 | 后续要求 |
| --- | --- | --- |
| 01 | 草稿 | 按技术教程模板复查 |
| 02 | 草稿 | 保留 LLM 原理，不创建独立 Agent |
| 03 | 已完成待复查 | 保留 Prompt 技术内容，降低对最终项目的强绑定 |
| 04 | 技术教程已完成 | Function Calling 原理、渐进实验和真实调用 |
| 05 | 技术教程已完成 | MCP 原理、对比实验和工程边界 |
| 06 | 技术教程已完成 | RAG 原理、检索实验、生产架构与评测 |
| 07 | 技术教程已完成 | 独立讲透 Context / Memory |
| 08 | 技术教程已完成 | 独立讲透单 Agent Planning |
| 09 | 技术教程已完成 | Skill、Agent-facing CLI、认证授权和 Web/API 到 CLI 的改造 |
| 10 | 技术教程已完成 | Harness 定义、运行协议、权限、状态、恢复、验收和生产取舍 |
| 11 | 技术教程已完成 | 框架底层分类、PydanticAI、LangGraph、Microsoft Agent Framework 与生产选型 |
| 12 | 技术教程已完成 | Evals、Tracing、分层 Guardrails、HITL、发布门禁与生产取舍 |
| 13 | 提纲 | 综合实现产研协作助手 Capstone |
| 14 | 扩展教程已完成 | 行业选型、数据闭环、风险分级、三个案例与上线阶梯 |

## 下一步

1. 复查第四至十二章的发布阅读体验和图表渲染效果。
2. 设计并实现第十三章产研协作助手 Capstone。
3. 第十三章完成后执行全课程依赖、环境和发布检查。

## 第 2 章复查点

1. 文字密度是否合适。
2. 代码单元颗粒度是否适合阅读。
3. attention 实验已补 Q/K/V、权重计算、逐 token 生成过程。
4. 训练过程已补 step、epoch、loss、参数更新、推理生成区别。
5. 第 2 章重复内容已整理：实验 4 负责生成链路，实验 5 负责训练链路。
6. 实验 5 已补训练后参数续写，用于连接训练结果和推理过程。
7. Attention 已按位置保存权重，并修正最后位置 Query 的说明。
8. context window 实验已改为优先保留 system、当前问题和检索证据。
9. 第 2 章全部代码单元已补中文注释，复杂 Python 语法已说明阅读方式。

## 当前注意事项

1. 不要重新引入章节 README。
2. 不要先写发布稿。
3. 不要把 notebook 写成命令行教程。
4. 不要在第 2 章一开始引入复杂数学推导。
5. 第 2 章代码优先使用标准库。
