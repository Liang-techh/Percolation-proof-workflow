# P5-026 ConeIndex: signed-cover consumer follow-up

Date: 2026-09-08. Scope: source-independent index/cover interface only.

## Current result and changed files

The requested concrete indexing infrastructure already exists in
`NEW_CONE_INDEX_Core.lean`; this run preserved that file and independently
rechecked it locally. This run adds only:

- `NEW_CONE_INDEX_SignedCoverConsumer.lean`
- this review

No existing P5 file, state, registry, K_path/source artifact, Lake configuration,
or existing review was edited. No `.olean` output was requested. No admission,
integration, commit, or remote CI action was performed.

## Reading and concrete interface

Read `P5FeasibleConeSPN.lean`, `NEW_exact_geometry_spn.py`, the existing
`NEW_CONE_INDEX_Core.lean`/checker/review, and both P5-026 reviews:

- `review-T-P5-026-guyuefangyuan-20260907T1031.md`
- `review-T-P5-026-juyangxianzun-20260907T1048.md`

The latter review records a historical open concrete enumeration obligation.
The existing standalone ConeIndex core now supplies the following local
source-independent interface; this does not change that review or integrate
its portable SPN sidecar:

| Obligation | Existing core interface |
|---|---|
| finite labels | `ConeIndex = Cone × Cone`, cardinality 36 |
| global sign action | `flip`, `flip_flip`, `flip_ne` |
| 18 representatives | `Representative = Fin 3 × Cone`, `counts` |
| unique signed selection | `indexEquiv`, `expand_select`, `select_expand` |
| exact sign orbits | `same_representative_iff`, fiber cardinality 2 |
| arbitrary indexed sums | `sum_preserving_multiplicity` |
| full cover witnesses | `coverWitnessEquiv`, preserving the same parameter vector |
| boundary multiplicity | `cover_multiplicity`, `origin_multiplicity = 36` |

Representative first-channel order is `(pp, pnPos, pnNeg)`. Reversing the first
channel also reverses the second; independent channel reversal is not the
36-to-18 quotient. Equality of specialized matrices never removes index labels.

## New consumer and its precise hypotheses

For arbitrary representative type R, parameter type U, additive-group state V,
chart `R → U → V`, and admissibility predicate on U, define

```text
oriented r false u = chart r u
oriented r true  u = -chart r u.
```

The common cover premise is:

```text
forall z, exists r b u, admissible u and oriented r b u = z.
```

`all_iff_signed` proves that a state predicate holds globally iff it holds on
all admissible chart parameters in BOTH directions. No evenness is assumed.

`all_iff_representatives` removes the Bool quantifier only with the explicit
premise `forall z, P(-z) iff P(z)`. This is a property consumer, NOT a quotient
of cover witnesses and NOT a replacement for the core multiplicity sum.

`non_even_guard` proves that nonnegativity on nonnegative real parameters
does not imply nonnegativity of every real state (the witness is -1). Thus
the evenness premise cannot simply be omitted in general.

For the concrete core, the intended arguments are `R := Representative`,
`U := Vec`, `V := Vec`, `admissible := Orthant`, and
`chart r u := RouteBP5ConeIndex.chart (representativeCone r) u`.
Its signed cover and `chart_expand` give the required cover premise.
This argument mapping is documentation, not a newly compiled cross-module
adapter: the new file intentionally imports only Mathlib and is generic.

At a fixed state z, membership of cone c need not equal membership of flip(c).
The valid geometric relation also negates z. Therefore applying `sum_invariant`
to fixed-state membership without proving its premise would be incorrect.
Keep `cover_multiplicity` with both summands; at the origin all 36 labels remain.

## Focused verification performed this run

Direct local Lean 4.32.0 checking, using existing Mathlib dependency caches:

- New consumer: no error diagnostics; three printed axiom audits. The two
  generic equivalences depend only on `propext`; the real counterexample uses
  `propext, Classical.choice, Quot.sound`. No `sorryAx`.
- Existing core: exit 0, all 16 printed audits use only
  `propext, Classical.choice, Quot.sound`. No `sorryAx`.
- Existing Python checker: normal and optimized (`-O`) runs both exit 0.
  Each checks 36 labels, 18 representatives, 1296 orbit pairs, 169 exact
  boundary probes and 11 rejected negative controls. Python probes are not
  universal real proofs; the universal cover is in the checked Lean core.

Reproduction from repository root (outputs only to console):

```powershell
$taskLeanPaths = Get-ChildItem -LiteralPath examples/local_fkg/.lake/packages -Directory |
  ForEach-Object { Join-Path $_.FullName '.lake/build/lib/lean' } |
  Where-Object { Test-Path -LiteralPath $_ }
$env:LEAN_PATH = $taskLeanPaths -join ';'
& C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_SignedCoverConsumer.lean
& C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_Core.lean
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_check.py --self-test
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_check.py --self-test
```

The checker confirmed its frozen input hashes for the original proof attempt
and geometry checker. No rebuild of all dependencies or full regression was run.

## Explicitly not established

No concrete K_path, source authentication, physical/Float64 residual binding,
18 concrete SPN certificates, P8/trajectory coverage, P5 closure, or registry
eligibility is supplied or implied. Local Lean checking of these source-independent
interfaces does not close any of those separate obligations.
