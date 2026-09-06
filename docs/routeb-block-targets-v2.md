# Original block targets: domain and terminal are different

Read-only inspection of `routeB_dense_Mq/routeB_pmi_certificate.jl` (SHA-256
`235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77`)
resolves an important distinction left incomplete in the first extraction.

- Lines 52-53 define domain weights `pw=[1.5,0.8]` and terminal weights
  `qw=[3,2]` separately.
- Lines 100-101 define `p=1.5*(q4²+q5²)+0.8*(v4²+v5²)` and
  `qpoly=3*(q4²+q5²)+2*(v4²+v5²)`.
- Line 291 uses the domain target `p<=eta=5.6` along the storage tube.
- Line 298 uses a **different** terminal target `qpoly(T)<=alpha=12`.

The requested theorem must preserve BOTH quantities and thresholds, as well
as the saved-V tube, original 12-dimensional initial set, disturbance family
and DH implementation semantics. An alternative proof certificate must still
imply the same requested properties.

Algebraically `2p<=qpoly<=(5/2)p`. Therefore p<=5.6 only implies qpoly<=14,
not the requested 12. The rational configuration q4=q5=v5=0, v4=5/2 has
p=5 and qpoly=25/2: it is a counterexample to this SET implication, not a
claimed trajectory counterexample from X0. A stronger p<=4.8 is sufficient
for the terminal condition, but should not replace direct qpoly comparison
if unnecessarily conservative.

`examples/routeb_implicit_port/BlockTargets.lean` formalizes these elementary
set comparisons. Compilation status is recorded separately with its real log.

The previous `ShiftBudgetObstruction.no_coarse_terminal_budget` declaration
contains threshold 28/5 literally. Despite its historical name, its scope is
the coarse p-domain budget, NOT a full formalization of the original terminal
qpoly/alpha condition. Its numeric obstruction remains true; interpret the
old progress report's phrase “terminal bound 5.6” as a terminology error.
Do not rewrite old proof logs or claim that the original terminal target was
refuted. The next DAG version should bind both domain and terminal statements.
