# Route-B P4 sharp residual bridge

This sidecar formalizes the exact scalar interface identified by `T-P4-005`:

```text
forall x, 0 <= p*x^2 + 2*x*r + d*y^2
  <-> r^2 <= p*d*y^2       (p > 0)
```

It also proves the triangle/envelope bridge from three force-side residual
pieces and verifies that the rational coefficient `c=1/4` is strictly below
the concrete `p*d` budget `350003000000001/5000000000000000`.

This is an exact-real child only. It does not bind `r` to deployed Julia/DH
semantics, prove cell coverage, or promote P4/M4.
