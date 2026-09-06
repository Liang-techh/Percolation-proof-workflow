import DHPowerBinding
import ChristoffelPower

open scoped BigOperators

namespace RouteBMechanicalAssembly

open RouteBDHPowerBinding RouteBChristoffelPower

theorem mechanical_derivative_assembly
    (Ma : Mat) (T : Fin 6 → Fin 6 → Fin 6 → ℝ) (v a gA : Vec)
    (dK dU dUc dE : ℝ)
    (hK : dK = (∑ i, v i * matVec Ma a i) +
      (1 / 2 : ℝ) * ∑ i, v i * (∑ j, massRate T v i j * v j))
    (hU : dU = ∑ i, v i * gA i)
    (hE : dE = dK + dU + dUc) :
    dE = (∑ i, v i * (matVec Ma a i + christoffelForce T v i + gA i)) + dUc := by
  have hc := christoffel_power_identity T v
  simp only [mul_add, Finset.sum_add_distrib]
  linarith

/- Parent assembly: hC is proved from the tensor formula, not supplied as
   an additional physics hypothesis. Kinetic/potential differentiation and
   the component bounds remain explicit obligations. -/
theorem full_power_bound_from_mechanical_derivatives
    (Ma Mi : Mat) (T : Fin 6 → Fin 6 → Fin 6 → ℝ)
    (kp q g0 v a tauI cI gA gI eps : Vec) (w dK dU dUc dE : ℝ)
    (hK : dK = (∑ i, v i * matVec Ma a i) +
      (1 / 2 : ℝ) * ∑ i, v i * (∑ j, massRate T v i j * v j))
    (hU : dU = ∑ i, v i * gA i)
    (hE : dE = dK + dU + dUc)
    (hUc : dUc = ∑ i, (kp i * q i - g0 i) * v i)
    (herr : ∀ i, |forceError Ma Mi a (controller kp q v g0 w)
      tauI (christoffelForce T v) cI gA gI i| ≤ eps i) :
    dE ≤ (631227 / 1086800 : ℝ) * w ^ 2 +
      ∑ i, eps i ^ 2 / (2 * RouteBSupplyCore.damping i) := by
  exact implemented_energy_bound_of_component_enclosures
    Ma Mi kp q g0 v a tauI (christoffelForce T v) cI gA gI eps w dUc dE hUc
    (mechanical_derivative_assembly Ma T v a gA dK dU dUc dE hK hU hE) herr

#print axioms mechanical_derivative_assembly
#print axioms full_power_bound_from_mechanical_derivatives

end RouteBMechanicalAssembly
