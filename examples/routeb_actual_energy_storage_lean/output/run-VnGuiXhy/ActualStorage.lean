import ReferenceMass

set_option autoImplicit false
open scoped BigOperators

namespace RouteBActualEnergyStorage
noncomputable section
open RouteBSignedGap

/-- The actual signed gap, specialized from the compiled definition at one state.
H, M, U and Uzero remain explicit source inputs. -/
def actualSignedGap (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) : ℝ :=
  signedGap M0 H (fun _ => M) (fun _ => q) (fun _ => v) (fun _ => U) Uzero 0

def W0 (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) : ℝ :=
  kinetic M0 v - actualSignedGap H M U Uzero q v + (7/75) * q 3^2

def MassPSD (M : Mat 6) : Prop := ∀ z : Vec 6, 0 ≤ quad M z

/-- This equality is algebra, before any Fourier-source identification. -/
theorem W0_actual_energy (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) :
    W0 H M U Uzero q v = kinetic M v + (U-Uzero-kinetic H q) + (7/75)*q 3^2 := by
  unfold W0 actualSignedGap signedGap
  ring

/-- Source identities are hypotheses, while the remainder identity is proved. -/
theorem W0_source_energy (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6)
    (hH : H = H0) (hU : U = referencePotential q)
    (hUzero : Uzero = RouteBGravityTwistFloor.U0) :
    W0 H M U Uzero q v = kinetic M v + referenceR q + (7/75)*q 3^2 := by
  rw [W0_actual_energy, hH, hU, hUzero, reference_remainder]

theorem corrected_remainder_nonneg (q : Vec 6) (hcap : q 3^2 ≤ 56/15) :
    0 ≤ referenceR q + (7/75)*q 3^2 := by
  have h := mul_nonneg (sq_nonneg (q 3)) (sub_nonneg.mpr hcap)
  nlinarith [referenceR_floor q]

theorem W0_nonneg (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6)
    (hH : H = H0) (hU : U = referencePotential q)
    (hUzero : Uzero = RouteBGravityTwistFloor.U0)
    (hM : MassPSD M) (hcap : q 3^2 ≤ 56/15) :
    0 ≤ W0 H M U Uzero q v := by
  rw [W0_source_energy H M U Uzero q v hH hU hUzero]
  have hk : 0 ≤ kinetic M v := mul_nonneg (by norm_num) (hM v)
  linarith [corrected_remainder_nonneg q hcap]

/-- Binding an external nominal matrix to the literal reference is explicit. -/
theorem W0_from_source_nominal (Msource H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6)
    (hMsource : Msource = M0) :
    kinetic Msource v - signedGap Msource H (fun _ => M) (fun _ => q)
      (fun _ => v) (fun _ => U) Uzero 0 + (7/75)*q 3^2 = W0 H M U Uzero q v := by
  subst Msource
  rfl

def storageV (f : ℝ) (p : Vec 6) (h : ℝ) (H M : Mat 6)
    (U Uzero : ℝ) (q v : Vec 6) (c : ℝ) : ℝ :=
  f * W0 H M U Uzero q v + (∑ i, p i * q i^2) + h*c^2

theorem storageV_nonneg (f : ℝ) (p : Vec 6) (h : ℝ) (H M : Mat 6)
    (U Uzero : ℝ) (q v : Vec 6) (c : ℝ)
    (hf : 0 ≤ f) (hp : ∀ i, 0 ≤ p i) (hh : 0 ≤ h)
    (hH : H = H0) (hU : U = referencePotential q)
    (hUzero : Uzero = RouteBGravityTwistFloor.U0)
    (hM : MassPSD M) (hcap : q 3^2 ≤ 56/15) :
    0 ≤ storageV f p h H M U Uzero q v c := by
  exact add_nonneg
    (add_nonneg (mul_nonneg hf (W0_nonneg H M U Uzero q v hH hU hUzero hM hcap))
      (Finset.sum_nonneg (fun i _ => mul_nonneg (hp i) (sq_nonneg (q i)))))
    (mul_nonneg hh (sq_nonneg c))

