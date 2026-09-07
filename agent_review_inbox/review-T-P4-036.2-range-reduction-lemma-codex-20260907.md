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

A Lean-facing local helper can be stated independently of the Route-B source:

```lean
lemma sin_sub_linear_remainder
    (y : ℝ) : |Real.sin y - y| ≤ |y| ^ 3 / 6 := by
  -- Taylor integral remainder; use |cos t| ≤ 1 under the integral.
  exact abs_integral_kernel_bound_sin y
```

The name `abs_integral_kernel_bound_sin` is a proof-draft placeholder for the
small integral-remainder lemma to be proved or located in the pinned Mathlib
environment. It is not an imported theorem claim. Applying it with `hqabs`
and `norm_num` yields `sin_local_taylor_bound`, then

```text
-3/20 - 9/16000 = -2409/16000
  ≤ sin(q) ≤
  3/20 + 9/16000 = 2409/16000.
```

For cosine, the degree-one Taylor remainder and the global upper bound give

```text
|cos(y) - 1| ≤ |y|^2 / 2,
cos(y) ≤ 1,
cos(y) ≥ 1 - y^2/2 ≥ 1 - (3/20)^2/2 = 791/800.
```

The final range transport uses exact quarter-turn identities:

```lean
have hsin_shift : Real.sin (theta2 q) = -Real.cos q := by
  unfold theta2
  rw [Real.sin_sub, Real.sin_pi_div_two, Real.cos_pi_div_two]
  ring

have hcos_shift : Real.cos (theta2 q) = Real.sin q := by
  unfold theta2
  rw [Real.cos_sub, Real.sin_pi_div_two, Real.cos_pi_div_two]
  ring
```

Here the `Real.*_pi_div_two` names are proof-draft names to be checked against
the pinned Mathlib API. The mathematical content is the exact identities
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

## Review status

```text
mathematical_scope: one exact-real theta row
proof_draft: present, uncompiled
Float64_binding: OPEN
libm_binding: OPEN
D1_D2_D3: OPEN
coverage: OPEN
formal_certificate_allowed: false
registry_promoted: false
```

