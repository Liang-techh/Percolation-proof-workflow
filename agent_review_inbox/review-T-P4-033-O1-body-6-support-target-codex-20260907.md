# O1 human body-6 support/entry target

Status: `OPEN_BODY_LABEL_SEMANTIC_MISMATCH`

Scope is CSV body `6`, zero-based body `5`.  No Lean/Lake command was run and
no CSV equality was used as a proof.

## Machine-readable target

The generated target is:

`examples/routeb_b45_source_comparator_lean/O1_BODY_6_SUPPORT_TARGET.json`

It records the exact support evaluator shape:

```text
entry(row,col,q) = sum over tagged support rows r with the same row/col of
  (real_num/real_den) * cos(sum_k nu_k*q_k)
  - (imag_num/imag_den) * sin(sum_k nu_k*q_k)
```

The target that would be required after semantic repair is:

```text
forall q i j,
  sourceBodyMass q (5 : Fin 6) i j = body6TraceEvaluator q i j
```

This is recorded as blocked, not asserted.

## Sparse block summary

The selected `body=6` bucket contains 610 tagged rows and 32 matrix entries.
Using the existing `B=(4,5)`, `D=(1,2,3,6)` convention:

```text
D_D: 16 entries / 382 terms
D_B:  7 entries / 112 terms
B_D:  7 entries / 112 terms
B_B:  2 entries /   4 terms
```

The per-entry term counts and frequency coordinate bounds are stored in the
JSON target; no aggregate reconstruction is claimed here.

## Fail-closed semantic obstruction

The current body-labelled artifact places the complete 610-row
aggregate-shaped support under `body=6`.  Therefore it is not an admissible
human body-6 slice, and the target cannot be converted into `h_body_6`.
The smallest missing artifact is a separately emitted source-side Fourier
slice for human body 6, with an explicit `body=6` label, source/state key, and
entrywise provenance distinct from the aggregate payload.

## Next proof decomposition

```text
L0  bind the corrected body=6 slice to human body-6 sourceBodyMass
L1  expand sourceBodyMass q 5 through bodyMass/bodyJv/bodyJw
L2  define body6TraceEvaluator from the corrected sparse support
L3  prove every supported entry and the zero complement entrywise
L4  compose the result into h_body_6
```

Until L0 exists, L1–L4 remain blocked.  Registry, comparator, and formal
certificate admission remain false.

## Hashes

```text
generate_body6_support_target.py
4E81FDFFBF06230DC82D31E460349AAFB5A824A908D36304D4EABC0E2E97BBB8

O1_BODY_6_SUPPORT_TARGET.json
379D3D4CB91119FB5553AD718908001681AE30477272A6EFE6B5AB7526ECFFF9

body-labelled trace input
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

frozen 610-row source snapshot
A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8
```
