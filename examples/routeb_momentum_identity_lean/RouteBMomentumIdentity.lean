import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBMomentumIdentity

noncomputable section

/-!
Pure exact-real algebra for the block-(4,5) momentum seam.

The fields of `TrigInputs` are intentionally ordinary real variables.  Their
names record the intended sine/cosine slots, but this leaf does not assert any
trigonometric relation between them.  In particular, this module has no DH,
Julia, trajectory, residual, or interval-bound premise.
-/

structure TrigInputs where
  sinS : ℝ
  cosS : ℝ
  sinX : ℝ
  cosX : ℝ
  sinY : ℝ
  cosY : ℝ
  sinZ : ℝ
  cosZ : ℝ

def A0 : ℝ := 7 / 60
def m : ℝ := 40147 / 800000
def J : ℝ := 1 / 60
def mu : ℝ := 1 / 1000000
def k : ℝ := 147 / 800000
def b : ℝ := 399 / 400000
def d : ℝ := 441 / 400000
def j : ℝ := 21 / 80000
def e : ℝ := 21 / 50000

def A (t : TrigInputs) : ℝ := A0 + k * t.sinY ^ 2

def H (t : TrigInputs) : ℝ := d * t.sinZ + e

def F (t : TrigInputs) : ℝ :=
  A t * t.cosS +
    t.sinY *
      (t.cosX * (H t + b * t.sinS + k * t.sinS * t.cosY) +
        j * t.cosS * t.sinX)

def f (t : TrigInputs) : ℝ :=
  -t.sinX * t.sinY * (b + k * t.cosY)

def h (t : TrigInputs) : ℝ :=
  (m + b * t.cosY) * t.sinS * t.sinX +
    H t * t.sinX * t.cosY +
    j * (t.sinS * t.sinY - t.cosS * t.cosX * t.cosY)

def g (t : TrigInputs) : ℝ :=
  t.cosX * (m + b * t.cosY)

def delta4 (t : TrigInputs) : ℝ :=
  -d * t.cosZ * t.sinX * t.sinY

def delta5 (t : TrigInputs) : ℝ :=
  d * (t.cosZ * t.cosX * t.cosY - t.sinZ * t.sinY)

def V (v2 v3 : ℝ) : ℝ := v2 + v3

def R4 : ℝ := A0 + mu
def R5 : ℝ := m + mu

def sigma4 (t : TrigInputs) (v1 v2 v3 v4 v6 : ℝ) : ℝ :=
  k * t.sinY ^ 2 * v4 + F t * v1 + f t * V v2 v3 +
    delta4 t * v2 + J * t.cosY * v6

def sigma5 (t : TrigInputs) (v1 v2 v3 : ℝ) : ℝ :=
  h t * v1 + g t * V v2 v3 + delta5 t * v2

def p4 (t : TrigInputs) (v1 v2 v3 v4 v6 : ℝ) : ℝ :=
  (A t + mu) * v4 + F t * v1 + f t * V v2 v3 +
    delta4 t * v2 + J * t.cosY * v6

def p5 (t : TrigInputs) (v1 v2 v3 v5 : ℝ) : ℝ :=
  (m + mu) * v5 + h t * v1 + g t * V v2 v3 + delta5 t * v2

/-! The same sigma expressions before the common `V = v2 + v3` rewrite. -/

def sigma4Separated (t : TrigInputs) (v1 v2 v3 v4 v6 : ℝ) : ℝ :=
  k * t.sinY ^ 2 * v4 + F t * v1 + f t * v2 + f t * v3 +
    delta4 t * v2 + J * t.cosY * v6

def sigma5Separated (t : TrigInputs) (v1 v2 v3 : ℝ) : ℝ :=
  h t * v1 + g t * v2 + g t * v3 + delta5 t * v2

theorem V_def (v2 v3 : ℝ) : V v2 v3 = v2 + v3 := by
  rfl

theorem linear_recombination (c v2 v3 : ℝ) :
    c * v2 + c * v3 = c * V v2 v3 := by
  unfold V
  ring

theorem f_V_recombination (t : TrigInputs) (v2 v3 : ℝ) :
    f t * v2 + f t * v3 = f t * V v2 v3 := by
  exact linear_recombination (f t) v2 v3

theorem g_V_recombination (t : TrigInputs) (v2 v3 : ℝ) :
    g t * v2 + g t * v3 = g t * V v2 v3 := by
  exact linear_recombination (g t) v2 v3

theorem sigma4_V_correlation (t : TrigInputs) (v1 v2 v3 v4 v6 : ℝ) :
    sigma4Separated t v1 v2 v3 v4 v6 = sigma4 t v1 v2 v3 v4 v6 := by
  unfold sigma4Separated sigma4
  rw [← f_V_recombination t v2 v3]
  ring

theorem sigma5_V_correlation (t : TrigInputs) (v1 v2 v3 : ℝ) :
    sigma5Separated t v1 v2 v3 = sigma5 t v1 v2 v3 := by
  unfold sigma5Separated sigma5
  rw [← g_V_recombination t v2 v3]
  ring

theorem p4_minus_R4v4_eq_sigma4
    (t : TrigInputs) (v1 v2 v3 v4 v6 : ℝ) :
    p4 t v1 v2 v3 v4 v6 - R4 * v4 =
      sigma4 t v1 v2 v3 v4 v6 := by
  unfold p4 sigma4 R4 A A0
  ring

theorem p5_minus_R5v5_eq_sigma5
    (t : TrigInputs) (v1 v2 v3 v5 : ℝ) :
    p5 t v1 v2 v3 v5 - R5 * v5 =
    sigma5 t v1 v2 v3 := by
  unfold p5 sigma5 R5
  ring

theorem momentum_identity_seam
    (t : TrigInputs) (v1 v2 v3 v4 v5 v6 : ℝ) :
    (p4 t v1 v2 v3 v4 v6 - R4 * v4 = sigma4 t v1 v2 v3 v4 v6) ∧
      (p5 t v1 v2 v3 v5 - R5 * v5 = sigma5 t v1 v2 v3) := by
  exact ⟨p4_minus_R4v4_eq_sigma4 t v1 v2 v3 v4 v6,
    p5_minus_R5v5_eq_sigma5 t v1 v2 v3 v5⟩

theorem p4_eq_reference_plus_sigma4
    (t : TrigInputs) (v1 v2 v3 v4 v6 : ℝ) :
    p4 t v1 v2 v3 v4 v6 =
      R4 * v4 + sigma4 t v1 v2 v3 v4 v6 := by
  have h := p4_minus_R4v4_eq_sigma4 t v1 v2 v3 v4 v6
  linarith

theorem p5_eq_reference_plus_sigma5
    (t : TrigInputs) (v1 v2 v3 v5 : ℝ) :
    p5 t v1 v2 v3 v5 = R5 * v5 + sigma5 t v1 v2 v3 := by
  have h := p5_minus_R5v5_eq_sigma5 t v1 v2 v3 v5
  linarith

#print axioms V_def
#print axioms linear_recombination
#print axioms f_V_recombination
#print axioms g_V_recombination
#print axioms sigma4_V_correlation
#print axioms sigma5_V_correlation
#print axioms p4_minus_R4v4_eq_sigma4
#print axioms p5_minus_R5v5_eq_sigma5
#print axioms momentum_identity_seam
#print axioms p4_eq_reference_plus_sigma4
#print axioms p5_eq_reference_plus_sigma5

end
end RouteBMomentumIdentity
