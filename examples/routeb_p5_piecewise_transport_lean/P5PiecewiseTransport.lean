import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Route-B P5 piecewise cell/path transport sidecar

This file formalizes the finite algebraic layer from
`review-T-P5-023-liuguanyi-20260907T0916.md`.

The source/calculus layer is deliberately outside this sidecar: a checker must
certify each connecting segment and provide its local residual increment bound.
The theorems below compose those segment contracts, telescope the force error,
and produce the squared centered-gain consumer used by P5.  No Julia/Float64
Jacobian semantics, concrete P8 cell chain, ODE coverage, provenance, admission,
or final integration claim is made here.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5PiecewiseTransport

noncomputable section

/-- Explicit finite linear force map. -/
def forceMap {p m : ℕ}
    (A : Fin p → Fin m → ℝ)
    (x : Fin m → ℝ)
    (a : Fin p) : ℝ :=
  ∑ i, A a i * x i

/-- One segment's source-to-consumer transport coefficient. -/
def segmentK {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (s : Fin R) (a : Fin p) (q : Fin k) : ℝ :=
  ∑ i, ∑ j, Aabs a i * (H s i j * S s j q)

/-- Sum of all segment transport coefficients along a certified path. -/
def pathK {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (a : Fin p) (q : Fin k) : ℝ :=
  ∑ s, segmentK Aabs H S s a q

/-- Frobenius-style squared gain charged by the complete certified path. -/
def pathEll2 {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ) : ℝ :=
  ∑ a, ∑ q, pathK Aabs H S a q ^ 2

/-- Scalar finite telescoping identity for a path with `R` increments. -/
theorem telescoping_nat (f : ℕ → ℝ) (R : ℕ) :
    (∑ r in Finset.range R, (f (r + 1) - f r)) = f R - f 0 := by
  induction R with
  | zero => simp
  | succ R ih =>
      rw [Finset.sum_range_succ, ih]
      ring

/-- Triangle inequality for the explicit finite force map. -/
theorem forceMap_abs_le {p m : ℕ}
    (A : Fin p → Fin m → ℝ)
    (x : Fin m → ℝ)
    (a : Fin p) :
    |forceMap A x a| ≤ ∑ i, |A a i| * |x i| := by
  have h := Finset.abs_sum_le_sum_abs (fun i : Fin m => A a i * x i) Finset.univ
  simpa [forceMap, abs_mul] using h

/-- After an exact telescoping of the raw residual into segment increments,
force-map magnitude is bounded by the sum of the segmentwise magnitudes. -/
theorem forceMap_piecewise_abs_le {R p m : ℕ}
    (A : Fin p → Fin m → ℝ)
    (de : Fin R → Fin m → ℝ)
    (a : Fin p) :
    |forceMap A (fun i => ∑ s, de s i) a| ≤
      ∑ s, ∑ i, |A a i| * |de s i| := by
  calc
    |forceMap A (fun i => ∑ s, de s i) a| ≤
        ∑ i, |A a i| * |∑ s, de s i| :=
      forceMap_abs_le A (fun i => ∑ s, de s i) a
    _ ≤ ∑ i, |A a i| * (∑ s, |de s i|) := by
      apply Finset.sum_le_sum
      intro i hi
      apply mul_le_mul_of_nonneg_left
      · exact Finset.abs_sum_le_sum_abs (fun s : Fin R => de s i) Finset.univ
      · exact abs_nonneg (A a i)
    _ = ∑ s, ∑ i, |A a i| * |de s i| := by
      calc
        (∑ i, |A a i| * (∑ s, |de s i|)) =
            ∑ i, ∑ s, |A a i| * |de s i| := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [Finset.mul_sum]
        _ = ∑ s, ∑ i, |A a i| * |de s i| := Finset.sum_comm

/-- Distributive/reindexing identity for one certified segment. -/
theorem segment_expansion {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (dz : Fin k → ℝ)
    (s : Fin R) (a : Fin p) :
    (∑ i, Aabs a i * (∑ j, H s i j * (∑ q, S s j q * |dz q|))) =
      ∑ q, segmentK Aabs H S s a q * |dz q| := by
  calc
    (∑ i, Aabs a i * (∑ j, H s i j * (∑ q, S s j q * |dz q|))) =
        ∑ i, ∑ j, ∑ q,
          Aabs a i * (H s i j * (S s j q * |dz q|)) := by
            simp_rw [Finset.mul_sum]
    _ = ∑ i, ∑ q, ∑ j,
          Aabs a i * (H s i j * (S s j q * |dz q|)) := by
            apply Finset.sum_congr rfl
            intro i hi
            exact Finset.sum_comm
    _ = ∑ q, ∑ i, ∑ j,
          Aabs a i * (H s i j * (S s j q * |dz q|)) := by
            exact Finset.sum_comm
    _ = ∑ q, segmentK Aabs H S s a q * |dz q| := by
      apply Finset.sum_congr rfl
      intro q hq
      simp [segmentK, Finset.sum_mul, mul_assoc]

/-- All segment expansions compose into the single path coefficient `pathK`. -/
theorem path_expansion {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (dz : Fin k → ℝ)
    (a : Fin p) :
    (∑ s, ∑ i, Aabs a i *
      (∑ j, H s i j * (∑ q, S s j q * |dz q|))) =
      ∑ q, pathK Aabs H S a q * |dz q| := by
  calc
    (∑ s, ∑ i, Aabs a i *
      (∑ j, H s i j * (∑ q, S s j q * |dz q|))) =
        ∑ s, ∑ q, segmentK Aabs H S s a q * |dz q| := by
      apply Finset.sum_congr rfl
      intro s hs
      exact segment_expansion Aabs H S dz s a
    _ = ∑ q, ∑ s, segmentK Aabs H S s a q * |dz q| := Finset.sum_comm
    _ = ∑ q, pathK Aabs H S a q * |dz q| := by
      apply Finset.sum_congr rfl
      intro q hq
      rw [pathK, Finset.sum_mul]

/-- Local state-coordinate and residual increment contracts compose along any
finite certified segment chain.  The force premise is deliberately a
post-telescoping component contract, so cell geometry remains upstream. -/
theorem piecewise_component_transport {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (dxi : Fin R → Fin n → ℝ)
    (dz : Fin k → ℝ)
    (de : Fin R → Fin m → ℝ)
    (rc : Fin p → ℝ)
    (hA : ∀ a i, 0 ≤ Aabs a i)
    (hH : ∀ s i j, 0 ≤ H s i j)
    (hState : ∀ s j, |dxi s j| ≤ ∑ q, S s j q * |dz q|)
    (hJac : ∀ s i, |de s i| ≤ ∑ j, H s i j * |dxi s j|)
    (hForce : ∀ a, |rc a| ≤ ∑ s, ∑ i, Aabs a i * |de s i|) :
    ∀ a, |rc a| ≤ ∑ q, pathK Aabs H S a q * |dz q| := by
  intro a
  calc
    |rc a| ≤ ∑ s, ∑ i, Aabs a i * |de s i| := hForce a
    _ ≤ ∑ s, ∑ i, Aabs a i * (∑ j, H s i j * |dxi s j|) := by
      apply Finset.sum_le_sum
      intro s hs
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left (hJac s i) (hA a i)
    _ ≤ ∑ s, ∑ i, Aabs a i *
        (∑ j, H s i j * (∑ q, S s j q * |dz q|)) := by
      apply Finset.sum_le_sum
      intro s hs
      apply Finset.sum_le_sum
      intro i hi
      apply mul_le_mul_of_nonneg_left
      · apply Finset.sum_le_sum
        intro j hj
        exact mul_le_mul_of_nonneg_left (hState s j) (hH s i j)
      · exact hA a i
    _ = ∑ q, pathK Aabs H S a q * |dz q| :=
      path_expansion Aabs H S dz a

/-- Row-wise finite Cauchy converts component path bounds into a squared gain. -/
theorem frobenius_centered_gain {p k : ℕ}
    (K : Fin p → Fin k → ℝ)
    (rc : Fin p → ℝ)
    (dz : Fin k → ℝ)
    (hcomp : ∀ a, |rc a| ≤ ∑ q, K a q * |dz q|) :
    (∑ a, rc a ^ 2) ≤
      (∑ a, ∑ q, K a q ^ 2) * (∑ q, dz q ^ 2) := by
  have hrow : ∀ a,
      rc a ^ 2 ≤ (∑ q, K a q ^ 2) * (∑ q, dz q ^ 2) := by
    intro a
    have hsumNonneg : 0 ≤ ∑ q, K a q * |dz q| :=
      le_trans (abs_nonneg (rc a)) (hcomp a)
    have hsquare :
        rc a ^ 2 ≤ (∑ q, K a q * |dz q|) ^ 2 := by
      rw [sq_le_sq]
      simpa [abs_of_nonneg hsumNonneg] using hcomp a
    have hcauchy :=
      Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (K a) (fun q => |dz q|)
    have hcauchy' :
        (∑ q, K a q * |dz q|) ^ 2 ≤
          (∑ q, K a q ^ 2) * (∑ q, dz q ^ 2) := by
      simpa [sq_abs] using hcauchy
    exact hsquare.trans hcauchy'
  calc
    (∑ a, rc a ^ 2) ≤
        ∑ a, ((∑ q, K a q ^ 2) * (∑ q, dz q ^ 2)) := by
      exact Finset.sum_le_sum fun a ha => hrow a
    _ = (∑ a, ∑ q, K a q ^ 2) * (∑ q, dz q ^ 2) := by
      rw [Finset.sum_mul]

/-- Main source-independent piecewise path theorem. -/
theorem piecewise_centered_gain {R p m n k : ℕ}
    (Aabs : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (dxi : Fin R → Fin n → ℝ)
    (dz : Fin k → ℝ)
    (de : Fin R → Fin m → ℝ)
    (rc : Fin p → ℝ)
    (hA : ∀ a i, 0 ≤ Aabs a i)
    (hH : ∀ s i j, 0 ≤ H s i j)
    (hState : ∀ s j, |dxi s j| ≤ ∑ q, S s j q * |dz q|)
    (hJac : ∀ s i, |de s i| ≤ ∑ j, H s i j * |dxi s j|)
    (hForce : ∀ a, |rc a| ≤ ∑ s, ∑ i, Aabs a i * |de s i|) :
    (∑ a, rc a ^ 2) ≤
      pathEll2 Aabs H S * (∑ q, dz q ^ 2) := by
  have hcomp :=
    piecewise_component_transport Aabs H S dxi dz de rc hA hH hState hJac hForce
  simpa [pathEll2] using
    (frobenius_centered_gain (fun a q => pathK Aabs H S a q) rc dz hcomp)

/-- Specialization in which the centered force is exactly the force map of the
sum of certified raw residual increments.  Raw-PMI normalization, when needed,
is represented only by `A` here and is therefore applied exactly once. -/
theorem piecewise_force_centered_gain {R p m n k : ℕ}
    (A : Fin p → Fin m → ℝ)
    (H : Fin R → Fin m → Fin n → ℝ)
    (S : Fin R → Fin n → Fin k → ℝ)
    (dxi : Fin R → Fin n → ℝ)
    (dz : Fin k → ℝ)
    (de : Fin R → Fin m → ℝ)
    (hH : ∀ s i j, 0 ≤ H s i j)
    (hState : ∀ s j, |dxi s j| ≤ ∑ q, S s j q * |dz q|)
    (hJac : ∀ s i, |de s i| ≤ ∑ j, H s i j * |dxi s j|) :
    (∑ a, forceMap A (fun i => ∑ s, de s i) a ^ 2) ≤
      pathEll2 (fun a i => |A a i|) H S * (∑ q, dz q ^ 2) := by
  apply piecewise_centered_gain
      (fun a i => |A a i|) H S dxi dz de
      (fun a => forceMap A (fun i => ∑ s, de s i) a)
  · intro a i
    exact abs_nonneg (A a i)
  · exact hH
  · exact hState
  · exact hJac
  · intro a
    exact forceMap_piecewise_abs_le A de a

/-- A minimal failure boundary: zero local budgets on disconnected pieces do
not constrain an unbridged endpoint jump.  A connecting-path premise is
therefore logically indispensable. -/
theorem unbridged_endpoint_jump (M : ℝ) (hM : 0 < M) :
    ∃ eMinus ePlus : ℝ,
      |ePlus - eMinus| = M ∧ ¬ |ePlus - eMinus| ≤ 0 := by
  refine ⟨0, M, ?_, ?_⟩
  · simpa [abs_of_pos hM]
  · simpa [abs_of_pos hM] using (not_le.mpr hM)

#print axioms telescoping_nat
#print axioms forceMap_abs_le
#print axioms forceMap_piecewise_abs_le
#print axioms segment_expansion
#print axioms path_expansion
#print axioms piecewise_component_transport
#print axioms frobenius_centered_gain
#print axioms piecewise_centered_gain
#print axioms piecewise_force_centered_gain
#print axioms unbridged_endpoint_jump

end

end RouteBP5PiecewiseTransport
