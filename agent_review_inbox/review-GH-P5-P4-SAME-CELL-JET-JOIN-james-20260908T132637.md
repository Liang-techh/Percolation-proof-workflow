---
kind: review_result
review_id: review-GH-P5-P4-SAME-CELL-JET-JOIN-james-20260908T132637
task_id: GH-P5-P4-SAME-CELL-JET-JOIN
source_agent: James
created_at: 2026-09-08T13:26:37-06:00
inspected_commit: 769590f5f704a658607040739a90945ea5b5a6ec
status: pending
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_ANALYTIC_B_DB_BRIDGE_AND_PATH_JOIN_CONTRACT
source_binding_proven: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
---

# Same-cell jet join: controller identity, an analytic b/Db bridge, and the 13-to-4 seam

## Result and delta from prior reviews

There is a constructible conditional connection, but no complete same-cell
source-consumer packet was found in the inspected sources. Three useful deltas:

1. The current slab producer/checker and jet extractor use the SAME DH damping.
   Their controller agreement is visible in code, although the cell's
   `source_hashes` only records M/C/G. Add this missing identity edge; do not
   report a current controller mismatch merely because Fourier code is imported.
2. For an EXPLICIT choice of Fourier analytic nominal flow and DH analytic
   actual flow, b and Db can be defined by two exact linear descriptor equations
   using their known damping difference. They need not remain arbitrary fields.
3. A 6x13 acceleration jet does not by itself instantiate the existing 2x4
   K-path consumer. Its `state_bound` and `force_eq` require a same-witness path
   and anchor/fiber contract. This is distinct from finding an inverse or metric.

Only this immutable review is added. Source files and hashes were read; no
extractor, producer, slab checker, arithmetic regression, Julia or Lean was run.
No state/registry changes, synthetic packet, integration or admission occurred.

Prior inputs read: `NEW_REVIEW_P5_EXACT_DH_CELL_SOURCE_JET_CONTRACT_20260908.md`,
`NEW_REVIEW_P5_SAME_CELL_GRAPH_JET_ADDITIVE_CONTRACT_20260908.md`, the same-tube
and external-source-fields Sartre reviews, and James's additive-port and
metric-reference reviews at 130041/130629. Their existing graph/IFT, metric
inverse mismatch and Schur-budget analyses are retained, not re-audited here.

## 1. A real controller identity edge, currently missing from the cell key

External root E is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.

`robot_formal_v1/exact_checks/initial_analytic_slab.py:31` and
`check_initial_analytic_slab.py:48` use

```text
Kp = (1,4/5,7/10,3/5,1/2,2/5)
dDH = (13/10,11/10,19/20,4/5,13/20,1/2)
GwI = (1,1/2,3/10,1/5,1/10,1/20).
```

These match `routeB_compact_dh_gain_descriptor_regeneration_audit.jl:15-21`,
which the jet extractor parses. Both use analytic M/C/G, g0 at q=0, and mass
regularization 1/1000000 on the diagonal once. The slab encloses the RHS with
these gains; the jet gives its polynomial expression and physical derivatives.
The slab JSON pins only M/C/G, not this controller interpretation. Therefore
the appropriate new dependency is a controller/RHS equality certificate plus
the producer/checker code pins, not a guessed zero damping correction.

This is fresh text/byte evidence only. No claim is made that the stored bounds
were regenerated or independently checked this turn. The previous jet digest
`c1cee2bc333ead4211842a086e68fae4f52fc95400c78e729935abba19dec139`
is historical evidence from the source-jet review; the future checker must
recompute it. It is not a newly checked hash of emitted coefficients here.

## 2. Conditional exact b/Db from the existing two analytic controllers

Do NOT impose this split on an intended P5 source. If the caller explicitly
binds nominal fF to the historical Fourier analytic controller and actual fD
to the DH analytic controller, the shared mass yields a very small bridge.
From Fourier model lines150-156,

```text
dF = (9/5,7/5,19/20,1/2,13/20,4/5)
Delta = diag(dF-dDH) = diag(1/2,3/10,0,-3/10,0,3/10)
RD-RF = Delta*v.
```

On the SAME open neighborhood where M is C1 and nonsingular, define beta and
Z by the unique linear solutions

```text
M*beta = Delta*v
M*(Z h) = Delta*h_v - DM[h_q]*beta,       h=(h_q,h_v,h_w).
```

