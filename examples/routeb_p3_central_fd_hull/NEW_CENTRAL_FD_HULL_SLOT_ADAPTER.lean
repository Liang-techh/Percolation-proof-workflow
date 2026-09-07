import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Typed dM-slot adapter for the P3 central-FD hull

The source-shaped tensor stores `dM[i,j,k]`: mass row, mass column, then
differentiated coordinate.  The existing Christoffel consumer stores
`T[k,i,j]`: differentiated coordinate first, then the two mass slots.  This
file makes that permutation explicit and proves the corresponding remainder
and radius transport.  It is exact-real and source-independent.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullSlotAdapter

noncomputable section

variable {ι : Type*} [Fintype ι]

abbrev DMTensor (ι : Type*) := ι → ι → ι → ℝ
abbrev DerivativeTensor (ι : Type*) := ι → ι → ι → ℝ

/-- Source/storage order: `dM i j k`. -/
def dmToDerivative (dM : DMTensor ι) : DerivativeTensor ι :=
  fun k i j => dM i j k

/-- Inverse map back to source/storage order. -/
def derivativeToDM (T : DerivativeTensor ι) : DMTensor ι :=
  fun i j k => T k i j

theorem derivativeToDM_dmToDerivative (dM : DMTensor ι) :
    derivativeToDM (dmToDerivative dM) = dM := by
  funext i j k
  rfl

theorem dmToDerivative_derivativeToDM (T : DerivativeTensor ι) :
    dmToDerivative (derivativeToDM T) = T := by
  funext k i j
  rfl

/-- The source-shaped radius receives the same slot permutation. -/
def dmRadiusToDerivative (mu : DMTensor ι) : DerivativeTensor ι :=
  fun k i j => mu i j k

theorem dm_radius_transport
    (R mu : DMTensor ι)
    (hR : ∀ i j k, |R i j k| ≤ mu i j k) :
    ∀ k i j,
      |dmToDerivative R k i j| ≤ dmRadiusToDerivative mu k i j := by
  intro k i j
  exact hR i j k

/-- Consumer-shaped Christoffel force, with derivative coordinate first. -/
def consumerForce
    (T : DerivativeTensor ι) (v : ι → ℝ) (i : ι) : ℝ :=
  ∑ j, ∑ k,
    ((T k i j + T j i k - T i j k) / 2) * v j * v k

/-- Source-shaped spelling of the same nested contraction. -/
def sourceDMForce
    (dM : DMTensor ι) (v : ι → ℝ) (i : ι) : ℝ :=
  ∑ j, ∑ k,
    ((dM i j k + dM i k j - dM j k i) / 2) * v j * v k

/-- Exact bridge from source `dM[i,j,k]` to consumer `T[k,i,j]`. -/
theorem sourceDMForce_eq_consumerForce
    (dM : DMTensor ι) (v : ι → ℝ) (i : ι) :
    sourceDMForce dM v i = consumerForce (dmToDerivative dM) v i := by
  rfl

/-- The permutation commutes with pointwise tensor addition. -/
theorem dmToDerivative_add
    (A B : DMTensor ι) :
    dmToDerivative (fun i j k => A i j k + B i j k) =
      fun k i j => dmToDerivative A k i j + dmToDerivative B k i j := by
  funext k i j
  rfl

/-- The exact-real FD remainder keeps its source slots while the consumer sees
the corresponding derivative-first tensor. -/
def dmRemainder (dMfd dMan : DMTensor ι) : DMTensor ι :=
  fun i j k => dMfd i j k - dMan i j k

def derivativeRemainder
    (dMfd dMan : DMTensor ι) : DerivativeTensor ι :=
  dmToDerivative (dmRemainder dMfd dMan)

theorem derivativeRemainder_apply
    (dMfd dMan : DMTensor ι) (k i j : ι) :
    derivativeRemainder dMfd dMan k i j =
      dmToDerivative dMfd k i j - dmToDerivative dMan k i j := by
  rfl

theorem derivativeRemainder_radius
    (dMfd dMan mu : DMTensor ι)
    (hR : ∀ i j k, |dMfd i j k - dMan i j k| ≤ mu i j k) :
    ∀ k i j,
      |derivativeRemainder dMfd dMan k i j| ≤
        dmRadiusToDerivative mu k i j := by
  intro k i j
  exact hR i j k

/-- A source-shaped Christoffel remainder can be consumed without an implicit
slot rewrite: the mapped source force difference is the consumer force of the
mapped derivative remainder. -/
theorem sourceDMForce_remainder_bridge
    (dMtrue dMfd : DMTensor ι) (v : ι → ℝ) (i : ι) :
    sourceDMForce dMfd v i - sourceDMForce dMtrue v i =
      consumerForce (derivativeRemainder dMfd dMtrue) v i := by
  unfold sourceDMForce consumerForce derivativeRemainder dmRemainder
    dmToDerivative
  simp only [Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro j hj
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-! The following bridge is the exact interface expected by a consumer that
already has a derivative-first tensor remainder bound. -/

theorem mapped_remainder_is_derivative_first
    (dMfd dMtrue mu : DMTensor ι)
    (hR : ∀ i j k, |dMfd i j k - dMtrue i j k| ≤ mu i j k) :
    (∀ k i j,
      |derivativeRemainder dMfd dMtrue k i j| ≤
        dmRadiusToDerivative mu k i j) :=
  derivativeRemainder_radius dMfd dMtrue mu hR

end

end RouteBP3CentralFDHullSlotAdapter

#print axioms RouteBP3CentralFDHullSlotAdapter.derivativeToDM_dmToDerivative
#print axioms RouteBP3CentralFDHullSlotAdapter.dmToDerivative_derivativeToDM
#print axioms RouteBP3CentralFDHullSlotAdapter.sourceDMForce_eq_consumerForce
#print axioms RouteBP3CentralFDHullSlotAdapter.sourceDMForce_remainder_bridge
#print axioms RouteBP3CentralFDHullSlotAdapter.derivativeRemainder_radius
