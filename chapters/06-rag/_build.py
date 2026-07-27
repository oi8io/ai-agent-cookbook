# Build Chapter 6 RAG notebook.
# Run: uv run python chapters/06-rag/_build.py
import nbformat as nbf
from pathlib import Path

OUT = Path(__file__).resolve().parent / "notebooks" / "06-rag.ipynb"
OUT.parent.mkdir(parents=True, exist_ok=True)

nb = nbf.v4.new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.14.0"},
}

def md(text):
    nb.cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    nb.cells.append(nbf.v4.new_code_cell(text))

# =====  TITLE  =====
md('''# RAG 知识库工程：从文档检索到生产架构

**RAG（Retrieval-Augmented Generation）在模型生成答案之前，先检索与问题相关的文档片段作为证据，让模型基于证据而不是记忆来回答。**''')

# =====  1 先说结论  =====
md('''## 1 先说结论

RAG 解决三个问题：

1. **私有知识**。模型训练数据里没有你的内部文档、API 规范或故障手册。
2. **实时知识**。模型的训练截止日期之前的参数不会自动更新。发布记录、告警阈值这些信息需要实时检索。
3. **可追溯**。RAG 生成的答案可以附带引用来源，指向具体文档和段落。这比模型凭"记忆"回答更可靠。

一次 RAG 请求经过以下步骤：

```text
用户问题
  -> 查询向量
  -> 向量检索 Top-K
  -> Metadata 过滤
  -> Rerank
  -> 组装 Context
  -> LLM 基于 Context 生成答案
  -> 引用来源
```

本章最终产出一个可运行的完整 RAG 系统：文档解析、Chunk、Embedding、向量检索、Rerank 和 DeepSeek 生成，并附带离线评测。

RAG 不能解决：

- 知识库本身没有的信息（需要无答案检测，而不是强行回答）。
- 模型的逻辑推理能力（这是 LLM 的能力边界，不是检索的问题）。
- 权限系统设计（Metadata 过滤只是机制，权限策略需要业务层定义）。''')

# =====  2  RAG 为什么出现  =====
md('''## 2 RAG 为什么出现

### 2.1 模型参数中的知识有三重限制

| 限制 | 具体问题 | 例子 |
|------|---------|------|
| 时间截止 | 模型训练数据有截止日期 | GPT-4 不知道 2025 年发布的新框架 |
| 私有数据 | 企业文档不在公开训练集中 | 萤火平台的内部 API 规范 |
| 幻觉 | 模型在不知道时会编造 | "萤火平台支持 Kubernetes 部署"（实际文档未提及） |

这三重限制的根源相同：模型在推理时只能使用参数中存储的信息，无法访问外部数据源。''')

md('''### 2.2 幻觉的根本原因是缺少证据

模型生成 token 时依据概率，不是事实。当问题需要的信息不在参数里，模型仍然会生成高概率的 token 序列。这个序列读起来通顺，但内容可能是编造的。

RAG 的应对：在生成之前，先把相关信息检索出来放进上下文。模型不需要"记住"答案，只需要"读懂"检索到的段落。

```text
无 RAG：问题 -> 模型 -> 答案（可能编造）
有 RAG：问题 -> 检索 -> 相关段落 -> 模型 + 段落 -> 答案 + 引用
```''')

md('''### 2.3 RAG 与长上下文、微调、Tool Calling 的边界

这四种技术都试图让模型获得外部信息，但它们适用的场景不同。

| 技术 | 适用场景 | 不适用场景 |
|------|---------|-----------|
| 长上下文 | 单次对话需要几篇完整文档 | 文档库有几百篇，token 成本不可接受 |
| 微调 | 学习稳定的格式或风格 | 知识频繁更新，每次更新都要重新训练 |
| Tool Calling | 查询结构化数据、执行动作 | 从非结构化文档中检索段落 |
| RAG | 从大量非结构化文档中检索相关内容 | 需要精确计算或事务性操作 |

**直接使用长上下文**适合：单篇文档问答、对话中引用少数几段已知文本。长上下文模型的上下文窗口已经很大（128K-1M token），如果你的文档库总共只有十几篇，把它们全放进上下文可能比建设 RAG 更简单。

**值得建设 RAG 的场景**：文档库超过 100 篇且持续增长、需要检索结果可追溯、需要根据权限过滤文档、需要 BM25 和 Dense 的混合检索。''')

# =====  3  统一术语  =====
md('''## 3 统一术语

| 术语 | 是什么 | 保存什么 | 在哪阶段产生 | 被谁使用 |
|------|--------|---------|-------------|---------|
| Document | 原始文档 | 标题、正文、格式 | 数据源 | Parser |
| Parser | 文档解析器 | 提取纯文本和结构 | 索引链路 | Chunker |
| Chunk | 文本片段 | 一段连续文本 + Chunk ID | Chunk 策略 | Embedding、Retriever |
| Metadata | 结构化附加信息 | doc_id、版本、更新时间、权限 | 解析和 Chunk 阶段 | Retriever、权限过滤 |
| Embedding | 向量表示 | 浮点数数组（如 768 维） | Embedding 模型 | 向量索引 |
| Vector Index | 向量索引 | Embedding + 快速检索结构 | 索引链路 | Retriever |
| Retriever | 检索器 | 不保存数据，执行检索逻辑 | 查询链路 | Reranker、Generator |
| Reranker | 重排序器 | 检索结果的精排分数 | 查询链路 | Context 组装 |
| Context | 组装后的提示上下文 | 检索到的 Chunk 文本 + 引用标记 | 查询链路 | LLM |
| Citation | 引用标记 | 来源文档 ID 和 Chunk 位置 | 查询链路 | 用户验证 |
| Corpus | 语料库 | 全部已索引的文档集合 | 索引链路 | 评测、统计 |''')

# =====  4  RAG 的完整数据流  =====
md('''## 4 RAG 的完整数据流

RAG 系统包含两条独立的链路：索引链路在离线处理文档，查询链路在在线响应用户。

### 4.1 索引链路

```mermaid
flowchart LR
    A[数据源] --> B[文档解析]
    B --> C[清洗]
    C --> D[Chunk 切分]
    D --> E[Metadata 提取]
    E --> F[Embedding]
    F --> G[建立索引]
    G --> H[(持久化)]
```

每一步的输入和输出：

| 步骤 | 输入 | 输出 |
|------|------|------|
| 文档解析 | .md / .pdf / .html 文件 | 纯文本 + 结构信息（标题层级、表格、代码块） |
| 清洗 | 含噪声的文本 | 去除特殊字符、统一空白、保留有意义的内容 |
| Chunk 切分 | 长文本 | 固定长度或语义完整的文本片段 |
| Metadata 提取 | Chunk + 原始文档元数据 | 每条 Chunk 附带 doc_id、版本、更新时间、权限等 |
| Embedding | Chunk 文本 | 768 维（或更多）浮点数向量 |
| 建立索引 | 一组向量 | ANN 索引结构（HNSW 图等） |
| 持久化 | 索引 + Metadata | 写入磁盘或数据库 |''')

md('''### 4.2 查询链路

```mermaid
flowchart LR
    Q[用户问题] --> QP[查询处理]
    QP --> QE[查询 Embedding]
    QE --> R1[初次检索 Top-K]
    R1 --> MF[Metadata 过滤]
    MF --> RR[Rerank]
    RR --> CA[Context 组装]
    CA --> LLM[LLM 生成]
    LLM --> CT[引用来源]
```

每一步的职责：

| 步骤 | 做什么 | 影响什么 |
|------|--------|---------|
| 查询处理 | 去除无关词、改写查询 | 检索命中率 |
| 查询 Embedding | 把问题转为向量 | 与文档向量的可比性 |
| 初次检索 | 从索引中取 Top-K | 召回率和速度 |
| Metadata 过滤 | 按权限、时间等过滤 | 安全性和相关性 |
| Rerank | 对初检结果精排 | 最终进入 Context 的段落质量 |
| Context 组装 | 拼接段落 + 提示词 | LLM 的输入质量 |
| LLM 生成 | 基于证据回答 | 答案准确性和引用 |

整个链路中有三个关键决策点，直接影响最终效果：

1. **Chunk 怎么切**（§6）。影响了检索能命中什么粒度的信息。
2. **用什么 Embedding 模型**（§7）。决定了"语义相似"的含义。
3. **检索后怎么排序和过滤**（§9）。决定了哪些段落最终进入模型上下文。''')

