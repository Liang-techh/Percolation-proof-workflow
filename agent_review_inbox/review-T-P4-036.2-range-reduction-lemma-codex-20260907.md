---
kind: review_result
task_id: T-P4-036.2
source_agent: Codex
created_at: 2026-09-07
integration_status: pending
---

# Minimal exact-real range-reduction/Taylor lemma

## Selected child

This review isolates one row only: link `i=2`, `theta`, whose canonical phase is
`k_theta[2] = -1`. The exact source expression is

```text
x(q) = q - pi/2,       q ∈ [-3/20, 3/20].
```

The smallest useful exact-real child is:

```text
EXACT_REAL_THETA2_RANGE_REDUCTION_TAYLOR_DRAFT
scope: one theta row, one local q interval
status: conditional exact-real lemma, not LEAN_VERIFIED
```

It is intentionally narrower than the 12-row contract and does not claim to
close the virtual frontier row, O2, or any source-execution boundary.

## Precise statement

Let `I = Set.Icc (-3/20 : ℝ) (3/20)`. Define

```lean
def theta2 (q : ℝ) : ℝ := q - Real.pi / 2
def reduced2 (q : ℝ) : ℝ := theta2 q + Real.pi / 2

def Contains (a b x : ℝ) : Prop := a ≤ x ∧ x ≤ b
```

A minimal fixed-endpoint theorem is:

```lean
theorem theta2_exact_real_interval
    {q : ℝ} (hq : q ∈ Set.Icc (-3 / 20) (3 / 20)) :
    reduced2 q = q ∧
    Contains (-1 : ℝ) (-791 / 800) (Real.sin (theta2 q)) ∧
    Contains (-2409 / 16000) (2409 / 16000) (Real.cos (theta2 q)) := by
  ...
```

The endpoints are deliberately conservative and exact. They need not equal the
much tighter endpoints printed in the existing 12-row CSV; an integration
adapter must either use these wider endpoints or separately prove that the CSV
endpoints contain them.

The two local Taylor bounds needed by the theorem are:

```lean
theorem sin_local_taylor_bound
    {y : ℝ} (hy : |y| ≤ 3 / 20) :
    |Real.sin y - y| ≤ 9 / 16000 := by
  ...

theorem cos_local_taylor_bound
    {y : ℝ} (hy : |y| ≤ 3 / 20) :
    791 / 800 ≤ Real.cos y ∧ Real.cos y ≤ 1 := by
  ...
```

These are exact-real statements. No machine number appears in their types.

## Proof draft

The reduction step is ring arithmetic, with no approximation to `pi`:

```lean
have hreduce : reduced2 q = q := by
  unfold reduced2 theta2
  ring
```

From `hq`, obtain the absolute-value bound:

```lean
have hqabs : |q| ≤ (3 / 20 : ℝ) := by
  rw [abs_le]
  exact ⟨hq.1, hq.2⟩
```

For the sine bound, use the integral Taylor remainder at zero through degree
two. Since `sin 0 = 0`, `cos 0 = 1`, and the third derivative of `sin` is
`-cos`, the exact remainder identity gives

```text
|sin(y) - y| ≤ |y|^3 / 6 ≤ (3/20)^3 / 6 = 9/16000.
```

A preliminary proof draft used an `abs_integral_kernel_bound_sin` helper here;
the pinned API result below supersedes that placeholder. Applying the exact
`Real.abs_sub_sin_le` theorem with `hqabs` and rational normalization yields
`sin_local_taylor_bound`, then

```text
-3/20 - 9/16000 = -2409/16000
  ≤ sin(q) ≤
  3/20 + 9/16000 = 2409/16000.
```

## Pinned Mathlib API result

The placeholder above can be removed for the sine child. In the pinned source
tree

```text
artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/Mathlib
```

the exact public theorem is:

```lean
Real.abs_sub_sin_le (x : ℝ) :
  |x - Real.sin x| ≤ |x| ^ 3 / 6
```

It is in `Analysis/SpecialFunctions/Trigonometric/Bounds.lean` and is already
the scalar cubic Taylor remainder needed here. It has no positivity or domain
side condition. Thus the Lean-facing helper should be stated as:

```lean
lemma sin_sub_linear_remainder (y : ℝ) :
    |y - Real.sin y| ≤ |y| ^ 3 / 6 :=
  Real.abs_sub_sin_le y
```

