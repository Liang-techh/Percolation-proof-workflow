import Mathlib

namespace RouteBP5InitialReferenceBridge

abbrev Vec2 := Fin 2 → ℝ
abbrev Vec4 := Fin 4 → ℝ

/-- Split typed state for the current P5 reference seam.  The D/B partition is
made explicit here; binding it to the deployed six-coordinate ordering remains
a separate source/interface theorem. -/
structure SplitState where
  qD : Vec4
  vD : Vec4
  qB : Vec2
  vB : Vec2

/-- Position-square budget over the explicit D/B partition. -/
def qEnergy (x : SplitState) : ℝ :=
  (∑ i, (x.qD i) ^ 2) + ∑ i, (x.qB i) ^ 2

/-- Velocity-square budget over the explicit D/B partition. -/
def vEnergy (x : SplitState) : ℝ :=
  (∑ i, (x.vD i) ^ 2) + ∑ i, (x.vB i) ^ 2

/-- Remote-coordinate part of the P5-098 weighted budget. -/
noncomputable def pD (x : SplitState) : ℝ :=
  (3 / 2 : ℝ) * ∑ i, (x.qD i) ^ 2 +
    (4 / 5 : ℝ) * ∑ i, (x.vD i) ^ 2

/-- Two-channel block part of the weighted budget. -/
noncomputable def pB (q v : Vec2) : ℝ :=
  (3 / 2 : ℝ) * ∑ i, (q i) ^ 2 +
    (4 / 5 : ℝ) * ∑ i, (v i) ^ 2

/-- Ordinary full-state budget expressed through the same explicit partition. -/
noncomputable def pFull (x : SplitState) : ℝ :=
  (3 / 2 : ℝ) * qEnergy x + (4 / 5 : ℝ) * vEnergy x

/-- Hybrid budget: keep the actual D coordinates and replace only the B block
by the selected nominal reference coordinates. -/
noncomputable def hybridBudget (x : SplitState) (qbar vbar : Vec2) : ℝ :=
  pD x + pB qbar vbar

theorem qEnergy_nonneg (x : SplitState) : 0 ≤ qEnergy x := by
  unfold qEnergy
  positivity

theorem vEnergy_nonneg (x : SplitState) : 0 ≤ vEnergy x := by
  unfold vEnergy
  positivity

/-- Exact partition identity underlying the initial-reference reduction. -/
theorem pFull_split (x : SplitState) :
    pFull x = pD x + pB x.qB x.vB := by
  simp [pFull, pD, pB, qEnergy, vEnergy]
  ring

/-- If the nominal block initial state is the actual block initial state, the
hybrid budget is exactly the ordinary full-state budget. -/
theorem hybridBudget_eq_full_of_block_match
    (x : SplitState) (qbar vbar : Vec2)
    (hq : qbar = x.qB) (hv : vbar = x.vB) :
    hybridBudget x qbar vbar = pFull x := by
  subst qbar
  subst vbar
  simpa [hybridBudget] using (pFull_split x).symm

/-- Pure scalar arithmetic for the already-recorded initial ball. -/
theorem weighted_initial_ball_bound
    (Q V : ℝ)
    (_hQ : 0 ≤ Q) (hV : 0 ≤ V)
    (hball : Q + V ≤ (9 / 400 : ℝ)) :
    (3 / 2 : ℝ) * Q + (4 / 5 : ℝ) * V ≤ (27 / 800 : ℝ) := by
  nlinarith

theorem pFull_le_27_over_800_of_ball
    (x : SplitState)
    (hball : qEnergy x + vEnergy x ≤ (9 / 400 : ℝ)) :
    pFull x ≤ (27 / 800 : ℝ) := by
  exact weighted_initial_ball_bound
    (qEnergy x) (vEnergy x) (qEnergy_nonneg x) (vEnergy_nonneg x) hball

theorem pFull_lt_28_over_5_of_ball
    (x : SplitState)
    (hball : qEnergy x + vEnergy x ≤ (9 / 400 : ℝ)) :
    pFull x < (28 / 5 : ℝ) := by
  have h := pFull_le_27_over_800_of_ball x hball
  nlinarith

theorem hybridBudget_le_27_over_800_of_initial_match
    (x : SplitState) (qbar vbar : Vec2)
    (hq : qbar = x.qB) (hv : vbar = x.vB)
    (hball : qEnergy x + vEnergy x ≤ (9 / 400 : ℝ)) :
    hybridBudget x qbar vbar ≤ (27 / 800 : ℝ) := by
  rw [hybridBudget_eq_full_of_block_match x qbar vbar hq hv]
  exact pFull_le_27_over_800_of_ball x hball

theorem hybridBudget_lt_28_over_5_of_initial_match
    (x : SplitState) (qbar vbar : Vec2)
    (hq : qbar = x.qB) (hv : vbar = x.vB)
    (hball : qEnergy x + vEnergy x ≤ (9 / 400 : ℝ)) :
    hybridBudget x qbar vbar < (28 / 5 : ℝ) := by
  rw [hybridBudget_eq_full_of_block_match x qbar vbar hq hv]
  exact pFull_lt_28_over_5_of_ball x hball

/-- Minimal state carrying a graph-dependent field.  `graphValue` stands for a
quantity that must be recomputed from the same deterministic source semantics
when the B block is replaced. -/
structure AnchoredState (Remote Block Graph : Type*) where
  remote : Remote
  qB : Block
  vB : Block
  graphValue : Graph

