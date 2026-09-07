# T-P4-033 O0/P-NE — FourierMass to Newton–EulerMass

**Verdict:** `OBSTRUCTION_P_NE_FUNCTION_EQUALITY_NOT_BOUND`

The current exact sidecars do not provide a consumable same-key theorem

```text
FourierMass(source_key, q) = NewtonEulerMass^mu(q).
```

They provide only conditional algebraic seams. No `L_base` arithmetic or
previous baseline ledger is repeated here.

## Canonical target

Use one exact-real regularized convention throughout:

```text
Q6       := Fin 6 → ℝ
Mat6     := Matrix (Fin 6) (Fin 6) ℝ
Body     := Fin 6
Freq     := Fin 6 → ℤ
mu       := 1/1000000
q-domain := ∀ k, |q k| ≤ 1/1000

FourierMass^mu(q) i j
  := Σ row : Fin 610, row(row).entry=(i,j)
       [ re(row) cos(ν(row)·q) - im(row) sin(ν(row)·q) ]
     + if i=j then mu else 0

NewtonEulerMass^mu(q) i j
  := Σ body : Fin 6,
       [ m_body Σ a, Jv(body,q,a,i) Jv(body,q,a,j)
         + Σ a b, Jw(body,q,a,i) I_body(a,b) Jw(body,q,b,j) ]
     + if i=j then mu else 0.
```

The exact `Jv/Jw`, frame/COM, parent-axis, body masses, isotropic inertia,
block order `B=(4,5), D=(1,2,3,6)`, and the regularizer must all be the terms
named by the same source/state key:

```text
source_key =
routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
|mu=1/1000000|contract=exp(i*nu*q)

state_key =
routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)
|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
```

## What the existing sidecars actually prove

1. `SourceMassFourierBridge.lean` proves
   `sourceMass_to_regularized_fullSixBodyFourier`, but only under
   ```text
   h_body : ∀ body r s, bodyContribution body r s = fourierBody body q r s.
   ```
   The `fourierBody` is an abstract parameter; the theorem does not identify
   it with the 610-row payload.

2. `Full610AggregateComparator.lean` is compiled and proves the regularized
   source-to-CSV relation only under both
   ```text
   h_aggregate : csvAggregate massPayload q = Σ body, fourierBody body q
   h_body      : bodyContribution body = fourierBody body q.
   ```
   Its compile receipt explicitly leaves both premises open.

3. `RouteBO1PerBodyExactSource.lean` gives an exact-real Newton–Euler body
   definition through `sourceContract` and a frame/contract extensional bridge.
   `RouteBO1PerBodyTraceAdapter.lean` defines six concrete targets
   `h_body_1` through `h_body_6`, but proves none of them.

4. `BodyTraceEvaluator.lean` is a generated 727-row body-labelled evaluator,
   not a proof. It is marked `GENERATED_UNCOMPILED`; the corresponding receipt
   is `OPEN_H_BODY_PROOFS_UNCOMPILED`.

5. `ExactCoefficientBridge.lean` proves the generic implication
   “equal finite rational coefficient maps imply equal real cos/sin
   evaluators.” It has no Lean reified exact-DH coefficient map and therefore
   cannot instantiate the implication for the current payload. The executable
   coefficient checker is not a kernel theorem.

6. `MassZeroBridge.lean` proves only the literal q=0 aggregate plus regularizer
   identity. It cannot supply equality as a function of q.

Therefore the exact-real frame and mass algebra are present, and the payload
is exact data, but the semantic join between them is absent.

## Smallest consumable receipt

The smallest route is one direct theorem/receipt, with no abstract premise
fields left:

```text
receipt_kind = exact_real_fourier_newton_euler_mass_binding
source_key, state_key, mu_exact=1/1000000
q_domain = ∀ k, |q k| ≤ 1/1000
block_order = B=(4,5), D=(1,2,3,6)
orientation = Matrix row/column order 1..6

theorem h_fourier_mass_newton_euler :
  ∀ q, q ∈ q_domain →
    FourierMass^mu(source_key,q) = NewtonEulerMass^mu(source_key,q)
```

The receipt must include the exact definitions or immutable hashes of both
functions, the payload hash, the exact source constants, a compiled `.olean`,
exit code, `#print axioms`, and a zero `sorry/admit/axiom` audit. A source hash
or a Float64 agreement is not a substitute.

The minimal decomposed route, if the direct theorem is too large, is:

```text
h_body :
  ∀ body q i j, BodyMass_NE(source_key,body,q,i,j)
                 = BodyFourier(payload_body_trace,body,q,i,j)

h_aggregate :
  ∀ q i j, CSV610Mass(payload_610,q,i,j)
             = Σ body : Fin 6, BodyFourier(payload_body_trace,body,q,i,j)

h_regularizer :
  NewtonEulerMass^mu = NewtonEulerMass^0 + mu * I
                      and FourierMass^mu = CSV610Mass + mu * I
```

All three statements must be in one receipt and use the same
`source_key/state_key/mu`; `h_body` must be six concrete proofs, not a
structure field or target proposition. `h_aggregate` must be a function-level
identity for all q in the domain, not an all-rows numeric comparison.

## Exact obstruction

The missing atomic fact is:

```text
∀ body q i j,
  contractMass(sourceContract q, body, routeBMass body, routeBInertia body) i j
    = bodyTraceEvaluator body q i j.
```

The next missing aggregate fact is the corresponding finite-row function lift
from `massPayload` (610 rows) to the sum of those six body evaluators. Until
these are supplied and compiled under the canonical keys, the available
sidecars cannot assert `FourierMass = NewtonEulerMass^mu`; `source_binding_proven`
must remain false.

No registry/state mutation was made, and no Float64 or numerical candidate was
used as proof.
