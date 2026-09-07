# T-P4-033 O0 — physical baseline binding ledger

**Result:** `OBSTRUCTION_SAME_KEY_PHYSICAL_BINDINGS_INCOMPLETE`

This review does not recompute `L_base`. It treats the already-derived exact
value

```text
L_base = 120442959/280443400
```

as an inherited child input. The question here is only whether the physical
premises needed to consume that child are bound to one canonical source,
state, block orientation, and metric key.

## Canonical binding

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

The required acceptance conjunction is

```text
NE_semantics(source_key, mu, q-cell)
∧ BB_all_q(source_key, state_key)
∧ BB_sym(source_key, state_key)
∧ baseline_budget_id(source_key, state_key)
∧ B_up_id(source_key, state_key, metric_key).
```

It is not present as an authoritative receipt at the current boundary.

## Premise ledger

| ID | Exact premise required by the consumer | Same-key evidence currently present | Missing authoritative field | Status |
|---|---|---|---|---|
| `P-NE` | The exact Fourier evaluator denotes the real Newton–Euler mass `M^mu(q)` on the stated q-cell, with the same exact `mu=1/1000000`, DH rows, inertia convention, and B/D ordering. | Exact rational Fourier CSV and the Newton–Euler implementation use the same declared structural data. | A semantic equality receipt, not merely matching implementation/source descriptions; it must bind `source_key`, `state_key`, `mu`, and block extraction. | **missing** |
| `P-BB-ALLQ` | `∀ q` in the keyed cell, `‖M_BB^mu(q)-M_BB^mu(0)‖_∞ ≤ 147/800000000`. | `NUMBERS.json` reports this exact rational bound under the exact-Fourier source contract and the same q-cell key, evidence level E1 conditional. | Authoritative acceptance that the bound applies to the real Newton–Euler `M_BB^mu(q)`; current artifact is an algebraic Fourier enclosure conditional on `P-NE`. | **conditional only** |
| `P-SYM` | `∀ q` in the keyed cell, `M_BB^mu(q) = (M_BB^mu(q))ᵀ`, with the same `(B,D)=(4,5),(1,2,3,6)` orientation. | Newton–Euler code has the structural form `Jv'Jv + Jw' R(I/3)R'Jw + mu I`, which is symmetric at the implementation level. | Exact-real semantic bridge for the source table, or an exact coefficient-level symmetry certificate keyed to the same source/state. The implementation is Float64 and is not itself an exact receipt. | **unbound** |
| `P-BUDGET` | `baseline_budget(q,a_B) = a_Bᵀ M_BB^mu(q) a_B` for the physical storage/budget expression, with no omitted q-dependent term and no duplicate port/residual charge. | Nominal storage audit contains the algebraic form `K_B0 = 1/2 dq_Bᵀ M0_BB dq_B`; D-base notes define `l_base = F_B - B0*a_B`. | A same-key all-q physical energy identity naming `baseline_budget`, `M_BB^mu`, `a_B`, block order, and charge ownership. | **missing** |
| `P-BUP` | `B_up = diag(1402217/12000000, 200739/4000000)` is the canonical physical O0 metric and `A_up(q,a_B)=a_Bᵀ B_up a_B`, under `metric_key`; any q-dependence/upper-bound claim is also keyed. | Weighted adapter receipt has the exact matrix, `beta=200739/4000000`, `s=1/5`, Euclidean-2 left-output orientation, and the same source/state keys. | A typed physical identity connecting this matrix to the O0 baseline/storage consumer, plus its exact proof status. The current adapter establishes metric data/algebra, not the Newton–Euler physical interpretation. | **conditional algebraic only** |
| `P-MU` | Every occurrence of the regularizer in the physical mass identity and Fourier evaluator is the exact real `mu=1/1000000`. | `mu` is encoded in `source_key` and used in the q=0 exact coefficient interpretation. | A semantic receipt that the physical Newton–Euler expression and the Fourier table share this exact-real parameter; no Float64 evidence can discharge it. | **missing** |

## Minimal receipt contract

A consumable physical baseline receipt needs exactly the following fields (the
values already present above may be referenced rather than duplicated):

```text
receipt_kind = exact_same_key_physical_baseline_binding
source_key, state_key, metric_key
source_norm = induced_infinity
output_norm = euclidean_2
orientation = B=(4,5), D=(1,2,3,6), left-output
exact_mu = 1/1000000

newton_euler_mass_semantics:
  theorem_or_export_receipt = <authoritative exact-real equality>
  statement = FourierMass(source_key,q) = M_NewtonEuler^mu(q)
  domain = q_i ∈ [-1/1000,1/1000]

bb_all_q:
  bound = 147/800000000
  statement = ∀ q in domain, ‖M_BB^mu(q)-M_BB^mu(0)‖∞ ≤ bound

symmetry:
  statement = ∀ q in domain, M_BB^mu(q) = (M_BB^mu(q))ᵀ

baseline_budget_identity:
  statement = baseline_budget(q,a_B) = a_Bᵀ M_BB^mu(q) a_B
  charge_ownership = no duplicate port/residual term

b_up_identity:
  matrix = [[1402217/12000000,0],[0,200739/4000000]]
  statement = A_up(q,a_B) = a_Bᵀ B_up a_B
  physical_role = canonical O0 storage/metric term
```

The receipt must carry a single `source_key`/`state_key` pair on all five
blocks. A receipt that only has the Fourier `dMBB` number, only has the
structural Julia formula, or only has the weighted adapter matrix is not
consumable.

## Conditional derivation boundary

If `P-NE ∧ P-BB-ALLQ ∧ P-SYM ∧ P-BUDGET ∧ P-BUP` is later accepted, the
previous exact `L_base` derivation can be consumed unchanged. No new norm,
lower-bound, normalization, or Schur arithmetic is needed here. Until then,
the exact rational number is a conditional child, not an authoritative
physical baseline theorem.

No global lower, unit normalization, old Float64 ledger, registry promotion,
or main-state mutation was used.
