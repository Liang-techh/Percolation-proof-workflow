# Verification report

Status: independently verified with `verify.sh` on 2026-09-06.

The sidecar is isolated under this directory and has no registry integration.
Its only Lean target is `AnthropicFLTReusable.lean`; the project pins Lean
`4.33.1`. The upstream snapshot's Mathlib revision is retained as provenance:
`db584cd6d46c92f209a44c0f1c829460d327499d`; this minimal API probe imports only
`Lean`, so the verifier does not clone or compile Mathlib.

The verification contract is:

- `LEAN_BUILD_EXIT_CODE=0` from `lake build`;
- source scan rejects `axiom`, `sorry`, `native_decide`, and `unsafe` in Lean files;
- the declaration output contains no axiom/sorry diagnostic;
- the final line reports `AXIOM_AUDIT=PASS`.

Observed result:

- `LEAN_BUILD_EXIT_CODE=0`;
- `P2M_TYPE_EQ AnthropicFLTReusable.reusableStatement AnthropicFLTReusable.reusableProof`;
- `AXIOM_AUDIT=PASS (no axiom/sorry diagnostics)`;
- no Lean warnings.

This is architecture/API reuse only. It is not Route-B theorem admission and
does not prove any PDE/ODE theorem, interval coverage, remainder enclosure,
flowpipe inclusion, or terminal-transfer obligation. A passing build therefore
must not be interpreted as `LEAN_VERIFIED`, comparator acceptance, or registry
promotion.
