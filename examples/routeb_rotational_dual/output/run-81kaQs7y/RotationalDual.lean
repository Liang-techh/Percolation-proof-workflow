import Mathlib.Tactic

set_option autoImplicit false
open scoped BigOperators

namespace RouteBRotationalDual
noncomputable section

abbrev Vec := Fin 6 → ℝ
abbrev V3 := Fin 3 → ℝ
def dot3 (x y : V3) : ℝ := ∑ k, x k * y k
def sq3 (x : V3) : ℝ := dot3 x x
def dot6 (x y : Vec) : ℝ := ∑ i, x i * y i
def norm6 (x : Vec) : ℝ := dot6 x x
def weight : Vec := ![1/3, 1/5, 7/60, 1/15, 1/30, 1/60]
def prev (u : Fin 6 → V3) : Fin 6 → V3 :=
  ![fun _ => 0, u 0, u 1, u 2, u 3, u 4]
def nextForce (f : Vec) (z : Fin 6 → V3) : Fin 6 → V3 :=
  ![fun k => f 1*z 1 k, fun k => f 2*z 2 k,
    fun k => f 3*z 3 k, fun k => f 4*z 4 k,
    fun k => f 5*z 5 k, fun _ => 0]
def dual (f : Vec) (z : Fin 6 → V3) (i : Fin 6) : V3 :=
  fun k => f i*z i k-nextForce f z i k
def rotational (u : Fin 6 → V3) : ℝ := ∑ i, weight i * sq3 (u i)
def dualCost (f : Vec) (z : Fin 6 → V3) : ℝ := ∑ i, sq3 (dual f z i)/weight i
def forceMetric (f : Vec) : ℝ :=
  3*f 0^2+8*f 1^2+(95/7)*f 2^2+(165/7)*f 3^2+45*f 4^2+90*f 5^2-10*f 1*f 2

theorem scalar_completion (a u w : ℝ) (hw : 0 < w) :
    2*a*u-w*u^2 ≤ a^2/w := by
  apply (le_div_iff₀ hw).2
  nlinarith [sq_nonneg (a-w*u)]

theorem vector_completion (a u : V3) (w : ℝ) (hw : 0 < w) :
    2*dot3 a u-w*sq3 u ≤ sq3 a/w := by
  have h0 := scalar_completion (a 0) (u 0) w hw
  have h1 := scalar_completion (a 1) (u 1) w hw
  have h2 := scalar_completion (a 2) (u 2) w hw
  simp only [pow_two] at h0 h1 h2
  simp only [sq3,dot3,Fin.sum_univ_three]
  simp only [add_div]
  nlinarith

theorem work_telescopes (f v : Vec) (z u : Fin 6 → V3)
    (unit : ∀ i, sq3 (z i)=1)
    (link : ∀ i k, u i k-prev u i k=v i*z i k) :
    dot6 f v = ∑ i, dot3 (dual f z i) (u i) := by
  have each (i : Fin 6) : f i*v i = ∑ k, f i*z i k*(u i k-prev u i k) := by
    simp_rw [link]
    calc
      f i*v i = f i*v i*sq3 (z i) := by rw [unit]; ring
      _ = _ := by simp [sq3,dot3,Fin.sum_univ_three]; ring
  unfold dot6
  simp_rw [each]
  simp [dual,nextForce,prev,dot3,Fin.sum_univ_six,Fin.sum_univ_three]
  ring

