import NEW_BODY6_SLICE_KEYEDSTORAGETRANSFER20260907

set_option autoImplicit false
open scoped BigOperators

namespace NEW_BODY6_SLICE_INITIALCROSSDELTA20260907
noncomputable section
open NEW_BODY6_SLICE_KEYEDSTORAGETRANSFER20260907

/- OPEN_UNCOMPILED. All norms below are explicitly Euclidean finite sums;
   no use is made of the default norm on Fin 6 -> Real. -/
abbrev Vec := Fin 6 → ℝ
abbrev Mat := Fin 6 → Fin 6 → ℝ
abbrev State := Vec × Vec
def normSq (u : Vec) : ℝ := ∑ i, (u i)^2
def cross (A : Mat) (u v : Vec) : ℝ := ∑ i, u i * (∑ j, A i j * v j)
def radius : ℝ := 3/20
def eps : ℝ := 1/1000
def massCap : ℝ := 163847401/96000000
def deltaX0 : ℝ := 491542203/25600000000000

def blockInitial : Set State := {x |
  (∀ i, i ≠ 3 → i ≠ 4 → x.1 i = 0 ∧ x.2 i = 0) ∧
  normSq x.1 + normSq x.2 ≤ radius^2}

/- Bilinear form of an induced Euclidean operator bound. It must hold for
   THIS matrix evaluator on Q, not merely for its origin or another source. -/
def EuclideanMassBound (M : Vec → Mat) (Q : Set Vec) : Prop :=
  ∀ q ∈ Q, ∀ u v : Vec,
    |cross (M q) u v| ≤ massCap * (Real.sqrt (normSq u) * Real.sqrt (normSq v))

/- Optional l1 route: row AND column bounds suffice for the Euclidean bound.
   This record is not automatically converted by this leaf; see review. -/
structure RowColumnL1Bound (M : Vec → Mat) (Q : Set Vec) : Prop where
  rows : ∀ q ∈ Q, ∀ i, (∑ j, |M q i j|) ≤ massCap
  columns : ∀ q ∈ Q, ∀ j, (∑ i, |M q i j|) ≤ massCap

theorem sqrt_product_young_attempt (u v : Vec) :
    Real.sqrt (normSq u) * Real.sqrt (normSq v) ≤ (normSq u + normSq v)/2 := by
  have hu : 0 ≤ normSq u := Finset.sum_nonneg (fun i _ => sq_nonneg (u i))
  have hv : 0 ≤ normSq v := Finset.sum_nonneg (fun i _ => sq_nonneg (v i))
  have hsu := Real.sq_sqrt hu
  have hsv := Real.sq_sqrt hv
  nlinarith [sq_nonneg (Real.sqrt (normSq u) - Real.sqrt (normSq v))]

theorem delta_exact_attempt : eps * massCap * radius^2 / 2 = deltaX0 := by
  norm_num [eps, massCap, radius, deltaX0]

theorem cross_bound_on_initial_attempt (M : Vec → Mat) (Q : Set Vec)
    (hM : EuclideanMassBound M Q) (x : State)
    (hx : x ∈ blockInitial) (hq : x.1 ∈ Q) :
    |eps * cross (M x.1) x.1 x.2| ≤ deltaX0 := by
  have hm := hM x.1 hq x.1 x.2
  have hy := sqrt_product_young_attempt x.1 x.2
  have hc : 0 ≤ massCap := by norm_num [massCap]
  have he : 0 ≤ eps := by norm_num [eps]
  have hsize := hx.2
  have hp := mul_le_mul_of_nonneg_left hy hc
  have hb : |cross (M x.1) x.1 x.2| ≤ massCap * radius^2 / 2 := by
    have hr := mul_le_mul_of_nonneg_left hsize hc
    nlinarith
  calc
    |eps * cross (M x.1) x.1 x.2| = eps * |cross (M x.1) x.1 x.2| := by
      rw [abs_mul, abs_of_nonneg he]
    _ ≤ eps * (massCap * radius^2 / 2) := mul_le_mul_of_nonneg_left hb he
    _ = deltaX0 := by rw [← delta_exact_attempt]; ring

/- The configuration domain, same-source matrix equality, and actual storage
   difference are independent fields. No hash label supplies these proofs. -/
structure InitialCrossBinding (Msource Mbound : Vec → Mat) (Q : Set Vec)
    (src dst : Candidate State) : Prop where
  configsInDomain : ∀ x ∈ blockInitial, x.1 ∈ Q
  sameMass : ∀ q ∈ Q, Msource q = Mbound q
  massBound : EuclideanMassBound Mbound Q
  difference : ∀ x ∈ blockInitial,
    |dst.V x - src.V x| ≤ |eps * cross (Msource x.1) x.1 x.2|

theorem initial_one_sided_delta_attempt (Msource Mbound : Vec → Mat) (Q : Set Vec)
    (src dst : Candidate State) (h : InitialCrossBinding Msource Mbound Q src dst) :
    ∀ x ∈ blockInitial, dst.V x ≤ src.V x + deltaX0 := by
  intro x hx
  have hd := h.difference x hx
  rw [h.sameMass x.1 (h.configsInDomain x hx)] at hd
  have hb := cross_bound_on_initial_attempt Mbound Q h.massBound x hx (h.configsInDomain x hx)
  have hu := (abs_le.mp (hd.trans hb)).2
  linarith

def initialScope (initialDigest domainDigest : String) : Scope State :=
  ⟨blockInitial, blockInitial, initialDigest, domainDigest⟩

theorem keyed_initial_transfer_contract_attempt
    (Msource Mbound : Vec → Mat) (Q : Set Vec) (src dst : Candidate State)
    (h : InitialCrossBinding Msource Mbound Q src dst)
    (initialDigest domainDigest : String) (receipt : ReceiptKey)
    (hkey : receipt = keyOf src dst (initialScope initialDigest domainDigest)) :
    TransferContract src dst (initialScope initialDigest domainDigest) receipt deltaX0 :=
  ⟨hkey, fun _ hx => hx, initial_one_sided_delta_attempt Msource Mbound Q src dst h⟩

/- Scope is X0 only. A whole-path use requires a new radius/domain bound,
   source comparison and compatible key; none is inferred from X0. -/
end
end NEW_BODY6_SLICE_INITIALCROSSDELTA20260907
