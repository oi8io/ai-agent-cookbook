---
illustration_id: 04
type: framework
style: editorial
palette: macaron
language: zh
aspect: 16:9
output: ../04-framework-replan-routing-v4.png
supersedes: 03-framework-replan-routing-v3.png
---

单 Agent Planning：失败后跳入修复分支 - Conceptual Framework

Create a clean 16:9 editorial framework diagram. Use only two rows and a simple elbow-shaped reroute. Preserve the exact order of every node.

TOP ROW — `初始计划`
- Left to right: `Goal` → `inspect` → `clean_v1` → `validate_v1`.
- Green checks on `inspect` and `clean_v1`.
- `validate_v1` is coral red with a cross and exact error `duplicate_order_id: A102`.
- A faded disabled `write_audit` sits to the right.
- One dashed crossed-out arrow goes from `validate_v1` to faded `write_audit`, labeled `原依赖失效`.

LOWER ROW — `重规划后的路径`
- Put `Plan Patch` directly below `validate_v1`.
- One thick vertical coral arrow starts at the bottom of `validate_v1` and ends at the top of `Plan Patch`, labeled `失败证据`.
- Inside `Plan Patch`: `保留成功步骤`, `插入修复步骤`, `重接 audit 依赖`.
- To the RIGHT of `Plan Patch`, draw one straight active arrow to `deduplicate_r1`.
- Continue strictly left to right: `Plan Patch` → `deduplicate_r1` → `validate_r2` → `write_audit` → `succeeded`.
- Green check on `validate_r2`, with `validation_passed` below it.
- Do not draw any other arrow between rows. Do not place `deduplicate_r1` below or left of `Plan Patch`.

TAKEAWAY: `失败后保留已完成步骤，只修改未完成计划`

ARROW AUDIT:
1. Goal → inspect → clean_v1 → validate_v1.
2. validate_v1 - -X- -> disabled write_audit.
3. validate_v1 ↓ Plan Patch.
4. Plan Patch → deduplicate_r1 → validate_r2 → write_audit → succeeded.
5. Exactly these arrows, no others.

LABELS: Use only the labels listed above. Large crisp text. Keep identifiers in Latin characters and explanations in Simplified Chinese.

STYLE: Magazine editorial explainer, exact grid, flat rounded rectangles, professional typography, charcoal outlines, generous white space, no characters, no icons except check/cross, no gradients, no decorative elements.

PALETTE: warm cream (#F5F0E8), charcoal (#2D2D2D), sky blue (#A8D8EA), mint (#B5E5CF), lavender (#D5C6E0), peach (#FFD5C2), coral (#E8655A) only for failure and reroute. Never show color names or hex codes as visible text.

ASPECT: 16:9 landscape. Medium density. The arrow from `Plan Patch` to `deduplicate_r1` must be clearly connected at both ends.
