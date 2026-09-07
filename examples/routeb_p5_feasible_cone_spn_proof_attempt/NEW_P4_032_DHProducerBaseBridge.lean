import NEW_P4_032_SameSourceConsumerPacket

/-!
OPEN_UNCOMPILED. Exact compact-DH branch formula and conditional producer
port bridge. These are source transcriptions, not authenticated true-DH
equations or certified interval coverage. No Lean/Lake or registry action.
-/
set_option autoImplicit false

namespace RouteBP4032DHProducerBaseBridge

open RouteBP4032SameSourceConsumerPacket RouteBP4032BlockDefects

noncomputable section

structure State where
  angles : Fin 4 → ℝ -- q2,q3,q4,q5, in this order
  velocity : Fin 2 → ℝ -- dq4,dq5
  acceleration : BVec -- a4,a5
  distalCorrection : DVec
  portResidual : BVec
  disturbance : ℝ
  time : ℝ

/-- Compact descriptor DH branch: force coordinates after multiplication
by I4=1/5 and I5=1/10, then subtraction of M0_BB*a_B. -/
def dhLBase (x : State) : BVec := ![
  -(3 / 4) * x.angles 2 - (4 / 5) * x.velocity 0 +
    (1 / 5) * x.disturbance + (1 / 100) * x.angles 3 -
    (350003 / 3000000) * x.acceleration 0,
  -(29 / 50) * x.angles 3 - (13 / 20) * x.velocity 1 +
    (1 / 10) * x.disturbance + (1 / 200) * x.angles 2 -
    (200739 / 4000000) * x.acceleration 1]

def producerMetric (x : State) : ℝ :=
  (1402217 / 12000000) * x.acceleration 0 ^ 2 +
  (200739 / 4000000) * x.acceleration 1 ^ 2

/-- Intended exact domain of the producer's four-angle ball contraction.
Floating-point cell endpoints and their coverage still require reification. -/
def producerGeometry (x : State) : Prop :=
  x.angles 0 ^ 2 + x.angles 1 ^ 2 + x.angles 2 ^ 2 + x.angles 3 ^ 2 ≤ 56 / 15 ∧
  -(5 * Real.pi / 6) ≤ x.angles 1 ∧ x.angles 1 ≤ 5 * Real.pi / 6

def blockP (x : State) : ℝ :=
  (3 / 2) * (x.angles 2 ^ 2 + x.angles 3 ^ 2) +
  (4 / 5) * (x.velocity 0 ^ 2 + x.velocity 1 ^ 2)

structure MassFields where
  tailMass : State → DD
  tailInverse : State → DD
  deltaCross : State → DB
  portCross : State → BD

def source (key : SourceKey) (D : State → Prop) (base : State → ℝ) :
    SourceFields key State where
  domain := D
  base := base
  lBase := dhLBase
  port := State.portResidual
  acceleration := State.acceleration

theorem source_metric_eq (key : SourceKey) (D : State → Prop) (base : State → ℝ)
    (x : State) : metric (source key D base) x = producerMetric x := rfl

/-- Actual matrices must be identified with one regularized mass source.
The zero-defect descriptor equation is an explicit premise, not inferred
from the compact branch name or from the full physical equations. -/
structure ProducerChain {key : SourceKey} (row : RowInterpretation key)
    (mass : MassFields) (D : State → Prop) : Prop where
  dh_branch : key.branch = .dh
  eta_eq : row.eta = 28 / 5
  geometry : ∀ x, D x → producerGeometry x
  inverse : ∀ x, D x → mass.tailInverse x * mass.tailMass x = (1 : DD)
  descriptor : ∀ x, D x →
    mass.tailMass x *ᵥ x.distalCorrection + mass.deltaCross x *ᵥ x.acceleration = 0
  port_eq : ∀ x, D x →
    x.portResidual - mass.portCross x *ᵥ x.distalCorrection = 0
  operator_bound : ∀ x, D x →
    sqNorm (Rport (mass.portCross x) (mass.tailInverse x) (mass.deltaCross x)
      *ᵥ x.acceleration) ≤ row.rhoSq * producerMetric x

