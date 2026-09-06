# Final receipt — homogeneous seven-slot prefix projection

Status: **PASS — homogeneous frame prefixes project to cumulative rotation prefixes**

This Mathlib-only leaf proves two reusable facts: products of homogeneous 4x4
frames remain homogeneous, and the top-left 3x3 block of every Route-B
seven-slot prefix is exactly the corresponding cumulative 3x3 rotation prefix.

Successful pinned run: `output/run-7hl40Fdl`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
HomogeneousPrefixProjection_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
HomogeneousPrefixProjection.lean  fb7f079446da4caca14e3835efc5c294eea7fdf399ebb6f290d00d910235b6ba
HomogeneousPrefixProjection.olean b0800b9e3a12890b1701025e757b2162985e72d44fb709f23328f6f1e417996a
terminal.log                     f5af88fe718026e5f39caf35a0471b32e43692268ee076eb16d8b1ec2321f723
```

Only standard logical axioms occur in the axiom reports. This is a compiled
candidate for the Route-B proof DAG, not a comparator-accepted source theorem.
