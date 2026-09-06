# B45-5 descriptor residual terms adapter candidate

This independent Lean sidecar aligns the exact
`rho_kc=(q5/100,q4/200)` term with the existing six-term descriptor residual
ledger.  It keeps source binding as two explicit comparator premises and adds
no axiom.

Run `verify.sh` under WSL for the pinned, targeted Lean check.  This candidate
is not registered and does not modify the main theorem DAG or persistent state.
