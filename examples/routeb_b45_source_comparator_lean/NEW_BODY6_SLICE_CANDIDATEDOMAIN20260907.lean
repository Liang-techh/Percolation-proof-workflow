import NEW_BODY6_SLICE_DOMAINREPAIR20260907

set_option autoImplicit false
open scoped BigOperators

namespace NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907

noncomputable section

open NEW_BODY6_SLICE_MARGINUNIFORM20260907 NEW_BODY6_SLICE_SCHURMARGIN20260907
open NEW_BODY6_SLICE_ENTRYMARGIN20260907 NEW_BODY6_SLICE_DOMAINREPAIR20260907
open NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open RouteBO1PerBodyExactSource RouteBBodySemanticCore RouteBSourceContractAdapter

/- OPEN_UNCOMPILED. Literal exact-real transcriptions, NOT a proof that an
   arbitrary current candidate uses these predicates. See same-stem review.
   O1 consumer cell, original delivery region, and active energy domain differ. -/
def o1ConsumerCell : Set Config := {q | ∀ i, |q i| ≤ (1 / 1000 : ℝ)}

theorem zero_mem_o1_cell_attempt : (0 : Config) ∈ o1ConsumerCell := by
  intro i
  norm_num

def jointRadius : Fin 6 → ℝ :=
  ![Real.pi, Real.pi, 5 * Real.pi / 6, Real.pi, Real.pi, 2 * Real.pi]

def jointBounds (q : Config) : Prop := ∀ i, |q i| < jointRadius i

def blockP (q v : Config) : ℝ :=
  (3 / 2) * ((q 3)^2 + (q 4)^2) + (4 / 5) * ((v 3)^2 + (v 4)^2)

def deliveryStateDomain (q v : Config) : Prop :=
  jointBounds q ∧ blockP q v ≤ (28 / 5 : ℝ)

def deliveryQDomain : Set Config := {q | ∃ v : Config, deliveryStateDomain q v}

theorem joint_radius_pos_attempt (i : Fin 6) : 0 < jointRadius i := by
  fin_cases i <;> norm_num [jointRadius] <;> positivity

theorem zero_delivery_state_attempt : deliveryStateDomain 0 0 := by
  constructor
  · intro i
    simpa using joint_radius_pos_attempt i
  · norm_num [blockP]

theorem zero_mem_delivery_projection_attempt : (0 : Config) ∈ deliveryQDomain :=
  ⟨0, zero_delivery_state_attempt⟩

/- Extra initial/time/disturbance constraints do not remove this particular
   witness. These are NOT inferred to be a complete formal candidate domain. -/
def initialBall (q v : Config) : Prop :=
  (∑ i, (q i)^2) + (∑ i, (v i)^2) ≤ (9 / 400 : ℝ)

def disturbanceGraph (t w slope : ℝ) : Prop :=
  0 ≤ t ∧ t ≤ 1 ∧ slope^2 ≤ 3 ∧ w = slope * t

theorem zero_initial_and_disturbance_attempt :
    initialBall 0 0 ∧ disturbanceGraph 0 0 0 := by
  norm_num [initialBall, disturbanceGraph]

/- The active README domain is V <= 1, with circle lifts. V is an explicit
   source input: there is no silent substitution of delivery blockP for V. -/
def activeLiftedDomain (V : Config → Config → ℝ)
    (q v cosine sine : Config) : Prop :=
  V q v ≤ 1 ∧ ∀ i, (cosine i)^2 + (sine i)^2 = 1

def activeQDomain (V : Config → Config → ℝ) : Set Config :=
  {q | ∃ v cosine sine : Config, activeLiftedDomain V q v cosine sine}

theorem zero_active_lift_attempt (V : Config → Config → ℝ) (hV : V 0 0 ≤ 1) :
    activeLiftedDomain V 0 0 (fun _ => 1) 0 := by
  refine ⟨hV, ?_⟩
  intro i
  norm_num

theorem zero_mem_active_projection_attempt (V : Config → Config → ℝ)
    (hV : V 0 0 ≤ 1) : (0 : Config) ∈ activeQDomain V :=
  ⟨0, (fun _ => 1), 0, zero_active_lift_attempt V hV⟩

theorem origin_lift_has_correct_angles_attempt (i : Fin 6) :
    Real.cos ((0 : Config) i) = 1 ∧ Real.sin ((0 : Config) i) = 0 := by
  norm_num

/- It suffices to bind ONE point. Requiring all-q ExactPhysicalFamily would
   be stronger than the logical requirements of this obstruction. -/
def Body6RAtZeroBinding (R : Config → FrontBlock) : Prop :=
  R 0 = sourceCoefficient (0 : Config) (3 / 20) (1 / 60)

theorem physical_weights_attempt : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ) := by
  norm_num [SourceWeightsTarget, routeBMass, routeBInertiaScalar]

theorem family_implies_zero_binding_attempt (D : Set Config)
    (R : Config → FrontBlock) (hz : (0 : Config) ∈ D)
    (he : ExactPhysicalFamily D R) : Body6RAtZeroBinding R := by
  funext i j
  exact he 0 hz i j

theorem candidate_strict_obstruction_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock)
    (hz : (0 : Config) ∈ D) (hr : Body6RAtZeroBinding R)
    (mu : ℝ) (hmu : 0 < mu) : ¬ UniformMargin D R mu := by
  intro hu
  have hm := hu 0 hz
  change R 0 = sourceCoefficient (0 : Config) (3 / 20) (1 / 60) at hr
  rw [hr] at hm
  exact source_zero_no_positive_margin_attempt hc hw mu hmu hm

