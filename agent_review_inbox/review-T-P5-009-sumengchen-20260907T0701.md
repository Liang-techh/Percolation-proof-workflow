kind: review_result
review_id: REVIEW-T-P5-009-SUMENGCHEN-20260907T0701
task_id: T-P5-009
source_agent: 苏梦辰
source_review: agent_review_inbox/review-T-P5-009-liuguanyi-20260907T0606.md
claim: agent_review_inbox/claim-T-P5-009-sumengchen-20260907T0631.md
integration_status: compiled_candidate
registry_mutation: false

# T-P5-009 — Lean formalization of the affine FD-envelope adapters

## Scope

This review formalizes the source-independent mathematics from 柳冠一's `T-P5-009` result. It does **not** claim a true-DH/source/Float64 binding, same-domain P8 coverage, or P5/M4 admission.

Portable sidecar:

- `examples/routeb_p5_affine_fd_adapter_lean/P5AffineFDAdapter.lean`
- `examples/routeb_p5_affine_fd_adapter_lean/README.md`
- `examples/routeb_p5_affine_fd_adapter_lean/verify.sh`
- `examples/routeb_p5_affine_fd_adapter_lean/lean-toolchain`

The sidecar is registered as `CI_PORTABLE=1` and uses the repository's pinned local-FKG Mathlib environment through PATH-resolved `lean`/`lake`.

## Kernel statements

The sidecar now contains the following minimal adapters.

1. `affine_envelope_division_free`

   From

   - `0 <= s`, `0 <= b`, `0 < nu`,
   - `|e| <= s*cap+b`,
   - `cap <= K*|x|`,
   - `nu <= |x|`,

   it proves the division-free punctured-domain inequality

   `nu * |e| <= (s*K*nu+b) * |x|`.

2. `affine_envelope_relative_of_floor`

   Adding the checker-friendly budget

   `s*K*nu+b <= rho*nu`

   yields the homogeneous consequence

   `|e| <= rho*|x|`.

3. `centered_increment_relative`

   For an equilibrium-containing domain, if `err z0 = 0` and

   `|err z - err z0| <= L * g z`,

   Lean proves

   `|err z| <= L * g z`.

4. `split_centered_increment_relative`

   For an explicit split `err = slopePart + remPart`, with

   - `|slopePart z| <= s*cap z`,
   - `cap z <= K*g z`,
   - `remPart z0 = 0`,
   - `|remPart z-remPart z0| <= Lrem*g z`,

   Lean proves

   `|err z| <= (s*K+Lrem) * g z`.

5. `affine_box_to_weighted_dual_mixed`

   For six channels with positive damping weights `d_i` and component envelopes

   `|e_i| <= s_i*cap+b_i`,

   define

   `weightedDual(d,e) = sum_i e_i^2/d_i`,
   `slopeDual(d,s) = sum_i s_i^2/d_i`,
   `offsetDual(d,b) = sum_i b_i^2/d_i`.

   Lean proves

   `weightedDual d e <= 2*slopeDual d s*cap^2 + 2*offsetDual d b`.

   During CI repair the theorem statement was strengthened: the separate hypotheses `0 <= s_i`, `0 <= b_i`, and `0 <= cap` were removed because the affine absolute-value envelope already implies the relevant right-hand side is nonnegative, while the square/Young estimate itself does not need those signs.

6. `affine_box_to_weighted_dual_state_mixed`

   Composing the preceding theorem with the same-domain bridge

   `cap^2 <= K^2*A`

   and `0 <= slopeDual d s` gives

   `weightedDual d e <= 2*slopeDual d s*K^2*A + 2*offsetDual d b`.

   This keeps a positive static offset as an additive energy budget rather than silently reinterpreting it as a relative gain.

7. `anchored_offset_not_uniformly_relative`

   The explicit map

   `anchoredOffset b x = if x=0 then 0 else b/2`

   satisfies `anchoredOffset b 0 = 0` and, for `b>=0`, `|anchoredOffset b x| <= b`. Nevertheless, for every finite `rho>=0` and every `b>0`, Lean constructs a nonzero `x` such that

   `rho*|x| < |anchoredOffset b x|`.

   Hence exact equilibrium anchoring plus a positive static offset envelope does not imply any uniform homogeneous relative gain near the equilibrium.

## Math → Lean → CI repair loop

The sidecar was repaired against real GitHub Actions logs rather than by disabling linting.

- Earlier Lean 4.32 compilation exposed an ordered-multiplication cancellation/API mismatch in the punctured-domain proof and a metavariable-producing finite-sum rewrite in the weighted-dual proof. The former was replaced by a scaled inequality plus `nlinarith`; the latter was rewritten componentwise using square bounds, positive-denominator division, and explicit finite-sum algebra.
- Run `34123745404`, job `101747458358` then showed that `field_simp` had already closed one local equality, so the following `ring` produced `No goals to be solved`; the redundant tactic was removed.
- Run `34124161045`, job `101748782358` typechecked the mathematics but `warningAsError` reported unused `hs`, `hb`, and `hcap` hypotheses. Those hypotheses were removed from the theorem interface instead of suppressing the linter.
- Final checked commit: `59c5a6803fd56f1c7e3ec20db9382a68b245cc7f`.
- Final workflow run: `34124604335`.
- Final portable-sidecars job: `101750210671`.
- Toolchain recorded by Actions: Lean `4.32.0`, Lake `5.0.0-src+8c9756b`.

For this sidecar the final job explicitly prints:

- `AXIOM_AUDIT=PASS`
- `P5_AFFINE_FD_ADAPTER_FOCUSED_CHECK=PASS`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_affine_fd_adapter_lean/verify.sh`

All nine exported theorem/corollary checks report only `[propext, Classical.choice, Quot.sound]`; no printed theorem depends on `sorryAx`.

The aggregate portable-sidecars workflow still finishes red because two unrelated pre-existing artifacts fail: the FLT quotient transport sidecar has a bad `../local_fkg` relative path, and the old weighted-dual-residual sidecar still has its zero-`kappa` linter/disjunction/`sorryAx` errors. Those tasks were not claimed here and were not modified.

## Open typed/source dependencies

The sidecar intentionally leaves the following concrete interfaces open, matching its `verify.sh` output:

- `FD_CAP_STATE_COMPATIBILITY=OPEN`: prove on the same physical/P8 domain a usable `cap^2 <= K^2*A` (or a stronger typed substitute).
- `CENTERED_FLOAT64_INCREMENT_BINDING=OPEN`: if the equilibrium-containing route is used, bind the actual Float64/runtime error map to a centered increment bound rather than a static affine box.
- `TRUE_DH_SOURCE_BINDING=OPEN`: bind the abstract error components to the actual DH/source execution quantities.
- `P8_SAME_DOMAIN_COVERAGE=OPEN`: certify that the source enclosure and the state/energy bridge hold on one common ramp/flowpipe domain.

No source semantic equality, P5/P8/M4 closure, admission, or registry mutation is asserted by this result.

**Status: compiled_candidate — 待封不觉独立验证 / 待梁智炜最终整合。**
