# RouteB concrete storage design, revision46

Delivered: an explicit sparse W0 storage coefficient vector from the permitted
second and final collocation LP; exact rational beta/initial-budget checks;
the requested exact ramp witness; and concrete obstructions to promoting the
sampled candidate to uniform zero-supply dissipation. **Full T=1 actual J<=1
remains OPEN.** This directory alone was written. State was revision46 at this
leaf's final read.

Coordinator update: the second zero-supply candidate is also **rejected** by
the separately owned exact source audit
`../routeb_storage_origin_gate/output/run-20260905T211357Z-f7fae1f0/results.json`.
At the allowed initial state q6=1/100, v6=-1/400, all other coordinates and
c zero, the audit reports initial norm squared 17/160000 and
Vdot=5421217529307363077/120000000000000000000000>0.
The coordinator reports exact Fourier M66/potential-line checks and a negative
determinant from the zero local qq66 and nonzero qv66 entries. This leaf did
not execute or independently reread that audit; its result and path were
supplied by the coordinator. This rejects the returned coefficient vector,
not the W0 family or the actual J target. Next frontier: the full 13x13 local
quadratic gate, or a certified positive supply within the remaining budget.

See [DERIVATION.md](DERIVATION.md) for the coefficients, P,k,z,Z, source
cancellations, initial/endpoint bounds, and the remaining certificate gates.
The final coefficient vector is in
[lp_candidate_evidence.json](output/lp-20260905T210840Z-ac3429b0/lp_candidate_evidence.json).

| Retained run | Outcome |
|---|---|
| `output/run-20260905T205645Z-63b40a65` | Earlier exact acceleration-storage construction; initial bound .0124658264613; one outer-endpoint obstruction. Historical, superseded by W0. |
| `output/lp-20260905T210233Z-e9203653` | First LP, 70 static points; candidate objective .3323448596441 after its recorded inflation/rounding; c coefficients zero; numerical violation 7.07175072e-8, **not feasible at 1e-8**. |
| `output/post-20260905T210708Z-19f7d8ba` | No optimization. Retained deterministic coefficient repair; exact actual-initial-direction and requested ramp obstructions. Repair also fails uniform zero-supply dissipation. |
| `output/lp-20260905T210840Z-ac3429b0` | Second/final LP, 80 static points including both obstructions and nine ramp rows. No coefficient inflation. Exact beta passes; initial expression .3343861976041548; numerical violation 2.46131304e-12. Still a candidate, and a1=0 obstructs uniform zero-supply closure near the terminal time. |

Every run contains `before_run.json`, copied code/inputs, `terminal.log`, and
`receipt.json`. All four exited zero with snapshot stability. The final LP's
receipt also reports all original inputs unchanged. Exit zero means execution
completed; it does not certify a mathematical target or a floating LP optimum.

Only two LP calls were made. No ODE/trajectory integrations, new sweeps,
dependency installations, browser calls, broad regression, Lean compilation,
registry changes, or other-directory writes occurred. Numerical residual
checks and the exact coefficient/initial checks have deliberately different
evidence status. No new formal theorem is claimed here.

The root scripts retain the latest versions; each old run's saved scripts are
authoritative for that run. In particular the first LP's script and plan were
not relabelled as the second LP. `verify_lp.py` now describes the second run;
it was not run a third time. The analysis below was written after the runs and
is not falsely presented as a pre-execution snapshot.
