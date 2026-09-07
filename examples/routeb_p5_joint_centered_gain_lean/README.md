# Route-B P5 joint centered-gain Lean sidecar

This focused sidecar formalizes the source-independent mathematics from
`agent_review_inbox/review-T-P5-024-kuangmanmozun-20260907T0945.md`.

It proves, for the exact block-(4,5) dissipation quadratic `Q`,

```text
25 * U * N <= 144 * Q^2,
```

where `N = x4^2+x5^2+y4^2+y5^2` and
`U = (x4+y4)^2+(x5+y5)^2`.  The proof uses an exact rational LDL/SOS
certificate for

```text
(24/5) Q - (7/10) U - (10/7) N >= 0
```

and the square identity behind weighted AM-GM.  It then proves the generic
centered small-gain consumer

```text
rcSq <= ell2*N,
coupling^2 <= U*rcSq,
144*ell2 <= 25*mu^2
  -> |coupling| <= mu*Q,
```

plus a no-bias decay corollary, exact improvement arithmetic over the older
`2720*ell2 <= 457*mu^2` condition, and the rational `(0,15,0,14)` regression
witness ruling out the universal constant `23/4`.

The sidecar is intentionally independent of Julia/DH/Float64 semantics and of
the T-P5-023 cell/path transport.  It does **not** prove source Jacobian bounds,
anchor-bias bounds, P8 same-domain coverage, ODE continuation, provenance,
P5/P8/M4 closure, or registry admission.

Run from this directory with `./verify.sh`.  The script locates `lake` on
`PATH`, checks the pinned local Lake environment/toolchain, compiles with
`-DwarningAsError=true`, and rejects `sorryAx`/unexpected axiom diagnostics.

Status after a successful focused compile is only `compiled_candidate`:
待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
