import NEW_P4_032_SourcePositiveTargetBinding
import NEW_P4_032_MinimalResidualBudgetAdapter

/-!
OPEN_UNCOMPILED. Minimal same-source Young allocation and P4 scalar adapter.
No Lean/Lake run, CSV importer, authenticated source, PSD or registry claim.
Keys are declared provenance, not verification of files or their semantics.
-/
set_option autoImplicit false

namespace RouteBP4032SameSourceConsumerPacket

open RouteBP4032UniformParameterBridge RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter RouteBP4032DualScaleComposition
open RouteBP4032MinimalResidualBudgetAdapter RouteBP4032NominalDirectionAudit

noncomputable section

inductive ControllerBranch where
  | fourier | dh
  deriving DecidableEq

/-- Must be frozen by the external source audit before constructing evidence. -/
structure SourceKey where
  branch : ControllerBranch
  controllerDigest : String
  storageDigest : String
  massDigest : String
  objectContract : String
  domainContract : String
  unitsContract : String

def sqNorm (v : Fin 2 → ℝ) : ℝ := v 0 ^ 2 + v 1 ^ 2

/-- Functions at one source state; lBase and port are generalized-force
vectors in the same coordinates. This is a model, not source authentication. -/
structure SourceFields (key : SourceKey) (X : Type*) where
  domain : X → Prop
  base : X → ℝ
  lBase : X → Fin 2 → ℝ
  port : X → Fin 2 → ℝ
  acceleration : X → Fin 2 → ℝ

def metric {key : SourceKey} {X : Type*} (src : SourceFields key X) (x : X) : ℝ :=
  (1402217 / 12000000) * (src.acceleration x 0)^2 +
  (200739 / 4000000) * (src.acceleration x 1)^2

def totalSq {key : SourceKey} {X : Type*} (src : SourceFields key X) (x : X) : ℝ :=
  sqNorm (fun i => src.lBase x i + src.port x i)

theorem metric_nonnegative {key : SourceKey} {X : Type*}
    (src : SourceFields key X) (x : X) : 0 ≤ metric src x := by
  unfold metric
  positivity

theorem young_two_vectors (u v : Fin 2 → ℝ) :
    sqNorm (fun i => u i + v i) ≤ 2 * sqNorm u + 2 * sqNorm v := by
  unfold sqNorm
  nlinarith [sq_nonneg (u 0 - v 0), sq_nonneg (u 1 - v 1)]

/-- A completed row interpretation, not a copy of the incomplete CSV row.
charge may be a justified conservative enlargement of the printed token.
The exact interpretation/rounding provenance remains an external obligation. -/
structure RowInterpretation (key : SourceKey) where
  csvDigest : String
  producerDigest : String
  partitionDigest : String
  physicalLine : Nat
  eta : ℚ
  theta : ℚ
  printedCharge : String
  charge : ℝ
  rhoSq : ℝ
  theta_one : theta = 1
  rho_nonnegative : 0 ≤ rhoSq
  young_charge : 2 * rhoSq ≤ charge

/-- This bound ties the selected row to the actual source functions/domain.
A matching key or hash string alone cannot construct it. -/
structure RowSourceEvidence {key : SourceKey} {X : Type*}
    (row : RowInterpretation key) (src : SourceFields key X) : Prop where
  port_bound : ∀ x, src.domain x → sqNorm (src.port x) ≤ row.rhoSq * metric src x

theorem charge_nonnegative {key : SourceKey} (row : RowInterpretation key) :
    0 ≤ row.charge := by
  have h := row.young_charge
  have hr := row.rho_nonnegative
  linarith

theorem total_residual_bound {key : SourceKey} {X : Type*}
    (row : RowInterpretation key) (src : SourceFields key X)
    (e : RowSourceEvidence row src) (x : X) (hx : src.domain x) :
    totalSq src x ≤ 2 * sqNorm (src.lBase x) + row.charge * metric src x := by
  have hy := young_two_vectors (src.lBase x) (src.port x)
  have hp := e.port_bound x hx
  have hc := mul_le_mul_of_nonneg_right row.young_charge (metric_nonnegative src x)
  dsimp [totalSq]
  nlinarith

/-- Three uniform bounds are a sufficient rectangular allocation route.
Their derivation (including any energy estimate) is not reconstructed here. -/
structure UniformBounds {key : SourceKey} {X : Type*} (src : SourceFields key X) where
  baseFloor : ℝ
  residualSqCap : ℝ
  metricCap : ℝ
  base_lower : ∀ x, src.domain x → baseFloor ≤ src.base x
  residual_upper : ∀ x, src.domain x → sqNorm (src.lBase x) ≤ residualSqCap
  metric_upper : ∀ x, src.domain x → metric src x ≤ metricCap

