# T-P4-033 O0 — H_acc deployed-source semantic export

## Verdict

`OPEN_H_ACC_NO_DEPLOYED_SEMANTIC_EXPORT`.

This review isolates the physical source-binding atom `H_acc`. It does not
consume `baseline_budget` or any Schur margin, does not run Lean/Lake, and does
not claim `VERIFIED`.

## Exact target

Let

```text
Q1000 = { q in R^6 | forall k in {1,...,6}, abs(q_k) <= 1/1000 }.
```

The deployed pre-regularizer accumulator is the six-body sum before the final
`regularization*I` term. The exact-real target is

```text
M_NE^0(q)
 = sum_{ii=1}^6 [
     m_ii * Jv_ii(q)^T * Jv_ii(q)
   + Jw_ii(q)^T * R_ii(q) * (I_val_ii/3 * I_3)
       * R_ii(q)^T * Jw_ii(q)
   ].
```

The source-binding theorem must be split into two contracts; a Float64
machine equality is not silently identified with an exact-real equality:

```text
H_acc_expr(source_key):
  forall q in Q1000,
    RealSemantics(M_acc^J-DAG(q)) = M_NE^0(source_key,q).

H_acc_round(source_key):
  forall q in Q1000,
    DecodeFloat64(M_acc^J(q))
      belongs to RoundInterval(M_NE^0(source_key,q), epsilon_acc(q)),
  with an explicit outward rounding enclosure epsilon_acc.
```

`H_acc_expr` is the semantic identity. `H_acc_round` is a separate runtime or
interval contract and normally has a nonzero error radius.

## Deployed source anchors

The audited deployed source is
`C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\dhport_lib.jl`.

- `dhport_lib.jl:46-48`: `mass_matrix`, `M=zeros(6,6)`.
- `dhport_lib.jl:49-52`: body loop `ii=1:6`, midpoint COM
  `0.5*(o[:,ii]+o[:,ii+1])`, body rotation `Ri`, and isotropic inertia
  `(I_val[ii]/3)*I`.
- `dhport_lib.jl:53-57`: zeroed Jacobian blocks, prefix loop `jj=1:ii`,
  `Jv[:,jj]=cross(z[:,jj],pcom-o[:,jj])`, and `Jw[:,jj]=z[:,jj]`.
- `dhport_lib.jl:58-59`: per-body Gram contribution is accumulated into `M`.
- `dhport_lib.jl:60`: final `Float64(regularization)*I` is added outside the
  six-body loop and is excluded from `M_acc^J`.

The source snapshot hash is
`aebe6db09b2d943448c5d701631109db8a5eeb070cc66593e5dbaca26485936`.

## Provenance and present evidence

The available body-instrumentation report is bound by:

```text
REPORT.md sha256       = c0af0ce130c147430665568b39d0f327cb84aa67e6d3350a4ea785a86ca08066
deployed dhport hash   = aebe6db09b2d943448c5d701631109db8a5eeb070cc66593e5dbaca26485936
exact generator hash   = 9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b
frozen Fourier CSV     = a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
instrumented copy hash = fc95e8e070dc146349a3abc7743f4a51498f9563650d6881e960f8e2976d16fd
```

That report records an exact-generator self-check:

```text
aggregate_equals_sum_body_exact = true
aggregate_vs_frozen_csv_exact   = true
aggregate rows                   = 610
body trace rows                  = 727
random Fourier max error         = 8.881784197001252e-16
```

This is useful structural evidence for the body sum and its order, but it is
not a deployed Julia semantic export: the report explicitly says that the
exact Fourier generator is an artifact-local Python copy, does not prove
extensional equality with Julia Float64 `mass_matrix(q)` for every `q`, and
the proposed Julia trace patch was not applied or executed. No runtime
pre-regularizer trace or interval enclosure is therefore available.

## Binding matrix

```text
source hash                  bound to deployed text: yes
body order ii=1..6           source-text bound: yes
matrix/index order           Julia 1-based source-text bound: yes
jacobian prefix jj=1..ii     source-text bound: yes
axis timing                  z[:,ii] before current transform: report/source bound
COM rule                     midpoint of o[:,ii], o[:,ii+1]: report/source bound
q-domain Q1000               absent from deployed theorem/export: open
exact-real target M_NE^0     absent as a deployed-bound export: open
M_acc^J runtime witness      absent: open
rounding/interval enclosure  absent: open
Julia-to-exact evaluator map absent: open
```

## Precise obstruction

The source text determines a plausible finite operation order, but source text
plus finite exact-generator traces do not establish either required semantic
bridge:

1. there is no exported evaluator map from every deployed Julia node
   (`Tc`, `o`, `z`, `Jv`, `Jw`, `Ri`, body Gram term, and accumulator update) to
   the exact-real nodes defining `M_NE^0`; and
2. there is no all-`q` interval receipt over `Q1000` that encloses the actual
   Float64 pre-regularizer result and the exact-real target with recorded
   operation order.

The distinction is material even for a fixed expression shape. For example,
with binary64 round-to-nearest, `fl(1 + 2^-54) = 1`, while the exact real value
is `1 + 2^-54`. Thus source DAG shape, a source hash, and finite point traces
cannot prove exact machine equality with `M_NE^0`.

## Immutable receipt state

```text
status                         = OPEN_H_ACC_NO_DEPLOYED_SEMANTIC_EXPORT
source_hash_bound              = true
loop_index_order_bound         = source-text only
q_domain_bound                 = absent from deployed mass_matrix theorem/export
exact_real_target_bound        = absent
runtime_pre_regularizer_trace  = absent
interval_rounding_enclosure    = absent
finite_exact_fourier_copy      = present but not Julia-bound
baseline_consumed              = false
schur_consumed                 = false
verified                       = false
```

## Minimal next artifact

Produce one of the following artifacts, fixed to the same source snapshot:

```text
routeb_o0_h_acc_pre_regularizer_export/
  SOURCE_SNAPSHOT/dhport_lib.jl
  source_dag_manifest.json
  pre_regularizer_trace.csv or interval_boxes/
  exact_target_definition.json
  verify_h_acc_export.py
  RECEIPT.md
```

The manifest must bind `source_key`, deployed source hash, exact-target hash,
and a typed evaluator map for all nodes listed above. For every exported state
or interval box it must include all 36 pre-regularizer matrix entries, the six
body contributions, the 1-based `ii`/`jj` order, axis timing, midpoint COM
rule, and the declared `Q1000` coverage. An acceptable semantic receipt is
either an exact DAG identity (`H_acc_expr`) or a complete outward interval
proof (`H_acc_round`) with per-entry bounds, trig-node enclosures, matrix
product/accumulation rounding, stdout/stderr, and exit code. Sampling or
self-comparison of an uncoupled exact generator is insufficient.

## Conclusion

`H_acc` remains open at the deployed-source semantic-export boundary. The
available hashes and body-loop anchors fix the candidate source contract, but
the missing artifact is specifically a same-source, all-`q` evaluator/interval
receipt connecting Julia's pre-regularizer accumulator to exact-real `M_NE^0`.
No baseline, Schur, Lean, Lake, or deployed-tau equivalence claim is consumed
or made.
