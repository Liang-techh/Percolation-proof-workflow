---
kind: review_result
review_id: review-T-P8-010-fengbujue-20260906T2318
task_id: T-P8-010
parent_task_id: T-P8-007
source_agent: 封不觉
created_at: 2026-09-06T23:18:00-06:00
integration_status: pending
admission_label: compiled_candidate
review_of: review-T-P8-007-choupizhu-20260906T2307
inspected_commit: 0723aea49d4051af7cb1c6e5848b1a1984e6bbdc
proposed_integration_target: theorem
requested_action: retain_as_compiled_candidate_only
---

# T-P8-010 — independent final-gate review of compiled ramp-tail sidecar

## Final gate decision

**Decision: `compiled_candidate` for the abstract ramp-tail calculus child only.**

This review independently accepts the kernel/compile status of the exact sidecar at commit
`0723aea49d4051af7cb1c6e5848b1a1984e6bbdc`. It does **not** promote P8, M4, source binding, reachability, flowpipe coverage, terminal comparator, or the verified registry.

The theorem statements correctly express the intended pure calculus seam under hypotheses that are stronger than the eventual interval-local parent needs: the derivative assumptions hold for every `t : ℝ`. This is a strengthening of assumptions, not a silent weakening of the theorem. The separate interval-local refinement remains `T-P8-009` and is not required to classify this exact artifact as a compiled candidate.

## Exact artifact identity and provenance

Passing source snapshot:

- repository commit / Actions `head_sha`: `0723aea49d4051af7cb1c6e5848b1a1984e6bbdc`
- Lean source: `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`
- Lean source Git blob: `0bcac8908b2492ae72279ef0cd05b2d6634bc3a9`
- verifier: `examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh`
- verifier Git blob: `89144cf54bcdc1d71db8230b9387103c5298b1cf`
- sidecar `lean-toolchain` Git blob: `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`
- sidecar toolchain content: `leanprover/lean4:v4.32.0`
- reused `examples/local_fkg/lean-toolchain` blob: `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`
- reused `examples/local_fkg/lake-manifest.json` blob: `09a7132a667a8b7fbf5f32ff781fd8c6e6b11bc9`
- pinned Mathlib revision in that manifest: `81a5d257c8e410db227a6665ed08f64fea08e997`
- workflow file at passing commit: `.github/workflows/lean-agent-sidecars.yml`
- workflow Git blob: `97f4ac81d789ef05788314a5760d1f3d5fb866cd`
- pinned upstream `anthropics/formal-math` commit used by workflow: `795efb86f191735c5481675763537cfb4ff37e55`

The submitted review's processed marker is:

- `agent_review_inbox/processed/review-T-P8-007-choupizhu-20260906T2307.json`
- marker Git blob: `93877e9a0aa363e6959ab9ef9c597bee503cf5e6`
- review SHA-256 recorded by marker: `962EF48F7109459795C09D25042ADC31DAB184D84D3063C0DE488217B730D69E`
- classification: `pending_ramp_sidecar_validation`
- admission effect: `none`

Important provenance note: the processed marker's `source_commit` is `21ec7b34033ba8a2a62c8831e4d20b59635d0ac0`, because the submitted review also mentioned a later unrelated main head. The actual compile evidence is unambiguously bound to GitHub Actions `head_sha = 0723aea49d4051af7cb1c6e5848b1a1984e6bbdc` and the exact blobs above. Therefore the marker's generic `source_commit` field must **not** be interpreted as the compile commit. Future integrator parsing should prefer an explicit `inspected_commit` / `compiled_commit` field over the first incidental 40-character SHA appearing in prose.

## Independently fetched GitHub Actions evidence

Workflow: `Lean agent sidecars`

- run_id: `34085393805`
- job_id: `101628339820`
- runner: `ubuntu-24.04`
- run conclusion: `success`
- job `portable-sidecars` conclusion: `success`
- checkout step: `success`
- pinned formal-math checkout: `success`
- checksum-verified Elan install: `success`
- pinned local-FKG Lake bootstrap: `success`
- `Run portable agent sidecars`: `success`

The decoded GitHub-hosted job log independently confirms:

```text
git checkout ... 0723aea49d4051af7cb1c6e5848b1a1984e6bbdc
LOCAL_FKG_TOOLCHAIN=leanprover/lean4:v4.32.0
Lake version 5.0.0-src+8c9756b (Lean version 4.32.0)
mathlib ... revision '81a5d257c8e410db227a6665ed08f64fea08e997'
```

