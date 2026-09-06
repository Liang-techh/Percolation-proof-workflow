# Concrete W0 coefficients and the full-horizon gates

This is the handoff for the original full12 ball ||(q,v)||<=3/20,
w=ct, c^2<=3, T=1, actual delta=a-a0 and J=int delta'Ldelta. All source
and physical/implementation premises retain their original scope.

## 1. Source and the chosen family

Use the COMPLETE exact `reference.json` in signed source run
`run-20260905T203532Z-b2dcff09/inputs`: M0, H0, M0 inverse R, and A14.
No block projection, diagonal mass, or replacement nominal trajectory enters.
Write S=K+H0, where

    K=diag(1,4/5,7/10,3/5,1/2,2/5),
    D=diag(13/10,11/10,19/20,4/5,13/20,1/2),
    G=(1,1/2,3/10,1/5,1/10,1/20),
    a0=R(-Sq-Dv+Gw).

L=Q^-1, Q has diagonal (3,8,95/7,165/7,45,90), Q23=Q32=-5;
in particular L22=19/117, L23=7/117, L33=56/585. Other diagonal entries
are 1/3,7/165,1/45,1/90, in coordinates 1,4,5,6 respectively.

Distinguish the potential remainder Rp from the matrix R:

    Rp=U-U(0)-q'H0q/2,
    Sgap=v'(M0-M)v/2-Rp,
    W0=v'M0v/2-Sgap+(7/75)q4^2
      =v'Mv/2+Rp+(7/75)q4^2.

The audited source gives Rp>=-q4^4/40. Consequently, on
q4^2<=56/15 and M>=L>0,

    W0 >= v'Mv/2 + q4^2(7/75-q4^2/40) >= 0.

The q4 condition follows from the ORIGINAL domain quantity being at most
28/5, since that quantity includes (3/2)q4^2. This is a conditional domain
argument; it does not independently prove that the solution stays there.

Set tau=1-t, use j=1,...,8 ONLY, and select

    V=f W0 + sum_i p_i q_i^2 + h_c c^2,
    f=sum_j a_j tau^j, p_i=sum_j p_ji tau^j, h_c=sum_j c_j tau^j,
    a_j,p_ji,c_j >= 0.

Thus V>=0 at EVERY covered prefix endpoint, and V(1)=0. In Y=(q,v,w,c),

    Pqq=diag(p_i)+(7f/75)E44, Pvv=f M0/2, Pcc=h_c,
    all other blocks zero, k=-f.

This is an actual globally compatible differentiable P(t),k(t), with
g=Bdelta'P Y+(k/2)M0v=0 identically. It supersedes the earlier signed
acceleration-storage choice, whose endpoint lower bound was costly.

Under the source balance and signed-gap chain rule, with eta counted once,

    W0dot=-v'Sq-v'Dv+v'Gw+(14/75)q4 v4+v'eta,
    d=Vdot=f'W0+f W0dot +sum_i[p_i' q_i^2+2p_i q_i v_i]+h_c' c^2.

Both full mass/Christoffel work and the source potential gradient cancel in
this derivative. The real source Rpotential, M and residual still enter W0
and the acceleration cost; none is set to its nominal value away from q=0.

## 2. Actual returned coefficients, second and final LP

Every coefficient not displayed below is EXACTLY zero. Fractions, not the
solver's floating status, define the proposed functions:

| Coefficient | Exact value |
|---|---|
| a8 | 6995146470641/1000000000000 |
| p1_1 | 17535437/125000000000 |
| p1_2 | 2543546915047/250000000000 |
| p1_3 | 2054718657/200000000000 |
| p1_4 | 208283/1000000000000 |
| p1_5 | 15279087/1000000000000 |
| c4 | 141378301/1000000000000 |
| p5_2 | 2497160242683/1000000000000 |
| p6_2 | 1039070909897/500000000000 |
| p8_3 | 304901221437/125000000000 |
| beta | 2949897944533/200000000000 |

In particular f=6.995146470641 tau^8 and
h_c=0.000141378301 tau^4; the ramp reserve is positive.

The second LP used the first 70 predetermined static states plus ten fixed
rows: q=0,v=G/1000,c=1 at t=1/4,1/2,3/4; six q=0,v=e_i/1000,c=1
rows at t=1/2; and the actual initial state q2=1/100,v2=3/200,c=0.
The central ramp row imports exact W0,W0dot,cost from the rational source
witness. The remaining source evaluations are floating analytic-source
collocation, with eta=0. Full point definitions and rows are in `lp_problem.json`.

