# P8 minimal Picard-step report

Status: **LEAN_VERIFIED_INTERFACE_OPEN**

Local verification result: **PASS**.  The exact command
`cd /home/z5242/sos_lean && lake env lean -DwarningAsError=true
.../RouteBP8PicardStep.lean` returned exit code `0`.  A source scan of this
directory found no `sorry`, `admit`, or `axiom` declaration.  Only this leaf
was compiled.

The new leaf proves the structural part of the P8 decomposition:

- `State14 := Fin 14 → ℝ` with the full `q,dq,w,c` coordinate order;
- exact ramp coordinates `w(t)=c*t` and `c'=0` at the lifted-state level;
- `FullX0 ⊆ InitialBox`, using only the energy bound and `c²≤3`;
- an interval RHS premise implies inclusion of one Picard image in the
  coordinatewise propagated box;
- the ramp premise gives the exact Picard update for `w` and the frozen `c`
  coordinate;
- the parent theorem combines the initial-box child and the Picard child.

The concrete `full_rhs!` binding remains **OPEN**.  The current Route-B
source-side artifacts identify the Julia source fields and the required
14-coordinate receipt shape, but do not provide a Lean definition of the
deployed RHS together with kernel-checkable interval endpoints.  Therefore
the interface keeps `F : State14 → State14` abstract and requires the exact
premise `hbox`; no numeric probe, CSV, or sampled trajectory is promoted to a
proof.

The present one-step interval theorem is purely order-theoretic and does not
claim existence, uniqueness, global coverage, continuation, entry, or terminal
transfer.

The remaining open frontier is therefore the source-bound child theorem for
`hbox`: a concrete 14-coordinate RHS interval enclosure on each chosen box,
with authenticated source semantics and outward-rounded endpoints.  Until
that child is supplied, this file is an interface theorem and not a full
physical Route-B flowpipe certificate.
