# Route-B P4 O0 regularizer semantics bridge

This is the coordinator-side, exact-rational interface for the recorded
`Float64(1e-6)` fact. It is intentionally limited to the regularizer seam; it
does not bind the rest of `dhport_lib.jl`.

## Scalar contract

The bridge fixes the two values as exact rationals:

```text
mu_float64 = 4722366482869645 / 4722366482869645213696
mu_exact   = 1 / 1000000
delta      = mu_exact - mu_float64
           = 3339 / 73786976294838206464000000 > 0
```

Thus `mu_float64 < mu_exact`, and the outward scalar interval is
`[mu_float64, mu_exact]`. The larger rational `1/1000000` is not a lower bound
for the deployed regularizer.

`routeb_regularizer_fact()` returns this contract. The value is anchored to
the recorded binary64 bit pattern `0x3eb0c6f7a0b5ed8d`; the function does not
execute Julia or claim a libm/operation trace.

## Matrix and block propagation

`propagate_routeb_regularizer_diagonal(base_matrix)` accepts an exact-rational
common unregularized base. Under that explicit premise it constructs

```text
M_float = M0 + mu_float64 I
M_exact = M0 + mu_exact I
M_float = M_exact - delta I.
```

The returned `RouteBRegularizerInclusion` exposes `lower_matrix = M_float`,
`upper_matrix = M_exact`, and `difference_matrix = delta I`. With the current
one-based Route-B partition `B=(4,5)`, `D=(1,2,3,6)`, the same result is
available for `BB` and `DD`; `BD` and `DB` have zero shift. This is a
conditional regularizer propagation statement, not a Float64-to-exact
enclosure for the unregularized base.

`audit_routeb_regularizer_inclusion(float64_matrix, exact_real_matrix)` checks
the same relation for matrices that have already been converted to explicit
integer/`Fraction` representations. It rejects Python floats so a machine
output cannot silently become an exact-real input.

## Resolvent boundary

`derive_routeb_resolvent_port_propagation` is a separate consumer. It returns
`PENDING_RESOLVENT_PREMISE` unless the caller supplies an explicit
`RouteBExactResolventPremise` for the exact-real `M_DD(mu_exact)` inverse. If
`K >= ||M_DD(mu_exact)^(-1)||` and `delta*K < 1`, it returns only the
conditional bounds

The premise's `proves_exact_real_bound` flag defaults to false. It must be set
explicitly after an authoritative exact-real inverse receipt is available;
typing a rational `K` alone is not sufficient.

```text
||M_DD(mu_float)^(-1)|| <= K/(1-delta*K)
||M_DD(mu_float)^(-1)-M_DD(mu_exact)^(-1)||
    <= delta*K^2/(1-delta*K).
```

A port bound additionally requires nonnegative `M_BD` and `DeltaM_DB` norm
bounds and an explicitly supplied source/state key matching the inverse premise;
omitting that key is fail-closed. The helper never infers invertibility,
an inverse norm bound, or a coupling bound from the regularizer alone.

For the genuinely rounded evaluator seam, the companion
`derive_routeb_general_resolvent_port_propagation` consumes an explicit
`epsilon_a >= ||A_float-A_exact||` and independent exact-rational B/C block
bounds. When `epsilon_a*K < 1`, it returns the three-term estimate

```text
||Bf-Br|| Kf ||Cf|| + ||Br|| DeltaK ||Cf||
  + ||Br|| K ||Cf-Cr||,
```

where `Kf = K/(1-epsilon_a*K)` and
`DeltaK = epsilon_a*K^2/(1-epsilon_a*K)`. This is intentionally an
unweighted conditional bound. Conversion to the `B_up` energy metric and
consumption of the Schur/Young margin remain separate O0-R2/O0-R3 premises.

`convert_routeb_port_bound_to_weighted_metric` implements the O0-R2 scalar
conversion when the caller supplies a proved `B_up >= beta I` witness through
an exact rational `s` satisfying `s^2 <= beta`. It returns the conservative
bound `unweighted_port_bound / s`, requires matching source keys, and rejects
an unproven metric witness; `metric_lower_bound_proven` must be explicitly set
to true. It deliberately records
`schur_margin_consumed=false`; O0-R3 must still prove the remaining budget
inequality.

`consume_routeb_schur_margin` implements O0-R3's scalar budget consumer. Given
same-key weighted baseline `rho_r`, perturbation `epsilon_R`, `theta > 0`, and
an exact remaining margin, it computes
`(1+1/theta)*((rho_r+epsilon_R)^2-rho_r^2)` and rejects insufficient margin or
provenance mismatch. The baseline and perturbation proof flags are explicit and
default false, so exact-rational candidate numbers cannot silently pass as
authoritative bounds. This is only a budget arithmetic result: it does not
prove either input bound or the underlying physical PMI statement.

The API and focused tests do not run Lean/Lake, Julia, SOS, trajectory checks,
or broad regression, and all result objects keep
`formal_certificate_allowed=False` and `registry_eligible=False`.