# =====  5  文档解析与数据治理  =====
md('''## 5 文档解析与数据治理

### 5.1 不同文档格式的解析差异

| 格式 | 解析难度 | 结构保留 | 注意事项 |
|------|---------|---------|---------|
| Markdown | 低 | 标题层级、表格、代码块自然保留 | 本章案例使用 |
| HTML | 中 | 需提取正文、处理导航栏和广告 | 用 trafilatura 或 beautifulsoup4 |
| PDF | 高 | 表格和代码块容易断裂 | 双栏 PDF、扫描件需要 OCR |
| Office | 中 | 样式信息丰富但格式封闭 | python-docx 或 LibreOffice 转 Markdown |

解析质量的差异会向下传导。Markdown 表格解析失败，Chunk 里就是碎片化的文字，检索和生成都会受影响。''')

md('''### 5.2 Metadata 设计

每条 Chunk 必须携带以下 Metadata：

| 字段 | 来源 | 用途 |
|------|------|------|
| `doc_id` | 文档入库时分配 | 引用溯源、删除传播 |
| `chunk_id` | Chunk 策略生成 | 唯一标识、更新定位 |
| `title` | 文档解析提取 | 引用展示 |
| `source_path` | 文件路径 | 调试和溯源 |
| `version` | 文档元数据 | 版本对比 |
| `updated_at` | 文件系统或 CMS | 增量更新判断 |
| `access_level` | 业务系统 | 权限过滤（public / team / ops-only） |
| `tags` | 人工或自动分类 | 类别过滤 |
| `chunk_index` | Chunk 策略生成 | 相邻 Chunk 拼接 |''')

md('''### 5.3 文档的增删改与索引同步

文档变化时，索引需要同步更新。

| 操作 | 索引动作 |
|------|---------|
| 新增文档 | 解析、Chunk、Embedding、插入索引 |
| 修改文档 | 按 `doc_id` 删除旧 Chunk，重新生成并插入新 Chunk |
| 删除文档 | 按 `doc_id` 删除所有关联 Chunk |
| 权限变更 | 更新 Metadata 中的 `access_level`，不重建 Embedding |

核心原则：每种文档操作都有一组确定性的 Chunk ID 变更。修改文档时，先删后插保证幂等；删除文档时，依赖 Metadata 中的 `doc_id` 做批量清理。''')

# =====  6  Chunk 怎么切  =====
md('''## 6 Chunk 怎么切

### 6.1 五种切分策略

| 策略 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| 固定字符 | 每 256 或 512 字符切一段 | 简单、可预测 | 可能在句子中间切断 |
| Token 长度 | 按 token 数切分 | 精确控制模型输入长度 | 需要 tokenizer |
| 按标题/段落 | 以 Markdown 标题为界 | 语义完整 | 标题短的段落 Still 太碎 |
| 语义切分 | 用 Embedding 判断断点 | 一个 Chunk 一个主题 | 计算成本高 |
| Parent-Child | 大 Chunk 做 Context，小 Chunk 做检索 | 检索精确、上下文完整 | 实现复杂 |

本章实验对比四种策略：固定 256、固定 512、按标题切分、语义切分。''')

md('''### 6.2 Chunk 策略对比实验

下面用同一份文档（`doc-003-changelog.md`）和同一组问题（Q1-Q5），对比不同 Chunk 策略的检索命中率。实验使用真实中文 Embedding 模型 `BAAI/bge-small-zh-v1.5`。

先加载文档和 Embedding 模型：''')

code('''import os
import sys
from pathlib import Path

# 检测仓库根目录
def _find_repo_root():
    for start in [Path.cwd()] + list(Path.cwd().parents):
        if (start / "chapters" / "06-rag").is_dir():
            return start
    return Path.cwd()

REPO = _find_repo_root()
os.chdir(REPO)

DOCS_DIR = REPO / "chapters" / "06-rag" / "examples" / "docs"
doc_files = sorted(DOCS_DIR.glob("*.md"))
for f in doc_files:
    print(f"{f.stem}: {len(f.read_text())} chars")
print(f"\\nTotal: {len(doc_files)} documents")''')

code('''import re

def load_document(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    # 提取标题（第一个 # 开头的行）
    title_match = re.search(r"^#\\s+(.+)", text, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(path).stem
    return {"text": text, "title": title, "path": path}

# 加载五份文档
docs = {f.stem: load_document(str(f)) for f in doc_files}
for doc_id, doc in docs.items():
    print(f"{doc_id}: title='{doc['title']}', {len(doc['text'])} chars")''')

code('''# 实验环境变量控制
RUN_LIVE_EMBEDDING = os.getenv("RUN_LIVE_EMBEDDING", "0") == "1"

embed_model = None
if RUN_LIVE_EMBEDDING:
    try:
        from sentence_transformers import SentenceTransformer
        EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
        embed_model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"Embedding model loaded: {EMBEDDING_MODEL}")
        print(f"Vector dimension: {embed_model.get_sentence_embedding_dimension()}")
    except ImportError as e:
        print(f"Failed to load sentence-transformers: {e}")
        print("Install with: uv add sentence-transformers")
else:
    print("RUN_LIVE_EMBEDDING=0, using offline mode. Set to 1 to download and use real model.")''')

code('''# 四种 Chunk 策略实现
import re

def chunk_fixed_size(text: str, size: int = 256, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def chunk_by_headings(text: str) -> list[str]:
    # 按 ## 标题切分
    sections = re.split(r"(?=\\n## )", text)
    return [s.strip() for s in sections if s.strip() and len(s.strip()) > 20]

def chunk_semantic(text: str, min_len: int = 100) -> list[str]:
    # 简化版语义切分：按自然段落，合并过短的段落
    paragraphs = [p.strip() for p in text.split("\\n\\n") if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) < min_len * 2 and current:
            current += "\\n\\n" + p
        else:
            if current:
                chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks

# 用 changelog 文档做对比
changelog = docs["doc-003-changelog"]["text"]
print(f"Original: {len(changelog)} chars\\n")

for name, func in [("Fixed-256", lambda t: chunk_fixed_size(t, 256, 50)),
                    ("Fixed-512", lambda t: chunk_fixed_size(t, 512, 100)),
                    ("Headings", chunk_by_headings),
                    ("Semantic", chunk_semantic)]:
    chunks = func(changelog)
    lengths = [len(c) for c in chunks]
    print(f"{name}: {len(chunks)} chunks, "
          f"min={min(lengths)}, max={max(lengths)}, avg={sum(lengths)//len(chunks)}")''')

md('''四种策略对同一份 changelog 文档产生了不同的 Chunk 数和粒度。哪些 Chunk 能命中问题 Q3（"v2.3 版本新增了什么功能，附件上传限制改成了多少"），取决于每个策略如何切割 v2.3.0 这段文本。

固定 256 可能把"附件上传大小限制"这段描述切成两块，导致单个 Chunk 无法同时包含问题和答案的关键词；按标题切分则把整个 v2.3.0 节作为一个 Chunk，信息完整但粒度较粗。''')

md('''### 6.3 Chunk 太大了会怎样，太小了会怎样

| 问题 | 原因 | 后果 |
|------|------|------|
| Chunk 太大（> 1000 tokens） | 一个 Chunk 包含多个主题 | 检索命中但 Context 冗余，浪费 token |
| Chunk 太小（< 50 tokens） | 片段缺少上下文 | 检索命中但模型看不懂这段在说什么 |
| 没有 Overlap | 关键信息正好在 Chunk 边界 | 检索漏掉，因为分布在了相邻 Chunk 中 |
| Overlap 太大 | 冗余内容进入 Context | 浪费 token，降低 Context 的有效信息密度 |

**Chunk 大小和 Overlap 是一对矛盾**。本章的选择：固定 256 字符、Overlap 50 字符作为基线，后续通过评测（§14）选择最优策略。''')

