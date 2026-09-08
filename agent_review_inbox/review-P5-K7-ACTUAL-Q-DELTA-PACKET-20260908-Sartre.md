---
kind: review_result
task_id: P5-K7-ACTUAL-Q-DELTA-PACKET-20260908
agent: Sartre
status: pending
source_indexed_K_construction: candidate
current_block456_beta_target_feasibility: rejected
source_binding_proven: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# Actual block456 K7: source-indexed construction and an exact budget obstruction

## Outcome

There is a source-indexed algebraic choice of Q and Delta making K positive semidefinite; unrestricted K feasibility is not the essential bottleneck. Below it is constructed from the actual mass CSV, block456 port equations and nominal metric, not from a toy matrix. Its coefficient expansion and full-domain source proof are still pending.

More importantly, the existing block456 beta/nominal-residual target fails at an exact point of the full analytic acceleration graph: q=0, velocity=0, w=1. The remote port is zero there, but beta-lBase' H lBase < -11/100. Thus no Q/Delta satisfying the cap can make the current combined allocation nonnegative on a domain containing this point, for any lambda>1 and nonnegative requested target. This is an exact-rational source-artifact obstruction, not a Lean theorem, trajectory claim, Float64 runtime claim, or rejection of every possible redesigned P5 target.

Only this review was written. No source script, state, registry, shared adapter or older review was changed. No Lean/Lake, Julia producer, SDP, broad regression or extractor rerun was performed. Small read-only Python Fraction calculations evaluated the actual CSV at the origin, inverted rational matrices, checked the graph residual exactly and compared rational bounds.

## 1. Concrete field selection and source joins

External root E is `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`; D is E/`routeB_dense_Mq`. All paths in the hash table are relative to E.

Use human joint numbering throughout this review:

- D-block=(1,2,3), C-block=(4,5,6); E_D,E_C are the corresponding 3x6 selection matrices.
- z=(q1..q6,v1..v6,w), dimension 13. The 12 optional lift variables are (cos(qi),sin(qi)), not independent physical inputs. Actual mass support uses only joints 2..5.
- alpha is the full six-dimensional analytic acceleration, not the three-dimensional `vD456` variable.
- M(z)=the 296-row rational mass CSV plus (1/1000000) I6. `routeB_factorized_descriptor_model.jl` actually loads this same CSV as Mdirect; no separate mass-data file needs inventing. Its Jv/Jw factorization-to-Mdirect identity is a separate source/physical-lift gate, not implied by this shared filename.
- R=R_DH=-Kp*q-d_DH*v+G(0)+GwI*w-C(q)[v,v]-G(q), from the exact DH-gain regeneration. G and C are the hashed rational CSVs. G0=M alpha-R=0. This cap does not need the 78 G1 jet equations.
- A=M_DD, B=M_DC, Cb=M_CD, B0=B(0), N0=M_CC(0), each 3x3; H=N0^-1.

The descriptor's actual residual definitions are

```
A vD + (B-B0) aC = 0,
r = Cb vD,
lBase = D_I fC - N0 aC,
lTotal = lBase+r,
D_I = diag(1/5,1/10,1/20).
```

On the chosen full graph, bind aC=E_C alpha and define eta by A eta=E_D R-B0 E_C alpha; then vD=E_D alpha-eta. A must be nonsingular if uniqueness/elimination is claimed. The old `vD456` must never be replaced directly by E_D alpha.

The factorized source damping is (9/5,7/5,19/20,1/2,13/20,4/5), whereas d_DH=(13/10,11/10,19/20,4/5,13/20,1/2). In particular,

```
R_DH-R_factorized = (v1/2,3*v2/10,0,-3*v4/10,0,3*v6/10).
```

Keeping the existing fC as a deliberately selected nominal reference is mathematically possible, but does not make it the DH-gain nominal field. Replacing its damping by DH damping changes D_I fC by (-3*v4/10,0,3*v6/10); carry this change in the baseline or explicitly in the local defect, never silently. At the counterexample v=0, both versions coincide, so this mismatch cannot remove that obstruction.

The final join from lTotal to any claimed actual force/storage/variational target remains an explicit obligation. The present rejection concerns the displayed block456 descriptor target evaluated on the full analytic graph, not a different physical target that has not been identified with it.

## 2. Actual rational metric, not an unspecified H

Exact CSV origin substitution gives

```
N0 = [[350003/3000000, 0, 1/60],
      [0, 200739/4000000, 0],
      [1/60, 0, 50003/3000000]]

B0 = [[7/60, -21/80000, 1/60],
      [0, 41827/800000, 0],
      [0, 8189/160000, 0]]

H = [[50003000000/5000400003, 0, -50000000000/5000400003],
     [0, 4000000/200739, 0],
     [-50000000000/5000400003, 0, 350003000000/5000400003]]
```