The exact quarter-turn transport is also present, directly in the `Real`
namespace, in `Analysis/SpecialFunctions/Trigonometric/Basic.lean`:

```lean
Real.sin_sub_pi_div_two (x : ℝ) :
  Real.sin (x - Real.pi / 2) = -Real.cos x

Real.cos_sub_pi_div_two (x : ℝ) :
  Real.cos (x - Real.pi / 2) = Real.sin x
```

These are preferable to expanding `Real.sin_sub`/`Real.cos_sub` and then
supplying `Real.sin_pi_div_two` and `Real.cos_pi_div_two`; the latter two also
exist, but are not needed by the minimal transport step:

```lean
have hsin_shift : Real.sin (theta2 q) = -Real.cos q := by
  simpa [theta2] using Real.sin_sub_pi_div_two q
have hcos_shift : Real.cos (theta2 q) = Real.sin q := by
  simpa [theta2] using Real.cos_sub_pi_div_two q
```

For the cosine enclosure no second generic Taylor instantiation is required.
The pinned `Bounds.lean` exposes the exact polynomial lower bound

```lean
Real.one_sub_sq_div_two_le_cos {x : ℝ} :
  1 - x ^ 2 / 2 ≤ Real.cos x
```

and the global upper bound is `Real.cos_le_one (x : ℝ)`. Consequently the
local helper can be reduced to:

```lean
lemma cos_local_taylor_bound
    {y : ℝ} (hy : |y| ≤ 3 / 20) :
    791 / 800 ≤ Real.cos y ∧ Real.cos y ≤ 1 := by
  constructor
  · calc
      (791 / 800 : ℝ) ≤ 1 - y ^ 2 / 2 := by
        have hsq : y ^ 2 ≤ (3 / 20 : ℝ) ^ 2 := by
          have hsq' : |y| ^ 2 ≤ (3 / 20 : ℝ) ^ 2 :=
            pow_le_pow_left₀ (abs_nonneg y) hy 2
          simpa [sq_abs] using hsq'
        nlinarith [hsq]
      _ ≤ Real.cos y := Real.one_sub_sq_div_two_le_cos
  · exact Real.cos_le_one y
```

The displayed `nlinarith` line is a proof draft: its only mathematical input
is `hy` (after converting `hy` to `-3/20 ≤ y ∧ y ≤ 3/20`), not a numerical
receipt. The sine arithmetic similarly instantiates `Real.abs_sub_sin_le q`
and bounds `|q| ^ 3 / 6` by `9/16000`.

## Exact API obstruction / compile boundary

No quarter-turn API obstruction was found: the two direct theorem names and
their argument types above match the pinned source. No ready-made theorem with
the exact name or type

```lean
|Real.cos y - 1| ≤ |y| ^ 2 / 2
```

was found. That is not a mathematical gap, because
`Real.one_sub_sq_div_two_le_cos` plus `Real.cos_le_one` is sufficient for this
child. If an implementation insists on deriving both sine and cosine from a
generic Taylor theorem, the pinned `TaylorIntegral.lean` only offers the
higher-dimensional
`map_add_eq_sum_add_integral_iteratedFDeriv`; it does not expose a scalar
sin/cos remainder theorem with the required interval-bound conclusion. Such an
implementation must additionally prove derivative simplification and bound
the interval integral. That generic route is therefore an API/adapter burden,
not a reason to replace the direct `Bounds.lean` lemmas.

Lean/Lake compilation was intentionally not run under this task's boundary.
Accordingly, this review makes no claim that the draft syntax has been
elaborated in the repository's active environment. The precise remaining
compile check, if later authorized, is import availability for
`Trigonometric.Basic` and `Trigonometric.Bounds`, followed by ordinary tactic
normalization of the rational inequalities; it is not a missing theorem-name
claim.

For cosine, the pinned quadratic lower-bound lemma and the global upper bound
give

```text
cos(y) ≤ 1,
cos(y) ≥ 1 - y^2/2 ≥ 1 - (3/20)^2/2 = 791/800.
```

The final range transport uses exact quarter-turn identities:

```lean
have hsin_shift : Real.sin (theta2 q) = -Real.cos q := by
  simpa [theta2] using Real.sin_sub_pi_div_two q

have hcos_shift : Real.cos (theta2 q) = Real.sin q := by
  simpa [theta2] using Real.cos_sub_pi_div_two q
```

