# Route-B remote acceleration budget

The compiled `examples/routeb_rotational_dual/RotationalDual.lean` sidecar
contains the source-independent scalar consequence

```text
‖a‖² / 90 ≤ mass.
```

Restricting the full vector to the remote coordinates `D=(1,2,3,6)` gives the
conditional candidate

```text
‖a_D‖² ≤ 90 · mass.
```

For comparison, applying the four coordinatewise force-metric bounds and
summing gives the weaker `‖a_D‖² ≤ (802/7)·mass`.  The tighter `90` bound is
preferable, but it is usable by P4 only after an adapter proves that `mass` is
the same full-state kinetic budget at the same source/state key.  It does not
bound `M_BD`, does not prove the descriptor equation, and does not imply
trajectory coverage.

`routeb_remote_accel_budget.py` and its checker preserve these assumptions and
keep both formal admission and registry eligibility closed.
