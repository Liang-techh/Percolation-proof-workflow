# Local reference force versus the historical port residual

The new reference force is not the old `l_total`. With B=(4,5), D=(1,2,3,6), and the same acceleration and reference block in both definitions, the exact identities are

\[
\boxed{e_B=(M_{ref}-M_{BB})a_B-M_{BD}a_D-C_B-G_B+g_{0,B}+\eta_B}
\]

and

\[
\boxed{e_B=(I_B+Kp_Bq_B+D_Bv_B-G^{in}_Bw)+r_B-l_{total}}.
\]

The first is the physical-force decomposition, conditional on the specified real-valued model/implementation meanings below. The second is an algebraic change of residual definition. Neither proves the proposed total residualCost integral ≤0.1. The independent trajectory screen and total-budget decision remain with the main task.

## Definitions, controller, and block balance

Use `G^{in}` for the disturbance coefficient and G for gravity. From the read-only `dhport_lib.jl`,

\[
Kp_B=(3/5,1/2),\quad D_B=(4/5,13/20),\quad
G^{in}_B=(1/5,1/10),\qquad
\tau=-Kp\,q-Dv+g_0+G^{in}w.
\]

Here `D=Kd+b_fr`, and `G^{in}` is the intended exact value of `gw_coef .* I_val`, not `gw_coef` alone. The function named `exact_ddq` evaluates mass, C, G and `G0v` in Float64 and returns a backslash solve; its name does not certify an exact solve.

Define `e_B=Mref_BB a_B+Kp_Bq_B+D_Bv_B-G^{in}_Bw`. For exact source-real FD semantics, M includes the explicit `10^-6 I`, C is the six-vector of Christoffel forces assembled from centered mass differences, and G is the centered potential gradient, with `h=1/100000`. Then
`M_BB a_B+M_BD a_D=tau_B-C_B-G_B`, which immediately gives the first boxed identity with η=0. It is componentwise and does not require a mass inverse, a velocity/acceleration bound, or Cauchy/Young inequalities. Remote acceleration is the entire actual a_D, not an auxiliary port variable.

If `Mref` is the recorded nominal regularized block `M(0)_BB`, the source Fourier mass coefficients give the further exact simplification

\[
M_{ref}=\operatorname{diag}\left(\frac{350003}{3000000},\frac{200739}{4000000}\right),
\quad M_{BB}(q)=M_{ref}+\operatorname{diag}\left(\frac{147}{800000}\sin^2q_5,0\right).
\]

Thus the reference-block mass-mismatch force is exactly
`(-(147/800000) sin²(q5) a4, 0)`. This special case is conditional on that choice of Mref; the Lean identity supports an arbitrary 2×2 reference matrix. The mass/physical-DH identification remains the existing exact-real source seam, not a newly proved physical theorem.

## Implementation errors: signs and single accounting

The imported `RouteBDHPowerBinding` definitions use Ma for the chosen analytic mass, Mi for the interpreted computed mass, a for the returned acceleration, and separate analytic/computed force vectors. Let

\[
\tau_A=-Kp\,q-Dv+g_0+G^{in}w,\qquad
s_i=(M_i a)_i-(\tau_{I,i}-C_{I,i}-G_{I,i}),
\]

\[
\eta_i=\sum_j(M_a-M_i)_{ij}a_j+(\tau_I-\tau_A)_i
+(C_A-C_I)_i+(G_A-G_I)_i+s_i.
\]

The existing theorem proves `Ma a+CA+GA=tauA+eta` exactly for arbitrary real-valued inputs. The new `implemented_reference_force` reuses it and proves the first boxed identity with `M=Ma,C=CA,G=GA`. In particular the mass-implementation error acts on **all six** accelerations and has sign `Ma-Mi`.

For auditing the original numerical call, the terms mean:

- `tauI-tauA`: represented parameter and torque arithmetic errors, computed `G0v`, damping addition, and the disturbance divide-then-multiply path. The chosen exact g0 must be the same in tauA and in the displayed decomposition.
- `CA-CI`, `GA-GI`: analytic-to-exact-FD truncation plus exact-FD-to-Float64 evaluation error, if CA,GA are analytic. Equivalently choose CA,GA as exact-FD forces and include only implementation discrepancy here. Do not add the truncation budget twice. Raw C/G in the new force decomposition are not themselves small FD remainders.
- `Ma-Mi`: mass parameters, trigonometry, matrix arithmetic, and regularizer representation. An unregularized reference model versus the regularized source needs the explicit regularizer mismatch, rather than silently discarding it.
- `s`: both solve residual and final RHS assembly rounding. If `bhat` is the actual rounded vector supplied to backslash, let `rsolve=Mi*a-bhat` and `δb=bhat-(tauI-CI-GI)`. Then `s=rsolve+δb`. Do not add either again after using s.

The identities are exact for interpreted outputs; no bound on any of these implementation errors, continuous numerical trajectory, or integrated cost is established here.

## Why the old budgets do not transfer

The historical `routeB_compact_port_implicit_accel_elimination.py` explicitly records
`l_total=I_B-M0_BB*a_B+r_B`. The matching direct descriptor defines `I_B=IVAL_B .* fB`, a **nominal model force**, not the actual inertial action and not an identity matrix. The old port is `r_B=M_BD*nu_D`, with
`nu_D=a_D-a_D_nom`; its nominal-distal bridge satisfies
`M_DD*a_D_nom+M0_DB*a_B=tau_D-C_D-G_D`. Thus generally
`M_BD*a_D=M_BD*a_D_nom+r_B`; bounding r_B alone does not bound the full remote inertial term.

