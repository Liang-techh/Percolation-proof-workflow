# Attempt history

All compile attempts preserve GainBridge.lean, verify.sh, and available report
files before execution. The terminal log is written synchronously and includes
both LEAN_COMPILE_EXIT_CODE and VERIFY_EXIT_CODE. No run is declared successful
before its observed exit status. The finite-horizon convolution derivation is
not a Lean theorem in this leaf; only the displayed scalar gates are compiled.

During read-only lemma discovery, rg was unavailable inside WSL, so grep was
used. The old Data/Real/Sqrt.lean path was only a deprecated forwarding module;
the sqrt_le_iff declaration was found in Analysis/Real/Sqrt.lean. These were
discovery commands, not failed Lean compile attempts.

## First compile: failed, retained

`output/run-7YTDR4EX` exited with LEAN_COMPILE_EXIT_CODE=1 and VERIFY_EXIT_CODE=1.
The scalar admission/feedback lemmas elaborated and printed only standard
axioms. The run nevertheless FAILED because direct4Squared and direct5Squared
were declared computable despite division in Real. The two
`lean.dependsOnNoncomputable` diagnostics and original source are preserved.
They were repaired by marking those two definitions noncomputable.

The next source revision also adds the main's newly supplied exact N,H gate.
Its gain receipt is copied and hashed before compilation. The second run's
actual status is recorded only after its subprocess finishes.
