# Route-B minimal source loop

This is an independent, Mathlib-only Lean leaf for the Julia-style finite-body
mass loop.  It formalizes:

- six finite bodies and the Julia mass/inertia tables;
- explicit cutoff gating for COM/Jv/Jw data;
- isotropic inertia followed by a body rotation;
- equality of the finite body accumulation with generic `massFromLinks`.

It deliberately imports no Route-B project module and does not modify the main
state, DAG, or registry.