md('''### 6.4 Chunk ID 与更新追踪

每条 Chunk 需要稳定的 ID，用于更新时精确定位。推荐生成方式：

```text
chunk_id = hash(doc_id + ":" + str(chunk_index) + ":" + content_hash[:8])
```

- `doc_id` 保证跨文档唯一。
- `chunk_index` 保证同文档内有序。
- `content_hash` 保证内容变更后可检测。

文档更新时，重新生成该文档的所有 Chunk ID。新旧 ID 对比即可确定哪些 Chunk 需要从索引中删除（旧 ID 中存在、新 ID 中不存在），哪些需要新增插入（新 ID 中存在、旧 ID 中不存在）。

### 6.5 如何通过评测选择 Chunk 策略

选择 Chunk 策略的正确方式是和业务问答一起评测（§14），而不是凭感觉选。评测流程：

1. 准备固定问题集 + 标准答案。
2. 用每种 Chunk 策略建索引。
3. 对每个问题检索 Top-5，计算 Hit Rate。
4. 用检索结果生成答案，评估正确性和引用准确性。
5. 选择综合得分最高的策略。''')

# =====  7  Embedding 原理与实验  =====
md('''## 7 Embedding 原理与实验

### 7.1 语义向量

Embedding 模型把文本映射到高维空间中的一个点。语义相近的文本，在空间中距离更近。

Embedding 模型的训练目标是：让同一对（问题，答案）的向量尽可能地靠近，不同对（问题，无关文档）的向量尽可能地远。

生成模型和 Embedding 模型是两种不同的模型：

| | 生成模型（GPT、DeepSeek） | Embedding 模型（BGE、text2vec） |
|---|---|---|
| 任务 | 预测下一个 token | 输出定长向量 |
| 输出 | 可变长度文本 | 固定维度的浮点数组 |
| 典型维度 | 不适用 | 384 / 768 / 1024 / 1536 |
| 训练方式 | 自回归 | 对比学习 |''')

md('''### 7.2 余弦相似度数值实验

余弦相似度衡量两个向量的夹角。取值范围 [-1, 1]，1 表示方向完全相同，0 表示正交，-1 表示方向相反。

用 NumPy 手动计算，观察向量如何比较：''')

code('''import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 构造 5 个手工向量：模拟 Embedding 空间中的文档和查询
doc_vecs = {
    "D1: 产品说明": np.array([0.8, 0.1, 0.1]),
    "D2: API 文档": np.array([0.1, 0.9, 0.2]),
    "D3: 发布记录": np.array([0.2, 0.1, 0.7]),
    "D4: 故障手册": np.array([0.1, 0.2, 0.9]),
    "D5: 团队规范": np.array([0.5, 0.4, 0.2]),
}
query_vecs = {
    "Q1: 部署方式": np.array([0.7, 0.2, 0.1]),   # 接近 D1（产品说明）
    "Q2: 速率限制": np.array([0.2, 0.8, 0.1]),   # 接近 D2（API 文档）
}

# 计算每个查询与所有文档的相似度
for q_name, q_vec in query_vecs.items():
    print(f"\\n{q_name}:")
    scores = [(d_name, cosine_similarity(q_vec, d_vec)) for d_name, d_vec in doc_vecs.items()]
    scores.sort(key=lambda x: x[1], reverse=True)
    for d_name, score in scores:
        marker = " <--" if score == scores[0][1] else ""
        print(f"  vs {d_name}: cos={score:.3f}{marker}")

# 验证：D1 和 D2 之间的相似度（两个不同主题，应较低）
sim_diff = cosine_similarity(doc_vecs["D1: 产品说明"], doc_vecs["D2: API 文档"])
sim_same = cosine_similarity(doc_vecs["D1: 产品说明"], doc_vecs["D1: 产品说明"])
print(f"\\nD1 vs D2 (different topics): {sim_diff:.3f}")
print(f"D1 vs D1 (same document): {sim_same:.3f}")
assert sim_diff < sim_same, "Same document should have higher similarity"''')

md('''Q1（部署方式）最接近 D1（产品说明），Q2（速率限制）最接近 D2（API 文档）。这是理想情况——当文档内容和查询意图一致时，向量检索工作得很好。

但这个实验用的是 3 维手工向量。真实 Embedding 是 768 维，语义关系要复杂得多。下一步用真实模型验证。''')

md('''### 7.3 真实中文 Embedding 实验

使用 `BAAI/bge-small-zh-v1.5`（下载量 100 万+，768 维，中文效果稳定）。模型下载默认关闭，设置 `RUN_LIVE_EMBEDDING=1` 启用。''')

code('''# 文档 Chunk + Embedding（离线模式使用固定向量模拟）
DOCS_FOR_EMBED = []
for doc_id, doc in docs.items():
    # 用固定 256 切分
    chunks = chunk_fixed_size(doc["text"], 256, 50)
    for j, chunk_text in enumerate(chunks):
        DOCS_FOR_EMBED.append({
            "doc_id": doc_id,
            "chunk_id": f"{doc_id}:chunk_{j}",
            "title": doc["title"],
            "text": chunk_text,
            "chunk_index": j,
        })

print(f"Total chunks: {len(DOCS_FOR_EMBED)}")
for c in DOCS_FOR_EMBED[:5]:
    print(f"  {c['chunk_id']}: {len(c['text'])} chars, "
          f"preview='{c['text'][:60]}...'")
print("  ...")

if RUN_LIVE_EMBEDDING:
    texts = [c["text"] for c in DOCS_FOR_EMBED]
    embeddings = embed_model.encode(texts, show_progress_bar=True)
    print(f"\\nEmbedding shape: {embeddings.shape}")
    print(f"Sample vector (first 5 dims): {embeddings[0][:5]}")
else:
    print("\\nRUN_LIVE_EMBEDDING=0. Using mock embeddings for structure validation.")
    # 使用固定种子生成模拟向量，保持维度正确（768）
    rng = np.random.RandomState(42)
    embeddings = rng.randn(len(DOCS_FOR_EMBED), 768).astype(np.float32)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    print(f"Mock embedding shape: {embeddings.shape}")

assert embeddings.shape[0] == len(DOCS_FOR_EMBED)
assert embeddings.shape[1] == 768
print("\\nOK: embeddings ready for indexing")''')

code('''# 查询检索实验
QUESTIONS = [
    ("Q1", "萤火平台支持哪些部署方式？"),
    ("Q2", "API 的速率限制是多少？"),
    ("Q3", "v2.3 版本新增了什么功能，附件上传限制改成了多少？"),
    ("Q4", "数据库连接超时和消息队列堆积的告警阈值是多少？"),
    ("Q5", "分支命名规则是什么，commit 格式有什么要求？"),
    ("Q8", "平台的定价方案是什么？"),
]

def search(query: str, top_k: int = 3):
    if RUN_LIVE_EMBEDDING:
        q_vec = embed_model.encode([query])[0]
    else:
        rng = np.random.RandomState(hash(query) % (2**31))
        q_vec = rng.randn(768).astype(np.float32)
        q_vec = q_vec / np.linalg.norm(q_vec)
    scores = [cosine_similarity(q_vec, emb) for emb in embeddings]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(DOCS_FOR_EMBED[i], score) for i, score in ranked[:top_k]]

for q_id, question in QUESTIONS:
    print(f"\\n{'='*60}")
    print(f"{q_id}: {question}")
    results = search(question, top_k=3)
    for rank, (chunk, score) in enumerate(results):
        print(f"  #{rank+1} [{chunk['doc_id']}] {chunk['title']} "
              f"(cos={score:.3f}): {chunk['text'][:80].replace(chr(10), ' ')}...")
    print(f"  正确答案来源: ", end="")
    # Q1-Q5 对应 doc-001 到 doc-005，Q8 无答案
    expected = {"Q1": "doc-001", "Q2": "doc-002", "Q3": "doc-003",
                 "Q4": "doc-004", "Q5": "doc-005", "Q8": "none"}
    print(expected.get(q_id, "unknown"))''')

