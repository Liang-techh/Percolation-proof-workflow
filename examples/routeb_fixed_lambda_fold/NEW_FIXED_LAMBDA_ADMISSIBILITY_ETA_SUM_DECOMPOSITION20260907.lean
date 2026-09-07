import NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_TOTAL_ABSORPTION20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaEtaSumDecomposition

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget
open RouteBFixedLambdaWeightedAbsorption

noncomputable section

/-!
This sidecar handles only the additive eta-partition seam.  The tagged row
sets are supplied as finite subcollections of the existing union, together
with explicit finite cover/disjointness and sum-partition premises.  No
physical-domain or source coverage statement is encoded.
-/

structure ExplicitEtaSumPartition
    (f : Declared577SparseFold) where
  eta27Rows : Finset (EtaTag × Nat)
  eta56Rows : Finset (EtaTag × Nat)
  cover : unionRows f = eta27Rows ∪ eta56Rows
  disjoint : Disjoint eta27Rows eta56Rows
  sum_partition :
    ∀ g : (EtaTag × Nat) → ℚ,
      (∑ x in unionRows f, g x) =
        (∑ x in eta27Rows, g x) + (∑ x in eta56Rows, g x)

def eta27WeightedLoadTotal
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in p.eta27Rows, coeff x * load x

def eta56WeightedLoadTotal
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in p.eta56Rows, coeff x * load x

def eta27WeightedMarginTotal
    {f : Declared577SparseFold} {lambda : ℚ}
    (p : ExplicitEtaSumPartition f)
    (coeff : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in p.eta27Rows,
    coeff x * marginAt lambda (unionRow f x)

def eta56WeightedMarginTotal
    {f : Declared577SparseFold} {lambda : ℚ}
    (p : ExplicitEtaSumPartition f)
    (coeff : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in p.eta56Rows,
    coeff x * marginAt lambda (unionRow f x)

theorem eta27_mem_union
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    {x : EtaTag × Nat} (hx : x ∈ p.eta27Rows) :
    x ∈ unionRows f := by
  rw [p.cover]
  exact Finset.mem_union.mpr (Or.inl hx)

theorem eta56_mem_union
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    {x : EtaTag × Nat} (hx : x ∈ p.eta56Rows) :
    x ∈ unionRows f := by
  rw [p.cover]
  exact Finset.mem_union.mpr (Or.inr hx)

theorem weighted_load_union_eq_eta_sum
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ) :
    weightedLoadTotal coeff load =
      eta27WeightedLoadTotal p coeff load +
        eta56WeightedLoadTotal p coeff load := by
  exact p.sum_partition (fun x => coeff x * load x)

theorem weighted_margin_union_eq_eta_sum
    {f : Declared577SparseFold} {lambda : ℚ}
    (p : ExplicitEtaSumPartition f)
    (coeff : (EtaTag × Nat) → ℚ) :
    weightedMarginTotal coeff =
      eta27WeightedMarginTotal p coeff +
        eta56WeightedMarginTotal p coeff := by
  exact p.sum_partition
    (fun x => coeff x * marginAt lambda (unionRow f x))

theorem eta27_weighted_load_nonnegative
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : ∀ x ∈ p.eta27Rows, 0 ≤ coeff x)
    (hload : ∀ x ∈ p.eta27Rows, 0 ≤ load x) :
    0 ≤ eta27WeightedLoadTotal p coeff load := by
  unfold eta27WeightedLoadTotal
  apply Finset.sum_nonneg
  intro x hx
  exact mul_nonneg (hcoeff x hx) (hload x hx)

theorem eta56_weighted_load_nonnegative
    {f : Declared577SparseFold}
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : ∀ x ∈ p.eta56Rows, 0 ≤ coeff x)
    (hload : ∀ x ∈ p.eta56Rows, 0 ≤ load x) :
    0 ≤ eta56WeightedLoadTotal p coeff load := by
  unfold eta56WeightedLoadTotal
  apply Finset.sum_nonneg
  intro x hx
  exact mul_nonneg (hcoeff x hx) (hload x hx)

theorem eta27_weighted_load_le_eta_delta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load) :
    eta27WeightedLoadTotal p coeff load ≤
      ∑ x in p.eta27Rows, coeff x * b.delta := by
  unfold eta27WeightedLoadTotal
  apply Finset.sum_le_sum
  intro x hx
  exact weighted_load_term_le_delta_term b coeff load hcoeff hload x
    (eta27_mem_union p hx)

theorem eta56_weighted_load_le_eta_delta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load) :
    eta56WeightedLoadTotal p coeff load ≤
      ∑ x in p.eta56Rows, coeff x * b.delta := by
  unfold eta56WeightedLoadTotal
  apply Finset.sum_le_sum
  intro x hx
  exact weighted_load_term_le_delta_term b coeff load hcoeff hload x
    (eta56_mem_union p hx)

theorem eta27_weighted_delta_le_eta_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff) :
    (∑ x in p.eta27Rows, coeff x * b.delta) ≤
      eta27WeightedMarginTotal p coeff := by
  unfold eta27WeightedMarginTotal
  apply Finset.sum_le_sum
  intro x hx
  exact weighted_delta_term_le_margin_term b coeff hcoeff x
    (eta27_mem_union p hx)

theorem eta56_weighted_delta_le_eta_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff) :
    (∑ x in p.eta56Rows, coeff x * b.delta) ≤
      eta56WeightedMarginTotal p coeff := by
  unfold eta56WeightedMarginTotal
  apply Finset.sum_le_sum
  intro x hx
  exact weighted_delta_term_le_margin_term b coeff hcoeff x
    (eta56_mem_union p hx)

/- Admission boundary: these are finite additive decompositions over supplied
   tagged subsets.  No source, receipt, digest, or physical-domain coverage
   claim is introduced. -/

#print axioms weighted_load_union_eq_eta_sum
#print axioms weighted_margin_union_eq_eta_sum
#print axioms eta27_weighted_load_nonnegative
#print axioms eta56_weighted_load_nonnegative
#print axioms eta27_weighted_load_le_eta_delta
#print axioms eta56_weighted_load_le_eta_delta
#print axioms eta27_weighted_delta_le_eta_margin
#print axioms eta56_weighted_delta_le_eta_margin

end
end RouteBFixedLambdaEtaSumDecomposition
