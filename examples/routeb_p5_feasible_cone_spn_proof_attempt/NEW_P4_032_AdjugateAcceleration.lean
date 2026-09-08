import Mathlib

/-!
OPEN_UNCOMPILED / pending. Source-independent symmetric 2x2 descriptor
identities and a rational projected-acceleration interface. Signed terms are
contracted before absolute enclosure. No DH/source/trajectory binding or
Lean/kernel receipt is asserted. No local Lean/Lake run was performed.
-/
set_option autoImplicit false

namespace RouteBP4032AdjugateAcceleration

def det2 (a b c : ℝ) : ℝ := a * c - b ^ 2
def numerator1 (b c f1 f2 : ℝ) : ℝ := c * f1 - b * f2
def numerator2 (a b f1 f2 : ℝ) : ℝ := a * f2 - b * f1
def projectedNumerator (a b c f1 f2 ell1 ell2 : ℝ) : ℝ :=
  ell1 * numerator1 b c f1 f2 + ell2 * numerator2 a b f1 f2

theorem cramer_identity (a b c f1 f2 u1 u2 : ℝ)
    (h1 : a * u1 + b * u2 = f1) (h2 : b * u1 + c * u2 = f2) :
    det2 a b c * u1 = numerator1 b c f1 f2 ∧
    det2 a b c * u2 = numerator2 a b f1 f2 := by
  constructor
  · calc
      det2 a b c * u1 = c * (a * u1 + b * u2) - b * (b * u1 + c * u2) := by
        unfold det2
        ring
      _ = numerator1 b c f1 f2 := by rw [h1, h2]; rfl
  · calc
      det2 a b c * u2 = a * (b * u1 + c * u2) - b * (a * u1 + b * u2) := by
        unfold det2
        ring
      _ = numerator2 a b f1 f2 := by rw [h1, h2]; rfl

theorem projected_identity (a b c f1 f2 u1 u2 ell1 ell2 : ℝ)
    (h1 : a * u1 + b * u2 = f1) (h2 : b * u1 + c * u2 = f2) :
    det2 a b c * (ell1 * u1 + ell2 * u2) =
      projectedNumerator a b c f1 f2 ell1 ell2 := by
  obtain ⟨hc1, hc2⟩ := cramer_identity a b c f1 f2 u1 u2 h1 h2
  calc
    det2 a b c * (ell1 * u1 + ell2 * u2) =
        ell1 * (det2 a b c * u1) + ell2 * (det2 a b c * u2) := by ring
    _ = projectedNumerator a b c f1 f2 ell1 ell2 := by
      rw [hc1, hc2]
      rfl

/-- Division-free order gate. The enclosure itself supplies 0 <= R;
nonnegativity of upper is consequently implied, rather than needed here. -/
theorem abs_bound_of_positive_multiplier (D delta u N R upper : ℝ)
    (hdelta : 0 < delta) (hD : delta ≤ D) (hid : D * u = N)
    (hN : |N| ≤ R) (hgate : R ≤ delta * upper) : |u| ≤ upper := by
  have hDpos : 0 < D := lt_of_lt_of_le hdelta hD
  have hscaled : D * |u| ≤ R := by
    simpa only [← hid, abs_mul, abs_of_pos hDpos] using hN
  have hsmall : delta * |u| ≤ D * |u| :=
    mul_le_mul_of_nonneg_right hD (abs_nonneg u)
  exact (mul_le_mul_left hdelta).mp (hsmall.trans (hscaled.trans hgate))

theorem projected_accel_bound (a b c f1 f2 u1 u2 ell1 ell2 delta R upper : ℝ)
    (h1 : a * u1 + b * u2 = f1) (h2 : b * u1 + c * u2 = f2)
    (hdelta : 0 < delta) (hdet : delta ≤ det2 a b c)
    (hnum : |projectedNumerator a b c f1 f2 ell1 ell2| ≤ R)
    (hgate : R ≤ delta * upper) : |ell1 * u1 + ell2 * u2| ≤ upper :=
  abs_bound_of_positive_multiplier (det2 a b c) delta _ _ R upper
    hdelta hdet (projected_identity a b c f1 f2 u1 u2 ell1 ell2 h1 h2) hnum hgate

