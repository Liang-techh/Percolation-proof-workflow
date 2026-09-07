# T-P4-033 O0-R3 — same-key physical ledger review

Date: 2026-09-07  
Scope: only the O0-R3 consumer after `consume_routeb_schur_margin` landed.  This is a read-only review; it does not promote O0, modify the main state, or consume a Schur margin.

## Verdict

There is currently **no consumable same-key physical pair**

```text
(weighted baseline rho_r, remaining Schur margin)
```

in the workspace.  The available records are either conditional numerical candidates, use a different physical quantity, or lack the source/state key required by the O0-R3 API.

## Exact O0-R3 contract

For one fixed cell/state key and one fixed rational `theta > 0`, the required
baseline and perturbation statements are

```text
||R_r a_B||_2^2 <= rho_r^2 * A_up,
|| (R_f - R_r) B_up^(-1/2) ||_2 <= epsilon_R,
A_up := a_B^T B_up a_B >= 0.
```

The second line may equivalently be supplied as
`|| (R_f-R_r) a_B ||_2 <= epsilon_R * sqrt(A_up)`.  Both constants must be
exact rationals in the same left-output weighted metric and under the same
source/state key.  Then

```text
rho_f <= rho_r + epsilon_R,
added_charge(theta) = (1 + 1/theta) * ((rho_r+epsilon_R)^2-rho_r^2).
```

If `m_r` is the already remaining baseline Schur margin in that same cell and
normalization, the minimal consumer inequality is

```text
added_charge(theta) <= m_r
```

with leftover `m_f = m_r-added_charge(theta)`.  A strict physical Schur
certificate additionally needs `m_f > 0`; equality is only a nonnegative
budget result.  In the equivalent fixed-`lambda` form, `lambda=1+1/theta`
and the charge is `lambda*((rho_r+epsilon_R)^2-rho_r^2)`.

If the ledger stores only a squared number `g_r = rho_r^2`, it must also supply
an exact rational witness `rbar_r >= 0` with `g_r <= rbar_r^2`; O0-R3 then
consumes `rbar_r`, not `g_r` as if it were `rho_r`.

## What is present, and why it does not bind

### 1. Resolved-cell port candidate

`P4.residual_port_frobenius_bound` is still `status=open`,
`verified_artifact=null`, `registry_eligible=false`, and
`comparator_accepted=false` at state revision 500.  It records candidate rows

```text
eta=2.7: rho_F^2=4227/500000, charge=4227/100000,
         candidate margin=15773/100000
eta=5.6: rho_F^2=34547/1000000, charge=34547/200000,
         candidate margin=5453/200000
```

but these are not an O0-R3 receipt: the metadata has no canonical
`source_key`/`metric_source_key`, stores `rho_F^2` rather than a rational
`rho_r` witness, and leaves open the typed `R_port*a_B=r_B` binding,
regularized force-scale binding, true-DH/Float64 semantics, interval replay,
full coverage, and coefficient-level absorption.  Its source and cover hashes
are artifact provenance, not the same-key theorem binding required by
`consume_routeb_schur_margin`.

The recorded `rho2_induced` cannot repair this gap: the independent replay
records cells where the Frobenius candidate exceeds the induced candidate (22
cells for eta 2.7 and 39 for eta 5.6).  No pointwise substitution between the
two norms is admissible without a separate metric theorem.

### 2. Physical Schur ledger

`artifacts/task_DP_physical_schur_margin_20260906/ledger.json` is explicitly
`BLOCKED_MISSING_A_GT_MU_AND_PHYSICAL_COUPLING_RECEIPT`.  Its conditional
formula is

```text
E_mu = mu*B_BD*B_DB/(A*(A-mu)),
M_lower = 1-rho_reg-E_mu,
```

with gates `A > mu` and `rho_reg+E_mu < 1`.  It explicitly has no admitted
same-domain physical `A > mu`, no metric-compatible outward-rounded physical
`B_BD,B_DB`, no checked BU resolvent bridge, and no complete zero-unresolved-box
coverage.  Consequently it supplies neither a numeric weighted `rho_r` nor a
remaining margin `m_r` consumable by O0-R3.  The `rho_reg` in this report is not
silently identified with the weighted port gain `rho_r`.

