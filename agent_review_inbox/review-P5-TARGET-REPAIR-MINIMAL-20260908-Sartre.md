---
kind: review_result
task_id: P5-TARGET-REPAIR-MINIMAL-20260908
agent: Sartre
status: candidate
integration_status: pending
original_nonnegative_target_at_witness: rejected
source_binding_proven: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# Minimal target repair: exact budget, baseline and decomposition boundaries

## 1. Decision

For the already established actual graph point q=v=0,w=1, a change of residual/port decomposition alone cannot restore the original nonnegative target: its exact value is negative before any Young relaxation. A genuine beta increment or a weaker target can restore pointwise allocation, but changes the statement or consumes an independently justified upstream budget. Recentring the nominal residual without compensation changes the measured target; compensating it preserves the original target and preserves the obstruction.

There are three distinct deficits, not one:

```
G = h-b                         intrinsic exact-target deficit
Gamma = 2h-b                    lambda=2 deficit with sharp point cap 0
Gamma_old = 2h-b+2d             lambda=2 deficit with existing global cap d
```

All are exact, positive and defined from the locked source below. G<Gamma<Gamma_old. Gamma_old is strictly between 1/2 and 3/5 in the source's scalar normalization. The thresholds below are necessary at this point and sufficient only for the displayed pointwise algebra; none establishes positivity on the whole cell or a repaired dynamical theorem.

Scope: only this immutable review was added. No Qs expansion, toy model, sampling, Lean/Lake, SDP, dynamics simulation, shared script/state/registry edit, or implementation of a proposed repair. The only computation was Fraction algebra on the previously established source witness, to simplify/check the repair inequalities. The previous full mass solve was not rerun.

## 2. Fixed source, metric, point and exact quantities

External root E: `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
Workspace root W: `C:/Users/z5242/Desktop/重构版/工作流`.

The fixed source is the analytic mass CSV plus (1/1000000) I6, the DH-gain analytic RHS, C-block=(4,5,6), D-block=(1,2,3), and nominal descriptor

```
aC = E_C alpha,  M alpha=R_DH,
A vD+(B-B0)aC=0,  r=M_CD vD,
ell=D_I fC-N0 aC,  lTotal=ell+r,
D_I=diag(1/5,1/10,1/20), H=N0^-1,
P=beta-lTotal' H lTotal.
```

At q=v=0,w=1, R_DH=GwI; the previous review checked all six graph equations exactly. Its source acceleration C-component is a=nC/D with

```
D = 55045306919641125471053338193373
nC = (15496010610460899685191174600000,
      57359628436617187133182572800000,
      82562335976049469352722168650000).

N0 = [[350003/3000000,0,1/60],
      [0,200739/4000000,0],
      [1/60,0,50003/3000000]]
H = [[50003000000/5000400003,0,-50000000000/5000400003],
     [0,4000000/200739,0],
     [-50000000000/5000400003,0,350003000000/5000400003]].
```

Define the following exact rational quantities; these finite expressions are also their precise coefficient specification:

```
k = (1/5,1/10,1/20)-N0*a = ell_* = lTotal_*,
S = a'a,
b = S/100+1/20 = beta_*,
h = k'Hk,
d = (589578/1000000)*
      ((133374/1000000)*a1^2+(50185/1000000)*a2^2+(33335/1000000)*a3^2).
```

Here a1,a2,a3 label physical joints 4,5,6, not remote acceleration. B-B0=0 gives r_*=0. d is the value of the **existing symbolic global cap**, not the true zero port norm. Its global enclosure proof remains pending; here only its exact numeric value in the allocation expression is used. N0/H and the force-like vector k retain the off-diagonal coupling and original units.

For exact reproducibility, writing
T=6758722017363098327650876161130774484190251396262627754497272897204629481055540 gives

```
G = 908496145006016245606224697730990370520062591844085847627884168761717525947223 / T
Gamma = 2385725165280437386413665293324305992717331018379028255833360562921055025947223 / T
d = 16679985913685612236554768565259685505490250470068766564369844793 /
    201999054258499411281123329601138458565684930158015886369407808600.
