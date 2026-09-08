import Mathlib

namespace RouteBP4Joint6RationalResidualBridge

/-- A rational residual CSE indexed by both a cell key and an observable/source key.
Two values with different keys have different types, so downstream adapters cannot
silently splice numerator/denominator evidence from unrelated cells or observables. -/
structure ResidualCSE (α CellKey SourceKey : Type)
    (cell : CellKey) (source : SourceKey) where
  num : α → ℝ
  den : α → ℝ

noncomputable def residualValue
    {α CellKey SourceKey : Type} {cell : CellKey} {source : SourceKey}
    (r : ResidualCSE α CellKey SourceKey cell source) (x : α) : ℝ :=
  r.num x / r.den x

def crossMismatch
    {α CellKey SourceKey : Type} {cell : CellKey} {source : SourceKey}
    (actual contract : ResidualCSE α CellKey SourceKey cell source) (x : α) : ℝ :=
  actual.num x * contract.den x - contract.num x * actual.den x

def denProduct
    {α CellKey SourceKey : Type} {cell : CellKey} {source : SourceKey}
    (actual contract : ResidualCSE α CellKey SourceKey cell source) (x : α) : ℝ :=
  actual.den x * contract.den x

/-- A positive lower bound on `|d|` forces `d ≠ 0`. -/
theorem ne_zero_of_pos_le_abs
    (d delta : ℝ) (hdelta : 0 < delta) (hlower : delta ≤ |d|) : d ≠ 0 := by
  by_contra hd
  simp [hd] at hlower
  linarith

/-- Exact signed cross-multiplication identity for two rational residuals. -/
theorem rational_residual_sub_eq_cross_mul_div
    (Na Da Nc Dc : ℝ) (hDa : Da ≠ 0) (hDc : Dc ≠ 0) :
    Na / Da - Nc / Dc = (Na * Dc - Nc * Da) / (Da * Dc) := by
  field_simp [hDa, hDc]

/-- Equality of rational residuals follows from the signed cross mismatch `Q = 0`. -/
theorem rational_residual_eq_of_cross_mul
    (Na Da Nc Dc : ℝ) (hDa : Da ≠ 0) (hDc : Dc ≠ 0)
    (hcross : Na * Dc - Nc * Da = 0) :
    Na / Da = Nc / Dc := by
  have hsub := rational_residual_sub_eq_cross_mul_div Na Da Nc Dc hDa hDc
  rw [hcross] at hsub
  simp at hsub
  linarith

/-- Generic quotient bound from a signed numerator enclosure and a positive
lower bound on the denominator magnitude. -/
theorem abs_div_le_of_abs_num_le
    (n d delta A : ℝ)
    (hdelta : 0 < delta)
    (hlower : delta ≤ |d|)
    (hnum : |n| ≤ A) :
    |n / d| ≤ A / delta := by
  have hd : d ≠ 0 := ne_zero_of_pos_le_abs d delta hdelta hlower
  have habsd_pos : 0 < |d| := abs_pos.mpr hd
  rw [abs_div]
  apply (le_div_iff₀ hdelta).2
  calc
    |n| / |d| * delta ≤ |n| / |d| * |d| := by
      exact mul_le_mul_of_nonneg_left hlower
        (div_nonneg (abs_nonneg n) (le_of_lt habsd_pos))
    _ = |n| := by
      field_simp [ne_of_gt habsd_pos]
    _ ≤ A := hnum

/-- Separate same-cell denominator lower bounds multiply without any sign choice. -/
theorem abs_den_product_lower
    (Da Dc deltaA deltaC : ℝ)
    (_hdeltaA : 0 < deltaA) (hdeltaC : 0 < deltaC)
    (hDa : deltaA ≤ |Da|) (hDc : deltaC ≤ |Dc|) :
    deltaA * deltaC ≤ |Da * Dc| := by
  rw [abs_mul]
  exact mul_le_mul hDa hDc (le_of_lt hdeltaC) (abs_nonneg Da)

