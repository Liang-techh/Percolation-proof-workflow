import NEW_FIXED_LAMBDA_ADMISSIBILITY_SPARSE_DIGEST_FOLD20260907
import Mathlib.Data.List.Basic

set_option autoImplicit false

namespace RouteBFixedLambdaCanonicalDigestComposition

open RouteBFixedLambdaSparseDigestFold

noncomputable section

/-!
This sidecar handles only the canonical-encoding/digest composition seam.  It
does not implement SHA-256.  In particular, two per-partition digest tokens
do not determine the digest of their concatenated payload; an external union
oracle/token binding is therefore an explicit premise.
-/

structure UnionDigestBinding (f : Declared577SparseFold) where
  digest : ExactWitnessDigest
  oracle : List String → ExactWitnessDigest
  binding :
    digest = oracle (selectedRowEncoding f.eta27 ++
      selectedRowEncoding f.eta56)

structure CanonicalDigestComposition (f : Declared577SparseFold) where
  eta27Encoding : List String
  eta56Encoding : List String
  unionEncoding : List String
  eta27Digest : ExactWitnessDigest
  eta56Digest : ExactWitnessDigest
  unionDigest : ExactWitnessDigest
  unionOracle : List String → ExactWitnessDigest
  eta27_encoding_eq :
    eta27Encoding = selectedRowEncoding f.eta27
  eta56_encoding_eq :
    eta56Encoding = selectedRowEncoding f.eta56
  union_encoding_eq_concat :
    unionEncoding = eta27Encoding ++ eta56Encoding
  eta27_digest_eq : eta27Digest = f.eta27.digest
  eta56_digest_eq : eta56Digest = f.eta56.digest
  union_digest_eq_oracle : unionDigest = unionOracle unionEncoding

theorem eta27_digest_binding
    {f : Declared577SparseFold}
    (c : CanonicalDigestComposition f) :
    c.eta27Digest = f.eta27.digestOracle c.eta27Encoding := by
  rw [c.eta27_digest_eq, c.eta27_encoding_eq]
  exact digest_tracks_selected_rows f.eta27

theorem eta56_digest_binding
    {f : Declared577SparseFold}
    (c : CanonicalDigestComposition f) :
    c.eta56Digest = f.eta56.digestOracle c.eta56Encoding := by
  rw [c.eta56_digest_eq, c.eta56_encoding_eq]
  exact digest_tracks_selected_rows f.eta56

/-!
The union binding is obtained only after the external composition record
supplies both canonical per-partition encodings and the exact union-oracle
result for their concatenation.
-/
theorem union_digest_binding_of_consistent_encoding
    {f : Declared577SparseFold}
    (c : CanonicalDigestComposition f) :
    c.unionDigest = c.unionOracle
      (selectedRowEncoding f.eta27 ++ selectedRowEncoding f.eta56) := by
  rw [c.union_digest_eq_oracle, c.union_encoding_eq_concat,
    c.eta27_encoding_eq, c.eta56_encoding_eq]

def compose_union_digest_binding
    {f : Declared577SparseFold}
    (c : CanonicalDigestComposition f) :
    UnionDigestBinding f :=
  { digest := c.unionDigest
    oracle := c.unionOracle
    binding := union_digest_binding_of_consistent_encoding c }

theorem composed_union_binding_is_the_supplied_token
    {f : Declared577SparseFold}
    (c : CanonicalDigestComposition f) :
    (compose_union_digest_binding c).digest = c.unionDigest := by
  rfl

theorem composed_union_binding_uses_concat_encoding
    {f : Declared577SparseFold}
    (c : CanonicalDigestComposition f) :
    (compose_union_digest_binding c).binding := by
  exact union_digest_binding_of_consistent_encoding c

/-!
The two per-partition bindings and the union binding are separate facts.  No
claim is made that the first two tokens can be hashed together internally.
-/

#print axioms eta27_digest_binding
#print axioms eta56_digest_binding
#print axioms union_digest_binding_of_consistent_encoding
#print axioms compose_union_digest_binding
#print axioms composed_union_binding_is_the_supplied_token
#print axioms composed_union_binding_uses_concat_encoding

end
end RouteBFixedLambdaCanonicalDigestComposition
