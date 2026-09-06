import ActualStorage

set_option autoImplicit false
open scoped BigOperators

namespace RouteBActualStorageDerivative
open RouteBSignedGap RouteBActualEnergyStorage
noncomputable section

/-- K+H0 uses the literal reference Hessian; K remains a source input. -/
def stiffness (K : Mat 6) : Mat 6 := fun i j => K i j + H0 i j

def W0rate (K D : Mat 6) (G q v eta : Vec 6) (w : ℝ) : ℝ :=
  -dot v (mv (stiffness K) q) - quad D v + dot v G * w +
    (14/75) * q 3 * v 3 + dot v eta

theorem mv_stiffness (K : Mat 6) (q : Vec 6) :
    mv (stiffness K) q = fun i => mv K q i + mv H0 q i := by
  ext i
  simp only [mv, stiffness, add_mul, Finset.sum_add_distrib]

/-- The finite M0 delta terms cancel; no final derivative identity is assumed. -/
theorem delta_cancellation (v a0 delta eta : Vec 6) :
    dot v (mv M0 (fun i => a0 i + delta i)) -
      (dot v (mv M0 delta) - dot v eta) = dot v (mv M0 a0) + dot v eta := by
  simp only [dot, mv, mul_add, Finset.sum_add_distrib]
  ring

theorem nominal_power (K D : Mat 6) (G q v a0 : Vec 6) (w : ℝ)
    (nominal : ∀ i, mv M0 a0 i = -mv (stiffness K) q i - mv D v i + G i * w) :
    dot v (mv M0 a0) = -dot v (mv (stiffness K) q) - quad D v + dot v G * w := by
  have hn := funext nominal
  rw [hn]
  simp only [dot, quad, mul_add, mul_sub, mul_neg,
    Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_neg_distrib,
    Finset.sum_mul, mul_assoc]

/-- Modular composition with the PREVIOUS signed-gap derivative, not W0dot. -/
theorem hasDerivAt_W0_of_signedGap (K D : Mat 6) (G : Vec 6)
    (M : ℝ → Mat 6) (U : ℝ → ℝ) (q v : ℝ → Vec 6) (Uzero t w : ℝ)
    (a0 delta eta : Vec 6)
    (hq : ∀ i, HasDerivAt (fun s => q s i) (v t i) t)
    (hv : ∀ i, HasDerivAt (fun s => v s i) (a0 i + delta i) t)
    (hgap : HasDerivAt (signedGap M0 H0 M q v U Uzero)
      (dot (v t) (mv M0 delta) - dot (v t) eta) t)
    (nominal : ∀ i, mv M0 a0 i =
      -mv (stiffness K) (q t) i - mv D (v t) i + G i * w) :
    HasDerivAt (fun s => W0 H0 (M s) (U s) Uzero (q s) (v s))
      (W0rate K D G (q t) (v t) eta w) t := by
  have hk := hasDerivAt_kinetic_const M0 v (fun i => a0 i + delta i) t hv M0_symmetric
  have hc := ((hq 3).pow 2).const_mul (7/75 : ℝ)
  have hh := (hk.sub hgap).add hc
  change HasDerivAt (fun s => kinetic M0 (v s) -
    signedGap M0 H0 M q v U Uzero s + (7/75 : ℝ) * q s 3^2) _ t
  convert hh using 1 <;> try rfl
  unfold W0rate
  rw [delta_cancellation, nominal_power K D G (q t) (v t) a0 w nominal]
  ring

/-- Source data at the actual state. The only dynamics premises are kinematics,
source derivatives, actual force balance, and explicit SAME-state nominal balance.
Neither a gap derivative nor a storage derivative is a field. -/
structure SourceAt (K D : Mat 6) (G : Vec 6) (M : Vec 6 → Mat 6) (U : Vec 6 → ℝ)
    (q v : ℝ → Vec 6) (t w : ℝ) where
  a0 : Vec 6
  delta : Vec 6
  eta : Vec 6
  gravity : Vec 6
  DM : Fin 6 → Fin 6 → Vec 6 →L[ℝ] ℝ
  DU : Vec 6 →L[ℝ] ℝ
  T : Fin 6 → Fin 6 → Fin 6 → ℝ
  mass_symmetric : Symmetric (M (q t))
  qdot : ∀ i, HasDerivAt (fun s => q s i) (v t i) t
  vdot : ∀ i, HasDerivAt (fun s => v s i) (a0 i + delta i) t
  mass_derivative : ∀ i j, HasFDerivAt (fun x => M x i j) (DM i j) (q t)
  tensor_binding : ∀ i j x, DM i j x = ∑ k, T k i j * x k
  potential_derivative : HasFDerivAt U DU (q t)
  gravity_binding : ∀ x, DU x = dot x gravity
  actual : ∀ i, mv (M (q t)) (fun j => a0 j + delta j) i +
    RouteBChristoffelPower.christoffelForce T (v t) i + gravity i =
      -mv K (q t) i - mv D (v t) i + G i * w + eta i
  nominal : ∀ i, mv M0 a0 i = -mv (stiffness K) (q t) i - mv D (v t) i + G i * w

