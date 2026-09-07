import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 central finite-difference to derivative-hull interface

This is a source-independent exact-real algebraic seam.  The first tensor
slot is the differentiated coordinate, so `T k i j` means the derivative of
the `(i,j)` observable in coordinate `k`.  The remainder contract keeps the
central secant, machine/lift error, derivative-hull error, and exported-center
error separate.  No field in this file identifies a source implementation,
Float64 execution, an interval partition, or an admission receipt.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHull

noncomputable section

variable {ι : Type*} [Fintype ι]

abbrev Tensor (ι : Type*) := ι → ι → ι → ℝ

/-! ## Exact source-index algebra -/

/-- The source Christoffel coefficient with tensor order `T k i j`.

The order is intentional: `k` is the differentiation coordinate, while `i`
and `j` are the two mass-matrix slots. -/
def sourceGamma (T : Tensor ι) (i j k : ι) : ℝ :=
  (T k i j + T j i k - T i j k) / 2

/-- The nested-loop source contraction. -/
def sourceCdq (T : Tensor ι) (v : ι → ℝ) (i : ι) : ℝ :=
  ∑ j, ∑ k, sourceGamma T i j k * v j * v k

/-- The generic Christoffel consumer written with the same index order. -/
def christoffelForce (T : Tensor ι) (v : ι → ℝ) (i : ι) : ℝ :=
  ∑ j, ∑ k, ((T k i j + T j i k - T i j k) / 2) * v j * v k

/-- Exact-real source-index bridge; no symmetry of `T` is required. -/
theorem sourceCdq_eq_christoffelForce
    (T : Tensor ι) (v : ι → ℝ) (i : ι) :
    sourceCdq T v i = christoffelForce T v i := by
  rfl

theorem christoffelForce_add
    (T R : Tensor ι) (v : ι → ℝ) (i : ι) :
    christoffelForce (fun k i j => T k i j + R k i j) v i =
      christoffelForce T v i + christoffelForce R v i := by
  unfold christoffelForce
  simp only [Pi.add_apply]
  apply Finset.sum_congr rfl
  intro j hj
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-! ## Componentwise tensor remainder -/

/-- The three-term coefficient radius induced by a derivative-tensor radius. -/
def gammaRadius (mu : Tensor ι) (i j k : ι) : ℝ :=
  (mu k i j + mu j i k + mu i j k) / 2

theorem nested_abs_sum_bound (f : ι → ι → ℝ) :
    |∑ j, ∑ k, f j k| ≤ ∑ j, ∑ k, |f j k| := by
  calc
    |∑ j, ∑ k, f j k| ≤ ∑ j, |∑ k, f j k| := by
      simpa using
        (Finset.abs_sum_le_sum_abs (fun j => ∑ k, f j k) Finset.univ)
    _ ≤ ∑ j, ∑ k, |f j k| := by
      apply Finset.sum_le_sum
      intro j hj
      simpa using
        (Finset.abs_sum_le_sum_abs (fun k => f j k) Finset.univ)

theorem gamma_abs_le_radius
    (mu R : Tensor ι)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hR : ∀ k i j, |R k i j| ≤ mu k i j)
    (i j k : ι) :
    |sourceGamma R i j k| ≤ gammaRadius mu i j k := by
  have hnum :
      |R k i j + R j i k - R i j k| ≤
        mu k i j + mu j i k + mu i j k := by
    calc
      |R k i j + R j i k - R i j k| ≤
          |R k i j + R j i k| + |R i j k| :=
        by
          simpa [sub_eq_add_neg, abs_neg] using
            (abs_add_le (R k i j + R j i k) (-R i j k))
      _ ≤ (|R k i j| + |R j i k|) + |R i j k| := by
        gcongr
        exact abs_add_le _ _
      _ ≤ mu k i j + mu j i k + mu i j k := by
        gcongr
        · exact hR k i j
        · exact hR j i k
        · exact hR i j k
  unfold sourceGamma gammaRadius
  rw [abs_div]
  norm_num
  exact div_le_div_of_nonneg_right hnum (by norm_num)

/-- A componentwise bound for the exact-real central-FD tensor remainder.

