import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic

/-!
  Route-B P3: the smallest single-entry source/interval contract.

  This is deliberately a conditional contract.  `floatValue` is the real
  interpretation of one deployed Float64 result, while `ExactDHInterval` is
  an explicit premise about the exact DH evaluator.  No premise here asserts
  that the Julia evaluator equals the exact evaluator; that bridge remains an
  external, auditable obligation.
-/

set_option autoImplicit false

namespace RouteBP3MassEntryBridge

abbrev I6 := Fin 6
abbrev Q6 := I6 → ℝ

structure Box where
  lo : I6 → ℚ
  hi : I6 → ℚ

def Box.contains (B : Box) (q : Q6) : Prop :=
  ∀ k, (B.lo k : ℝ) ≤ q k ∧ q k ≤ (B.hi k : ℝ)

structure IntervalRat where
  lo : ℚ
  hi : ℚ

def IntervalRat.contains (I : IntervalRat) (x : ℝ) : Prop :=
  (I.lo : ℝ) ≤ x ∧ x ≤ (I.hi : ℝ)

theorem interval_contains_translated
    (I : IntervalRat) (x y : ℝ)
    (hxy : x = y) (hx : I.contains x) : I.contains y := by
  simpa [hxy] using hx

/- The receipt carries the fields that must be authenticated by the external
   checker.  The proposition field is intentionally supplied with its proof;
   ordinary printed Float64 output cannot manufacture this structure. -/
structure Float64TraceReceipt where
  sourceHash : String
  operationTraceHash : String
  runtime : String
  finiteNormalNoOverflow : Prop
  finiteNormalProof : finiteNormalNoOverflow
  value : ℝ

def regularizer : ℚ := 1 / 1000000

theorem regularizer_is_explicit : regularizer = (1 / 1000000 : ℚ) := by
  rfl

/- Exact interval soundness for one fixed M[i,j] entry.  The evaluator and
  interval are parameters, so this theorem does not silently define either
  one to be the other. -/
def ExactDHInterval
    (MExact : Q6 → I6 → I6 → ℝ) (B : Box) (I : IntervalRat)
    (i j : I6) : Prop :=
  ∀ q, B.contains q → I.contains (MExact q i j)

def Float64Trace
    (MFloat : Q6 → I6 → I6 → ℝ) (qhat : Q6)
    (i j : I6) (receipt : Float64TraceReceipt) : Prop :=
  receipt.value = MFloat qhat i j

theorem mass_entry_float64_to_exact_interval
    (B : Box) (I : IntervalRat)
    (MExact MFloat : Q6 → I6 → I6 → ℝ)
    (i j : I6) (qhat : Q6) (receipt : Float64TraceReceipt)
    (hExact : ExactDHInterval MExact B I i j)
    (_hInput : B.contains qhat)
    (hTrace : Float64Trace MFloat qhat i j receipt)
    (hReceiptIn : I.contains receipt.value) :
    I.contains (MFloat qhat i j) ∧
      (∀ q, B.contains q → I.contains (MExact q i j)) := by
  constructor
  · exact interval_contains_translated I receipt.value (MFloat qhat i j)
      hTrace hReceiptIn
  · exact hExact

/- The first component is the machine-side conclusion; the second component
   is the exact-real box conclusion.  The theorem remains conditional on both
   `hExact` and the receipt premises above. -/
theorem mass_entry_float64_membership
    (B : Box) (I : IntervalRat)
    (MExact MFloat : Q6 → I6 → I6 → ℝ)
    (i j : I6) (qhat : Q6) (receipt : Float64TraceReceipt)
    (hExact : ExactDHInterval MExact B I i j)
    (hInput : B.contains qhat)
    (hTrace : Float64Trace MFloat qhat i j receipt)
    (hReceiptIn : I.contains receipt.value) :
    I.contains (MFloat qhat i j) :=
  (mass_entry_float64_to_exact_interval B I MExact MFloat i j qhat receipt
    hExact hInput hTrace hReceiptIn).1

#print axioms interval_contains_translated
#print axioms regularizer_is_explicit
#print axioms mass_entry_float64_to_exact_interval
#print axioms mass_entry_float64_membership

end RouteBP3MassEntryBridge
