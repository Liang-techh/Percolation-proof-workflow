# T-P5-043 direct two-channel feasibility gate — Lean sidecar

This portable sidecar formalizes the **source-independent algebraic elimination layer** from 狂蛮魔尊 `T-P5-043`.

It proves, in pinned Lean/Mathlib:

- a signed one-radical square-free iff;
- a signed two-radical square-free iff, retaining both required positivity guards;
- exact denominator-clearing bridges for E/E, I/E, E/I and I/I branch costs;
- the I/E, E/I and I/I review-form polynomial gates with strict inequalities;
- a branch-cost FAIL corollary;
- exact rational regressions for a strict I/I PASS, a boundary-only I/I equality, and the two sign-guard counterexamples.

## Typed boundary

This sidecar **does not** re-prove the T-P5-042 optimization theorem that identifies the endpoint/interior branch infima of

`g(rho)=((R-rho)^2/m+C)/(a-rho)`.

Accordingly, its direct branch theorems consume the already-derived endpoint/interior cost formula as their semantic input.  Lifting a branch-gate FAIL to the stronger statement “no admissible `rho4,rho5` exist” still depends on the T-P5-042 infimum/attainment bridge (including the degenerate non-attained `R=a,C=0` case).

Also out of scope: concrete signed `(u,x)` source-row binding, anchor/FD/controller/solve bias, Float64 or true-DH semantics, P8 coverage/flowpipe, provenance/admission, P5/P8/M4 closure, and registry mutation.

## Verification

From this directory, with the repository pinned `examples/local_fkg` environment available and `lake`/`lean` on `PATH`:

```bash
./verify.sh
```

The verifier compiles with `-DwarningAsError=true`, requires every public theorem's `#print axioms` report, rejects `sorryAx`, and rejects `sorry`/`admit` placeholders.

Status after a successful focused compile remains **compiled_candidate** only: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
