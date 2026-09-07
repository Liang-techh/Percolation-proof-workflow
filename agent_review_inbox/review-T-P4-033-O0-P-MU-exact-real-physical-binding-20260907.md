# T-P4-033 O0 — P-MU exact-real physical binding

**Result:** `OPEN_P_MU_SEMANTIC_BINDING`

This is a new, narrow O0 physical-binding child.  It does not consume an
unproved physical premise, does not recompute `L_base`, and does not consume
the strict Schur margin.  It separates the regularizer-parameter join from
the already-open Fourier/Newton–Euler function equality (`P-NE`) and from the
already-open physical budget identity (`P-BUDGET`).

## 1. Strict-margin context

The current strict consumer uses one keyed baseline lower factor and one keyed
weighted perturbation:

```text
lambda = 1 + 1/theta,
m_r    = L_base - lambda*rho_r^2,
m_f    = L_base - lambda*(rho_r + epsilon_R)^2,
strict admission requires m_f > 0.
```

The inherited exact candidate is

```text
L_base = 120442959/280443400,
```

but it remains conditional.  `P-MU` below only fixes which regularized matrix
the physical budget is referring to; it supplies neither `L_base` nor
`rho_r`, `epsilon_R`, positivity, coverage, or a Schur reserve.

## 2. New atomic statement

Use the canonical source/state keys already fixed by the O0 ledger:

```text
source_key =
routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
|mu=1/1000000|contract=exp(i*nu*q)

state_key =
routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)
|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
```

Let `I_6` be the exact-real six-dimensional identity, `P_B` the selector for
coordinates `(4,5)`, and `P_D` the selector for `(1,2,3,6)`.  The proposed
physical parameter-binding atom is:

```text
P-MU(source_key, state_key):

  mu_NE(source_key) = mu_Fourier(source_key) = 1/1000000

  forall q in q_domain, i,j in {1,...,6},
    M_NE^mu(q)[i,j] = M_NE^0(q)[i,j] + (if i=j then mu_NE(source_key) else 0)

  forall q in q_domain, i,j in {1,...,6},
    M_Fourier^mu(q)[i,j]
      = M_Fourier^0(q)[i,j]
        + (if i=j then mu_Fourier(source_key) else 0).
```

The exact block consequence needed by the O0 baseline consumer is part of the
same receipt, but is not a new physical lower-bound premise:

```text
forall q in q_domain,
  P_B M_NE^mu(q) P_B^T
    = P_B M_NE^0(q) P_B^T + (1/1000000) I_2,

forall a_B in R^2,
  a_B^T M_NE,BB^mu(q) a_B
    = a_B^T M_NE,BB^0(q) a_B + (1/1000000)||a_B||_2^2.
```

The same two equations must hold for the Fourier-side block.  The block
projection is algebraic only; the receipt must still identify the physical
side and the Fourier side with the same `source_key`, `state_key`, and
coordinate order.  In particular, this atom does **not** assert
`M_Fourier^mu = M_NE^mu`; that is the separate `P-NE` child.

## 3. Why this is independent and useful

`P-NE` can be true for the unregularized terms while the parameter join is
false.  Conversely, a literal `1e-6` in a source file does not establish that
the exact-real theorem uses `1/1000000`, nor that both evaluators inserted it
at the same matrix boundary.  `P-MU` is therefore the smallest typed join
that lets a later `P-NE` receipt compare like-for-like regularized matrices.

It is not a replacement for `P-BUDGET`: even after `P-MU`, the physical
storage/budget expression still needs the separately typed identity
`baseline_budget(q,a_B) = a_B^T M_NE,BB^mu(q) a_B` with charge ownership.

## 4. Counterexample / obstruction

Take one q in the domain and let both unregularized matrices be zero:

```text
M_NE^0(q) = 0_6,6,
M_Fourier^0(q) = 0_6,6,
mu_NE = 0,
mu_Fourier = 1/1000000.
```

For `a_B=(1,0)`, the Fourier-side block energy is `1/1000000`, while the
physical-side block energy is `0`.  Thus the Fourier-side assertion

```text
a_B^T M_Fourier,BB^mu(q) a_B >= (1/1000000)||a_B||_2^2
```