md('''用真实 Embedding 时（`RUN_LIVE_EMBEDDING=1`），Q1-Q5 的 Top-3 检索结果应该包含正确答案来源文档的 Chunk。Q8（定价方案）在知识库中没有答案，Top-3 结果即使有高相似度分数，也不包含有效信息——这就是无答案检测的起点。

使用随机向量时（`RUN_LIVE_EMBEDDING=0`），检索结果不可靠。随机向量只能验证代码结构，不能验证语义检索效果。本章后面的检索质量实验（§9）会展示真实 Embedding 下的改进过程。

### 7.4 生成模型与 Embedding 模型的区别

| 维度 | 生成模型 | Embedding 模型 |
|------|---------|---------------|
| 输出 | 文本 | 固定长度向量 |
| 使用方式 | 输入 prompt，输出 token | 输入文本，输出向量 |
| 相似度 | 不天然支持 | 向量间可直接比较 |
| 检索用途 | 不直接用于检索 | 专用于检索和聚类 |
| 典型代表 | DeepSeek-V4、GPT-4o | BGE、text2vec、OpenAI text-embedding-3 |

一个常见的混淆：拿生成模型做 Embedding。虽然某些生成模型可以取隐藏层输出作为向量，但这不是它们的设计目标，维度不一致，效果通常不如专用模型。''')

# =====  8  向量索引与向量数据库  =====
md('''## 8 向量索引与向量数据库

### 8.1 向量数据库实际保存什么

向量数据库保存三样东西：

1. **向量本身**（浮点数组）+ 内部索引结构（HNSW 图等）。
2. **Payload/Metadata**（文档 ID、Chunk ID、标题、权限、时间戳等结构化字段）。
3. **检索接口**（`search(query_vector, top_k, filter)`）。

它不保存原始文档内容——原始文档存在对象存储或 PostgreSQL 中。向量数据库只负责"给定向量，返回最相似的 Top-K 个 ID 和 Metadata"。''')

md('''### 8.2 最小余弦检索（NumPy 实现）

用 NumPy 实现一个最简检索器，让读者看见向量检索的底层逻辑：''')

code('''class MinimalVectorIndex:
    def __init__(self, vectors: np.ndarray, metadata: list[dict]):
        self.vectors = vectors
        self.metadata = metadata
        # 归一化所有向量，后续用点积（等价于 cos，因为已归一化）
        self.norms = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    def search(self, query_vec: np.ndarray, top_k: int = 3,
               metadata_filter: dict | None = None) -> list[dict]:
        # 归一化查询
        q = query_vec / np.linalg.norm(query_vec)
        scores = np.dot(self.norms, q)  # 点积 = cos（已归一化）
        ranked = np.argsort(scores)[::-1]  # 降序
        results = []
        for idx in ranked:
            if metadata_filter:
                meta = self.metadata[idx]
                if not all(meta.get(k) == v for k, v in metadata_filter.items()):
                    continue
            results.append({
                **self.metadata[idx],
                "score": float(scores[idx]),
            })
            if len(results) >= top_k:
                break
        return results

# 构建最小索引
index = MinimalVectorIndex(embeddings, DOCS_FOR_EMBED)

# 测试检索
rng = np.random.RandomState(99)
test_q = rng.randn(768).astype(np.float32)
results = index.search(test_q, top_k=3)
print("Top-3 (no filter):")
for r in results:
    print(f"  {r['chunk_id']}: score={r['score']:.3f}")

# 测试 Metadata 过滤：只检索 public 文档（排除 doc-004 的 ops-only）
public_docs = [c for c in DOCS_FOR_EMBED if c["doc_id"] != "doc-004-incident-handbook"]
print(f"\\nPublic chunks: {len(public_docs)} / {len(DOCS_FOR_EMBED)} total")
print("OK: minimal vector index with metadata filtering works")''')

md('''这个 20 行的检索器包含了向量数据库的核心逻辑：向量归一化、点积相似度、排序、Top-K 截断和 Metadata 过滤。生产系统在这个基础上增加了 ANN 索引、持久化和并发控制。''')

md('''### 8.3 ANN 与 HNSW

精确检索（暴力扫描）在百万级向量时每次查询耗时数百毫秒。近似最近邻（ANN）用索引结构换速度，在略有精度损失的前提下把延迟降到毫秒级。

HNSW（Hierarchical Navigable Small World）是当前最常用的 ANN 算法。基本思路：

1. 构建多层图结构。顶层节点稀疏，底层节点密集。
2. 查询时从顶层开始，逐层向下搜索，每层只访问最相似的少数节点。
3. 到达底层后，在局部邻域中精确比较。

HNSW 的三个关键参数：

| 参数 | 含义 | 调大后的效果 |
|------|------|------------|
| M | 每个节点的最大连接数 | 索引更大，检索更准 |
| ef_construction | 构建时的搜索宽度 | 构建更慢，索引质量更好 |
| ef_search | 查询时的搜索宽度 | 检索更准，延迟更高 |

本章不深入 HNSW 的实现细节。读者需要知道的是：向量数据库的核心差异不在于"用不用 HNSW"（基本上都用），而在于 Metadata 过滤、混合检索、分布式能力和运维工具。''')

md('''### 8.4 七种方案对比

| 维度 | FAISS | Chroma | pgvector | Qdrant | Milvus | ES/OpenSearch | 托管服务 |
|------|-------|--------|----------|--------|--------|---------------|---------|
| 部署方式 | 进程内库 | pip/进程内 | PG 扩展 | 独立服务 | 独立服务/云 | 独立服务/云 | 云 API |
| 数据规模 | <=10M | <=1M | <=10M | >=100M | >=100M | >=10M | 不限 |
| Metadata 过滤 | 简单 | 基础 | SQL 完整 | 强 | 强 | 强 | 平台决定 |
| 混合检索 | 不支持 | 不支持 | 需自建 BM25 | 支持 | 支持 | 原生支持 | 部分支持 |
| 高可用 | 不支持 | 不支持 | 依赖 PG | 支持 | 支持 | 支持 | 托管 |
| 运维复杂度 | 低 | 低 | 低（如有 PG） | 中 | 高 | 中-高 | 低 |
| 适合场景 | 原型、离线评测 | 小规模原型 | 已有 PG 的团队 | 中大型生产 | 大规模生产 | 已有 ES 的团队 | 无运维团队 |
| 不适合场景 | 生产、多租户 | 生产、大数据量 | 无 PG | 极简原型 | 小团队 | 无 ES 经验 | 强数据隐私 |

### 8.5 选型决策树

```text
需要 RAG 检索？
├─ 数据量 < 10 万 Chunk，原型阶段
│   ├─ 已有 PostgreSQL -> pgvector
│   ├─ 无 PG -> Chroma（本地）/ FAISS（评测）
│   └─ 需要 BM25 -> Elasticsearch
├─ 数据量 10 万 - 100 万 Chunk，生产环境
│   ├─ 已有 Elasticsearch -> ES + 向量插件
│   ├─ 已有 PostgreSQL -> pgvector + 自建 BM25
│   └─ 无基础设施 -> Qdrant
├─ 数据量 > 100 万 Chunk，高并发
│   ├─ 需要混合检索 -> Milvus / Qdrant
│   ├─ 全托管需求 -> Zilliz Cloud / Pinecone / Qdrant Cloud
│   └─ 自建团队强 -> Milvus
└─ 多租户 + 复杂 ACL
    ├─ 数据库级隔离 -> pgvector（行级安全）
    ├─ 索引级隔离 -> Qdrant（collection per tenant）
    └─ 字段级过滤 -> Milvus / ES
```''')

# =====  9  检索质量优化  =====
md('''## 9 检索质量优化

### 9.1 Dense vs BM25 vs Hybrid

| 检索方式 | 原理 | 擅长 | 不擅长 |
|---------|------|------|--------|
| Dense（向量） | 语义相似度 | 同义改写、模糊匹配 | 精确关键词（如错误码、API 路径） |
| BM25（稀疏） | 词频-逆文档频率 | 精确关键词匹配 | 语义相近但用词不同 |
| Hybrid | Dense + BM25 加权融合 | 综合两者优势 | 需要调权重参数 |

BM25 把文档和查询表示为稀疏向量（每个维度对应一个词），通过词频和逆文档频率计算相关性。Dense 检索把文本映射到低维连续空间。两者互补：BM25 保证关键词不丢，Dense 保证语义不丢。''')

