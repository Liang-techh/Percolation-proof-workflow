# P3 Fin 6 central-FD hull consumer

Status: exact-real typed consumer candidate, pending independent review.

## Delivered specialization

`NEW_CENTRAL_FD_HULL_FIN6_CONSUMER.lean` specializes the derivative-first
central-FD remainder interface to `Fin 6`:

```text
T[k,i,j]   derivative-first reference tensor
R[k,i,j]   derivative-first remainder tensor
mu[k,i,j]  derivative-first nonnegative radius
```

It deliberately does not repeat the source/storage permutation. That is the
responsibility of `NEW_CENTRAL_FD_HULL_SLOT_ADAPTER.lean`.

## Consumer results

- `gamma6_abs_le_radius6` converts the tensor radius into the explicit
  three-term Christoffel coefficient radius.
- `fd_component_bound6` produces, for each `i : Fin 6`, the explicit
  velocity-quadratic bound

  ```text
  sum j,k, gammaRadius6 mu i j k * |v[j] * v[k]|.
  ```

- `fd_power_error6` aggregates the six component bounds into the typed power
  consumer

  ```text
  |sum i, v[i] * force_error[i]|
    <= sum i, |v[i]| * componentBound6 mu v i.
  ```

No `mu` values, velocity bounds, gains, or domain constants are selected.

## Composition with the slot adapter

For source-shaped data, first use

```text
T  := dmToDerivative dMtrue
R  := derivativeRemainder dMfd dMtrue
mu := dmRadiusToDerivative mu_source.
```

The hypotheses transported by `derivativeRemainder_radius` then match the
premises of `fd_component_bound6` and `fd_power_error6` exactly. Thus the
consumer sees no implicit index rewrite.

## Boundary

This leaf is only finite-dimensional exact-real algebra. It does not establish
that a concrete evaluator has the declared tensor semantics, does not provide
IEEE/Float64 rounding or operation traces, and does not prove any numerical
radius. It also does not establish interval coverage, flowpipe inclusion,
source binding, P3/P4/P5/M4 closure, admission, or registry promotion.

No local Lean/Lake command was run, as required. Independent review should
check elaboration, imports, `#print axioms`, and placeholder absence in the
pinned environment. Compilation, if later obtained, remains only a candidate
receipt and cannot itself close a workflow gate.

