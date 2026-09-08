# Review Result: T-P5-048 — singular rank-one Lyapunov boundary Lean sidecar

- `record_type`: `review_result`
- `review_id`: `T-P5-048-sumengchen-20260907T2223`
- `task_id`: `T-P5-048`
- `agent`: `苏梦辰`
- `source_agent`: `苏梦辰`
- `created_at`: `2026-09-07T22:23:00-06:00`
- `status`: `compiled_candidate`
- `admission`: `compiled_candidate`
- `math_source`: `agent_review_inbox/review-T-P5-048-honglianmozun-20260907T2150.md`
- `math_source_commit`: `da7a0f0995cfb633fa66ead4cad8ca3859af5eff`
- `claim`: `agent_review_inbox/claim-T-P5-048-sumengchen-20260907T2202.md`
- `claim_commit`: `f306bedd0eb389dd70f2ad5198f68f866eac1239`
- `final_sidecar_commit`: `0c8d05c55373b5ca2fb9e9590c073739999e3d69`
- `dependencies`: `T-P5-044` positive-definite signed/correlated 2x2 completion; 红莲魔尊 `T-P5-048` mathematical derivation
- `integration_scope`: source-independent singular rank-one algebra only; no P5/M4 parent-state, registry, admission, provenance, Float64, source, ODE, or P8 mutation

## 1. Implemented portable sidecar

Created:

- `examples/routeb_p5_singular_rank_one_lean/P5SingularRankOne.lean`
- `examples/routeb_p5_singular_rank_one_lean/README.md`
- `examples/routeb_p5_singular_rank_one_lean/verify.sh`
- `examples/routeb_p5_singular_rank_one_lean/lean-toolchain`

The sidecar pins `leanprover/lean4:v4.32.0`. `verify.sh` resolves `lake` and `lean` from `PATH`, reuses `examples/local_fkg/lake-manifest.json`, checks the toolchain match, runs with `-DwarningAsError=true`, performs `#print axioms` auditing, rejects `sorryAx`, and is registered with `CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`.

## 2. Kernel theorem decomposition

The sidecar defines

- `quad p q s u4 u5 = p*u4^2 + 2*q*u4*u5 + s*u5^2`,
- `bias b4 b5 u4 u5 = b4*u4 + b5*u5`,
- `det2 p q s = p*s-q^2`,
- `adjNumerator p q s b4 b5 = s*b4^2 - 2*q*b4*b5 + p*b5^2`,
- `decayRate r = (109-r)/200`.

Ten exported kernel statements are checked:

1. `rank_one_completion_identity`:
   under `p*s=q^2` and `p*b5=q*b4`,
   `4*p*(quad+bias)+b4^2 = (2*(p*u4+q*u5)+b4)^2`.

2. `rank_one_bias_completion_cleared`:
   division-free sharp completion
   `4*p*(-quad-bias) <= b4^2`.

3. `rank_one_bias_completion`:
   with `0<p`,
   `-quad-bias <= b4^2/(4*p)`.

4. `rank_one_kernel_quadratic`:
   for the explicit kernel ray `u=t*(-q,p)`, `quad=0` under `p*s=q^2`.

5. `rank_one_kernel_bias`:
   on the same ray, `bias=t*(p*b5-q*b4)`.

6. `rank_one_incompatible_no_uniform_upper_bound`:
   if `p*b5 != q*b4`, there is no finite `C` bounding `-quad-bias` uniformly along the kernel ray. This makes the range-compatibility obstruction a kernel theorem rather than a checker convention.

7. `rank_one_first_exit_gate`:
   from the caller's Lyapunov ledger, `V=1/4`, `0<p`, rank-one compatibility, and exact polynomial gate
   `200*b4^2 < (109-r)*p`,
   conclude `Vdot<0`.

8. `rank_one_parameter_tube_gate`:
   for nonzero `dc`, compatibility `p*g5=q*g4`, and
   `600*g4^2 < (109-r)*p`,
   the `Vd=dc^2/12` incremental ledger has `Vdot<0`.

9. `compatible_adjugate_numerator_identity`:
   under compatibility,
   `p*adjNumerator = det2*b4^2`.
   This is the exact algebraic bridge to the positive-definite T-P5-044 numerator.

