# External catalog validator

`percolation_workflow.external_catalog` is a small, read-only boundary for
external Anthropic FLT candidates. `validate_catalog_file(path)` checks the
source commit, license, Lean toolchain, Mathlib revision, candidate path and
attribution, and accepts only classifications `1`, `2`, or `3`.

It returns classifications, a SHA-256 provenance hash of canonical catalog JSON,
and a derived Route-B reuse set. Pure number-theory candidates, and all
classification `3` candidates, remain provenance-only. The validator does not
import, update, or consult registry/admission layers and never writes the catalog.
