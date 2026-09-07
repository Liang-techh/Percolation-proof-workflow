# Route-B P4 scalar Young feasibility Lean sidecar

This portable sidecar formalizes the source-independent algebra from
`agent_review_inbox/review-T-P4-038-guyuefangyuan-20260907T1521.md`.

It freezes the one-row sign-robust Young cost

```text
(1+theta) A + (1+1/theta) P
```

and proves:

- exact multiplication identity and the division-free quadratic equivalence;
- necessity of `G=D-A-P>0` and `4*A*P <= G^2` for a feasible positive `theta`;
- the constructive rational witness `theta=G/(2*A)` and its exact gap;
- the historical `lambda=1+2*A/G` witness and the same exact gap;
- a strict-reserve specialization with `Gm=D-m-A-P`;
- exact rational success/failure sanity examples from the upstream review.

The constructive theorems deliberately do **not** carry a redundant `P>=0`
hypothesis once positive `G` and the discriminant inequality have already been
supplied.  The necessity theorem retains `P>=0`, because it is used to force
`G>0` from an arbitrary feasible row.

## Portable verification

The sidecar pins Lean `4.32.0` in `lean-toolchain` and reuses the repository's
pinned `examples/local_fkg` Lake environment.  `verify.sh` discovers `lake` and
`lean` from `PATH`, contains `CI_PORTABLE=1`, compiles with
`-DwarningAsError=true`, checks every public theorem has a `#print axioms`
report, and fails if `sorryAx` appears.

```bash
bash examples/routeb_p4_young_feasibility_lean/verify.sh
```

The repository workflow `.github/workflows/lean-agent-sidecars.yml` executes
this verifier on GitHub-hosted runners.

## Explicitly not proved here

This sidecar does not bind concrete P4 values of `A`, `P`, `D`, or `m`; it does
not prove the same-cell/common-`lambda` multi-row intersection from T-P4-039,
true-DH or Float64 evaluator semantics, trajectory/domain coverage, source
provenance/admission, registry mutation, or P4/M4 final closure.

Status after a successful compile remains `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
