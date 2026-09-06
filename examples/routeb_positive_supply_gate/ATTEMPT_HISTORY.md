# Positive-supply gate attempts

The final run output/run-IL9p8Cz4 froze the current source, analytical audit,
derivation and runner before compiling. The exact Fraction audit passed and
the four generic Lean theorems compiled with warnings-as-errors and standard
axioms only.

The runner itself had two repaired setup/elaboration attempts before the final
run: a shell snapshot path escaping bug and unused/normalization issues in
the Lean source. Those diagnostics are not hidden; only run-IL9p8Cz4 is the
successful receipt. No LP, trajectory, scan or broad regression was run.
