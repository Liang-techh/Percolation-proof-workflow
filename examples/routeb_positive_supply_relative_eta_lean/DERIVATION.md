# Derivation and scope

## Exact scalar lemma

The frozen `(e4+e5)` slice has

```text
A = 2002229/24000000,
D = 29/20,
K = 36802229/24000000 = A + D.
```

For `0 <= tau <= 1` and `kappa < K`,

```text
A + tau*D - tau*kappa
  = (1-tau)*A + tau*(A+D-kappa) > 0.
```

If `|etaU| <= kappa*rho`, then `etaU <= kappa*rho`, hence

```text
rho*(A+tau*D) - tau*etaU
  >= rho*(A+tau*D-kappa*tau) > 0.
```

Multiplication by `rho > 0` gives the requested strict denominator result.
The Lean proof makes the endpoint/convex-combination argument explicit.

## Direct-gate alternative

Define

```text
Residual = E - a1*denominator
directGate := Residual <= b.
```

The leaf proves, with no denominator sign and no division,

```text
directGate <-> E <= b + a1*denominator.
```

This is the appropriate interface for a small-`rho` branch or an
equilibrium supply-floor branch. The relative-eta theorem can be conjoined
when the division route is needed, but the direct gate itself does not depend
on that positivity theorem.

## Explicit non-claims

The scalar `etaU` is an abstract real parameter. The leaf does not prove that
it is a projection of the true-DH source defect, does not prove the relative
bound from any physical implementation, and does not prove a polynomial
supply budget, continuation, reachability, or `J <= 1`.
