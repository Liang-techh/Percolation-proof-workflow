import ActualStorage
import ActualShift

set_option autoImplicit false
open scoped BigOperators

namespace NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907
noncomputable section

/- OPEN_UNCOMPILED sidecar. The imported leaves have historical receipts;
   that does not constitute compilation or instantiation of this sidecar. -/
abbrev Vec := Fin 6 → ℝ
abbrev Mat := Fin 6 → Fin 6 → ℝ

structure Sample where
  q : Vec
  v : Vec
  slope : ℝ

structure StorageData where
  f : ℝ → ℝ
  p : ℝ → Vec
  h : ℝ → ℝ
  H : Mat
  M : Vec → Mat
  U : Vec → ℝ
  Uzero : ℝ

def actualAt (d : StorageData) (t : ℝ) (x : Sample) : ℝ :=
  RouteBActualEnergyStorage.storageV (d.f t) (d.p t) (d.h t)
    d.H (d.M x.q) (d.U x.q) d.Uzero x.q x.v x.slope

def ledgerV0 : ℝ := 492033745203 / 25600000000000
def ledgerBar : ℝ := 1
def initialFormula (d : StorageData) (beta : ℝ) : ℝ :=
  (9/400)*beta + 3*(d.f 0)/10000 + 3*(d.h 0)

/- Exactly the premises of the existing storageV_initial_upper theorem;
   no physical source identity or actual gap bound is manufactured. -/
structure ActualInitialPremises (d : StorageData) (x : Sample) (beta : ℝ) : Prop where
  fNonneg : 0 ≤ d.f 0
  hNonneg : 0 ≤ d.h 0
  ball : RouteBActualEnergyStorage.normSq x.q + RouteBActualEnergyStorage.normSq x.v ≤ 9/400
  gap : -(3/10000) ≤ RouteBActualEnergyStorage.actualSignedGap
    d.H (d.M x.q) (d.U x.q) d.Uzero x.q x.v
  ramp : x.slope^2 ≤ 3
  betaV : d.f 0 / 2 ≤ beta
  betaQ : ∀ i, RouteBActualEnergyStorage.positionWeight (d.f 0) (d.p 0) i ≤ beta

theorem existing_initial_theorem_instance_attempt (d : StorageData)
    (x : Sample) (beta : ℝ) (h : ActualInitialPremises d x beta) :
    actualAt d 0 x ≤ initialFormula d beta :=
  RouteBActualEnergyStorage.storageV_initial_upper
    (d.f 0) (d.p 0) (d.h 0) beta d.H (d.M x.q) (d.U x.q) d.Uzero
    x.q x.v x.slope h.fNonneg h.hNonneg h.ball h.gap h.ramp h.betaV h.betaQ

structure InitialLedgerBinding (d : StorageData) (L : ℝ → Sample → ℝ)
    (X0 : Set Sample) (beta : ℝ) : Prop where
  sameInitial : ∀ x ∈ X0, L 0 x = actualAt d 0 x
  initialPremises : ∀ x ∈ X0, ActualInitialPremises d x beta
  budgetToV0 : initialFormula d beta ≤ ledgerV0

theorem initial_ledger_bound_attempt (d : StorageData) (L : ℝ → Sample → ℝ)
    (X0 : Set Sample) (beta : ℝ) (h : InitialLedgerBinding d L X0 beta) :
    ∀ x ∈ X0, L 0 x ≤ ledgerV0 := by
  intro x hx
  rw [h.sameInitial x hx]
  exact (existing_initial_theorem_instance_attempt d x beta
    (h.initialPremises x hx)).trans h.budgetToV0

/- Path, tube and identity are distinct remaining mathematical inputs.
   In particular, pathInDomain is not inferred from the desired barrier. -/
structure PathLedgerBinding (d : StorageData) (L : ℝ → Sample → ℝ)
    (D : ℝ → Set Sample) (path : ℝ → Sample) (tube : ℝ) : Prop where
  sameStorage : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x ∈ D t, L t x = actualAt d t x
  pathInDomain : ∀ t ∈ Set.Icc (0 : ℝ) 1, path t ∈ D t
  sourceTube : ∀ t ∈ Set.Icc (0 : ℝ) 1, actualAt d t (path t) ≤ tube
  tubeBelowBar : tube < ledgerBar

theorem path_ledger_barrier_attempt (d : StorageData) (L : ℝ → Sample → ℝ)
    (D : ℝ → Set Sample) (path : ℝ → Sample) (tube : ℝ)
    (h : PathLedgerBinding d L D path tube) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, L t (path t) < ledgerBar := by
  intro t ht
  rw [h.sameStorage t ht (path t) (h.pathInDomain t ht)]
  exact (h.sourceTube t ht).trans_lt h.tubeBelowBar

/- This optional block comparison retains the EXACT shift of ActualShift.
   A ledger V must bind to E+B if it wants this particular inequality. -/
def encodedShiftedEnergy (M : Mat) (q v : Vec) : ℝ :=
  RouteBShiftedStorage.kinetic M v + RouteBPotentialSlice.W q + (4079979/400000)

theorem existing_shifted_comparison_instance_attempt (M : Mat) (q v : Vec)
    (hmass : (9401/1000000 : ℝ) * (∑ i, v i^2) ≤
      ∑ i, v i * (∑ j, M i j * v j)) :
    RouteBShiftedStorage.p45 q v ≤
      (1600000/9401 : ℝ) * encodedShiftedEnergy M q v :=
  RouteBActualShift.actual_p45_bound q v M
    (RouteBShiftedStorage.kinetic M v + RouteBPotentialSlice.W q) hmass rfl

theorem component_cap_does_not_imply_storage_cap_attempt :
    ¬ ((5/2 : ℝ)^2 ≤ 56/15) := by norm_num

theorem w0_initial_number_fits_ledger_attempt :
    (231/20000 : ℝ) ≤ ledgerV0 := by norm_num [ledgerV0]

/- A weak upper bound is not evidence that the true output exceeds 45. -/
theorem shifted_comparison_baseline_exceeds_45_attempt :
    (45 : ℝ) < (1600000/9401) * (4079979/400000) := by norm_num

/- No instance of either ledger-binding record is asserted. Initial/path
   compatibility, ODE, source semantics and continuation remain external. -/
end
end NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907
