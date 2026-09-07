import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Route-B P5 coordinate-aware residual transport sidecar

This file formalizes the finite-sum algebra from
`review-T-P5-022-liuguanyi-20260907T0820.md`.

The upstream mathematical review separates the source/calculus layer from the
consumer layer.  This sidecar starts *after* a source checker has produced:

* component displacement bounds from consumer coordinates to source coordinates;
* component increment/Jacobian bounds for a raw residual;
* a typed raw-force to consumer-force absolute coefficient table.

It proves that those component bounds compose into the Frobenius-style squared
centered gain consumed by P5, and that raw anchor component boxes compose into a
squared force-anchor budget.  No Julia/Float64 derivative semantics, ODE/P8
coverage, source hash, or registry/admission claim is made here.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5CoordinateTransport

noncomputable section

/-- Entrywise transport coefficient
`K[a,k] = sum_i sum_j Aabs[a,i] * H[i,j] * S[j,k]`. -/
def transportedK {p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin m → Fin n → ℝ)
    (S : Fin n → Fin k → ℝ)
    (a : Fin p) (r : Fin k) : ℝ :=
  ∑ i, ∑ j, Aabs a i * (H i j * S j r)

/-- Frobenius-style squared centered-gain budget. -/
def transportEll2 {p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin m → Fin n → ℝ)
    (S : Fin n → Fin k → ℝ) : ℝ :=
  ∑ a, ∑ r, transportedK Aabs H S a r ^ 2

