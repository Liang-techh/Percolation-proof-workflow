# O1 body-2 source expansion and trace fold

Status: `OPEN_BODY_2_SOURCE_AND_TRACE_PREMISES`

This review addresses only the second body leaf.  No evaluator regeneration,
full-table audit, or Lean/Lake invocation was performed.

## Concrete exact target

`RouteBO1PerBodyTraceAdapter.lean` now contains the following independent
targets:

```text
h_body_2_source_expanded_target

  forall q i j,
    (4/5) * sum_a Jv₂(a,i) * Jv₂(a,j)
      + sum_a_b Jw₂(a,i) * I₂(a,b) * Jw₂(b,j)
    = piecewise_body_2_expression(q,i,j)

h_body_2_expected_entry_target

  forall q i j,
    sourceBodyMass q 1 i j = piecewise_body_2_expression(q,i,j)

h_body_2_trace_fold_target

  forall q i j,
    piecewise_body_2_expression(q,i,j)
      = bodyTraceEvaluator 1 q i j
```

The piecewise expression is:

```text
(i,j)=(0,0): 20953/100000 + (42/3125) sin(q 1)
                 - (441/100000) cos(2*q 1)
(i,j)=(1,1): 10441/50000
otherwise:    0
```

The existing `h_body_2_of_entry_targets` is only the conditional composition
of the two premises into `h_body_2`; it does not assert either premise.

## Minimal source proof path

The source side needs compiled pointwise lemmas for the first three source
frames/slots:

1. origin slot 0 is zero and parent axis joint 0 is world z;
2. origin slot 1 has translation `(2/25*cos(q 0), 2/25*sin(q 0), 1/10)`;
3. joint-1 parent axis is `(-sin(q 0), cos(q 0), 0)`;
4. origin slot 2 minus slot 1 is
   `(21/100*sin(q 1)*cos(q 0),
     21/100*sin(q 1)*sin(q 0),
     21/100*cos(q 1))`.

Then `bodyJv/bodyJw` active-column reduction gives orthogonal columns.  With
mass `4/5` and isotropic inertia `1/5`, the `(0,0)` term expands as

```text
1/5 + (4/5) * (2/25 + (21/200)*sin(q 1))^2
```

which normalizes to the stated cosine/sine expression using
`sin_sq_add_cos_sq` and the double-angle identity.  The `(1,1)` term is
`1/5 + (4/5)*(21/200)^2 = 10441/50000`; cross and inactive entries reduce to
zero by the axis/Jacobian orthogonality and inactive-column lemmas.

## Minimal trace proof path

Rewrite `bodyTraceRows` as the six generated body blocks, use
`List.foldl_append`, and eliminate non-body-2 rows through the guard in
`traceRowContribution`.  The body-2 block then has five `(0,0)` frequency
terms and one constant `(1,1)` term.  Reduce `tracePhase` to `q 1` and use
the real sine/cosine parity identities to obtain the displayed expression.

No source or trace premise is currently proved.  The only valid next step is
to compile these pointwise expansion lemmas in the pinned environment and
then discharge the two open targets before using the conditional composition.

## Hashes

```text
RouteBO1PerBodyTraceAdapter.lean
8D3AA7716897269F2885A471A225EA11995869944E7D623DE33978F442EE7EDB

BodyTraceEvaluator.lean
B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA

body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

O1_BODY_2_SOURCE_BRIDGE_RECEIPT.json
257F5EDB95FBF0CE8DDC410DB50D70C508137FD8F278BD76E387F79042D11124
```
