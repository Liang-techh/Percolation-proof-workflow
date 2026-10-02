---
kind: review_result
review_id: review-T-P3-015-liuchuanafeng-20261002T0515Z
source_agent: 流川枫
created_at: 2026-10-02T05:15:00Z
inspected_commit: 00b8077b1b9f6db68275d2ca0fd8b66badeb206a
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_m33_exact_lower_lean/README.md
  - examples/routeb_m33_exact_lower_lean/M33LowerBound.lean
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/SHA256SUMS.csv
  - examples/routeb_source_binding_audit/snapshots/current_exact/routeB_fourier_mass_full_rational.csv
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
task_id: T-P3-015
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P3-015 admission probe: exact M33 Fourier leaf lift

## Question

Does commit `00b8077b1b9f6db68275d2ca0fd8b66badeb206a` contain `P3.m33_exact_fourier_source_leaf` and `task_routeb_source_fourier_binding_current`, with a kernel-friendly coefficient identity that preserves the canonical `dhport_lib.jl` hash, the rationalization convention, an 11-mode witness, and active angles `{q4,q5}`?

## Decision

**No named leaf, so keep `admission_label: pending`.** The named predicate and external artifact are absent. The nearest in-tree packet does preserve the cited source hash and an 11-mode `{q4,q5}` witness, and those modes reduce to the sidecar Fourier formula only after adding the diagonal regularizer `1/10^6`. That reduction is a rational coefficient identity, not source equality, not a Lean receipt, and not Float64 semantics.

This is not a rejected false formula: the coefficient pairing holds. It is not `compiled_candidate` or `verified`: no theorem states the identity, and no pinned checker was executed. It is not architecture-only.

## Evidence inspected (read-only)

1. **Named source packet is not in this commit.**
   Queue scope names `P3.m33_exact_fourier_source_leaf` and `task_routeb_source_fourier_binding_current`. Neither path exists. The lower-bound README cites the artifact by name only and does not vendor it. GitHub code search for those identifiers returned no hits (`incomplete_results` may hide matches; absence was also checked against the recursive `examples/` tree).

2. **Canonical hash is preserved on the in-tree snapshot, not on a new exporter.**
   `examples/routeb_source_binding_audit/SHA256SUMS.csv` records `snapshots/original_target/dhport_lib.jl` SHA-256 `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` (3832 bytes). That matches the hash cited by `examples/routeb_m33_exact_lower_lean/README.md`. Blob SHA of the Julia file is `27cf497b6f27919eb5b554369fb1444f4314c942`. This review did not re-hash the file and did not re-prove that the snapshot equals a deployed `routeB_dense_Mq/dhport_lib.jl`.

3. **11-mode witness, active angles `{q4,q5}`.**
   `routeB_fourier_mass_full_rational.csv` (blob `d7840a9c2e9c0485bcd78f209af7143e4e3ed303`; manifest SHA-256 `a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8`) has exactly 11 rows with `row=3,col=3`. Every row has `nu1=nu2=nu3=nu6=0` and `imag_num=0`, so only `q4` and `q5` appear. Rationalization convention in the CSV is `real_num/real_den` with denominator `imag_den=1`.

   Nonzero frequency pairs `(nu4,nu5)` and coefficients:

   - `(0,0)`: `2431931/9600000`
   - `(0,±1)`: `399/400000` each
   - `(0,±2)` and `(±2,0)`: `147/6400000` each
   - `(±2,±2)` and `(±2,∓2)`: `-147/12800000` each

4. **Coefficient identity, conditional on cosine pairing and the regularizer.**
   Pairing even modes as `2 a_nu cos(nu·q)` gives

   - `cos(q5)` coefficient `399/200000`
   - `cos(2 q4)` and `cos(2 q5)` coefficients `147/3200000`
   - `cos(2 q4±2 q5)` coefficients `-147/6400000`

   The product identity `cos A cos B = (1/2)(cos(A+B)+cos(A-B))` then matches the sidecar factor `147/3200000 * (cos(2 q4)+cos(2 q5)-cos(2 q4)cos(2 q5))`. The constant matches the README formula only after the source diagonal regularizer:

   `2431931/9600000 + 1/1000000 = 12159703/48000000`.

   Exit code of this `Fraction` replay: `0`. This is not a kernel proof. `M33LowerBound.lean` consumes the closed form and does not mention the 11 modes, the CSV hash, or `dhport_lib.jl`.

5. **Source equality remains the open obligation.**
   `examples/routeb_source_binding_audit/REPORT.md` classifies full `M(q)` reconstruction as OPEN (B45-1). It records that the Fourier generator is a parallel analytic interface and that `ReferenceMass.lean` is literal, with `physical_DH_identification_proved=false`. The 11-mode reduction does not discharge that gate.

## Assumptions still required

- the cosine-even pairing is the exporter's actual evaluation convention;
- the CSV constant excludes `10^-6 I`, and the sidecar constant includes it;
- functional equality between `dhport_lib.jl` `M[3,3]` and the CSV evaluator;
- Float64/libm rounding, all-entry binding, and P3 coverage, all still separate.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P3-015` open.
- Requested action: do not register an M33 Fourier source leaf; do not edit registry, `state.json`, or formal certificates.
- Next owner should attach `task_routeb_source_fourier_binding_current` or a theorem whose hypotheses are the 11 modes, the cosine pairing, and `+1/10^6`, explicitly not implying Float64 or all-entry coercivity. The pinned Lean slot should not treat `m33_lower_bound` as this child.

## Forbidden-boundary compliance

- Did not use grid samples as formula equality.
- Did not treat the exactized formula as Float64/libm semantic equivalence.
- Did not claim mass coercivity, inverse bounds, or P3/formal-gate closure.
- Did not promote the checker leaf or this review to the verified registry.
- Did not edit registry, state, or formal proofs.
