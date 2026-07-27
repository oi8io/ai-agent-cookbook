# 发布指南

这个系列采用“notebook 为学习源稿，多平台按需改写”的方式。

也就是说：**每章先写成 notebook，博客、公众号、知乎、掘金等平台再从 notebook 提取文字、图和关键代码**。

## 推荐工作流

```text
chapters/xx-topic/notebooks/xx-topic.ipynb
  -> 作为学习源稿
  -> 本地运行和校对
  -> 按平台做轻量改写
  -> 发布到博客/公众号/知乎/掘金
  -> 在仓库索引里补发布链接
```

## 每章建议产物

每一章目录里保持这几类内容：

```text
notebooks/      # 学习源稿
notes.md        # 调研笔记，不直接发布
examples/       # 配套代码
tests/          # 验证代码
assets/         # 图片、架构图、截图，可选
```

发布时通常从 notebook 提取内容，代码示例可以：

- 直接贴关键片段
- 给 GitHub/Gitee 仓库链接
- 给具体 notebook cell 或示例文件链接
- 在文章末尾放运行命令

## 平台适配建议

### 个人博客

适合放完整长文。

建议保留：

- 章节标题
- 完整目录
- 代码块
- Mermaid 图或架构图
- 参考链接
- 仓库链接

如果使用 Hugo、Hexo、VitePress、Astro、Docusaurus 等静态站点，可以从 notebook 导出 Markdown 后补 frontmatter。

### 公众号

适合做“阅读体验更顺”的版本。

建议调整：

- 标题更口语化
- 段落更短
- 代码不要太长，只放关键片段
- 复杂表格改成列表
- 文章末尾放“配套代码仓库”

公众号不太适合放大量 runnable 细节，细节留在仓库。

### 知乎

适合“问题意识更强”的版本。

建议开头用问题切入：

- AI Agent 工程师到底在做什么？
- Function Calling 和 Tool Use 有什么区别？
- 为什么 RAG Demo 容易，RAG 上线很难？

知乎版本可以保留较多解释，但代码要控制长度。

### 掘金 / CSDN

适合偏工程教程。

建议保留：

- 环境准备
- 运行命令
- 核心代码
- 报错和排查
- 项目结构

这类平台可以更像“教程”，标题可以明确带技术关键词。

## 发布稿 frontmatter 模板

从 notebook 导出 Markdown 后，可以在发布稿顶部按需加入：

```yaml
---
title: "01 AI Agent 工程师导论"
description: "理解 AI Agent 和 Chatbot、RAG、Workflow 的区别，以及 Agent 工程师的能力栈。"
date: 2026-07-09
tags:
  - AI Agent
  - LLM
  - RAG
  - Tool Calling
  - Agent Engineering
series: "AI Agent Engineering Cookbook"
---
```

如果某个平台不支持 frontmatter，发布前删掉这段。

## 图片和图表

建议优先使用这几种：

- Mermaid：适合流程图、架构图、状态机。
- PNG/JPG：适合公众号、知乎这类平台。
- SVG：适合博客，但部分平台支持不好。

如果要多平台分发，最稳的方式是：

1. 在 Markdown 里维护 Mermaid 源图。
2. 发布到公众号/知乎前导出成 PNG。
3. 图片放到每章的 `assets/` 目录。

## 发布链接管理

每章发布后，可以在仓库索引增加链接列：

```text
| 章节 | 主题 | Notebook | 博客 | 公众号 | 知乎 |
```

这样仓库会变成系列的总入口。

## 推荐节奏

每章建议分两次发布：

1. **通识文章版**：讲清楚概念、工程问题和主线。
2. **代码实践版**：专门讲 notebook 怎么跑、怎么改、哪里会失败。

这样一章可以自然拆成两篇，不会又长又重。

## 最小发布清单

发布前检查：

- 标题是否清楚
- 开头是否说明这一章解决什么问题
- 代码是否能运行
- 命令是否验证过
- 图片是否能正常显示
- 是否有仓库链接
- 是否说明下一章讲什么