/-- Same-cell sup containment for the rational-residual mismatch. -/
theorem rational_residual_sup_le_of_cross_mul_bound
    (Na Da Nc Dc deltaA deltaC E : ℝ)
    (hdeltaA : 0 < deltaA) (hdeltaC : 0 < deltaC)
    (hDa : deltaA ≤ |Da|) (hDc : deltaC ≤ |Dc|)
    (hcross : |Na * Dc - Nc * Da| ≤ E) :
    |Na / Da - Nc / Dc| ≤ E / (deltaA * deltaC) := by
  have hDa0 : Da ≠ 0 := ne_zero_of_pos_le_abs Da deltaA hdeltaA hDa
  have hDc0 : Dc ≠ 0 := ne_zero_of_pos_le_abs Dc deltaC hdeltaC hDc
  rw [rational_residual_sub_eq_cross_mul_div Na Da Nc Dc hDa0 hDc0]
  exact abs_div_le_of_abs_num_le
    (Na * Dc - Nc * Da) (Da * Dc) (deltaA * deltaC) E
    (mul_pos hdeltaA hdeltaC)
    (abs_den_product_lower Da Dc deltaA deltaC hdeltaA hdeltaC hDa hDc)
    hcross

/-- Division-free sufficient gate for a requested mismatch budget `B`. -/
theorem division_free_residual_sup_gate
    (Na Da Nc Dc deltaA deltaC E B : ℝ)
    (hdeltaA : 0 < deltaA) (hdeltaC : 0 < deltaC)
    (hDa : deltaA ≤ |Da|) (hDc : deltaC ≤ |Dc|)
    (hcross : |Na * Dc - Nc * Da| ≤ E)
    (hgate : E ≤ B * (deltaA * deltaC)) :
    |Na / Da - Nc / Dc| ≤ B := by
  have hsup := rational_residual_sup_le_of_cross_mul_bound
    Na Da Nc Dc deltaA deltaC E hdeltaA hdeltaC hDa hDc hcross
  have hdelta : 0 < deltaA * deltaC := mul_pos hdeltaA hdeltaC
  have hbudget : E / (deltaA * deltaC) ≤ B := by
    exact (div_le_iff₀ hdelta).2 hgate
  exact hsup.trans hbudget

/-- Typed same-cell/same-source exact equality adapter.  The shared dependent
indices are the interface boundary; deployed source binding must instantiate them. -/
theorem same_cell_source_residual_eq
    {α CellKey SourceKey : Type} {cell : CellKey} {source : SourceKey}
    (actual contract : ResidualCSE α CellKey SourceKey cell source) (x : α)
    (hDa : actual.den x ≠ 0) (hDc : contract.den x ≠ 0)
    (hcross : crossMismatch actual contract x = 0) :
    residualValue actual x = residualValue contract x := by
  exact rational_residual_eq_of_cross_mul
    (actual.num x) (actual.den x) (contract.num x) (contract.den x)
    hDa hDc hcross

/-- Typed same-cell/same-source division-free sup adapter. -/
theorem same_cell_source_division_free_sup_gate
    {α CellKey SourceKey : Type} {cell : CellKey} {source : SourceKey}
    (actual contract : ResidualCSE α CellKey SourceKey cell source) (x : α)
    (deltaA deltaC E B : ℝ)
    (hdeltaA : 0 < deltaA) (hdeltaC : 0 < deltaC)
    (hDa : deltaA ≤ |actual.den x|) (hDc : deltaC ≤ |contract.den x|)
    (hcross : |crossMismatch actual contract x| ≤ E)
    (hgate : E ≤ B * (deltaA * deltaC)) :
    |residualValue actual x - residualValue contract x| ≤ B := by
  exact division_free_residual_sup_gate
    (actual.num x) (actual.den x) (contract.num x) (contract.den x)
    deltaA deltaC E B hdeltaA hdeltaC hDa hDc hcross hgate

/-- Exact split used for a same-cell Lipschitz packet.  It preserves the signed
cross-mismatch cancellation before absolute-value enclosure. -/
theorem quotient_difference_split
    (Qx Qy Px Py : ℝ) (hPx : Px ≠ 0) (hPy : Py ≠ 0) :
    Qx / Px - Qy / Py =
      (Qx - Qy) / Px + Qy * (Py - Px) / (Px * Py) := by
  field_simp [hPx, hPy]
  ring

