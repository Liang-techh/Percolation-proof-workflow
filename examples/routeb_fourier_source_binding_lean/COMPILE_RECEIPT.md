# Compile receipt: P3 exact coefficient bridge

Status: `PASS`.

- Lean: `4.33.1`, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib cache: `0df444a360eaa60ab8c11dca51a86af692955474`
- Command: `wsl -d Ubuntu -- bash examples/routeb_fourier_source_binding_lean/verify.sh`
- Attempt directory: `output/run-kmTEX16O`
- `ExactCoefficientBridge_COMPILE_EXIT_CODE=0`
- `VERIFY_EXIT_CODE=0`
- `warningAsError=true`

The printed axiom reports for the exported theorems contain only
`propext`, `Classical.choice`, and `Quot.sound`.  No `sorry`, `admit`, or
user-declared axiom is used.

The receipt covers only the generic exact evaluator bridge.  The source/table
coefficient equality is the separate exact Python checker leaf recorded in
`CHECK_RESULT.json`; its source hash and exactization convention remain
mandatory provenance premises.
