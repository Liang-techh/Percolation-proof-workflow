# Route-B P5 near-sharp scalar centered-gain Lean sidecar

This portable sidecar formalizes the source-independent mathematical child in
`agent_review_inbox/review-T-P5-027-kuangmanmozun-20260907T1044.md`, consuming
the arithmetic correction recorded in
`agent_review_inbox/companion-T-P5-027-kuangmanmozun-20260907T1048.md`.

It proves:

- the exact rational weighted comparison
  `(75/106) U + (106/75) N <= (47984317/10000000) Q` by an explicit rational
  LDL/SOS identity;
- the near-sharp division-free metric
  `400000000000000 U N <= 2302494677956489 Q^2`;
- a square-only scalar residual consumer under
  `2302494677956489*ell2 <= 400000000000000*mu^2`;
- the corrected old-minus-new constant difference
  `1505322043511/400000000000000`;
- the exact sharpness-bracket width and the integer lower witness
  `z0=(2379,73046,1832,68229)`.

The sidecar deliberately does **not** prove a concrete `ell2_path`/`K_path`,
Julia/DH/Float64 semantic binding, P8 path/cell coverage, ODE continuation,
source provenance/admission, registry mutation, or P5/P8/M4 closure.

Run the focused check with:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_near_sharp_centered_gain_lean/verify.sh
```

`verify.sh` locates `lake` on `PATH`, checks the pinned local Lake environment
and `lake-manifest.json`, compiles with `-DwarningAsError=true`, requires an
axiom report for every exported theorem, and rejects `sorryAx`/unknown-module/
Lean errors.
