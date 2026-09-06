# Route-B structural statement comparator

This is the first comparator stage for the two new Lean sidecars. It compares
the exact indexed declaration surface in the delivered source with the
successful pre-run snapshot and checks required semantic fragments. It is a
conservative pre-comparator only: it does not run the upstream comparator,
prove physical DH/source binding, or permit registry promotion.

Run from the workspace root with `python -B
examples/routeb_structural_comparator/compare.py`. The output is immutable
under a new timestamped directory and reports `accepted=true` only for this
structural check.
