# P3 central-FD to derivative-hull bridge

Status: mathematical candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_INTERFACE.lean` records the exact-real, source-independent
bridge needed to consume a central finite-difference derivative enclosure.
The file uses arbitrary finite index types and fixes only the slot convention

```text
T[k,i,j] = derivative in coordinate k of observable (i,j).
```

The new directory is intentionally isolated. No state, registry, shared script,
source snapshot, or other agent artifact was modified.

## Closed algebraic seams

1. `sourceCdq_eq_christoffelForce` is definitional equality between the nested
   source contraction and the generic tensor consumer. The bridge does not
   assume tensor symmetry and does not reorder the source slots.
2. `christoffelForce_add` proves exact tensor linearity. Therefore a finite-
   difference tensor `Tfd = T + R` can be split without changing the consumer.
3. If `|R[k,i,j]| <= mu[k,i,j]`, then

   ```text
   |Gamma_R[i,j,k]| <=
     (mu[k,i,j] + mu[j,i,k] + mu[i,j,k]) / 2.
   ```

   `fd_christoffel_component_error` lifts this to the velocity-quadratic force.
4. `fd_christoffel_power_error` keeps the tensor remainder as a tensor and
   gives a weighted cubic-power consumer. It does not collapse the remainder
   into six affine offsets.
5. `central_fd_remainder_decomposition` is an exact telescoping identity. The
   four terms are, in order:

   ```text
   machineValue - centralSecant
   centralSecant - derivative
   derivative - derivativeHullCenter
   derivativeHullCenter - exportedCenter.
   ```

   `central_fd_to_derivative_hull` counts each supplied radius exactly once and
   returns membership in the exported center plus the sum radius.

## Contract boundary

`CentralFDDerivativeHullContract` contains:

| field family | mathematical role |
|---|---|
| `eval`, `shift`, `step`, `centralSecant_spec` | exact definition of the central secant |
| `machineValue`, `machine_error` | a separately lifted/deployed value and its error to the exact secant |
| `derivative`, `central_error` | analytic derivative and central-FD truncation remainder |
| `derivativeHullCenter`, `derivativeHullRadius`, `derivative_hull` | independently supplied derivative hull |
| `exportedCenter`, `exportRadius`, `export_error` | serialization/export center discrepancy |

The contract requires nonnegative component radii and a nonzero step. It does
not manufacture any of these premises from a source hash, a sample, a CSV, or
an executable status.

## Explicit non-claims

This candidate does **not** prove:

- equality of a deployed Julia/DH evaluator with `eval` or `machineValue`;
- IEEE-754/libm rounding bounds, operation traces, or Float64-to-real lifting;
- a concrete Fourier coefficient bound or a value for `mu`;
- interval-cell coverage, boundary ownership, flowpipe inclusion, or terminal
  transfer;
- source semantics for mass, gravity, or Coriolis quantities;
- P3, P4, P5, M4, registry, or admission closure.

In particular, the central-FD algebraic theorem must not be read as replacing
the source's execution with analytic differentiation. A future source adapter
must instantiate `eval`, `shift`, `centralSecant`, and the four remainder
premises separately.

## Consumer map

| downstream use | supplied theorem/interface | still required outside this leaf |
|---|---|---|
| source `dM` index orientation | `sourceCdq_eq_christoffelForce` | source-semantic binding |
| exact-real FD tensor mismatch | `christoffelForce_add`, `fd_christoffel_component_error` | a same-domain `mu` premise |
| cubic P5 power charge | `fd_christoffel_power_error` | velocity/domain bound and downstream absorption |
| exported derivative interval | `central_fd_to_derivative_hull` | machine rounding, derivative hull, export evidence |

## Verification boundary

No local Lean/Lake command was run, by task constraint. The file is therefore
an uncompiled candidate pending an independent pinned-environment review. That
review should check imports, theorem elaboration, `#print axioms`, and the
absence of placeholders before any workflow integration. A successful compile,
if later obtained, would still be only a compiled candidate and would not
promote any registry or admission state.

