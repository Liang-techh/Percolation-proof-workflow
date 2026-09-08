import NEW_QUOTIENT_CLM_API_REPAIR_20260908

set_option autoImplicit false

namespace FLTQuotientCLMReceiptProbe

/- OPEN_UNCOMPILED. Explicit type wrappers only, no physical domain instance.
   Upstream Apache/Imperial/Anthropic notices are preserved by the imported
   candidate and its companion handoff; this probe copies no number theory. -/

def checkQuotientType {R : Type*} [Ring R] (G H : Type*)
    [AddCommGroup G] [Module R G] [AddCommGroup H] [Module R H]
    [TopologicalSpace G] [TopologicalSpace H]
    (G' : Submodule R G) (H' : Submodule R H) (e : G ≃L[R] H)
    (h : Submodule.map e.toLinearMap G' = H') :
    (G ⧸ G') ≃L[R] (H ⧸ H') :=
  FLTQuotientCLMAPIRepair.quotientContinuousLinearEquiv G H G' H' e h

def checkProductType {R ι : Type*} [CommRing R] {G : ι → Type*}
    [(i : ι) → AddCommGroup (G i)] [(i : ι) → Module R (G i)]
    [(i : ι) → TopologicalSpace (G i)]
    [(i : ι) → IsTopologicalAddGroup (G i)] [Fintype ι] [DecidableEq ι]
    (p : (i : ι) → Submodule R (G i)) :
    (((i : ι) → G i) ⧸ Submodule.pi Set.univ p) ≃L[R]
      ((i : ι) → G i ⧸ p i) :=
  FLTQuotientCLMAPIRepair.quotientPiContinuousLinearEquiv p

#check @FLTQuotientCLMAPIRepair.quotientContinuousLinearEquiv
#check @FLTQuotientCLMAPIRepair.quotientPiContinuousLinearEquiv
#print axioms FLTQuotientCLMAPIRepair.quotientContinuousLinearEquiv
#print axioms FLTQuotientCLMAPIRepair.quotientPiContinuousLinearEquiv
#print axioms checkQuotientType
#print axioms checkProductType

end FLTQuotientCLMReceiptProbe
