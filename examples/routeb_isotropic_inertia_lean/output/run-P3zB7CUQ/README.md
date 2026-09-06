# Isotropic inertia rotation bridge

This Mathlib-only leaf proves that a row-orthogonal 3x3 rotation preserves a
scalar identity inertia: `R * (s I) * Rᵀ = s I`. It is the exact algebraic
bridge needed to compare Julia's rotated isotropic body inertia with the
contract core's fixed inertia matrix.
