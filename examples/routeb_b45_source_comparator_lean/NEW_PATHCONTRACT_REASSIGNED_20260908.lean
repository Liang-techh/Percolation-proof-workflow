import RouteBO1Body6CanonicalExportTargets

set_option autoImplicit false

namespace Body6PathContractReassigned

noncomputable section

open RouteBO1PerBodyExactSource RouteBO1Body6CanonicalExportTargets

/-!
OPEN_UNCOMPILED / theorem decomposition only. No source/compile receipt.
Human body 6 and column 6 are both represented by Fin 6 value 5.
Canonical rows encode values, not reversible raw provenance labels.
-/

structure SixthColumnPathContract {X Physical : Type*}
    (embed : X → Physical) (qOf : Physical → Q6)
    (domain : ℝ → Set X) (Omega : Set Q6) (path : ℝ → X)
    (rows : List CanonicalRow)
    (physicalRow : ℝ → Physical → Fin 6 → ℝ) (cap : ℝ → Fin 6 → ℝ) : Prop where
  projection : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x ∈ domain t,
    qOf (embed x) ∈ Omega
  inclusion : ∀ t ∈ Set.Icc (0 : ℝ) 1, path t ∈ domain t
  physicalIdentity : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x ∈ domain t, ∀ i : Fin 6,
    physicalRow t (embed x) i = sourceBodyMass (qOf (embed x)) (5 : Fin 6) i 5
  sourceIdentity : ∀ q ∈ Omega, ∀ i : Fin 6,
    sourceBodyMass q (5 : Fin 6) i 5 = body6CanonicalEvaluator rows q i 5
  canonicalCap : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ i : Fin 6,
    |body6CanonicalEvaluator rows (qOf (embed (path t))) i 5| ≤ cap t i

theorem physical_eq_canonical_on_path {X Physical : Type*}
    (embed : X → Physical) (qOf : Physical → Q6)
    (domain : ℝ → Set X) (Omega : Set Q6) (path : ℝ → X)
    (rows : List CanonicalRow)
    (physicalRow : ℝ → Physical → Fin 6 → ℝ) (cap : ℝ → Fin 6 → ℝ)
    (h : SixthColumnPathContract embed qOf domain Omega path rows physicalRow cap) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ i : Fin 6,
      physicalRow t (embed (path t)) i =
        body6CanonicalEvaluator rows (qOf (embed (path t))) i 5 := by
  intro t ht i
  exact (h.physicalIdentity t ht (path t) (h.inclusion t ht) i).trans
    (h.sourceIdentity _ (h.projection t ht (path t) (h.inclusion t ht)) i)

theorem transport_physical_row_cap {X Physical : Type*}
    (embed : X → Physical) (qOf : Physical → Q6)
    (domain : ℝ → Set X) (Omega : Set Q6) (path : ℝ → X)
    (rows : List CanonicalRow)
    (physicalRow : ℝ → Physical → Fin 6 → ℝ) (cap : ℝ → Fin 6 → ℝ)
    (h : SixthColumnPathContract embed qOf domain Omega path rows physicalRow cap) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ i : Fin 6,
      |physicalRow t (embed (path t)) i| ≤ cap t i := by
  intro t ht i
  rw [physical_eq_canonical_on_path embed qOf domain Omega path rows physicalRow cap h t ht i]
  exact h.canonicalCap t ht i

end
end Body6PathContractReassigned
