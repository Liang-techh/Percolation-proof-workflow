import Mathlib

set_option autoImplicit false

namespace NEW_BODY6_SLICE_STORAGEIDENTITY20260907
noncomputable section

/- OPEN_UNCOMPILED. Equality is required only on the specified comparison
   domain; a recorded scalar is not a proof indexed by a storage function. -/
def SameStorageIdentity {X : Type*} (D : Set X) (V W : X → ℝ) : Prop :=
  ∀ x ∈ D, V x = W x

structure InitialBoundBinding {X : Type*} (X0 : Set X)
    (V : X → ℝ) (upper : ℝ) : Prop where
  bound : ∀ x ∈ X0, V x ≤ upper

/- A sublevel conclusion along a specified path. This does not assert an
   ODE or prove a first-exit/continuation argument. -/
def SublevelBarrier {X : Type*} (T : ℝ) (V : X → ℝ)
    (path : ℝ → X) (bar : ℝ) : Prop :=
  ∀ t ∈ Set.Icc (0 : ℝ) T, V (path t) ≤ bar

theorem initial_bound_transfer_attempt {X : Type*} (X0 D : Set X)
    (V W : X → ℝ) (upper : ℝ) (hX : X0 ⊆ D)
    (hSame : SameStorageIdentity D V W) (hBound : InitialBoundBinding X0 V upper) :
    InitialBoundBinding X0 W upper := by
  constructor
  intro x hx
  rw [← hSame x (hX hx)]
  exact hBound.bound x hx

theorem barrier_transfer_attempt {X : Type*} (D : Set X) (V W : X → ℝ)
    (T bar : ℝ) (path : ℝ → X) (hSame : SameStorageIdentity D V W)
    (hPath : ∀ t ∈ Set.Icc (0 : ℝ) T, path t ∈ D)
    (hBarrier : SublevelBarrier T V path bar) : SublevelBarrier T W path bar := by
  intro t ht
  rw [← hSame (path t) (hPath t ht)]
  exact hBarrier t ht

/- A known offset transfers only with the corresponding threshold offset. -/
theorem offset_barrier_iff_attempt {X : Type*} (V : X → ℝ)
    (T bar beta : ℝ) (path : ℝ → X) :
    SublevelBarrier T (fun x => V x + beta) path (bar + beta) ↔
      SublevelBarrier T V path bar := by
  constructor <;> intro h t ht <;> have hb := h t ht <;> dsimp at hb ⊢ <;> linarith

abbrev State := Fin 12 → ℝ

/- Original block-only initial set, not the full twelve-dimensional ball.
   x[0..5]=q, x[6..11]=v; retained joints 4,5 use 3,4,9,10. -/
def blockOnlyInitial : Set State := {x |
  (∀ i, i ≠ 3 → i ≠ 4 → i ≠ 9 → i ≠ 10 → x i = 0) ∧
  (x 3)^2 + (x 4)^2 + (x 9)^2 + (x 10)^2 ≤ (9 / 400 : ℝ)}

def recordedInitialUpper : ℝ := 492033745203 / 25600000000000
def vBar : ℝ := 1

/- No constructor is supplied for the current external candidate. In
   particular, Vfull_DH and V_eps are separate typed inputs. -/
structure RouteBInitialTransfer (D : Set State)
    (Vfull_DH V_eps : State → ℝ) : Prop where
  sameStorage : SameStorageIdentity D V_eps Vfull_DH
  initialInDomain : blockOnlyInitial ⊆ D
  exportedInitial : InitialBoundBinding blockOnlyInitial V_eps recordedInitialUpper

theorem routeb_bound_transfers_if_bound_attempt (D : Set State)
    (Vfull_DH V_eps : State → ℝ) (h : RouteBInitialTransfer D Vfull_DH V_eps) :
    InitialBoundBinding blockOnlyInitial Vfull_DH recordedInitialUpper :=
  initial_bound_transfer_attempt blockOnlyInitial D V_eps Vfull_DH
    recordedInitialUpper h.initialInDomain h.sameStorage h.exportedInitial

theorem scalar_budget_below_bar_attempt : recordedInitialUpper < vBar := by
  norm_num [recordedInitialUpper, vBar]

/- Even genuinely valid initial bounds using the SAME scalar do not transfer
   a future barrier: V(x)=0 and W(x)=2x agree at x=0, but not along x(t)=t. -/
theorem shared_initial_bound_counterexample_attempt :
    ∃ V W : ℝ → ℝ,
      InitialBoundBinding {0} V 0 ∧ InitialBoundBinding {0} W 0 ∧
      SublevelBarrier 1 V (fun t => t) 1 ∧
      ¬ SublevelBarrier 1 W (fun t => t) 1 := by
  refine ⟨(fun _ => 0), (fun x => 2*x), ?_, ?_, ?_, ?_⟩
  · constructor
    intro x hx
    norm_num
  · constructor
    intro x hx
    have he : x = 0 := Set.mem_singleton_iff.mp hx
    subst x
    norm_num
  · intro t ht
    norm_num
  · intro h
    have hb := h 1 (by norm_num)
    norm_num at hb

/- Identical derivatives alone miss the additive constant: both storage
   derivatives are zero, but the fixed threshold 1 rejects W=2 everywhere.
   This example does NOT supply an initial bound W(0)<=0. -/
theorem derivative_identity_counterexample_attempt :
    (∀ t : ℝ, deriv (fun _ : ℝ => (0 : ℝ)) t =
      deriv (fun _ : ℝ => (2 : ℝ)) t) ∧
    SublevelBarrier 1 (fun _ : ℝ => 0) (fun t => t) 1 ∧
    ¬ SublevelBarrier 1 (fun _ : ℝ => 2) (fun t => t) 1 := by
  refine ⟨?_, ?_, ?_⟩
  · intro t
    simp
  · intro t ht
    norm_num
  · intro h
    have hb := h 0 (by norm_num)
    norm_num at hb

/- No impossibility is claimed when both the target initial bound and a
   sufficient target derivative/integrated budget are actually proved. -/
end
end NEW_BODY6_SLICE_STORAGEIDENTITY20260907
