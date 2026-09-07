import NEW_KPATH_INTERFACE_Core

/-!
UNCOMPILED CANDIDATE. No Lean/Lake run is authorized for this round.
Typed seam only: the Python checker does not construct this proof object.
No concrete path table, source residual, rational SPN witness or instance.
-/

set_option autoImplicit false

namespace RouteBP5KPathRationalBinding

abbrev RationalGain := Fin 2 → Fin 4 → ℚ

/-- K should be the existing transportedGain for the actual supplied path;
G is the gain parameter used by ConeGapBinding and the future SPN certificate.
Both exact real/rational table identifications remain explicit proof obligations.
No receipt, hash string, or Python boolean is a constructor for these fields. -/
structure ExactComparisonBinding
    (K G : RouteBP5KPathInterface.NonnegativeGain) where
  pathTable : RationalGain
  certTable : RationalGain
  path_nonnegative : ∀ a j, 0 ≤ pathTable a j
  cert_nonnegative : ∀ a j, 0 ≤ certTable a j
  comparison : ∀ a j, pathTable a j ≤ certTable a j
  path_entry_eq : ∀ a j, K.value a j = (pathTable a j : ℝ)
  cert_entry_eq : ∀ a j, G.value a j = (certTable a j : ℝ)

/-- Candidate cast adapter; not a current kernel-verification claim. -/
theorem ExactComparisonBinding.toComponentLE
    {K G : RouteBP5KPathInterface.NonnegativeGain}
    (b : ExactComparisonBinding K G) :
    RouteBP5KPathInterface.ComponentLE K.value G.value := by
  intro a j
  rw [b.path_entry_eq a j, b.cert_entry_eq a j]
  exact_mod_cast b.comparison a j

end RouteBP5KPathRationalBinding
