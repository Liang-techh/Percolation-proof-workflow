# Route-B P8 minimal full-X0/ramp Picard-step interface

This leaf provides a small exact-real interface for one full-X0/ramp Picard
step.  It is intentionally conditional: the deployed `full_rhs!` source and
its interval enclosure are not silently reconstructed from numerical probes.

The Lean file contains:

1. a genuine `Fin 14 → ℝ` lifted state with coordinate order
   `q₁…q₆,dq₁…dq₆,w,c`;
2. the ramp lift and exact `w=c*t`, `c` coordinate formulas;
3. the full initial contract `sum(qᵢ²+dqᵢ²) ≤ 9/400`, `w=0`, `c²≤3`;
4. a proved inclusion of that contract in an explicit finite initial box;
5. a pure interval-arithmetic decomposition proving one Picard image is in
   the propagated step box, together with the exact ramp coordinate update
   `w₀+h*c` and frozen `c` coordinate.

`fullX0_ramp_picard_step_decomposition` is the parent interface.  Its
`hbox` argument is the authenticated child theorem still needed from the
source-bound RHS/interval producer.  `hramp` records the two exact ramp
components and the conclusion exposes their effect on the Picard image; it
does not manufacture an ODE certificate.

No `sorry`, `admit`, or non-standard axiom is present.  No sampled trajectory
is used as proof evidence.

The local verification command (using the pinned `/home/z5242/sos_lean`
environment) is:

```text
./verify.sh
```

Equivalently:

```text
cd /home/z5242/sos_lean
lake env lean -DwarningAsError=true \
  /mnt/c/Users/z5242/Desktop/重构版/工作流/examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean
```

Only this leaf is compiled; no project-wide regression suite is run.