The pinned direct names are therefore resolved, not placeholders. The
mathematical content is the exact identities
`sin(q-pi/2)=-cos(q)` and `cos(q-pi/2)=sin(q)`. Combining them with the two
local bounds gives

```text
-1 ≤ sin(q-pi/2) ≤ -791/800,
-2409/16000 ≤ cos(q-pi/2) ≤ 2409/16000.
```

The sign reversal in the first interval is an exact order reversal, not a
floating-point operation.

## What this does and does not depend on

### Canonical source

The row is source-indexed by the canonical `theta=q[ii]+DH[ii,1]` expression,
link order `i=2`, and phase `-1`. The relevant source anchor is

```text
dhport_lib.jl SHA-256:
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

The exact-real contract artifacts used for row identity are:

```text
P3_DH_TRIG_CHAIN_CONTRACT.md:
78E8AB5695BC47ED3347D6AA10F3BD7E2BC7B84D6C0A9120ADB31E277EC09CA1
routeb_p3_dh_trig_chain_contract.csv:
87C326FD0E2F2A69EB330A562E30917521DB2C35C69E5A4AFECC6932998CA8E3
```

These hashes bind the row's intended source position. They do not prove a
Float64 execution or the correctness of the CSV endpoints.

### State and coverage

The current routing snapshot observed for the parent was revision `502`, state
checksum
`e394753701c9654a8de69d525cf29c9af3f522ee5cb1ae42406ee6d750c391ca`. Its
`P4.true_dh_float64_evaluator_enclosure` metadata routes `.1-.4` as virtual
children and requires per-box coverage. This review does not modify that state
or use its metadata as a proof.

The lemma depends only on the local input premise `q∈[-3/20,3/20]`. It does
not establish that this interval is part of the covered O2 partition, does not
cover `dq/w`, and does not compose six links or any `q`-shifted finite-
difference boxes. A D1 consumer must supply the matching box-membership and
row-index premises; a separate coverage receipt is still required.

## Explicit non-coverage boundary

This theorem uses `Real.pi`, `Real.sin`, and `Real.cos` only. It contains no:

```text
Float64/Bin64 decode or rounded q+DH addition
Julia or libm call semantics
actual sin/cos output bits or runtime identity
T_prev*A_i, parent-z extraction, FK/COM/Jacobian/mass/potential DAG
operation-schedule realization or outward machine-operation receipt
per-box/full-domain coverage
```

Therefore it cannot discharge T-P4-036.1 or `.3`, cannot close D1/D2/D3 in
`.4`, and cannot be used as a Float64/libm or finite-DH proof. The next child
must add a separately evidenced machine-argument/libm enclosure before this
row can feed a deployed finite-DAG propagation.

## Fresh minimal Lean compile receipt

The following standalone exact-real sidecar was compiled after adding only the
required `noncomputable section` for `Real.pi`:

```text
source:
  artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/
  DownstreamTest/Theta2ExactRealApi.lean
source_sha256:
  F47E94BEB7F2A9B5B949C3CFB3E352C95CB38149C8A1812A7AF4E47CD5D7961B
olean:
  artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/
  DownstreamTest/Theta2ExactRealApi.olean
olean_sha256:
  9D3153AC10F26B05D06CB4AD64D7BF0FF03CD83234CB94DFDC11750CCCB80F54
toolchain:
  leanprover/lean4:v4.33.1
Lean:
  Lean (version 4.33.1, x86_64-w64-windows-gnu,
  commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
command:
  lake env lean -o DownstreamTest\Theta2ExactRealApi.olean
    DownstreamTest\Theta2ExactRealApi.lean
exit_code: 0
stdout_stderr: empty
```

The compiled declarations are exactly `theta2_sin`, `theta2_cos`,
`sin_linear_remainder`, `cos_quadratic_lower`, and `cos_global_upper`. An
initial attempt from outside the pinned Mathlib root was rejected before
elaboration with the precise path error “input file ... must be contained in
root directory”; it was not an API failure. The successful receipt above uses
the same source inside `DownstreamTest` and is the authoritative one.

## Review status

```text
mathematical_scope: one exact-real theta row
proof_draft: minimal API sidecar compiled
Float64_binding: OPEN
libm_binding: OPEN
D1_D2_D3: OPEN
coverage: OPEN
formal_certificate_allowed: false
registry_promoted: false
```