For the exact P8 verifier, the same GitHub runner log records:

```text
Running examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
'RouteBP8RampReconstruction.ramp_c_constant' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.ramp_w_eq_mul' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.ramp_reconstruction' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.state_tail_reconstruction' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.state_terminal_one' depends on axioms: [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT=PASS
P8_RAMP_RECONSTRUCTION_FOCUSED_CHECK=PASS
PORTABLE_SIDECARS_RUN=2
```

GitHub job exit/conclusion is successful. No `sorryAx`, compile error, unknown module, or extra project-specific axiom appears in the five theorem reports.

The workflow also proves the CI is not a no-op: two earlier commits failed specifically in the `Run portable agent sidecars` step (runs `34085002837` / job `101627229462` and `34085159285` / job `101627671006`) before the final corrected commit passed.

## Statement and hypothesis audit

The compiled file proves exactly these semantic facts:

1. `ramp_c_constant`: `c 0 = c0` and `∀ t, HasDerivAt c 0 t` imply `∀ t, c t = c0`.
2. `ramp_w_eq_mul`: `w 0 = 0`, `∀ t, c t = c0`, and `∀ t, HasDerivAt w (c t) t` imply `∀ t, w t = c0 * t`.
3. `ramp_reconstruction`: combines the two facts.
4. `state_tail_reconstruction`: instantiates them on typed slots of `State14 := Fin 14 → ℝ`, with `wSlot = 12` and `cSlot = 13`.
5. `state_terminal_one`: derives `z 1 wSlot = c0`.

These statements genuinely encode the ramp-tail semantics requested by `T-P8-006`; they are not tautological range/equality wrappers. The hypotheses are sufficient. They are deliberately stronger than an interval-local `[0,1]` theorem because they require derivatives for every real time. The file comments disclose this boundary explicitly.

## Counterexample / semantic-risk audit

No counterexample exists to the stated abstract theorem under its hypotheses. The main semantic risk is over-promotion: the theorem says nothing about whether a deployed trajectory actually satisfies those derivative hypotheses.

In particular, this candidate does **not** establish:

- deployed Julia/DH first-12 RHS semantic equality;
- equality of the deployed 13th derivative with the ramp tail (which is known to be the wrong full-13 binding for nonzero `c0`);
- existence or uniqueness of the relevant ODE solution;
- outward interval containment or first-exit closure;
- continuation/full `[0,1]` domain coverage;
- flowpipe/reachability certification;
- source receipt freshness for the physical model;
- P8 parent completion or M4 completion.

The mathematical review correctly requires first-12 source binding to remain separate from adapter-supplied tail equations.

## Admission boundary

### Gates passed for this exact sidecar

- theorem statement semantic audit: **PASS**
- hypotheses sufficient for stated theorem: **PASS**
- portable verifier registered with `CI_PORTABLE=1`: **PASS**
- pinned toolchain identity: **PASS**
- GitHub-hosted focused compile/kernel execution: **PASS**
- `#print axioms` audit on all five exported theorems: **PASS**
- no `sorryAx`: **PASS**
- source/blob identity for compiled commit: **PASS**

### Gates not supplied by this artifact

- physical/source binding: **OPEN**
- current physical receipt/fresh provenance for P8 source: **OPEN / separate lane**
- ODE existence and regularity for deployed trajectory: **OPEN**
- `[0,1]` coverage / continuation / flowpipe: **OPEN**
- parent dependency closure: **OPEN**
- registry admission: **NOT ELIGIBLE**

## Directed follow-up

- **苏梦辰 / `T-P8-009`**: if the parent requires the weaker interval-local/end-point formulation, prove it as a separate child and bind the parent hypotheses to it. Do not rewrite this already compiled artifact.
- **P8 mathematical/source-binding lane (`T-P8-008` and successors)**: prove the first-12 deployed source semantic bridge and later existence/coverage obligations. Keep the ramp tail adapter separate.
- **梁智炜**: retain this result as `compiled_candidate` metadata only. No P8/M4 node or registry promotion follows yet.

No rework is required from 臭屁猪 for the exact compiled version `0723aea49d4051af7cb1c6e5848b1a1984e6bbdc`.

## Final verdict

`T-P8-007` / commit `0723aea49d4051af7cb1c6e5848b1a1984e6bbdc` is independently validated as a **`compiled_candidate`** for the abstract ramp-tail calculus theorem set.

**Promotion beyond compiled-candidate status is rejected at this stage because source binding, trajectory existence, domain coverage, flowpipe and parent dependencies remain open.**
