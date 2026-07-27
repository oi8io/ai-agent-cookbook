---
illustration_id: 02
type: framework
style: editorial
palette: macaron
language: zh
aspect: 16:9
output: ../02-framework-replan-routing-v2.png
supersedes: 01-framework-replan-routing-v1.png
---

单 Agent Planning：失败节点与重规划跳转 - Conceptual Framework

Create one publication-ready 16:9 raster framework diagram for a Chinese technical tutorial. Accuracy of arrow origins and destinations is the highest priority.

LAYOUT: Three aligned rows. Use a strict grid. The failed `validate_v1` node, the `Plan Patch` module, and the recovery destination `deduplicate_r1` MUST share the same vertical center line. This creates one unmistakable top-to-bottom rerouting column.

TOP ROW — label `初始计划`
- Left-to-right active path: `Goal` → `inspect` → `clean_v1` → `validate_v1`.
- `inspect` and `clean_v1` have green check marks.
- `validate_v1` is coral red with a cross icon.
- Directly under `validate_v1`, inside the same node or immediately below it, show `duplicate_order_id: A102`.
- A faded `write_audit` node sits to the right of `validate_v1`.
- Draw one dashed crossed-out horizontal arrow from `validate_v1` to the faded `write_audit`, labeled `原依赖失效`.

MIDDLE ROW — one lavender module labeled `Plan Patch`
- Place it DIRECTLY BELOW `validate_v1`, never below `clean_v1` or `inspect`.
- Draw one thick coral vertical arrow whose origin visibly touches the BOTTOM CENTER of `validate_v1` and whose destination visibly touches the TOP CENTER of `Plan Patch`.
- Put the label `失败证据` beside that vertical arrow.
- Inside `Plan Patch`, show exactly three short lines: `保留成功步骤`, `插入修复步骤`, `重接 audit 依赖`.

BOTTOM ROW — label `恢复计划`
- Place `deduplicate_r1` DIRECTLY BELOW `Plan Patch`.
- Draw one thick solid arrow from the BOTTOM CENTER of `Plan Patch` to the TOP CENTER of `deduplicate_r1`.
- Continue left-to-right: `deduplicate_r1` → `validate_r2` → `write_audit` → `succeeded`.
- `validate_r2` has a green check and compact label `validation_passed`.
- Do not draw any other cross-row connector. In particular, do not draw arrows from `inspect` or `clean_v1` into the bottom row.

BOTTOM TAKEAWAY: `失败后保留已完成步骤，只修改未完成计划`

ARROW CONSTRAINTS:
1. Failure arrow starts only at `validate_v1` and ends only at `Plan Patch`.
2. Recovery arrow starts only at `Plan Patch` and ends only at `deduplicate_r1`.
3. The disabled dashed arrow starts at `validate_v1` and ends at faded `write_audit`.
4. No arrow may originate from `inspect` or `clean_v1` except their normal top-row execution arrows.

LABELS: Use only the exact labels above. Code identifiers stay in Latin characters; explanations use Simplified Chinese. Large crisp text, correct spelling, no extra text.

STYLE: High-quality magazine editorial explainer, clean flat shapes, precise grid alignment, professional typography, thin charcoal outlines, restrained check/cross icons, generous white space, no characters, no photorealism, no decoration, no gradients.

COLORS: Warm cream background (#F5F0E8); deep charcoal text and outlines (#2D2D2D); sky blue (#A8D8EA) neutral nodes; mint green (#B5E5CF) completed and recovered nodes; lavender (#D5C6E0) Plan Patch; peach (#FFD5C2) initial grouping; coral red (#E8655A) only failure node, failure arrow, and crossed dependency.

Color values and color names are rendering guidance only. Do not display color names, hex codes, or palette labels as visible text.

Clean composition with generous white space. Simple background. ASPECT: 16:9 landscape, medium information density, optimized for full notebook width.
