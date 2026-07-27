---
illustration_id: 01
type: framework
style: editorial
palette: macaron
language: zh
aspect: 16:9
output: ../01-framework-replan-routing.png
---

单 Agent Planning：失败后如何改道 - Conceptual Framework

Create one publication-ready 16:9 raster framework diagram for a Chinese technical tutorial. The image must explain the exact execution route, the failed step, and the new route inserted by replanning.

STRUCTURE: Three horizontal layers, read left to right, with one clear downward failure jump from the top layer to the middle layer and one recovery route across the bottom layer. Keep the diagram airy and immediately readable.

ZONES:

1. TOP LAYER — title label `初始计划`
   - Four rounded nodes connected left to right: `Goal` → `inspect` → `clean_v1` → `validate_v1`.
   - `inspect` and `clean_v1` have small green check marks.
   - `validate_v1` is the single failure node, emphasized in coral red with a clear cross icon.
   - Directly below that node, show the exact compact error label: `duplicate_order_id: A102`.
   - To the right, show `write_audit` as a faded disabled node. Draw a dashed crossed-out arrow from `validate_v1` to `write_audit`, labeled `原依赖失效`.

2. MIDDLE LAYER — central lavender decision module labeled exactly `Plan Patch`
   - A strong coral arrow drops from failed `validate_v1` into this module, labeled `失败证据`.
   - Inside or beside the module, use three very short callouts: `保留成功步骤`, `插入修复步骤`, `重接 audit 依赖`.
   - This layer visually communicates that completed work remains valid and only the unfinished route changes.

3. BOTTOM LAYER — title label `恢复计划`
   - Four mint/blue rounded nodes connected left to right: `deduplicate_r1` → `validate_r2` → `write_audit` → `succeeded`.
   - `validate_r2` has a green check mark and a tiny label `validation_passed`.
   - A thin connector from `clean_v1` down to `deduplicate_r1` is labeled `复用已有产物`.
   - A solid arrow from `Plan Patch` points to `deduplicate_r1` to make the jump destination unambiguous.

RELATIONSHIPS:
- Solid arrows mean active execution.
- Dashed crossed-out arrow means invalidated dependency.
- Coral means failure or rerouting.
- Mint means recovered success.
- Lavender means planning/control decision.

BOTTOM TAKEAWAY: one short line centered at the bottom: `失败后保留已完成步骤，只修改未完成计划`

LABELS: Use only the exact labels listed above. Keep code identifiers in Latin characters and explanatory labels in Simplified Chinese. Do not invent extra labels. Text must be large, crisp, correctly spelled, and readable at notebook width.

STYLE: High-quality magazine editorial explainer. Clean flat shapes, structured hierarchy, professional typography, thin charcoal outlines, restrained icons, generous white space, no characters, no photorealism, no decorative clutter, no gradients.

COLORS: Warm cream background (#F5F0E8); deep charcoal text and outlines (#2D2D2D); sky blue (#A8D8EA) for neutral information; mint green (#B5E5CF) for completed and recovered nodes; lavender (#D5C6E0) for Plan Patch; peach (#FFD5C2) for initial-plan grouping; coral red (#E8655A) only for `validate_v1`, the failure arrow, and crossed dependency.

Color values and color names are rendering guidance only. Do not display color names, hex codes, or palette labels as visible text in the image.

Clean composition with generous white space. Simple background. Main elements centered and aligned to a clear grid.

ASPECT: 16:9 landscape, medium information density, optimized for an article embedded at full notebook width.
