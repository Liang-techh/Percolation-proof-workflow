# Terminal gate formalization receipt

Status: PASS

Successful run: output/run-WLanCOzI
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib commit 0df444a360eaa60ab8c11dca51a86af692955474
-DwarningAsError=true, cached dependencies only
TerminalGate_COMPILE_EXIT_CODE=0; VERIFY_EXIT_CODE=0
SNAPSHOT_HASHES_UNCHANGED=true

## Hashes

| Artifact | SHA-256 |
|---|---|
| TerminalGate.lean | 1029fb6aa8c374b46e0a75e7180df98d4d6aec4f1079c895f8ff242c5e49cb89 |
| TerminalGate.olean | 0113f2184e87c2239b39420b7b9a8818838ac7f054bb029beb66a969323cd182 |
| terminal.log | 6c24f5187ac74432c6928ba835164b96bda624ae4d9711d5ad6fb01b001b84ae |
| before_run.sha256 | d46d273e6f92b1fe46f8b3e51ca7faa02014a48926b413f28e08bdfb4505117c |

The successful run is byte-identical to the delivered source. The four
exported theorem reports contain only propext, Classical.choice and
Quot.sound; there is no sorry, admit or custom axiom in the source.

Exported entry points are decayPolynomial_nonneg,
gate_implies_terminal_lower_bound, fixed_terminal_gate_failure, and
no_uniform_bZero_gate_of_strict_residual. They formalize a bounded terminal
residual gate with explicit hypotheses. The source quartic floor, order
bounds, physical DH binding, positive-supply budget and actual J<=1 remain
external obligations. This sidecar is not a certificate admission and does
not modify the persistent registry.
