# Anthropic FLT differentiable-coordinate adapter

Status: `pending`; direct-reuse API candidate, not registry-admitted.

## Selection and provenance

Selected theorem:

```text
Algebra.exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential
```

The exact upstream declaration is pinned to
`upstream/anthropics-fermats-last-theorem` commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, file
`Theorems/Thm_Algebra_exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential.lean`.
The source blob is `258acd99b2b98065e948b27f966c410b91c8a263`; the audited
imports include `Mathlib`, `P2M.Util`, and the matching `P2M.Sol` proof.
Repository attribution is Apache-2.0.

## Exact applicability

The theorem requires `[CommRing S]`, `[IsDomain S]`, `[Algebra ℂ S]`,
`[Algebra.FiniteType ℂ S]`, `Algebra.Smooth ℂ S`, the rank equation
`Module.rank S (KaehlerDifferential ℂ S) = n`, an evaluation hom
`σ₀ : S →ₐ[ℂ] ℂ`, a coordinate family `t : Fin n → S`, and the displayed
Kähler-differential generation condition. It concludes a positive-radius local
bijective evaluation-coordinate map, differentiable factorization for every
`s : S`, and finite-support neighborhood stability.

Classification is `direct_reuse` for the theorem shape, with a low-to-moderate
ambient adaptation risk: the finite-dimensional coordinate conclusion is
generic in shape, but the scalar field is `ℂ` and the hypotheses are genuinely
Kähler/algebraic.

## Boundary

The sidecar packages the audited conclusion shape only. It does not copy the
upstream FLT arithmetic proof, assert a local compilation receipt, or claim a
Route-B/PDE coordinate chart, interval enclosure, domain coverage, or flowpipe
theorem. A target adapter must separately discharge the ambient typeclass,
scalar/topology, source provenance, and any downstream admission gates.

No local registry/state was modified. The sidecar remains pending/open and no
wide regression was run.
