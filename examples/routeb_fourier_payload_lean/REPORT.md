# P3 payload report

## Result

`PENDING — CSV PAYLOAD REIFIED; EXACTIZED DH MAP EQUALITY OPEN`

The generator read the canonical exact rational mass CSV and verified before
emission:

```text
csv_sha256 = a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
csv_rows = 610
unique_(entry,frequency)_keys = 610
nonempty_matrix_entries = 32
full_matrix_index_cardinality = 36
```

`Payload.lean` uses the `FiniteTableReification` interface. The table fields
and theorems are kernel-checkable: key uniqueness, support completeness,
entry reconstruction, row cardinality, full-index cardinality, the four
empty supports, and exact row-to-lookup coefficient equality. Rational values
are literal `ℚ` expressions; no Float64, trigonometric evaluation, solver,
or Python theorem is imported into Lean.

## Focused verification

The intended command is:

```text
bash examples/routeb_fourier_payload_lean/verify.sh
```

It compiles only `ExactCoefficientBridge.lean`,
`FiniteTableReification.lean`, `PayloadRows.lean`, and `Payload.lean`, with
warnings treated as errors. It does not run the repository test suite.

## Boundary and next step

The payload gives a concrete CSV-side reification, not a DH-source theorem.
In particular, this sidecar intentionally does not assert

```text
exactizedDHSourceCoeff i j ν = frozenCsvCoeff i j ν
```

for any external exactized DH map. The next executable step is to implement a
separate, reviewed Lean reification of the DH Laurent recursion (or generate
small trusted recursion blocks) and discharge the per-row equality premise in
`conditional_source_csv_equality_on_support`. That step must also record its
source formula and normalization assumptions; this payload cannot substitute
for it.

The sidecar contains no proof escape-hatch declarations.
