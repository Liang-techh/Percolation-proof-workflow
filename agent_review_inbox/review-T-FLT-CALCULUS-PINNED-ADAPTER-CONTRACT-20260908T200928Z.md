---
kind: review_result
review_id: review-T-FLT-CALCULUS-PINNED-ADAPTER-CONTRACT-20260908T200928Z
task_id: T-FLT-CALCULUS-PINNED-ADAPTER-CONTRACT-20260908
source_agent: Codex-pinned-adapter-contract
created_at: 2026-09-08T20:09:28Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: FROZEN_TWO_DECLARATION_HANDOFF_UNCOMPILED
contract_version: 1
classification_abstract: 1
classification_routeb: 2
lean_compile_status: not_run
comparator_status: missing
runner_dispatched: false
routeb_source_closure: false
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
shared_scripts_mutation: false
requested_action: coordinator-approved GitHub runner may consume the frozen unit; return actual evidence without promotion
---

# Pinned adapter contract: two declarations, no source producer

This is an immutable handoff, not an execution receipt. It replaces no existing
intake or review. Only this new Markdown file is written. No local/remote Lean,
Lake, comparator, CI dispatch or simulation was run.

Scope is exactly the two declarations in the frozen payload below. The earlier
full-space convenience theorem and optional FLT/cotangent port are excluded
from this unit. If a runner needs to change the statement, imports, namespace,
pins or payload, return an API_REPAIR_REQUIRED proposal in a new immutable
review; do not silently revise this contract.

## 1. Authoritative inputs

Parent review:
`review-T-FLT-CALCULUS-CHAIN-RULE-ADAPTER-20260908T200328Z.md`,
raw SHA-256
`7325701e343362a34e25956e9575250b76344bedadc21654ad4adb22240fd627`.

Target toolchain: **leanprover/lean4:v4.32.0**.
Target Mathlib repository: https://github.com/leanprover-community/mathlib4
Target commit: **81a5d257c8e410db227a6665ed08f64fea08e997**.

Current local_fkg manifest rev/inputRev and Mathlib checkout HEAD were rechecked
and agree with this target; this checks source configuration, not usable binaries.
The local manifest raw hash observed in the parent is
`6cad04cdeb731b8af3594767512923ac9b9fe7e00808f91ddcb30c846e3891f3`.
A clean GitHub adapter package need not copy local_fkg's unrelated percolation
path dependency. Record its own complete resolved dependency lock and verify
Mathlib and its dependency pins; do not pretend it used the local manifest bytes.
No automatic upgrade to FLT's Mathlib/Lean pair is allowed.

Direct imports, in order:

1. `Mathlib.Analysis.Calculus.FDeriv.Comp`
2. `Mathlib.Analysis.Calculus.FDeriv.Congr`

Both import FDeriv.Basic. This is the fixed direct import surface, not a claim
that the transitive closure has been compiled or minimized. Do not replace
these with umbrella `Mathlib`, FLT or P2M imports in this contract.

| Path under Mathlib/Analysis/Calculus/FDeriv/ | Git blob SHA-1 | Raw Git-object SHA-256 |
|---|---|---|
| Comp.lean | b569401f8f2ceb72d072d6b088af2630a164d1ed | 22b49670dfaa646c560b62e60674ac86288f32b09e920c00cf2d867c60f36a80 |
| Congr.lean | fa50ff49921b4ef098c0bd002b539889fa104963 | 5cad1d8c7480eac00c7004b6ec5ee9dd64ac80a833f10ad92936cdac4abe9673 |
| Basic.lean | 538d55195de38bdc0f57b569fd484ecea2f295b9 | a4e41e70a5c80c4289f24e2ca5e9511ca8278b2aec9ab0b9e5100f7df9ef7929 |

All three blob identities/hashes were freshly checked from raw `git show`
bytes. Relevant declarations: Comp 74-78, Congr 166-168, Basic 426-430.
Mathlib source headers name Jeremy Avigad, Sebastien Gouezel and Yury Kudryashov;
copyright 2019 Jeremy Avigad, Apache-2.0. Preserve notices in the runner package.

