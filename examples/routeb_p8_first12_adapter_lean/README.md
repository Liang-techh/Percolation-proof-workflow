# Route-B P8 first-12 ramp-elimination adapter

Task: `T-P8-008`  
Formalization Agent: `苏梦辰`  
Mathematics source: `review-T-P8-008-guyuefangyuan-20260907T0231.md` (`古月方源`)

This sidecar formalizes the source-independent algebraic part of the P8 adapter.
It keeps the literal 13-state source and the 14-state ramp lift deliberately
separate, and authenticates only coordinates `0..11` of the source.

Formalized statements:

- `forgetTail_rampLift`: forgetting the 14-state tail from `rampLift m c t`
  gives the exact 13-state source input `(m, c*t)`;
- `timeLift_first12_on_ramp`: the first twelve outputs of the existing
  `timeLift` reduce exactly to the explicit-time mechanical field obtained by
  substituting `w = c*t` into the source;
- `timeLift_tail_on_ramp`: the adapter-owned tail is `(w',c')=(c,0)`;
- `repair13_preserves_first12` / `repair13_tail`: repairing the source tail
  changes no mechanical output and sets only the tail derivative to `c`;
- `repair13_eq_source_at_iff_c_zero` and
  `repair13_eq_source_iff_c_zero`: under the typed literal-source premise
  `S(x)_w = 0`, repaired and literal fields agree exactly only for `c=0`;
- `repair13_ne_source_of_c_ne_zero`: a nonzero ramp therefore cannot be
  advertised as equality with the literal zero-tail 13-state source.

The sidecar intentionally does **not** bind Julia `full_rhs!`, prove ODE
existence/continuation, interval enclosure, flowpipe coverage, terminal transfer,
provenance/admission, or mutate the theorem registry.  Those remain separate
physical/source gates.

`verify.sh` is `CI_PORTABLE=1`: it resolves `lake` from `PATH`, checks the pinned
Lean toolchain against `examples/local_fkg`, compiles the existing P8 Picard and
contract-adapter dependencies first, then compiles this file with
`-DwarningAsError=true` and audits printed axioms for `sorryAx`.
