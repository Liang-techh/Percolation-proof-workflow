# Route-B source mass-table adapter

This Mathlib-only sidecar fixes the six source mass and isotropic inertia
constants as exact rational tables and specializes the existing contract mass
functional to those tables.  It proves only the ideal-real algebraic adapter;
it does not claim equality with the Julia Float64 evaluator or with the Fourier
CSV until the separate source comparator is closed.
