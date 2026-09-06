import Mathlib

set_option autoImplicit false

/-!
Minimal, deliberately conditional first-exit/domain bridge for Route-B P8.

The declarations separate four interfaces:

1. a local estimate whose hypotheses include membership in the source domain;
2. existence/attainment of a first exit;
3. passage of strict-prefix estimates to the candidate exit and exclusion of
   the boundary there;
4. an ODE continuation criterion after domain closure.

No numerical probe, finite list of reachsets, or `coverageComplete = false`
receipt supplies any of these interfaces.
-/

namespace RouteBFirstExitBridge

def InHorizon (T t : ℝ) : Prop := 0 ≤ t ∧ t ≤ T

def DomainSafeThrough {State : Type*}
    (domain : State → Prop) (trajectory : ℝ → State) (T : ℝ) : Prop :=
  ∀ t, InHorizon T t → domain (trajectory t)

def LocalCertificate {State : Type*}
    (domain : State → Prop) (conclusion : State → Prop)
    (trajectory : ℝ → State) (T : ℝ) : Prop :=
  ∀ t, InHorizon T t → domain (trajectory t) → conclusion (trajectory t)

/-- A domain-local estimate becomes global on the horizon only after domain
closure has been supplied independently. -/
theorem localCertificate_of_domainSafe {State : Type*}
    {domain conclusion : State → Prop} {trajectory : ℝ → State} {T : ℝ}
    (hSafe : DomainSafeThrough domain trajectory T)
    (hLocal : LocalCertificate domain conclusion trajectory T) :
    ∀ t, InHorizon T t → conclusion (trajectory t) := by
  intro t ht
  exact hLocal t ht (hSafe t ht)

/-- Data obtained from continuity/compactness when a trajectory really has an
attained first exit. The prefix is strict: the local source estimate is never
assumed at or after the candidate exit. -/
structure FirstExitWitness {State : Type*}
    (domain boundary : State → Prop) (trajectory : ℝ → State) (T : ℝ) where
  time : ℝ
  positive : 0 < time
  inHorizon : InHorizon T time
  insideBefore : ∀ s, 0 ≤ s → s < time → domain (trajectory s)
  onBoundary : boundary (trajectory time)

/-- This is the topological first-exit theorem still required from the concrete
Route-B state domain and continuous trajectory. -/
def FirstExitAttainment {State : Type*}
    (domain boundary : State → Prop) (trajectory : ℝ → State) (T : ℝ) : Prop :=
  domain (trajectory 0) →
    ¬ DomainSafeThrough domain trajectory T →
      Nonempty (FirstExitWitness domain boundary trajectory T)

/-- This interface contains the analytic limit step: estimates valid on every
strict pre-exit prefix must imply an interior-margin predicate at the attained
candidate exit. Continuity/absolute continuity is not hidden in the assembly
theorem; it belongs in an implementation of this premise. -/
def PrefixLimitMargin {State : Type*}
    (domain interiorMargin : State → Prop)
    (trajectory : ℝ → State) (T : ℝ) : Prop :=
  ∀ τ, InHorizon T τ →
    (∀ s, 0 ≤ s → s < τ → domain (trajectory s)) →
      interiorMargin (trajectory τ)

def BoundarySeparated {State : Type*}
    (boundary interiorMargin : State → Prop) : Prop :=
  ∀ y, interiorMargin y → ¬ boundary y

/-- Pure first-exit contradiction. It does not prove first-exit attainment,
the prefix limit estimate, or any ODE continuation result. -/
theorem domainSafeThrough_of_firstExit {State : Type*}
    {domain boundary interiorMargin : State → Prop}
    {trajectory : ℝ → State} {T : ℝ}
    (hInitial : domain (trajectory 0))
    (hExit : FirstExitAttainment domain boundary trajectory T)
    (hPrefix : PrefixLimitMargin domain interiorMargin trajectory T)
    (hSeparated : BoundarySeparated boundary interiorMargin) :
    DomainSafeThrough domain trajectory T := by
  by_contra hUnsafe
  obtain ⟨exit⟩ := hExit hInitial hUnsafe
  have hMargin : interiorMargin (trajectory exit.time) :=
    hPrefix exit.time exit.inHorizon exit.insideBefore
  exact (hSeparated (trajectory exit.time) hMargin) exit.onBoundary

/-- `available t` records that the concrete maximal solution is defined with
the required regularity at time `t`. -/
def ExistsThrough (available : ℝ → Prop) (T : ℝ) : Prop :=
  ∀ t, InHorizon T t → available t

/-- A concrete ODE adapter must prove this from local existence/uniqueness plus
an extension theorem (for example, local Lipschitzness and compact containment).
Domain closure alone is not treated as an existence theorem. -/
def ContinuationCriterion {State : Type*}
    (domain : State → Prop) (trajectory : ℝ → State)
    (available : ℝ → Prop) (T : ℝ) : Prop :=
  DomainSafeThrough domain trajectory T → ExistsThrough available T

theorem existsThrough_of_domainSafe_and_continuation {State : Type*}
    {domain : State → Prop} {trajectory : ℝ → State}
    {available : ℝ → Prop} {T : ℝ}
    (hSafe : DomainSafeThrough domain trajectory T)
    (hContinuation : ContinuationCriterion domain trajectory available T) :
    ExistsThrough available T :=
  hContinuation hSafe

/-- Honest P8 assembly: local estimates, domain closure, and continuation are
three separate outputs and retain their separate premises. -/
theorem p8_firstExit_domain_continuation_assembly {State : Type*}
    {domain boundary interiorMargin conclusion : State → Prop}
    {trajectory : ℝ → State} {available : ℝ → Prop} {T : ℝ}
    (hInitial : domain (trajectory 0))
    (hExit : FirstExitAttainment domain boundary trajectory T)
    (hPrefix : PrefixLimitMargin domain interiorMargin trajectory T)
    (hSeparated : BoundarySeparated boundary interiorMargin)
    (hLocal : LocalCertificate domain conclusion trajectory T)
    (hContinuation : ContinuationCriterion domain trajectory available T) :
    DomainSafeThrough domain trajectory T ∧
      (∀ t, InHorizon T t → conclusion (trajectory t)) ∧
      ExistsThrough available T := by
  have hSafe : DomainSafeThrough domain trajectory T :=
    domainSafeThrough_of_firstExit hInitial hExit hPrefix hSeparated
  exact ⟨hSafe, localCertificate_of_domainSafe hSafe hLocal,
    existsThrough_of_domainSafe_and_continuation hSafe hContinuation⟩

structure ProbeReceipt where
  coverageComplete : Bool

/-- Fail-closed admission gate for an external coverage receipt. -/
def ProbeMayDischarge (receipt : ProbeReceipt) (claim : Prop) : Prop :=
  receipt.coverageComplete = true ∧ claim

theorem coverageFalse_probe_cannot_discharge
    (receipt : ProbeReceipt) (claim : Prop)
    (hFalse : receipt.coverageComplete = false) :
    ¬ ProbeMayDischarge receipt claim := by
  simp [ProbeMayDischarge, hFalse]

#print axioms localCertificate_of_domainSafe
#print axioms domainSafeThrough_of_firstExit
#print axioms existsThrough_of_domainSafe_and_continuation
#print axioms p8_firstExit_domain_continuation_assembly
#print axioms coverageFalse_probe_cannot_discharge

end RouteBFirstExitBridge
