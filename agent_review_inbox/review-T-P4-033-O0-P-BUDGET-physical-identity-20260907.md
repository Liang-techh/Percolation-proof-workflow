# T-P4-033 O0 — P-BUDGET physical identity source-binding receipt

**Result:** `OPEN_P_BUDGET_PHYSICAL_IDENTITY`

This review is limited to the physical identity for `baseline_budget`.  It
does not consume `L_base`, any `M_BB` lower bound, a Schur margin, or a force
residual bound.  No Lean/Lake command was run and no `VERIFIED` status is
claimed.

## Required identity

With the canonical block order

```text
B = (4,5), D = (1,2,3,6),
P_B : R^6 -> R^2,
M_phys^mu(q) = mass_matrix(q; regularization=1e-6),
```

the current O0 ledger asks for the same-key physical statement

```text
P-BUDGET(source_key,state_key):

forall q in q_domain, forall a_B in R^2,
  baseline_budget(q,a_B)
    = a_B^T [P_B M_phys^mu(q) P_B^T] a_B,

charge_ownership:
  the mass term is charged exactly once;
  no port/residual term is hidden inside baseline_budget and charged again.
```

This statement has two logically separate parts:

1. the physical meaning of `baseline_budget` and the role of `a_B`;
2. the source identity connecting the physical mass block to the deployed
   `mass_matrix` output.

Neither part is present as a consumable same-key source receipt.

## What the deployed source actually exposes

The deployed source `dhport_lib.jl` defines the mass output as a regularized
Float64 matrix, but does not define a quantity named `baseline_budget`:

```text
robot_final/dhport_lib.jl:46-60
  mass_matrix(q; regularization=...)
  accumulates M and returns M + Float64(regularization) * I_6
```

The descriptor interface uses a different object:

```text
robot_final/routeB_descriptor_residual_interface.jl:7
  include("dhport_lib.jl")

robot_final/routeB_descriptor_residual_interface.jl:13-18
  M(q)a = tau - C(q,dq)dq - G(q),
  l45 = [I4 f4; I5 f5] - M0_BB[a4;a5]

robot_final/routeB_descriptor_residual_interface.jl:22-23
  M0 = readdlm(routeB_Mq_M0.csv, ',', Float64)
  M0_BB = [M0[4,4] 0.0; 0.0 M0[5,5]]

robot_final/routeB_descriptor_residual_interface.jl:40-57
  Mq = arm_MCG(q,dq), rhs=tau-Cdq-Gq, a=Mq\rhs,
  l = IVAL_B*f_B - M0_BB*a_B.
```

Thus the source gives a physical acceleration solve and a nominal diagonal
linking residual, not a physical budget identity.  In particular, the source
does not establish that `baseline_budget` is based on the full regularized
block `M_phys,BB^mu(q)` rather than on `M0_BB`.

The existing exact rational descriptor bridge separately records:

```text
routeB_dense_Mq/P4_PHYSICAL_RATIONAL_DESCRIPTOR_BRIDGE.md:18-27
  the final tail PMI must use the complete 2x2 M0_BB;
  the old diagonal convenience matrix is not the final certificate model.
```

This is a direct source/interface mismatch for `P-BUDGET`, not a body-geometry
issue.

## Normalization and variable-role obstruction

The source descriptor variable `a_B` is an acceleration block because it is
returned by `a = Mq \ rhs`.  The existing storage leaf uses velocity `dq_B`
and the kinetic normalization

```text
K_B0 = (1/2) dq_B^T M0_BB dq_B.
```

Therefore the current string `baseline_budget(q,a_B)` does not identify a
unique physical quantity.  A minimal receipt must explicitly choose one of:

```text
acceleration-budget convention:
  baseline_budget(q,a_B) = a_B^T M_phys,BB^mu(q) a_B;

kinetic-storage convention:
  baseline_budget(q,dq_B) = (1/2) dq_B^T M_phys,BB^mu(q) dq_B.
```

These are not interchangeable by renaming `dq_B` to `a_B`; the source gives
them different physical roles.

## Charge-ownership obstruction

The deployed linking expression permits at least two algebraically consistent
ledger conventions.  Write

```text
M_phys,BB^mu(q) a_B
  = M0_BB a_B + (M_phys,BB^mu(q)-M0_BB) a_B.
```

Convention A assigns the full mass quadratic to the baseline:

```text
baseline_A = a_B^T M_phys,BB^mu(q) a_B,
mass_residual_A = 0.
```