Together with the existing graph identities for alphaD/alphaF, these imply
beta=alphaD-alphaF and Z=D beta. With F=-fF, fD=(v,alphaD), the desired split is

```text
fD = -F+b,      b=(0,beta),      Db[h]=(0,Z h).
DF[h]=-(h_v,YF h),              YF=YD-Z.
```

Thus the existing DH jet plus this linear defect solve suffices to define the
Fourier nominal jet as well; a second symbolic inverse expansion is unnecessary.
This constructs conditional functions, not concrete certified bounds on them.
The sign is opposite to the descriptor difference: the regeneration code's
`descriptor_DH-descriptor_F=(dDH-dF)*v`, while the RHS difference is Delta*v.

This b is ONLY the ideal controller-damping difference. It excludes runtime
FD/libm/solve/IEEE defects and does not declare them zero. If the actual source
uses a different nominal split, its corresponding force defect and derivative
must replace Delta*v. The old residual interface's nominal cross-coupling is
not covered by this damping-only formula.

For a separately supplied full-state W(t,x), x=(q,v), this branch fixes
`Sb=DW[b]+Db^T W+W Db`. If W=W(q) is actually proved, DW[b]=0 because b_q=0,
not because beta=0. This useful simplification cannot be applied to a generic
W(q,v,t), a force metric, or an unbound matrix named W.

The actual variation is for fixed input w(t): use h_w=0 when forming D_x f.
For variations in the input, the extra acceleration term YD_w*delta_w belongs
in the separately defined variation forcing e; it must not be silently folded
into the state Jacobian. Measurable bounded w(t) supplies no time derivative.
No current variational defect, metric carrier or signed-rate certificate is
supplied by these equations alone.

## 3. Exact 13-to-4 path contract for the existing K consumer

Read `NEW_KPATH_INTERFACE_Core.lean:60-76,101-133`. It accepts a full witness
type X but its bound is homogeneous in z:X->R4, ordered (x4,x5,y4,y5), and its
output is two force coordinates. Neither z nor the physical residual is fixed
by a 13D mechanical jet. In particular y4/y5 cannot be silently renamed v4/v5.

One concrete implementable contract, conditional on the intended residual:

- Name a C1 source residual g:R13->Rm, an actual force map A:Rm->R2
  (i.e. a 2-by-m matrix), and a physical coordinate map z.
- For each full witness s, specify endpoints zeta_0(s),...,zeta_N(s) and the
  SAME residual increments de_j=g(zeta_(j+1))-g(zeta_j).
- Prove the whole straight segment for each pair stays in the jet's derivative
  domain. Endpoint membership alone is not that proof; alternatively provide
  a suitable non-straight path and its corresponding integral bound.
- Give exact nonnegative tables Hjac_j and Scoord_j with
  `|D_k g_i|<=Hjac_j[i,k]` everywhere on that segment and
  `|zeta_(j+1)[k]-zeta_j[k]|<=sum_l Scoord_j[k,l]*|z(s)[l]|`.
- Prove `rc(s)=A*sum_j de_j` for the actual centered force, not a similarly
  named acceleration or port. FTC then supplies the exact existing
  `increment_bound`, while the last two items are `state_bound`/`force_eq`.

For a direct mechanical port p=MBD*alphaD_remote, its derivative can use
DM and YD; for other residuals use their actual source formula. For block456
the port has THREE outputs, so it is not this Fin-2 force without a supplied
physical projection/identity. The generic P4 Schur consumer can instead use
n=3 and a cap, without claiming a K-path instance.

The minimal obstruction is at the anchor/fiber, before optimizing Hjac:
`ComponentBinding.zero_at_origin` requires rc(s)=0 for EVERY admitted witness
with z(s)=0, including its remote coordinates and input. If those can vary
independently, a full-state derivative bound alone does not imply this property
or `state_bound`. This is a necessary-condition obstruction, not a constructed
counterexample to the actual residual.

A fiberwise anchor with identical remote coordinates/input can avoid bounding
their increments by z, but then
`r_actual = rc + A*g(zeta_0) + remaining_bias` must be proved and the anchor
term retained in the additive branch. Do not assert it is zero. This is how the
same graph jet can support both a centered K-path and a P4 additive cap without
charging a port twice or inventing a remote homogeneous gain.

## 4. Executable packet join contract (proposed, no packet emitted)