/-- Pairwise Lipschitz-style mismatch bound.  `r` is an abstract same-cell
point distance supplied by the downstream metric/domain layer. -/
theorem rational_residual_pair_lipschitz_of_cross_mul_packet
    (Qx Qy Px Py delta E LQ LP r : ℝ)
    (hdelta : 0 < delta)
    (hPx : delta ≤ |Px|) (hPy : delta ≤ |Py|)
    (hQy : |Qy| ≤ E) (hE : 0 ≤ E)
    (hQdiff : |Qx - Qy| ≤ LQ * r)
    (hPdiff : |Py - Px| ≤ LP * r) :
    |Qx / Px - Qy / Py| ≤
      (LQ / delta + E * LP / delta^2) * r := by
  have hPx0 : Px ≠ 0 := ne_zero_of_pos_le_abs Px delta hdelta hPx
  have hPy0 : Py ≠ 0 := ne_zero_of_pos_le_abs Py delta hdelta hPy
  have hfirst : |(Qx - Qy) / Px| ≤ (LQ * r) / delta :=
    abs_div_le_of_abs_num_le (Qx - Qy) Px delta (LQ * r)
      hdelta hPx hQdiff
  have hdelta_sq : 0 < delta^2 := by positivity
  have hprod_lower : delta^2 ≤ |Px * Py| := by
    rw [pow_two, abs_mul]
    exact mul_le_mul hPx hPy (le_of_lt hdelta) (abs_nonneg Px)
  have hsecond_num : |Qy * (Py - Px)| ≤ E * (LP * r) := by
    rw [abs_mul]
    exact mul_le_mul hQy hPdiff (abs_nonneg (Py - Px)) hE
  have hsecond : |Qy * (Py - Px) / (Px * Py)| ≤
      (E * (LP * r)) / delta^2 :=
    abs_div_le_of_abs_num_le (Qy * (Py - Px)) (Px * Py) (delta^2)
      (E * (LP * r)) hdelta_sq hprod_lower hsecond_num
  rw [quotient_difference_split Qx Qy Px Py hPx0 hPy0]
  calc
    |(Qx - Qy) / Px + Qy * (Py - Px) / (Px * Py)| ≤
        |(Qx - Qy) / Px| + |Qy * (Py - Px) / (Px * Py)| := abs_add_le _ _
    _ ≤ (LQ * r) / delta + (E * (LP * r)) / delta^2 :=
      add_le_add hfirst hsecond
    _ = (LQ / delta + E * LP / delta^2) * r := by ring

/-- Division-free sufficient gate for a requested pairwise Lipschitz budget `L`. -/
theorem division_free_residual_lipschitz_gate
    (Qx Qy Px Py delta E LQ LP L r : ℝ)
    (hdelta : 0 < delta)
    (hPx : delta ≤ |Px|) (hPy : delta ≤ |Py|)
    (hQy : |Qy| ≤ E) (hE : 0 ≤ E)
    (hQdiff : |Qx - Qy| ≤ LQ * r)
    (hPdiff : |Py - Px| ≤ LP * r)
    (hr : 0 ≤ r)
    (hgate : delta * LQ + E * LP ≤ L * delta^2) :
    |Qx / Px - Qy / Py| ≤ L * r := by
  have hraw := rational_residual_pair_lipschitz_of_cross_mul_packet
    Qx Qy Px Py delta E LQ LP r hdelta hPx hPy hQy hE hQdiff hPdiff
  have hdelta_sq : 0 < delta^2 := by positivity
  have hdelta0 : delta ≠ 0 := ne_of_gt hdelta
  have hcoeff_identity :
      LQ / delta + E * LP / delta^2 =
        (delta * LQ + E * LP) / delta^2 := by
    field_simp [hdelta0]
  have hcoeff : LQ / delta + E * LP / delta^2 ≤ L := by
    rw [hcoeff_identity]
    exact (div_le_iff₀ hdelta_sq).2 hgate
  exact hraw.trans (mul_le_mul_of_nonneg_right hcoeff hr)

#print axioms ne_zero_of_pos_le_abs
#print axioms rational_residual_sub_eq_cross_mul_div
#print axioms rational_residual_eq_of_cross_mul
#print axioms abs_div_le_of_abs_num_le
#print axioms abs_den_product_lower
#print axioms rational_residual_sup_le_of_cross_mul_bound
#print axioms division_free_residual_sup_gate
#print axioms same_cell_source_residual_eq
#print axioms same_cell_source_division_free_sup_gate
#print axioms quotient_difference_split
#print axioms rational_residual_pair_lipschitz_of_cross_mul_packet
#print axioms division_free_residual_lipschitz_gate

end RouteBP4Joint6RationalResidualBridge
