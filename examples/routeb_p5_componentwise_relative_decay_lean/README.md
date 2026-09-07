# Route-B P5 componentwise relative residual decay

Task: `T-P5-006`.

This sidecar formalizes the source-independent implication

```text
|r_i| <= rho_i |v_i|,  rho_i < d_i
------------------------------------------------
dE <= -sum_i (d_i-rho_i) v_i^2
```

and a uniform-rate corollary using `lambda <= d_i-rho_i`. It preserves the
coordinatewise damping structure and avoids collapsing the problem to a
coarse Euclidean minimum.

The relative residual premise must still be proved on the same covered
true-DH domain for the deployed force-error decomposition. This sidecar does
not establish source binding, coverage, flowpipe, or P5/M4 admission.
