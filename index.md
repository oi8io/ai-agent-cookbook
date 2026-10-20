# AI Agent Engineering Cookbook

以 Notebook 为阅读入口的 AI Agent 工程教程，中文副标题为“从基础原理到生产级智能体系统”。

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

```{note}
本网站由 [Jupyter Book](https://jupyterbook.org) 直接从仓库中的 Notebook 渲染生成。
所有教学内容以 Notebook 为唯一事实源，修改源文件后重新构建即可更新本站。
```

## 开始阅读

左侧目录按课程主线排列，从[第一章](chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro)开始。

在线运行无需安装环境，可直接打开 [Google Colab](https://colab.research.google.com/github/oi8io/ai-agent-cookbook/blob/main/chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro.ipynb)。Colab 运行环境是临时的；涉及 API Key、本地 Ollama 或其他外部服务时，仍需按对应章节完成配置。

本地阅读和运行：

```bash
uv sync
uv run jupyter lab
```

需要运行真实模型或本地服务时，复制 `.env.example` 为 `.env`，再按对应章节填写配置；默认验证不会发起真实调用。

每一章尽量包含三件事：

- 一个用于学习理解的 Python notebook，包含概念、代码、输出、断言和边界
- 必要时补充脚本化 runnable
- 一组工程问题清单：为什么这样做、哪里会失败、上线前要补什么

## 目录

| 章节 | 主题 | 状态 |
| --- | --- | --- |
| 01 | [AI Agent 工程全景](chapters/01-agent-engineer-intro/notebooks/01-agent-engineer-intro) | 草稿 |
| 02 | [LLM 初识](chapters/02-llm-basics/notebooks/02-llm-basics) | 草稿 |
| 03 | [面向产研协作助手 V0 的提示词工程](chapters/03-prompt-engineering/notebooks/03-prompt-engineering) | 已完成待复查 |
| 04 | [Function Calling](chapters/04-tool-calling/notebooks/04-tool-calling) | 技术教程已完成 |
| 05 | [MCP](chapters/05-mcp/notebooks/05-mcp) | 技术教程已完成 |
| 06 | [RAG 知识库工程](chapters/06-rag/notebooks/06-rag) | 技术教程已完成 |
| 07 | [上下文工程](chapters/07-context-memory/notebooks/07-context-memory) | 技术教程已完成 |
| 08 | [Agent Loop](chapters/08-agent-loop/notebooks/08-agent-loop) | 技术教程已完成 |
| 09 | [Agent Skills 与 Agent-facing CLI](chapters/09-agent-skills-cli/notebooks/09-agent-skills-cli) | 技术教程已完成 |
| 10 | [Agent Harness Engineering](chapters/10-harness-engineering/notebooks/10-harness-engineering) | 技术教程已完成 |
| 11 | [Agent Frameworks](chapters/11-frameworks/notebooks/11-frameworks) | 技术教程已完成 |
| 12 | [生产控制](chapters/12-evals-guardrails/notebooks/12-evals-guardrails) | 按新规范完成 |
| 13 | [Capstone](chapters/13-capstone/notebooks/13-capstone) | 提纲 |
| 14 | [行业 Agent 落地](chapters/14-industry-cases/notebooks/14-industry-cases) | 扩展教程已完成 |

## 仓库与文档

| 资源 | 用途 |
|------|------|
| [GitHub 仓库](https://github.com/oi8io/ai-agent-cookbook) | 源文件、Notebook 与发布物 |
| [AGENTS.md](https://github.com/oi8io/ai-agent-cookbook/blob/main/AGENTS.md) | Agent 操作协议（启动流程、DoD、禁止事项） |
| [docs/status.md](https://github.com/oi8io/ai-agent-cookbook/blob/main/docs/status.md) | 项目进度与状态（唯一事实源） |
| [docs/roadmap.md](https://github.com/oi8io/ai-agent-cookbook/blob/main/docs/roadmap.md) | 课程路线、章节大纲与依赖关系 |
| [docs/writing-guide.md](https://github.com/oi8io/ai-agent-cookbook/blob/main/docs/writing-guide.md) | 写作规范（风格、结构、代码要求） |
| [docs/notebook-template.md](https://github.com/oi8io/ai-agent-cookbook/blob/main/docs/notebook-template.md) | Notebook 结构模板 |
| [docs/publishing-guide.md](https://github.com/oi8io/ai-agent-cookbook/blob/main/docs/publishing-guide.md) | 多平台发布工作流 |