HiGHS primal/dual tolerance was 1e-10, time limit 30 seconds. There was ONE
second solve and no inflation of its coefficients. The rounded rational vector
has max saved source-row violation 2.4613130393761614e-12. This is within the
stated numerical 1e-8 diagnostic tolerance, NOT exact nonpositivity and NOT
uniform source certification. The near-terminal obstruction in section 6
prevents interpreting this vector as a zero-supply solution of the full problem.

## 3. Exact initial and endpoint budget for that vector

The source M0 absolute row sums are

    (1887427/2000000,11224907/12000000,7144697/12000000,
     250001/1000000,615649/4000000,50001/1000000),

all below 1. Symmetry/Gershgorin implies M0<=I. The signed source audit gives
Sgap(0)>=-149492741/500000000000 > -3/10000 on the ENTIRE original ball.
This also yields W0(0)<=231/20000 using the shared ball, not two separate balls.

Let A=sum a_j, Pi=sum p_ji, Hc=sum c_j. The stronger combined bound used by
the LP is

    beta>=A/2, beta>=Pi+(7A/75 if i=4 else 0),
    V(0)<=9 beta/400 +3A/10000+3Hc.

All these inequalities were rechecked with Fraction after coefficient
rounding. beta_before=beta_after=2949897944533/200000000000; no upward repair
was necessary in the final run. Its exact slacks, ordered as A/2 then i=1..6:

    22503832974689/2000000000000,
    14749349439169/1000000000000,
    0,
    3075001589471/250000000000,
    1057245688284163/75000000000000,
    7374737221789/500000000000,
    2949897944533/200000000000.

Therefore, CONDITIONAL ON the stated initial/source binding,

    V(0) <= 835965494010387/2500000000000000
         = 0.3343861976041548.

All covered endpoint charges are zero because V>=0, not because the large
signed Sgap bound was ignored. If a valid nonnegative supply b(t) is later
certified, the available initial-budget arithmetic is

    int_0^1 b < 1-835965494010387/2500000000000000
               = 0.6656138023958452.

This number is a prospective supply allowance. Neither it nor the initial
objective is an established J bound. The zero-supply candidate fails the
uniform condition explained below.

## 4. Fixed affine multiplier and the scalar certificate to be proved

Use the coordinator's fixed-Z scalar gate with

    dM=M0-M, r=dM*a0+H0q-grad U-C+eta, h=Rr,
    Z=I, z=(RLR-R)r=(RL-I)h, e=dM(I+RL)h.

No source inverse or contraction epsilon is needed; 2M-L>=L. The signed
source scalar independent of all storage coefficients is

    Cost_R=h'Lh+2(RLh)'dM h+e'Qe.