theorem dual_cost_explicit (f : Vec) (z : Fin 6 → V3)
    (unit : ∀ i, sq3 (z i)=1)
    (h01 : dot3 (z 0) (z 1)=0) (h12 : dot3 (z 1) (z 2)=1)
    (h23 : dot3 (z 2) (z 3)=0) (h34 : dot3 (z 3) (z 4)=0)
    (h45 : dot3 (z 4) (z 5)=0) :
    dualCost f z = forceMetric f := by
  have expansion : dualCost f z =
      3*(f 0^2*sq3 (z 0)+f 1^2*sq3 (z 1)-2*f 0*f 1*dot3 (z 0) (z 1))+
      5*(f 1^2*sq3 (z 1)+f 2^2*sq3 (z 2)-2*f 1*f 2*dot3 (z 1) (z 2))+
      (60/7)*(f 2^2*sq3 (z 2)+f 3^2*sq3 (z 3)-2*f 2*f 3*dot3 (z 2) (z 3))+
      15*(f 3^2*sq3 (z 3)+f 4^2*sq3 (z 4)-2*f 3*f 4*dot3 (z 3) (z 4))+
      30*(f 4^2*sq3 (z 4)+f 5^2*sq3 (z 5)-2*f 4*f 5*dot3 (z 4) (z 5))+
      60*f 5^2*sq3 (z 5) := by
    simp [dualCost,dual,nextForce,weight,sq3,dot3,Fin.sum_univ_six,Fin.sum_univ_three]
    ring
  rw [expansion]
  simp_rw [unit,h01,h12,h23,h34,h45]
  unfold forceMetric
  ring

theorem fenchel_rotational (f v : Vec) (z u : Fin 6 → V3)
    (hwork : dot6 f v = ∑ i, dot3 (dual f z i) (u i)) :
    2*dot6 f v-rotational u ≤ dualCost f z := by
  have each (i : Fin 6) : 2*dot3 (dual f z i) (u i)-weight i*sq3 (u i) ≤
      sq3 (dual f z i)/weight i := by
    apply vector_completion
    fin_cases i <;> norm_num [weight]
  have h := Finset.sum_le_sum (s:=Finset.univ) (fun i _ => each i)
  simpa only [Finset.sum_sub_distrib,← Finset.mul_sum,← hwork,rotational,dualCost] using h

theorem metric_upper (f : Vec) : forceMetric f ≤ 90*norm6 f := by
  have h := sq_nonneg (f 1+f 2)
  have h0 := sq_nonneg (f 0)
  have h1 := sq_nonneg (f 1)
  have h2 := sq_nonneg (f 2)
  have h3 := sq_nonneg (f 3)
  have h4 := sq_nonneg (f 4)
  norm_num [forceMetric,norm6,dot6,Fin.sum_univ_six]
  nlinarith

/- Given the established dual work inequality, no inverse computation or
   free-acceleration relaxation is needed for these source-independent gates. -/
theorem coercivity_from_dual (v : Vec) (mass : ℝ)
    (hdual : ∀ f, 2*dot6 f v-mass ≤ forceMetric f) :
    norm6 v/90 ≤ mass := by
  let f : Vec := fun i => v i/90
  have h := hdual f
  have hb := metric_upper f
  have hw : dot6 f v = norm6 v/90 := by
    simp [f,dot6,norm6,Fin.sum_univ_six]; ring
  have hn : norm6 f = norm6 v/8100 := by
    simp [f,dot6,norm6,Fin.sum_univ_six]; ring
  rw [hw] at h
  rw [hn] at hb
  linarith

theorem regularized_coercivity (v : Vec) (massBase mass : ℝ)
    (hbase : norm6 v/90 ≤ massBase)
    (hreg : massBase+norm6 v/1000000 ≤ mass) :
    (100009/9000000 : ℝ)*norm6 v ≤ mass := by linarith

theorem force_balance_bound (f a : Vec) (mass : ℝ)
    (hdual : 2*dot6 f a-mass ≤ forceMetric f)
    (balance : mass=dot6 f a) : dot6 f a ≤ forceMetric f := by
  linarith

theorem dh_axes_mass_dual (f v : Vec) (z u : Fin 6 → V3) (mass : ℝ)
    (unit : ∀ i, sq3 (z i)=1)
    (link : ∀ i k, u i k-prev u i k=v i*z i k)
    (h01 : dot3 (z 0) (z 1)=0) (h12 : dot3 (z 1) (z 2)=1)
    (h23 : dot3 (z 2) (z 3)=0) (h34 : dot3 (z 3) (z 4)=0)
    (h45 : dot3 (z 4) (z 5)=0) (hM : rotational u ≤ mass) :
    2*dot6 f v-mass ≤ forceMetric f := by
  have hw := work_telescopes f v z u unit link
  have hf := fenchel_rotational f v z u hw
  rw [dual_cost_explicit f z unit h01 h12 h23 h34 h45] at hf
  linarith

