# Route-B leaf admission bridge

This is a pure, fail-closed adapter from a compiled Lean leaf receipt to a
theorem-DAG advisory artifact. It records the leaf identity, source hash,
scope, open obligations, and three admission gates: source binding, coverage,
and terminal transfer.

The adapter never imports or writes the workflow registry. Every output has
`candidate_status: compiled_candidate`, `registry_status: pending`,
`verified: false`, and `promotion_allowed: false`. Missing evidence is
`pending`; malformed or explicitly negative evidence is `rejected`. An
`advisory_ready` artifact is still not a registry admission.

Focused check:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q tests/test_routeb_leaf_admission_bridge.py
```
