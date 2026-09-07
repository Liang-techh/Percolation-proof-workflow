# O1 human body-3 source expansion and trace fold

Status: `OPEN_BODY_3_SOURCE_AND_TRACE_PREMISES`

Scope is restricted to human body-3, zero-based body `2`.  No other body leaf
was modified, and no Lean/Lake command was run.

## Exact piecewise target

The adapter now defines independent `Prop` targets for source expansion and
trace reduction.  The target real evaluator is:

```text
(0,0) = 80467/600000 + (63/3125) sin(q 1)
                    - (1323/100000) cos(2*q 1)
(0,1) = (1,0) = -(63/20000) cos(q 1)
(1,1) = 21469/150000
(1,2) = (2,1) = (2,2) = 7/60
otherwise = 0
```

The corresponding tagged terms are the `nu2=±2`, `nu2=±1`, and zero-frequency
rows for `(0,0)`, the `nu2=±1` rows for `(0,1)` and `(1,0)`, and the constant
rows for the remaining five nonzero entries.  The exact rational labels are
recorded in the canonical receipt.

## Minimal source proof path

Use the existing source-contract slot bridge, then add compiled pointwise
lemmas for slots 0 through 3:

1. `o0=0`, `o1=(2/25*c0,2/25*s0,1/10)`;
2. `o2-o1=(21/100*s1*c0,21/100*s1*s0,21/100*c1)`;
3. `o3-o2=(1/20)*z2` and `z2=z1=(-s0,c0,0)`;
4. `z0=(0,0,1)` and `z0 ⟂ z1`, with `z1=z2`.

For body 2, reduce inactive columns after column 2.  The required Gram
identities are:

```text
Jv0 = (2/25 + (21/100)*s1) z1 - (1/40) x0
Jv1 = (21/100) * (c1*x0 - s1*e3)
Jv2 = 0
Jw0 = e3, Jw1 = Jw2 = z1
```

With mass `3/5` and diagonal isotropic inertia `7/60`, `ring_nf` plus
`sin_sq_add_cos_sq` and the double-angle identity yields the displayed
coefficients; cross terms use the explicit orthogonality identities.

## Minimal trace-fold path

Apply `List.foldl_append` to the generated body blocks, eliminate rows whose
body/row/col guard does not match, and reduce the body-3 block entrywise.  For
`(0,0)`, combine the five signed frequency atoms using sine parity and cosine
parity.  For the other nonzero entries, reduce the two frequency atoms or the
constant atom; all remaining guards fold to zero.

`h_body_3_of_entry_targets` only composes the two open premises into the
existing `h_body_3` proposition.  It is not a proof of either premise and is
not a source receipt.

## Canonical receipt and hashes

Receipt: `examples/routeb_b45_source_comparator_lean/O1_BODY_3_SOURCE_BRIDGE_RECEIPT.json`

```text
RouteBO1PerBodyTraceAdapter.lean
C6FC99DE41F8A5010CD79F18B89FD39811B63717810E437A5AE88DD6095F2FE7

BodyTraceEvaluator.lean
B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA

body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

O1_BODY_3_SOURCE_BRIDGE_RECEIPT.json
36F9206FA3AF2651751193D209B1622B4B8D30D40D98C35410D31D1BB959DD4E
```
