---
illustration_id: 03
type: framework
style: editorial
palette: macaron
language: zh
aspect: 16:9
output: ../03-framework-replan-routing-v3.png
supersedes: 02-framework-replan-routing-v2.png
---

单 Agent Planning：失败节点与准确跳转目标 - Conceptual Framework

Create a publication-ready 16:9 raster framework diagram. This is a control-flow diagram; every arrow must preserve the exact execution order.

NON-NEGOTIABLE GEOMETRY:
- Build one vertical rerouting spine with exactly three nodes sharing the SAME x-coordinate:
  TOP: `validate_v1`
  MIDDLE: `Plan Patch`
  BOTTOM: `deduplicate_r1`
- Draw a straight vertical coral arrow `validate_v1` ↓ `Plan Patch`.
- Draw a straight vertical coral arrow `Plan Patch` ↓ `deduplicate_r1`.
- The second arrow MUST end at `deduplicate_r1`. It must never end at `validate_r2`.
- Place `validate_r2`, `write_audit`, and `succeeded` only to the RIGHT of `deduplicate_r1`.
- There must be no bottom-row node to the left of `deduplicate_r1`.

TOP — label `初始计划`
- Compact left-to-right path: `Goal` → `inspect` → `clean_v1` → `validate_v1`.
- Green checks on `inspect` and `clean_v1`.
- Coral failure node `validate_v1` with cross icon and exact error `duplicate_order_id: A102`.
- Faded disabled `write_audit` to the right, connected from `validate_v1` by one dashed crossed-out arrow labeled `原依赖失效`.

MIDDLE — label `计划修复`
- Lavender `Plan Patch` directly below `validate_v1`.
- The upper vertical arrow is labeled `失败证据`.
- Three short lines inside: `保留成功步骤`, `插入修复步骤`, `重接 audit 依赖`.

BOTTOM — label `恢复计划`
- `deduplicate_r1` directly below `Plan Patch`, at the start of the bottom execution path.
- Continue horizontally to the right: `deduplicate_r1` → `validate_r2` → `write_audit` → `succeeded`.
- Green check on `validate_r2`, exact small label `validation_passed`.

TAKEAWAY: `失败后保留已完成步骤，只修改未完成计划`

ARROW AUDIT:
1. Normal top path: Goal → inspect → clean_v1 → validate_v1.
2. Failed old dependency: validate_v1 - -X- -> faded write_audit.
3. Reroute: validate_v1 ↓ Plan Patch ↓ deduplicate_r1.
4. Recovery: deduplicate_r1 → validate_r2 → write_audit → succeeded.
5. No other arrows.

LABELS: Only the exact labels above. Large crisp text. Code identifiers in Latin characters; explanations in Simplified Chinese. No invented words.

STYLE: Magazine editorial explainer, precise grid, flat rounded nodes, professional typography, charcoal outlines, restrained check/cross icons, generous white space, no humans, no photorealism, no gradients, no decorative clutter.

PALETTE: warm cream background (#F5F0E8), charcoal (#2D2D2D), sky blue (#A8D8EA), mint (#B5E5CF), lavender (#D5C6E0), peach (#FFD5C2), coral red (#E8655A) only for failure and reroute.

Color names and hex codes are rendering instructions only; never show them as text. ASPECT: 16:9 landscape.