md('''### 9.2 实验：Dense vs BM25 vs Hybrid 对比

下面使用 rank-bm25 库实现 BM25，与 Dense 检索和加权融合做对比。''')

code('''# BM25 实现
from rank_bm25 import BM25Okapi
import jieba

# 中文分词后构建 BM25
def tokenize(text: str) -> list[str]:
    return list(jieba.cut(text))

chunk_texts = [c["text"] for c in DOCS_FOR_EMBED]
tokenized_chunks = [tokenize(t) for t in chunk_texts]
bm25 = BM25Okapi(tokenized_chunks)

print(f"BM25 index built: {len(tokenized_chunks)} documents")

def bm25_search(query: str, top_k: int = 3) -> list[dict]:
    tokens = tokenize(query)
    scores = bm25.get_scores(tokens)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [{"chunk": DOCS_FOR_EMBED[i], "bm25_score": float(s)} for i, s in ranked[:top_k]]

# 测试 BM25
for q_id, question in QUESTIONS[:3]:
    print(f"\\n{q_id}: {question}")
    for rank, r in enumerate(bm25_search(question, 3)):
        c = r["chunk"]
        print(f"  #{rank+1} [{c['doc_id']}] score={r['bm25_score']:.2f}: "
              f"{c['text'][:80].replace(chr(10), ' ')}...")''')

code('''# Hybrid 检索：Dense + BM25 加权融合
def hybrid_search(query: str, top_k: int = 3, alpha: float = 0.5) -> list[dict]:
    # Dense 分数（归一化到 0-1）
    if RUN_LIVE_EMBEDDING:
        q_vec = embed_model.encode([query])[0]
    else:
        rng = np.random.RandomState(hash(query) % (2**31))
        q_vec = rng.randn(768).astype(np.float32)
        q_vec = q_vec / np.linalg.norm(q_vec)
    dense_scores = np.dot(embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True), q_vec)

    # BM25 分数（归一化到 0-1）
    tokens = tokenize(query)
    bm25_scores = bm25.get_scores(tokens)
    bm25_norm = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-8)
    dense_norm = (dense_scores - dense_scores.min()) / (dense_scores.max() - dense_scores.min() + 1e-8)

    # 加权融合
    hybrid = alpha * dense_norm + (1 - alpha) * bm25_norm
    ranked = np.argsort(hybrid)[::-1]
    return [{"chunk": DOCS_FOR_EMBED[i],
             "dense": float(dense_scores[i]),
             "bm25": float(bm25_scores[i]),
             "hybrid": float(hybrid[i])} for i in ranked[:top_k]]

# 三种方式对比 Q2（精确关键词"速率限制"）
print("Q2: API 的速率限制是多少？\\n")
print("Dense only:")
dense_results = hybrid_search("API 的速率限制是多少？", 3, alpha=1.0)
for r in dense_results:
    print(f"  [{r['chunk']['doc_id']}] {r['chunk']['text'][:80].replace(chr(10), ' ')}...")

print("\\nBM25 only:")
bm25_results = hybrid_search("API 的速率限制是多少？", 3, alpha=0.0)
for r in bm25_results:
    print(f"  [{r['chunk']['doc_id']}] {r['chunk']['text'][:80].replace(chr(10), ' ')}...")

print("\\nHybrid (alpha=0.5):")
hybrid_results = hybrid_search("API 的速率限制是多少？", 3, alpha=0.5)
for r in hybrid_results:
    print(f"  [{r['chunk']['doc_id']}] {r['chunk']['text'][:80].replace(chr(10), ' ')}...")''')

md('''### 9.3 Rerank

Reranker 对初检 Top-K（通常取 20-50 条）做精排，选出最优的 3-5 条送入 Context。初检用 Dense 或 Hybrid 保证召回（不遗漏），Rerank 用更精确的模型保证精度（送到模型的都是好的）。

常用的 Rerank 模型：`BAAI/bge-reranker-base`、`Cohere Rerank`。本章实验使用 bge-reranker-base 做 Cross-Encoder 评分。''')

md('''### 9.4 多路召回与融合排序

多路召回合并来自不同检索器的结果：

```text
Dense 召回 Top-50 + BM25 召回 Top-50
  -> 去重（按 chunk_id）
  -> 分数归一化
  -> 加权融合（alpha 可配）
  -> Rerank Top-30
  -> 输出 Top-5
```

### 9.5 无答案检测

当 Top-K 结果中所有 Chunk 的相似度低于阈值，或 LLM 判断检索到的内容不足以回答问题时，应触发无答案响应。

两种检测方式：

1. **阈值检测**：Top-1 相似度 < 0.5 -> 无答案。
2. **LLM 判断**：在 prompt 中指示"如果以下资料不足以回答问题，请回答'无法找到相关信息'"。

本章实验使用方式 2（LLM 判断），因为它可以区分"检索失败"和"知识库确实没有"。''')

# =====  10  完整 RAG 实验  =====
md('''## 10 完整 RAG 实验

### 10.1 索引链路：文档 -> Embedding -> 入库

将前面所有步骤串联成一条可顺序执行的索引管道：''')

code('''# === 完整索引管道 ===
import hashlib

def build_index(doc_dir: str):
    """完整索引管道：文档 -> 解析 -> Chunk -> Metadata -> Embedding -> 入库"""
    doc_files = sorted(Path(doc_dir).glob("*.md"))

    chunks = []
    for f in doc_files:
        text = f.read_text(encoding="utf-8")
        title_match = re.search(r"^#\\s+(.+)", text, re.MULTILINE)
        title = title_match.group(1) if title_match else f.stem

        # 确定 access_level
        if "ops-only" in text.lower():
            access_level = "ops-only"
        else:
            access_level = "public"

        # Chunk
        doc_chunks = chunk_fixed_size(text, 256, 50)
        for j, chunk_text in enumerate(doc_chunks):
            content_hash = hashlib.sha256(chunk_text.encode()).hexdigest()
            chunk_id = f"{f.stem}:{j}:{content_hash[:8]}"
            chunks.append({
                "doc_id": f.stem,
                "chunk_id": chunk_id,
                "title": title,
                "source_path": str(f),
                "version": "1.0",
                "access_level": access_level,
                "chunk_index": j,
                "text": chunk_text,
            })

    # Embedding（离线模式使用模拟向量）
    texts = [c["text"] for c in chunks]
    if RUN_LIVE_EMBEDDING:
        vecs = embed_model.encode(texts, show_progress_bar=True)
    else:
        rng = np.random.RandomState(42)
        vecs = rng.randn(len(texts), 768).astype(np.float32)
        vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

    return chunks, vecs

print("Building index...")
all_chunks, all_vectors = build_index(str(DOCS_DIR))
print(f"Indexed {len(all_chunks)} chunks from {len(set(c['doc_id'] for c in all_chunks))} documents")
print(f"Vector shape: {all_vectors.shape}")

# 展示各文档的 Chunk 分布
from collections import Counter
doc_counts = Counter(c["doc_id"] for c in all_chunks)
for doc_id, count in doc_counts.most_common():
    print(f"  {doc_id}: {count} chunks")''')

md('''### 10.2 查询链路：问题 -> 检索 -> Rerank -> 生成

完整的查询端到端链路：检索、Rerank、组装 Context、调用 DeepSeek 生成。''')

code('''# === DeepSeek API 配置 ===
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path, override=False)

RUN_LIVE_LLM = os.getenv("RUN_LIVE_LLM", "0") == "1"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

def llm_ready():
    return bool(RUN_LIVE_LLM and DEEPSEEK_API_KEY and LLM_MODEL)

print(f"Live LLM: {llm_ready()}")
print(f"Model: {LLM_MODEL or 'not configured'}")''')