If `Tfd = T + R`, then the force difference is bounded using the same `mu`
tensor three times in the coefficient formula, with no source or runtime
interpretation hidden in the statement. -/
theorem fd_christoffel_component_error
    (T R mu : Tensor ι) (v : ι → ℝ) (i : ι)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hR : ∀ k i j, |R k i j| ≤ mu k i j) :
    |christoffelForce (fun k i j => T k i j + R k i j) v i -
        christoffelForce T v i| ≤
      ∑ j, ∑ k, gammaRadius mu i j k * |v j * v k| := by
  have hAdd := christoffelForce_add T R v i
  have hGamma : ∀ j k, |sourceGamma R i j k| ≤ gammaRadius mu i j k := by
    intro j k
    exact gamma_abs_le_radius mu R hmu hR i j k
  calc
    |christoffelForce (fun k i j => T k i j + R k i j) v i -
        christoffelForce T v i| = |christoffelForce R v i| := by
      rw [hAdd]
      congr 1
      ring
    _ ≤ ∑ j, ∑ k, |sourceGamma R i j k * v j * v k| := by
      exact nested_abs_sum_bound
        (fun j k => sourceGamma R i j k * v j * v k)
    _ = ∑ j, ∑ k, |sourceGamma R i j k| * |v j * v k| := by
      apply Finset.sum_congr rfl
      intro j hj
      apply Finset.sum_congr rfl
      intro k hk
      simp [abs_mul, mul_assoc]
    _ ≤ ∑ j, ∑ k, gammaRadius mu i j k * |v j * v k| := by
      apply Finset.sum_le_sum
      intro j hj
      apply Finset.sum_le_sum
      intro k hk
      exact mul_le_mul_of_nonneg_right (hGamma j k) (abs_nonneg _)

/-! ## A power-level consumer (the tensor remainder is not collapsed to six
component offsets). -/

def componentRadius (mu : Tensor ι) (v : ι → ℝ) (i : ι) : ℝ :=
  ∑ j, ∑ k, gammaRadius mu i j k * |v j * v k|

theorem fd_christoffel_power_error
    (T R mu : Tensor ι) (v : ι → ℝ)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hR : ∀ k i j, |R k i j| ≤ mu k i j) :
    |∑ i, v i *
        (christoffelForce (fun k i j => T k i j + R k i j) v i -
          christoffelForce T v i)| ≤
      ∑ i, |v i| * componentRadius mu v i := by
  calc
    |∑ i, v i *
        (christoffelForce (fun k i j => T k i j + R k i j) v i -
          christoffelForce T v i)| ≤
        ∑ i, |v i *
          (christoffelForce (fun k i j => T k i j + R k i j) v i -
            christoffelForce T v i)| := by
      simpa using
        (Finset.abs_sum_le_sum_abs
          (fun i => v i *
            (christoffelForce (fun k i j => T k i j + R k i j) v i -
              christoffelForce T v i)) Finset.univ)
    _ = ∑ i, |v i| * |
        christoffelForce (fun k i j => T k i j + R k i j) v i -
          christoffelForce T v i| := by
      apply Finset.sum_congr rfl
      intro i hi
      simp [abs_mul]
    _ ≤ ∑ i, |v i| * componentRadius mu v i := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left
        (fd_christoffel_component_error T R mu v i hmu hR)
        (abs_nonneg _)

/-! ## Typed central-FD / derivative-hull remainder contract -/

/-- A pointwise contract for one observable `a` and one differentiated
coordinate `k`.

`centralSecant` is the exact-real central operator.  `machineValue` is an
arbitrary lifted/deployed value and is not definitionally identified with it.
`derivativeHullCenter` is the center of an independently supplied derivative
hull; `exportedCenter` allows a separately serialized center. -/
structure CentralFDDerivativeHullContract (X A K : Type*) where
  step : ℝ
  step_ne_zero : step ≠ 0
  eval : X → A → ℝ
  shift : X → ℝ → K → X
  centralSecant : X → A → K → ℝ
  machineValue : X → A → K → ℝ
  derivative : X → A → K → ℝ
  derivativeHullCenter : X → A → K → ℝ
  exportedCenter : X → A → K → ℝ
  machineRadius : X → A → K → ℝ
  centralRadius : X → A → K → ℝ
  derivativeHullRadius : X → A → K → ℝ
  exportRadius : X → A → K → ℝ
  centralSecant_spec : ∀ x a k,
    centralSecant x a k =
      (eval (shift x step k) a - eval (shift x (-step) k) a) /
        (2 * step)
  machine_error : ∀ x a k,
    |machineValue x a k - centralSecant x a k| ≤ machineRadius x a k
  central_error : ∀ x a k,
    |centralSecant x a k - derivative x a k| ≤ centralRadius x a k
  derivative_hull : ∀ x a k,
    |derivative x a k - derivativeHullCenter x a k| ≤
      derivativeHullRadius x a k
  export_error : ∀ x a k,
    |derivativeHullCenter x a k - exportedCenter x a k| ≤
      exportRadius x a k
  machineRadius_nonneg : ∀ x a k, 0 ≤ machineRadius x a k
  centralRadius_nonneg : ∀ x a k, 0 ≤ centralRadius x a k
  derivativeHullRadius_nonneg : ∀ x a k, 0 ≤ derivativeHullRadius x a k
  exportRadius_nonneg : ∀ x a k, 0 ≤ exportRadius x a k

def totalRadius {X A K : Type*}
    (C : CentralFDDerivativeHullContract X A K)
    (x : X) (a : A) (k : K) : ℝ :=
  C.machineRadius x a k + C.centralRadius x a k +
    C.derivativeHullRadius x a k + C.exportRadius x a k

