# GH-LEAN-BODY6-PATHDOMAIN-REPAIR

Agent/source_agent: **巨阳仙尊**.

This is a focused portable compilation/axiom audit for
`examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean`
after the coordinator's `cap + B` / `B + cap` repair.  The audit does not change
the target theorem statements.  It copies the current target to a temporary Lean
file, appends `#print axioms` commands for the seven public theorem leaves, and
compiles it under the repository-pinned `examples/local_fkg` Lake environment.

The repaired proof keeps the input budget as `cap + B <= bar`, derives the
commuted inequality `B + cap <= bar`, and only then composes it with
`add_le_add_right (hCap t ht) B`.  This is an arithmetic/order repair only.
It does **not** prove whole-path inclusion, physical DH/source projection,
storage identity source binding, ODE continuation/coverage, or registry/admission.

Run with:

```bash
CI_PORTABLE=1 bash verify.sh
```

A green receipt is only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
