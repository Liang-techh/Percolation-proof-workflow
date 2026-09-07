# Route-B P4: exact `M_BD a_D` projection obstruction

The current block-only PMI variables cannot control the remote term in the
true descriptor equation.  This is an exact negative result from the rational
Fourier mass snapshot, not a sampled numerical claim.

## Exact computation at `q=0`

Re-summing `routeB_fourier_mass_BD_rational.csv` at `q=0` gives, with
`B=(4,5)` and `D=(1,2,3,6)`,

```text
M_BD(0) =
  [  7/60          0          0       1/60       ]
  [ -21/80000   41827/800000 8189/160000  0     ].
```

In particular,

```text
M_BD(0)e1 = (7/60,-21/80000)
||M_BD(0)e1||² = 784003969/57600000000 > 0.
```

The local checker is `scripts/check_routeb_p4_mbd_obstruction.py`; it uses
only exact rational arithmetic and reports `PROJECTION_OBSTRUCTION_EXACT`.

## Consequence for the theorem DAG

Fix all currently projected block variables at zero and take
`a_D=lambda*e1`.  The block projection remains unchanged, while

```text
rho_remote(lambda) = lambda * (7/60,-21/80000).
```

Its squared norm is the positive factor above times `lambda²`, so no finite
remote bound depending only on the current block projection can be proved.
This does not claim that an arbitrary `lambda` occurs on a physical trajectory;
it is a projection countermodel showing that a physical trajectory/full-state
premise is missing.

The smallest repair seam is one of:

1. a full-state descriptor equation with a bounded `a_D` on the same covered
   domain;
2. an exact Schur elimination that binds `M_BD`, `M_DD`, and the remote force;
3. a typed adapter proving an equivalent remote residual enclosure.

Until one of these is present, P4/M4 remain open and
`formal_certificate_allowed=false`.