theorem minimal_candidate_obstruction_attempt (hc : CenterOffsetTarget)
    (D : Set Config) (R : Config → FrontBlock)
    (hz : (0 : Config) ∈ D) (hr : Body6RAtZeroBinding R) :
    ¬ ∃ mu : ℝ, 0 < mu ∧ UniformMargin D R mu := by
  rintro ⟨mu, hp, hu⟩
  exact candidate_strict_obstruction_attempt hc physical_weights_attempt
    D R hz hr mu hp hu

/- A documented projection contained in D suffices; no domain equality or
   finite-cell coverage theorem is needed for this one-point refutation. -/
theorem delivery_bound_candidate_obstruction_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock)
    (hD : deliveryQDomain ⊆ D) (hr : Body6RAtZeroBinding R)
    (mu : ℝ) (hmu : 0 < mu) : ¬ UniformMargin D R mu :=
  candidate_strict_obstruction_attempt hc hw D R
    (hD zero_mem_delivery_projection_attempt) hr mu hmu

theorem active_bound_candidate_obstruction_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock) (V : Config → Config → ℝ)
    (hV : V 0 0 ≤ 1) (hD : activeQDomain V ⊆ D)
    (hr : Body6RAtZeroBinding R) (mu : ℝ) (hmu : 0 < mu) :
    ¬ UniformMargin D R mu :=
  candidate_strict_obstruction_attempt hc hw D R
    (hD (zero_mem_active_projection_attempt V hV)) hr mu hmu

theorem o1_body6_strict_obstruction_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (mu : ℝ) (hmu : 0 < mu) :
    ¬ UniformMargin o1ConsumerCell
      (fun q => sourceCoefficient q (3 / 20) (1 / 60)) mu :=
  candidate_strict_obstruction_attempt hc hw o1ConsumerCell
    (fun q => sourceCoefficient q (3 / 20) (1 / 60))
    zero_mem_o1_cell_attempt rfl mu hmu

/- Exact-real M/C-force/G transcription of dhport_lib.jl, NOT Float64
   evaluation. The returned C object is Cdq (a vector), not a 6x6 C matrix.
   Mass regularizer epsMass is different from the requested Schur margin mu. -/
def epsMass : ℝ := 1 / 1000000
def fdStep : ℝ := 1 / 100000

def sourceAggregateM (q : Config) : Mat6 := fun i j =>
  (∑ b : Fin 6, sourceBodyMass q b i j) + if i = j then epsMass else 0

def sourcePotential (q : Config) : ℝ :=
  ∑ b : Fin 6, routeBMass b * (981 / 100) *
    bodyCom (sourceContract q).origins b 2

def shifted (q : Config) (k : Fin 6) (h : ℝ) : Config :=
  fun i => q i + if i = k then h else 0

def massFD (q : Config) (i j k : Fin 6) : ℝ :=
  (sourceAggregateM (shifted q k fdStep) i j -
    sourceAggregateM (shifted q k (-fdStep)) i j) / (2 * fdStep)

def sourceCForce (q v : Config) : Config := fun i =>
  ∑ j : Fin 6, ∑ k : Fin 6,
    (1 / 2) * (massFD q i j k + massFD q i k j - massFD q j k i) * v j * v k

def sourceG (q : Config) : Config := fun k =>
  (sourcePotential (shifted q k fdStep) -
    sourcePotential (shifted q k (-fdStep))) / (2 * fdStep)

/- Unfilled extensional obligations for externally supplied exact-real M/C/G.
   Hash matches are provenance only. Shifted-input and Float64 enclosures are
   additional obligations described in the review, not asserted by this type. -/
structure ExactRealMCGSourceBinding (M : Config → Mat6)
    (Cforce : Config → Config → Config) (G : Config → Config)
    (U : Config → ℝ) : Prop where
  mass : ∀ q, M q = sourceAggregateM q
  coriolisForce : ∀ q v, Cforce q v = sourceCForce q v
  gravity : ∀ q, G q = sourceG q
  potential : ∀ q, U q = sourcePotential q

/- M/C/G binding cannot manufacture a BODY6 remainder binding. A request
   bundle records both, and its refutation uses only the necessary fields. -/
structure BoundBody6Request (D : Set Config) (R : Config → FrontBlock)
    (M : Config → Mat6) (Cforce : Config → Config → Config)
    (G : Config → Config) (U : Config → ℝ) : Prop where
  zeroInDomain : (0 : Config) ∈ D
  center : CenterOffsetTarget
  weights : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)
  body6RAtZero : Body6RAtZeroBinding R
  mcg : ExactRealMCGSourceBinding M Cforce G U

theorem mcg_bound_body6_request_obstruction_attempt
    (D : Set Config) (R : Config → FrontBlock) (M : Config → Mat6)
    (Cforce : Config → Config → Config) (G : Config → Config) (U : Config → ℝ)
    (hb : BoundBody6Request D R M Cforce G U) :
    ¬ ∃ mu : ℝ, 0 < mu ∧ UniformMargin D R mu := by
  rintro ⟨mu, hp, hu⟩
  exact candidate_strict_obstruction_attempt hb.center hb.weights D R
    hb.zeroInDomain hb.body6RAtZero mu hp hu

/- No conclusion about the Schur complement of sourceAggregateM follows.
   No PSD, source admission, coverage, ODE, or compiled-Lean claim is made. -/
end
end NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907
