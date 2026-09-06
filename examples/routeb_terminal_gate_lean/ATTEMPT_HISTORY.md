# Attempt history

Both snapshots are preserved under `output/`.

| Snapshot | Result | Evidence |
| --- | --- | --- |
| `run-dFJTqX02` | Failed before compilation output was recorded | The prospective snapshot exists, but the terminal log stops at the Lean command. |
| `run-FELXKx7A` | Failed, `VERIFY_EXIT_CODE=1` | `decayPolynomial_factor` rewrite failure, an invalid unfold target in `fixed_terminal_gate_failure`, and warnings-as-errors for unused hypotheses. |

The second log also prints `sorryAx` in theorem axiom reports because the
source did not elaborate successfully. Those reports are not evidence of a
compiled theorem and are explicitly rejected here.

No `FINAL_RECEIPT.md` is provided. This formalization is blocked and is not
promoted; the exact Python terminal audit remains the active route.

3. run-WLanCOzI: exit 0 after the coordinator repaired the stale declaration
   references and the terminal-supply unfold. The four exported gate lemmas
   compile with warnings-as-errors and their axiom reports contain only the
   standard axioms. This is the first successful terminal Lean sidecar; it
   remains source-unbound and does not prove the physical candidate or J<=1.
