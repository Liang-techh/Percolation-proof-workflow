import B45MinimalInterface
import DescriptorTermsAdapter

set_option autoImplicit false

namespace RouteBB45SchurResidualRepair

noncomputable section

open RouteBB45MinimalInterface
open RouteBB45DescriptorTermsAdapter
open RouteBB45ResidualDecomposition

structure Binding
    (I : DescriptorSchurInterface) (x : State)
    (q v : Vec2) (w : ℝ) (t : DescriptorResidualTerms) where
  aB_eq : I.aB x = t.accelerationB
  massBB_eq : I.MBB x (I.aB x) = t.massBB t.accelerationB
  remote_eq : I.MBD x (I.aD x) = t.remoteMassAcceleration
  coriolis_eq : I.coriolis x = t.coriolis
  gravity_eq : I.gravityDefect x = t.gravity
  fd_eq : I.fdRemainder x = t.gravityAtZero
  force_eq : sourceDescriptorRhs t = expectedSourceForce q v w t

theorem exact_descriptor_residual
    (I : DescriptorSchurInterface) (x : State)
    (q v : Vec2) (w : ℝ) (t : DescriptorResidualTerms)
    (h : Binding I x q v w t) :
    blockResidual q v w t.accelerationB = descriptorResidualTotal q t := by
  apply blockResidual_eq_descriptorResidualTotal q v w t
  exact h.force_eq.symm

theorem schur_remainder_bound
    (I : DescriptorSchurInterface) (x : State)
    (q v : Vec2) (w : ℝ) (t : DescriptorResidualTerms)
    (gamma : ℝ) (h : Binding I x q v w t)
    (hledger : sqNorm (descriptorResidualTotal q t) ≤ gamma) :
    sqNorm (blockResidual q v w t.accelerationB) ≤ gamma := by
  rw [exact_descriptor_residual I x q v w t h]
  exact hledger

theorem remote_term_transport
    (I : DescriptorSchurInterface) (x : State)
    (q v : Vec2) (w : ℝ) (t : DescriptorResidualTerms)
    (h : Binding I x q v w t) :
    sqNorm (rhoRemote t.remoteMassAcceleration) ≤ I.gammaRemote := by
  rw [← h.remote_eq]
  simpa [rhoRemote] using I.remote_schur_bound x

#print axioms exact_descriptor_residual
#print axioms schur_remainder_bound
#print axioms remote_term_transport

end
end RouteBB45SchurResidualRepair