FLT provenance is **context only**, not a dependency:
Anthropic commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`,
`Definitions/Def_Algebra_PointDerivations.lean`,
blob `a6a95f7e3170eb079c42c30deaa06a562d42f53d`;
its Lean 4.33.1 / Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
must not be mixed into this target. Its map_comp organizes linear value
post-composition; it is not the provenance of Mathlib's analytic chain rule.

## 2. Frozen payload

Suggested runner-only filename: `RouteBChainRulePinned.lean`.
Extract exactly the single lean block between the markers below; encode UTF-8
without BOM, normalize line endings to LF and keep exactly one terminal LF.
Expected byte length: **1251**.
Expected SHA-256: **7431c74649a7d29f76039d8aaa01ac2ae18989b0da70b56227a5cedd1618a7de**.

This hash was computed from the payload text; it is not a compiled artifact
hash. No Lean file has been created locally.

<!-- BEGIN_FROZEN_ADAPTER -->
```lean
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.Calculus.FDeriv.Congr

set_option autoImplicit false
noncomputable section
universe u v
namespace RouteBChainRulePinned

variable {Z : Type u} {E : Type v}
  [NormedAddCommGroup Z] [NormedSpace ℝ Z]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {T : Z → E} {f : E → ℝ} {actual : Z → ℝ}
  {J : Z →L[ℝ] E} {ell : E →L[ℝ] ℝ}
  {s : Set Z} {t : Set E} {z : Z}

theorem source_pullback_within
    (hT : HasFDerivWithinAt T J s z)
    (hf : HasFDerivWithinAt f ell t (T z))
    (hmap : Set.MapsTo T s t)
    (hsource : Set.EqOn actual (f ∘ T) s)
    (hz : z ∈ s) :
    HasFDerivWithinAt actual (ell.comp J) s z :=
  (hf.comp z hT hmap).congr' hsource hz

theorem source_pullback_direction
    (hT : HasFDerivWithinAt T J s z)
    (hf : HasFDerivWithinAt f ell t (T z))
    (hmap : Set.MapsTo T s t)
    (hsource : Set.EqOn actual (f ∘ T) s)
    (hz : z ∈ s) (hu : UniqueDiffWithinAt ℝ s z) (w : Z) :
    (fderivWithin ℝ actual s z) w = ell (J w) := by
  have hd := source_pullback_within hT hf hmap hsource hz
  rw [hd.fderivWithin hu]
  rfl

#print axioms source_pullback_within
#print axioms source_pullback_direction
end RouteBChainRulePinned
```
<!-- END_FROZEN_ADAPTER -->

Required exports:

- `RouteBChainRulePinned.source_pullback_within`
- `RouteBChainRulePinned.source_pullback_direction`

The exact binder telescope is the frozen source's used section parameters
followed by each declaration's explicit arguments, with universes u/v retained.
A trusted reference challenge must freeze this telescope and conclusion
**independently of the candidate's elaborated type**. Do not generate the
challenge by querying the candidate and accepting that answer.

## 3. Contract invariants

Both declarations require real normed additive groups/spaces Z and E,
T:Z→E, f:E→Real, actual:Z→Real, J:Z→L[Real]E, ell:E→L[Real]Real,
s:Set Z, t:Set E, z:Z. They retain:

- hT: the actual supplied within-s derivative of T at z is J;
- hf: the supplied within-t derivative of f at **T z** is ell;
- hmap: **MapsTo T s t**, not point membership T z∈t;
- hsource: **EqOn actual (f∘T) s**, not only equality at z;
- hz: z∈s, to use congr'.

Only the direction declaration adds **UniqueDiffWithinAt Real s z** and w:Z.
Do not add uniqueness to the first declaration or demand it on t; do not
remove it from the second. No completeness, finite dimension, invertibility,
global differentiability or extra conclusion hypothesis is permitted.

Underlying within-set composition needs no z∈s or uniqueness itself; hz is
needed here to consume EqOn with congr'. A legitimately different local-germ
or Tendsto contract is possible, but would be a different reviewed contract.
Do not silently shrink s to s∩T⁻¹(t).

The output of the first theorem is a derivative relation, not a selected
fderivWithin value. The second uses the uniqueness premise to identify that
operator and then evaluates it at w. At a boundary this is not a claim that
every w is realizable by an admissible path.

## 4. Runner gates and comparator

The coordinator must approve a GitHub runner and trusted comparator before
dispatch. None is selected or launched here. Missing approved comparator
identity is **COMPARATOR_MISSING**, not a reason to fabricate success.

The authorized job should:

1. Check the packet/payload hashes and target pins before compilation. Use a
   clean isolated adapter package, verified resolved lock, recorded Lean binary
   identity and compiler-discovered import/object provenance. Obtain trusted
   dependencies without compiling the FLT tree.
2. Compile the frozen unit only (plus small isolated comparator/negative-control
   modules) with warnings treated as errors. Preserve native exit, stdout and
   stderr separately. Record any generated .olean/.ilean hashes as actual
   artifacts, never fill them from expected names.
3. Capture both fully elaborated declaration types and declaration-level
   `#print axioms` output. Require no sorryAx and no unapproved/custom axioms.
   Proposed upper allowance is the usual propext/Classical.choice/Quot.sound;
   report the actual set, which may be smaller, and obtain the coordinator's
   axiom-policy approval. A whitelist is not a fabricated observed axiom set.
