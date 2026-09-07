# Attempt history

This sidecar is intentionally small and uses only exact real pair algebra.

- `run-uqSFVpAd`: failed because the exact-real definitions needed an explicit
  `noncomputable section`, pair equality was not opened with `Prod.ext`, and
  the first `rho_kc` proof left division normalization goals.
- `run-k5bfFvda`: definitions and theorem proofs compiled, but the unnamed
  `noncomputable section` was closed with the wrong `end` form.
- `run-AeO1JYiI`: repaired candidate; compile/verify passed with standard
  axioms only and no `sorry`/`admit`.
- `local-20260907-kc-coordinate-budget`: added the normalized-to-force
  coordinate theorem and the exact `7/18750` block-domain squared budget;
  pinned Lean compilation and axiom receipt are pending on the GitHub Lean
  worker, so this extension is not yet admitted.