```

The Fraction calculation checked h>b, d>0 and 1/2<Gamma+2d<3/5. Previous b<9/100 and h>1/5 bounds already give G>11/100 and Gamma>31/100. No decimal estimate is used to justify a threshold.

Use q_H(x)=x'Hx and inner product <x,y>_H=x'Hy. beta, target t, Delta and q_H all have the same scalar charge units. lambda is dimensionless. An increment in the coefficient of w^2 has charge/input-squared units; one in |aC|^2 has charge/acceleration-squared units. Their values happen to be directly comparable at the normalized w_*=1 only after evaluating their monomials. No change to mass, regularizer, metric, source gains or normalization is proposed as a free repair.

## 3. Comparison at fixed lambda=2 and target t=0

| Proposed change | Exact pointwise threshold | Effect on original statement |
|---|---|---|
| beta -> beta+g | g_* >= Gamma+2 Delta_* with the original split | P_new=P_old+g; P_new>=0 gives only P_old>=-g unless independently funded |
| target floor 0 -> -tau | tau_* >= Gamma+2 Delta_* with the original split | Explicitly weaker conclusion P_old>=-tau |
| compensated split ell'=ell-u, r'=r+u | Best possible relaxed charge is h; b<h, so impossible without a budget/floor change | Total P, source and metric unchanged |
| uncompensated nominal recenter lTotal'=lTotal-gvec | 2 q_H(k-gvec_*) <= b when new port is zero | Measures a different residual; must rederive source/target join |

Delta_*=0 is the sharp point cap, whereas Delta_*=d preserves the actual current cap expression. A point cap of zero is not a license to set the port cap to zero away from this point. If a target t_*>0 is required, add t_* to every scalar budget/loss threshold in the first two rows.

## 4. Repair A: increase beta with an explicitly funded scalar increment

For lambda>1, let c_lambda=lambda/(lambda-1). With the original split and any chosen cap Delta_*>=0, the exact condition is

```
g_* >= t_* + lambda*Delta_* + c_lambda*h - b.
```

This is necessary and sufficient for nonnegative allocation at this fixed point. At lambda=2, sharp cap 0, the minimal increment is Gamma; retaining the old cap requires Gamma_old, not Gamma.

If beta's coefficients are changed by nonnegative delta_a and delta_w while retaining the source monomials, then

```
g_* = delta_a*S + delta_w.
delta_a*S+delta_w >= Gamma+2Delta_*+t_*.
```

Increasing coefficients of |qC|^2 or |vC|^2 alone has zero effect here. For one-coefficient repairs at lambda=2,t=0:

```
new beta_w >= 2h+2Delta_*-S/100,
new beta_a >= (2h+2Delta_*-1/20)/S.
```

These thresholds are exact rational expressions from section 2; S>0. No arbitrary coefficient fit is required. As a discriminating check on the existing rational design value 3/25, exact arithmetic gives

```
(3/25)*S+1/20 > 2h,
(3/25)*S+1/20 < 2h+2d.
```

Thus beta_a=3/25 is pointwise adequate **only with sufficiently improved cap**; it is rejected as a stand-alone repair retaining lambda=2 and the old global cap. This is not an endorsement of that coefficient on the full domain.

The intrinsic exact-target condition with zero port is only g_*>=G+t_*. With the original split, cap=0 and finite lambda, one needs the strict inequality g_*>G+t_* to find a usable lambda, specifically

```
lambda >= 1+h/(b+g_*-t_*-h).
```

At g_*=G+t_* the exact target is zero, but no finite lambda succeeds with the original split. For a fixed positive cap Delta_*, the minimum relaxed charge over lambda>1 is (sqrt(h)+sqrt(Delta_*))^2, attained at lambda=1+sqrt(h/Delta_*). This exact real optimization still leaves a positive deficit; tuning lambda alone does not repair b<h. It is not a proposed rational/compiled lambda witness.

Statement boundary: increasing beta changes the displayed P. If the intended theorem must remain P_old>=0, simultaneously require P_new>=g; then beta+g and target+g cancel in the allocation and no gain is obtained. Funding g from some other proven slack may preserve a larger final theorem, but that donor budget must be identified and debited. It is not supplied by the K schema or this review.

## 5. Repair B: change the target baseline, with both meanings distinguished

### B1. Lower the scalar target floor

Keep beta, source and residual unchanged and ask for P_old>=-tau. The original-split allocation condition is

```
tau_* >= lambda*Delta_*+c_lambda*h-b.
```

At lambda=2 this is Gamma (sharp cap) or Gamma_old (old cap). The strongest true pointwise floor is P_*=-G. The Young route's floor -Gamma is weaker by h when Delta=0. With the optimal compensated split in section 6, tau_*=G is sufficient for exact pointwise allocation equality. That still weakens the original nonnegative theorem; it does not prove it.

Since the system on the q=v=0 axis has alpha(w)=alpha(1)w and all displayed charges scale by w^2, tau(z)=Gamma*w^2 or Gamma_old*w^2 restores the corresponding fixed-split allocation along this entire axis, not just w=1. This follows algebraically from the exact graph, not from sampling. It is not a bound off that axis. A supply-rate interpretation would change the disturbance gain and needs its own storage/integration contract; a negative floor is not a stability or invariant-set theorem by itself.

### B2. Recenter the nominal force residual

If “baseline” means the reference vector, use a force-like correction gvec with the same units as lTotal and define

```
fC_new = fC-D_I^-1*gvec,
lTotal_new = lTotal-gvec             (if the old port is retained),
P_new-P_old = 2<lTotal,gvec>_H-q_H(gvec).
```

The actual dynamics M alpha=R and H may remain unchanged, but the residual being certified has changed. With r_*=0, lambda=2, sharp cap=0, restoring allocation requires exactly

```
q_H(k-gvec_*) <= b/2.
```

The minimum correction H-norm is sqrt(h)-sqrt(b/2), attained by an H-collinear correction. For gvec_*=c*k the exact condition is (1-c)^2<=b/(2h); a square-root threshold need not be rational. A concrete source-indexed recentering is gvec(z)=k*w using the rational k in section 2: then the new residual is zero on the q=v=0 axis. This specifies a mathematical candidate, not an implementation or a verified full-cell reference design.

At the witness its apparent gain is exactly h: P_new=b while P_old=b-h. To represent the old theorem faithfully, debit the correction C(z)=2<lTotal,gvec>_H-q_H(gvec) from beta, or prove P_new>=C. At the witness this requires b>=h and fails. If instead the shifted vector is added back to the port, it is merely the compensated decomposition below. Neither interpretation permits silently discarding the source force correction.

## 6. Repair C: preserve total residual and optimize the split

For any three-vector u, set ell'=ell-u and r'=r+u. At the witness lTotal=k and r=0, so any valid new cap has the form Delta'=q_H(u)+epsilon with epsilon>=0. Completing the square gives

```
lambda*Delta'+c_lambda*q_H(k-u)
= h + lambda^2/(lambda-1)*q_H(u-k/lambda) + lambda*epsilon.
```

The right-hand side is at least h because the actual H is positive definite. It follows that no compensated split can restore allocation with the original b and t>=0. This is an all-u algebraic obstruction, not a failed search.

The optimum is u=k/lambda with an exact cap epsilon=0. At lambda=2, ell'=k/2, r'=k/2, Delta'=h/4: the relaxed charge becomes h, not zero. Thus the split removes precisely the extra h of the old lambda=2, zero-port Young bound, but leaves G=h-b. It cannot remove intrinsic target negativity.

Combined minimal repairs at this point are now sharp and attained:

- beta increment g_*=G+t_* plus this optimal split and cap gives allocation equality;
- target floor t_*=-G with unchanged beta plus this split gives allocation equality.

These pointwise optima require a source-defined u(z) and a corresponding valid cap over the actual domain before they can be used globally. An old cap for r cannot be reused for r+u. Moving all residual into the port, or into the baseline, also pays its metric charge and cannot beat h.

## 7. Rejected alternatives and next hop

Rejected for the original nonnegative target and the stated domain:

1. Tune Q, lambda or the zero-port cap alone: even exact Delta=0 cannot overcome b<h.
2. Declare joint/remote terms inactive because r_*=0 and drop ell: ell_*=k is nonzero and source-bound.
3. Use beta_a=3/25 while keeping the old cap and lambda=2: fails the exact inequality above.
4. Increase q/v beta weights alone: their monomials vanish at the witness.
5. Recenter fC and omit the compensating force/target correction: changes the statement and is not a proof of the old one.
6. Compensate the split but retain the old port cap: the cap is for a different vector.
7. Diagonalize/scale H without a source-consistent metric transformation, or retune physical source gains/regularizer as a “budget” operation: changes metric, units or source.
8. Exclude w=1 by silently replacing measurable |w|<=2 with a ramp-only law: changes the domain/input quantifier. The DH/factorized damping difference vanishes at v=0 and does not remove this point.
9. Add g to both beta and target and claim new slack: the additions cancel; the old theorem remains obstructed.
10. Treat a repaired point or the entire origin-input axis as full-cell/trajectory coverage: off-axis source, storage, FD/runtime and domain obligations remain open.

Recommended mathematical next hop: first decide whether the larger intended theorem can legitimately supply an additive beta budget, or is willing to adopt an explicit negative/supply-rate floor or a recentered error target. Do not change any of these silently. If statement changes are not allowed and no donor budget is available, the existing displayed target cannot be repaired on this domain. If an authorized beta/floor adjustment is selected, the compensated split identifies the sharp pointwise minimum G; a proof route retaining the existing split/cap must budget Gamma or Gamma_old instead. No next-hop design is implemented here.

## 8. Recomputed source identities and validation scope

| Root/path | SHA-256 |
|---|---|
| E/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |
| E/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |
| E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| E/routeB_dense_Mq/routeB_factorized_descriptor_model.jl | C3007D5E30FEEB963A86B9589ADE3CA7D95B16316E753E8D18B007AA044CD427 |
| E/routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9 |
| E/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| W/agent_review_inbox/review-P5-K7-ACTUAL-Q-DELTA-PACKET-20260908-Sartre.md | 95F4913696A909364F907664CD22D28024568A3E28B9382917C9438600420E05 |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean | A76375770D563F86F7DE80FDEA970E8D0D0FADD1ED917C262B725C7A8BA47648 |

The prior review preserves the full graph witness, H inverse check and the remaining source hashes. The current turn re-read the actual descriptor/Schur definitions and generic consumer declaration; hashes above were recomputed. New Fraction-only design arithmetic exited 0 with `EXACT_POINT_REPAIR_ARITHMETIC_PASS`. The completed-square and statement-change identities are mathematical derivations, not executed Lean proofs. Status is candidate design / pending global source integration; the unmodified original target remains rejected at the witness. No VERIFIED or registry promotion is claimed.
