# T-P4-033 O0 — P-MU/P-BUDGET source-binding triple

**Result:** `PARTIAL_RECEIPT_H_MU_EXACT_SIDE_H_ACC_OPEN_H_MU_1E6_OPEN`

Scope is restricted to the three physical source-binding atoms requested by
the O0 strict-margin frontier.  No baseline or Schur premise is consumed; no
Lean/Lake command is run in this review; no `VERIFIED` status is assigned.

## Canonical atoms

Let `q` be a six-coordinate state and let the deployed pre-regularizer
accumulator be `M_acc^J(q)`.  The exact-real physical Newton–Euler mass before
regularization is `M_NE^0(q)`.

```text
H_acc(source_key):
  forall q in the declared q-domain,
    ExactDecode(M_acc^J(q)) = M_NE^0(source_key,q).

H_mu(source_key):
  for every exact-real matrix M and i,j,
    addMassRegularizer(M)[i,j]
      = M[i,j] + (if i=j then (1/1000000 : R) else 0).

H_mu_1e6(source_key):
  the regularization argument used by the deployed physical source and the
  exact Fourier/source evaluator is the same exact-real parameter
  mu(source_key) = 1/1000000.
```

The B-block consequence of `H_mu`, with `B=(4,5)`, is:

```text
M_NE,BB^mu(q) = M_NE,BB^0(q) + (1/1000000) I_2,

forall a_B : R^2,
  a_B^T M_NE,BB^mu(q) a_B
    = a_B^T M_NE,BB^0(q) a_B + (1/1000000)||a_B||_2^2.
```

This is only an insertion/projection identity.  It does not imply the
physical budget identity

```text
baseline_budget(q,a_B) = a_B^T M_NE,BB^mu(q) a_B,
```

which remains a separate `P-BUDGET` obligation with explicit charge
ownership.

## Evidence disposition

### H_mu — exact side theorem available, source join still open

The existing `MassRegularizer.lean` defines the exact-real operation
`addMassRegularizer M` with `(1/1000000 : R)` and proves entrywise diagonal,
off-diagonal, constant-difference, and conditional composition facts.  Its
existing receipt records a successful pinned run and standard logic axioms
only.  This is enough for the exact-side statement `H_mu` as an abstract
matrix operation.

It is not enough to claim `H_mu` for the deployed physical source, because the
theorem does not identify its abstract `M` with the Julia accumulator
`M_acc^J(q)`.  Therefore the physical disposition is:

```text
H_mu.exact_side = available
H_mu.physical_source_binding = OPEN
```

### H_mu_1e6 — literal comparator only

The deployed source declares `const MASS_REGULARIZER = 1e-6` and adds
`Float64(regularization) * I`.  The existing source comparator reports the
normalized field match

```text
source: 1/1000000       evidence: dhport_lib.jl:27
bridge: 1/1000000       evidence: RouteBP4ConditionInstantiation.lean:regularizer
match: true
```

However, that comparator compares source text/declared conventions.  It does
not prove the runtime Float64 value is the exact real rational `1/1000000`.
The exact binary64 value used by the regularizer API is

```text
mu_f64 =
4722366482869645 / 4722366482869645213696
```

and the exact contract value satisfies

```text
delta = 1/1000000 - mu_f64 > 0.
```

Thus the source-level status is:

```text
H_mu_1e6.literal_comparator = PASS_LITERAL_ONLY
H_mu_1e6.exact_runtime_binding = OPEN
```

### H_acc — no source theorem/receipt

The source anchors expose the accumulator construction:

```text
robot_final/dhport_lib.jl:46-59
  M=zeros(6,6), six-body loop, Jv/Jw construction, and body Gram addition

robot_final/dhport_lib.jl:60
  return M + Float64(regularization) .* I
```

The existing body-trace provenance closes an exact Fourier-generator copy to
the frozen 610-row payload, but its own boundary states that it does not prove
extensional equality between that copy and Julia Float64 `mass_matrix(q)` for
every `q`.  Hence it cannot discharge:

```text
ExactDecode(M_acc^J(q)) = M_NE^0(q).
```

The smallest missing receipt is one source-level semantic export carrying,
for the same `source_key` and q-domain,

```text
accumulator_definition_hash
exact_target_definition_hash
q_domain
body_loop_order = 1:6
matrix_index_order = 1:6
pre_regularizer = true
statement = ExactDecode(M_acc^J(q)) = M_NE^0(q)
runtime_or_interval_evidence = <required>
```

