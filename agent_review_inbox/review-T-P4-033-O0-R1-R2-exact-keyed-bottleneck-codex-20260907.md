# T-P4-033 O0-R1/R2 — exact keyed bottleneck review

Date: 2026-09-07  
Scope: exact `K`, weighted baseline `rho_r`, and weighted perturbation
`epsilon_R` under one canonical source/state receipt. No existing ledger is
consumed; no O0 closure is claimed.

## Disposition

The workspace still has no consumable physical receipt. The useful result is a
conditional exact interface: if all fields below are supplied under one
canonical key, O0-R1/R2 arithmetic is closed. The current port candidate does
not meet it because it supplies only an unverified squared candidate and lacks
the exact-real inverse, metric, and physical source bindings.

## O0-R1 exact resolvent interface

Let `A_r=M_DD(mu_exact)`, `A_f=M_DD(mu_float)`,
`||A_r^(-1)||_n <= K`, and `||A_f-A_r||_n <= epsilon_A`.

`K` and `epsilon_A` are exact nonnegative rationals, `n` is one compatible
induced norm, and the inverse inequality has an authoritative exact-real
receipt with `proves_exact_real_bound=true`.

The exact gate and outputs are: `epsilon_A*K < 1`,
`K_f=K/(1-epsilon_A*K)`, and
`DeltaK=epsilon_A*K^2/(1-epsilon_A*K)`.

For `B=M_BD` and `C=DeltaM_DB`, same-key exact bounds
`||B_f-B_r||_n<=dB`, `||B_r||_n<=Br`, `||C_f||_n<=Cf`, and
`||C_f-C_r||_n<=dC` give
`U_R=dB*K_f*Cf + Br*DeltaK*Cf + Br*K*dC`.

Every quantity must share the same `source_key`, evaluator semantics,
cell/domain key, block orientation, and norm convention. A numeric `K` without
the exact-real receipt is an obstruction even when `epsilon_A*K<1` numerically.

## O0-R2 weighted construction

The preferred direct statements are:

- `||R_r a_B||_2^2 <= rho_r^2*A_up`;
- `||(R_f-R_r)a_B||_2 <= epsilon_R*sqrt(A_up)`;
- `A_up=a_B^T*B_up*a_B`.

`rho_r` and `epsilon_R` must be exact nonnegative rationals in the same
left-output `B_up` metric. Equivalently, with `B_up=S^T*S`, require
`||R_r*S^(-1)||_2<=rho_r` and
`||(R_f-R_r)*S^(-1)||_2<=epsilon_R`.

If only unweighted induced-2 bounds are available, the exact same-key
conversion requires `B_up>=beta*I`, `beta>0`, `s>0`, `s^2<=beta`,
`||R_r||_2<=U_r`, and `||R_f-R_r||_2<=U_delta`; then
`rho_r=U_r/s` and `epsilon_R=U_delta/s`.

This division is only a conditional conversion. It does not prove the metric
lower bound or the physical identity `R_port a_B=r_B`.

If the baseline is supplied as a squared bound `g_r`, the receipt must provide
an exact rational witness `rho_r>=0` and prove `g_r<=rho_r^2`. The field `g_r`
must never be passed as `rho_r` to O0-R3.

## Minimal canonical join fields

The smallest receipt must contain these fields:

- `schema=routeb.o0.r1r2.exact_keyed_receipt.v1`, `status`, `receipt_id`;
- `source_key` and `state_key`, with canonicalized source hashes, cell/domain,
  evaluator state, coordinate order, and metric orientation;
- exact/Float64 `mu` semantics, FD step, force scale, coefficient revision,
  and rounding/interval mode;
- `norm`, `M_DD(mu_exact)`, exact rational `K`,
  `proves_exact_real_bound=true`, and its pinned proof/interval receipt;
- exact `epsilon_A`, `dB`, `Br`, `Cf`, `dC`, plus derived exact `K_f`, `DeltaK`,
  and `U_R` with `epsilon_A*K<1`;
- `B_up`, exact `beta`, exact `s`, proofs `s>0`, `s^2<=beta`, and
  `B_up>=beta I` under the same key;
- exact weighted `rho_r` and `epsilon_R` with separate baseline and
  perturbation proof receipts;
- key equalities: all source keys equal, all state keys equal, and all norm
  conventions equal.

The physical adapter must additionally attach a typed proof receipt for
`R_port a_B=r_B`; otherwise the join remains non-physical and pending.

## Minimal counterexamples

1. **Numeric `K` is not authority.** Take scalar candidate `K=1` and
   `epsilon_A=1/2`. If the actual exact-real block is `A_r=1/4`, then the
   true inverse norm is `4` and the true product is `2>=1`; the resolvent
   conclusion is false. The default `proves_exact_real_bound=false` must reject
   before computing `K_f` or `DeltaK`.

2. **Squared/root confusion.** Let scalar `B_up=1` and `R_r=1/2`. The valid
   squared bound is `g_r=rho_F^2=1/4`, while the valid root is `rho_r=1/2`.
   Passing `1/4` as `rho_r` asserts `1/4<=1/16`, which is false.

3. **Metric/source mismatch.** Let `||R||_2<=1`, but actual scalar
   `B_up=1/4`. The weighted gain is `||R*B_up^(-1/2)||=2`. Reusing `s=1`
   from another source returns the false bound `rho=1`.

4. **Norm mismatch.** An infinity-norm `K` and a 2-norm `epsilon_A` cannot be
   multiplied in the Neumann condition without an exact conversion receipt.

## Smallest next child

Produce one cell (or an explicitly uniform domain) with exact `K`,
`epsilon_A`, `dB`, `Br`, `Cf`, `dC`, `s`, `beta`, `rho_r`, and `epsilon_R`,
plus all key equalities and proof-status flags. If exact-real `K` authority,
the metric lower-bound proof, or `R_port a_B=r_B` is absent, return an explicit
obstruction rather than a candidate weighted bound.

