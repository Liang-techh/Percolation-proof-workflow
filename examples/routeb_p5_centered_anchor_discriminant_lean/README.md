# Route-B P5 centered/anchor discriminant Lean sidecar

Formalizes the exact-real parameter-elimination algebra from `agent_review_inbox/review-T-P5-021-honglianmozun-20260907T0800.md`.

The sidecar proves a generic `balanced_square_split`: for `D>0`, `X,Y>=0`, positive linear headroom `D-X-Y>0`, and strict discriminant `4XY < (D-X-Y)^2`, the explicit rational witness

`mu = (D+X-Y)/(2D)`

lies strictly in `(0,1)` and satisfies both strict square budgets `X < D mu^2` and `Y < D(1-mu)^2`. It then specializes this to the current P5 centered/anchor ledger, the `Vstar=1/4` checker, and the common physical-margin checker.

This is a source-independent exact-real child. It does **not** bind `ell2`, `B2`, `Vstar`, or `sigma` to deployed Julia/Float64 semantics, does not prove ODE continuation or P8 coverage, and does not close P5/M4 or alter registry state.

Focused verification:

```bash
./verify.sh
```

The script is portable for GitHub Actions (`CI_PORTABLE=1`), requires `lake`/`lean` on `PATH`, and reuses the repository-pinned `examples/local_fkg` Lake environment after checking the pinned toolchain.
