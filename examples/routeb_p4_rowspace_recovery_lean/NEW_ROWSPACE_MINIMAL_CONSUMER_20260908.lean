import NEW_ROWSPACE_RECOVERY_20260908

set_option autoImplicit false

namespace RouteBP4RowspaceMinimalConsumer

/-!
OPEN_UNCOMPILED. L.comp Y = P is the linear-map form of L*Y=P.
One fixed L serves every query. No DH instance, norm estimate or receipt.
-/

variable {X O Z : Type*}
variable [AddCommGroup X] [Module ℝ X]
variable [AddCommGroup O] [Module ℝ O]
variable [AddCommGroup Z] [Module ℝ Z]

theorem recover_with_defect (Y : X →ₗ[ℝ] O) (P : X →ₗ[ℝ] Z)
    (L : O →ₗ[ℝ] Z) (hFactor : L.comp Y = P)
    (x : X) (b e : O) (hObs : Y x = b + e) :
    P x = L b + L e := by
  have hf := congrArg (fun F : X →ₗ[ℝ] Z => F x) hFactor
  change L (Y x) = P x at hf
  rw [← hf, hObs, map_add]

/-- Recovery existence is uniform in x,b,e, not a pointwise choice of L. -/
theorem exists_uniform_recovery (Y : X →ₗ[ℝ] O) (P : X →ₗ[ℝ] Z)
    (hFactor : ∃ L : O →ₗ[ℝ] Z, L.comp Y = P) :
    ∃ L : O →ₗ[ℝ] Z, L.comp Y = P ∧
      ∀ (x : X) (b e : O), Y x = b + e → P x = L b + L e := by
  obtain ⟨L, hL⟩ := hFactor
  exact ⟨L, hL, fun x b e hObs => recover_with_defect Y P L hL x b e hObs⟩

/-- The error bound is a separate input on the SAME L as the factorization. -/
theorem coordinate_defect_bound (Y : X →ₗ[ℝ] O) (P : X →ₗ[ℝ] Z)
    (L : O →ₗ[ℝ] Z) (hFactor : L.comp Y = P)
    (coordinate : Z →ₗ[ℝ] ℝ) (x : X) (b e : O) (delta : ℝ)
    (hObs : Y x = b + e) (hError : |coordinate (L e)| ≤ delta) :
    |coordinate (P x) - coordinate (L b)| ≤ delta := by
  rw [recover_with_defect Y P L hFactor x b e hObs, map_add, add_sub_cancel_left]
  exact hError

/-- Finite matrix-sized spaces without importing matrix multiplication APIs.
Y is m-by-n, P is k-by-n and L is k-by-m in the standard coordinate bases. -/
theorem finite_coordinate_defect_bound {n m k : ℕ}
    (Y : (Fin n → ℝ) →ₗ[ℝ] (Fin m → ℝ))
    (P : (Fin n → ℝ) →ₗ[ℝ] (Fin k → ℝ))
    (L : (Fin m → ℝ) →ₗ[ℝ] (Fin k → ℝ)) (hFactor : L.comp Y = P)
    (x : Fin n → ℝ) (b e : Fin m → ℝ) (delta : Fin k → ℝ)
    (hObs : Y x = b + e) (hError : ∀ i, |L e i| ≤ delta i) :
    ∀ i, |P x i - L b i| ≤ delta i := by
  intro i
  have h := congrArg (fun v : Fin k → ℝ => v i)
    (recover_with_defect Y P L hFactor x b e hObs)
  change P x i = L b i + L e i at h
  rw [h, add_sub_cancel_left]
  exact hError i

end RouteBP4RowspaceMinimalConsumer