A source hash or an exact Fourier self-comparison alone is insufficient.

## Minimal exact missing conjunction

To obtain a physical `P-MU` receipt without consuming baseline/Schur, the
minimum semantic conjunction is:

```text
H_acc
and H_mu_1e6
and same_source_key(H_acc,H_mu_1e6)
and same_q_domain(H_acc,H_mu_1e6).
```

`H_mu` is then the exact algebraic propagation rule.  `P-BUDGET` still needs
the independent identity:

```text
forall q,a_B,
  baseline_budget(q,a_B) = a_B^T M_NE,BB^mu(q) a_B,
  no_duplicate_port_or_residual_charge.
```

No `L_base`, `rho_r`, `epsilon_R`, `m_r`, or `m_f` field is admitted by this
conjunction.

## Counterexample receipt

Use a zero pre-regularizer accumulator, so no body geometry is involved:

```text
M_acc^J(q) = M_NE^0(q) = 0_6,6,
mu_J = mu_f64,
mu_contract = 1/1000000,
a_B = (1,0).
```

Then:

```text
a_B^T M_BB^J a_B        = mu_f64,
a_B^T M_BB^contract a_B = 1/1000000,
gap                      = delta > 0.
```

Therefore the literal comparator cannot be promoted to `H_mu_1e6`, and the
exact-side `H_mu` cannot be applied to the deployed physical accumulator
without `H_acc` and the exact parameter-decoding contract.

## Immutable receipt

```text
receipt_kind = routeb_o0_physical_source_binding_triple
status = PARTIAL_RECEIPT_H_MU_EXACT_SIDE_H_ACC_OPEN_H_MU_1E6_OPEN
baseline_consumed = false
schur_consumed = false
verified = false

H_acc:
  status = OPEN_REQUIRED_SOURCE_SEMANTIC_EXPORT

H_mu:
  exact_side_status = AVAILABLE_FROM_EXISTING_RECEIPT
  physical_source_status = OPEN

H_mu_1e6:
  literal_comparator_status = PASS_LITERAL_ONLY
  exact_runtime_status = OPEN

P-BUDGET:
  status = OPEN_INDEPENDENT_PHYSICAL_QUADRATIC_IDENTITY
```

## Provenance hashes

Deployed Julia source (both audited copies):

```text
robot_final/dhport_lib.jl
routeB_dense_Mq/dhport_lib.jl
sha256 = AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

Existing exact regularizer receipt/source artifacts:

```text
examples/routeb_mass_regularizer_lean/FINAL_RECEIPT.md
  sha256 = A352452F526E979C91EC7B4AAE125D09DEED2A9A9CCD61AEB7F7C86A4CB54B37

examples/routeb_mass_regularizer_lean/output/run-8qHz1Tiv/MassRegularizer.lean
  sha256 = CD8DAFA426A77D867E541F6855B71E58157D383BBBFA214A2712235BF851528B

examples/routeb_mass_regularizer_lean/output/run-8qHz1Tiv/MassRegularizer.olean
  sha256 = F3B2566F78DF4E9A4BBDBBA7A7F58319C6C4B5315FE57E87A80CB343AF18667A
```

Existing literal comparator receipt:

```text
artifacts/routeb_agent_source_comparator_20260906T181500Z/result.json
  sha256 = 29E1906D2B62815E37332B909DC7EA8D0FF7AC7BC1DFAB7A31C38DE7AC10F4B1
  status = FAIL_CLOSED_MISMATCH
  mass_regularizer field = match true
  M0_block, FD, l45, D-domain, and coverage = mismatched/open
```

Existing body-trace provenance boundary:

```text
artifacts/routeb_agent_authoritative_body_instrument_20260906T021137/REPORT.md
  sha256 = C0AF0CE130C147430665568B39D0F327CB84AA67E6D3350A4EA785A86CA08066
  exact Fourier/body-copy checks = present
  Julia Float64 mass_matrix extensional equality = explicitly not proved
```

## Final disposition

The only currently consumable part is the exact-side regularizer insertion
rule `H_mu`.  `H_mu_1e6` is a source-literal match, not an exact runtime
binding, and `H_acc` has no source semantic theorem/receipt.  The physical
`P-MU/P-BUDGET` gate therefore remains open, with the exact missing export and
counterexample recorded above.  No baseline or strict Schur result is changed.
