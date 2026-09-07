# Route-B P4 decimal/source-binding audit

Run the focused audit from PowerShell:

```powershell
python audit.py --external-root C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized
```

The checker separates three claims:

1. decimal spelling equality: the CSV token and its exact rational reification;
2. Float64 value equality: equality of the parsed IEEE-754 binary64 value;
3. true-DH mass equality: equality with the canonical Julia `mass_matrix` under
   its stated regularization semantics.

Only the first two are locally checkable from the exported token. The third is
fail-closed `PENDING` until an exact DH model, pinned Float64 execution trace,
regularization witness, and a sound bridge to the real statement are supplied.

`DecimalReification.lean` is the corresponding small kernel-checked leaf. It
proves decimal reification only and must not be promoted to the verified
registry as a source-binding theorem.