/-- Reuses the existing exact negative-sign Rport identity. -/
def rowEvidenceFromProducer {key : SourceKey} (row : RowInterpretation key)
    (mass : MassFields) (D : State → Prop) (base : State → ℝ)
    (h : ProducerChain row mass D) : RowSourceEvidence row (source key D base) where
  port_bound := by
    intro x hx
    change sqNorm x.portResidual ≤ row.rhoSq * producerMetric x
    rw [zero_defect_port_identity (mass.tailMass x) (mass.tailInverse x)
      (mass.deltaCross x) (mass.portCross x) x.distalCorrection x.acceleration
      x.portResidual (h.inverse x hx) (h.descriptor x hx) (h.port_eq x hx)]
    exact h.operator_bound x hx

/-- The remaining concrete base inequality, retaining correlations. -/
structure BaseDominance (D : State → Prop) (base : State → ℝ)
    (charge target : ℝ) : Prop where
  positive : 0 < target
  lower : ∀ x, D x →
    target + 2 * sqNorm (dhLBase x) + charge * producerMetric x ≤ base x

def packetFromProducer {key : SourceKey} (row : RowInterpretation key)
    (mass : MassFields) (D : State → Prop) (base : State → ℝ) (target : ℝ)
    (h : ProducerChain row mass D) (b : BaseDominance D base row.charge target) :
    ConsumerPacket row (source key D base) target where
  row_source := rowEvidenceFromProducer row mass D base h
  allocation := ⟨b.positive, b.lower⟩

/-- A formal acceleration ray, not a demonstrated ODE/descriptor trajectory. -/
def accelerationRay (z : ℝ) : State where
  angles := 0
  velocity := 0
  acceleration := ![z, 0]
  distalCorrection := 0
  portResidual := 0
  disturbance := 0
  time := 0

theorem ray_base_residual (z : ℝ) :
    sqNorm (dhLBase (accelerationRay z)) = (350003 / 3000000 : ℝ)^2 * z^2 := by
  norm_num [sqNorm, dhLBase, accelerationRay] <;> ring

theorem ray_metric (z : ℝ) :
    producerMetric (accelerationRay z) = (1402217 / 12000000 : ℝ) * z^2 := by
  norm_num [producerMetric, accelerationRay]

theorem ray_producer_geometry (z : ℝ) : producerGeometry (accelerationRay z) := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [accelerationRay]
  · change -(5 * Real.pi / 6) ≤ (0 : ℝ)
    nlinarith [Real.pi_pos]
  · change (0 : ℝ) ≤ 5 * Real.pi / 6
    positivity

/-- Every allowed ray point demands this exact quadratic growth of base. -/
theorem required_base_on_ray (D : State → Prop) (base : State → ℝ)
    (charge target z : ℝ) (b : BaseDominance D base charge target)
    (hx : D (accelerationRay z)) :
    target + (2 * (350003 / 3000000 : ℝ)^2 +
      charge * (1402217 / 12000000)) * z^2 ≤ base (accelerationRay z) := by
  have hb := b.lower (accelerationRay z) hx
  rw [ray_base_residual, ray_metric] at hb
  nlinarith

/-- The angle-only producer geometry cannot supply a positive base budget. -/
theorem zero_base_ray_obstruction (D : State → Prop) (base : State → ℝ)
    (charge target : ℝ) (hc : 0 ≤ charge) (hx : D (accelerationRay 1))
    (hb : base (accelerationRay 1) ≤ 0) : ¬ BaseDominance D base charge target := by
  intro b
  have hr := required_base_on_ray D base charge target 1 b hx
  have hp := b.positive
  norm_num at hr
  nlinarith

def remoteAnglePoint : State :=
  { accelerationRay 0 with angles := ![2, 0, 0, 0] }

/-- p45 alone does not cover the producer's four-angle ball. -/
theorem block_domain_not_producer_domain :
    blockP remoteAnglePoint ≤ (28 / 5 : ℝ) ∧ ¬ producerGeometry remoteAnglePoint := by
  norm_num [blockP, producerGeometry, remoteAnglePoint, accelerationRay]

end
end RouteBP4032DHProducerBaseBridge