def lowerAction (v : Vec) : Vec :=
  ![v 0/3, (19/117)*v 1+(7/117)*v 2,
    (7/117)*v 1+(56/585)*v 2, (7/165)*v 3, v 4/45, v 5/90]
def lowerMetric (v : Vec) : ℝ :=
  v 0^2/3+(19/117)*v 1^2+(56/585)*v 2^2+(7/165)*v 3^2+
    v 4^2/45+v 5^2/90+(14/117)*v 1*v 2

theorem exact_anisotropic_mass_lower (v : Vec) (mass : ℝ)
    (hdual : ∀ f, 2*dot6 f v-mass ≤ forceMetric f) : lowerMetric v ≤ mass := by
  have h := hdual (lowerAction v)
  have hd : dot6 (lowerAction v) v = lowerMetric v := by
    simp [dot6,lowerAction,lowerMetric,Fin.sum_univ_six]; ring
  have hq : forceMetric (lowerAction v) = lowerMetric v := by
    simp [forceMetric,lowerAction,lowerMetric]; ring
  rw [hd,hq] at h
  linarith

theorem acceleration4_energy (a : Vec) (mass : ℝ)
    (hdual : ∀ f, 2*dot6 f a-mass ≤ forceMetric f) :
    a 3^2 ≤ (165/7 : ℝ)*mass := by
  let f : Vec := ![0,0,0,(7/165)*a 3,0,0]
  have h := hdual f
  have hd : dot6 f a = (7/165)*a 3^2 := by
    simp [dot6,f,Fin.sum_univ_six]; ring
  have hq : forceMetric f = (7/165)*a 3^2 := by simp [forceMetric,f]; ring
  rw [hd,hq] at h
  linarith

theorem acceleration5_energy (a : Vec) (mass : ℝ)
    (hdual : ∀ f, 2*dot6 f a-mass ≤ forceMetric f) :
    a 4^2 ≤ (45 : ℝ)*mass := by
  let f : Vec := ![0,0,0,0,a 4/45,0]
  have h := hdual f
  have hd : dot6 f a = a 4^2/45 := by simp [dot6,f,Fin.sum_univ_six]; ring
  have hq : forceMetric f = a 4^2/45 := by simp [forceMetric,f]; ring
  rw [hd,hq] at h
  linarith

/- The exact MBB-Mref structure proved by the source coefficient audit is
   diag((147/800000)*sin(q5)^2,0). This is that component only, not total e. -/
theorem reference_mass_mismatch_cost (a : Vec) (mass : ℝ) (s : ℝ)
    (hs : s^2 ≤ 1) (hdual : ∀ f, 2*dot6 f a-mass ≤ forceMetric f) :
    ((147/800000 : ℝ)*s^2*a 3)^2/(8/5 : ℝ) ≤
      (101871 / 204800000000 : ℝ)*mass := by
  have ha := acceleration4_energy a mass hdual
  have hs0 := sq_nonneg s
  have hs4 : (s^2)^2 ≤ 1 := by nlinarith
  have hprod := mul_le_mul_of_nonneg_right hs4 (sq_nonneg (a 3))
  nlinarith

#print axioms work_telescopes
#print axioms dual_cost_explicit
#print axioms fenchel_rotational
#print axioms metric_upper
#print axioms coercivity_from_dual
#print axioms regularized_coercivity
#print axioms force_balance_bound
#print axioms dh_axes_mass_dual
#print axioms exact_anisotropic_mass_lower
#print axioms acceleration4_energy
#print axioms acceleration5_energy
#print axioms reference_mass_mismatch_cost
end
end RouteBRotationalDual
