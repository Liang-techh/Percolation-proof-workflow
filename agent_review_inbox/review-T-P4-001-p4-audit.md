---
kind: review_result
task_id: T-P4-001
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P4-001 review: exact Schur leaf versus true residual/source binding

## Scope and inspected evidence

Inspected:

- `examples/routeb_p4_next_child/P4RationalSchurAbsorption.lean`
- `examples/routeb_p4_next_child/README.md`
- `examples/routeb_p4_next_child/REPORT.md`
- `examples/routeb_p4_next_child/verify.sh`
- `examples/routeb_p4_next_child/verify.log`
- `examples/routeb_p4_decimal_source_binding_audit/audit.py`
- `examples/routeb_p4_decimal_source_binding_audit/audit_report.json`
- `examples/routeb_p4_decimal_source_binding_audit/REPORT.md`
- external source snapshot and provenance under `routeB_dense_Mq/`

The exact Schur leaf proves an algebraic implication only. It consumes a
premise of the form `residual^2 ≤ ell^2*y^2`, with `p=3/5`, `ell=1/100`, and
`d=116667666666667/10^15`. It does not construct `residual` from the Julia
true-DH dynamics, prove that `d` is the DH mass entry, prove cell coverage, or
prove that the residual envelope holds over the physical domain. Therefore it
is a reusable downstream consumer, not a P4 physical certificate.

## Reproduced commands and results

1. Exact Schur Lean leaf (pinned environment):

```text
cwd: examples/local_fkg
command: C:\Users\z5242\.elan\bin\lake.exe env lean -DwarningAsError=true ..\routeb_p4_next_child\P4RationalSchurAbsorption.lean
exit_code: 0
axiom output: only propext, Classical.choice, Quot.sound
AXIOM_AUDIT: PASS (no sorryAx, admit, or custom axiom)
```

Source SHA-256:

```text
P4RationalSchurAbsorption.lean
CA3511B93A22D11D3E1D7BA9BDE2CB60CA1DCD426736A70E9979325BFD4EC96C
```

2. Decimal/source audit, direct underlying command (the checked-in
`verify.ps1` wrapper currently treats a named argument as positional and
therefore exits 2; this is recorded rather than hidden):

```text
python examples/routeb_p4_decimal_source_binding_audit/audit.py --external-root C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized
exit_code: 0
decimal_spelling_equality: PASS
float64_value_equality: PASS
true_dh_mass_equality: PENDING
formal_certificate_allowed: false
verified_registry_mutation: false
```

Audit report SHA-256:

```text
audit_report.json
BC2C2E0C32D5FD3171E0CA05D821B76EF283E5AB1C0D56B7181BD2442CA821F3
```

External provenance hashes recorded by the audit:

```text
routeB_dense_Mq/routeB_Mq_M0.csv
28D98AD71D1D6C2CBE830872CAD9077F2F7B4E2D932794217EB68868FD2E2B40
routeB_dense_Mq/dhport_lib.jl
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

## Consumption judgment

The exact leaf can be connected to P4 only through a new receipt adapter that
supplies, for the same fixed cell and channel:

1. canonical-source identity and hash;
2. an executable/pinned Float64-to-real or outward-interval semantic bridge
   for the mass coefficient and all residual inputs;
3. the actual force/acceleration normalization (the C2 audit forbids silently
   substituting a force residual for an acceleration residual);
4. interval coverage for the cell and a proof of the pointwise residual
   envelope; and
5. domain-wide aggregation/coverage before M4 admission.

Decimal reification and equal IEEE-754 bits establish neither item 2 nor item
 3. The abstract Lean premise must remain visibly conditional. No registry,
state, or admission flag was changed by this review.

## Next child theorem

`P4_TRUE_DH_RESIDUAL_ENVELOPE_ON_CELL`:

> For one fixed Route-B cell and Schur channel, a pinned canonical true-DH
> execution trace, with explicit force-to-acceleration normalization, yields
> certified interval bounds for `d`, `p`, and the actual residual, from which
> `residual^2 ≤ ell^2*y^2` follows pointwise; instantiate
> `RouteBP4NextChild.residual_absorption` only after those premises are
> independently admitted.

Minimum receipt fields: source commit/hash, cell coordinates, q/witness trace,
IEEE operation/rounding witness, regularization semantics, interval enclosure,
normalization map, residual formula, coverage statement, checker command and
exit code, Lean OLean hash, and explicit `true_dh_binding` status. Until these
fields are complete, integration status is `pending` and P4/M4 remain open.
