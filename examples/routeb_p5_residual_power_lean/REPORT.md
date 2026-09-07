# Route-B P5 residual-power child report

Status: **LEAN_COMPILED_CANDIDATE — exact scalar closure only**

The sidecar formalizes five exact consequences of
`y ≤ -δ*x^2 + ε*x`: the global upper bound, retained dissipation, a
parameterized Young family, the strict threshold, and strict decay under a
relative residual bound `ρ < δ`.

Focused receipt (2026-09-07):

- output: `output/run-4UQHUWtH`
- `DISSIPATIVE_RESIDUAL_POWER_COMPILE_EXIT_CODE=0`
- `FOCUSED_CHECK=PASS`
- `EXACT_DISSIPATIVE_CLOSURE=PASS`
- OLean SHA-256: `6d06e1ac82bf6a558f827a50ba2c3716e19defc1bc1f73e480b2e5bac5502529`
- compile log SHA-256: `6cbc21c11e9484c41b5c17fd5bc1ad98b81a489f53b605f317bd13f266fda20b`
- axiom audit: only `propext`, `Classical.choice`, `Quot.sound`

The DH dynamics, coercivity/residual premises, units conversion, domain
coverage, and M4 admission remain separate open obligations.
