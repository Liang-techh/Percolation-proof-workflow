# Task AE: exact terminal-cap leaf

`TerminalCapAE.lean` is a standalone exact-real Lean leaf. It proves

`p <= 24/5  ->  qpoly <= 12`

using the sharp coefficient comparison `qpoly <= (5/2) p`. It also exposes the
same implication through a direct storage comparison, so a different storage
`S` may be used if `qpoly <= (5/2) S` and `S <= 24/5` are proved.

The witness in the final theorem shows that the original set-level threshold
`p <= 28/5` does not imply `qpoly <= 12`; it only implies `qpoly <= 14`.
This is arithmetic/set-level information, not a dynamically reachable
counterexample.

Run only this leaf with:

```text
wsl -d Ubuntu -- bash examples/routeb_terminal_cap_ae/verify.sh
```

This leaf does not prove storage evolution, physical source binding, domain
coverage, continuation, or a flowpipe. In particular, it cannot replace the
flowpipe obligation.
