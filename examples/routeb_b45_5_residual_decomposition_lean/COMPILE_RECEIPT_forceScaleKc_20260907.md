# Fresh pinned compile/axiom receipt: `forceScaleKc_eq_rhoKc`

## Identity

- Candidate source: `ResidualDecomposition.lean`
- Source SHA-256: `3946389828B94AFF3B258A4635B58A7CA1BE6FF2CE4414E9BEF9553E25653CC9`
- Fresh compile run: `output/run-force-scale-20260907T071433603`
- OLean SHA-256: `C8CA784F9C9AECFD2DCAE0163157FEF9A969B18809E12184FF87449504486528`
- OLean size: `592128` bytes

## Pinned worker

- Lean: `4.33.1`
- Lean commit: `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`
- `warningAsError`: `true`
- Dependency mode: existing pinned Mathlib checkout/cache; no dependency download

## Compile and axiom result

- canonical `ResidualDecomposition.lean` compile exit: `0`
- fresh theorem-check exit: `0`
- `sorry/admit` source scan: `PASS`

The fresh theorem-check emitted:

```text
'RouteBB45ResidualDecomposition.rhoKc_exact' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBB45ResidualDecomposition.forceScaleKc_eq_rhoKc' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBB45ResidualDecomposition.rhoKc_sq_le_of_block_energy' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBB45ResidualDecomposition.residual_decomposition' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBB45ResidualDecomposition.residual_decomposition_with_explicit_kc' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Thus `forceScaleKc_eq_rhoKc` has no `sorryAx`, `admit`, or custom axiom in this
receipt; its transitive axiom set is the standard Lean logic set shown above.

## Comparator and physical boundary

- exact statement comparator: `NOT RUN / OPEN`
- source comparator binding: `OPEN`
- Float64-to-`ℝ` binding: `OPEN`
- registry promotion: `false`
- deployed `tau` equivalence: `NOT CLAIMED / OPEN`

The receipt certifies only the exact-real adapter identity

\[
  \operatorname{diag}(1/5,1/10)(q_5/20,q_4/20)
  =(q_5/100,q_4/200).
\]

It does not certify that deployed `dhport_lib.jl`'s `tau` contains or equals
this cross-force term, nor that the lifted descriptor rows equal the deployed
torque law. `forceScaleKc_eq_rhoKc` remains a compositional adapter child only.

## Scope note

`liftedKcForce_eq_rhoKc` is an optional review-level bridge and is not a
declaration in the canonical `ResidualDecomposition.lean` source covered by
this receipt. The receipt therefore makes no canonical-source claim for that
optional declaration. `rhoKc_sq_le_of_block_energy` is included above because
it is present in and compiled with the canonical sidecar; its energy hypothesis
remains an external domain obligation.

