# Prospective attempt history

Each output/run-* directory is created before its compiler invocation.
Its before_run.sha256 and terminal.log are authoritative for that attempt.
1. `run-PI4odfJr`: exit 1. Finite-sum scalar extraction in the homogeneous
   block expansion, a final definitional unfolding in optimalZ_balance,
   and two unused simp arguments. Failed downstream axiom prints include
   sorryAx and are not verification evidence. Fixed in the next snapshot.
   The centered dual SOS extension was added after this run's snapshot.
2. `run-f8hFVD0S`: exit 0 (2026-09-05T20:56:57Z). Fixed-Z losslessness,
   finite-vector congruence, coercivity, and generic centered dual SOS/bound
   all passed warningAsError=true. All printed axioms were only propext,
   Classical.choice, Quot.sound. Source SHA256:
   55014c3d2e3e7b2231d7a9c86dad78109c38fd0743232bff85986aaed45951ac.
   After this snapshot, added strict positivity, actual affine recentering,
   the full affine scalar gate, and frozen center equations; these require
   a fresh compile and are not covered by this run.
3. `run-fPFjFk7U`: exit 1. The affine recentering, strict positivity, and
   complete affine centered gate checked without sorryAx; the two frozen
   center identities failed only because beta reduction was needed before
   rewriting their component equations. Added explicit reduction and a
   composed frozen_affine_dual_bound handoff for the next attempt.