def positionWeight (f : ℝ) (p : Vec 6) (i : Fin 6) : ℝ :=
  p i + if i = 3 then 7*f/75 else 0

theorem position_weight_identity (f : ℝ) (p q : Vec 6) :
    (∑ i, positionWeight f p i * q i^2) =
      (∑ i, p i * q i^2) + f*(7/75)*q 3^2 := by
  simp [positionWeight, add_mul, Finset.sum_add_distrib, ite_mul]
  <;> ring

/-- A full twelve-coordinate ball. The initial signed-gap audit is a premise,
not inferred from the gravity lower floor (which gives the opposite bound). -/
theorem storageV_initial_upper (f : ℝ) (p : Vec 6) (h beta : ℝ) (H M : Mat 6)
    (U Uzero : ℝ) (q v : Vec 6) (c : ℝ)
    (hf : 0 ≤ f) (hh : 0 ≤ h)
    (hball : normSq q + normSq v ≤ 9/400)
    (hgap : -(3/10000) ≤ actualSignedGap H M U Uzero q v)
    (hc : c^2 ≤ 3) (hbetaV : f/2 ≤ beta)
    (hbetaQ : ∀ i, positionWeight f p i ≤ beta) :
    storageV f p h H M U Uzero q v c ≤ (9/400)*beta + 3*f/10000 + 3*h := by
  have hb : 0 ≤ beta := by linarith
  have hk := mul_le_mul_of_nonneg_left (kinetic_M0_upper v) hf
  have hs := mul_le_mul_of_nonneg_left hgap hf
  have hcv := mul_le_mul_of_nonneg_left hc hh
  have hvb := mul_le_mul_of_nonneg_right hbetaV (normSq_nonneg v)
  have hqb : (∑ i, positionWeight f p i * q i^2) ≤ beta * normSq q := by
    unfold normSq
    rw [Finset.mul_sum]
    exact Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_right (hbetaQ i)
      (sq_nonneg (q i)))
  have hbb := mul_le_mul_of_nonneg_left hball hb
  rw [position_weight_identity] at hqb
  dsimp [storageV, W0]
  nlinarith only [hk, hs, hcv, hvb, hqb, hbb]

theorem W0_initial_upper (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6)
    (hball : normSq q + normSq v ≤ 9/400)
    (hgap : -(3/10000) ≤ actualSignedGap H M U Uzero q v) :
    W0 H M U Uzero q v ≤ 231/20000 := by
  have hb : ∀ i : Fin 6, positionWeight 1 (fun _ => 0) i ≤ (1/2 : ℝ) := by
    intro i
    unfold positionWeight
    split_ifs <;> norm_num
  have h := storageV_initial_upper 1 (fun _ => 0) 0 (1/2) H M U Uzero q v 0
    (by norm_num) (by norm_num) hball hgap (by norm_num) (by norm_num) hb
  norm_num [storageV] at h
  exact h

/-- Positive powers j=1,...,d. A constant power j=0 would need zero coefficient
to satisfy the terminal constraint. d=0 gives the zero polynomial. -/
def decayPolynomial {d : ℕ} (a : Fin d → ℝ) (t : ℝ) : ℝ :=
  ∑ j, a j * (1-t)^(j.val+1)

theorem decayPolynomial_nonneg {d : ℕ} (a : Fin d → ℝ) (t : ℝ)
    (ha : ∀ j, 0 ≤ a j) (ht : t ≤ 1) : 0 ≤ decayPolynomial a t :=
  Finset.sum_nonneg (fun j _ => mul_nonneg (ha j) (pow_nonneg (sub_nonneg.mpr ht) _))

theorem decayPolynomial_one {d : ℕ} (a : Fin d → ℝ) : decayPolynomial a 1 = 0 := by
  simp [decayPolynomial]