Convention B assigns the nominal quadratic to the baseline and the mass defect
to the residual ledger:

```text
baseline_B = a_B^T M0_BB a_B,
mass_residual_B = a_B^T(M_phys,BB^mu(q)-M0_BB)a_B.
```

Both conventions are compatible with the source's displayed `l` expression,
because that expression names only `M0_BB a_B`; the source contains no
`baseline_budget` or `charge_ownership` field selecting A or B.  A later
residual budget that includes `mass_residual_B` cannot be combined with
`baseline_A` without an explicit no-duplicate-charge theorem.

### Concrete counterexample

At one fixed state, take the two-dimensional toy blocks

```text
M_phys,BB^mu = I_2,
M0_BB = 0_2,
a_B = (1,0).
```

Then

```text
baseline_A = 1,
baseline_B = 0,
mass_residual_B = 1.
```

The total `baseline + mass_residual` is the same, but the strict baseline
factor and the residual charge are different.  Since current provenance does
not state which ownership convention is intended, `P-BUDGET` is
non-identifiable from the source anchors alone.

## Smallest source-binding repair

One direct receipt can close this child without proving any baseline margin,
provided it contains all fields below:

```text
receipt_kind = routeb_o0_p_budget_physical_identity
status = <OPEN until all fields are present>
source_key = <canonical exact source key>
state_key = <canonical q-cell and B/D key>
block_order = B=(4,5), D=(1,2,3,6)
regularizer = 1/1000000 exact-real parameter
variable_role = acceleration a_B | velocity dq_B
normalization = 1 | 1/2

physical_budget_definition:
  baseline_budget(q,x_B) = normalization *
    x_B^T [P_B M_phys^mu(q) P_B^T] x_B

source_mass_binding:
  forall q in q_domain,
    M_phys^mu(q) = ExactDecode(mass_matrix_Julia(q; regularization=1e-6))

block_binding:
  M_phys,BB^mu(q) = P_B M_phys^mu(q) P_B^T

charge_ownership:
  mass_defect_in_baseline = true | false
  mass_defect_in_residual = true | false
  port_term_in_baseline = false
  residual_charge_disjoint = true

provenance:
  deployed_source_hash = <hash>
  budget_definition_hash = <hash>
  exact_target_hash = <hash>
  source_semantic_receipt = <authoritative receipt>
```

The two ownership booleans must not both be true unless the receipt also
contains an explicit cancellation/accounting identity.  The present O0
ledger's required choice is the full-mass convention, but that choice is not
yet bound to the deployed source.

## Current immutable disposition

```text
receipt_kind = routeb_o0_p_budget_physical_identity
status = OPEN_P_BUDGET_PHYSICAL_IDENTITY
source_anchor_Mq = present
source_anchor_B = present (4,5)
source_anchor_M0_BB = present, but diagonal convenience only
baseline_budget_definition = absent from deployed Julia/source
variable_role_and_normalization = ambiguous (a_B acceleration vs dq_B velocity)
charge_ownership = absent
full_M_phys_BB_source_binding = absent
baseline_consumed = false
schur_consumed = false
verified = false
```

## Provenance hashes

```text
robot_final/dhport_lib.jl
  sha256 = AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936

robot_final/routeB_descriptor_residual_interface.jl
  sha256 = D3D21705E5E904A080E4B86DC4C380788D2323C155570A8E7B40D62B11BB0A24

robot_final/routeB_Mq_M0.csv
  sha256 = 28D98AD71D1D6C2CBE830872CAD9077F2F7B4E2D932794217EB68868FD2E2B40

robot_final/routeB_dense_Mq/P4_PHYSICAL_RATIONAL_DESCRIPTOR_BRIDGE.md
  sha256 = 68BBC8D4B4455A547D6A251E67F0B3A075B32827541DBF7CEC827B56D06A9487

agent_review_inbox/receipt-T-P4-033-O0-physical-baseline-binding-ledger-20260907.json
  status = OBSTRUCTION_SAME_KEY_PHYSICAL_BINDINGS_INCOMPLETE
```

## Final verdict

No minimal physical `P-BUDGET` receipt can be closed from the current source.
The exact missing content is not another mass calculation: it is (i) a
definition of `baseline_budget` with variable role and normalization, (ii) a
same-key full regularized `M_BB^mu(q)` source binding, and (iii) a disjoint
charge-ownership declaration for the `M0_BB` linking residual.  Until those
fields are supplied, `P-BUDGET` remains OPEN and must not affect baseline or
Schur admission.
