# Actual direct-compiler results

Final verification: **PASS**, 2026-09-05T18:10:15Z.

- [Current source](PortAbsorption.lean)
- [Verifier](verify.sh)
- [Successful compiler output](output/run-WBILxhTq/compile.log)
- [Successful full verification log](output/run-WBILxhTq/verify.log)
- [Exact successfully compiled source snapshot](output/run-WBILxhTq/PortAbsorption.lean)
- [Compiled artifact](output/run-WBILxhTq/PortAbsorption.olean)

The final log records `LEAN_COMPILE_EXIT_CODE=0` and `VERIFY_EXIT_CODE=0`.
Lean: 4.33.1, binary commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`.
Compilation used `-DwarningAsError=true` and cached libraries with the direct
compiler. No broad tests, dependency build/download, Julia execution, or solver run.

All nine `#print axioms` reports in the successful log list only
`propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx` or
source-specific axiom in the compiled proof dependencies.

Final SHA-256 values:

```text
PortAbsorption.lean
bd7d97ac8ad3c764e70cb69c94a0fc20d51a35c178ac509bebf5e43bf93800fb
verify.sh
dc3dbf06e74c2c41ae1acc1e344d83ad41a315c19a427911805dcc85cdce649a
PortAbsorption.olean
37e8e12957f4675af5f9c77e7daf5215c0c980af49df5d2da7bc7b560bec78db
```

## Retained failures

Every run has its own source and verifier snapshots. Logs are real compiler
output and have not been rewritten to hide failures.

| Run | Exit | Actual issue | Logs |
| --- | --- | --- | --- |
| `run-OC9mzFDq` | 1 | Missing finite-sum import/lemma, sum distribution, negated-division normalization, and numeric denominator normalization. | [compile](output/run-OC9mzFDq/compile.log), [verify](output/run-OC9mzFDq/verify.log) |
| `run-ppYU1b6k` | 1 | Sum rewrite direction and inequality normalization in the constant specialization. | [compile](output/run-ppYU1b6k/compile.log), [verify](output/run-ppYU1b6k/verify.log) |
| `run-w5aD94YY` | 1 | All proofs elaborated, but the unnecessary `<;>` tactic-sequencing linter failed under warnings-as-errors. | [compile](output/run-w5aD94YY/compile.log), [verify](output/run-w5aD94YY/verify.log) |

The first run's log includes `LEAN_COMPILE_EXIT_CODE=1`; its final EXIT-trap
line was not captured with the inherited process-substitution logging style.
The command itself returned exit 1. The verifier was changed to direct log
redirection with replay on exit; subsequent logs contain both exit markers.
The first two failed compilations show Lean's error-recovery `sorryAx` reports.
Those failed snapshots are not the accepted proof. The successful final source
has no such dependency.

## Scope and remaining application premise

The accepted theorem requires the actual port enclosure
`sqNorm r <= rhoSq * AB` and actual scalar positivity `0 <= phi`, with
`0 <= nu` and `0 < sRes + nu`. Connecting these generic real quantities to the
robot's corrected dissipation and proving domain membership are external work.

The inspected report explicitly warns that the current acceleration domain is
missing and Phi is unbounded below for free acceleration. This result does not
claim current SOS feasibility or close that domain gate. The main task retains
the descriptor-compatible acceleration bound and domain obligation.

The three inspected target files were read only. Their SHA-256 values were
rechecked during verification and matched the values recorded in README.md.
