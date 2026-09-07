# O1 human body-4 source expansion and trace fold

Status: `OPEN_BODY_4_SOURCE_AND_TRACE_PREMISES`

Scope is restricted to human body-4, zero-based body `3`.  The evaluator was
not regenerated, no other body target was changed, and no Lean/Lake command
was run.

## Exact piecewise Fourier target

The adapter defines `body_4_piecewise` and separate source/trace `Prop`
targets.  With `x = q (1 : Joint)` and `y = q (2 : Joint)`, the target is:

```text
(0,0) = 48511/600000 + (42/3125) sin(x) + (19/3125) sin(x+y)
       - (441/50000) cos(2x) + (399/50000) cos(y)
       - (399/50000) cos(2x+y) - (361/200000) cos(2x+2y)
(0,1) = (1,0) = -(19/10000) cos(x+y) - (21/5000) cos(x)
(0,2) = (2,0) = -(19/10000) cos(x+y)
(0,3) = (3,0) = (1/15) cos(x+y)
(1,1) = 211/2400 + (399/25000) cos(y)
(1,2) = (2,1) = 21083/300000 + (399/50000) cos(y)
(2,2) = 21083/300000
(3,3) = 1/15
otherwise = 0
```

The receipt preserves the signed `nu2,nu3` rational coefficient labels for
the source trace.  No coefficient equality is promoted to a Lean proof.

## Minimal source expansion path

The body-4 source target is the direct `bodyMass` Gram expansion with
`routeBMass 3 = 2/5` and isotropic diagonal inertia `1/15`.  The reusable
geometric lemmas needed are:

1. expand prefix slots 0 through 4, including origins and parent axes;
2. establish `z0=(0,0,1)`, `z1=z2=(-sin(q0),cos(q0),0)`, and an explicit
   `q1,q2` formula for `z3`;
3. establish `o4-o3=(19/100) z3`, hence body-4 `Jv` column 3 is zero;
4. reduce active `bodyJv/bodyJw` columns and their dot products, with the
   q0 terms cancelling by orthogonality;
5. normalize the seven-term `(0,0)` expression and the remaining nonzero
   entries using sine/cosine parity, `sin_sq_add_cos_sq`, and double-angle
   identities.

These are required lemmas/targets, not receipts.

## Minimal trace-fold path

Use `List.foldl_append` over the generated body blocks, eliminate mismatched
body/row/col guards, and reduce the body-4 block entrywise.  Pair the signed
frequency terms for `(0,0)`, `(0,1)`, `(1,0)`, `(0,2)`, `(2,0)`, and `(0,3)`,
`(3,0)`; reduce the constant terms separately.  The result must match
`body_4_piecewise`, after which `h_body_4_of_entry_targets` is only a
conditional composition.

## Fail-closed boundary

No source expansion premise, trace-fold premise, or `h_body_4` proof is
asserted.  Registry/comparator/formal-certificate admission remains false.

Receipt: `examples/routeb_b45_source_comparator_lean/O1_BODY_4_SOURCE_BRIDGE_RECEIPT.json`

## Hashes

```text
RouteBO1PerBodyTraceAdapter.lean
25F099EC5EB7F699C789AE29AA45DF0FBB24FF06547F498740968F5E1B3C9976

BodyTraceEvaluator.lean
B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA

body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

O1_BODY_4_SOURCE_BRIDGE_RECEIPT.json
488ABD76AD0F5548CFA85A690C9505748806FF8AF324FBA90C08D06D1E44A5A4
```
