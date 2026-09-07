import NEW_FIXED_LAMBDA_ADMISSIBILITY_TYPED_RECEIPT_AUDIT20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaCanonicalDigestNormalization

open RouteBFixedLambdaExactStatementBoundary
open RouteBFixedLambdaTypedReceiptAudit

noncomputable section

/-!
This sidecar distinguishes a typed canonical statement digest from a byte
artifact hash and from ordinary text similarity.  The canonical digest
function is an explicit external oracle parameter; no hash algorithm or
checker execution is silently invented here.
-/

structure CanonicalStatementForm where
  binder : List String
  quantifier_order : List String
  term_order : List String
  normalization : String
  body : String

def CanonicalStatementEquivalent
    (candidate target : CanonicalStatementForm) : Prop :=
  candidate.binder = target.binder ∧
    candidate.quantifier_order = target.quantifier_order ∧
    candidate.term_order = target.term_order ∧
    candidate.normalization = target.normalization ∧
    candidate.body = target.body

def OrdinaryTextSimilar
    (candidate target : CanonicalStatementForm) : Prop :=
  candidate.body = target.body

def canonicalTargetStatement : CanonicalStatementForm :=
  { binder := ["load : ℝ", "margin : ℝ"]
    quantifier_order := ["fixed-lambda", "finite-tagged-rows"]
    term_order := ["load", "margin"]
    normalization := "canonical ℚ→ℝ casts; subtraction normalized in ℝ"
    body := "load < margin" }

def approximatelySimilarCandidate : CanonicalStatementForm :=
  { binder := ["load : ℝ", "margin : ℝ"]
    quantifier_order := ["fixed-lambda", "finite-tagged-rows"]
    term_order := ["margin", "load"]
    normalization := "canonical ℚ→ℝ casts; subtraction normalized in ℝ"
    body := "load < margin" }

/-!
The candidate has identical body text but a different canonical term order.
It is therefore a concrete near-text counterexample, not an exact statement
match.  Text similarity is deliberately not used as a digest/binding proof.
-/
theorem approximate_text_does_not_imply_canonical_equivalence :
    OrdinaryTextSimilar approximatelySimilarCandidate canonicalTargetStatement ∧
      ¬ CanonicalStatementEquivalent
        approximatelySimilarCandidate canonicalTargetStatement := by
  constructor
  · rfl
  · intro h
    have horder :
        (["margin", "load"] : List String) = ["load", "margin"] := h.2.2.1
    simp at horder

abbrev CanonicalDigestOracle :=
  CanonicalStatementForm → ExactStatementDigest

structure CanonicalDigestReceiptRecord
    (candidate target : CanonicalStatementForm) where
  source_artifact : Option SourceArtifact
  artifact_hash : Option ByteHash
  exact_statement_digest : Option ExactStatementDigest

def CanonicalReceiptPending
    {candidate target : CanonicalStatementForm}
    (record : CanonicalDigestReceiptRecord candidate target) : Prop :=
  record.source_artifact = none ∨
    record.artifact_hash = none ∨
    record.exact_statement_digest = none

def CanonicalReceiptRejected
    {candidate target : CanonicalStatementForm}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : CanonicalDigestReceiptRecord candidate target) : Prop :=
  ¬ CanonicalStatementEquivalent candidate target ∨
    expectedDigest ≠ oracle target ∨
    record.artifact_hash ≠ some expectedHash ∨
    record.exact_statement_digest ≠ some expectedDigest ∨
    (∃ artifact,
      record.source_artifact = some artifact ∧
        (artifact.artifact_id = "" ∨
          artifact.provenance = none ∨
          artifact.byte_hash ≠ some expectedHash))

/-!
All exact bindings are explicit.  In particular, the receipt digest is bound
to the target through `expectedDigest = oracle target`, while the byte hash is
bound separately to the source artifact and the receipt hash.
-/
structure CanonicalDigestReceiptAdmissionContract
    {candidate target : CanonicalStatementForm}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : CanonicalDigestReceiptRecord candidate target) where
  artifact : SourceArtifact
  source_artifact_eq : record.source_artifact = some artifact
  artifact_id_nonempty : artifact.artifact_id ≠ ""
  artifact_provenance_present :
    ∃ origin, artifact.provenance = some origin ∧ origin ≠ ""
  artifact_byte_hash_eq : artifact.byte_hash = some expectedHash
  receipt_artifact_hash_eq : record.artifact_hash = some expectedHash
  statement_equivalence :
    CanonicalStatementEquivalent candidate target
  receipt_digest_eq_expected :
    record.exact_statement_digest = some expectedDigest
  expected_digest_eq_target : expectedDigest = oracle target
  pending_absent : ¬ CanonicalReceiptPending record
  rejected_absent : ¬ CanonicalReceiptRejected oracle expectedHash expectedDigest record

theorem pending_cannot_admit_canonical_receipt
    {candidate target : CanonicalStatementForm}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {record : CanonicalDigestReceiptRecord candidate target}
    (pending : CanonicalReceiptPending record) :
    ¬ Nonempty
      (CanonicalDigestReceiptAdmissionContract
        oracle expectedHash expectedDigest record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  exact admitted.pending_absent pending

theorem rejected_cannot_admit_canonical_receipt
    {candidate target : CanonicalStatementForm}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {record : CanonicalDigestReceiptRecord candidate target}
    (rejected : CanonicalReceiptRejected
      oracle expectedHash expectedDigest record) :
    ¬ Nonempty
      (CanonicalDigestReceiptAdmissionContract
        oracle expectedHash expectedDigest record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  exact admitted.rejected_absent rejected

theorem near_text_counterexample_is_rejected
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : CanonicalDigestReceiptRecord
      approximatelySimilarCandidate canonicalTargetStatement)
    (hrecord : ¬ CanonicalStatementEquivalent
      approximatelySimilarCandidate canonicalTargetStatement) :
    CanonicalReceiptRejected oracle expectedHash expectedDigest record := by
  exact Or.inl hrecord

/-!
No theorem below maps a complete canonical receipt to VERIFIED or to a
registry entry.  The digest oracle, byte-level hash computation, and source
provenance chain remain explicit external obligations.
-/

#print axioms approximate_text_does_not_imply_canonical_equivalence
#print axioms pending_cannot_admit_canonical_receipt
#print axioms rejected_cannot_admit_canonical_receipt
#print axioms near_text_counterexample_is_rejected

end
end RouteBFixedLambdaCanonicalDigestNormalization
