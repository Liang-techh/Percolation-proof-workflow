# T-P4-033 O0-R1/R2 — same-key perturbation-map check

Date: 2026-09-07  
State read-only snapshot: revision 504  
Status: `OBSTRUCTION_NO_SAME_KEY_PERTURBATION_RECEIPT`  
Scope: search for an actual same-key bound on `R_f-R_r`; do not repeat the
`rho` square-root arithmetic and do not consume the existing port candidate.

## Conditional reduction found

The O0 rounding receipt records zero off-diagonal regularizer shifts:
`M_BD,f-M_BD,r=0` and `M_DB,f-M_DB,r=0`. If `M0_DB` is also bound to the same
source/state key, then the O0-R1 three-term estimate simplifies from

`dB*K_f*Cf + Br*DeltaK*Cf + Br*K*dC`

to

`U_delta = Br*Cf*DeltaK`

with the exact conditional substitutions

`DeltaK = delta*K^2/(1-delta*K)` and `delta*K<1`.

Therefore a same-key weighted perturbation child could use

`epsilon_R = Br*Cf*delta*K^2 / ((1-delta*K)*s)`

provided all of the following are proven under one canonical key:

- exact-real `K >= 0` with `proves_exact_real_bound=true`;
- exact `delta`, exact `Br >= ||M_BD,r||`, and exact `Cf >= ||DeltaM_DB,f||`;
- `delta*K<1` in the same induced norm;
- exact `B_up >= beta I`, `s>0`, `s^2<=beta`, with the same left-output metric;
- the zero-shift equalities and the identity of the map being bounded.

This is a useful symbolic child interface, not a current receipt.

## Why no actual same-key bound was found

The available artifacts do not contain the required tuple
`(K, Br, Cf, source_key, state_key)`:

1. `routeB_compact_port_frobenius_ledger.csv` and its input partition export a
   bound for one normalized map `T=R*B_up^(-1/2)`. They do not export separate
   maps `R_r`, `R_f`, or `R_f-R_r`, and have no canonical `source_key` or
   `state_key` for an O0 perturbation join.
2. `task_routeb_o0_rounding_bridge_audit/RECEIPT.json` explicitly marks
   `M_DD_inverse_bound=false` and `R_port_bound=false`; its zero off-diagonal
   shift is only a matrix-entry fact and does not supply `K`, `Br`, or `Cf`.
3. The exact-real inverse flag is fail-closed by default. A numerical DD
   inverse value cannot be substituted for the authoritative `K` needed in
   `DeltaK`.
4. Existing `rho2_m0`/mass/Euclidean fields are bounds in distinct metric or
   map roles. None is an enclosure of `R_f-R_r`; subtracting two unrelated
   upper bounds is not a perturbation theorem.
5. The physical typed equality `R_port*a_B=r_B` remains absent, so even a
   future algebraic `epsilon_R` would not yet be a physical residual bound.

## Minimal obstruction

The smallest missing receipt is a same-key exact-real perturbation receipt
containing:

`source_key`, `state_key`, `K`, `proves_exact_real_bound=true`, `delta*K<1`,
`Br`, `Cf`, the zero-shift equalities, and either a direct weighted
`epsilon_R` or the exact metric witness `s` needed by the displayed formula.

If the zero-shift premise is not accepted as authoritative, the receipt must
instead supply exact `dB` and `dC` and use the unreduced bound

`epsilon_R = (dB*K_f*Cf + Br*DeltaK*Cf + Br*K*dC)/s`.

Until this tuple is present, the correct result is
`PENDING/OBSTRUCTION_NO_SAME_KEY_PERTURBATION_RECEIPT`; the candidate
`rho_27`/`rho_56` values cannot be joined to it, and O0-R1/R2 must not be
reported as consumed.

