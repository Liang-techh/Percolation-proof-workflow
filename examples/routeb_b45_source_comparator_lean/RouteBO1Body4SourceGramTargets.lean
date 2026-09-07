import RouteBO1PerBodyTraceAdapter
import SourceContractIndexAdapter

set_option autoImplicit false

namespace RouteBO1Body4SourceGramTargets

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1PerBodyTraceAdapter
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBFrameSlotAccessor

/-!
Source-side child statements only. Human body 4 = body index 3.
No inhabitants of these targets are supplied; this file has not been elaborated.
The terminal seam is h_body_4_expected_entry_target, NOT h_body_4.
Jv/Jw are indexed [spatial coordinate, joint], Gram is [joint, joint].
-/

abbrev V3 := Fin 3 → ℝ
abbrev F4 := Matrix (Fin 4) (Fin 4) ℝ
abbrev body4 : Body := 3

def phi (q : Q6) : ℝ := q 1 + q 2
def b (q : Q6) : ℝ := (21 / 100 : ℝ) * Real.sin (q 1)
def c (q : Q6) : ℝ := (21 / 100 : ℝ) * Real.cos (q 1)
def d : ℝ := 1 / 20
def e : ℝ := 19 / 200
def aa (q : Q6) : ℝ := 2 / 25 + b q + e * Real.sin (phi q)
def pp (q : Q6) : ℝ := c q + e * Real.cos (phi q)
def qq (q : Q6) : ℝ := b q + e * Real.sin (phi q)

/-- Coordinates in the right-handed basis (er, et, ez). -/
def vec (q : Q6) (r t z : ℝ) : V3 :=
  ![r * Real.cos (q 0) - t * Real.sin (q 0),
    r * Real.sin (q 0) + t * Real.cos (q 0), z]

def dot (u v : V3) : ℝ := ∑ a : Axis, u a * v a

/-- Structural prefix equations preserve the multiplication association. -/
def Body4PrefixSlotsTarget : Prop :=
  ∀ q : Q6,
    routeBFrameSlot q 0 = (1 : F4) ∧
    routeBFrameSlot q 1 = (1 : F4) * routeBStepFunction q 0 ∧
    routeBFrameSlot q 2 = ((1 : F4) * routeBStepFunction q 0) *
      routeBStepFunction q 1 ∧
    routeBFrameSlot q 3 = (((1 : F4) * routeBStepFunction q 0) *
      routeBStepFunction q 1) * routeBStepFunction q 2 ∧
    routeBFrameSlot q 4 = ((((1 : F4) * routeBStepFunction q 0) *
      routeBStepFunction q 1) * routeBStepFunction q 2) * routeBStepFunction q 3

/- Only top spatial rows for slots 0..3; no full slot-4 rotation target. -/
def prefixX (q : Q6) (s : Fin 4) : V3 :=
  match s.val with
  | 0 => ![1, 0, 0]
  | 1 => vec q 1 0 0
  | 2 => vec q (Real.sin (q 1)) 0 (Real.cos (q 1))
  | 3 => vec q (Real.cos (phi q)) 0 (-Real.sin (phi q))
  | _ => 0

def prefixY (q : Q6) (s : Fin 4) : V3 :=
  match s.val with
  | 0 => ![0, 1, 0]
  | 1 => vec q 0 0 (-1)
  | 2 => vec q (Real.cos (q 1)) 0 (-Real.sin (q 1))
  | 3 => vec q 0 1 0
  | _ => 0

def prefixZ (q : Q6) (s : Fin 4) : V3 :=
  match s.val with
  | 0 => vec q 0 0 1
  | 1 => vec q 0 1 0
  | 2 => vec q 0 1 0
  | 3 => vec q (Real.sin (phi q)) 0 (Real.cos (phi q))
  | _ => 0

def prefixO (q : Q6) (s : Fin 4) : V3 :=
  match s.val with
  | 0 => 0
  | 1 => vec q (2 / 25) 0 (1 / 10)
  | 2 => vec q (2 / 25 + b q) 0 (1 / 10 + c q)
  | 3 => vec q (2 / 25 + b q) d (1 / 10 + c q)
  | _ => 0

