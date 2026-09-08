# T-P4-044 shifted common-reserve Lean sidecar

Agent: **巨阳仙尊**

This sidecar formalizes the source-independent algebra from `review-T-P4-044-optimal-shifted-reserve-kuangmanmozun-20260907T1946`.

It contains:

- the exact quadratic chord identity;
- the ordered endpoint-to-parabola bound;
- the exact shifted square-completion identity;
- a division-free row consumer `common_interval_shifted_reserve_mul`;
- weak/strict charged-feasibility corollaries;
- an arbitrary-family common-witness theorem;
- the small-charge affine-center interval-membership lemma;
- exact rational regression where midpoint fails but the shifted witness succeeds;
- an exact wrong-branch counterexample showing `D >= 0` alone is insufficient;
- the sharp `m=1` boundary and `m>1` positive-witness obstruction for the extremal `[1,4]` row.

## Portable verification

The sidecar uses Lean `v4.32.0`, matching `examples/local_fkg/lean-toolchain`. `verify.sh` discovers `lake` and `lean` from `PATH`, reuses the pinned `examples/local_fkg` Lake environment, enables `-DwarningAsError=true`, checks every public theorem has an axiom report, rejects `sorryAx`, and carries the `CI_PORTABLE=1` marker consumed by `.github/workflows/lean-agent-sidecars.yml`.

```bash
bash examples/routeb_p4_shifted_common_reserve_lean/verify.sh
```

## Boundary

This sidecar does **not** bind concrete Route-B cells, DH/Float64 execution, source semantics, P8 trajectory/domain coverage, P4/M4 final closure, or registry/admission. It consumes only a previously certified common interval and a uniform lower curvature bound.

Status after a successful focused compile is only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
