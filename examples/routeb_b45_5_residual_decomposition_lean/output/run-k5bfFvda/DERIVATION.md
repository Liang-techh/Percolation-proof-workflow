# Derivation contract

The source audit writes the actual block force as

```text
r_B = -K_B q_B - B_B v_B + u_B w + G0_B - C_B - G_B.
```

The PMI nominal force after multiplying by `D_B=diag(1/5,1/10)` is

```text
D_B f_B = -K_B q_B - B_B v_B + u_B w
          - diag(3/20,2/25) q_B + (q5/100,q4/200).
```

The descriptor premise is represented by

```text
r_B = M_BB a_B + remote_B.
```

Subtracting `D0 a_B`, with `D0=diag(1/5,1/10)`, gives the theorem in the
Lean sidecar.  The theorem is conditional algebra: `sourceForce` is a compact
exact-real source-force interface and `hdesc` is the explicit source descriptor
binding premise.  No bound, source implementation equality, reachability, or
Float64 statement is hidden in the theorem.

