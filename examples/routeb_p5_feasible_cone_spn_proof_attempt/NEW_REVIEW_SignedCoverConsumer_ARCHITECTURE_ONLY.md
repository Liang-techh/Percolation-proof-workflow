# SignedCoverConsumer independent scope/provenance review

Date: 2026-09-08.
Suggested task_id: `T-P5-026-SIGNED-COVER-CONSUMER-ARCHITECTURE`.
This is a proposed descriptive child identifier only, not an allocated task or
StateStore node. No queue, StateStore, registry, or admission update is requested
or performed by this review.

**Classification: architecture-only; generic source-independent sidecar.**
Local Lean checking passed; concrete P5 frontier binding remains absent.

## Exact statements

Namespace: `RouteBP5ConeIndexConsumer`.
Parameters: arbitrary types `R U V`, `[AddGroup V]`, `chart : R → U → V`,
`admissible : U → Prop`, `P : V → Prop`. Define
`oriented chart r b u := if b then -chart r u else chart r u`.

The shared hypothesis is

```text
cover : ∀ z, ∃ r b u, admissible u ∧ oriented chart r b u = z.
```

The exact conclusions are:

```text
all_iff_signed:
  (∀ z, P z) ↔ ∀ r b u, admissible u → P (oriented chart r b u)

all_iff_representatives:
  under even : ∀ z, P (-z) ↔ P z,
  (∀ z, P z) ↔ ∀ r u, admissible u → P (chart r u)

non_even_guard:
  (∀ u : ℝ, 0 ≤ u → 0 ≤ u) ∧ ¬ (∀ z : ℝ, 0 ≤ z).
```

The last theorem is a simple real counterexample guard, not a complete typed
countermodel instantiation of the generic cover interface. Evenness is an
explicit sufficient transport premise; this file does not prove that every
individual predicate must be globally even for a particular reduction to hold.

There is no Fintype hypothesis, cardinality theorem, concrete ConeIndex import,
matrix definition, SPN instance, residual, or physical source object in this
file. Consequently it does not independently prove a concrete 36-to-18 result
or a multiplicity-preserving cover. Those belong to the existing separate core.
Its useful addition is separating the signed-cover consumer from the stronger
consumer that is allowed to discard orientation.

## Source and provenance

Artifact: `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_SignedCoverConsumer.lean`.
SHA-256: `ea9a87281e096caf2e3b082a31dd0fbb00efc85016376dbd8ad735b39d41f4b8`.
Inspection repository HEAD: `62ee72feec94987ec95378ddd1a593df355ec977`.
HEAD identifies inspection context, not a claim that this uncommitted artifact
is contained in that commit. The artifact hash identifies the checked bytes.

The implementation imports only `Mathlib.Data.Real.Basic` and `Mathlib.Tactic`.
Its mathematical motivation is the P5-026 closed-cone/global-sign review by
古月方源 (`review-T-P5-026-guyuefangyuan-20260907T1031.md`) and the historical
generic sidecar review by 巨阳仙尊 (`review-T-P5-026-juyangxianzun-20260907T1048.md`).
Those reviews are context, not a kernel or source-authentication receipt for
this new artifact. Their old remote CI claims were not revalidated here.

The intended relationship with the existing ConeIndex core is documented:
take `R := Representative`, `U := Vec`, `V := Vec`, `admissible := Orthant`,
and representative chart `fun r u => chart (representativeCone r) u`.
The core's `signed_representative_cover` and `chart_expand` are the intended
cover inputs. This file contains no compiled cross-module instantiation of
that mapping. It also does not import or bind the old `P5FeasibleConeSPN.lean`
or execute `NEW_exact_geometry_spn.py` as proof evidence.

## Local Lean evidence: correction of the suggested uncompiled boundary

It would be inaccurate to label this artifact "not compiled locally".
The preceding task ran Lean on it, and this follow-up independently reran
the consumer alone with explicit propagation of its own process exit code:

```powershell
$taskLeanPaths = Get-ChildItem -LiteralPath examples/local_fkg/.lake/packages -Directory |
  ForEach-Object { Join-Path $_.FullName '.lake/build/lib/lean' } |
  Where-Object { Test-Path -LiteralPath $_ }
$env:LEAN_PATH = $taskLeanPaths -join ';'
& C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_SignedCoverConsumer.lean
exit $LASTEXITCODE
```

Observed exit code: **0**. All three axiom audits printed:

```text
all_iff_signed:          [propext]
all_iff_representatives: [propext]
non_even_guard:          [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, error or warning appeared. This is local elaboration/kernel
checking against existing Lean 4.32.0/Mathlib caches, not a clean dependency
rebuild, independent remote receipt, or admission event. No `.olean` was
requested and no runtime artifact was written. The compiler output is in
the task tool transcript; this Markdown records the observation but is not
a registered machine-verifiable receipt.

**What has not been compiled or established:** a cross-module concrete P5
adapter; an actual same-tube/source predicate with its evenness proof; a
source-bound K_path or 18 SPN witnesses; any P5 closure consumer instance.

## Current frontier relevance and disposition

Read-only literal reference search across `src`, `artifacts/routeb_6dof`,
`agent_review_inbox` and `examples` found this namespace/artifact only in its
own Lean file and preceding review. This is bounded textual evidence, not
a claim to have exhaustively resolved every possible indirect reference.

The inspected task queue's P5-093 frontier and same-tube-source packet notes
require actual source witnesses such as `F, DF, W, Wt, DW, b, Db, e` and
coverage on the same tube. This generic orientation lemma supplies none of
those objects and does not discharge a named live frontier dependency.

Recommendation: retain under the suggested P5-026 architecture child as a
reusable library candidate, **architecture-only**, not a closure-priority
P5-081..093 result and not a conditional pass for an actual source packet.
Only revisit integration when a concrete caller and exact remaining theorem
obligation are identified. No further generic strengthening is needed now.

No concrete K_path, source/provenance authentication, P5/P8/M4 closure, or
registry eligibility is claimed. This follow-up adds only this review and
does not modify the sidecar, StateStore, registry, queue, or existing review.
