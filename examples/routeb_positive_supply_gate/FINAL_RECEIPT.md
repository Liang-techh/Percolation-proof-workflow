# Positive-supply gate receipt

Status: PASS

Successful run: output/run-IL9p8Cz4
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib commit 0df444a360eaa60ab8c11dca51a86af692955474
-DwarningAsError=true; cached dependencies only
PositiveSupplyGate_COMPILE_EXIT_CODE=0; VERIFY_EXIT_CODE=0
SNAPSHOT_HASHES_UNCHANGED=true

| Artifact | SHA-256 |
|---|---|
| PositiveSupplyGate.lean | f5002568a092ffad7ed1c6a42fa4ec6ce4544bf9d4eb0001b59a73eca334d3f4 |
| PositiveSupplyGate.olean | c47591997657ca175c1377d65450df35cfbe7955d03173f92534fd6e3eb33627 |
| terminal.log | see output/run-IL9p8Cz4/terminal.log |

The four exported theorem reports contain only propext, Classical.choice and
Quot.sound. The leaf proves only generic finite first-order and coefficient
budget implications with explicit hypotheses. It does not prove a uniform
positive-supply bound, physical source binding, or J<=1, and does not modify
the theorem registry.
