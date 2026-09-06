# Concrete block inertia and momentum cancellation

Status: exact rational Fourier coefficient audit PASSED. No Lean compilation was
attempted; these are reproducible coefficient identities, not a new Lean or
Float64/physical-DH identification theorem. All work is confined to this folder.
The original integrated residualCost <= 0.1 remains OPEN.

The initial audit attempts failed, first on M41 and then on M61. The latter
repair also corrected provisional C4/C5 v1*v6 signs before their checks ran.
See [ATTEMPT_HISTORY.md](ATTEMPT_HISTORY.md) for the incorrect/corrected formulas,
observed failures, and the explicit absence of saved initial snapshots. The
status above refers only to the final corrected successful runs.

Run from the workspace: `python -B examples/routeb_inertial_structure/audit.py`.
Inputs and their SHA256 values are recorded in `audit_results.json`. The audit
checks all 610 input mass rows for reality, symmetry and cyclic q1/q6; 18 concrete
mass entries, 108 ordered Christoffel entries (rows 4,5,6), 42 unordered block
velocity-monomial transport identities, and the joint column-defect SOS below.
`block_coriolis_coefficients.csv` contains the exact ordered coefficients of C4,C5;
both off-diagonal velocity orders are included and must not be doubled again.

## 1. Compact actual crossing rows

Coordinates and velocities are real, unrestricted, with q differentiable and
qdot=v. Put s=q2+q3, z=q3, x=q4, y=q5, V=v2+v3, and

```
A0=7/60, m=40147/800000, J=1/60, mu=1/1000000,
k=147/800000, b=399/400000, d=441/400000,
j=21/80000, e=21/50000,
A=A0+k sin²y, H=d sin(q2)+e.
```

The following are identities of the entire rational Fourier coefficient maps,
not fitted values. Write F=M41, f=M43, h=M51, g=M53:

```
F = A cos s + sin y [cos x (H+b sin s+k sin s cos y)+j cos s sin x],
f = -sin x sin y (b+k cos y),
h = (m+b cos y) sin s sin x + H sin x cos y
      + j (sin s sin y-cos s cos x cos y),
g = cos x (m+b cos y),
delta4 = -d cos z sin x sin y,
delta5 = d (cos z cos x cos y-sin z sin y).

M_BD = [ F, f+delta4, f, J cos y ;
         h, g+delta5, g, 0       ],   D=(1,2,3,6).
M_BB = diag(A+mu,m+mu).
```

In particular M56=0, but **M46=cos(q5)/60 is not constant**. M66=J+mu.
The unregularized Fourier CSV is augmented by mu I only on the diagonal.
The large columns 2 and 3 combine through V; their difference has the exact SOS

```
d²-delta4²-delta5²
 = d²(sin z cos y+cos z cos x sin y)²
   +d²(cos z sin x cos y)².
```

Consequently delta4²+delta5² <= 194481/160000000000 for all real q.
For any scalar u the entire correction vector has squared norm <= d²u²;
this applies to u=v2 or a2 without splitting its two components.
In the actual residualCost metric this gives the concrete contribution bound
`(5/8)(delta4 u)^2+(10/13)(delta5 u)^2 <= (194481/208000000000)u^2`.
This is a bound for that vector alone, not an additive total-cost assertion
discarding cross terms with the remaining force.
Both joint bounds are sharp: z=x=y=0 gives delta4=0 and delta5=d.

**Use the acceleration sum, not separate triangle bounds:** the full remote
inertial action is exactly

```
M_BD a_D = (F,h) a1 + (f,g) (a2+a3)
               + (delta4,delta5) a2 + (J cos y,0) a6.
```

In particular retain a2+a3 with its sign/cancellation. Conditional on the main
task's independently proved dual inequality `a2² <= 8 a^T M a` and `Ma=force`,
`a^T M a <= Q(force)` yields

```
weightedCost(delta*a2)
 <= (194481/208000000000) a2²
 <= (194481/26000000000) Q(force).
```

The final rational coefficient is checked by this audit; the dual theorem is
not re-proved or imported here. This is one isolated force-part estimate and
does not eliminate cross terms in weightedCost of the complete e_R.
Also |f|<=b+k/2, |M42|<=b+k/2+d, |g|<=m+b,
|M52|<=m+b+d. The last uses the joint SOS for delta5.
There is no assumption that the full dynamics depends only on s: q2 and z
remain explicitly in H and delta. Thus no unjustified remote symmetry reduction.

## 2. Concrete Christoffel and reference-force identities

Let D_t be the ordinary total derivative along qdot=v, and define
T_i=(1/2) sum_{j,k=1}^6 (partial_i M_jk) v_j v_k, i=4,5.
Every coefficient of these two explicitly instantiated quadratic forms is saved
under `half_kinetic_block_derivative` in the JSON. For j<k its saved coefficient
is partial_i M_jk; for j=k it is (1/2) partial_i M_jj.
This is a finite encoding from the actual full mass, not an assumed bound on T.
The compact exact analytic Coriolis formulas are

