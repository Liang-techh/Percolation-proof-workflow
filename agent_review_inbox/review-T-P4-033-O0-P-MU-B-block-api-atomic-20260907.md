# T-P4-033 O0 — P-MU/B-block exact API atomic

**Result:** `PASS_CONDITIONAL_EXACT_API_OPEN_SOURCE_BINDING`

This review isolates the smallest useful algebraic child available in the
current exact regularizer API.  It does not repeat DH/body geometry, does not
consume `P-NE` or `P-BUDGET`, and does not admit `L_base` or the strict Schur
margin as physical facts.

## Atomic that is actually available

Let `M : Mat(6,6,R)` be one exact rational base accumulator, let
`mu : R`, and let `P_B` select the ordered coordinates `B=(4,5)`.  Define

```text
addDiag(M,mu) = M + mu I_6.
```

The exact API supports the following finite-dimensional identity:

```text
P_B addDiag(M,mu) P_B^T
  = P_B M P_B^T + mu I_2,

forall a_B : R^2,
  a_B^T (P_B addDiag(M,mu) P_B^T) a_B
    = a_B^T (P_B M P_B^T) a_B + mu(a_B,1^2 + a_B,2^2).
```

With the canonical exact convention `mu=1/1000000`, this is:

```text
a_B^T M_BB^mu a_B
  = a_B^T M_BB^0 a_B + (1/1000000)||a_B||_2^2.
```

The same statement holds for `D=(1,2,3,6)` with `I_4`, while the off-blocks
are unchanged:

```text
M_BD^mu = M_BD^0,
M_DB^mu = M_DB^0.
```

This is the useful O0 interface: regularization changes the B quadratic
budget by exactly one typed diagonal term and cannot create a port/coupling
term.  It is an exact API identity conditional only on one common exact base
matrix; it is not a statement that Julia produced that matrix.

## Strict-margin boundary

The strict consumer remains:

```text
lambda = 1 + 1/theta,
m_r = L_base - lambda*rho_r^2,
m_f = L_base - lambda*(rho_r + epsilon_R)^2,
m_f > 0.
```

The atomic above may be used inside a future physical budget identity, but it
does not establish

```text
baseline_budget(q,a_B) = a_B^T M_BB^mu(q) a_B,
```

nor does it establish the exact-real identity between the deployed DH
accumulator and the API's `M`.  Consequently it cannot set
`baseline_bound_proven`, `semantic_binding_proven`, `m_r_positive`, or
`schur_margin_consumed`.

## Minimal source theorem still missing

The deployed source has a concrete pre-regularizer accumulator `M_acc^J(q)`
from the loop at `dhport_lib.jl:47-59`.  The smallest missing source contract
is not a new geometry theorem; it is this typed semantic statement:

```text
H_acc(source_key):
  forall q in the keyed q-domain,
    ExactDecode(M_acc^J(q)) = M_NE^0(source_key,q),

H_mu(source_key):
  ExactDecode(Float64(regularization)) = mu_source(source_key),

H_mu_1e6(source_key):
  mu_source(source_key) = 1/1000000.
```

To consume the exact API atomic with the deployed physical model, all three
must use the same `source_key`, q-domain, and B/D order.  A weaker but valid
alternative is to define the exact target with the binary64 rational

```text
mu_f64 =
4722366482869645 / 4722366482869645213696
```

and prove `H_mu` with `mu_source=mu_f64`.  That would prove the insertion
identity for the decoded deployed value, but it would not prove the existing
exact-real contract `mu=1/1000000`; the two differ by the positive exact
quantity

```text
delta = 1/1000000 - mu_f64 > 0.
```

## Counterexample receipt

The source-binding gap is witnessed without any DH geometry.  Take the same
zero base accumulator on both sides:

```text
M_acc^J(q) = M_NE^0(q) = 0_6,6,
mu_J = mu_f64,
mu_exact = 1/1000000,
a_B = (1,0).
```

Then the deployed-decoded B energy and exact-contract B energy are

```text
a_B^T M_BB^J a_B    = mu_f64,
a_B^T M_BB^exact a_B = 1/1000000,
difference            = delta > 0.
```

Thus even perfect agreement of all unregularized terms does not imply the
exact `P-MU` identity.  The difference is diagonal and does not alter `M_BD`
or `M_DB`, but it does alter any physical `P-BUDGET` equality and therefore
cannot be ignored in a strict baseline ledger.

## Focused API receipt

```text
receipt_kind = routeb_o0_p_mu_b_block_exact_api_atomic
status = PASS_CONDITIONAL_EXACT_API_OPEN_SOURCE_BINDING
command =
  $env:PYTHONPATH='src'; python -m pytest -q
  tests/test_routeb_regularizer_semantics.py
  -k 'scalar_fact_keeps_float64_below_exact_rational or common_base_propagates_only_diagonal_delta'
  --disable-warnings
exit_code = 0
stdout = 2 passed, 32 deselected in 0.08s
stderr = <empty>

checked_api:
  src/percolation_workflow/routeb_regularizer_semantics.py
  schema = routeb.regularizer_semantics.v1
  exact_mu = 1/1000000
  float64_mu_bits = 0x3eb0c6f7a0b5ed8d
  B = (4,5)
  D = (1,2,3,6)

receipt_scope:
  exact_common_base_diagonal_propagation = conditional algebra only
  physical_source_binding = OPEN
  P-BUDGET = OPEN
  strict_Schur_margin = NOT_CONSUMED
  formal_certificate = false
```

The focused receipt is an API-level test receipt, not a Lean/kernel theorem
and not a Julia runtime receipt.

## Source anchors and hashes

Deployed source:

```text
robot_final/dhport_lib.jl:27
  const MASS_REGULARIZER = 1e-6

robot_final/dhport_lib.jl:46-60
  fk-derived Float64 accumulator followed by
  M + Float64(regularization) .* Matrix{Float64}(I,6,6)

robot_final/dhport_lib.jl:73-82
  arm_MCG reuses the regularization argument at q, q+h, q-h

sha256 = AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

Exact API:

```text
src/percolation_workflow/routeb_regularizer_semantics.py:24-30
  exact/Float64 constants and B/D coordinate order

src/percolation_workflow/routeb_regularizer_semantics.py:374-424
  exact rational input gate and diagonal delta inclusion

src/percolation_workflow/routeb_regularizer_semantics.py:427-463
  common-base full-matrix and B/D block propagation
```

Test anchors:

```text
tests/test_routeb_regularizer_semantics.py:32-40
  exact Float64-versus-rational scalar fact

tests/test_routeb_regularizer_semantics.py:87-99
  common-base block propagation and unchanged off-blocks
```

## Verdict

The exact regularizer API gives one genuinely usable conditional atomic:
diagonal insertion commutes with B-block extraction and propagates to the
quadratic form as `mu||a_B||^2`.  The smallest remaining physical gap is the
same-key source theorem for the pre-regularizer accumulator plus the exact
parameter interpretation.  Until that theorem/receipt exists, this result
must remain `PASS_CONDITIONAL_EXACT_API_OPEN_SOURCE_BINDING`; it is not a
physical `P-BUDGET` closure and does not consume the strict Schur margin.