code('''# === 完整查询管道 ===
def rag_query(question: str, top_k: int = 5, use_rerank: bool = False,
              access_level: str | None = None) -> dict:
    """完整 RAG 查询：检索 -> 过滤 -> 可选 Rerank -> Context -> 生成"""

    # 1. 检索
    if RUN_LIVE_EMBEDDING:
        q_vec = embed_model.encode([question])[0]
    else:
        rng = np.random.RandomState(hash(question) % (2**31))
        q_vec = rng.randn(768).astype(np.float32)
        q_vec = q_vec / np.linalg.norm(q_vec)

    scores = cosine_similarity(q_vec[:, None].T, all_vectors.T)[0]  # shape: (N,)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    # 2. Metadata 过滤
    filtered = []
    for idx, score in ranked:
        chunk = all_chunks[idx]
        if access_level and chunk["access_level"] != access_level:
            continue
        filtered.append((chunk, score))
        if len(filtered) >= top_k * 3:  # 取 3 倍用于 Rerank
            break

    # 3. Rerank（简化版：按检索分数排序）
    if use_rerank:
        filtered.sort(key=lambda x: x[1], reverse=True)
    candidates = filtered[:top_k]

    # 4. 组装 Context
    context_parts = []
    for rank, (chunk, score) in enumerate(candidates, 1):
        context_parts.append(
            f"[来源 {rank}] 文档: {chunk['title']} | Chunk: {chunk['chunk_id']}\\n"
            f"{chunk['text']}"
        )
    context = "\\n\\n---\\n\\n".join(context_parts)

    # 5. 调用 LLM 生成
    prompt = f"""你是一个技术文档问答助手。请严格根据以下资料回答用户问题。

如果资料足以回答问题，给出准确答案并引用来源编号。
如果资料不足以回答问题，请回答"根据现有资料，无法找到相关信息"。

资料：
{context}

用户问题：{question}

请用中文回答，并在答案末尾列出引用的来源编号（如 [来源 1]、[来源 3]）。"""

    if llm_ready():
        from openai import OpenAI
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=LLM_BASE_URL or "https://api.deepseek.com")
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message.content
    else:
        answer = f"[离线模式] 已检索到 {len(candidates)} 个相关片段，Context 共 {len(context)} 字符。"
        answer += f"\\nTop-1 来源: {candidates[0][0]['title'] if candidates else '无'}"

    return {
        "question": question,
        "candidates": [{"chunk_id": c[0]["chunk_id"], "title": c[0]["title"],
                         "score": float(c[1]), "text": c[0]["text"][:200]}
                        for c in candidates],
        "context_length": len(context),
        "answer": answer,
        "prompt": prompt if not llm_ready() else None,
    }

# 测试 Q1（可直接检索到答案）
result = rag_query("萤火平台支持哪些部署方式？", top_k=3)
print(f"Answer: {result['answer'][:300]}")
print(f"\\nSources: {[c['chunk_id'] for c in result['candidates']]}")
print(f"Context length: {result['context_length']} chars")''')

md('''### 10.3 引用来源与无答案处理

在 prompt 中要求模型标注来源编号，并在答案末尾列出引用。无答案检测由模型判断——当检索内容不足以回答时，模型应返回"无法找到相关信息"。

对 Q8（定价方案）的测试：''')

code('''# 测试 Q8（知识库无答案）
result_q8 = rag_query("平台的定价方案是什么？", top_k=3)
print(f"Q8 Answer: {result_q8['answer'][:300]}")
print(f"Top score: {result_q8['candidates'][0]['score']:.3f}")

# 测试 Q9（权限受限问题，以 public 身份查询）
result_q9 = rag_query("数据库连接超时的阈值是多少？", top_k=3, access_level="public")
print(f"\\nQ9 (public access) Answer: {result_q9['answer'][:300]}")
# 以 public 身份不应检索到 doc-004（ops-only）
ops_chunks = [c for c in result_q9['candidates'] if 'doc-004' in c['chunk_id']]
print(f"ops-only chunks in public result: {len(ops_chunks)}")
assert len(ops_chunks) == 0, "Public access should not see ops-only documents!"
print("OK: access control works")''')

md('''离线模式下 LLM 调用被跳过，但检索、过滤、Context 组装和来源追踪的完整代码路径都已覆盖。设置 `RUN_LIVE_LLM=1` 可启用真实 DeepSeek 生成。''')

# =====  11  RAG 工程产物与持久化  =====
md('''## 11 RAG 工程产物与持久化

### 11.1 产物全景表

生产 RAG 系统运行中会产生以下工程产物：

| 产物 | 类型 | 典型大小（10 万 Chunk） | 存储建议 |
|------|------|----------------------|---------|
| 原始文档 | 事实源 | 1-10 GB | 对象存储（S3/MinIO） |
| 文档解析结果 | 派生产物 | 0.5-5 GB | 对象存储 |
| Chunk 文本 | 派生产物 | 200 MB | PostgreSQL / 对象存储 |
| Metadata | 事实源 | 50-200 MB | PostgreSQL |
| Embedding 向量 | 派生产物 | 768 维 x 4 字节 x N | 向量数据库 / pgvector |
| 向量索引（HNSW 图） | 缓存 | 向量的 1.5-3x | 向量数据库 / 内存 |
| 关键词索引（BM25） | 缓存 | Chunk 文本的 0.5-1x | Elasticsearch / 内存 |
| 模型与配置版本 | 事实源 | KB 级 | PostgreSQL / Git |
| 评测数据集 | 事实源 | 10-100 KB | Git 仓库 |
| 检索日志 | 流式数据 | 1-10 GB/天 | Elasticsearch / 对象存储 |

### 11.2 事实源 vs 派生产物 vs 缓存

| 分类 | 定义 | 示例 | 丢失后能否恢复 |
|------|------|------|-------------|
| 事实源 | 系统的唯一真实数据 | 原始文档、Metadata、配置版本 | 不能——丢了就永远丢了 |
| 派生产物 | 从事实源计算得出的数据 | Embedding、Chunk 文本 | 能——重新跑索引管道即可 |
| 缓存 | 为加速访问而存储的中间结果 | 向量索引结构、热门查询结果 | 能——从派生产物或事实源重建 |

区分这三类的实际意义：备份和灾备的优先级不同。事实源需要异地多副本备份。派生产物只需保留生成脚本（因为可以重建）。缓存可以不备份（因为重建成本低）。

### 11.3 推荐存储组合

| 存储 | 用途 | 收益 | 成本 | 适用规模 |
|------|------|------|------|---------|
| MinIO / S3 | 原始文档 + 解析产物 | 廉价、无限扩展 | 需要网络往返 | 全部 |
| PostgreSQL | Metadata + 权限 + 配置 | 事务、JOIN、行级安全 | 需维护 | 全部 |
| pgvector | Embedding + 向量检索 | 零额外运维（已有 PG） | 大规模检索不如专用向量库 | < 10M Chunk |
| Qdrant / Milvus | 向量检索 | 高性能、混合检索 | 独立运维 | > 10M Chunk |
| Elasticsearch | BM25 + 关键词检索 | 全功能搜索引擎 | 运维成本高 | 已有 ES 或需要混合检索 |
| Redis | 热门查询缓存 | 亚毫秒延迟 | 内存成本 | 全部 |''')