def Body4PrefixColumnsTarget : Prop :=
  ∀ (q : Q6) (s : Fin 4) (a : Axis),
    let slot : Fin 7 := ⟨s.val, Nat.lt_trans s.isLt (by decide)⟩
    let row := RouteBFrameOriginAxis.embed3 a
    routeBFrameSlot q slot row 0 = prefixX q s a ∧
    routeBFrameSlot q slot row 1 = prefixY q s a ∧
    routeBFrameSlot q slot row 2 = prefixZ q s a ∧
    routeBFrameSlot q slot row 3 = prefixO q s a

/-- T3[:,3]=(0,0,19/100,1), so q 3 is absent from this column. -/
def Body4Slot4TranslationTarget : Prop :=
  ∀ (q : Q6) (a : Axis),
    RouteBFrameOriginAxis.origin (routeBFrameSlot q 4) a =
      RouteBFrameOriginAxis.origin (routeBFrameSlot q 3) a +
        (19 / 100 : ℝ) * RouteBFrameOriginAxis.zAxis (routeBFrameSlot q 3) a

def Body4SourceOriginsTarget : Prop :=
  ∀ q : Q6,
    (sourceContract q).origins 0 = prefixO q 0 ∧
    (sourceContract q).origins 1 = prefixO q 1 ∧
    (sourceContract q).origins 2 = prefixO q 2 ∧
    (sourceContract q).origins 3 = prefixO q 3 ∧
    (sourceContract q).origins 4 =
      vec q (2 / 25 + b q + (19 / 100) * Real.sin (phi q)) d
        (1 / 10 + c q + (19 / 100) * Real.cos (phi q))

def Body4SourceAxesTarget : Prop :=
  ∀ (q : Q6) (j : Fin 4),
    (sourceContract q).axes ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩ = prefixZ q j

def displacement (q : Q6) (j : Fin 4) : V3 :=
  match j.val with
  | 0 => vec q (aa q) d (1 / 10 + pp q)
  | 1 => vec q (qq q) d (pp q)
  | 2 => vec q (e * Real.sin (phi q)) d (e * Real.cos (phi q))
  | 3 => vec q (e * Real.sin (phi q)) 0 (e * Real.cos (phi q))
  | _ => 0

def Body4ComTarget : Prop :=
  ∀ q : Q6,
    bodyCom (sourceContract q).origins body4 = vec q (aa q) d (1 / 10 + pp q)

def Body4DisplacementsTarget : Prop :=
  ∀ (q : Q6) (j : Fin 4) (a : Axis),
    bodyCom (sourceContract q).origins body4 a -
      (sourceContract q).origins ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩ a =
        displacement q j a

