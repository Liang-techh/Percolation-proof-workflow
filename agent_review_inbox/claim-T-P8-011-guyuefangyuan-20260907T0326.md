---
kind: task_claim
task_id: T-P8-011
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T03:26:00-06:00
inspected_commit: fed35ac879f20ebc3c0371219d552a652db83d2f
status: claimed
---

# T-P8-011 — ramp-eliminated flowpipe transport and domain compatibility

I claim a new disjoint mathematical child downstream of `T-P8-008`. Scope: prove the set/trajectory-level transport between a 12-state explicit-time mechanical flowpipe for `w=c*t` and the existing 14-state ramp representation, and derive the exact necessary source-domain condition on the ramp coordinate over `[0,T]`. This does not redo the `T-P8-008` algebra/Lean sidecar, does not bind Julia source semantics, and does not claim ODE existence, interval enclosure, flowpipe construction, provenance, or admission.
