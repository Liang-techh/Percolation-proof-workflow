# Compile receipt: SourceMassFourierBridge

## Pinned wrapper refresh (2026-09-06)

- Status: `compiled candidate`.
- Wrapper: `lakefile.lean` with Lean `v4.33.1`; `.lake/packages` points to the
  existing `/home/z5242/sos_lean/.lake/packages` cache and uses its pinned
  `lake-manifest.json`.
- Command: `lake env lean SourceMassFourierBridge.lean -o
  .lake/build/lib/lean/SourceMassFourierBridge.olean`.
- Terminal log: `output/run-pinned-20260906/terminal.log`.
- Real output: `.lake/build/lib/lean/SourceMassFourierBridge.olean`.
- The log contains exit code `0` from the successful Lean invocation; the
  `#print axioms` output is retained and reports only `propext`,
  `Classical.choice`, and `Quot.sound` for the two bridge theorems.

This refresh changes only the verification environment. It does not discharge
the conditional `h_body` premise, the per-body comparator, the 610-row
aggregate binding, or the Float64/DH bridge.

- Target: `SourceMassFourierBridge.lean`
- Requested toolchain: `leanprover/lean4:v4.33.1`
- Command:

  ```powershell
  $env:LEAN_PATH = "...\\upstream\\formal-math\\percolation\\.lake\\build\\lib\\lean"
  elan run leanprover/lean4:v4.33.1 lean SourceMassFourierBridge.lean
  ```

- Result: failed before elaboration, exit code 1.
- Exact diagnostic:

  ```text
  error: unknown module prefix 'Mathlib'
  No directory 'Mathlib' or file 'Mathlib.olean' in the search path entries:
  ...\\upstream\\formal-math\\percolation\\.lake\\build\\lib\\lean
  c:\\Users\\z5242\\.elan\\toolchains\\leanprover--lean4---v4.33.1\\lib\\lean
  ```

## Audit conclusion

No `.olean` or `LEAN_VERIFIED` claim is emitted. The target has no independent
`lakefile.toml`, `lake-manifest.json`, or `verify.sh`, and the available search
path does not contain `Mathlib.olean`; therefore an independent pinned
4.33.1/Mathlib compile cannot be established from this workspace state.

The source theorem remains explicitly conditional on `h_body`; this receipt
does not discharge the per-body comparator and does not assert any 610-row
aggregate binding.