def Body4BasisDotTarget : Prop :=
  ∀ (q : Q6) (r t z r' t' z' : ℝ),
    dot (vec q r t z) (vec q r' t' z') = r * r' + t * t' + z * z'

def Body4BasisCrossTarget : Prop :=
  ∀ (q : Q6) (r t z r' t' z' : ℝ),
    cross3 (vec q r t z) (vec q r' t' z') =
      vec q (t * z' - z * t') (z * r' - r * z') (r * t' - t * r')

def vcol (q : Q6) (j : Joint) : V3 :=
  match j.val with
  | 0 => vec q (-d) (aa q) 0
  | 1 => vec q (pp q) 0 (-qq q)
  | 2 => vec q (e * Real.cos (phi q)) 0 (-e * Real.sin (phi q))
  | _ => 0

def wcol (q : Q6) (j : Joint) : V3 :=
  match j.val with
  | 0 => vec q 0 0 1
  | 1 => vec q 0 1 0
  | 2 => vec q 0 1 0
  | 3 => vec q (Real.sin (phi q)) 0 (Real.cos (phi q))
  | _ => 0

/-- Joint 3 is active; its zero Jv must come from the parallel cross product. -/
def Body4JvTarget : Prop :=
  ∀ (q : Q6) (a : Axis) (j : Joint),
    bodyJv (sourceContract q).origins (sourceContract q).axes body4 a j = vcol q j a

def Body4JwTarget : Prop :=
  ∀ (q : Q6) (a : Axis) (j : Joint),
    bodyJw (sourceContract q).axes body4 a j = wcol q j a

def Body4InactiveTarget : Prop :=
  ∀ (q : Q6) (a : Axis) (j : Joint), 3 < j.val →
    bodyJv (sourceContract q).origins (sourceContract q).axes body4 a j = 0 ∧
    bodyJw (sourceContract q).axes body4 a j = 0

/- Unexpanded scalar Gram tables, including inactive rows AND columns. -/
def gv (q : Q6) (i j : Joint) : ℝ :=
  match i.val, j.val with
  | 0, 0 => aa q ^ 2 + d ^ 2
  | 0, 1 | 1, 0 => -d * pp q
  | 0, 2 | 2, 0 => -d * e * Real.cos (phi q)
  | 1, 1 => pp q ^ 2 + qq q ^ 2
  | 1, 2 | 2, 1 => e * (pp q * Real.cos (phi q) + qq q * Real.sin (phi q))
  | 2, 2 => e ^ 2
  | _, _ => 0

def gw (q : Q6) (i j : Joint) : ℝ :=
  match i.val, j.val with
  | 0, 0 | 1, 1 | 1, 2 | 2, 1 | 2, 2 | 3, 3 => 1
  | 0, 3 | 3, 0 => Real.cos (phi q)
  | _, _ => 0

def Body4LinearGramTarget : Prop :=
  ∀ (q : Q6) (i j : Joint), dot (vcol q i) (vcol q j) = gv q i j

def Body4AngularGramTarget : Prop :=
  ∀ (q : Q6) (i j : Joint), dot (wcol q i) (wcol q j) = gw q i j

/-- Inertia entries are ALREADY I_val/3; do not divide by three again. -/
def Body4InertiaTarget : Prop :=
  routeBMass body4 = (2 / 5 : ℝ) ∧
  ∀ a b : Axis, routeBInertia body4 a b = if a = b then (1 / 15 : ℝ) else 0

def Body4SourceGramTarget : Prop :=
  ∀ (q : Q6) (i j : Joint),
    sourceBodyMass q body4 i j = (2 / 5 : ℝ) * gv q i j + (1 / 15 : ℝ) * gw q i j

/- Scalar identities are separate from all source/list/matrix reductions. -/
def Body4UnitCircleTarget : Prop :=
  ∀ x : ℝ, Real.sin x ^ 2 + Real.cos x ^ 2 = 1

def Body4AngleAdditionTarget : Prop :=
  ∀ x y : ℝ,
    Real.sin (x + y) = Real.sin x * Real.cos y + Real.cos x * Real.sin y ∧
    Real.cos (x + y) = Real.cos x * Real.cos y - Real.sin x * Real.sin y

def Body4MixedTrigTarget : Prop :=
  ∀ x y : ℝ,
    Real.sin x * Real.sin (x + y) + Real.cos x * Real.cos (x + y) = Real.cos y

def Body4SquareTrigTarget : Prop :=
  ∀ x : ℝ, Real.sin x ^ 2 = (1 - Real.cos (2 * x)) / 2

def Body4ProductTrigTarget : Prop :=
  ∀ x y : ℝ,
    Real.sin x * Real.sin (x + y) = (Real.cos y - Real.cos (2 * x + y)) / 2

/-- Two uses of one mixed inner product; independent of q 0. -/
def Body4QuadraticReductionTarget : Prop :=
  ∀ q : Q6,
    pp q ^ 2 + qq q ^ 2 =
      (441 / 10000 : ℝ) + 361 / 40000 + (399 / 10000) * Real.cos (q 2) ∧
    e * (pp q * Real.cos (phi q) + qq q * Real.sin (phi q)) =
      (361 / 40000 : ℝ) + (399 / 20000) * Real.cos (q 2)

/-- Hardest scalar child: seven-term target is referenced, not redefined. -/
def Body4Scalar00Target : Prop :=
  ∀ q : Q6,
    (2 / 5 : ℝ) * (aa q ^ 2 + d ^ 2) + 1 / 15 = body_4_piecewise q 0 0

def Body4GramToPiecewiseTarget : Prop :=
  ∀ (q : Q6) (i j : Joint),
    (2 / 5 : ℝ) * gv q i j + (1 / 15 : ℝ) * gw q i j = body_4_piecewise q i j

/-- Direct existing adapter seams. Neither target is inhabited here. -/
def Body4ExpectedEntryHandoffTarget : Prop := h_body_4_expected_entry_target
def Body4ExpandedHandoffTarget : Prop := h_body_4_source_expanded_target

end
end RouteBO1Body4SourceGramTargets