### 3. Downstream adapter

`P4.combined_schur_port_energy_adapter` remains open.  Its interface correctly
uses `rho=rho_F^2` and `A=A_up`, but its typed `l_base`/`A_up` binding and
residual PMI/flowpipe consumption are unresolved.  The diagnostic interface
consistency pass is not a proof or a same-key physical receipt.

## Minimum receipt needed to unblock O0-R3

One per-cell (or one uniform-domain) receipt must contain all of the following,
under one canonical key `K`:

1. `K` binds source paths and hashes, true-DH versus deployed Float64
   evaluator semantics, exact `mu`, FD step, force scale, coefficient version,
   interval/rounding mode, coordinate order, and the cell/domain state key.
2. A weighted baseline theorem for the actual `R_r` with exact rational
   `rho_r`, or `g_r` plus an exact rational upper-root witness.
3. A weighted perturbation theorem for the actual `R_f-R_r` with exact
   rational `epsilon_R`, in the same `B_up` and left-output norm convention.
4. A baseline Schur receipt with exact rational `m_r`, the same `theta` (or
   fixed `lambda`), the same `A_up`, `l_base`, coordinate order, and a proof
   that `m_r > 0` is the remaining budget after the baseline charge.
5. A checked identity tying the supplied port map to the physical residual,
   `R_port a_B = r_B`, plus domain/flowpipe coverage for every consumed cell.
6. The exact arithmetic check
   `lambda*((rho_r+epsilon_R)^2-rho_r^2) < m_r` for strict closure
   (or `<=` if only a nonnegative remainder is intended).

Until this receipt exists, O0-R3 is correctly fail-closed and no O0 closure
claim should be made.

## Added O0-R1 hard gate: inverse `K` is not numeric evidence

`RouteBExactResolventPremise.proves_exact_real_bound` now defaults to
`false`.  This is the correct admission boundary and applies before either
the common-base or quantitative-`epsilon_A` resolvent path may be consumed:

```text
proves_exact_real_bound = true
```

must be explicitly supplied by an authoritative exact-real receipt.  A
nonnegative/exact-rational-looking `K`, a floating-point inverse calculation,
or a DD numerical ledger does not establish
`||M_DD(mu_exact)^(-1)|| <= K`.  Without that receipt, O0-R1 must return
`OPEN_FAIL_CLOSED` with
`exact_real_inverse_bound_not_authoritatively_supplied`; the condition
`epsilon_A*K < 1` is not a usable theorem premise.

This propagates directly to O0-R3.  If `epsilon_R` was derived through the
resolvent chain, it is unavailable for physical consumption until the same
exact-real `K` receipt, the same `source_key`, and the same norm convention are
bound.  O0-R3 must therefore return obstruction even when a physical-looking
ledger contains numeric `K`, `rho_r`, and margin fields.  Such fields may be
retained as candidates, but cannot be passed to
`consume_routeb_schur_margin` as verified inputs.

The minimum O0-R1 receipt is: exact-real matrix/evaluator identity for
`M_DD(mu)`, exact rational `K >= 0`, a proof certificate or pinned theorem
showing the stated induced norm bound, the norm convention, domain/cell
coverage, and the canonical `source_key` shared with `epsilon_A`, `B/C`,
`B_up`, `rho_r`, and `m_r`.  Only after this receipt and
`epsilon_A*K < 1` may the resulting `K_f`, `DeltaK`, and `epsilon_R` be
considered inputs to the O0-R3 inequality above.

## Evidence snapshot

```text
state: artifacts/routeb_6dof/state.json
state revision: 500
state sha256: F50FBC724308C228460CD2FE3D313C22589F0564C9556A142482A6D6152E76D8
physical report sha256: BBB491B4453BD7814175F9BF6981C5A523E3CA50160FAF8D9658E94B128CD4D7
physical ledger sha256: 6E4D5CB800AF58141914CFAE2EE75DCAAD571B1C84DE636A8C91200098A69DD9
main state modified by this review: false
registry promotion by this review: false
```
