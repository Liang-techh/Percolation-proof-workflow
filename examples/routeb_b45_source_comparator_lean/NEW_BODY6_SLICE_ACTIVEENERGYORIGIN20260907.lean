import NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907

set_option autoImplicit false
open scoped BigOperators

namespace NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907
noncomputable section

open NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907
open NEW_BODY6_SLICE_MARGINUNIFORM20260907 NEW_BODY6_SLICE_SCHURMARGIN20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907
open RouteBO1PerBodyExactSource

/- OPEN_UNCOMPILED. These are explicit expressions and conditional bindings.
   The active external candidate is NOT silently redefined or normalized. -/
def kineticAt (M : Config → Mat6) (q v : Config) : ℝ :=
  (1 / 2) * ∑ i : Fin 6, ∑ j : Fin 6, M q i j * v i * v j

def controllerAt (kp linear q : Config) : ℝ :=
  (1 / 2) * (∑ i : Fin 6, kp i * (q i)^2) + (∑ i : Fin 6, linear i * q i)

def normalizedEnergy (M : Config → Mat6) (U : Config → ℝ)
    (kp linear q v : Config) : ℝ :=
  kineticAt M q v + U q - U 0 + controllerAt kp linear q

def offsetEnergy (M : Config → Mat6) (U : Config → ℝ)
    (kp linear : Config) (beta : ℝ) (q v : Config) : ℝ :=
  normalizedEnergy M U kp linear q v + beta

theorem normalized_origin_attempt (M : Config → Mat6) (U : Config → ℝ)
    (kp linear : Config) : normalizedEnergy M U kp linear 0 0 = 0 := by
  simp [normalizedEnergy, kineticAt, controllerAt]

theorem offset_origin_attempt (M : Config → Mat6) (U : Config → ℝ)
    (kp linear : Config) (beta : ℝ) : offsetEnergy M U kp linear beta 0 0 = beta := by
  simp [offsetEnergy, normalized_origin_attempt]

/- Derivative identities do not determine beta; sublevel membership does. -/
theorem offset_origin_admissible_iff_attempt (M : Config → Mat6) (U : Config → ℝ)
    (kp linear : Config) (beta : ℝ) :
    offsetEnergy M U kp linear beta 0 0 ≤ 1 ↔ beta ≤ 1 := by
  rw [offset_origin_attempt]

/- Literal gravity expression in energy_power_rewrite and regenerated DH
   gain audit. Zero-based angles q[1..4] correspond to joints 2..5. -/
def auditedGravity (q : Config) : ℝ :=
  (762237 / 200000) * Real.cos (q 1) +
  (242307 / 200000) *
    (Real.cos (q 1) * Real.cos (q 2) - Real.sin (q 1) * Real.sin (q 2)) +
  (20601 / 400000) *
    (Real.cos (q 1) * Real.cos (q 2) - Real.sin (q 1) * Real.sin (q 2)) *
    Real.cos (q 4) -
  (20601 / 400000) *
    (Real.sin (q 1) * Real.cos (q 2) + Real.cos (q 1) * Real.sin (q 2)) *
    Real.cos (q 3) * Real.sin (q 4)

def auditedRawEnergy (M : Config → Mat6) (kp linear q v : Config) : ℝ :=
  kineticAt M q v + auditedGravity q + controllerAt kp linear q

def auditedShiftedEnergy (M : Config → Mat6) (kp linear q v : Config) : ℝ :=
  auditedRawEnergy M kp linear q v + (205029 / 40000)

theorem raw_origin_attempt (M : Config → Mat6) (kp linear : Config) :
    auditedRawEnergy M kp linear 0 0 = (2029689 / 400000 : ℝ) := by
  norm_num [auditedRawEnergy, kineticAt, auditedGravity, controllerAt]

theorem shifted_origin_attempt (M : Config → Mat6) (kp linear : Config) :
    auditedShiftedEnergy M kp linear 0 0 = (4079979 / 400000 : ℝ) := by
  rw [auditedShiftedEnergy, raw_origin_attempt]
  norm_num

/- This rejects the specified lifted ORIGIN, not every point in its
   configuration projection (which existentially quantifies velocity). -/
theorem raw_lifted_origin_rejected_attempt (M : Config → Mat6) (kp linear : Config) :
    ¬ activeLiftedDomain (auditedRawEnergy M kp linear) 0 0 (fun _ => 1) 0 := by
  intro h
  have hV := h.1
  rw [raw_origin_attempt] at hV
  norm_num at hV

theorem shifted_lifted_origin_rejected_attempt (M : Config → Mat6) (kp linear : Config) :
    ¬ activeLiftedDomain (auditedShiftedEnergy M kp linear) 0 0 (fun _ => 1) 0 := by
  intro h
  have hV := h.1
  rw [shifted_origin_attempt] at hV
  norm_num at hV

/- Rational DH origin COM-height ledger; relation to sourceContract origins
   is NOT claimed here. The review records the exact quarter-turn calculation. -/
def originCOMHeight : Fin 6 → ℝ := ![1/20, 41/200, 31/100, 81/200, 1/2, 107/200]
def originPotentialLedger : ℝ :=
  ∑ b : Fin 6, routeBMass b * (981/100) * originCOMHeight b

theorem origin_potential_ledger_attempt :
    originPotentialLedger = (3108789 / 400000 : ℝ) := by
  norm_num [originPotentialLedger, routeBMass, originCOMHeight, Fin.sum_univ_succ]

theorem origin_potential_offset_attempt :
    originPotentialLedger - auditedGravity 0 = (10791 / 4000 : ℝ) := by
  rw [origin_potential_ledger_attempt]
  norm_num [auditedGravity]

/- A source-selected normalized expression has the correct circle witness.
   Normalization alone proves neither PSD nor energy/flow validity. -/
theorem normalized_lifted_origin_attempt (M : Config → Mat6) (U : Config → ℝ)
    (kp linear : Config) :
    activeLiftedDomain (normalizedEnergy M U kp linear) 0 0 (fun _ => 1) 0 := by
  apply zero_active_lift_attempt
  rw [normalized_origin_attempt]
  norm_num

/- Only the pointwise V binding is needed for this origin witness. Neither
   the reviewed scripts nor a power identity supplies this binding by itself. -/
theorem bound_active_origin_attempt (V : Config → Config → ℝ)
    (M : Config → Mat6) (U : Config → ℝ) (kp linear : Config)
    (hV : V 0 0 = normalizedEnergy M U kp linear 0 0) :
    (0 : Config) ∈ activeQDomain V := by
  apply zero_mem_active_projection_attempt
  rw [hV, normalized_origin_attempt]
  norm_num

theorem bound_active_body6_obstruction_attempt (V : Config → Config → ℝ)
    (M : Config → Mat6) (U : Config → ℝ) (kp linear : Config)
    (hV : V 0 0 = normalizedEnergy M U kp linear 0 0)
    (D : Set Config) (hD : activeQDomain V ⊆ D)
    (R : Config → FrontBlock) (hr : Body6RAtZeroBinding R)
    (hc : CenterOffsetTarget) :
    ¬ ∃ mu : ℝ, 0 < mu ∧ UniformMargin D R mu :=
  minimal_candidate_obstruction_attempt hc D R
    (hD (bound_active_origin_attempt V M U kp linear hV)) hr

/- No actual-candidate origin membership is asserted without hV/hD.
   No result about full regularized M/C/G follows from the BODY6 obstruction. -/
end
end NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907
