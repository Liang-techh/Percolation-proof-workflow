import CoupledResolvent
import ChristoffelPower
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pi
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

set_option autoImplicit false
open scoped BigOperators

namespace RouteBSignedGap
noncomputable section

abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Mat (n : ℕ) := Fin n → Fin n → ℝ
def dot {n : ℕ} (x y : Vec n) : ℝ := ∑ i, x i * y i
def mv {n : ℕ} (M : Mat n) (x : Vec n) : Vec n := fun i => ∑ j, M i j * x j
def quad {n : ℕ} (M : Mat n) (x : Vec n) : ℝ := dot x (mv M x)
def kinetic {n : ℕ} (M : Mat n) (x : Vec n) : ℝ := (1/2 : ℝ) * quad M x
def Symmetric {n : ℕ} (M : Mat n) : Prop := ∀ i j, M i j = M j i

theorem dot_mv_symm {n : ℕ} (M : Mat n) (x y : Vec n) (hM : Symmetric M) :
    dot x (mv M y) = dot y (mv M x) := by
  simp only [dot, mv, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  rw [hM j i]
  ring

/-- Differentiate the actual finite double sum; no assumed kinetic power equality. -/
theorem hasDerivAt_bilinear {n : ℕ} (M : ℝ → Mat n) (x y : ℝ → Vec n)
    (Md : Mat n) (xd yd : Vec n) (t : ℝ)
    (hM : ∀ i j, HasDerivAt (fun s => M s i j) (Md i j) t)
    (hx : ∀ i, HasDerivAt (fun s => x s i) (xd i) t)
    (hy : ∀ i, HasDerivAt (fun s => y s i) (yd i) t) :
    HasDerivAt (fun s => dot (x s) (mv (M s) (y s)))
      (dot xd (mv (M t) (y t)) + dot (x t) (mv Md (y t)) +
        dot (x t) (mv (M t) yd)) t := by
  have h := HasDerivAt.fun_sum (u := Finset.univ) (fun i _ =>
    HasDerivAt.fun_sum (u := Finset.univ) (fun j _ =>
      (hx i).mul ((hM i j).mul (hy j))))
  convert h using 1 <;> try rfl
  · funext s
    simp only [dot, mv, Finset.mul_sum, Pi.mul_apply]
  · simp only [dot, mv, Finset.mul_sum, ← Finset.sum_add_distrib, Pi.mul_apply]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring

theorem hasDerivAt_kinetic {n : ℕ} (M : ℝ → Mat n) (v : ℝ → Vec n)
    (Md : Mat n) (a : Vec n) (t : ℝ)
    (hM : ∀ i j, HasDerivAt (fun s => M s i j) (Md i j) t)
    (hv : ∀ i, HasDerivAt (fun s => v s i) (a i) t)
    (hsym : Symmetric (M t)) :
    HasDerivAt (fun s => kinetic (M s) (v s))
      (dot (v t) (mv (M t) a) + (1/2 : ℝ) * quad Md (v t)) t := by
  have h := (hasDerivAt_bilinear M v v Md a a t hM hv hv).const_mul (1/2 : ℝ)
  rw [dot_mv_symm (M t) a (v t) hsym] at h
  convert h using 1 <;> try rfl
  dsimp [quad]
  ring

theorem hasDerivAt_kinetic_const {n : ℕ} (M : Mat n) (v : ℝ → Vec n)
    (a : Vec n) (t : ℝ) (hv : ∀ i, HasDerivAt (fun s => v s i) (a i) t)
    (hsym : Symmetric M) :
    HasDerivAt (fun s => kinetic M (v s)) (dot (v t) (mv M a)) t := by
  simpa [quad, dot, mv] using hasDerivAt_kinetic (fun _ => M) v
    (fun _ _ => 0) a t (fun i j => hasDerivAt_const t (M i j)) hv hsym

/-- U is the actual potential along q; this gap and its remainder are signed. -/
def signedGap {n : ℕ} (M0 H0 : Mat n) (M : ℝ → Mat n)
    (q v : ℝ → Vec n) (U : ℝ → ℝ) (Uzero : ℝ) (t : ℝ) : ℝ :=
  kinetic M0 (v t) - kinetic (M t) (v t) -
    (U t - Uzero - kinetic H0 (q t))

/-- a0 is the nominal acceleration at the SAME q,v, with the SAME drive.
The analytic Coriolis force is the tensor formula, so its power cancellation
is proved by the cached Christoffel theorem, not passed in as a hypothesis. -/
theorem hasDerivAt_signedGap {n : ℕ} (M0 H0 : Mat n) (M : ℝ → Mat n)
    (q v : ℝ → Vec n) (U : ℝ → ℝ) (Uzero t : ℝ)
    (T : Fin n → Fin n → Fin n → ℝ) (a a0 G drive eta : Vec n)
    (hM0 : Symmetric M0) (hH0 : Symmetric H0) (hMs : Symmetric (M t))
    (hq : ∀ i, HasDerivAt (fun s => q s i) (v t i) t)
    (hv : ∀ i, HasDerivAt (fun s => v s i) (a i) t)
    (hM : ∀ i j, HasDerivAt (fun s => M s i j)
      (RouteBChristoffelPower.massRate T (v t) i j) t)
    (hU : HasDerivAt U (dot (v t) G) t)
    (actual : ∀ i, mv (M t) a i + RouteBChristoffelPower.christoffelForce T (v t) i
      + G i = drive i + eta i)
    (nominal : ∀ i, mv M0 a0 i + mv H0 (q t) i = drive i) :
    HasDerivAt (signedGap M0 H0 M q v U Uzero)
      (dot (v t) (mv M0 (fun i => a i - a0 i)) - dot (v t) eta) t := by
  have hn := hasDerivAt_kinetic_const M0 v a t hv hM0
  have ha := hasDerivAt_kinetic M v _ a t hM hv hMs
  have hp := hasDerivAt_kinetic_const H0 q (v t) t hq hH0
  rw [dot_mv_symm H0 (q t) (v t) hH0] at hp
  have hc := RouteBChristoffelPower.christoffel_power_identity T (v t)
  change dot (v t) (RouteBChristoffelPower.christoffelForce T (v t)) =
    (1/2 : ℝ) * quad (RouteBChristoffelPower.massRate T (v t)) (v t) at hc
  rw [← hc] at ha
  have h := (hn.sub ha).sub ((hU.sub_const Uzero).sub hp)
  have balance : dot (v t) (mv M0 a) -
      (dot (v t) (mv (M t) a) +
        dot (v t) (RouteBChristoffelPower.christoffelForce T (v t))) -
      (dot (v t) G - dot (v t) (mv H0 (q t))) =
      dot (v t) (mv M0 (fun i => a i-a0 i)) - dot (v t) eta := by
    simp only [dot, mv, mul_sub,
      ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_sub_distrib]
    have hai := actual i
    have hni := nominal i
    dsimp [mv] at hai hni
    have hai' := congrArg (fun x : ℝ => v t i * x) hai
    have hni' := congrArg (fun x : ℝ => v t i * x) hni
    nlinarith only [hai', hni']
  rw [balance] at h
  exact h

/-- Cached implementation defect identity supplies actual balance with eta once. -/
theorem implemented_actual_balance (Ma Mi : Mat 6)
    (a tauA tauI cA cI gA gI : Vec 6) :
    ∀ i, mv Ma a i + cA i + gA i = tauA i +
      RouteBDHPowerBinding.forceError Ma Mi a tauA tauI cA cI gA gI i :=
  fun i => RouteBDHPowerBinding.implemented_force_identity Ma Mi a tauA tauI cA cI gA gI i

/-- Reuse the exact current-state resolvent; eta is already inside its residual. -/
theorem same_state_residual (M M0 H0 : Mat 6) (q a a0 C G drive eta : Vec 6)
    (actual : ∀ i, mv M a i + C i + G i = drive i + eta i)
    (nominal : ∀ i, mv M0 a0 i + mv H0 q i = drive i) :
    ∀ i, mv M (fun j => a j - a0 j) i =
      RouteBCoupledResolvent.nonlinearForce M M0 a0 (mv H0 q) C G eta i :=
  RouteBCoupledResolvent.acceleration_free_resolvent M M0 a a0 (mv H0 q) C G eta drive
    actual nominal

#print axioms hasDerivAt_bilinear
#print axioms hasDerivAt_kinetic
#print axioms hasDerivAt_signedGap
#print axioms implemented_actual_balance
#print axioms same_state_residual

end
end RouteBSignedGap
