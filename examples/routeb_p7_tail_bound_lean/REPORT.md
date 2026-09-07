# Route-B P7 tail bound report

Status: **LEAN_COMPILED_CANDIDATE — exact arithmetic only**

The external independent checker
`robot_final/verify_physical_rational_tail_global_bound.py` passed with seven
factorization terms and strict bounds for both `qmax=13/50` and `qmax=3/8`.
The Lean sidecar then reified the exact rational `rho`, inverse-block entries,
and `u1/u2` values and proved both strict inequalities with `norm_num`.

Focused Lean receipt:

- output: `output/run-pw9I9OSp`
- `TAIL_GLOBAL_BOUND_COMPILE_EXIT_CODE=0`
- `FOCUSED_CHECK=PASS`
- `EXACT_RATIONAL_TAIL_ARITHMETIC=PASS`
- OLean SHA-256: `c7bafd74dd6f413d025aadeadee3bb85979d3b5ffaaabfbbc019bd18bf2c1927`
- compile log SHA-256: `fa6ba98557988c422d7928f52d8f7f07b82aa5d8315237f048fddfbbe2ece4ad`
- axiom audit: only `propext`, `Classical.choice`, `Quot.sound`

The exact source/checker hashes are recorded in `compile_receipt.json`. The
physical source binding, full residual absorption, trajectory coverage,
terminal transfer, and registry admission remain false/open.