theorem decayPolynomial_zero {d : ℕ} (a : Fin d → ℝ) :
    decayPolynomial a 0 = ∑ j, a j := by simp [decayPolynomial]

def synthesisV {d : ℕ} (F : Fin d → ℝ) (P : Fin 6 → Fin d → ℝ)
    (C : Fin d → ℝ) (t : ℝ) (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) (c : ℝ) : ℝ :=
  storageV (decayPolynomial F t) (fun i => decayPolynomial (P i) t)
    (decayPolynomial C t) H M U Uzero q v c

def PDomain (t : ℝ) (q : Vec 6) : Prop := 0 ≤ t ∧ t ≤ 1 ∧ q 3^2 ≤ 56/15

theorem synthesisV_nonneg_on_P {d : ℕ} (F : Fin d → ℝ) (P : Fin 6 → Fin d → ℝ)
    (C : Fin d → ℝ) (t : ℝ) (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) (c : ℝ)
    (hF : ∀ j, 0 ≤ F j) (hP : ∀ i j, 0 ≤ P i j) (hC : ∀ j, 0 ≤ C j)
    (hDomain : PDomain t q) (hH : H = H0) (hU : U = referencePotential q)
    (hUzero : Uzero = RouteBGravityTwistFloor.U0) (hM : MassPSD M) :
    0 ≤ synthesisV F P C t H M U Uzero q v c :=
  storageV_nonneg _ _ _ H M U Uzero q v c
    (decayPolynomial_nonneg F t hF hDomain.2.1)
    (fun i => decayPolynomial_nonneg (P i) t (hP i) hDomain.2.1)
    (decayPolynomial_nonneg C t hC hDomain.2.1)
    hH hU hUzero hM hDomain.2.2

theorem synthesisV_terminal {d : ℕ} (F : Fin d → ℝ) (P : Fin 6 → Fin d → ℝ)
    (C : Fin d → ℝ) (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) (c : ℝ) :
    synthesisV F P C 1 H M U Uzero q v c = 0 := by
  simp [synthesisV, storageV, decayPolynomial_one]

/-- Linear initial-budget constraints in the LP's coefficient sums. -/
theorem synthesisV_initial_upper {d : ℕ} (F : Fin d → ℝ) (P : Fin 6 → Fin d → ℝ)
    (C : Fin d → ℝ) (beta : ℝ) (H M : Mat 6) (U Uzero : ℝ) (q v : Vec 6) (c : ℝ)
    (hF : ∀ j, 0 ≤ F j) (hC : ∀ j, 0 ≤ C j)
    (hball : normSq q + normSq v ≤ 9/400)
    (hgap : -(3/10000) ≤ actualSignedGap H M U Uzero q v)
    (hc : c^2 ≤ 3) (hbetaV : (∑ j, F j)/2 ≤ beta)
    (hbetaQ : ∀ i, positionWeight (∑ j, F j) (fun k => ∑ j, P k j) i ≤ beta) :
    synthesisV F P C 0 H M U Uzero q v c ≤
      (9/400)*beta + 3*(∑ j, F j)/10000 + 3*(∑ j, C j) := by
  simp only [synthesisV, decayPolynomial_zero]
  exact storageV_initial_upper _ _ _ _ H M U Uzero q v c
    (Finset.sum_nonneg (fun j _ => hF j)) (Finset.sum_nonneg (fun j _ => hC j))
    hball hgap hc hbetaV hbetaQ

end
end RouteBActualEnergyStorage

#print axioms RouteBActualEnergyStorage.W0_nonneg
#print axioms RouteBActualEnergyStorage.W0_from_source_nominal
#print axioms RouteBActualEnergyStorage.W0_initial_upper
#print axioms RouteBActualEnergyStorage.storageV_initial_upper
#print axioms RouteBActualEnergyStorage.synthesisV_nonneg_on_P
#print axioms RouteBActualEnergyStorage.synthesisV_terminal
#print axioms RouteBActualEnergyStorage.synthesisV_initial_upper