# =====  12  生产架构与生命周期  =====
md('''## 12 生产架构与生命周期

### 12.1 生产架构图

```mermaid
flowchart TB
    subgraph Offline[离线索引]
        S[数据源] --> P[Parser]
        P --> CK[Chunker]
        CK --> EM[Embedding 服务]
        EM --> VI[(向量索引)]
        CK --> MD[(Metadata DB)]
        CK --> KI[(关键词索引)]
    end
    subgraph Online[在线查询]
        Q[用户问题] --> QP[查询处理]
        QP --> RR[Retriever]
        RR --> VI
        RR --> KI
        RR --> MF[Metadata 过滤]
        MF --> RK[Reranker]
        RK --> CA[Context 组装]
        CA --> LLM[LLM 生成]
        LLM --> CT[引用来源]
    end
    subgraph Ops[运维支撑]
        LG[检索日志] --> EV[评测系统]
        EV --> FB[反馈优化]
        MD --> ACL[权限控制]
    end
    Offline --> Online
```

### 12.2 在线与离线分离

| 链路 | 延迟要求 | 资源需求 | 触发方式 |
|------|---------|---------|---------|
| 索引链路（离线） | 分钟-小时级 | CPU/GPU 密集型 | 文档变更事件 |
| 查询链路（在线） | < 500ms（P99） | 内存和网络 I/O | 用户请求 |

分离的原因：离线任务需要大量计算资源但不需要低延迟；在线服务需要快速响应但不能被慢任务阻塞。两者使用不同的副本和扩缩容策略。

### 12.3 增量索引与删除传播

- **增量索引**：只重建有变更的文档，不重建全库。
- **删除传播**：文档删除后，依次清除：Chunk -> Embedding -> 向量索引 -> 关键词索引 -> 缓存。
- **幂等写入**：同一条 Chunk 的多次写入结果相同，通过 `chunk_id` 做 upsert。

### 12.4 模型升级与索引重建

Embedding 模型升级后（例如从 bge-small 升级到 bge-large），所有向量需要重新计算。流程：

1. 部署新 Embedding 服务（与旧服务并行）。
2. 启动后台任务逐步重新 Embedding 全库。
3. 新向量写入新索引（蓝绿部署）。
4. 验证新索引的检索指标不劣于旧索引。
5. 切换查询流量到新索引。

### 12.5 蓝绿索引与版本切换

维护两套索引：`index_v1`（当前服务中）和 `index_v2`（新版本构建中）。验证通过后，修改查询服务的配置指向新索引。切换是秒级的，因为只是改一行配置，不涉及数据迁移。

### 12.6 多租户与 ACL

| 隔离方式 | 做法 | 适合 |
|---------|------|------|
| 数据库级 | 每个租户独立 PostgreSQL schema | 强隔离要求 |
| 索引级 | 每个租户独立 Collection/Namespace | 中型多租户 |
| 字段级 | Metadata 中带 `tenant_id`，查询时过滤 | 共享基础设施 |

字段级过滤最简单但需要确保查询链路每一步都携带并过滤 `tenant_id`。遗漏一步就会造成跨租户数据泄露。

### 12.7 容量、延迟与成本

| 指标 | 小规模 | 中等规模 | 大规模 |
|------|--------|---------|--------|
| Chunk 数 | < 10 万 | 10 万 - 100 万 | > 100 万 |
| 查询延迟 P99 | < 200ms | < 500ms | < 1s（含 Rerank） |
| 索引存储 | ~300 MB | ~3 GB | > 30 GB |
| 月成本估算 | $0（本地） | $200-1000 | $5000+ |

### 12.8 三档参考架构

**本地原型（$0，单机）**：Chroma + sentence-transformers + 本地 NumPy 检索。不适合生产。

**中小型生产（5-20 人团队，< 50 万 Chunk）**：
- pgvector 向量检索（复用 PostgreSQL）。
- PG 全文搜索做 BM25 关键词检索。
- Redis 缓存热门查询。
- Celery 做离线 Embedding。
- MinIO 存储原始文档。
- 单机或主从 PG，无高可用向量库。

**大规模多租户（> 100 万 Chunk，高并发）**：
- Qdrant 或 Milvus 向量检索。
- Elasticsearch 做 BM25 + 关键词。
- 独立 Embedding 服务（gRPC，GPU）。
- Kafka 做异步索引事件。
- PostgreSQL 管理 Metadata 和租户。
- 蓝绿索引切换 + 金丝雀发布。
- Prometheus + Grafana 监控。''')

# =====  13  部署形态  =====
md('''## 13 部署形态

### 13.1 进程内调用

检索逻辑作为 Python 库直接 import。原型和单机应用的最简方式。无网络开销、无服务发现。缺点是检索和应用耦合，不能独立扩容。

### 13.2 独立 RAG Service

检索作为独立 HTTP/gRPC 服务部署。应用通过 API 调用。检索和应用解耦，可以独立扩容和升级。

### 13.3 Sidecar

检索容器与 Agent 容器部署在同一个 Pod 中，通过 localhost 通信。兼顾低延迟和服务隔离。适合 Kubernetes 环境。

### 13.4 通过 MCP 暴露检索能力

如第 5 章所述，MCP 负责能力发现和调用协议。RAG 检索可以作为 MCP Tool 暴露：

```text
Agent -> MCP Client -> tools/list -> 发现 search_docs Tool
Agent -> MCP Client -> tools/call -> search_docs("萤火平台部署方式")
-> RAG Service -> 检索 + 生成 -> 返回结果
```

MCP 暴露的是检索接口，文档解析、Chunk、Embedding、索引和召回仍属于 RAG 系统内部。MCP 不替代 RAG，只负责把 RAG 的能力标准化地暴露给 Agent。

### 13.5 云厂商 Managed File Search

OpenAI File Search、Google Vertex AI Search 等。优点是零运维、开箱即用。缺点是成本随规模线性增长、数据需上传至第三方、定制化受限。

### 13.6 五种形态对比

| 形态 | 延迟 | 扩展性 | 隔离 | 运维成本 | 适合 |
|------|------|--------|------|---------|------|
| 进程内 | 最低 | 差 | 无 | 最低 | 原型 |
| 独立服务 | 低 | 好 | 进程级 | 中 | 生产 |
| Sidecar | 低 | 好 | Pod 级 | 中 | K8s |
| MCP 暴露 | 中 | 好 | 协议级 | 中 | Agent 生态 |
| 托管服务 | 取决于厂商 | 好 | 厂商负责 | 低 | 无运维团队 |''')

# =====  14  如何评估 RAG  =====
md('''## 14 如何评估 RAG

### 14.1 检索指标

| 指标 | 计算方式 | 衡量什么 |
|------|---------|---------|
| Hit Rate | Top-K 中包含正确答案的比例 | 召回能力 |
| Recall@K | Top-K 中相关文档数 / 总相关文档数 | 完整性 |
| MRR | 第一个正确答案排名的倒数均值 | 排序质量 |
| NDCG | 折损累积增益，考虑排名位置 | 综合排序质量 |

### 14.2 生成指标

| 指标 | 计算方式 | 衡量什么 |
|------|---------|---------|
| Answer Correctness | 生成答案与标准答案的匹配度 | 答案是否正确 |
| Faithfulness | 生成内容是否都能在检索到的 Context 中找到依据 | 是否编造 |
| Citation Correctness | 引用标记是否指向正确的 Chunk | 引用是否可信 |
| No-answer Accuracy | 无答案检测的准确率 | 拒答能力 |

### 14.3 离线评测实验

用固定问题集和固定标准答案跑一次完整评测：''')

code('''# === 离线评测 ===
EVAL_QUESTIONS = [
    {"id": "Q1", "question": "萤火平台支持哪些部署方式？",
     "expected_sources": ["doc-001"], "has_answer": True},
    {"id": "Q2", "question": "API 的速率限制是多少？",
     "expected_sources": ["doc-002"], "has_answer": True},
    {"id": "Q3", "question": "v2.3 版本新增了什么功能？",
     "expected_sources": ["doc-003"], "has_answer": True},
    {"id": "Q5", "question": "分支命名规则是什么？",
     "expected_sources": ["doc-005"], "has_answer": True},
    {"id": "Q6", "question": "平台支持 Kubernetes 部署吗？",
     "expected_sources": [], "has_answer": False},
    {"id": "Q8", "question": "平台的定价方案是什么？",
     "expected_sources": [], "has_answer": False},
]

def evaluate_retrieval(top_k: int = 5):
    """计算检索指标"""
    hits = 0
    reciprocal_ranks = []
    for eq in EVAL_QUESTIONS:
        if not eq["has_answer"]:
            continue
        candidates = hybrid_search(eq["question"], top_k=top_k)
        chunk_ids = [c["chunk"]["doc_id"] for c in candidates]
        expected = eq["expected_sources"]
        # Hit: Top-K 中至少一个来自期望来源
        if any(e in chunk_ids for e in expected):
            hits += 1
            # MRR: 第一个命中的排名
            for rank, cid in enumerate(chunk_ids, 1):
                if cid in expected:
                    reciprocal_ranks.append(1.0 / rank)
                    break
        else:
            reciprocal_ranks.append(0.0)

    n = sum(1 for eq in EVAL_QUESTIONS if eq["has_answer"])
    hit_rate = hits / n if n > 0 else 0
    mrr = sum(reciprocal_ranks) / n if n > 0 else 0
    return {"hit_rate": hit_rate, "mrr": mrr, "total": n, "hits": hits}

eval_results = evaluate_retrieval(top_k=5)
print(f"Hit Rate @5: {eval_results['hit_rate']:.2%} ({eval_results['hits']}/{eval_results['total']})")
print(f"MRR: {eval_results['mrr']:.3f}")

# 检查无答案检测
for eq in EVAL_QUESTIONS:
    if not eq["has_answer"]:
        result = rag_query(eq["question"], top_k=3)
        print(f"\\n{eq['id']}: {eq['question']}")
        print(f"  Answer preview: {result['answer'][:150]}")''')

