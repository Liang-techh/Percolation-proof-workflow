# T-P5-112 same-cell graph anchor-budget Lean sidecar

Owner/source agent: **巨阳仙尊**.

Mathematical input: `agent_review_inbox/review-T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z.md` by 古月方源, inspected at commit `3072f9b62a333f96448defd626a67039adb50168`.

This sidecar deliberately formalizes only the source-independent trusted seam that can be checked without inventing missing DH data.  Its public theorems cover:

- exact transport from `M a'' = J2`, a squared lower-gain hypothesis, and a correlated `J2` cap to the second-jet energy bound;
- the division-free final gate `4*gamma*q <= H2 <= 4*gamma*Danchor -> q <= Danchor`;
- the cell-radius specialization `4*gamma*q <= K2*S^2 <= 4*gamma*Danchor`;
- a scalar approximate-left-inverse triangle/square lemma and the corresponding preconditioned anchor-budget consumer;
- the `alpha(x)=x^3` regression showing that a second jet checked only at the anchor cannot certify a finite-segment affine remainder;
- the scalar `M=eps` regression showing that nonsingularity alone gives no uniform numerical anchor budget.

## Intentionally open interface

This is **not** a formalization of the full analytic/source theorem.  In particular, the sidecar does not manufacture or certify the deployed `D2M`, `D2R`, or `J2` evaluator; the physical `(q,v,w)` pullback; whole-segment `C^2`/same-cell coverage; the Taylor integral remainder/Jensen step that produces `4*gamma*q <= H2`; a real numeric `gamma`, `chi`, `H2`, `K2`, `S`, or `Danchor`; the downstream moving-metric comparator; Float64/controller equivalence; P8 flowpipe coverage; or registry admission.

Accordingly, `same_cell_graph_affine_anchor_budget_of_four_mul` and `preconditioned_anchor_budget` consume the analytic remainder inequality as an explicit typed hypothesis.  This prevents an anchor-point Hessian or mere invertibility fact from being silently upgraded to whole-cell coverage.

## Portable focused check

`verify.sh` is marked `CI_PORTABLE=1`, requires `lake` and `lean` on `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires the pinned `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, scans for `sorry`/`admit`, checks every public theorem has a `#print axioms` report, and rejects `sorryAx`.

Expected toolchain: `leanprover/lean4:v4.32.0`.

A green run is only **compiled candidate** evidence.  It remains **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
