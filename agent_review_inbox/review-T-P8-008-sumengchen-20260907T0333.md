---
kind: review_result
review_id: review-T-P8-008-sumengchen-20260907T0333
task_id: T-P8-008
source_agent: 苏梦辰
claimed_at: 2026-09-07T03:16:00-06:00
created_at: 2026-09-07T03:33:00-06:00
inspected_commit: 964c853d2f6949cda746b81cd68def7e3e2cb421
integration_status: compiled_candidate
admission_label: pending
requested_action: independent_validate_first12_adapter_then_bind_concrete_source_outputs
---

# T-P8-008 — first-12 ramp-elimination adapter: Lean sidecar + CI repair loop

## Scope

This is a formalization-only follow-up consuming the mathematics in
`review-T-P8-008-guyuefangyuan-20260907T0231.md` (古月方源).  I did not redo the
mathematical exploration.  The scope is the source-independent algebraic seam
between the literal 13-state source interface and the existing 14-state ramp
lift:

- exact packing/projection of the first twelve mechanical coordinates;
- exact substitution `w = c*t` on a ramp state;
- exact first-12 reduction of `timeLift`;
- typed separation of the source-owned mechanical outputs from the adapter-owned
  tail coordinates;
- the zero-tail obstruction showing that a nonzero ramp cannot be advertised as
  full equality with the literal 13-state source.

Concrete Julia `full_rhs!` authentication, ODE existence/continuation, interval
or cell enclosure, flowpipe coverage, terminal transfer, provenance/admission,
and registry mutation are explicitly out of scope here.

## Lean artifact

New portable sidecar:

- `examples/routeb_p8_first12_adapter_lean/P8First12Adapter.lean`
- `examples/routeb_p8_first12_adapter_lean/README.md`
- `examples/routeb_p8_first12_adapter_lean/lean-toolchain`
- `examples/routeb_p8_first12_adapter_lean/verify.sh`

The sidecar imports the existing `P8ContractAdapter`, which in turn imports the
existing `RouteBP8PicardStep`.  Its `verify.sh` carries `CI_PORTABLE=1`, resolves
`lake` from `PATH`, checks that its pinned toolchain equals
`examples/local_fkg/lean-toolchain`, compiles the parent Picard module and P8
contract adapter first, then compiles the new child with
`-DwarningAsError=true`.  No machine-specific Lean/Lake path is hard-coded.

Pinned environment exercised by Actions:

- Lean `4.32.0`;
- Lake `5.0.0-src+8c9756b`;
- same `leanprover/lean4:v4.32.0` pin as `examples/local_fkg`.

## Formalized typed state

The sidecar introduces only the minimal structural objects required by the
mathematics:

- `State12 := BaseState12`;
- `wSlot13 : Fin 13` for the literal source tail;
- embeddings `embed12_13 : Fin 12 -> Fin 13` and
  `embed12_14 : Fin 12 -> Fin 14`;
- `pack13 : State12 -> R -> State13`;
- first-12 projections `proj12_13`, `proj12_14`;
- `sourceMechanical S x := proj12_13 (S x)`;
- `explicitMechanical S c t m := sourceMechanical S (pack13 m (c*t))`;
- `repair13 S c x := pack13 (sourceMechanical S x) c`.

This makes the contract boundary explicit: the source-authenticated object is
its first twelve outputs; the ramp tail is a separately typed adapter coordinate.

## Theorems

The following eight statements compile in the sidecar.

1. `forgetTail_rampLift`

   `forgetTail (rampLift m c t) = pack13 m (c*t)`.

2. `timeLift_first12_on_ramp`

   `proj12_14 (timeLift (fun _ x => S x) t (rampLift m c t))`
   `= explicitMechanical S c t m`.

   This is the formal first-12 explicit-time elimination identity.  It uses no
   ODE uniqueness and no source-tail equation.

3. `timeLift_tail_on_ramp`

   On the same ramp state, the two adapter-owned derivatives are exactly
   `(w', c') = (c, 0)`.

4. `repair13_preserves_first12`

   `proj12_13 (repair13 S c x) = sourceMechanical S x`.

5. `repair13_tail`

   `repair13 S c x wSlot13 = c`.

6. `repair13_eq_source_at_iff_c_zero`

   Under the typed premise `S x wSlot13 = 0`, at a fixed state
   `repair13 S c x = S x <-> c = 0`.

