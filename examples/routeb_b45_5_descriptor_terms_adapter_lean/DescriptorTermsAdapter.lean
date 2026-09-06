import ResidualDecomposition

set_option autoImplicit false

namespace RouteBB45DescriptorTermsAdapter

noncomputable section

open RouteBB45ResidualDecomposition

/- The source-owned entries of the block-(4,5) residual ledger.  The two
   nominal PMI terms `rhoMgl` and `rhoKc` are intentionally not fields: they
   are fixed by the exact-real nominal model already defined upstream. -/
structure DescriptorResidualTerms where
  coriolis : Vec2
  gravity : Vec2
  gravityAtZero : Vec2
  massBB : Vec2 → Vec2
  accelerationB : Vec2
  remoteMassAcceleration : Vec2

def sourceDescriptorRhs (t : DescriptorResidualTerms) : Vec2 :=
  vadd (t.massBB t.accelerationB) t.remoteMassAcceleration

def expectedSourceForce (q v : Vec2) (w : ℝ)
    (t : DescriptorResidualTerms) : Vec2 :=
  sourceForce q v w t.coriolis t.gravity t.gravityAtZero

def descriptorResidualTotal (q : Vec2) (t : DescriptorResidualTerms) : Vec2 :=
  vadd (rhoC t.coriolis)
    (vadd (rhoG t.gravity t.gravityAtZero)
      (vadd (rhoMgl q)
        (vadd (rhoKc q)
          (vadd (rhoMass t.massBB t.accelerationB)
            (rhoRemote t.remoteMassAcceleration)))))

/- `q = (q4,q5)`, so the cross-coupling contribution is definitionally
   `(q5/100,q4/200)`.  No source or numerical premise is involved. -/
theorem rhoKc_descriptor_term_exact (q4 q5 : ℝ) :
    rhoKc (q4, q5) = (q5 / 100, q4 / 200) := by
  rfl

/- Expose the same exact cross term in the packaged six-term ledger. -/
theorem descriptorResidualTotal_with_explicit_kc
    (q : Vec2) (t : DescriptorResidualTerms) :
    descriptorResidualTotal q t =
      vadd (rhoC t.coriolis)
        (vadd (rhoG t.gravity t.gravityAtZero)
          (vadd (rhoMgl q)
            (vadd (q.2 / 100, q.1 / 200)
              (vadd (rhoMass t.massBB t.accelerationB)
                (rhoRemote t.remoteMassAcceleration))))) := by
  rfl

/- Pure descriptor seam.  A later source comparator must establish the one
   equality below for concrete source functions; this theorem only transports
   it into the existing six-term decomposition. -/
theorem blockResidual_eq_descriptorResidualTotal
    (q v : Vec2) (w : ℝ) (t : DescriptorResidualTerms)
    (hdescriptor : expectedSourceForce q v w t = sourceDescriptorRhs t) :
    blockResidual q v w t.accelerationB = descriptorResidualTotal q t := by
  exact residual_decomposition q v w t.coriolis t.gravity t.gravityAtZero
    t.massBB t.accelerationB t.remoteMassAcceleration hdescriptor

/- Comparator-facing form.  The comparator has two independent obligations:
   (1) identify the concrete source block force with the exact-real force
   expression, and (2) prove that the same source force is the BB block action
   plus the remote BD action.  Both are theorem premises, never axioms. -/
theorem blockResidual_eq_descriptorResidualTotal_of_source_comparator
    (q v : Vec2) (w : ℝ) (t : DescriptorResidualTerms)
    (sourceBlockForce : Vec2)
    (hforceBinding : sourceBlockForce = expectedSourceForce q v w t)
    (hblockDescriptor : sourceBlockForce = sourceDescriptorRhs t) :
    blockResidual q v w t.accelerationB = descriptorResidualTotal q t := by
  apply blockResidual_eq_descriptorResidualTotal q v w t
  exact hforceBinding.symm.trans hblockDescriptor

#print axioms rhoKc_descriptor_term_exact
#print axioms descriptorResidualTotal_with_explicit_kc
#print axioms blockResidual_eq_descriptorResidualTotal
#print axioms blockResidual_eq_descriptorResidualTotal_of_source_comparator

end

end RouteBB45DescriptorTermsAdapter
