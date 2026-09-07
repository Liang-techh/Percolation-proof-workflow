# Fixed-lambda two-eta sparse union review

## Scope and status

This sidecar adds the missing union/accounting seam for the two declared eta
partitions.  It reuses the selected-box parent lemma and does not repeat the
coefficient bridge or selected-box positivity proof.

No Lean or Lake command was run.  The file is an uncompiled proof skeleton;
there is no kernel, comparator, or registry status claim.

## Contract supplied

- `EtaTag × Nat` tags local row indices before union, so index reuse between
  eta=2.7 and eta=5.6 cannot create a false row collision.
- `CrossEtaLabelsDisjoint` is an explicit premise that box labels from the
  two eta slices do not overlap.
- `union_oneRowPerBox` combines each partition's local injectivity with that
  cross-eta label premise.
- `union_rows_card` preserves exact row accounting, and the declared premises
  imply `256 + 321 = 577` through `union_boxLabels_card`.
- `union_selected_box_has_positive_margin` lifts the existing uniform λ=2
  selected-box margin result to any box label in the tagged union, retaining a
  tagged row membership witness.

The digest and canonical-row bindings remain fields of the two input
partitions.  They are not computed or used to manufacture a Lean fact here.

## Remaining external premises and non-claims

The theorem consumes, rather than establishes, the two local one-row-per-box
facts, the cross-eta label-disjointness premise, row counts, positive
denominators, margin equations, and strict upper conditions.  It does not bind
any of these to the CSV/source evaluator or verify the SHA-256 digest.

The union is only the supplied finite declared artifact.  The cardinality 577
does not prove complete box coverage, dense labels, true-DH interval coverage,
missing-cell exclusion, residual/PDE/trajectory closure, or parent-node
formal closure.  No source theorem, registry promotion, or formal certificate
permission follows.

No state, registry, receipt, or shared script was modified.
