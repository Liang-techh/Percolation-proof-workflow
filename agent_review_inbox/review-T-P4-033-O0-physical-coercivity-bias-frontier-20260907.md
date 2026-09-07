# T-P4-033 O0 — physical coercivity / affine-bias frontier

**Disposition:** `OBSTRUCTION` (fail-closed; no consumable receipt)

本次只检查 exact-Fourier cell 是否已经给出同一 source/state/metric/orientation key 下的物理基线 coercivity 或 affine residual bias bound。没有使用 `L_base=1`，没有消费 `rho_F^2`、Float64 候选或旧 ledger，也没有消费 Schur margin、修改主 state 或注册 registry。

## Binding

```text
source_key = routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)
state_key = routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
metric_key = weighted-port:s=1/5|output_norm=euclidean_2|orientation=left-output
```

The checked source-side artifact is one conditional exact rational cell enclosure. It contains exact `MDD` inverse/resolvent and `MBD/MDB` perturbation data, but its evidence remains one-cell and port-side. It has no `baseline_budget`, `L_base`, physical residual identity, `R_rel`, `b_B`, `beta_bias`, `beta_abs`, or positive additive reserve.

The affine gain API computes
```text
gamma_bias = (1+tau)*rho_relative^2 + (1+1/tau)*beta_bias
```
but intentionally remains conditional unless authoritative relative and bias bounds, a fixed source key, and a root witness are supplied. It is not a physical receipt.

## Exact missing coercivity contract

For `A_up(q,a_B) = a_B^T B_up(q) a_B`, a consumable child must provide under the same keys and coordinate/orientation convention:
```text
B_up(q) is PSD
baseline_budget(q,a_B) >= L_base * A_up(q,a_B)    for every a_B
L_base : exact rational
L_base >= 0
```
and a typed physical identity for `baseline_budget`. For fixed exact `theta > 0), set `lambda = 1 + 1/theta`. The strict R1/R3 join is
```text
m_r = L_base - lambda*rho_r^2
m_f = L_base - lambda*(rho_r + epsilon_R)^2
m_f > 0
```
or equivalently `L_base > lambda*(rho_r + epsilon_R)^2). No unit normalization is implicit.

## Exact affine-bias alternatives

If the physical residual is `r_B = R_rel*a_B + b_B`, the relative interface requires the same-key exact statements
```text
||R_rel*a_B||_2^2 <= rho_relative^2 * A_up
||b_B||_2^2 <= beta_bias * A_up
beta_bias >= 0
tau > 0 exact
(1+tau)*rho_relative^2 + (1+1/tau)*beta_bias <= rho_bias^2
```
with an authoritative root witness. The strict baseline join is `L_base > lambda*(rho_bias + epsilon_R)^2).

The absolute alternative requires, with the same physical identity and keys,
```text
||b_B||_2^2 <= beta_abs
m_add > (1+1/tau)*beta_abs
```
where `m_add` is an exact positive additive reserve in the same physical storage and output norm. `beta_abs` cannot be renamed `beta_bias*A_up`.

## Minimal obstruction

The existing `Br/K/Cf` tuple permits both energy-side completions
```text
L_base = lambda*(rho_r + epsilon_R)^2       -> m_f = 0
L_base = lambda*(rho_r + epsilon_R)^2 + 1   -> m_f = 1
```
because no artifact field distinguishes them. Therefore `L_base` and positive reserve are not derivable from the port tuple. Also, `b_B != 0) and `a_B=0) give `A_up=0` but `||r_B||_2^2>0), so a homogeneous rho bound is false without relative bias control.

## Smallest next child receipt

Produce exactly one of: (1) same-key baseline coercivity with exact `B_up), PSD witness, `A_up), physical `baseline_budget`, exact `L_base), norm/orientation, and strict `m_f>0`; (2) same-key relative bias with physical `R_rel*a_B+b_B), exact `rho_relative`, `beta_bias), `tau), root witness, and the strict join; or (3) same-key absolute bias with exact `beta_abs) and positive exact `m_add). Until then O0 remains blocked. This is not an O0 closure claim.

