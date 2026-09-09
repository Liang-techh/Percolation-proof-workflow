---
kind: task_claim
task_id: T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T23:18:00Z'
lease_expires_at: '2026-09-10T00:18:00Z'
completed_at: '2026-09-09T23:31:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY, T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN, T-P5-193-AFFINE-BOX-DEFECT-BRIDGE]'
status: completed
result_path: agent_review_inbox/review-T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER-guyuefangyuan-20260909T2328Z.md
result_commit: f6a493131c273ba0739ede6c2f7a986b71660ae1
companion_path: agent_review_inbox/companion-T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER-guyuefangyuan-20260909T2330Z.md
companion_commit: 428a001ad4cb4425fd599de1bdfd09dd118d8b3c
---
# Review Claim — correlation-preserving zonotope defect adapter

## Scope
Close the next mathematics seam explicitly left by T-P5-193: replace the independent componentwise defect box by a shared-latent correlated zonotope `rho = Z diag(a(e)) xi`, `|xi|<=1`, with affine nonnegative amplitudes `a(e)=H e+h0`. Derive exact support identities, an exact facet-normal viability lift, and a finite sign-fan reduction of the frozen-selector Lyapunov defect to the existing copositivity machinery.

## Non-overlap
Do not redo T-P5-191 affine Metzler viability, T-P5-192 selector/KKT Dini theory, T-P5-193 box support, fixed copositivity algorithms, source provenance/admission, Lean compilation, or physical trajectory coverage. Preserve the distinction between an exact zonotope differential inclusion and a zonotope used only as an outer enclosure of a more correlated source residual.

## Intended deliverable
A minimal theorem package giving: (1) `sup w·rho = |Z^T w|·a(e)` and the matching infimum; (2) robust viability with `S=|N Z|`, `N A-S H=Lambda N`, `Lambda` Metzler, `N c>=S h0`; (3) a selector sign fan using `F=Z^T G` and an exact quadratic-plus-linear defect formula; (4) exact pullback to finite cone generators; and (5) a rational example proving the zonotope packet can strictly beat the independent coordinate-box hull while remaining fail-closed about source semantics.