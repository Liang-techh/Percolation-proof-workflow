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

## Second compile: successful initial gate

`output/run-qAQf3tVM` completed with LEAN_COMPILE_EXIT_CODE=0 and
VERIFY_EXIT_CODE=0. All six printed theorems used only propext, Classical.choice
and Quot.sound. The compiled artifact SHA256 is
`4faa85cf54e88db854132fbcb7037200703b97ea2dfda6f078982a5d703ba9de`.
This successful source and its initial N,H,J<=.04 theorem remain intact.

## Final refined constants

The third source revision retains all earlier theorems and adds the FINAL
N=2877/200000, H=403089/500000, J<=1/20 scalar gate. Its wrapper snapshots both
gain receipts before compilation. The actual third-run result is to be recorded
after completion; no nonlinear J estimate is proved by this source revision.

## Third compile: successful refined residual gate

`output/run-wP7lELi5` completed with LEAN_COMPILE_EXIT_CODE=0 and
VERIFY_EXIT_CODE=0. All eight printed theorems used only standard axioms.
The compiled artifact SHA256 is
`1d66c00fe8ad9b5ad47edccf6d68f6e651ecf9e498967ffe8ddb827dcca366de`.
This J<=.05 residual gate remains available but is not mandatory for the
original P<5.6 and terminal Q<12 goals.

## Direct original-output extension

The fourth source revision adds the primary J<=1 state-output gates using
the final direct-output receipt run-20260905T194943Z-9ad8ada4. It changes no
target, initial set or input family and proves no nonlinear J bound.
A first multi-file editor patch for this extension failed on stale context in
this history file; no changes from that patch were applied, as checked by a
read. The extension was then applied in smaller patches. This was an editor
failure, not a Lean failure. The fourth run's source and all three gain receipts
are saved before compilation; its status is reported after completion.

## Fourth compile: successful direct-output clauses

`output/run-WcLvKoYF` completed with LEAN_COMPILE_EXIT_CODE=0 and
VERIFY_EXIT_CODE=0. All eleven printed theorems used only standard axioms.
Artifact SHA256:
`f3f49a00a0524c20dd595ceb4a0a7eb2ec9eb7cd6a75de76558ba0aa25d2b5e9`.

The final source revision exposes the requested paired name
`original_outputs_under_J_one` by combining the two already compiled fixed-
parameter clauses. This final compile is only to verify that named handoff;
there is no additional matrix audit or new gain estimate. The main's mistaken
verify.log filename lookups are not mathematical or Lean proof failures.
