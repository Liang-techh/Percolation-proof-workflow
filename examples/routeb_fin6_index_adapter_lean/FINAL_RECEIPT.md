# Final receipt

Status: `PASS — COMPILED_CANDIDATE_COMPARATOR_PENDING`

This receipt belongs only to the new finite-index source adapter.  The
successful pinned evidence is:

- Lean 4.33.1, pinned Mathlib commit;
- zero `sorry`, `admit`, and custom axioms;
- exact `Fin 6` ↔ Julia 1-based bijection;
- exact source-order and B/D mapping theorems;
- function-level frame binding: **OPEN**;
- function-level mass binding: **OPEN**.

Successful pinned run: `output/run-SU3YmHP0`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
Fin6IndexAdapter_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
FUNCTION_LEVEL_FRAME_BINDING=OPEN
FUNCTION_LEVEL_MASS_BINDING=OPEN
```

Hashes:

```text
Fin6IndexAdapter.lean  E795E93744A18D7C1BE84890D4AB04FF41E8F9BF480F11ACABE4A3B32684903D
Fin6IndexAdapter.olean D04E17A05C56BB58944943D4EB49051840563D97557F427475C11E8BBAB820C8
terminal.log          BE358E29F0B4B372F247579830E442CF88850D29DA5E1210F009BF44D86F20FD
```

The first failed run `run-sqlPwqpY` and its repairs are retained.  The runner
was repaired to use the available POSIX `grep` instead of assuming `rg` inside
WSL.

The sidecar is not a formal Route-B certificate and is not entered into the
shared theorem registry.
