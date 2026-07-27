# AI Agent Engineering Cookbook

一本以 Notebook 为阅读入口的 AI Agent 工程教程，中文副标题为“从基础原理到生产级智能体系统”。

目标：先分别学透 AI Agent 的核心技术，再在综合实践中实现服务产品、研发和测试协作的产研协作助手：

```text
LLM 原理
  -> Prompt
  -> Tool Calling
  -> MCP
  -> RAG
  -> Context / Memory
  -> Planning
  -> Agent Skills 与 Agent-facing CLI
  -> Harness Engineering
  -> Agent 框架
  -> 加入 Evals、Tracing、Guardrails 和人审
  -> 产研协作助手 Capstone
```

## 开始阅读

在线运行无需安装环境，直接从[第一章（Google Colab）](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro.ipynb)开始。Colab 运行环境是临时的；涉及 API Key、本地 Ollama 或其他外部服务时，仍需按对应章节完成配置。

本地阅读和运行：

```bash
uv sync
uv run jupyter lab
```

从[第一章 Notebook](chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro.ipynb)开始阅读。需要运行真实模型或本地服务时，复制 `.env.example` 为 `.env`，再按对应章节填写配置；默认验证不会发起真实调用。

每一章尽量包含三件事：

- 一个用于学习理解的 Python notebook，包含概念、代码、输出、断言和边界
- 必要时补充脚本化 runnable
- 一组工程问题清单：为什么这样做、哪里会失败、上线前要补什么

## 目录

| 章节 | 主题 | Notebook | 在线运行 | 状态 |
| --- | --- | --- | --- | --- |
| 01 | AI Agent 工程师导论 | [01-agent-engineer-intro.ipynb](chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro.ipynb) | 草稿 |
| 02 | LLM 初识：Transformer、Attention 与生成机制 | [02-llm-basics.ipynb](chapters/02-llm-basics/notebooks/02-llm-basics.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/02-llm-basics/notebooks/02-llm-basics.ipynb) | 草稿 |
| 03 | 提示词工程与结构化输出 | [03-prompt-engineering.ipynb](chapters/03-prompt-engineering/notebooks/03-prompt-engineering.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/03-prompt-engineering/notebooks/03-prompt-engineering.ipynb) | 已完成待复查 |
| 04 | Function Calling / Tool Use | [04-tool-calling.ipynb](chapters/04-tool-calling/notebooks/04-tool-calling.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/04-tool-calling/notebooks/04-tool-calling.ipynb) | 技术教程已完成 |
| 05 | MCP：Agent 连接外部世界的协议 | [05-mcp.ipynb](chapters/05-mcp/notebooks/05-mcp.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/05-mcp/notebooks/05-mcp.ipynb) | 技术教程已完成 |
| 06 | RAG 知识库工程 | [06-rag.ipynb](chapters/06-rag/notebooks/06-rag.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/06-rag/notebooks/06-rag.ipynb) | 技术教程已完成 |
| 07 | 上下文工程：长对话、记忆、压缩与状态 | [07-context-memory.ipynb](chapters/07-context-memory/notebooks/07-context-memory.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/07-context-memory/notebooks/07-context-memory.ipynb) | 技术教程已完成 |
| 08 | Agent Planning 与执行循环 | [08-agent-loop.ipynb](chapters/08-agent-loop/notebooks/08-agent-loop.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/08-agent-loop/notebooks/08-agent-loop.ipynb) | 技术教程已完成 |
| 09 | Agent Skills 与 Agent-facing CLI | [09-agent-skills-cli.ipynb](chapters/09-agent-skills-cli/notebooks/09-agent-skills-cli.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/09-agent-skills-cli/notebooks/09-agent-skills-cli.ipynb) | 技术教程已完成 |
| 10 | Agent Harness Engineering | [10-harness-engineering.ipynb](chapters/10-harness-engineering/notebooks/10-harness-engineering.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/10-harness-engineering/notebooks/10-harness-engineering.ipynb) | 技术教程已完成 |
| 11 | Agent Frameworks：PydanticAI、LangGraph 与 Microsoft Agent Framework | [11-frameworks.ipynb](chapters/11-frameworks/notebooks/11-frameworks.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/11-frameworks/notebooks/11-frameworks.ipynb) | 技术教程已完成 |
| 12 | Evals、Tracing、Guardrails 与人审 | [12-evals-guardrails.ipynb](chapters/12-evals-guardrails/notebooks/12-evals-guardrails.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/12-evals-guardrails/notebooks/12-evals-guardrails.ipynb) | 技术教程已完成 |
| 13 | Capstone：完整产研协作助手 | [13-capstone.ipynb](chapters/13-capstone/notebooks/13-capstone.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/13-capstone/notebooks/13-capstone.ipynb) | 提纲 |
| 14 | 行业案例扩展 | [14-industry-cases.ipynb](chapters/14-industry-cases/notebooks/14-industry-cases.ipynb) | [Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/14-industry-cases/notebooks/14-industry-cases.ipynb) | 扩展教程已完成 |

## 仓库结构

```text
.
├── README.md
├── AGENTS.md                  # Agent 操作协议
├── pyproject.toml
├── uv.lock
├── .env.example
├── scripts/                   # CI 验证脚本
│   ├── validate_notebook.py
│   ├── check_cell_ids.py
│   ├── sync_status.py
│   └── check_env.py
├── docs/
│   ├── roadmap.md
│   ├── status.md
│   ├── publishing-guide.md
│   ├── notebook-template.md
│   └── writing-guide.md
├── chapters/
│   ├── 01-agent-engineer-intro/notebooks/
│   ├── 02-llm-basics/notebooks/
│   ├── 03-prompt-engineering/notebooks/
│   ├── 04-tool-calling/notebooks/
│   ├── 05-mcp/notebooks/
│   ├── 06-rag/notebooks/
│   ├── 07-context-memory/notebooks/
│   ├── 08-agent-loop/notebooks/
│   ├── 09-agent-skills-cli/notebooks/
│   ├── 10-harness-engineering/notebooks/
│   ├── 11-frameworks/notebooks/
│   ├── 12-evals-guardrails/notebooks/
│   ├── 13-capstone/notebooks/
│   └── 14-industry-cases/notebooks/
└── datasets/
```

## 文档导航

| 文档 | 用途 |
|------|------|
| [AGENTS.md](AGENTS.md) | Agent 操作协议（启动流程、DoD、禁止事项） |
| [docs/status.md](docs/status.md) | 项目进度与状态（唯一事实源） |
| [docs/roadmap.md](docs/roadmap.md) | 课程路线、章节大纲与依赖关系 |
| [docs/writing-guide.md](docs/writing-guide.md) | 写作规范（风格、结构、代码要求） |
| [docs/notebook-template.md](docs/notebook-template.md) | Notebook 结构模板 |
| [docs/publishing-guide.md](docs/publishing-guide.md) | 多平台发布工作流 |