Hash fields below are dependency identity, never mathematical evidence by
themselves. Canonical manifest bytes should use sorted keys, no floats, reduced
rational strings, ordered coordinate arrays, and explicit missing fields.

| Required record | Exact content and join condition |
|---|---|
| `analytic_source_key` | M/C/G, regeneration, imported model, extractor hashes; controller vectors/RHS identity, g0, regularizer semantics, c/s pullback and coefficient digest. |
| `domain_key` | Cell byte hash, exact q/v/w predicate, derivative neighborhood, input policy; producer/checker hashes plus their RHS-to-jet equality evidence. |
| `graph_key` | Above keys; M*alpha=R, M*Y=DR-DM*alpha; same valuation and nonsingularity/C1/total-unique evidence. |
| `split_key` | Explicit nominal and actual analytic source keys, sign convention, Delta/b/Z identities if using section2; separate runtime-refinement evidence when needed. |
| `carrier_key` | Physical z map, residual map, ordered B/D embeddings, force vs acceleration units, state/variation/input dimensions and transformations. |
| `metric_key` | Actual W/Wt/DW with carrier and derivative equalities; separately named port H and its linear transport T. Never join by equal dimension or the name W. |
| `path_key` | Endpoint maps, anchor, segment domains, Hjac/Scoord, increments, force_eq and anchor-bias identity; all reference the same graph/carrier keys. |
| `consumer_key` | Exact file hash and declaration, same valuation, metric normalization, cap/allocation or K comparison/gap/SPN witnesses; record which residual debit is consumed. |

For P4, `combined_of_port_budget` needs scalar cap Delta_port, not the P5
matrix W. Its path-independent branch can consume an actual H-metric graph
cap before Y, Db or a K-path is available. For P5 moving-metric kernels,
`P5MovingMetricContraction.lean` is explicitly a 2x2 scalar-coordinate algebra
leaf: a full 12D DF/W packet also needs a dimension-general theorem or a proved
restricted carrier/variation equation. Selecting two entries is not such a
restriction theorem.

Missing semantic evidence => pending. A present claimed equality contradicted
by exact data => reject that proposed join, not the underlying PDE/control
claim. Admission remains separately controlled; no metadata boolean may create
a proof inhabitant. Trajectory conclusions additionally require coverage and
continuation; no first-slab/local jet is promoted to whole-path closure.

## 5. Fresh input hashes

Paths starting `examples/` are under the workflow; other paths are under E.

| File | SHA-256 |
|---|---|
| routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| routeB_dense_Mq/routeB_analytic_gravity_cs_polynomial.csv | 2760489cba6dc2f2d25ac8f33fa5a25e430bb92040c022004d1ef949d3e09c5d |
| routeB_dense_Mq/routeB_analytic_coriolis_cs_polynomial.csv | cdc587afd26b2ab5498c5917e8c620e7c9aada8b2f5b4128c88df14e78b4e4bb |
| routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9 |
| routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl | 0fcf733144b3d7b1b08f328fe4ad24477057c56976f0ef53633c450d8fc4729d |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| robot_formal_v1/exact_checks/initial_analytic_slab.py | 97c96fb01bc9318af258a75d6b1371e3eef665fa760f401ce9f5a422ca164998 |
| robot_formal_v1/exact_checks/check_initial_analytic_slab.py | efa9f57d42e6cd70bd0cc5afdeef68a35673a880f5c53e992a2a182c4ca36340 |
| examples/routeb_p5_source_jet/NEW_EXACT_DH_CELL_JET_20260908.py | 3bd8ac1d468b6f73a5ff230f031ce3d38315b608c90ab0381762054bf0c5a6ae |
| examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Core.lean | 10c7e769e772a2f4475def1eb061e52319510cb906cb879c4234653f2d64a17c |
| examples/routeb_p5_moving_metric_contraction_lean/P5MovingMetricContraction.lean | e5950ad1b8ac474ddc814dd3fc993f68de128b5028d11726345e2b9ce3a44468 |
| examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean | a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648 |

Next smallest delivery: a separate keyed semantic join attachment proving the
DH RHS identity and actual residual/carrier/anchor identity, followed by either
the direct P4 graph cap or the K-path increment witness. The ideal b/Db branch
is available only if that nominal choice is intended. All concrete source,
metric, variation and admission claims remain pending.
