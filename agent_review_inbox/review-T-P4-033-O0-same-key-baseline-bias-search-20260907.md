# T-P4-033 O0 — same-key baseline/bias search

**Result:** `OBSTRUCTION`; no strict-Schur-consumable receipt found.

This is a narrow search of the current O0 source/metric material. No old Float64 ledger, `rho_F^2), unit normalization, Schur consumption, state mutation, or registry action was used.

## Same-key material actually available

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

The same-key exact port tuple is:
```text
K = 1194377771728717533600000000 / 18430531027503268060090421
Br = 320646431 / 2400000000
Cf = 1929397 / 4800000000
delta = 3339 / 73786976294838206464000000
epsilon_R(infinity) =
10884976891854242252555776013990910667449238154978439
/
1066565541595672284169870837304452361645809004477199488549594864814784000000
```

The same-key metric adapter also records
```text
B_up = diag(1402217/12000000, 200739/4000000)
beta = 200739/4000000
s = 1/5
s^2 = 1/25
beta - s^2 = 40739/4000000
epsilon_R(2,weighted) = 2*epsilon_R(infinity)/s
```
These are metric/port facts only; they do not define the physical baseline budget.

## Rejected apparent baseline candidate

The global-coverage receipt reports the exact rational
```text
regularized_global_lower = 1/1000000
```
but its scope is global interval/Taylor coverage, its status is `blocked_global_true_dh_coverage), and it supplies no exact-Fourier `source_key`, cell `state_key), weighted metric key, or theorem of the form
```text
baseline_budget(q,a_B) >= L_base * A_up(q,a_B)
```
It also leaves global residual absorption open. Therefore `1/1000000) is not a same-key `L_base) receipt and is not consumed.

## Exact consumer assumptions still missing

For `A_up=a_B^T B_up(q)a_B), a valid baseline child must bind the above keys and prove:
```text
B_up(q) is PSD
baseline_budget(q,a_B) >= L_base*A_up(q,a_B) for all a_B
L_base is an exact rational, L_base >= 0
baseline_budget has a typed physical identity
```
For fixed exact `theta>0), `lambda=1+1/theta), the strict consumer is:
```text
m_r = L_base - lambda*rho_r^2
m_f = L_base - lambda*(rho_r + epsilon_R)^2
m_f > 0
```
Thus a numeric lower bound on a different source/domain cannot be substituted for `L_base).

A relative affine receipt additionally needs the same-key physical identity `r_B=R_rel*a_B+b_B) and exact:
```text
||R_rel*a_B||_2^2 <= rho_relative^2*A_up
||b_B||_2^2 <= beta_bias*A_up
beta_bias >= 0
tau > 0
(1+tau)*rho_relative^2 + (1+1/tau)*beta_bias <= rho_bias^2
L_base > lambda*(rho_bias + epsilon_R)^2
```
The absolute alternative needs `||b_B||_2^2<=beta_abs) plus an exact positive same-key reserve `m_add>(1+1/tau)*beta_abs).

## Minimal obstruction

No searched artifact contains the required same-key fields:
`baseline_budget), exact `L_base), physical residual identity, `R_rel), `b_B), `beta_bias), `beta_abs), or `m_add). The available exact port tuple and metric lower bound therefore cannot consume the strict Schur margin.

