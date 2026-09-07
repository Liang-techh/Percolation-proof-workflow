---
kind: mathematical_frontier_review
task_id: T-P4-033-O1-AGGREGATE-FUNCTION-LIFT
source_agent: codex-local
date: 2026-09-07
status: OPEN_FORMALIZABLE_INDEPENDENT_LEAF
---

# O1 aggregate function lift — independent bottleneck

## Selection

当前 O1 parent 已拆成 7 个叶：一个 610-row finite-key 到 real `cos/sin` 的
`h_aggregate_function_lift`，以及六个 exact-DH body equalities。这里选择前者；
它不重复 `M_DD` source inhabitant、O0 strict margin、force source binding 或 O2
parent/sibling coverage。

当前 frontier 记录明确把 data-level aggregate exact pass 与 function-level Lean
lift 分开，并要求 source-bound evidence；见
`agent_review_inbox/task_queue.md:1968-1976`。

## Exact target

Use the existing types from
`examples/routeb_b45_full_610_aggregate_lean/Full610AggregateComparator.lean`:

```lean
abbrev Q6 := Fin 6 → ℝ
abbrev Mat6 := Fin 6 → Fin 6 → ℝ
abbrev Row := Fin 610

def complexEvalRow (r : CsvMassRow) (q : Q6) : ℝ :=
  Complex.re (((r.realCoeff : ℂ) + (r.imagCoeff : ℂ) * Complex.I) *
    Complex.exp (Complex.I * (phase r q : ℂ)))

def complexCsvAggregate (payload : Row → CsvMassRow) (q : Q6) : Mat6 :=
  fun i j => ∑ n : Row,
    if (payload n).row = i ∧ (payload n).col = j
    then complexEvalRow (payload n) q
    else 0
```

The first, purely function-level lift is:

```lean
theorem h_aggregate_real_lift
    (payload : Row → CsvMassRow) :
    ∀ q i j, complexCsvAggregate payload q i j =
      csvAggregate payload q i j := by
  intro q i j
  unfold complexCsvAggregate csvAggregate
  apply Finset.sum_congr rfl
  intro n hn
  by_cases h : (payload n).row = i ∧ (payload n).col = j
  · simp [h, complexEvalRow, realFourierAtom_complex_re_target]
  · simp [h]
```

For exactness, define `payloadCoeff payload i j ν : ℚ × ℚ` as the finite sum
over `n : Fin 610` of `(realCoeff, imagCoeff)` when the payload row/column and
frequency equal `(i,j,ν)`, and `(0,0)` otherwise. Define
`traceCoeff body i j ν : ℚ × ℚ` analogously by folding the tagged rows in
`bodyTraceRows` with `r.body=body`, `r.row=i`, `r.col=j`, and
`r.frequency=ν`; coefficient pairs use the tagged rational numerators and
denominators. Thus both are explicit finite rational functions, not runtime
samples.

The O1 aggregate leaf consumed by the parent is the stronger keyed composition:

```lean
theorem h_aggregate_function_lift
    (payload : Row → CsvMassRow)
    (h_keywise :
      ∀ i j (ν : Fin 6 → ℤ),
        payloadCoeff payload i j ν =
          ∑ body : Fin 6, traceCoeff body i j ν) :
    ∀ q i j,
      csvAggregate payload q i j =
        ∑ body : Fin 6, bodyTraceEvaluator body q i j := by
  -- finite-key regrouping, then h_aggregate_real_lift / atom additivity
  sorry
```

The `sorry` above is a target sketch only, not a proof claim. A final theorem
should replace it with the explicit finite sums and the existing
`realFourierAtom_add`/atom lift, with no opaque premise field. The keywise
premise must preserve the `Fin 6` row/column orientation and 610-row
cardinality.

## Dependencies

1. `CsvMassRow`, `phase`, `evalRow`, and `csvAggregate` are already defined at
   `Full610AggregateComparator.lean:32-50`.
2. One-based CSV labels must first be transported to `Fin 6`; the available
   round-trip API is at `Full610AggregateComparator.lean:15-30`.
3. The coefficient-to-real identity is the existing target
   `realFourierAtom_complex_re_target` at
   `examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyExactSource.lean:90-110`.
4. The body-labelled finite fold is `bodyTraceRows`/`traceAtom`/
   `bodyTraceEvaluator` at
   `examples/routeb_b45_source_comparator_lean/BodyTraceEvaluator.lean:778-813`.
5. The keywise equality `h_keywise` needs the frozen 610-row payload and
   727-row body trace under one source/hash key. It does **not** need the six
   exact-DH source equalities `h_body_1..h_body_6`; those remain separate
   parent leaves (`RouteBO1PerBodyTraceAdapter.lean:17-39`).

After this leaf, the existing conditional consumer theorem can use
`h_aggregate_function_lift` as its `h_aggregate` premise; it still cannot
identify `sourceBodyMass` with `fourierBody` or close O1 without all six
`h_body` leaves.

## Precise obstruction / counterexample

A single-state or data-level equality does not imply the required function
equality. Let one payload atom have `ν = 0, a = 1, b = 0`, and let an alternate
trace atom have `ν = (1,0,0,0,0,0), a = 1, b = 0`. At `q = 0` both values are `1`,
but at `q = (π,0,0,0,0,0)` they are `1` and `-1`. Thus a fixed-q comparator,
CSV hash, or aggregate row equality cannot discharge `∀ q`.

The remaining proof obligation is therefore exact keywise regrouping plus the
real `cos/sin` lift. The current generic atom lemma only handles one tagged
atom; no current theorem binds the complete 610-row payload function to the
body-labelled real evaluator. Until that bridge is proved and source-bound,
the status remains:

```text
h_aggregate_function_lift = OPEN
h_body_1..h_body_6 = OPEN independently
O1_parent = OPEN
formal_certificate_allowed = false
```

This review is a mathematical target/obstruction only; it does not claim
compile, source equality, runtime execution, or registry admission.
