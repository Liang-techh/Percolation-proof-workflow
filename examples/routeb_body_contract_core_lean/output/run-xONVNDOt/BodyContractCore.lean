import BodySemanticCore

set_option autoImplicit false

namespace RouteBBodyContractCore

noncomputable section

open RouteBBodySemanticCore

abbrev Vec3 := Fin 3 → ℝ
abbrev IMat := Mat 3 3
abbrev JMat := Mat 3 6

structure KinematicContract where
  origins : Fin 7 → Vec3
  axes : Fin 6 → Vec3

def contractJv (c : KinematicContract) (body : Fin 6) : JMat :=
  bodyJv c.origins c.axes body

def contractJw (c : KinematicContract) (body : Fin 6) : JMat :=
  bodyJw c.axes body

def contractMass (c : KinematicContract) (body : Fin 6)
    (mass : ℝ) (inertia : IMat) : Mat 6 6 :=
  bodyMass c.origins c.axes body mass inertia

theorem contractJv_congruent
    (c c' : KinematicContract) (body : Fin 6)
    (hOrigins : ∀ i a, c.origins i a = c'.origins i a)
    (hAxes : ∀ j a, c.axes j a = c'.axes j a) :
    contractJv c body = contractJv c' body := by
  funext a j
  by_cases h : j.val ≤ body.val
  · simp [contractJv, bodyJv, h, bodyCom, hOrigins, hAxes]
  · simp [contractJv, bodyJv, h, hOrigins, hAxes]

theorem contractJw_congruent
    (c c' : KinematicContract) (body : Fin 6)
    (hAxes : ∀ j a, c.axes j a = c'.axes j a) :
    contractJw c body = contractJw c' body := by
  funext a j
  by_cases h : j.val ≤ body.val
  · simp [contractJw, bodyJw, h, hAxes]
  · simp [contractJw, bodyJw, h, hAxes]

theorem contractMass_congruent
    (c c' : KinematicContract) (body : Fin 6)
    (mass : ℝ) (inertia : IMat)
    (hOrigins : ∀ i a, c.origins i a = c'.origins i a)
    (hAxes : ∀ j a, c.axes j a = c'.axes j a) :
    contractMass c body mass inertia = contractMass c' body mass inertia := by
  funext i j
  simp only [contractMass, bodyMass, linkMass]
  have hjv := congrFun (congrArg (fun x => x body)
    (contractJv_congruent c c' body hOrigins hAxes))
  have hjw := congrFun (congrArg (fun x => x body)
    (contractJw_congruent c c' body hAxes))
  rw [hjv, hjw]

theorem block45_contract_link4_cutoff
    (c : KinematicContract) (a : Fin 3) :
    contractJv c 3 a 4 = 0 := by
  exact block45_link4_joint5_inactive c.origins c.axes a

theorem block45_contract_link5_active
    (c : KinematicContract) (a : Fin 3) :
    contractJv c 4 a 4 =
      cross3 (c.axes 4) (fun b =>
        bodyCom c.origins 4 b - c.origins (prevOrigin 4) b) a := by
  exact block45_link5_joint5_active c.origins c.axes a

#print axioms contractJv_congruent
#print axioms contractJw_congruent
#print axioms contractMass_congruent
#print axioms block45_contract_link4_cutoff
#print axioms block45_contract_link5_active

end
end RouteBBodyContractCore