theorem coordinate_accel_bounds (a b c f1 f2 u1 u2 delta R1 R2 Q1 Q2 : ℝ)
    (h1 : a * u1 + b * u2 = f1) (h2 : b * u1 + c * u2 = f2)
    (hdelta : 0 < delta) (hdet : delta ≤ det2 a b c)
    (hN1 : |numerator1 b c f1 f2| ≤ R1) (hN2 : |numerator2 a b f1 f2| ≤ R2)
    (hg1 : R1 ≤ delta * Q1) (hg2 : R2 ≤ delta * Q2) :
    |u1| ≤ Q1 ∧ |u2| ≤ Q2 := by
  obtain ⟨hc1, hc2⟩ := cramer_identity a b c f1 f2 u1 u2 h1 h2
  exact ⟨abs_bound_of_positive_multiplier _ delta u1 _ R1 Q1 hdelta hdet hc1 hN1 hg1,
    abs_bound_of_positive_multiplier _ delta u2 _ R2 Q2 hdelta hdet hc2 hN2 hg2⟩

structure RationalPacket where
  delta : ℚ
  numeratorUpper : ℚ
  accelerationUpper : ℚ
  delta_pos : 0 < delta
  acceleration_nonneg : 0 ≤ accelerationUpper
  gate : numeratorUpper ≤ delta * accelerationUpper

structure DescriptorFields (X : Type*) where
  domain : X → Prop
  a b c f1 f2 acceleration1 acceleration2 observableAcceleration : X → ℝ
  ell1 ell2 : ℝ

/-- Every witness refers to the same state, domain and cell. The observable
equality is an explicit derivative/semantics obligation, not a chain-rule
theorem inferred from its name. The fixed affine offset has no algebraic role. -/
structure SameCellEvidence {X : Type*} (src : DescriptorFields X)
    (cell : X → Prop) (p : RationalPacket) : Prop where
  row1 : ∀ x, src.domain x → cell x →
    src.a x * src.acceleration1 x + src.b x * src.acceleration2 x = src.f1 x
  row2 : ∀ x, src.domain x → cell x →
    src.b x * src.acceleration1 x + src.c x * src.acceleration2 x = src.f2 x
  determinant_lower : ∀ x, src.domain x → cell x → (p.delta : ℝ) ≤
    det2 (src.a x) (src.b x) (src.c x)
  numerator_upper : ∀ x, src.domain x → cell x →
    |projectedNumerator (src.a x) (src.b x) (src.c x) (src.f1 x) (src.f2 x)
      src.ell1 src.ell2| ≤ (p.numeratorUpper : ℝ)
  observable_binding : ∀ x, src.domain x → cell x →
    src.observableAcceleration x =
      src.ell1 * src.acceleration1 x + src.ell2 * src.acceleration2 x

theorem same_cell_observable_cap {X : Type*} (src : DescriptorFields X)
    (cell : X → Prop) (p : RationalPacket) (e : SameCellEvidence src cell p) :
    ∀ x, src.domain x → cell x →
      |src.observableAcceleration x| ≤ (p.accelerationUpper : ℝ) := by
  intro x hx hc
  rw [e.observable_binding x hx hc]
  apply projected_accel_bound (src.a x) (src.b x) (src.c x) (src.f1 x) (src.f2 x)
    (src.acceleration1 x) (src.acceleration2 x) src.ell1 src.ell2 (p.delta : ℝ)
    (p.numeratorUpper : ℝ) (p.accelerationUpper : ℝ)
  · exact e.row1 x hx hc
  · exact e.row2 x hx hc
  · exact_mod_cast p.delta_pos
  · exact e.determinant_lower x hx hc
  · exact e.numerator_upper x hx hc
  · exact_mod_cast p.gate

/-- Correlated source-independent family from the remote mathematical review.
The raw box fallback loses cancellation even though the determinant is one. -/
theorem cancellation_family (t : ℝ) :
    det2 1 t (1 + t^2) = 1 ∧
    (1 : ℝ) * 0 + t * 1 = t ∧
    t * 0 + (1 + t^2) * 1 = 1 + t^2 ∧
    projectedNumerator 1 t (1 + t^2) t (1 + t^2) 1 0 = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · dsimp [det2]
    ring
  · ring
  · ring
  · dsimp [projectedNumerator, numerator1, numerator2]
    ring

theorem positive_box_loss (T : ℝ) (hT : 0 < T) : 0 < 2 * T * (1 + T^2) := by
  positivity

end RouteBP4032AdjugateAcceleration