4. Compare each candidate type against the separately frozen reference under
   the same pin. Require exact typed-contract identity (up to accepted
   alpha-renaming/definitional equality), not merely provability from a
   stronger assumption, a one-way implication, normalized text or a wrapper
   accepting the desired conclusion. Record the trusted comparator's policy.
5. Execute the controls in section 5; return every raw result, including
   failures. A source patch requires a new payload/hash/review, not silent
   in-place “repair”.

The live `src/percolation_workflow/comparator.py` was read, not executed or
modified. Its raw hash is
`b3e33aa73e9a606761e851156f5d0cdfb7e547b4febdc5d1a23598d20cc4aedb`.
`run_comparator` requires native exit 0 AND the exact standalone line
`Your solution is okay!` in stdout/stderr. That line is an output convention,
not an executable identity or proof: require a trusted, pinned tool/config and
actual runner linkage. `compare_statement` is only whitespace-normalized
text comparison, not a substitute. The pure receipt helper checks reported
acceptance/output but does not authenticate a process run; retain and check
the native comparator exit and runner provenance independently.

No concrete approved comparator executable/config was supplied for this unit.
Its repository/commit, executable hash, configuration hash and argv therefore
remain null until approved. A successful `#check` or a type-assignment probe
alone must not be labeled “comparator accepted”.

## 5. Focused negative controls, not yet executed

Run each control in isolation; never import a failing/mutant module into the
positive unit. Keep mutated source/reference hashes and logs distinct.

| ID / layer | Mutation | Required outcome and interpretation |
|---|---|---|
| NC-GOAL / comparator | Add an explicit hgoal equal to the conclusion of source_pullback_within, keep all original arguments, prove by exact hgoal | This is a deliberately easy-to-compile stronger-premise wrapper. Exact-contract comparator must reject; compiler success is not acceptance. |
| NC-EXTRA-UNIQUE / comparator | Add hu:UniqueDiffWithinAt Real s z to the first theorem, keep its original proof | Expected to compile, but comparator must reject the extra assumption. The original first theorem must still pass without hu. |
| NC-MAP / elaboration | Remove hmap from the first header, retain the original proof text | Expected failure specifically at the missing hmap reference. This checks frozen-telescope/proof plumbing only; it does not by itself prove MapsTo is mathematically necessary for all alternative rules. |
| NC-POINT / elaboration | Replace EqOn hsource by actual z=f(T z), retain the congr' proof | Expected type mismatch at congr'. One-point agreement is not germ agreement. It must never receive positive comparator status. |
| NC-NO-UNIQUE / elaboration | Remove hu from the direction theorem, retain the original proof | Expected missing-hu failure. Stronger mathematical warning: on singleton s many relative derivative operators exist; absence of hu cannot generally identify fderivWithin. |
| NC-EXIT / receipt boundary | In a separate in-memory receipt test report exit 1 together with the success line; also test exit 0 with only a prefixed/suffixed imitation line | Both must be rejected as comparator acceptance. Clearly label these as synthetic receipt tests, never actual compiler/comparator evidence. |
| NC-PIN / provenance | Compare an intentionally mismatched claimed Mathlib/payload hash against coordinator-owned expected values | Reject mismatch before admission; do not install another Mathlib version just to perform this negative control. |

