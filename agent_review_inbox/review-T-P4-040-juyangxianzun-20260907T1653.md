# Review result — T-P4-040 rational common-lambda interval guard

- task_id: T-P4-040
- agent: 巨阳仙尊
- source_agent: 巨阳仙尊
- mathematical_source: `agent_review_inbox/review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md`
- status: compiled_candidate
- scope: Lean theorem decomposition + portable GitHub-CI sidecar for exact-rational common-`lambda` interval, rounding, and source-envelope algebra

## 1. Formalization result

Added portable sidecar:

`examples/routeb_p4_rational_lambda_guard_lean/`

Main Lean file:

`examples/routeb_p4_rational_lambda_guard_lean/P4RationalLambdaGuard.lean`

The checker-facing quadratic is

`quadratic P G A s = P*s^2 - G*s + A`, with `s = lambda - 1` in the intended P4 consumer.

The sidecar contains 14 public theorems:

1. `quadratic_chord_identity`
   - exact identity
   - `q((1-t)a+t*b) = (1-t)q(a) + t*q(b) - P*t*(1-t)*(b-a)^2`.
2. `convex_quadratic_endpoint_interval`
   - `P>=0`, `0<=t<=1`, and both endpoints nonpositive imply the convex-combination point is nonpositive.
3. `convex_quadratic_on_interval`
   - direct interval form: `P>=0`, `a<=s<=b`, endpoint checks imply `q(s)<=0`.
   - handles the degenerate `a=b` case separately and otherwise constructs `t=(s-a)/(b-a)` internally.
4. `common_lambda_interval`
   - arbitrary row-index type `ι`; one shared `[a,b]` plus rowwise endpoint checks implies every row passes for every `s` in the interval.
   - no `Fintype` premise is needed in the kernel theorem; a finite checker may instantiate `ι` with its row type.
5. `common_fixed_lambda_interval`
   - direct consumer for `1+a <= lambda <= 1+b`, proving all rows at `s=lambda-1`.
6. `quadratic_center_plus_identity`
   - exact expansion of `q(s0+r)`.
7. `quadratic_center_minus_identity`
   - exact expansion of `q(s0-r)`.
8. `symmetric_rounding_guard`
   - `P>=0`, `r>=0`, `|s-s0|<=r`, and the two endpoint checks at `s0±r` imply `q(s)<=0`.
9. `rounding_preserves_lambda_gt_one`
   - `r<s0` plus `|s-s0|<=r` implies `1 < 1+s`.
10. `source_envelope_quadratic_le`
    - on `s>=0`, if `P<=Pup`, `Glow<=G`, `A<=Aup`, then
      `q(P,G,A,s) <= q(Pup,Glow,Aup,s)`.
    - importantly, the true `P` need not itself be nonnegative.
11. `source_envelope_common_lambda_interval`
    - rowwise one-sided coefficient envelopes plus `Pup>=0` and two upper-envelope endpoint checks certify every allowed true coefficient realization throughout the common interval.
12. `concave_endpoint_failure`
    - exact counterexample showing endpoint-only certification fails when convexity is dropped.
13. `midpoint_margin_not_global`
    - exact counterexample showing a negative nominal midpoint value alone is not a rounding-radius certificate.
14. `negative_shift_envelope_failure`
    - exact counterexample showing the `s>=0` sign premise is essential for the `Glow<=G` envelope direction.

This decomposition intentionally keeps square roots, algebraic root storage, eigenvalues, matrices, and Float64 decisions out of the kernel-facing certificate.

## 2. Portable CI artifact

Added:

- `examples/routeb_p4_rational_lambda_guard_lean/lean-toolchain`
  - `leanprover/lean4:v4.32.0`
- `examples/routeb_p4_rational_lambda_guard_lean/README.md`
- `examples/routeb_p4_rational_lambda_guard_lean/verify.sh`

`verify.sh` is marked `CI_PORTABLE=1`, finds `lake`/`lean` from `PATH`, reuses the pinned repository `examples/local_fkg` Lake root, checks toolchain equality, compiles with `-DwarningAsError=true`, performs a placeholder scan, requires a `#print axioms` report for every public theorem, and rejects `sorryAx`.

No machine-specific absolute path is hard-coded.

## 3. Real GitHub Actions result

Final sidecar head used by the run:

`b759403c69510a0e551212402efbc7c5b726e75e`

GitHub-hosted run/job:

- workflow: `Lean agent sidecars`
- run_id: `34167818945`
- job_id: `101882271517`
- runner: Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

The real job log for this sidecar reports:

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P4_RATIONAL_LAMBDA_GUARD_FOCUSED_CHECK=PASS
P4_CONCRETE_DH_SOURCE_COEFFICIENT_BINDING=OPEN
FLOAT64_REALIZATION_CONTAINMENT=OPEN
P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN
P4_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_rational_lambda_guard_lean/verify.sh
```

All 14 public declarations report only:

`[propext, Classical.choice, Quot.sound]`

No theorem in this sidecar contains `sorryAx`.

## 4. Shared-workflow qualification

The shared workflow run is globally red because it executes all registered portable sidecars and several independent old lanes fail. The real log shows failures in, among others, FLT quotient path resolution, M4 cross-branch, P5 componentwise/parameter-tube/weighted-dual, P7 tail Schur, and P8 ramp reconstruction.

Those failures are independent of `routeb_p4_rational_lambda_guard_lean`; this sidecar itself reached its explicit `SIDECAR_RESULT=PASS`. I did not modify or claim those other lanes.

## 5. Formalized interface boundary

The useful downstream checker contract is now exact and small:

- choose one rational shared interval `0 <= s_lo <= s_hi` (or the intended stronger `0 < s_lo <= s_hi` at source level),
- for every row provide either exact `(P,G,A)` with `P>=0`, or an upper-envelope triple `(Pup,Glow,Aup)` with `Pup>=0`,
- prove the two exact endpoint inequalities,
- separately prove the implementation's realized `s_impl=lambda_impl-1` belongs to the certified interval.

The Lean consumer then certifies every interior rational/real value without recomputing roots.

Still open and deliberately not claimed here:

- concrete DH/source row coefficients or coefficient envelopes;
- concrete shared rational interval for the actual P4 cell family;
- true-DH / Float64 implementation containment in that interval;
- source hashes / admission / registry mutation;
- P8 same-domain trajectory/flowpipe coverage;
- P4/M4 final closure or integration.

## 6. Status

`compiled_candidate` only.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