```
C4 = (D_t F)v1+(D_t f)V+(D_t delta4)v2
        +2k sin y cos y v4 v5-J sin y v5 v6-T4,
C5 = (D_t h)v1+(D_t g)V+(D_t delta5)v2-T5.
```

These formulas retain correlations and require no norm/Cauchy inflation. The
audit differentiates Fourier coefficients exactly and checks every velocity
monomial against the separate source Coriolis CSV. Additional checked compact
remote kinetic entries are

```
M33 = 608093/2400000+2b cos y-k sin²x sin²y,
E = (5187/200000)cos z+d(cos z cos y-sin z cos x sin y),
M23 = M33+E,   M22 = M33+2E+54553/200000
```

(before mu). These expose the V structure of the remote v2,v3 kinetic terms.

The source-instantiated momenta and nominal regularized reference R are

```
p4=(A+mu)v4+Fv1+fV+delta4 v2+J cos y v6,
p5=(m+mu)v5+hv1+gV+delta5 v2,
R=diag(A0+mu,m+mu),
sigma4=k sin²y v4+Fv1+fV+delta4 v2+J cos y v6,
sigma5=hv1+gV+delta5 v2.
```

Thus p_B=R v_B+sigma, and, for twice differentiable q,

```
M_BD a_D+M_BB a_B+C_B = dot p_B-T_B,
e_R = -dot sigma+T_B-G_B+g0_B+eta_B.
```

The second uses the same actual controller/reference-force definition as
`routeb_force_error_decomposition`: analytic M a+C+G=tau+eta,
tau=-Kp q-Dv+g0+G_in w, e_R=R a_B+Kp_B q_B+D_B v_B-G_in,B w.
It removes explicit remote accelerations exactly, rather than asserting the old
port residual equals the new reference force. A bound on sigma does NOT bound
dot sigma or its squared integral. Such control, and its correlations with T,
are the remaining budget issue; integration by parts alone does not close it.

## 3. Cyclic spin and the complete v6 part of C_B

All mass modes have nu1=nu6=0. Put
N=cos s cos y-sin s cos x sin y. The checked row 6 is

```
p6=(J+mu)v6+J[Nv1+sin x sin y V+cos y v4].
C4|v6 = -J sin y v6 [sin s sin x v1+cos x V+v5],
C5|v6 = J v6 [(cos s sin y+sin s cos x cos y)v1
                 -sin x cos y V+sin y v4].
```

There is no v6² term in C4,C5. In analytic Euler-Lagrange semantics with the
previously encoded q6-independent potential, dot p6=tau6 (not zero: q6 is driven).
With chi=J/(J+mu)=50000/50003, the quasi-momentum

```
pi4=p4-chi cos y p6
```

has **no v6 coefficient**, exactly.
The audit also saves all six concrete velocity coefficients of pi4 and checks
that its last coefficient is the zero Fourier polynomial. Its balance is

```
dot pi4=tau4-G4+T4-chi cos y tau6+chi sin y v5 p6
```

for analytic error-free semantics; add eta4-chi cos y eta6 otherwise.
Likewise p5 already has no v6 coefficient. This is a concrete spin-channel
cancellation, not a full acceleration elimination or a proof of a total gain.
The cyclic q1 momentum is driven as well, not conserved under this controller.

## 4. Source boundary and adjacent-axis check

The exact builder has DH_ALPHA=[-1,0,1,-1,1,0] in pi/2 units. The Julia DH table
has the same six twist entries. Its frame transform is Rz(theta)Rx(alpha), with
z_i recorded before applying joint i. Therefore, in ideal real arithmetic,
z_i dot z_(i+1)=cos(alpha_i), giving [0,1,0,0,0] for the five adjacent pairs.
No duplicate derivation of the main task's rotational-dual inverse bound is made.

The Julia implementation uses centered differences, Float64 and a backslash
solve, not analytic Christoffel evaluation. For ideal real centered FD with
common nonzero h, all row-6 mass frequencies are 0 or +/-1 in each coordinate,
so C6_FD=(sin h/h) C6_analytic. Thus in that model
dot p6=tau6+(1-sin h/h) C6_analytic, not simply tau6. This defect must also enter
the quasi-momentum balance. General C4,C5 do not have this common multiplier.
If eta already includes analytic-minus-FD forces, do not count them twice.

Mass parameter/trigonometric/arithmetic discrepancies, FD rounding (including
rounded q+/-h), controller arithmetic, represented mu, and solve/RHS residuals
remain separate in eta exactly as in the prior force-decomposition sidecar.
Ideal circle and adjacent-axis identities do not bound floating errors.
No trajectory screen, broad regression, download, target edit, state edit,
or registry admission was performed. No complete DD trig factorization is
required or claimed; the finite exact T4,T5 coefficient payload closes that
algebraic dependency without chasing a larger symbolic expression.