Keep this entire expression assembled before enclosure. Given the source
premises, the fixed-Z argument supplies delta'Ldelta<=Cost_R. At M=M0 it
equals the actual delta'Ldelta. The intended certificate is

    Cost_R + f'W0 + f[-v'Sq-v'Dv+v'Gw+(14/75)q4v4+v'eta]
      +sum_i[p_i' q_i^2+2p_i q_i v_i]+h_c'c^2 <= b(t).

For fixed real source data these are linear inequalities in the storage
coefficients and b. The LP used b=0 on its finite points. Uniform time/source
enclosures, an actual eta enclosure, and an integrated supply allowance are
still required; the scalar gate's formalization is being handled by the main
task and companion, not claimed as a new Lean result in this directory.

## 5. Exact failures of the first LP, retained rather than overwritten

The first candidate had every c_j=0, initial objective .3323448596440647,
and max numerical violation 7.071750719472882e-8, so it was NOT feasible at
1e-8. Its original scripts, inflation step and numerical status are preserved.

At the coordinator's predeclared q=0,t=1/2,c=1,v=G/1000, exact mass-CSV
derivative summation verifies M=M0 and yields the actual Christoffel force

    C=(7447/156250000000,-2069/50000000000,-103/10000000000,
       0,-21/50000000000,0).

The potential CSV gives grad U(0)=0 and Rp(0)=0. Hence r=-C,
delta=-R C (checked by M0 delta=-C), and Cost_R=delta'Ldelta exactly.
For the first LP coefficients,

    Vdot=279530726330014286211/25000000000000000000000000
        > 0.0000111812290532,
    delta'Ldelta approximately 3.2653461653766704e-15 >0.

The complete rational cost is in the witness JSON, not a floating proof.
Thus adding a c^2 reserve is mathematically necessary for that first
candidate, rather than just an LP numerical adjustment. More generally if
h_c'=0, q=0, t>0 and f>0, the linear-in-velocity drive defeats the
quadratic damping for small positive v parallel to G.

There is also an actual initial-data obstruction, independent of ramp:
q2=1/100,v2=3/200,c=w=0, all other coordinates zero. Its full12 radius
squared is 13/40000<9/400. The restricted mass coefficient M22 is constant
on this line, U=constant+(Agrav+Bgrav+Cgrav)cos(q2), and Psi(e)<=e^4/24.
For the first LP and its retained simple reserve repair this proves

    Vdot >= 11652476375725545296269/20000000000000000000000000 >0.

It therefore fails zero-supply dissipation already at permitted actual
initial data. Both this row and the ramp row were included in the second LP.
The repair run did not assert success merely from making its 70 old rows
numerically pass.

## 6. Necessary next gates; why the final sampled vector is still unclosed

**Origin quadratic gate.** For each t, let N(t) be the symmetric 13x13 matrix
in (q,v,c), with all unnamed blocks zero:

    Nqq=diag(p')+(7f'/75)E44,
    Nvv=f'M0/2-fD,
    Nqv=diag(p)-fS/2+(7f/75)E44,
    Nvc=f*t*G/2,
    Ncc=h_c'.

Because the residual cost starts at fourth order at the origin (eta=0),
b=0 on a source neighborhood requires N(t)<=0. This is an exact necessary
coefficient gate over the entire time interval, not another list of selected
directions. It was NOT verified for the final coefficients. The zero-ramp
reserve obstruction is also evident in its velocity/c principal blocks.
Polynomial/interval verification of -N(t)>=0 is the next finite exact check;
no dependency installation or additional solve was performed here.

Completed coordinator handoff: the second zero-supply coefficient vector is
also rejected by the separately owned source audit
`examples/routeb_storage_origin_gate/output/run-20260905T211357Z-f7fae1f0/results.json`.
For q6=1/100, v6=-1/400, all other coordinates and c zero, the coordinator
reports exact Fourier M66/potential-line identities, initial norm squared
17/160000, and

    Vdot=5421217529307363077/120000000000000000000000 > 0.

The zero local qq66 entry and nonzero qv66 entry give a negative determinant,
so the necessary negative-semidefinite quadratic gate fails. This is an
actual allowed initial-state obstruction to the second vector's zero-supply
dissipation, not a rejection of the W0 family or actual J<=1. The evidence
path and result were supplied by the coordinator; this leaf neither ran nor
independently reread that audit. No coefficient patch or further LP follows.
The next frontier is the full 13x13 local quadratic gate or a certified
positive supply, whose integrated allowance must respect section 3.

**Terminal velocity gate gives an actual obstruction to the returned a1=0.**
For q=0,c=0,v=rho(e4+e5), the source audit in affine_multiplier DERIVATION
gives C=(21/25000)rho^2 e1 (at rho=1/20 it is 21/10000000 e1), M=M0,
and nonzero cost E=(21/25000)^2 rho^4 e1'RLR e1>0. Every finite support
outer cell containing a neighborhood of zero includes such states for
sufficiently small nonzero rho. They are static cell states, not a claim of
reachability at t=1.

For the final candidate, a1=0, f=a8 tau^8, q=0,c=0 imply

    Cost_R+Vdot=E-a8[8 tau^7 W0+tau^8 v'Dv] -> E>0 as t->1.

Thus the uniform b=0 source-cell gate fails on an interval immediately before
1, not merely at the single terminal time. This is a mathematical obstruction
to the entire nonnegative polynomial family restricted to a1=0, on such
terminal source neighborhoods. It is NOT a refutation of actual J<=1.
For a repaired b=0 design the terminal condition must include, at least,

    a1 >= 2(21/25000)^2 rho^2(e1'RLR e1)/[(e4+e5)'M0(e4+e5)] > 0

for every admitted rho on this line. A first-order W0 coefficient, or a
certified positive supply, must be considered before treating more sampled
points as progress toward a uniform certificate. No third LP was run.

**Full target acceptance.** The remaining uniform inequality must retain
the actual M,r,Rp,eta and their correlations on every closed time/source cell
under the J<1 prefix assumption; bind the source/FD/Float64 semantics and
regularity; combine W0 positivity with the original domain/gain implication;
prove continuation and joint first-exit coverage. Then FTC gives
J(t)<=V(0)+int_0^t b-V(t), and a strict uniform budget below 1 rules out a
first hit. Terminal-only, origin-quadratic-only, numerical-collocation-only,
or solver-status-only evidence does not discharge these gates.
