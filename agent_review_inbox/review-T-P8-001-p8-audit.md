---
kind: review_result
task_id: T-P8-001
source_agent: Codex
created_at: 2026-09-06T21:00:00-06:00
integration_status: pending
---

# T-P8-001 — 13-state/14-state reachability contract audit

## Scope and inspected inputs

Inspected the current worktree at commit `35c34b4`, specifically:

- `docs/routeb-p8-flowpipe-binding-next.md`
- `docs/routeb-p8-next-concrete-child.md`
- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean`
- `examples/routeb_p8_contract_adapter/verify.sh`
- `examples/routeb_p8_rhs_payload_generator/receipt.template.json`

SHA-256 of the inspected local inputs:

| file | SHA-256 |
|---|---|
| `docs/routeb-p8-flowpipe-binding-next.md` | `47681DFC4DE2153B34AD8B2269FF747583D09E3FADDACA50FDA27D94BC43A6AB` |
| `docs/routeb-p8-next-concrete-child.md` | `9EF74058FB6711946A253A9DED55EB6CE91DDA01059A78999B413FF98E57AB0E` |
| `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` | `DC4BF1C7C0B1EE428EE3BF146E90801E08A2199FB931789699FE8073A82AB7F9` |
| `examples/routeb_p8_contract_adapter/verify.sh` | `DE46F7E19C186348FA6FEE88CD7E211B1B0F3D2759EF1FE8FD1C50EC37644917` |
| `examples/routeb_p8_rhs_payload_generator/receipt.template.json` | `545E99CB45B95D804962F70A3B5EC4A44F88BD9F4D6649976A986512B453A207` |

## Compatibility result

The deployed source contract is not compatible with the existing 14-state
ramp parent. The audited source has state order `q[1:6], dq[1:6], w`,
`julia_state_dimension=13`, and writes `du[13]=0`. It has no `c` input or
`du[13]=c`. The parent instead requires, for every 14-state `z`,

```text
F z wSlot = z cSlot
F z cSlot = 0
```

The natural zero-tail lift therefore fails on the legal state with all
coordinates zero except `c=1`: `FullX0` permits this state, while the lifted
source gives `F z wSlot=0` and the parent requires `1`. This is a semantic
incompatibility, not a missing endpoint entry.

## Exact commands and results

The focused command prescribed by the adapter was:

```text
bash examples/routeb_p8_contract_adapter/verify.sh
```

The existing focused receipt/report for this adapter records:

```text
P8_CONTRACT_ADAPTER_COMPILE=PASSED
SOURCE_RESTRICTION_CHECK=PASSED
TRUE_DH_BINDING=OPEN
exit code: 0
```

This result is a Lean compilation of the adapter and parent scaffold only.
It does not compile or bind the Julia RHS, does not establish interval
containment, and does not establish an ODE flowpipe. The local re-invocation
was not used as stronger evidence because the shell invocation did not return
a terminal result within the bounded command window.

The receipt template remains `receipt_status=pending_endpoint_payload`, with
all 12 dynamic endpoint intervals null, `w=[0,0]` justified only by the source
literal, and `c` marked as an unconsumed sidecar. Its top-level fields also
keep `LEAN_VERIFIED=false`, `formal_admission=not_theorem`, and
`ramp_binding=OPEN`.

## Classification

- **Conditional:** `timeLift_rampPremise` proves the parent ramp shape for an
  abstract time-indexed 13-state field `G`; this is an interface scaffold,
  not source binding.
- **Closed negative fact:** `zeroTailLift_not_ramp` proves that the literal
  zero-tail lift cannot satisfy the ramp premise.
- **Open:** exact source-to-`G` semantic binding for the first 12 components,
  including DH/FD/regularization/linear-solve semantics; a coherent choice of
  13-state explicit-time or genuine 14-state deployed RHS; outward interval
  enclosure; solution existence; local flowpipe; partition continuation and
  `[0,1]` coverage.
- **Blocked for the current contract:** instantiation of the 14-state ramp
  parent from the currently deployed 13-state source. The block is removable
  only by changing the source contract or selecting a formally defined
  explicit-time 13-state parent; no endpoint payload can remove it.

No state, registry, receipt, external source, or admission flag was modified.
`formal_certificate_allowed` must remain `false` and no registry promotion is
eligible.

## Shortest verifiable deployment route

The shortest route is to make the semantic contract choice first:

1. **S1 — source contract binding:** choose either (a) a real 14-state RHS
   with `w'=c, c'=0`, or (b) an explicit-time 13-state RHS `F13(t)` and prove
   `w(t)=c*t` in a new 13-state parent. Record source hashes, coordinate map,
   Float64/FD/solve semantics, and an exact-real adapter contract.
2. **S2 — contract theorem:** prove the selected ramp/time adapter and its
   equality to the deployed first 12 RHS components. The existing
   `timeLift_rampPremise` can be reused only after this binding premise is
   discharged.
3. **S3 — outward RHS containment:** for every certified cell and every point
   in that cell, prove outward-rounded lower/upper bounds for all selected
   RHS coordinates; replace the current null endpoint receipt.
4. **S4 — local flowpipe:** prove Picard image existence and the local tube
   invariant, then S5 partition compatibility/continuation through `T=1`.
5. **S6 — true-DH flowpipe theorem:** only after S1–S5 may the flowpipe result
   feed the existing first-exit/terminal assembly.

Next theorem: **`P8_SOURCE_CONTRACT_BINDING_13_OR_14`** (with the immediate
contract child **`P8_RAMP_BINDING`**). It must be a source-semantic theorem,
not a longer rollout or a filled-in endpoint payload.

