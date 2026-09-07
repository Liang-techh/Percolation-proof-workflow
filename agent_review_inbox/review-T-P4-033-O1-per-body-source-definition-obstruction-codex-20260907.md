# T-P4-033 O1 — immutable review: per-body exact-DH seam

## Narrow result

The existing source comparator can now be expanded to a concrete exact source
body evaluator:

```lean
sourceBodyMass q body :=
  contractMass (sourceContract q) body
    (routeBMass body) (routeBInertia body)
```

The candidate `RouteBO1PerBodyExactSource.lean` also exposes the six-body
generic theorem

```lean
∀ body : Fin 6,
  sourceBodyMass q body =
    bodyMass (sourceContract q).origins (sourceContract q).axes body
      (routeBMass body) (routeBInertia body)
```

and the existing exact frame/source bridge target
`sourceBodyMass_eq_juliaExactBodyMass`.

## Exact remaining seam

The six `h_body` goals remain open because the current source artifacts do not
define a Lean term for the body-labelled Fourier evaluator:

```lean
∀ body q i j, sourceBodyMass q body i j = fourierBody body q i j
```

The 727-row body trace supplies rational coefficients, but only as CSV/sidecar
data. It is not yet a Lean `fourierBody : Body → Q6 → Fin 6 → Fin 6 → ℝ`
joined to `sourceBodyMass`. This is the smallest missing typed artifact; no
new aggregate data is required.

## Minimal real function-lift lemma

The candidate marks the required analytic lift:

```lean
theorem realFourierAtom_complex_re_target
    (nu : Fin 6 → ℤ) (a b : ℚ) (q : Fin 6 → ℝ) :
    Complex.re (((a : ℂ) + (b : ℂ) * Complex.I) *
      Complex.exp (Complex.I * (phase nu q : ℂ))) =
      realFourierAtom nu a b q
```

Together with `realFourierAtom_add`, this is the minimal lemma needed to lift
keywise rational coefficient equality to the real `cos/sin` function equality
used by `h_aggregate`. The candidate is uncompiled; no verification claim is
made.

## Typed obstruction and executable correction

The required correction is a generated Lean `bodyTraceEvaluator` from the
hashed body trace, followed by six proofs of `h_body` against the concrete
`sourceBodyMass`. The generated evaluator must preserve body labels, row/col
labels, Fourier frequency, rational real/imaginary coefficients, and the same
source/state/q-cell key. After that, compile this candidate and apply the
real-function lift above. The current status is
`OPEN_TYPED_FOURIER_BODY_EXPORT`, not an abstract-only algebra obstruction.

The exact per-body source definition and typed obstruction are recorded in:

```text
examples/routeb_b45_source_comparator_lean/
  RouteBO1PerBodyExactSource.lean
  O1_PER_BODY_COMPARATOR_RECEIPT.json
```

## Hashes

```text
RouteBO1PerBodyExactSource.lean
C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553

O1_PER_BODY_COMPARATOR_RECEIPT.json
F7AEF8B7D2B5952E43A8E34BB16DBF4AA07A3238901967DB4E138F7AAE231C24

SourceBodyMassExtensionalProbe.lean
BC2A2136576AC0A726F168492789A24703642D44865C1CCE6AE9EEF57955F76B

body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

exact trace checker
11E84251109CFC297D806287AF783607C9765B2C6AC6B27CB0B91A636DE23073
```

## Immutable disposition

`sourceBodyMass = bodyMass`: exact candidate definition present.

`h_body`: blocked only by missing typed body-labelled Fourier evaluator and
the six source-to-Fourier proofs.

`real cos/sin lift`: minimal lemma target present, uncompiled.

No state or registry mutation was made.
