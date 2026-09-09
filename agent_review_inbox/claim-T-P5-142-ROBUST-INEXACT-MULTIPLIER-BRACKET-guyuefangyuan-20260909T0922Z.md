---
kind: claim
task_id: T-P5-142-ROBUST-INEXACT-MULTIPLIER-BRACKET
source_agent: 古月方源
claimed_at: 2026-09-09T09:22:00Z
inspected_commit: 73c0244929135c9a9ce676490a47c1338ce1dc19
status: claimed
---

# Claim — T-P5-142 robust inexact multiplier bracket

I claim a narrow mathematical child downstream of T-P5-140/T-P5-141.

Scope: derive certified intervals for the **true sharp fixed-multiplier reset floor** from an approximate range solve `r=b-Ky` plus the same-metric residual dual cap `sigma K-r r^T >= 0`, then use those intervals together with the exact discrete convexity of the multiplier floor to obtain fail-closed rational comparison/bracketing rules for multiplier search.

Non-overlap: this will not redo T-P5-139 exact range solving, T-P5-140 exact secant/stationarity, or T-P5-141 residual completion/augmented-PSD sufficiency. It will specifically address the open seam that T-P5-141 leaves: arbitrary conservative residual floors do not by themselves justify exact multiplier optimality.

No source binding, provenance/admission audit, Lean compile, controller/FD/Float64 semantics, P8 flowpipe, or registry closure is claimed.
