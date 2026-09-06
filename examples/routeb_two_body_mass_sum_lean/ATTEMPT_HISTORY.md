# Attempt history

## 2026-09-06

- `run-xKNs29U4`: the first proof draft failed because `Mat` was not opened
  from the semantic-core namespace and the sum wrapper was not unfolded.
- `run-PKEzakdr`: after the namespace repair, Lean exposed the expected
  wrapper-rewrite boundary.
- `run-jYZomeB7`: an explicit entrywise `change` followed by the two
  single-body equalities compiled and passed source restriction.

No broad regression was run and no registry promotion is made.