/-- Recompute the graph-dependent field after substituting the reference block. -/
def anchor
    {Remote Block Graph : Type*}
    (graph : Remote → Block → Block → Graph)
    (x : AnchoredState Remote Block Graph)
    (qbar vbar : Block) : AnchoredState Remote Block Graph where
  remote := x.remote
  qB := qbar
  vB := vbar
  graphValue := graph x.remote qbar vbar

/-- Same block values plus the same deterministic graph semantics make the
initial anchor literally the original state. -/
theorem anchor_eq_self_of_block_match
    {Remote Block Graph : Type*}
    (graph : Remote → Block → Block → Graph)
    (x : AnchoredState Remote Block Graph)
    (qbar vbar : Block)
    (hq : qbar = x.qB) (hv : vbar = x.vB)
    (hgraph : x.graphValue = graph x.remote x.qB x.vB) :
    anchor graph x qbar vbar = x := by
  cases x
  simp_all [anchor]

/-- Centered residual built from the exact same observable on the actual and
anchored states. -/
def centeredResidual
    {Remote Block Graph : Type*}
    (graph : Remote → Block → Block → Graph)
    (obs : AnchoredState Remote Block Graph → ℝ)
    (x : AnchoredState Remote Block Graph)
    (qbar vbar : Block) : ℝ :=
  obs x - obs (anchor graph x qbar vbar)

theorem centeredResidual_eq_zero_of_initial_match
    {Remote Block Graph : Type*}
    (graph : Remote → Block → Block → Graph)
    (obs : AnchoredState Remote Block Graph → ℝ)
    (x : AnchoredState Remote Block Graph)
    (qbar vbar : Block)
    (hq : qbar = x.qB) (hv : vbar = x.vB)
    (hgraph : x.graphValue = graph x.remote x.qB x.vB) :
    centeredResidual graph obs x qbar vbar = 0 := by
  have ha := anchor_eq_self_of_block_match graph x qbar vbar hq hv hgraph
  simp [centeredResidual, ha]

/-- Initial anchor equality does not by itself set the reference residual to
zero: the bias remains `obs x - lbar` until a separate nominal graph theorem
identifies `lbar`. -/
noncomputable def anchorBias
    {Remote Block Graph : Type*}
    (graph : Remote → Block → Block → Graph)
    (obs : AnchoredState Remote Block Graph → ℝ)
    (x : AnchoredState Remote Block Graph)
    (qbar vbar : Block) (lbar : ℝ) : ℝ :=
  obs (anchor graph x qbar vbar) - lbar

theorem anchorBias_eq_actual_minus_lbar_of_initial_match
    {Remote Block Graph : Type*}
    (graph : Remote → Block → Block → Graph)
    (obs : AnchoredState Remote Block Graph → ℝ)
    (x : AnchoredState Remote Block Graph)
    (qbar vbar : Block) (lbar : ℝ)
    (hq : qbar = x.qB) (hv : vbar = x.vB)
    (hgraph : x.graphValue = graph x.remote x.qB x.vB) :
    anchorBias graph obs x qbar vbar lbar = obs x - lbar := by
  rw [anchorBias, anchor_eq_self_of_block_match graph x qbar vbar hq hv hgraph]

/-- Division-free pointwise nominal residual interface.  `forcing` is the
right-hand side and `dynamics` is the complete mass+damping+stiffness side. -/
def nominalResidual (forcing dynamics : Vec2) : Vec2 :=
  fun i => forcing i - dynamics i

/-- A source-bound nominal graph equality implies the nominal residual is zero.
This theorem deliberately does not manufacture the graph equality. -/
theorem nominalResidual_eq_zero_of_graph
    (forcing dynamics : Vec2)
    (hgraph : ∀ i, forcing i = dynamics i) :
    nominalResidual forcing dynamics = 0 := by
  funext i
  simp [nominalResidual, hgraph i]

/-- Scalar pointwise model used only to make the missing-acceleration boundary
explicit. -/
noncomputable def scalarNominalResidual
    (q v a w M D B g : ℝ) : ℝ :=
  g * w - (M * a + D * v + B * q)

/-- Same q/v/input values need not determine `lbar` if acceleration/graph data
is not fixed.  Here only acceleration changes, and the residual changes from
0 to -1 exactly. -/
theorem same_qv_input_different_acceleration_residual :
    scalarNominalResidual 0 0 0 0 1 0 0 0 = 0 ∧
      scalarNominalResidual 0 0 1 0 1 0 0 0 = -1 := by
  norm_num [scalarNominalResidual]

#print axioms qEnergy_nonneg
#print axioms vEnergy_nonneg
#print axioms pFull_split
#print axioms hybridBudget_eq_full_of_block_match
#print axioms weighted_initial_ball_bound
#print axioms pFull_le_27_over_800_of_ball
#print axioms pFull_lt_28_over_5_of_ball
#print axioms hybridBudget_le_27_over_800_of_initial_match
#print axioms hybridBudget_lt_28_over_5_of_initial_match
#print axioms anchor_eq_self_of_block_match
#print axioms centeredResidual_eq_zero_of_initial_match
#print axioms anchorBias_eq_actual_minus_lbar_of_initial_match
#print axioms nominalResidual_eq_zero_of_graph
#print axioms same_qv_input_different_acceleration_residual

end RouteBP5InitialReferenceBridge