N0 is symmetric; its leading minors are exactly
350003/3000000, 23419750739/4000000000000 and 334591765400739/4000000000000000000, all positive. Fraction arithmetic checked N0 H=I. Thus the supplied constant matrix has an exact positive-definiteness justification by Sylvester and inversion, without floating eigenvalues. This arithmetic evidence is not a formal/source admission receipt. Preserve the 4–6 off-diagonal coupling; H is not three independent scalar weights.

## 3. Source-indexed Q, L, d0 and Delta construction

This improves the previous review's adjugate route without discarding forcing. Let

```
delta = det A, J = adj A,
m = det M, N = adj M,
Lbar = -Cb J (B-B0) E_C                 # 3x6 polynomial
F = Lbar N                             # 3x6 polynomial
Ls = m Lbar                            # 3x6 polynomial
d0s = 0                                # 3-vector, justified below
Qs = F' H F                            # 6x6 symmetric polynomial
s = delta^2 m^2.
```

Each coefficient is rational, with M and all block selections fixed by the actual CSV. The adjugates are algebraic constructions, not floating inverses or new fitted model data. Qs is a newly specified certificate candidate, not an existing solver payload. Coefficient expansion/hashing of Qs has not been executed.

The nominal equation gives delta*r=Lbar*alpha. This is also consistent with the previous affine port representation:

```
Lold = Cb (delta E_D + J B0 E_C),
d0old = -Cb J E_D R,
Lold alpha+d0old-Lbar alpha = Cb J E_D (M alpha-R).
```

Thus d0s=0 is a graph-ideal rewrite, not omission of R: R remains in Qs's bottom-block contraction and in the actual acceleration. It applies to this pure nominal-subtracted port only. A real additional local defect must be retained; no claim of d0=0 is made for an unspecified full residual.

Define the scaled actual port ds=delta*m*r=Ls alpha and choose

```
Delta_s = R' Qs R + p(z),
K_s = [[M' Qs M-Ls' H Ls, 0],
       [0, Delta_s-R' Qs R]]
    = diag(0_6x6,p(z)),
Delta = Delta_s/s.
```

The identity follows from NM=mI, hence FM=m Lbar. For p=0 this is a source-indexed K_s=0 candidate, not a toy PSD witness. It measures the exact graph port rather than bounding it by an unrelated number. It proves only algebraic feasibility with a freely chosen, potentially unusably large cap. No allocation conclusion follows.

For this representation, K_s PSD is equivalent to p>=0. Restoring the physical cap requires delta*m != 0 on the physical cell. Qs,Ls,Delta_s have only fixed rational coefficient denominators; clear them with a single positive integer. Delta has the state-dependent denominator s, which requires a nonzero/positive-domain witness. No independent scaling of matrix blocks is permitted. The adjugate matrix identity itself holds even at singular points, but division back to the actual port does not.

If insisting on a cap without polynomially expanded inverse factors, the exact p=0 expression remains a rational-function candidate rather than an exported finite SDP payload. Its size and source identity must be checked; its mere definition is not an efficient implementation or a complete certificate.

## 4. What the actual allocation reduces to

The existing source selects lambda=2 and

```
beta = (1/100)|aC|^2 + (1/10)(|qC|^2+|vC|^2) + (1/20)w^2.
```

