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

## Lean-agent target decomposition: `K_f`, `DeltaK`, `U_R`

The canonical exact-keyed interface should be handed to Lean as three small
targets. The first is pure exact arithmetic; the second is the norm estimate
for the already-expanded port difference; the third is only the adapter that
feeds the resolvent norm bounds into that estimate. This keeps matrix/source
binding assumptions visible instead of hiding them in a computed `U_R`.

### 1. Exact scalar resolvent layer

Use `ℝ` in the generic theorem (a receipt with rational fields is inserted by
the canonical `ℚ → ℝ` coercion), and define:

```lean
def K_f (K epsilon_A : ℝ) : ℝ :=
  K / (1 - epsilon_A * K)

def DeltaK (K epsilon_A : ℝ) : ℝ :=
  epsilon_A * K ^ 2 / (1 - epsilon_A * K)

def U_R (dB Br Cf dC K epsilon_A : ℝ) : ℝ :=
  dB * K_f K epsilon_A * Cf
    + Br * DeltaK K epsilon_A * Cf
    + Br * K * dC
```

The smallest arithmetic goal is:

```lean
theorem resolvent_scalar_decomposition
    {K epsilon_A : ℝ}
    (hK : 0 ≤ K) (hE : 0 ≤ epsilon_A)
    (hcontract : epsilon_A * K < 1) :
    0 ≤ K_f K epsilon_A ∧
    0 ≤ DeltaK K epsilon_A ∧
    DeltaK K epsilon_A = epsilon_A * K * K_f K epsilon_A ∧
    K_f K epsilon_A = K + DeltaK K epsilon_A := by
  -- `have hden : 0 < 1 - epsilon_A * K := sub_pos.mpr hcontract`
  -- then `field_simp [ne_of_gt hden]` / `ring` for the equalities.
  sorry
```

The `sorry` above is a target marker only and must not enter a receipt. The
only nontrivial premise is `hcontract`; positivity of the denominator is
derived from it. `K_f` and `DeltaK` are therefore exact derived fields, not
independent supplied claims.

### 2. Three-term norm layer

Let `Bf, Br` be the two `B` blocks, `If, Ir` the two D-block inverses, and
`Cf, Cr` the two `C` blocks. The source-side algebra must first provide the
exact expansion:

```lean
h_expand : Rf - Rr =
    (Bf - Br) * If * Cf
      + Br * (If - Ir) * Cf
      + Br * Ir * (Cf - Cr)
```

The minimal norm target is:

```lean
theorem norm_port_difference_le_U_R
    {E : Type*} [NormedRing E]
    (Rf Rr Bf Br If Ir Cf Cr : E)
    (dB BrN CfN dC K DeltaKN KfN URN : ℝ)
    (h_expand : Rf - Rr =
      (Bf - Br) * If * Cf
        + Br * (If - Ir) * Cf
        + Br * Ir * (Cf - Cr))
    (h_dB : ‖Bf - Br‖ ≤ dB)
    (h_Br : ‖Br‖ ≤ BrN)
    (h_Cf : ‖Cf‖ ≤ CfN)
    (h_dC : ‖Cf - Cr‖ ≤ dC)
    (h_If : ‖If‖ ≤ KfN)
    (h_Ir : ‖Ir‖ ≤ K)
    (h_Idiff : ‖If - Ir‖ ≤ DeltaKN)
    (h_nonneg : 0 ≤ dB ∧ 0 ≤ BrN ∧ 0 ≤ CfN ∧ 0 ≤ dC ∧ 0 ≤ KfN ∧
      0 ≤ K ∧ 0 ≤ DeltaKN) :
    ‖Rf - Rr‖ ≤ dB * KfN * CfN
      + BrN * DeltaKN * CfN
      + BrN * K * dC := by
  sorry
```

For the concrete matrix instance, instantiate `E` with the matrix algebra and
the *same* induced norm convention for all seven bound fields. The proof is only `h_expand`,
`norm_add_le`, `norm_mul_le`, and monotonicity of multiplication by the
nonnegative scalar bounds. No inverse API is needed in this layer.

### 3. Exact keyed adapter for `U_R`

The adapter target should combine the two layers without recomputing or
renaming the bounds:

```lean
theorem exact_keyed_U_R_target
    {E : Type*} [NormedRing E]
    (Rf Rr Bf BrM If Ir CfM CrM : E)
    (dB BrN CfN dC K epsilon_A : ℝ)
    (h_dB : 0 ≤ dB) (h_Br : 0 ≤ BrN) (h_Cf : 0 ≤ CfN) (h_dC : 0 ≤ dC)
    (h_inverse_f : ‖If‖ ≤ K_f K epsilon_A)
    (h_inverse_r : ‖Ir‖ ≤ K)
    (h_inverse_diff : ‖If - Ir‖ ≤ DeltaK K epsilon_A)
    (h_B_diff : ‖Bf - BrM‖ ≤ dB)
    (h_B_r : ‖BrM‖ ≤ BrN)
    (h_C_f : ‖CfM‖ ≤ CfN)
    (h_C_diff : ‖CfM - CrM‖ ≤ dC)
    (h_expand : Rf - Rr =
      (Bf - BrM) * If * CfM
        + BrM * (If - Ir) * CfM
        + BrM * Ir * (CfM - CrM)) :
    ‖Rf - Rr‖ ≤ U_R dB BrN CfN dC K epsilon_A := by
  sorry
```

This is intentionally a target signature: the concrete agent should replace
the schematic `E` with the actual matrix type and pass the exact keyed
premises. It must not prove the result by trusting a stored `U_R` value. A
receipt may record the arithmetic identity
`U_R = dB*K_f*Cf + Br*DeltaK*Cf + Br*K*dC`, but the norm inequality still
requires `h_expand` and all five component bounds.

## Minimum norm/source/state bindings

The Lean target is consumable only when the following fields are joined under
one canonical key:

- **Norm:** one compatible submultiplicative induced norm for `K`,
  `epsilon_A`, `dB`, `Br`, `Cf`, and `dC`; the norm name must be explicit
  (`induced_2` or `induced_infinity`). If converting `U_R` to O0-R2's
  weighted metric, additionally bind `metric.orientation = left_output`,
  `metric.norm = induced_2`, `B_up`, exact `beta`, exact `s`, `s > 0`,
  `s^2 ≤ beta`, and the proved `B_up ≥ beta I`.
- **Source:** `source_key`, source snapshot/hash, exact-real and deployed-μ
  semantics, FD step, force scale, coefficient revision, rounding/interval
  mode, block coordinate order, and the exact `M_DD`, `M_BD`, `M_DB`/`M0_DB`
  objects from which the four component bounds are derived.
- **State:** `state_key`, cell/domain id and q bounds, axis order, coverage,
  evaluator state, and the same regularization/rounding mode. The inverse,
  B/C coupling, and metric receipts must all carry the identical
  `source_key` and `state_key`; equality of artifact hashes alone is not the
  join.
- **Derived fields:** exact nonnegative `K`, `epsilon_A`, `dB`, `Br`, `Cf`,
  `dC`, the proof of `epsilon_A*K < 1`, and the derived exact `K_f`,
  `DeltaK`, `U_R`, with no Float64 approximation silently substituted.

The remaining mathematical obstruction is precise: without an authoritative
exact-real `‖A_r⁻¹‖ ≤ K`, the common norm convention, or the same-key
`h_expand`/B-C bounds, Lean can still prove the generic arithmetic lemmas but
cannot prove the keyed O0-R1/R2 claim. In that case the correct receipt
status remains open/pending rather than a numeric `U_R` admission.