def centralDifference {X A K : Type*}
    (eval : X → A → ℝ) (shift : X → ℝ → K → X) (step : ℝ)
    (x : X) (a : A) (k : K) : ℝ :=
  (eval (shift x step k) a - eval (shift x (-step) k) a) / (2 * step)

theorem central_secant_is_central_difference
    {X A K : Type*}
    (C : CentralFDDerivativeHullContract X A K)
    (x : X) (a : A) (k : K) :
    C.centralSecant x a k =
      centralDifference C.eval C.shift C.step x a k :=
  C.centralSecant_spec x a k

theorem totalRadius_nonneg
    {X A K : Type*}
    (C : CentralFDDerivativeHullContract X A K)
    (x : X) (a : A) (k : K) :
    0 ≤ totalRadius C x a k := by
  unfold totalRadius
  linarith [C.machineRadius_nonneg x a k,
    C.centralRadius_nonneg x a k,
    C.derivativeHullRadius_nonneg x a k,
    C.exportRadius_nonneg x a k]

/-- Exact telescoping decomposition: every contract radius occurs once. -/
theorem central_fd_remainder_decomposition
    {X A K : Type*}
    (C : CentralFDDerivativeHullContract X A K)
    (x : X) (a : A) (k : K) :
    C.machineValue x a k - C.exportedCenter x a k =
      (C.machineValue x a k - C.centralSecant x a k) +
      (C.centralSecant x a k - C.derivative x a k) +
      (C.derivative x a k - C.derivativeHullCenter x a k) +
      (C.derivativeHullCenter x a k - C.exportedCenter x a k) := by
  ring

/-- Composition of central-FD, machine, derivative-hull, and export errors.

The result is an exported-hull membership statement.  It does not assert that
any particular machine or source evaluator satisfies the contract. -/
theorem central_fd_to_derivative_hull
    {X A K : Type*}
    (C : CentralFDDerivativeHullContract X A K)
    (x : X) (a : A) (k : K) :
    |C.machineValue x a k - C.exportedCenter x a k| ≤
      totalRadius C x a k := by
  have hdecomp := central_fd_remainder_decomposition C x a k
  have htriangle :
      |(C.machineValue x a k - C.centralSecant x a k) +
          (C.centralSecant x a k - C.derivative x a k) +
          (C.derivative x a k - C.derivativeHullCenter x a k) +
          (C.derivativeHullCenter x a k - C.exportedCenter x a k)| ≤
        |C.machineValue x a k - C.centralSecant x a k| +
          |C.centralSecant x a k - C.derivative x a k| +
          |C.derivative x a k - C.derivativeHullCenter x a k| +
          |C.derivativeHullCenter x a k - C.exportedCenter x a k| := by
    calc
      |(C.machineValue x a k - C.centralSecant x a k) +
          (C.centralSecant x a k - C.derivative x a k) +
          (C.derivative x a k - C.derivativeHullCenter x a k) +
          (C.derivativeHullCenter x a k - C.exportedCenter x a k)| ≤
          |(C.machineValue x a k - C.centralSecant x a k) +
            (C.centralSecant x a k - C.derivative x a k) +
            (C.derivative x a k - C.derivativeHullCenter x a k)| +
            |C.derivativeHullCenter x a k - C.exportedCenter x a k| :=
        abs_add_le _ _
      _ ≤
          (|(C.machineValue x a k - C.centralSecant x a k) +
            (C.centralSecant x a k - C.derivative x a k)| +
            |C.derivative x a k - C.derivativeHullCenter x a k|) +
            |C.derivativeHullCenter x a k - C.exportedCenter x a k| := by
        gcongr
        exact abs_add_le _ _
      _ ≤
          (|C.machineValue x a k - C.centralSecant x a k| +
            |C.centralSecant x a k - C.derivative x a k|) +
            |C.derivative x a k - C.derivativeHullCenter x a k| +
            |C.derivativeHullCenter x a k - C.exportedCenter x a k| := by
        gcongr
        exact abs_add_le _ _
  rw [hdecomp]
  have hsum :
      |C.machineValue x a k - C.centralSecant x a k| +
          |C.centralSecant x a k - C.derivative x a k| +
          |C.derivative x a k - C.derivativeHullCenter x a k| +
          |C.derivativeHullCenter x a k - C.exportedCenter x a k| ≤
        totalRadius C x a k := by
    linarith [C.machine_error x a k,
      C.central_error x a k,
      C.derivative_hull x a k,
      C.export_error x a k]
  exact htriangle.trans hsum

end

end RouteBP3CentralFDHull

#print axioms RouteBP3CentralFDHull.sourceCdq_eq_christoffelForce
#print axioms RouteBP3CentralFDHull.christoffelForce_add
#print axioms RouteBP3CentralFDHull.fd_christoffel_component_error
#print axioms RouteBP3CentralFDHull.fd_christoffel_power_error
#print axioms RouteBP3CentralFDHull.central_fd_to_derivative_hull
