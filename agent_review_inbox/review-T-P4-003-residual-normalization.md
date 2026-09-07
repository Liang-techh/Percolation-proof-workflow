---
kind: review_result
task_id: T-P4-003
source_agent: Codex
created_at: 2026-09-06T22:40:00-06:00
integration_status: pending
---

# T-P4-003 review: force / PMI-side residual normalization

## Scope and inspected evidence

This is a read-only audit. I did not modify external Route-B source, registry
state, or run a full regression.

Inspected:

- `agent_review_inbox/task_queue.md`
- `docs/routeb-c2-d-normalization-audit.md`
- `agent_review_inbox/review-T-P4-002-one-channel.md`
- `agent_review_inbox/review-T-DAG-002-child-dag.md`
- `B45SchurResidualRepair.lean`
- `artifacts/routeb_agent_p4_source_bridge_next_20260906T092639Z/SourceToP4Bridge.lean`
- `artifacts/routeb_agent_p4_next_semantic_repair_20260906T100414Z/run-pinned/P4InterfacePMI.lean`

The inspection stayed within the requested boundary:

- force residual `l = I f - M0 a`
- PMI-side residual `d`

It did not attempt to close true-DH binding, coverage, or the P4 parent.

## Typed normalization conclusion

The available Lean sidecar already separates the two roles that matter here:

- `SourceToP4Bridge.source_force_expansion` and
  `SourceToP4Bridge.source_descriptor_residual_zero` keep the source-side
  force residual explicit.
- `RouteBAgentP4InterfacePMI.interfaceEquality_is_dRow` identifies the
  PMI-side interface condition as a `dRowEquality` premise.
- `RouteBAgentP4InterfacePMI.fullStatePMI_eq_schurResidual_on_interface`
  gives the algebraic bridge from the full block to the Schur residual only
  after that interface premise is admitted.

That is enough to justify a narrow typed normalization claim, but only as a
conditional adapter. It does not justify reusing `l` as `d`, and it does not
turn the source force residual into a PMI-side acceleration residual.

## Theorem signature

Smallest useful child theorem shape:

```text
theorem source_force_to_pmi_normalization
    (sourceEll sourceD sourceP : ℝ)
    (x a : ℝ)
    (h_force : l = I * f - M0 * a)
    (h_interface : RouteBAgentP4InterfacePMI.interfaceEquality sourceEll sourceD x a)
    (hd : 0 < sourceD) :
    RouteBAgentP4InterfacePMI.fullStatePMI sourceP sourceEll sourceD x a =
      RouteBAgentP4InterfacePMI.schurResidual sourceP sourceEll sourceD x
```

The exact names will depend on the eventual sidecar, but the theorem must keep
the source-side force residual and the PMI-side `d` as distinct typed objects.
It should only transport through the explicit interface premise, not through an
implicit semantic identification.

## Dependency chain

The minimal dependency chain is:

1. `B45SchurResidualRepair.Binding` for the source/descriptor residual binding
   discipline.
2. `SourceToP4Bridge.source_force_expansion` for the exact force-side
   expansion.
3. `SourceToP4Bridge.source_descriptor_residual_zero` for the residual-zero
   transport pattern.
4. `RouteBAgentP4InterfacePMI.interfaceEquality_is_dRow` for the typed
   interpretation of the PMI-side row condition.
5. `RouteBAgentP4InterfacePMI.fullStatePMI_eq_schurResidual_on_interface`
   for the Schur reduction on an admitted interface.

This is a typed-adapter dependency chain, not a physical certificate chain.

## Evidence boundary

What this audit can support:

- the source force residual is a generalized-force quantity, not an
  acceleration residual;
- the PMI-side `d` is a separate scalar interface parameter;
- a conditional algebraic bridge is available once the interface premise is
  admitted;
- the bridge can be used as a focused Lean sidecar without full regression.

What this audit does not support:

- true-DH closure;
- cell coverage;
- any claim that the source force residual and PMI-side `d` are the same
  object;
- any claim that the P4 parent is closed.

## Blocker

The blocker is semantic, not syntactic:

- no admitted theorem in the inspected material identifies `l = I f - M0 a`
  with the PMI-side residual `d`;
- the source bridge still needs an explicit normalization lemma that carries
  the force-side quantity into the PMI interface without collapsing the typed
  distinction;
- without that lemma, the sidecar stays conditional and cannot be promoted to a
  true-DH or coverage result.

## Focused sidecar status

The existing artifacts already provide the right shape for a focused sidecar.
I did not run a full regression or attempt to close the parent, because that
would exceed the requested scope.

The safest next Lean child is a one-step normalization lemma that rewrites the
source-side force residual into the PMI interface hypothesis and then delegates
to `fullStatePMI_eq_schurResidual_on_interface`.

