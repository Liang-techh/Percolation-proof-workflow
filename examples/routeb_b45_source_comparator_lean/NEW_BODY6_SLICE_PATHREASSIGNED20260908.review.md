# GH-MIXED-BODY6-PATH-REASSIGNED: independent contract audit

New sidecar status: **OPEN_UNCOMPILED / pending**. The reassigned path lane
reviews contract preservation and typed domain boundaries. No main Lean
compilation, regression, integration or registry mutation was performed.

## Exact repair comparison

Current PATHDOMAINPROJECTION source SHA-256:
`f55de2b76ed401e7962b1494d02826c8fc2f951d7137f02461edeb56d5757d62`.

The original same-stem review records the pre-repair source SHA-256:
`c3d0432fb2b53815bb9e23271ecadfa871e5526a96b9bf7b533efe392d2aa6ac`.

A read-only Python check replaced exactly this current proof fragment in
memory, without writing the dependency:

```lean
  have hCap' : F t (path t) + B ≤ cap + B := by
    simpa [add_comm] using (add_le_add_right (hCap t ht) B)
  exact hCap'.trans hBudget
```

with the historical fragment:

```lean
  exact (add_le_add_right (hCap t ht) B).trans hBudget
```

The resulting UTF-8/LF bytes hash exactly to the recorded pre-repair hash.
Thus this comparison supports preservation of the entire source outside
that proof fragment, including definitions, theorem binders, hypotheses and
conclusions. It is stronger than comparing an informal theorem summary.

The repair normalizes addition order through an explicitly typed intermediate.
The source cap is still F<=cap, value identity G=F+B and budget cap+B<=bar;
B is paid once. No sign condition, initial-only substitution, new domain,
time-horizon extension or missing physical hypothesis was introduced.
The separate already-shifted consumer remains unchanged and pays no extra B.

## Typed sidecar

`TransferInputs` packages the original five hypotheses with every index
explicit: project, fixed D, Q, full-state path, F, G, B, cap and bar.
`repaired_contract_adapter_attempt` calls the existing theorem with those
five fields and exactly its original conclusion. It does not reprove the
dependency or supply any field for an actual candidate.

`pullbackDomain project Q` is the time-independent preimage of Q.
The sidecar makes three precise statements about it:

- Its domain projection follows by definition.
- Whole-path membership in it is equivalent to projected membership in Q
  at every time in [0,1]; this still requires a whole-path proof.
- Membership in a specified D plus DomainProjection yields membership in
  this preimage. The reverse implication for an arbitrary specified D is
  not asserted.

The exact counterexample uses Q=univ, project=id and path(t)=t. Projected
membership holds for the whole horizon, yet the path leaves the specified
D(t)=(-infinity,0] at t=1. It reuses the existing domain obstruction without
repeating its proof. A pullback may omit velocity or other physical state
constraints, so selecting it cannot discharge membership in the actual D.

## Evidence and remaining obligations

The focused receipt
`agent_review_inbox/review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T082220.md`
reports PATHDOMAINPROJECTION exit 0 under Lean 4.32.0 and the baseline
axioms propext, Classical.choice and Quot.sound. Its PATHDOMAINPROJECTION
hash matches the current inspected source. That dependency success is
acknowledged without rerunning it. Historical OPEN_UNCOMPILED prose remains
a historical snapshot, not a refutation of the newer receipt.

The new sidecar itself has no compile/axiom receipt. Static source inspection,
placeholder scan, exact reconstruction and hash validation do not supply one.
Its SHA-256 is:
`2343ca9a6ad775643e344d2e78d66f4dd7960fa0c10a910fdb9864da1fa402ec`.

The actual coordinate projection, fixed-domain whole-path inclusion, storage
identity/source cap and DH binding remain external evidence. No initial
condition is promoted into path inclusion; no derivative identity is promoted
into an integrated bound. ODE existence/continuation, coverage, physical
source semantics, comparator acceptance and admission remain unproved here.
Keep this submission pending; no old leaf, receipt, registry or state was edited.