cannot be transferred to the physical baseline.  All unregularized
coefficients agree in this counterexample; only the unbound regularizer
parameter differs.  Hence a source literal, a q=0 comparison, or an
entrywise regularizer inclusion cannot discharge `P-MU`.

A second failure mode is insertion-order mismatch: if one consumer calls the
unregularized matrix while another calls `mass_matrix` with its default
regularization, their B-blocks differ by `(1/1000000)I_2`.  A strict margin
computed for one cannot be silently consumed by the other.

## 5. Required receipt (not present yet)

The minimal consumable receipt is:

```text
receipt_kind = routeb_o0_p_mu_exact_real_physical_binding
status = OPEN_P_MU_SEMANTIC_BINDING
source_key = <canonical source key above>
state_key = <canonical state key above>
block_order = B=(4,5), D=(1,2,3,6)
q_domain = forall k, abs(q[k]) <= 1/1000
exact_mu = 1/1000000

physical_source:
  unregularized_definition_hash = <hash>
  regularized_definition_hash = <hash>
  theorem_or_export = <exact-real statement for M_NE^mu=M_NE^0+mu*I>

fourier_source:
  unregularized_definition_hash = <hash>
  regularized_definition_hash = <hash>
  theorem_or_export = <exact-real statement for M_Fourier^mu=M_Fourier^0+mu*I>

parameter_join:
  mu_NE = 1/1000000
  mu_Fourier = 1/1000000
  same_source_key = true
  same_state_key = true

block_propagation:
  selector_B = (4,5)
  selector_D = (1,2,3,6)
  BB_identity = P_B*(M^0 + mu*I_6)*P_B^T = M_BB^0 + mu*I_2
  quadratic_identity = a_B^T*M_BB^mu*a_B = a_B^T*M_BB^0*a_B + mu*||a_B||_2^2

evidence:
  exact_real = true
  float64_only = false
  compile_or_kernel_receipt = <required if theorem-backed>
  axioms = <required>
  source_hashes = <required>
```

Acceptance of this receipt would close only `P-MU`.  It must not set
`semantic_binding_proven`, `baseline_bound_proven`, `m_r_positive`,
`m_f_positive`, or `schur_margin_consumed` in the O0 strict gate.

## 6. Audited source anchors

The deployed implementation currently has these relevant anchors:

```text
robot_final/dhport_lib.jl:27
  const MASS_REGULARIZER = 1e-6

robot_final/dhport_lib.jl:46
  function mass_matrix(q; regularization::Real = MASS_REGULARIZER)

robot_final/dhport_lib.jl:47-60
  unregularized DH/Jacobian mass accumulation, followed by
  M + Float64(regularization) .* Matrix{Float64}(I, 6, 6)

robot_final/dhport_lib.jl:73-82
  arm_MCG passes mass_regularization to mass_matrix at q, q+h, q-h.
```

The current file hash for that deployed source is:

```text
sha256 = AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

The exact-sidecar anchors are:

```text
src/percolation_workflow/routeb_regularizer_semantics.py:24-30
  schema, Float64 bits, exact-real mu=1/1000000, and B/D coordinates

src/percolation_workflow/routeb_regularizer_semantics.py:360-370
  recorded scalar fact and outward interval

src/percolation_workflow/routeb_regularizer_semantics.py:427-463
  conditional diagonal/block propagation from one common exact base matrix;
  its docstring explicitly disclaims a Julia physical-source claim.
```

The strict gate anchors are:

```text
src/percolation_workflow/routeb_o0_r3_receipt.py:68-74
  strict same-key receipt is conditional only

src/percolation_workflow/routeb_o0_r3_receipt.py:88-94
  source, metric, margin keys and semantic/physical proof flags are required

src/percolation_workflow/routeb_o0_r3_receipt.py:318-357
  exact rho/epsilon/theta/margin parsing and strict proof flags
```

## Verdict

`P-MU` is a distinct, formally precise atomic child.  Current evidence shows
the deployed Float64 literal and an exact-sidecar convention, but not the
required same-key exact-real semantic receipt.  Therefore the correct receipt
state is `OPEN_P_MU_SEMANTIC_BINDING`; no physical premise was consumed, no
strict Schur margin was admitted, and no deployed-tau equivalence or main
state mutation is claimed.