/-- Correlations can be retained by constructing this directly, without
separate uniform caps. target is in the unscaled source scalar units. -/
structure Allocation {key : SourceKey} {X : Type*}
    (row : RowInterpretation key) (src : SourceFields key X) (target : ℝ) : Prop where
  positive : 0 < target
  bound : ∀ x, src.domain x →
    target + 2 * sqNorm (src.lBase x) + row.charge * metric src x ≤ src.base x

/-- The minimal mathematical packet fixes one row, source object and target.
Neither member can be replaced by a similarly named record from another key. -/
structure ConsumerPacket {key : SourceKey} {X : Type*}
    (row : RowInterpretation key) (src : SourceFields key X) (target : ℝ) : Prop where
  row_source : RowSourceEvidence row src
  allocation : Allocation row src target

def allocationFromUniform {key : SourceKey} {X : Type*}
    (row : RowInterpretation key) (src : SourceFields key X) (u : UniformBounds src)
    (target : ℝ) (hp : 0 < target)
    (ha : target + 2 * u.residualSqCap + row.charge * u.metricCap ≤ u.baseFloor) :
    Allocation row src target where
  positive := hp
  bound := by
    intro x hx
    have hb := u.base_lower x hx
    have hr := u.residual_upper x hx
    have hm := mul_le_mul_of_nonneg_left (u.metric_upper x hx) (charge_nonnegative row)
    linarith

theorem allocated_source_floor {key : SourceKey} {X : Type*}
    (row : RowInterpretation key) (src : SourceFields key X)
    (e : RowSourceEvidence row src) (target : ℝ) (a : Allocation row src target) :
    ∀ x, src.domain x → target ≤ src.base x - totalSq src x := by
  intro x hx
  have ht := total_residual_bound row src e x hx
  have ha := a.bound x hx
  linarith

/-- Minimal actual P4 object identities. nu is a fixed positive scalar
normalization supplied separately, not inferred from sf or theta.
The P4 residual here is the TOTAL squared force residual, not A_up,
not ||lBase|| alone, and not an acceleration residual. -/
structure P4Binding {key : SourceKey} {X Z : Type*} (src : SourceFields key X)
    (f : ParameterField Z) (m : MarginField Z) (s : ScaleFields Z)
    (embed : X → Z) (nu : ℝ) : Prop where
  covered : ∀ x, src.domain x → f.domain (embed x)
  residual_eq : ∀ x, src.domain x → f.residual (embed x) = totalSq src x
  nominal_eq : ∀ x, src.domain x → m.nominal (embed x) = nu * src.base x
  gain_scale_eq : ∀ x, src.domain x →
    m.gain (embed x) * (s.residual (embed x)).value = nu

theorem allocated_P4_target {key : SourceKey} {X Z : Type*}
    (row : RowInterpretation key) (src : SourceFields key X)
    (e : RowSourceEvidence row src) (target : ℝ) (a : Allocation row src target)
    (f : ParameterField Z) (m : MarginField Z) (s : ScaleFields Z)
    (embed : X → Z) (nu : ℝ) (hnu : 0 < nu)
    (b : P4Binding src f m s embed nu)
    (comparison : ScaledComparison f m (residualValues s)) :
    ∀ x, src.domain x → 0 < nu * target ∧ nu * target ≤ m.margin (embed x) := by
  intro x hx
  refine ⟨mul_pos hnu a.positive, ?_⟩
  have hs := allocated_source_floor row src e target a x hx
  have hscaled := mul_le_mul_of_nonneg_left hs (le_of_lt hnu)
  have hc := comparison.lower (embed x) (b.covered x hx)
  simp only [residualValues, ← mul_assoc] at hc
  rw [b.nominal_eq x hx, b.residual_eq x hx, b.gain_scale_eq x hx] at hc
  calc
    nu * target ≤ nu * (src.base x - totalSq src x) := hscaled
    _ = nu * src.base x - nu * totalSq src x := by ring
    _ ≤ m.margin (embed x) := hc

/-- Optional BODY6/front route. It is NOT needed by allocated_P4_target.
This field must be proved if a caller claims that the front expression is
the same nominal used above; front scale is still distinct from beta. -/
structure FrontFactorization {key : SourceKey} {X Z : Type*}
    (src : SourceFields key X) (d : RemainderField Z) (s : ScaleFields Z)
    (embed : X → Z) (nu : ℝ) : Prop where
  body_eq : ∀ x, src.domain x → bodyExpression d s (embed x) = nu * src.base x

theorem front_equals_bound_nominal {key : SourceKey} {X Z : Type*}
    (src : SourceFields key X) (f : ParameterField Z) (m : MarginField Z)
    (d : RemainderField Z) (s : ScaleFields Z) (embed : X → Z) (nu : ℝ)
    (b : P4Binding src f m s embed nu) (front : FrontFactorization src d s embed nu) :
    ∀ x, src.domain x → bodyExpression d s (embed x) = m.nominal (embed x) := by
  intro x hx
  exact (front.body_eq x hx).trans (b.nominal_eq x hx).symm

end
end RouteBP4032SameSourceConsumerPacket