For requested lower target t(z), allocation requires Delta <= U, where
U=(beta-t-2*lBase' H lBase)/2. Substitute the actual graph using

```
ahat = E_C N R,
lhat = m D_I fC - N0 ahat,
betahat = (1/100)|ahat|^2
          + m^2*((1/10)(|qC|^2+|vC|^2)+(1/20)w^2).
```

Then the explicit Qs construction with the allocation-maximal cap Delta_s=s U has bottom entry S/2, with

```
S = delta^2*(betahat-m^2*t-2*lhat' H lhat) - 2*R' Qs R.
```

Consequently this exact-source route replaces a free K7 search by a scalar sign obligation S>=0, plus the denominator and source gates. This formula assumes t has an appropriate polynomial representation; any additional denominators in t require their own clearing. It does not assert S>=0. The following admissible graph point proves that the current t=0 choice cannot satisfy it on the full selected cell.

## 5. Exact graph counterexample: not a free-acceleration slice

Take q=v=0 and w=1. The domain artifact explicitly describes the full initial ball radius 3/20, measurable |w|<=2 and first slab; this state/input lies in its stated domain and in every displayed angle/velocity box. A constant w=1 is allowed there. No actual trajectory was integrated. A ramp-only input law or another smaller domain must not reuse this domain assertion without a separate join.

At this point R=GwI=(1,1/2,3/10,1/5,1/10,1/20); gravity cancels G(0)-G(0), and C[v,v]=0. Fraction Gaussian elimination of the actual regularized mass CSV gives alpha=n/D with

```
D = 55045306919641125471053338193373
n = (67072620432254444407085508000000,
     38059699292563014591671526000000,
     12771373085954591625310118400000,
     15496010610460899685191174600000,
     57359628436617187133182572800000,
     82562335976049469352722168650000).
```

All six entries of M(0) alpha-R were checked to be exactly zero. These accelerations are computed from source data, not independently assigned. At q=0, B-B0=0, so vD=0 and r=0 solve the nominal/port equations. Set aC=E_C alpha and lTotal=lBase. Also D_I fC=GwI_C at this state. Direct exact comparisons give

```
beta < 9/100,
lBase' H lBase > 1/5,
Pdirect = beta-lTotal' H lTotal < -11/100,
Aallocation(lambda=2,Delta=0,t=0) < -31/100.
```

Every valid cap at r=0 has Delta>=0. For any lambda>1 and t>=0,

```
Aallocation
= (lambda-1)*(beta-t-lambda*Delta)-lambda*lBase' H lBase
<= (lambda-1)*(beta-lBase' H lBase)-lBase' H lBase
< 0.
```

Thus no clever Q or tighter port estimate can repair this frozen target on a domain containing this point. This is stronger than the older free-aC origin-block diagnostic because the present alpha satisfies all six actual acceleration equations. It does not say K alone is infeasible: r=0 admits Delta=0, but even that optimal cap leaves a negative allocation. A proposed packet claiming both cap and nonnegative allocation for this fixed source target/domain should be rejected. A packet proposing a different target or input law remains pending until that change is explicit and justified.

For a compact independent reproduction, the following reads only the locked mass CSV; it writes nothing. After writing this review, this exact code block was extracted and executed with `python -B -c`: exit code 0 and `REVIEW_REPRODUCER_EXACT_ASSERTIONS_PASS`. It is embedded here, not saved as a separate checker artifact; this confirms its arithmetic assertions only, not formal admission:

```python
import csv
from fractions import Fraction as Q
from pathlib import Path
p = Path('C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv')
M = [[Q(0) for _ in range(6)] for _ in range(6)]
with p.open(encoding='utf-8-sig', newline='') as stream:
    for r in csv.DictReader(stream):
        if all(int(r['e'+str(k)]) == 0 for k in (2,4,6,8,10,12)):
            M[int(r['row'])-1][int(r['col'])-1] += Q(int(r['num']),int(r['den']))
for i in range(6): M[i][i] += Q(1,1000000)
D = 55045306919641125471053338193373
n = [67072620432254444407085508000000,38059699292563014591671526000000,
     12771373085954591625310118400000,15496010610460899685191174600000,
     57359628436617187133182572800000,82562335976049469352722168650000]
a = [Q(x,D) for x in n]
R = [Q(1),Q(1,2),Q(3,10),Q(1,5),Q(1,10),Q(1,20)]
H = [[Q(50003000000,5000400003),Q(0),Q(-50000000000,5000400003)],
     [Q(0),Q(4000000,200739),Q(0)],
     [Q(-50000000000,5000400003),Q(0),Q(350003000000,5000400003)]]
assert all(sum(M[i][j]*a[j] for j in range(6)) == R[i] for i in range(6))
assert all(sum(M[i+3][k+3]*H[k][j] for k in range(3)) == (i==j)
           for i in range(3) for j in range(3))
ell = [R[i+3]-sum(M[i+3][j+3]*a[j+3] for j in range(3)) for i in range(3)]
beta = Q(1,100)*sum(x*x for x in a[3:])+Q(1,20)
h = sum(ell[i]*H[i][j]*ell[j] for i in range(3) for j in range(3))
assert beta < Q(9,100) and h > Q(1,5)
assert beta-h < -Q(11,100) and beta-2*h < -Q(31,100)
```

## 6. Existing floating bounds and payload limits

The partition producer reads rational CSV coefficients into outward-rounded 256-bit BigFloat intervals, constructs the same reduced port -Cb A^-1(B-B0), and reports matching-metric `rho2_m0_upper` and Gershgorin `bdiag*_upper`. Its output is not a Q matrix. The common symbolic interface freezes the exact rational *numbers* 589578/1000000 and (133374,50185,33335)/1000000, but their status as uniform certified envelopes still needs the interval implementation, cover completeness, correct physical cell and outward-export evidence. Exact spelling of a rounded number does not establish the bound.

The interval dependency imports Float64 DH constants including the regularizer; equality/enclosure of the intended rational 1/1000000 must be checked, not presumed. This review did not revalidate that interval stack. The external-budget Python ledger additionally converts CSV values to Python float and computes diagnostic charges. Those decimal charges are not exact-rational PSD or allocation witnesses. Its negative coefficient budget entries alone were not used as the impossibility argument above.

The inspected block456 matrix-PMI CSV says ASSEMBLED_NO_SOLVE and matrix_dimension=4 (beta plus lTotal), not a 7x7 graph K certificate. It cannot fill the missing Qs/Delta_s coefficient packet. No actual source-indexed Q coefficient export or full-cell K/S positivity certificate was established by this targeted inspection; this is not an exhaustive claim about all files on the machine.

## 7. Source/artifact identities recomputed this turn

| Path relative to E | SHA-256 |
|---|---|
| routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |
| routeB_dense_Mq/routeB_analytic_coriolis_cs_polynomial.csv | CDC587AFD26B2AB5498C5917E8C620E7C9AADA8B2F5B4128C88DF14E78B4E4BB |
| routeB_dense_Mq/routeB_analytic_gravity_cs_polynomial.csv | 2760489CBA6DC2F2D25AC8F33FA5A25E430BB92040C022004D1EF949D3E09C5D |
| routeB_dense_Mq/routeB_factorized_descriptor_model.jl | C3007D5E30FEEB963A86B9589ADE3CA7D95B16316E753E8D18B007AA044CD427 |
| routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |
| routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9 |
| routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl | 0FCF733144B3D7B1B08F328FE4AD24477057C56976F0EF53633C450D8FC4729D |
| routeB_dense_Mq/dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |
| routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl | 62DF8B89F8025081DBA985C35863C6F427DDE71C225F50E1DBA949F0F60BF129 |
| routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.csv | 1AF8D59BF7253F992F13AD9318EA16AD5ADB8CFA387DC5866B2F41CA4836DCE4 |
| routeB_dense_Mq/routeB_interval_bounds.jl | 7C7B7254A00B5CE21F6B9F512D5DE7145CA8386E0420ECF71E92A5AEB5CA789F |
| routeB_dense_Mq/routeB_compact_block456_external_budget_ledger.py | 8D5EBB0F59D94F031C008574597C97CE2AA41408B7BBA70ADB71B4A4F0657C82 |
| routeB_dense_Mq/routeB_compact_block456_external_budget_ledger.csv | 06E8E2512B89508DCD01F45D54A12E871CC62B46766DB83B24FA79A255115743 |
| routeB_dense_Mq/routeB_compact_block456_matrix_pmi_probe.csv | 68EE030480F7907A9541974724ABD9169E75EC5DD45D773D1CD88DA782C8994C |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |

Hashes identify bytes, not semantic or kernel admission. Prior local reviews read for continuity were `agent_review_inbox/NEW_REVIEW_P5_K7_REAL_BLOCK456_INSTANTIATION_20260908.md` and `agent_review_inbox/NEW_REVIEW_P5_EXACT_RATIONAL_PSD_SCHEMA_ADDITIVE_HCAP_20260908.md`; they were not treated as compiled proofs.

## 8. Status and next hop

1. **candidate:** source-indexed adjugate Qs/Ls/Delta_s construction, with exact graph-ideal removal of d0 for the pure nominal port. Full coefficients and nonzero-domain/source witnesses are pending.
2. **rejected:** a packet claiming current beta, displayed lBase/lTotal, target>=0, and the full indicated analytic cell can satisfy both cap and allocation. The exact source point above defeats even Delta=0 and every lambda>1. This label is local to this review; no registry/state was edited.
3. **pending:** a redesigned actual target or differently justified input/domain contract. Do not spend the next step searching a larger Q for the frozen target. First independently check the supplied rational witness and decide whether the intended actual P5 target really equals this descriptor target. If yes, redesign/allocate beta or the residual decomposition under separate authorization, with storage and full-system obligations preserved. If no, supply the exact corrected source join and account for every added local/FD/runtime defect.

After that decision, expand the source-indexed Qs only if useful, and prove the scalar S/cell obligation with exact coefficient and coverage evidence. A K-PSD certificate cannot repair a target that is already negative at a source-valid point. No current Lean, VERIFIED, continuous-system or Float64-runtime theorem is claimed.
