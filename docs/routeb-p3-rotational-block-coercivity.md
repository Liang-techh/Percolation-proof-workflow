# Route-B P3: structural block-(4,5) coercivity candidate

This note records a non-sampling mathematical candidate for T-P3-011.  It is
stronger than the global `10^-6 I` regularizer bound, but it is not yet a
kernel theorem for the Float64 implementation.

## Exact-real link-level derivation

For a block vector `u_B=(u4,u5)`, the rotational part of the deployed mass
construction contributes, for link `i`,

```text
u_Bᵀ Jω_iᵀ (I_val[i]/3) I Jω_i u_B
  = (I_val[i]/3) ||Jω_i u_B||².
```

The source loop has `Jω[:,j]=z[:,j]` for `j<=i` and zero otherwise.  Hence
links 1–3 do not contribute to this principal block, while links 4–6 give

```text
link 4: (I4/3) u4²,
link 5: (I5/3) ||u4*z4 + u5*z5||²,
link 6: (I6/3) ||u4*z4 + u5*z5||².
```

The fourth DH twist is `alpha4=-pi/2`.  In the exact-real DH matrix this
implies `z4·z5=cos(alpha4)=0` and `||z4||=||z5||=1`.  With the source values

```text
I4=1/5, I5=1/10, I6=1/20,
```

the displayed rotational terms sum to

```text
(1/5)/3*u4² + ((1/10)+(1/20))/3*(u4²+u5²)
  = (7/60)u4² + (1/20)u5².
```

All translational terms and all omitted rotational terms are positive
semidefinite.  Therefore the exact-real, unregularized structural target is

```text
M_BB^(0)(q) ⪰ diag(7/60, 1/20)  for every q.
```

If the source's explicit regularizer is included, the corresponding target is

```text
M_BB^(1e-6)(q) ⪰ diag(7/60+1e-6, 1/20+1e-6).
```

Consequently, for a symmetric positive block,

```text
lambda_min(M_BB^(0)) >= 1/20,
||M_BB^(0)^(-1)||₂ <= 20,
lambda_min(M_BB^(1e-6)) >= 1/20+1e-6,
||M_BB^(1e-6)^(-1)||₂ <= 20,000,000/1,000,001.
```

The same operator-norm bound is a safe entrywise bound for the inverse matrix.

## Admission boundary

This derivation assumes exact-real rotation identities.  The deployed Julia
code evaluates `sin`, `cos`, and `pi` in `Float64`, so the following child
obligations remain open:

1. bind the source `Ri`, `z4`, `z5` values to an exact-real or directed-rounding
   rotation contract;
2. prove symmetry and the principal-block restriction for the same regularizer;
3. preserve the distinction between the unregularized physical DH matrix and
   the deployed `1e-6` implementation;
4. feed the resulting lower bound into the P4/P7 inverse and residual ledger.

Thus this is a `rigorous-structure candidate`, not `VERIFIED`; it does not
close P3, P4, P7, or M4 and does not enable the formal certificate gate.
