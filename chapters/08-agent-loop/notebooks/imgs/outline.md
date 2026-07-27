---
type: framework
density: minimal
style: editorial
palette: macaron
language: zh
image_count: 1
---

## Illustration 1

**Position**: 第 7 节 / 7.1 完整实验代码之前

**Purpose**: 标出首次校验失败的位置，并展示计划如何跳转到修复分支、重接依赖并恢复执行。

**Visual Content**: 上方是初始计划；`validate_v1` 因 `duplicate_order_id: A102` 失败。失败证据进入 `Plan Patch`，保留已成功步骤，插入 `deduplicate_r1` 和 `validate_r2`，再把 `write_audit` 的依赖切换到二次校验。下方是恢复后的成功路径。

**Type Application**: 使用分层 framework 表达初始计划、重规划决策和恢复计划之间的关系；箭头同时承担执行顺序和依赖改写语义。

**Filename**: 04-framework-replan-routing-v4.png

**Selection**: v4。前三个候选图因箭头起点或跳转终点不准确而保留为迭代记录，不嵌入正文。
