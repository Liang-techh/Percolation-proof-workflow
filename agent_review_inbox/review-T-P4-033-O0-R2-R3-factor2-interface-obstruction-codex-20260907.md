# T-P4-033 O0-R2/R3 — factor-2 weighted adapter join and strict-margin boundary

Date: 2026-09-07  
Observed state: revision 508  
Scope: exact-Fourier one-cell child only; no ledger consumption, registration,
or O0 closure.

## Verdict

The compiled Fin-2 theorem and the exact-Fourier output-2-norm receipt compose
at the scalar interface, but the O0-R3 consumer is still not callable. The
same exact-Fourier key has a proved weighted perturbation bound, while no
authoritative same-key weighted baseline `rho_r`, baseline remaining margin
`m_r`, or fixed `theta` is present.

The obstruction is therefore a missing strict-margin receipt, not a factor-2
or rational-arithmetic failure.

## Same-key adapter data

Use exactly these keys from the accepted exact-Fourier child:

```text
source_key = routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)
state_key  = routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
```

The metric fields are

```text
B_up = diag(1402217/12000000, 200739/4000000)
beta = 200739/4000000
s = 1/5 > 0
s^2 = 1/25 <= beta
```

The compiled theorem supplies the exact output conversion

```text
||y||_2 <= 2 ||y||_infinity    for y : Fin 2 -> R.
```

Consequently, from the accepted exact-Fourier infinity bound `U_infinity`,

```text
epsilon_2_weighted = 2*U_infinity/s = 10*U_infinity
 = 10884976891854242252555776013990910667449238154978439 /
   106656554159567228416987083730445236164580900447719948854959486481478400000
```

and the exact statement to hand to R3 is

```text
forall a_B,
  ||(R_f - R_r) a_B||_2
    <= epsilon_2_weighted * sqrt(a_B^T * B_up * a_B).
```

This uses the factor `2` and `s=1/5`; the arithmetic agrees with
`receipt-T-P4-033-O0-exact-fourier-cell-weighted-port-adapter-output-2norm-20260907.json`.
It remains a one-cell exact-Fourier conditional bound, not a deployed
Float64/global bound.

The norm tags must remain split at the join: the source tuple is bounded in
`induced_infinity`, while the R3 baseline/perturbation metric is `euclidean_2`
with the displayed `B_up`. A canonical consumer should therefore record both
`source_bound_norm=induced_infinity` and `metric_output_norm=euclidean_2`; it
must not relabel the former as the latter.

## Exact R3 join interface

A same-key baseline receipt must add an exact nonnegative `rho_r` in the same
left-output Euclidean metric:

```text
forall a_B,
  ||R_r a_B||_2 <= rho_r * sqrt(a_B^T * B_up * a_B).
```

The equivalent square-only form is accepted only together with an exact root
witness:

```text
forall a_B, ||R_r a_B||_2^2 <= g_r * (a_B^T * B_up * a_B),
0 <= g_r <= rho_r^2,
rho_r >= 0.
```

The same receipt must provide a fixed exact `theta > 0` and a proved positive
baseline remaining margin `m_r > 0`, all carrying the exact `source_key`,
`state_key`, cell, orientation, and metric tags above. The only scalar join
is

```text
lambda = 1 + 1/theta
charge = lambda * ((rho_r + epsilon_2_weighted)^2 - rho_r^2)
       = lambda * (2*rho_r*epsilon_2_weighted
                   + epsilon_2_weighted^2)
strict remainder: charge < m_r
leftover: m_f = m_r - charge > 0.
```

The canonical receipt auditor correctly requires `leftover > 0`. The lower
level `consume_routeb_schur_margin` helper accepts zero leftover as a
nonnegative arithmetic budget, so strict physical use must retain the
additional `m_f > 0` check.

## Why current candidates cannot be joined

The exact-Fourier port CSV exposes fields such as
`rho2_frobenius=4227/500000` (eta 2.7) and
`rho2_frobenius=34547/1000000` (eta 5.6), with candidate `theta`, charge, and
margin columns. Those rows have no canonical `source_key`/`state_key`, do
not prove that the squared quantity bounds the actual `R_r` in the current
`B_up` metric, and do not provide the typed physical baseline theorem. They
cannot be passed as `rho_r`, and their candidate margin cannot be renamed
`m_r`.

The earlier rational roots `rho_27=9195/100000` and
`rho_56=1859/10000` are valid arithmetic upper-root witnesses only if a new
receipt first proves the corresponding squared bounds for the actual `R_r`
under this exact key. They do not repair the missing baseline proof or
remaining-margin provenance.

## Minimal missing receipt

One exact-Fourier cell receipt must add:

1. `weighted_baseline.map = R_r`, exact `rho_r >= 0` (or `g_r` plus exact
   root witness), and a proof in the same `B_up`, output-2 metric;
2. fixed exact `theta > 0`, `lambda = 1 + 1/theta`, and exact `m_r > 0`
   after the baseline Schur charge;
3. the exact strict inequality
   `lambda*((rho_r+epsilon_2_weighted)^2-rho_r^2) < m_r` and its positive
   leftover;
4. unchanged source/state/norm/orientation equality, plus the physical
   `R_port*a_B=r_B` proof if the child is to be called physical.

Until these fields exist, the correct result is
`OPEN_FAIL_CLOSED: same_key_weighted_baseline_and_strict_margin_missing`.
No `rho_F^2`, old Float64 ledger, or unkeyed candidate margin is consumed.

## Existing evidence

- `agent_review_inbox/receipt-Fin2NormConversionCandidate-pinned-20260907.json`
  — compiled factor-2 theorem receipt;
- `agent_review_inbox/receipt-T-P4-033-O0-exact-fourier-cell-weighted-port-adapter-output-2norm-20260907.json`
  — same-key conditional weighted perturbation;
- `artifacts/routeb_6dof/state.json` — records the output-2 adapter but keeps
  `schur_margin_consumed=false` and the R3 baseline/margin fields unavailable.

```text
main_state_modified = false
registry_promoted = false
schur_margin_consumed = false
```