Writing `h_B=I_B+Kp_Bq_B+D_Bv_B-G^{in}_Bw`, rearrangement of the old link gives `e_B=h_B+r_B-l_total`, precisely as requested. Its use requires the same a_B and Mref; an independently evaluated nominal acceleration or a different reference metric breaks that identification. If an observed old link has defect `δlink=l_observed-(I_B-Mref*a_B+r_B)`, then `e_B=h_B+r_B-l_observed+δlink` instead.

For the source's explicitly selected DH controller branch, its nominal fB includes the extra nominal gravity stiffness and off-diagonal coupling, giving

\[
h_B=\left(-\frac3{20}q_4+\frac1{100}q_5,\quad
\frac1{200}q_4-\frac2{25}q_5\right).
\]

The historical default Fourier branch has `D4=1/2`, whereas actual DH `D4=4/5`; it adds `(3/10)v4` to h4. The q5 damping matches. The branch therefore cannot be silently inferred from a filename or an old scalar budget.

The exact square identity proved in Lean is, for each component,

\[
e_i^2=h_i^2+r_i^2+l_i^2+2h_ir_i-2h_il_i-2r_il_i.
\]

Multiplying by the desired metric weights and summing/integrating preserves this identity and its correlations. No factor-of-two/three norm split is imposed. Even in the special case h=0, the relevant quantity is `r-l`, not l alone. Old Euclidean, Mref-inverse, feature-dependent, or instantaneous port bounds also have different metrics/domains from a new weighted integral. None is automatically the proposed total cost bound.

## Exact gravity part, including moving remote angles

The imported, compiled 17-row factorization has `s=q2+q3`, `x=q4`, `y=q5`, `c=20601/400000`, and gives the analytic gravity components

\[
g_4=c\sin s\sin x\sin y,\qquad
g_5=-c(\cos s\sin y+\sin s\cos x\cos y).
\]

At the block origin these are `(0,-c sin s)`. They do not vanish merely because q4=q5=0. The component bounds `|g4|≤c|sin s sin x sin y|≤c` and `|g5|≤c` hold for all real q, but the following stronger joint identity retains the correlation:

\[
c^2-g_4^2-g_5^2
=c^2(\cos s\cos y-\sin s\cos x\sin y)^2
+c^2(\sin s\sin x\cos y)^2.
\]

It follows that `g4²+g5²≤c²`, and with the **actual** D4,D5,

\[
\frac{g_4^2}{8/5}+\frac{g_5^2}{13/10}
\le\frac{10}{13}c^2
=\boxed{\frac{424401201}{208000000000}}.
\]

The weighting step only uses `5/8≤10/13`; there is no separate-component sum inflation. This parameter-specific gravity-only bound is sharp: `s=pi/2,x=y=0` gives g4=0, g5=-c. A gravity-only integral over a horizon T is consequently bounded by this constant times T, whenever the signals satisfy the exact model semantics. This is not a bound on the square of the sum of gravity with the other force components.

For the **exact-real original FD** gravity, the q4/q5 Fourier frequencies are only 0 and ±1. Hence both derivatives have the same exact multiplier
`gFD_i=(sin h/h) g_i`. Since `h=1/100000` and `|sin h/h|≤1`, the same joint and weighted bounds hold for exact-FD gravity. The exact reference gravity gFD(0) is zero. The truncation satisfies
`|g_i-gFD_i|≤c*h²/6=6867/8000000000000000` for both block components; this improves the old q5 coefficient-l1 ledger by a factor of two. Float64 sample/argument/subtraction errors and computed g0 remain separate. The scalar FD multiplier argument is analytic here; the Lean SOS theorem concerns the explicit analytic gravity definitions.

## Reproduction and proof boundary

Final compile status: **PASS**, Lean 4.33.1, warnings treated as errors, `LEAN_COMPILE_EXIT_CODE=0` and `VERIFY_EXIT_CODE=0`. Successful run: `output/run-cbbq9MXx/verify.log`. All printed theorem dependencies are limited to `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` appears.

The two checkpoint candidates are `RouteBForceErrorDecomposition.implemented_reference_force` (exact algebraic decomposition reusing the implementation residual) and `RouteBForceErrorDecomposition.gravity_weighted_cost_rational` (the explicit gravity-only cost bound `424401201/208000000000`). The same compile also verifies `new_error_from_old_total`, the exact squared residual identity, the gravity SOS identity, and the joint gravity norm bound. Compiled artifact SHA-256: `26f3ed2c99644f32f89338ba6cd8b2dd7afe514d620521a0835c00df49c0f640`.

All files are confined to this new directory. `audit.py` reads the source, checks actual block gains, exact reference/variable block mass coefficients, FD gravity frequency support and ledger constants, and records SHA-256 evidence in `source_evidence.json`. It does not execute the target Julia code or a trajectory screen.

`verify.sh` uses the pinned cached Lean 4.33.1/mathlib and successful imported `DHPowerBinding`, `BlockPotential`, `PotentialSlice`, and `StorageObstruction` artifacts. Its own output directory records the source snapshot, hashes, compiler exit code, and `#print axioms` output. The formalized gravity bounds refer to the explicit analytic formulas; the coefficient-to-derivative/source binding is the documented exact audit, not a new physical-DH theorem. No Hessian/Taylor storage expansion, infrastructure rebuild, download, or total-budget certificate is included.
