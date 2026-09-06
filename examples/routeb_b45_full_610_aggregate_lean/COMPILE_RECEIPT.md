# Compile receipt — full 610-row aggregate comparator seam

Status: **PASS — exact-real conditional bridge compiled**

Pinned compiler: Lean 4.33.1, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.

Pinned Mathlib cache: `0df444a360eaa60ab8c11dca51a86af692955474`.

The command used the existing pinned `SourceMassFourierBridge.olean` and the
pinned package libraries, then compiled:

```text
lean -DwarningAsError=true --root=<sidecar> \
  -o <sidecar>/Full610AggregateComparator.olean \
  <sidecar>/Full610AggregateComparator.lean
```

Result: exit code `0`.

Artifact hashes:

```text
Full610AggregateComparator.lean  504a6947c0a627cee42f4df9304d332082e3668a3f26c34c9febc07b3bc56fe4
Full610AggregateComparator.olean 6232006ca5c4b330973b3e59fa87f365a76a4d058dd98e708cb343a0b03870a6
```

The three `#print axioms` reports contain only `propext`,
`Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, or `axiom` is used.

This receipt does not discharge the two comparator premises, the physical
DH-to-Fourier function identity, or the Julia `Float64` implementation bridge.
