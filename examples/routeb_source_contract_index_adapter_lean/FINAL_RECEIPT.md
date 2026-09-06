# Final receipt — Route-B source-contract index adapter

Status: **PASS — pinned Lean compiled candidate; not registry-admitted**

The sidecar fixes the source/body indexing convention without unfolding any DH
matrix entry:

- human body 4 (`Fin 6` index 3) uses COM origin slots 3 and 4;
- human body 5 (`Fin 6` index 4) uses COM origin slots 4 and 5;
- the last active Jv/Jw column of body 4 reads parent-axis slot 3;
- human joint 5 is inactive for body 4;
- the last active Jv/Jw column of body 5 reads parent-axis slot 4;
- human joint 6 is inactive for body 5.

Successful pinned run: `output/run-a7DRfXYo`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SourceContractIndexAdapter_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
DH_NUMERIC_EXPANSION=AVOIDED
JULIA_FLOAT64_BINDING=OPEN
MAIN_DAG_STATE_UNCHANGED=true
```

All thirteen `#print axioms` reports contain only `propext`,
`Classical.choice`, and `Quot.sound`. There are no `sorry`, `admit`, or axiom
declarations.

Hashes:

```text
SourceContractIndexAdapter.lean  2a18c7b6733af6245f3e5ba6dedd714a9ec7f28fd010122c0258611ce7aac452
SourceContractIndexAdapter.olean 50d88296516473e139828678507fda455467b052dd3330e5563f68f4aa41a9da
terminal.log                     ab5f101d1275530cfef9cf5e24388fa9da04236c42fc3332a2d7b2238d1f5584
```

Exactly one Lean compile was started for this sidecar. It is intentionally not
inserted into the main DAG or registry. The authoritative state was observed at
revision 95 with registry count zero after the run; that revision may include
unrelated concurrent workflow work, not this sidecar.
