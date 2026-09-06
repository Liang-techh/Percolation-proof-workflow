# Targeted exact audit history

`output/run-20260905T202634Z-e39dc9a3`: first execution passed. The run
snapshotted audit.py, verify.py, source algebra, reference and original mass/
potential coefficients before the child started. The synchronous terminal
receipt contains AUDIT_EXIT_CODE=0. It verifies 43 exact symbolic entry
identities, source membership of the point witness and an exact positive
congruence, not a trajectory, uniform storage or J budget.

No failed audit was hidden, no source/project was modified, and no full
regression or dependency installation was run. This directory has no Lean
verification claim; its companion finite-vector lemma is independently
compiled and recorded from routeb_signed_gap_lean.
