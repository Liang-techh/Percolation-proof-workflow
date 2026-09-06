# Parameter-specific rotational dual mass bound

Use the ideal exact-real DH model; source Float64 rotations/axes and the
matrix/solve implementation need a separate error bridge. `audit.py` verifies
the source parameter text and all small rational matrix identities. It does
not turn the DH program into a Lean definition.

Let the unit joint axes be z_i, v in R^6, omega_0=0 and
omega_i-omega_(i-1)=z_i v_i. The isotropic angular inertias in the source give
weights w=(1/3,1/5,7/60,1/15,1/30,1/60). Translational mass is PSD. Thus
the unregularized quadratic mass form dominates sum_i w_i |omega_i|^2.

The five adjacent axis inner products are (0,1,0,0,0): these are the cosines
of the first five DH alpha parameters, independent of every joint angle.
Do not use the *last* five twists or assume that all adjacent axes are
orthogonal; joints 2 and 3 are parallel.

For f_7=0, telescoping work and completing Cartesian squares give

    f.v = sum_i omega_i . (f_i z_i-f_(i+1) z_(i+1))
    2 f.v - v'Mv <= sum_i |f_i z_i-f_(i+1) z_(i+1)|^2 / w_i
                  = Q(f),

where the explicit right side is

    Q(f)=3 f1² +8 f2² +(95/7) f3² +(165/7) f4² +45 f5² +90 f6² -10 f2 f3.

This is a universal quadratic inequality, not sampled eigenvalue evidence.
Lean verifies the work telescoping, vector completion, exact expansion with
the unit/adjacency premises, and their assembly `dh_axes_mass_dual`.

## Consequences

The matrix Q is positive definite; its exact inverse L has diagonal

    (1/3, 19/117, 56/585, 7/165, 1/45, 1/90)

and L23=L32=7/117, all other off-diagonal entries zero. Substitution f=Lv
in the universal dual inequality proves M >= L. The alternative substitution
f=v/90 and Q(f)<=90|f|² proves M>=I/90. Including the source's exact-real
regularizer gives M>=100009/9000000 I, compared with the previous
9401/1000000 I. The anisotropic form retains substantially more information
than this scalar consequence. No matrix inverse is evaluated in Lean.

For an actual interpreted force balance Ma=f (with any implementation defect
explicitly incorporated into f), the same inequality gives a'Ma=f.a<=Q(f).
Testing the dual with a force supported on joint 4 or 5 gives

    a4² <= (165/7) a'Ma,    a5² <= 45 a'Ma.

This removes an independent acceleration-box assumption from these bounds.
It does not bound f, which still contains the full controller, Coriolis,
gravity and implementation terms.

## An actual residual component

The preceding exact coefficient audit identified
MBB-Mref=diag((147/800000) sin(q5)^2,0). Hence its contribution alone satisfies

    [((147/800000) sin(q5)^2 a4)^2]/(8/5)
       <= (101871/204800000000) a'Ma
       <= (101871/204800000000) Q(f).

The coefficient is about 4.97417e-7. Lean's final
`reference_mismatch_force_only` proves this implication, with s²<=1 as the
trigonometric interface and explicit force-balance/dual premises. This is
not a bound on total residualCost, and summing component bounds without
accounting for cross terms is invalid. Over time an integral bound on Q(f)
would bound this component, but that integral has not been proved here.

## Remaining binding and verification

- Prove the ideal DH frame recursion satisfies the axis, angular-velocity
  and kinetic premises in the same formal source model.
- Enclose Float64 rotation/axis, mass, FD force and solve differences rather
  than claiming exact orthogonality for rounded matrices.
- Control remote inertial/Coriolis and other force terms, their correlations,
  full-domain trajectory coverage and the total R<=0.1 budget.
- Comparator admission and the physical parent remain open; this is a
  compiled mathematical candidate, not a registry-verified certificate.

Pinned compiler success for the complete current module is
`output/run-JNEk4oY4/verify.log`. Earlier failed and partial-source successful
attempts are retained, not overwritten. Only this leaf was compiled; no
toolchain rebuild, trajectory sweep or full regression was performed.

The first failed run's file log omits its two terminal lines although the exec
tool returned them with exit code 1. `terminal-receipt.json` in that run records
this retrospective tool-result transcription and source hash. It is explicitly
failure-only evidence, not an invented successful compiler receipt.