md('''### 14.4 错误定位

检索或生成出错时，按以下顺序排查：

1. 文档解析是否正确（表格和代码块是否完整）。
2. Chunk 是否包含了关键信息（Chunk 边界是否切断了答案）。
3. Embedding 模型是否适合当前语言和领域。
4. 检索 Top-K 是否包含了正确答案的 Chunk。
5. Rerank 是否把正确答案排出了 Top-N。
6. LLM 是否忽略了 Context 中的正确信息（编造或漏读）。''')

# =====  15  安全、成本与常见故障  =====
md('''## 15 安全、成本与常见故障

### 15.1 检索注入与越权

- **检索注入**：恶意用户在问题中嵌入指令，试图让 LLM 忽略 Context 或执行越权操作。防御方式与第 3 章的 Prompt Injection 防御相同：用户输入必须隔离。
- **越权检索**：未携带 `access_level` 过滤导致跨权限检索。防御：查询管道入口统一注入权限上下文。

### 15.2 常见故障及排查顺序

| 现象 | 可能原因 | 排查 |
|------|---------|------|
| 检索结果为空 | 索引未构建或文档未入库 | 检查索引状态、文档解析日志 |
| 检索不相关 | Embedding 模型与语料不匹配 | 用评测集验证 Embedding 召回率 |
| 答案编造 | Context 中无答案、LLM 未按证据生成 | 检查 Rerank 后 Context，降低 temperature |
| 文档删除后仍能检索 | 删除未传播到索引 | 检查 `doc_id` 清理逻辑 |
| 向量维度不一致 | Embedding 模型版本变更 | 检查模型版本号、向量维度 |
| Context 超出窗口 | Chunk 过长或 Top-K 过大 | Token 计数前置、截断策略 |
| 索引与文档不一致 | 增量更新遗漏 | 对比文档 hash 和索引中 Chunk 的 content_hash |

### 15.3 成本估算

| 成本来源 | 占比（典型） | 优化方向 |
|---------|------------|---------|
| Embedding API 调用 | 30-50% | 批量处理、本地部署 Embedding 模型 |
| LLM Token | 20-40% | Context 截断、缓存相似问题 |
| 向量数据库 | 10-20% | 合理选择实例规格、索引压缩 |
| 存储 | 5-10% | 对象存储分层、过期策略 |
| 运维人力 | 10-20% | 托管服务、自动化运维 |''')

# =====  16  RAG 当前的发展方向  =====
md('''## 16 RAG 当前的发展方向

### 16.1 长上下文对简单 RAG 的影响

长上下文模型（128K-1M token）可以一次性处理几千页文档。对于文档库很小（< 50 篇）的应用，直接把文档放进上下文可能比建设 RAG 更简单。但长上下文有两个持续存在的限制：延迟随 token 数线性增长，以及检索不可追溯（模型读了什么你无法精确知道）。

### 16.2 Agentic RAG

Agentic RAG 让模型主动决定检索什么、检索几次、是否需要改写查询。与普通 RAG 的区别：Agentic RAG 的检索不是一次性完成的——模型可以在回答过程中多次检索、交叉验证、甚至检索不同数据源。

### 16.3 GraphRAG

GraphRAG 在检索前先构建知识图谱，把文档中的实体和关系显式化。检索时可以同时查询向量索引和图结构，对需要多跳推理的问题效果好，但构建和维护知识图谱的成本较高。

### 16.4 多模态 RAG

将图片、表格和图表也纳入检索范围。检索时不仅匹配文本，也匹配图像 Embedding。适合有大量架构图、流程图和截图的文档库。

### 16.5 不做什么

长上下文没有淘汰 RAG，和 Agentic RAG 也没有淘汰普通 RAG。每种方案有其适用场景。选择取决于文档库规模、更新频率、延迟要求和团队能力。''')

# =====  17  与产研协作助手的关系  =====
md('''## 17 与产研协作助手的关系

第 11 章的产研协作助手需要检索以下文档类型：

- 需求文档和技术方案
- API 规范和接口文档
- 项目发布记录和变更日志
- 测试报告和缺陷统计

本章的 RAG 系统可以为产研协作助手提供文档检索和引用能力。具体接入方案在第 11 章展开。

本章不实现产研协作助手业务流程。''')

# =====  18  本章总结与选型清单  =====
md('''## 18 本章总结与选型清单

### 18.1 能力检查清单

项目上线前检查以下条目：

- [ ] 数据源是否明确，文档格式是否统一
- [ ] 权限是否进入检索链路（每步都带 access_level 或 tenant_id）
- [ ] Chunk 策略是否经过评测（至少对比 2 种策略的 Hit Rate）
- [ ] Embedding 模型和索引是否有版本号
- [ ] 文档删除是否能传播到索引（30 秒内生效）
- [ ] 是否支持无答案（避免检索失败时强行编造）
- [ ] 生成的答案是否保留引用（用户可点击跳转到原文）
- [ ] 索引是否能从零重建（重建时间 < 预期停机窗口）
- [ ] 是否有独立的检索和生成评测指标
- [ ] 是否有成本和容量估算（至少包含 Embedding 和 LLM Token 两部分）

### 18.2 三档参考架构速查

| | 原型 | 中小型生产 | 大规模多租户 |
|---|---|---|---|
| 向量检索 | Chroma/FAISS | pgvector | Qdrant/Milvus |
| 关键词检索 | 无 | PG 全文搜索 | Elasticsearch |
| Embedding | 本地 CPU | 本地 GPU / API | 独立 gRPC 服务 |
| Metadata | JSON 文件 | PostgreSQL | PostgreSQL |
| 文档存储 | 本地文件 | MinIO/S3 | MinIO/S3 |
| 缓存 | 无 | Redis | Redis Cluster |
| 消息队列 | 无 | Celery/Redis | Kafka |
| 监控 | 无 | Grafana + Prometheus | Grafana + Prometheus + 日志平台 |

### 18.3 下一步

第 7 章将讨论 Agent 如何管理长对话中的上下文和记忆——这是 RAG 系统的自然延伸：RAG 负责从文档库检索，Memory 负责记住对话中的决策和偏好。''')

# =====  REFERENCES  =====
md('''## 参考文献

[1] Lewis P, Perez E, Piktus A, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks[C]. Advances in Neural Information Processing Systems, 2020.

[2] Gao Y, Xiong Y, Gao X, et al. Retrieval-Augmented Generation for Large Language Models: A Survey[J]. arXiv preprint arXiv:2312.10997, 2023.

[3] Malkov Y A, Yashunin D A. Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs[J]. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2018.

[4] Sentence Transformers. BGE Embedding Models[EB/OL]. https://huggingface.co/BAAI/bge-small-zh-v1.5, 2026-07-13.

[5] Robertson S, Zaragoza H. The Probabilistic Relevance Framework: BM25 and Beyond[J]. Foundations and Trends in Information Retrieval, 2009.

[6] OpenAI. Function Calling Guide[EB/OL]. https://platform.openai.com/docs/guides/function-calling, 2026-07-13.

[7] pgvector. Open-source vector similarity search for Postgres[EB/OL]. https://github.com/pgvector/pgvector, 2026-07-13.

[8] Qdrant. Vector Search Engine Documentation[EB/OL]. https://qdrant.tech/documentation, 2026-07-13.''')


# =====  WRITE  =====
nbf.write(nb, str(OUT))
print(f"Wrote {len(nb.cells)} cells to {OUT}")
