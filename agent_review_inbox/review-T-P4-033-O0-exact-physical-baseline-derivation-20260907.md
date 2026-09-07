# T-P4-033 O0 — exact physical baseline derivation from Newton–Euler mass block

**Result:** `CONDITIONAL_EXACT_SAME_KEY_BASELINE_DERIVATION`; exact rational child found, not yet a consumable physical receipt.

## Key

```text
source_key =
routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
|mu=1/1000000|contract=exp(i*nu*q)

state_key =
routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)
|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity

metric_key =
weighted-port:s=1/5|output_norm=euclidean_2|orientation=left-output
```

No global lower, unit normalization, old Float64 ledger, Schur consumer, or registry action is used.

## Exact derivation

The exact Fourier source has no nonzero ((4,5)) or ((5,4)) coefficient. Summing all exact real Fourier coefficients at q=0 and adding the exact-real `mu=1/1000000) diagonal gives
```text
M_BB^mu(0)
 = diag(7/60 + 1/1000000, 40147/800000 + 1/1000000)
 = diag(350003/3000000, 200739/4000000).
```

The same-cell exact Fourier enclosure supplies
```text
||M_BB^mu(q)-M_BB^mu(0)||_infinity <= d
d = 147/800000000.
```

Assuming the physical mass block is symmetric, `||E||_2 <= ||E||_infinity` for `E=M_BB^mu(q)-M_BB^mu(0)`. Hence
```text
a_B^T M_BB^mu(q) a_B
 >= (200739/4000000 - 147/800000000) ||a_B||_2^2
 = (40147653/800000000) ||a_B||_2^2.
```

The same-key weighted metric receipt supplies
```text
B_up = diag(1402217/12000000, 200739/4000000)
A_up = a_B^T B_up a_B
A_up <= (1402217/12000000) ||a_B||_2^2.
```

Therefore the exact relative baseline factor is
```text
L_base =
(40147653/800000000) / (1402217/12000000)
= 120442959/280443400 > 0,
```
and the conditional physical inequality is
```text
baseline_budget(q,a_B) := a_B^T M_BB^mu(q) a_B
 >= (120442959/280443400) * A_up(q,a_B).
```

For a future exact `theta>0), the strict Schur condition becomes the concrete rational gate
```text
(1+1/theta) * (rho_r + epsilon_R)^2
 < 120442959/280443400.
```
The resulting leftover is
```text
m_f = 120442959/280443400
      - (1+1/theta)*(rho_r+epsilon_R)^2 > 0.
```
No `rho_r) or `epsilon_R) candidate is consumed here.

## Unbound source premises

The derivation is not promoted to a physical receipt because these premises are not yet bound by the current exact-key receipt:

1. The exact Fourier table must be proved to equal the real Newton–Euler mass block `M^mu(q)), with the same exact `mu=1/1000000), not merely be an algebraic Fourier precursor.
2. The q=0 coefficient sum and the zero off-diagonal support must be accepted as the authoritative `M_BB^mu(0)) for this source key.
3. The reported `dMBB_inf_bound=147/800000000) must be an authoritative all-q cell enclosure for the same source/state key.
4. `M_BB^mu(q)) must be symmetric in the exact-real semantics used by the norm conversion.
5. The physical energy identity must bind `baseline_budget(q,a_B)` exactly to `a_B^T M_BB^mu(q) a_B`.
6. The weighted adapter's `B_up) matrix must be accepted as the same physical metric in the canonical O0 receipt, including its Euclidean-2 left-output convention.
7. A separate physical residual identity `R_port*a_B=r_B), or an exact affine decomposition with `R_rel,b_B), is still absent. The physical descriptor bridge only gives
   `a_D=S y+r_hat z/rho` and
   `M_BD a_D=(M_BD S)y+(M_BD r_hat)z/rho`; it does not bind this port to the O0 `a_B)-residual consumer.

Thus this child supplies a non-normalized exact `L_base) derivation, but strict Schur consumption still requires the listed source/semantic bindings and a same-key `rho_r,epsilon_R) residual receipt.