NC-GOAL and NC-EXTRA-UNIQUE are the critical **compile-success negatives** that
prevent replacing exact contract comparison with mere compilation. If they
do not compile, return their diagnostic and classify the comparator-negative
test inconclusive, not passed. For NC-MAP/POINT/NO-UNIQUE, infrastructure/import
failures are inconclusive; only the specified local error is the expected
elaboration failure. An unexpected successful mutation needs review, not
silent acceptance. These tests have not been run in this task.

## 6. Required evidence envelope

This is a field specification for a future immutable runner report, **not**
an instance of the existing workflow's compiled-candidate receipt schema.
Do not submit it directly to validate_candidate_receipt or invent DAG bindings.
The coordinator may map real evidence into that schema later, separately.

| Field group | Required content |
|---|---|
| identity | task_id; contract_version; this handoff URI/raw SHA-256; parent review hash; payload filename/encoding/length/SHA-256; reference challenge declaration IDs/source SHA-256 |
| origin | Mathlib repository+commit; Comp/Congr/Basic paths+blob+raw hashes above; FLT reference marked context_only; attribution files |
| runner | provider=GitHub; repository and immutable checkout commit; workflow file+commit; run_id, attempt, job_id, run URL; timestamps; OS/architecture/container identity; actual Lean version+binary hash |
| environment | actual lean-toolchain bytes/hash; Mathlib rev/inputRev/HEAD; isolated lake-manifest bytes/hash; dependency lock entries; actual imported source/object manifest and its digest |
| compilation | argv array, working directory, native exit, stdout/stderr artifact paths+raw hashes, compiler flags, full exported types, actual object paths+hashes |
| axioms | per-declaration raw reports and parsed sets; approved policy hash; strict-admission tool/config hash and actual outcome, if available |
| comparator | approved repository/commit/tool+config hashes; argv; actual native exit; stdout/stderr paths+hashes; target-pin reference/candidate identities; per-declaration type comparison outcome |
| controls | for each NC: mutation identity+source/reference hash, test layer, argv/exit/logs, expected vs actual outcome, passed/failed/inconclusive; synthetic receipt controls explicitly tagged |
| conclusions | generic_compile_status; comparator_status; negative_control_status; source_instance_status=pending; registry_status=pending; registry_eligible=false; formal_certificate_allowed=false |
| integrity | artifact index with retrieval locations/raw hashes; canonical evidence-object digest excluding its digest field; raw JSON file SHA-256 stored externally in the enclosing review |

Use canonical evidence-object hashing only under a recorded deterministic
encoding: UTF-8, sorted object keys, compact JSON, array order retained, no NaN,
strict duplicate-key rejection. Distinguish that canonical object digest from
the raw file SHA-256; neither authenticates GitHub provenance by itself.

At handoff time: runner identity, approved comparator identity/config, reference
challenge artifact hash, compile exit/log/object evidence, axiom results,
negative-control outcomes and Route-B source-instance evidence are all
**null/not_run**. Only source/payload identity hashes are presently populated.
If a tool is unavailable, report missing; if a present artifact has wrong hash,
report rejected. Do not synthesize placeholders resembling successful evidence.

A complete generic build/comparator receipt can be a compiled_candidate, but
never directly registry-eligible. Missing coordinator-owned statement/DAG/axiom
bindings remain pending for workflow admission. This contract supplies no
authoritative DAG node or parent theorem binding.

## 7. Explicit non-goals

hsource must be independently proved about the actual source interpretation;
do not define actual=f∘T merely to fill it. hT/hf and hmap must refer to the
same functions, domains, inputs and source semantics. Finite binary64 value
agreement, a graph hash or samples do not establish real-neighborhood equality.

Nothing here constructs the actual derivative, graph regularity, physical
moving-frame/time terms, material-metric identity, finite-difference remainder,
runtime error bound, contraction certificate or whole-path/flowpipe coverage.
FLT map_comp remains an optional sibling after a separate derivative/Leibniz
instance; it cannot supply these premises. No Route-B source closure follows
from either positive theorem.

Concurrent edits to shared state/review queues/scripts were observed but left
untouched. This task's sole output is this immutable review/handoff.
