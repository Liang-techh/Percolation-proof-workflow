import Mathlib

set_option autoImplicit false

namespace NEW_BODY6_SLICE_STEP6_Core20260907

noncomputable section

/- Source-independent algebra only. UNCOMPILED / NOT_RUN.
   No repository source, CSV, body evaluator or admission record is imported. -/

abbrev V3 := Fin 3 → ℝ
abbrev Frame := Matrix (Fin 4) (Fin 4) ℝ

def midpointV (o e : V3) : V3 := fun a => (o a + e a) / 2

def crossV (u v : V3) : V3 :=
  ![u 1 * v 2 - u 2 * v 1,
    u 2 * v 0 - u 0 * v 2,
    u 0 * v 1 - u 1 * v 0]

/- Neither orthogonality nor a homogeneous bottom row of F is needed.
   Only the last column of the right-hand step matters. -/
theorem product_endpoint_attempt (F A : Frame) (d : ℝ)
    (hcol : ∀ k : Fin 4, A k 3 = (![0, 0, d, 1] : Fin 4 → ℝ) k)
    (a : Fin 4) :
    (F * A) a 3 = F a 3 + d * F a 2 := by
  rw [Matrix.mul_apply]
  simp_rw [hcol]
  norm_num [Fin.sum_univ_succ] <;> ring

theorem endpoint_center_attempt (o e z : V3) (d : ℝ)
    (he : ∀ a, e a = o a + d * z a) :
    midpointV o e = fun a => o a + (d / 2) * z a := by
  funext a
  dsimp [midpointV]
  rw [he a]
  ring

theorem cross_scaled_self_attempt (z : V3) (s : ℝ) :
    crossV z (fun a => s * z a) = 0 := by
  funext a
  fin_cases a <;> simp [crossV] <;> ring

theorem endpoint_velocity_zero_attempt (o e z : V3) (d : ℝ)
    (he : ∀ a, e a = o a + d * z a) :
    crossV z (fun a => midpointV o e a - o a) = 0 := by
  rw [endpoint_center_attempt o e z d he]
  have hv : (fun a => o a + (d / 2) * z a - o a) =
      (fun a => (d / 2) * z a) := by funext a; ring
  rw [hv]
  exact cross_scaled_self_attempt z (d / 2)

/- Full signed frequencies, real coefficients only. The compact coordinates
   later instantiate x=q 1+q 2, y=q 3, z=q 4. No factor-two convention. -/
structure Row where
  row : Fin 6
  nx : ℤ
  ny : ℤ
  nz : ℤ
  coeff : ℚ
  deriving DecidableEq

def phase3 (r : Row) (x y z : ℝ) : ℝ :=
  (r.nx : ℝ) * x + (r.ny : ℝ) * y + (r.nz : ℝ) * z

def atom3 (r : Row) (x y z : ℝ) : ℝ :=
  (r.coeff : ℝ) * Real.cos (phase3 r x y z)

def evalRows (rs : List Row) (x y z : ℝ) (i : Fin 6) : ℝ :=
  (rs.map (fun r => if r.row = i then atom3 r x y z else 0)).sum

def rows23 : List Row :=
  [⟨0, -1, -1, -1, 1 / 480⟩,
   ⟨0, -1, -1, 1, -1 / 480⟩,
   ⟨0, -1, 0, -1, 1 / 240⟩,
   ⟨0, -1, 0, 1, 1 / 240⟩,
   ⟨0, -1, 1, -1, 1 / 480⟩,
   ⟨0, -1, 1, 1, -1 / 480⟩,
   ⟨0, 1, -1, -1, -1 / 480⟩,
   ⟨0, 1, -1, 1, 1 / 480⟩,
   ⟨0, 1, 0, -1, 1 / 240⟩,
   ⟨0, 1, 0, 1, 1 / 240⟩,
   ⟨0, 1, 1, -1, -1 / 480⟩,
   ⟨0, 1, 1, 1, 1 / 480⟩,
   ⟨1, 0, -1, -1, -1 / 240⟩,
   ⟨1, 0, -1, 1, 1 / 240⟩,
   ⟨1, 0, 1, -1, 1 / 240⟩,
   ⟨1, 0, 1, 1, -1 / 240⟩,
   ⟨2, 0, -1, -1, -1 / 240⟩,
   ⟨2, 0, -1, 1, 1 / 240⟩,
   ⟨2, 0, 1, -1, 1 / 240⟩,
   ⟨2, 0, 1, 1, -1 / 240⟩,
   ⟨3, 0, 0, -1, 1 / 120⟩,
   ⟨3, 0, 0, 1, 1 / 120⟩,
   ⟨5, 0, 0, 0, 1 / 60⟩]

def columnFormula (x y z : ℝ) (i : Fin 6) : ℝ :=
  (1 / 60 : ℝ) *
    (![Real.cos x * Real.cos z - Real.sin x * Real.cos y * Real.sin z,
       Real.sin y * Real.sin z, Real.sin y * Real.sin z,
       Real.cos z, 0, 1] : Fin 6 → ℝ) i

/- Finite trigonometric identity on three arbitrary real variables.
   This is a concrete proof attempt, not an assumed Fourier leaf. -/
theorem rows23_fold_attempt (x y z : ℝ) (i : Fin 6) :
    evalRows rows23 x y z i = columnFormula x y z i := by
  fin_cases i <;>
    norm_num [evalRows, rows23, atom3, phase3, columnFormula,
      Real.cos_add, Real.sin_add, Real.cos_sub, Real.sin_sub,
      Real.cos_neg, Real.sin_neg] <;> ring

end
end NEW_BODY6_SLICE_STEP6_Core20260907
