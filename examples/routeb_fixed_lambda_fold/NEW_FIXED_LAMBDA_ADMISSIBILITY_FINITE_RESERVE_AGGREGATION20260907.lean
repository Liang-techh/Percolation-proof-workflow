import NEW_FIXED_LAMBDA_ADMISSIBILITY_NO_DIVISION_RATIO20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaFiniteReserveAggregation

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaNoDivisionRatio

noncomputable section

/-!
This sidecar aggregates cross-multiplied reserves over a finite family of
declared cells.  `support` and `disjoint_supports` make the intended disjoint
cell premise explicit, but no union-completeness or physical-domain claim is
attached to that premise.
-/

structure FiniteDisjointCellFamily where
  rows : Finset Nat
  cell : Nat → CellMarginData ℚ
  support : Nat → Finset Nat
  disjoint_supports :
    ∀ {i j : Nat}, i ∈ rows → j ∈ rows → i ≠ j →
      Disjoint (support i) (support j)

def totalReserve
    (f : FiniteDisjointCellFamily)
    (reserve : Nat → ℚ) : ℚ :=
  ∑ i in f.rows, reserve i

def totalMargin
    (f : FiniteDisjointCellFamily)
    (lambda : ℚ) : ℚ :=
  ∑ i in f.rows, marginAt lambda (f.cell i)

def totalExternal
    (f : FiniteDisjointCellFamily) : ℚ :=
  ∑ i in f.rows, (f.cell i).externalGamma

def totalCellCharge
    (f : FiniteDisjointCellFamily) : ℚ :=
  ∑ i in f.rows, (f.cell i).cellGamma

theorem total_margin_additive
    (f : FiniteDisjointCellFamily) (lambda : ℚ) :
    totalMargin f lambda =
      totalExternal f - lambda * totalCellCharge f := by
  unfold totalMargin totalExternal totalCellCharge marginAt
  rw [Finset.sum_sub_distrib]
  rw [← Finset.mul_sum]

/-!
Each row keeps its own positive denominator through `CellMarginData`.  The
reserve hypothesis is cross-multiplied, so the aggregation theorem never
divides by a cell coefficient.
-/
theorem total_reserve_le_total_margin
    (f : FiniteDisjointCellFamily)
    (lambda : ℚ)
    (reserve : Nat → ℚ)
    (hreserve : ∀ i ∈ f.rows,
      lambda * (f.cell i).cellGamma + reserve i ≤
        (f.cell i).externalGamma) :
    totalReserve f reserve ≤ totalMargin f lambda := by
  unfold totalReserve totalMargin
  apply Finset.sum_le_sum
  intro i hi
  exact cross_multiplied_reserve_implies_margin_lower_bound
    (f.cell i) (hreserve i hi)

theorem total_reserve_le_external_minus_total_charge
    (f : FiniteDisjointCellFamily)
    (lambda : ℚ)
    (reserve : Nat → ℚ)
    (hreserve : ∀ i ∈ f.rows,
      lambda * (f.cell i).cellGamma + reserve i ≤
        (f.cell i).externalGamma) :
    totalReserve f reserve ≤
      totalExternal f - lambda * totalCellCharge f := by
  rw [← total_margin_additive f lambda]
  exact total_reserve_le_total_margin f lambda reserve hreserve

/-!
The disjointness premise is preserved as a projection for downstream cell
partition consumers; it is not silently upgraded into a coverage theorem.
-/
theorem disjoint_supports_remain_available
    (f : FiniteDisjointCellFamily) :
    ∀ {i j : Nat}, i ∈ f.rows → j ∈ f.rows → i ≠ j →
      Disjoint (f.support i) (f.support j) := by
  exact f.disjoint_supports

/- Admission boundary: these are finite additive consequences of explicit
   per-cell reserve and denominator premises only. -/

#print axioms total_margin_additive
#print axioms total_reserve_le_total_margin
#print axioms total_reserve_le_external_minus_total_charge
#print axioms disjoint_supports_remain_available

end
end RouteBFixedLambdaFiniteReserveAggregation