/-- One row of the anchor-box force transport. -/
def anchorRow {p m : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (c : Fin m → ℝ)
    (a : Fin p) : ℝ :=
  ∑ i, Aabs a i * c i

/-- Squared force-anchor budget obtained from component boxes. -/
def anchorB2 {p m : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (c : Fin m → ℝ) : ℝ :=
  ∑ a, anchorRow Aabs c a ^ 2

/-- Explicit finite-sum force map.  In the source adapter `A` may be the raw
PMI-to-generalized-force map, or the identity if the upstream residual is
already expressed in generalized-force coordinates. -/
def forceMap {p m : ℕ}
    (A : Fin p → Fin m → ℝ)
    (x : Fin m → ℝ)
    (a : Fin p) : ℝ :=
  ∑ i, A a i * x i

/-- Nonnegative source/checker coefficient tables produce nonnegative
transport coefficients.  This is useful as a typed checker sanity lemma; the
main finite-sum implication below only needs the already-proved component
bounds. -/
theorem transportedK_nonneg {p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin m → Fin n → ℝ)
    (S : Fin n → Fin k → ℝ)
    (hA : ∀ a i, 0 ≤ Aabs a i)
    (hH : ∀ i j, 0 ≤ H i j)
    (hS : ∀ j r, 0 ≤ S j r) :
    ∀ a r, 0 ≤ transportedK Aabs H S a r := by
  intro a r
  apply Finset.sum_nonneg
  intro i hi
  apply Finset.sum_nonneg
  intro j hj
  exact mul_nonneg (hA a i) (mul_nonneg (hH i j) (hS j r))

/-- Pure distributive/reindexing identity behind the coordinate transport. -/
theorem transport_expansion {p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin m → Fin n → ℝ)
    (S : Fin n → Fin k → ℝ)
    (dz : Fin k → ℝ)
    (a : Fin p) :
    (∑ i, Aabs a i * (∑ j, H i j * (∑ r, S j r * |dz r|))) =
      ∑ r, transportedK Aabs H S a r * |dz r| := by
  calc
    (∑ i, Aabs a i * (∑ j, H i j * (∑ r, S j r * |dz r|))) =
        ∑ i, ∑ j, ∑ r,
          Aabs a i * (H i j * (S j r * |dz r|)) := by
            simp_rw [Finset.mul_sum]
    _ = ∑ i, ∑ r, ∑ j,
          Aabs a i * (H i j * (S j r * |dz r|)) := by
            apply Finset.sum_congr rfl
            intro i hi
            exact Finset.sum_comm
    _ = ∑ r, ∑ i, ∑ j,
          Aabs a i * (H i j * (S j r * |dz r|)) := by
            exact Finset.sum_comm
    _ = ∑ r, transportedK Aabs H S a r * |dz r| := by
      apply Finset.sum_congr rfl
      intro r hr
      simp [transportedK, Finset.sum_mul, mul_assoc]

/-- Component-wise source-state, residual-increment, and force-coordinate
bounds compose into the transported row bound.  `Aabs` is intended to be
`|A|` entrywise, so its nonnegativity is explicit. -/
theorem component_transport {p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin m → Fin n → ℝ)
    (S : Fin n → Fin k → ℝ)
    (dxi : Fin n → ℝ)
    (dz : Fin k → ℝ)
    (de : Fin m → ℝ)
    (rc : Fin p → ℝ)
    (hA : ∀ a i, 0 ≤ Aabs a i)
    (hH : ∀ i j, 0 ≤ H i j)
    (hState : ∀ j, |dxi j| ≤ ∑ r, S j r * |dz r|)
    (hJac : ∀ i, |de i| ≤ ∑ j, H i j * |dxi j|)
    (hForce : ∀ a, |rc a| ≤ ∑ i, Aabs a i * |de i|) :
    ∀ a, |rc a| ≤ ∑ r, transportedK Aabs H S a r * |dz r| := by
  intro a
  calc
    |rc a| ≤ ∑ i, Aabs a i * |de i| := hForce a
    _ ≤ ∑ i, Aabs a i * (∑ j, H i j * |dxi j|) := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left (hJac i) (hA a i)
    _ ≤ ∑ i, Aabs a i * (∑ j, H i j * (∑ r, S j r * |dz r|)) := by
      apply Finset.sum_le_sum
      intro i hi
      apply mul_le_mul_of_nonneg_left
      · apply Finset.sum_le_sum
        intro j hj
        exact mul_le_mul_of_nonneg_left (hState j) (hH i j)
      · exact hA a i
    _ = ∑ r, transportedK Aabs H S a r * |dz r| :=
      transport_expansion Aabs H S dz a

/-- Row-wise Cauchy converts component bounds into a Frobenius squared-gain
consumer.  No square root or operator norm is needed. -/
theorem frobenius_centered_gain {p k : ℕ}
    (K : Fin p → Fin k → ℝ)
    (rc : Fin p → ℝ)
    (dz : Fin k → ℝ)
    (hcomp : ∀ a, |rc a| ≤ ∑ r, K a r * |dz r|) :
    (∑ a, rc a ^ 2) ≤
      (∑ a, ∑ r, K a r ^ 2) * (∑ r, dz r ^ 2) := by
  have hrow : ∀ a,
      rc a ^ 2 ≤ (∑ r, K a r ^ 2) * (∑ r, dz r ^ 2) := by
    intro a
    have hsumNonneg : 0 ≤ ∑ r, K a r * |dz r| :=
      le_trans (abs_nonneg (rc a)) (hcomp a)
    have hsquare :
        rc a ^ 2 ≤ (∑ r, K a r * |dz r|) ^ 2 := by
      rw [sq_le_sq]
      simpa [abs_of_nonneg hsumNonneg] using hcomp a
    have hcauchy :=
      Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (K a) (fun r => |dz r|)
    have hcauchy' :
        (∑ r, K a r * |dz r|) ^ 2 ≤
          (∑ r, K a r ^ 2) * (∑ r, dz r ^ 2) := by
      simpa [sq_abs] using hcauchy
    exact hsquare.trans hcauchy'
  calc
    (∑ a, rc a ^ 2) ≤
        ∑ a, ((∑ r, K a r ^ 2) * (∑ r, dz r ^ 2)) := by
      exact Finset.sum_le_sum fun a ha => hrow a
    _ = (∑ a, ∑ r, K a r ^ 2) * (∑ r, dz r ^ 2) := by
      rw [Finset.sum_mul]

/-- Main source-independent `T-P5-022` centered-gain theorem.  It consumes only
component contracts; the derivative/FTOC step that creates `hJac` remains a
separate source/calculus obligation. -/
theorem transported_jacobian_centered_gain {p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin m → Fin n → ℝ)
    (S : Fin n → Fin k → ℝ)
    (dxi : Fin n → ℝ)
    (dz : Fin k → ℝ)
    (de : Fin m → ℝ)
    (rc : Fin p → ℝ)
    (hA : ∀ a i, 0 ≤ Aabs a i)
    (hH : ∀ i j, 0 ≤ H i j)
    (hState : ∀ j, |dxi j| ≤ ∑ r, S j r * |dz r|)
    (hJac : ∀ i, |de i| ≤ ∑ j, H i j * |dxi j|)
    (hForce : ∀ a, |rc a| ≤ ∑ i, Aabs a i * |de i|) :
    (∑ a, rc a ^ 2) ≤
      transportEll2 Aabs H S * (∑ r, dz r ^ 2) := by
  have hcomp := component_transport Aabs H S dxi dz de rc hA hH hState hJac hForce
  simpa [transportEll2] using
    (frobenius_centered_gain (fun a r => transportedK Aabs H S a r) rc dz hcomp)

/-- Triangle inequality for the explicit finite-sum force map. -/
theorem forceMap_abs_le {p m : ℕ}
    (A : Fin p → Fin m → ℝ)
    (x : Fin m → ℝ)
    (a : Fin p) :
    |forceMap A x a| ≤ ∑ i, |A a i| * |x i| := by
  have h := Finset.abs_sum_le_sum_abs (fun i : Fin m => A a i * x i) Finset.univ
  simpa [forceMap, abs_mul] using h

/-- Raw anchor component boxes transported through an arbitrary finite force
map produce the squared `B2` budget.  The right-hand row is automatically
nonnegative because it upper-bounds an absolute value, so no redundant sign
hypothesis on `c` is required. -/
theorem force_map_anchor_box_to_B2 {p m : ℕ}
    (A : Fin p → Fin m → ℝ)
    (braw : Fin m → ℝ)
    (c : Fin m → ℝ)
    (hbox : ∀ i, |braw i| ≤ c i) :
    (∑ a, forceMap A braw a ^ 2) ≤
      anchorB2 (fun a i => |A a i|) c := by
  have hcomp : ∀ a,
      |forceMap A braw a| ≤ anchorRow (fun a i => |A a i|) c a := by
    intro a
    calc
      |forceMap A braw a| ≤ ∑ i, |A a i| * |braw i| := forceMap_abs_le A braw a
      _ ≤ ∑ i, |A a i| * c i := by
        apply Finset.sum_le_sum
        intro i hi
        exact mul_le_mul_of_nonneg_left (hbox i) (abs_nonneg (A a i))
      _ = anchorRow (fun a i => |A a i|) c a := rfl
  have hrow : ∀ a,
      forceMap A braw a ^ 2 ≤
        anchorRow (fun a i => |A a i|) c a ^ 2 := by
    intro a
    have hnonneg : 0 ≤ anchorRow (fun a i => |A a i|) c a :=
      le_trans (abs_nonneg (forceMap A braw a)) (hcomp a)
    rw [sq_le_sq]
    simpa [abs_of_nonneg hnonneg] using hcomp a
  simpa [anchorB2] using (Finset.sum_le_sum fun a ha => hrow a)

/-- Exact channel-4 raw-PMI force scaling: applying `1/5` to a squared raw
component charges exactly `1/25` of its square. -/
theorem raw_pmi_channel4_square_scale (x : ℝ) :
    (x / 5) ^ 2 = x ^ 2 / 25 := by
  ring

/-- Exact channel-5 raw-PMI force scaling: applying `1/10` to a squared raw
component charges exactly `1/100` of its square. -/
theorem raw_pmi_channel5_square_scale (x : ℝ) :
    (x / 10) ^ 2 = x ^ 2 / 100 := by
  ring

/-- A second accidental application of the channel-4 normalization divides the
already-generalized squared quantity by another factor `25`.  This theorem is a
typed arithmetic warning against double normalization, not a source claim. -/
theorem channel4_double_normalization_factor (x : ℝ) :
    ((x / 5) / 5) ^ 2 = (x / 5) ^ 2 / 25 := by
  ring

/-- The analogous accidental second channel-5 normalization divides the
already-generalized squared quantity by another factor `100`. -/
theorem channel5_double_normalization_factor (x : ℝ) :
    ((x / 10) / 10) ^ 2 = (x / 10) ^ 2 / 100 := by
  ring

#print axioms transportedK_nonneg
#print axioms transport_expansion
#print axioms component_transport
#print axioms frobenius_centered_gain
#print axioms transported_jacobian_centered_gain
#print axioms forceMap_abs_le
#print axioms force_map_anchor_box_to_B2
#print axioms raw_pmi_channel4_square_scale
#print axioms raw_pmi_channel5_square_scale
#print axioms channel4_double_normalization_factor
#print axioms channel5_double_normalization_factor

end

end RouteBP5CoordinateTransport