10. `rank_one_interior_gate_collapses`:
    under `0<p`, `p*s=q^2`, and compatibility, both `det2=0` and `adjNumerator=0`; hence a checker cannot apply the unreduced strict-interior determinant gate at the singular boundary.

The source review also records `0<=r<=1`; the two consumer theorems do not need this as an algebraic hypothesis because the strict polynomial gate together with `p>0` is already sufficient. The deployed/source domain restriction on `r` remains a caller-side binding obligation.

## 3. Real CI failure and repair loop

### First real Actions run — failed focused sidecar

- workflow: `Lean agent sidecars`
- run: `34185877244`
- job: `101933988425`
- head: `c1c5a3871d8a3d486d6f784037e7d7e6ed7c2e3b`

The real Lean 4.32 log exposed one T-P5-048 blocker in `rank_one_incompatible_no_uniform_upper_bound`:

`change -(t * d) <= C at h` failed because the target had normalized to

`-0 - t * (p*b5-q*b4) <= C`

and was not definitionally equal to the requested pattern. In this failed run the dependent theorem temporarily reported `sorryAx`; the other nine exported theorems already typechecked with the standard axiom set.

### Repair

Commit `0c8d05c55373b5ca2fb9e9590c073739999e3d69` preserves the theorem statement and constants and replaces the fragile definitional `change` with an explicit transported equality

`ht' : t*(p*b5-q*b4) = -(C+1)`

followed by `rw [hq, hb, ht']` and `linarith`.

### Second real Actions run — focused sidecar PASS

- workflow: `Lean agent sidecars`
- run: `34186328016`
- job: `101935276275`
- head: `0c8d05c55373b5ca2fb9e9590c073739999e3d69`
- environment: Lean `4.32.0` commit `8c9756b28d64dab099da31a4c09229a9e6a2ef35`; Lake `5.0.0-src+8c9756b`; mathlib `81a5d257c8e410db227a6665ed08f64fea08e997`; formal-math `795efb86f191735c5481675763537cfb4ff37e55`

The real log for `examples/routeb_p5_singular_rank_one_lean/verify.sh` reports:

- `AXIOM_AUDIT=PASS`
- `P5_SINGULAR_RANK_ONE_FOCUSED_CHECK=PASS`
- `RANGE_COMPATIBILITY_REQUIRED=true`
- `T_P5_044_POSITIVE_DEFINITE_LAYER_NOT_REPLACED=true`
- `SOURCE_FLOAT64_BINDING=OPEN`
- `P8_ODE_COVERAGE=OPEN`
- `P5_M4_FINAL_INTEGRATION=false`
- `REGISTRY_MUTATION=false`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_singular_rank_one_lean/verify.sh`

All ten exported theorems report only `[propext, Classical.choice, Quot.sound]`; the focused sidecar has no `sorryAx`.

The aggregate portable-sidecars job is still red, but the same log shows T-P5-048 itself is green. Remaining aggregate failures are other pre-existing/unclaimed sidecars, including FLT quotient path handling, M4 cross-branch, P5 componentwise/direct-two-channel/parameter-tube/weighted-dual-residual, P7 tail-Schur, and the old P8 ramp-reconstruction sidecar. They were not modified in this task.

## 4. Formal interface boundary / remaining work

What is now closed is the source-independent nonzero rank-one 2x2 algebraic boundary: strict positive definiteness is not necessary if the bias is range-compatible, while an incompatible kernel component is formally unbounded.

Still open and intentionally not fabricated here:

- a source/checker branch dispatcher between T-P5-044 `det>0` and T-P5-048 compatible `det=0`;
- concrete same-domain extraction/binding of `p,q,s,b4,b5` and incremental `g4,g5` from deployed DH/residual data;
- exact/interval proof of the compatibility equalities in the actual source branch;
- the fully degenerate `H=0` endpoint (`b=0` zero cost versus `b!=0` unbounded) as a separate optional kernel child;
- true-DH / Float64 / FD / controller / solve execution semantics and remainder accounting;
- ODE first-exit/continuation and P8 same-domain flowpipe coverage;
- any parent-state, DAG, registry, admission, provenance, or final-result mutation.

`T-P5-048` therefore remains `compiled_candidate` only. **待封不觉独立验证 / 待梁智炜最终整合**。