/-- Full source-derived result, invoking the cached finite kinetic/source theorem. -/
theorem hasDerivAt_W0_from_source (K D : Mat 6) (G : Vec 6)
    (M : Vec 6 → Mat 6) (U : Vec 6 → ℝ) (q v : ℝ → Vec 6) (Uzero t w : ℝ)
    (source : SourceAt K D G M U q v t w) :
    HasDerivAt (fun s => W0 H0 (M (q s)) (U (q s)) Uzero (q s) (v s))
      (W0rate K D G (q t) (v t) source.eta w) t := by
  have hn : ∀ i, mv M0 source.a0 i + mv H0 (q t) i =
      -mv K (q t) i - mv D (v t) i + G i * w := by
    intro i
    rw [source.nominal, mv_stiffness]
    dsimp only
    ring
  have hg := hasDerivAt_signedGap_from_source M0 H0 M U source.DM source.DU q v Uzero t
    source.T (fun i => source.a0 i + source.delta i) source.a0 source.gravity
    (fun i => -mv K (q t) i - mv D (v t) i + G i * w) source.eta
    M0_symmetric H0_symmetric source.mass_symmetric source.qdot source.vdot
    source.mass_derivative source.tensor_binding source.potential_derivative
    source.gravity_binding source.actual hn
  have hdelta : (fun i => source.a0 i + source.delta i - source.a0 i) = source.delta := by
    ext i
    ring
  rw [hdelta] at hg
  exact hasDerivAt_W0_of_signedGap K D G (fun s => M (q s)) (fun s => U (q s))
    q v Uzero t w source.a0 source.delta source.eta source.qdot source.vdot hg source.nominal

/-- Differentiate every actual term in the six-coordinate weighted square sum. -/
theorem hasDerivAt_position_sum (p q : ℝ → Vec 6) (pd v : Vec 6) (t : ℝ)
    (hp : ∀ i, HasDerivAt (fun s => p s i) (pd i) t)
    (hq : ∀ i, HasDerivAt (fun s => q s i) (v i) t) :
    HasDerivAt (fun s => ∑ i, p s i * q s i^2)
      (∑ i, (pd i * q t i^2 + 2 * p t i * q t i * v i)) t := by
  have hh := HasDerivAt.fun_sum (u := Finset.univ) (fun i _ => (hp i).mul ((hq i).pow 2))
  convert hh using 1 <;> try rfl
  apply Finset.sum_congr rfl
  intro i _
  ring

def storageRate (K D : Mat 6) (G : Vec 6) (M : Mat 6) (U Uzero : ℝ)
    (q v eta : Vec 6) (w f fd : ℝ) (p pd : Vec 6) (hd c : ℝ) : ℝ :=
  fd * W0 H0 M U Uzero q v + f * W0rate K D G q v eta w +
    (∑ i, (pd i * q i^2 + 2 * p i * q i * v i)) + hd * c^2

/-- Product-rule and finite-sum composition for the ACTUAL imported storageV.
This directly obtains W0dot from source; it never assumes the final rate. -/
theorem hasDerivAt_storageV_from_source (K D : Mat 6) (G : Vec 6)
    (M : Vec 6 → Mat 6) (U : Vec 6 → ℝ) (q v : ℝ → Vec 6) (Uzero t w : ℝ)
    (source : SourceAt K D G M U q v t w)
    (f h c : ℝ → ℝ) (p : ℝ → Vec 6) (fd hd : ℝ) (pd : Vec 6)
    (hf : HasDerivAt f fd t) (hh : HasDerivAt h hd t)
    (hp : ∀ i, HasDerivAt (fun s => p s i) (pd i) t)
    (hc : HasDerivAt c 0 t) :
    HasDerivAt (fun s => storageV (f s) (p s) (h s) H0 (M (q s)) (U (q s))
      Uzero (q s) (v s) (c s))
      (storageRate K D G (M (q t)) (U (q t)) Uzero (q t) (v t) source.eta
        w (f t) fd (p t) pd hd (c t)) t := by
  have hW := hasDerivAt_W0_from_source K D G M U q v Uzero t w source
  have hP := hasDerivAt_position_sum p q pd (v t) t hp source.qdot
  have hC := hh.mul (hc.pow 2)
  have hvv := ((hf.mul hW).add hP).add hC
  convert hvv using 1 <;> try rfl
  simp [storageRate]

end
end RouteBActualStorageDerivative

#print axioms RouteBActualStorageDerivative.delta_cancellation
#print axioms RouteBActualStorageDerivative.nominal_power
#print axioms RouteBActualStorageDerivative.hasDerivAt_W0_of_signedGap
#print axioms RouteBActualStorageDerivative.hasDerivAt_W0_from_source
#print axioms RouteBActualStorageDerivative.hasDerivAt_position_sum
#print axioms RouteBActualStorageDerivative.hasDerivAt_storageV_from_source