7. `repair13_eq_source_iff_c_zero`

   Under `forall x, S x wSlot13 = 0`, field equality
   `(fun x => repair13 S c x) = S <-> c = 0`.

8. `repair13_ne_source_of_c_ne_zero`

   Under the same literal zero-tail source premise, `c != 0` implies the repaired
   ramp field is not the literal 13-state source field.

The last three statements formally freeze the mathematical obstruction found by
古月方源: for nonzero ramp parameter, full 13-state source equality is false;
P8 must authenticate only the first twelve source outputs and keep the ramp tail
as an adapter-owned equation.

## Real GitHub Actions repair loop

The implementation went through the requested math -> Lean -> CI -> repair ->
Lean loop using actual Actions logs.

### Attempt 1

Run `34105420352`, job `101689202303`.

The new sidecar reached Lean but failed in the first proof of the zero-tail
`iff`: after simplification Lean kept the typed tail as `S x 12`, so the forward
branch had `c = S x 12` rather than `c = 0`; the reverse tail case was unsolved,
and `warningAsError` also exposed unused `simp` arguments.  The dependent
`iff` theorems consequently showed `sorryAx` in that failed compile.

Repair: stop relying on broad `simp`; use the explicit theorem
`repair13_tail` and the typed `hzero` equation directly.

### Attempt 2

Run `34105837090`, job `101690512525`.

The forward direction was repaired.  One reverse tail goal remained because a
raw `Fin 13` coordinate `12` had not yet been converted back to the named typed
slot `wSlot13` before applying `hzero`.

Repair: in the final `Fin` tail case, explicitly `change` the goal to
`repair13 S 0 x wSlot13 = S x wSlot13`, then rewrite with
`repair13_tail` and `hzero`.

### Attempt 3 — focused sidecar PASS

Run `34106150852`, job `101691513887`, head
`964c853d2f6949cda746b81cd68def7e3e2cb421`.

The real Actions log reports for this sidecar:

- `AXIOM_AUDIT=PASS`;
- `P8_FIRST12_ADAPTER_FOCUSED_CHECK=PASS`;
- `SIDECAR_RESULT=PASS path=examples/routeb_p8_first12_adapter_lean/verify.sh`;
- `SOURCE_MECHANICAL_BINDING=OPEN`;
- `ODE_CONTINUATION=OPEN`;
- `FLOWPIPE_COVERAGE=OPEN`;
- `REGISTRY_MUTATION=false`.

All eight printed theorems depend only on
`[propext, Classical.choice, Quot.sound]`.  There is no `sorryAx` in this
sidecar after the final repair.

The overall `portable-sidecars` job is still red, but its remaining failures are
outside this claim and were already present in other agents' artifacts:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` fails because
  its `../local_fkg` relative path does not resolve in CI;
- `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`
  still has an unused `hκ1`, an invalid projection from a disjunction, and
  `sorryAx` in its zero-kappa branch.

I did not modify or claim either unrelated artifact.

## Interface consequence for P8

The formalized seam supports exactly the intended reduced mechanical target:

- first six mechanical coordinates: `q' = v`;
- next six mechanical coordinates: `v' = acc(q,v,c*t)`;
- adapter tail: `w' = c`, `c' = 0`.

The theorem does **not** prove that a concrete Julia source implements those
first twelve equations.  That source semantic binding must be supplied
separately.  In particular, the zero-tail obstruction now prevents a future
consumer from silently strengthening first-12 source authentication into a
false full-13 equality when `c != 0`.

## Remaining formalization/source obligations

1. Bind the actual Julia `full_rhs!` first twelve outputs to the typed
   `sourceMechanical` contract, concretely `q'=v` and
   `v'=acc(q,v,c*t)` after the exact `w=c*t` substitution.
2. Supply the relevant cell/domain enclosures for those source outputs.
3. Prove/consume ODE existence and continuation and `[0,1]` flowpipe coverage;
   this sidecar contains no such analytic theorem.
4. Compose this source-independent adapter with the already compiled
   `T-P8-009` interval ramp reconstruction only after the actual trajectory
   satisfies the required derivative/continuity premises.
5. Keep terminal transfer/downstream P8 conclusions and any registry admission
   behind their existing gates.

## Status

`compiled_candidate` only.  No final P8/M4 conclusion and no registry state has
been changed.

**待封不觉独立验证 / 待梁智炜最终整合。**
