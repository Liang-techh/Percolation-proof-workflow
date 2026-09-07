# P3 exact DH-to-Fourier 36-entry source-binding leaf

This sidecar contains the smallest honest bridge that can be closed from the
current evidence.

`check_exact_coefficient_bridge.py` reads the canonical
`routeB_dense_Mq/dhport_lib.jl` by its locked SHA-256, interprets its decimal
parameters as rationals and its `pi/2` offsets as exact quarter turns, and
evaluates the complete 6x6 mass formula in a Gaussian-rational Laurent ring.
It compares all 36 coefficient maps against the frozen 610-row rational
Fourier mass table, adding the exact `1/1000000` diagonal regularizer.  This
closes an all-entry exact executable checker leaf, for every real `q` by the
standard Laurent evaluation interpretation.

`ExactCoefficientBridge.lean` proves the downstream kernel theorem:
equal coefficient maps imply equal real Fourier evaluators for every `q` and
all 36 matrix entries.  Its coefficient equality is an explicit premise; the
external Julia source is not silently treated as a Lean definition.

Run from the workflow root:

```powershell
python examples/routeb_fourier_source_binding_lean/check_exact_coefficient_bridge.py
wsl -d Ubuntu -- bash examples/routeb_fourier_source_binding_lean/verify.sh
```

The exact leaf does not prove Julia `Float64` execution, libm rounding,
directed intervals, the physical trajectory theorem, or a full Lean
source-to-table instantiation.  Therefore it is not registry-promotable as a
physical or formal Route-B certificate.
