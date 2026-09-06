# B45-1.2 frame recursion receipt

Status: PASS — `COMPILED_CANDIDATE_COMPARATOR_PENDING`

Successful run: `output/run-k87wlFSd`

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`
- `FourierNormalForm_COMPILE_EXIT_CODE=0`
- `FrameRecursion_COMPILE_EXIT_CODE=0`
- `VERIFY_EXIT_CODE=0`
- all exported frame-recursion theorems report only `propext`,
  `Classical.choice`, and `Quot.sound`
- no `sorry`, `admit`, or nonstandard axiom

| Artifact | SHA-256 |
|---|---|
| `FrameRecursion.lean` | `3361f2353b44052e6426e6b41e9f009cf4e5b3c6675a846ab856c1b82616cf10` |
| `FrameRecursion.olean` | `abf9e99fce858a3cbf94b3bf20238a9f6dcc701370a296676ffc52e0dbd9814b` |
| imported `FourierNormalForm.lean` | `56ec2f2d29a22942bcb83a3ba98197ae1ce4d607340072b81c013b8d358d3218` |
| imported `FourierNormalForm.olean` | `49d9dfaf04dae88f70301d697c26548ef65b5dcb3cd750b7a79eb2a7715917f1` |

The reusable contract is `prefixFrames_cons`:

`prefixFrames parent (current :: tail) = parent :: prefixFrames (parent * current) tail`.

`terminalFrame_eq_product` proves that the resulting terminal frame is
`parent * frameProduct steps`.  `routeBStepMatrix` uses the exact Route-B
phase, alpha, `a`, and `d` constants from the Fourier normal-form sidecar,
and `routeBFrameChain_cons` instantiates the same parent-axis-before-current
step contract for `(k,q)` pairs.

This is an exact finite matrix recursion only.  It does not bind Julia
`Float64` transforms, source frame/axis indexing, COM/Jacobian conventions,
or the full q-dependent mass function; those remain open B45-1 obligations.
