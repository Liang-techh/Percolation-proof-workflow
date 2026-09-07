# Compiled storage leaves to barrier ledger: field audit

Sidecar status: **OPEN_UNCOMPILED**. Existing compilation receipts were
inspected read-only; Lean/Lake and broad regression were not run. Only this
new sidecar and review were written. No state/registry admission occurred.

## Receipt evidence actually found

Both current source files match their successful-run snapshots and the
source hashes documented by their receipts. The retained compiled-object
hashes also match. This is a fresh read-only check of existing evidence,
not a fresh compilation or a revalidation of the entire compiler environment.

| Leaf | Existing successful receipt | Current/snapshot source SHA-256 | Retained object SHA-256 |
| --- | --- | --- | --- |
| `examples/routeb_actual_energy_storage_lean/ActualStorage.lean` | `output/run-ZWEIdfZ8/terminal.log:41-45`: compile exit 0, snapshots unchanged, verifier exit 0; completed 2026-09-05T21:11:05Z | `c20c900ca09039dc7c37c247d071c058a58dd7ca419a4865f2c1f7f29f6a01aa` | `7b3f8836286e56b7b306faf5bca26338752a16b1c271a2b6eb51a524bd05ae97` |
| `examples/routeb_shifted_storage/ActualShift.lean` | `output/actual-GqBg6J4g/verify.log:23-25`: compile exit 0, verifier exit 0; run started 2026-09-05T17:56:47Z | `d60976ce10dc670fd93dad045c5d97fc426ae6c69036de8a3266e16e26c96579` | `2e28e4c2b1d6834c70a314ca2545e51d6c5c8e2127739906a584131e9ae81f0c` |

Both logs record Lean 4.33.1 and Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. The seven printed final
ActualStorage theorems and eight ActualShift theorems list only
`propext, Classical.choice, Quot.sound`. Receipt claims about compilation
are supported by the inspected logs; their external-model premises remain
premises. `ReferenceMass.lean` currently has hash
`b77e00ab3cf236edc143fa963aba362a8279f2ca6caecaf5277726fac0c91607`,
matching the reuse receipt. Transitive artifacts were not rebuilt.

## Exact field-by-field binding table

Here **receipt** means the indicated conditional or encoded-model theorem
has existing compilation evidence; it does not mean its hypotheses have
been instantiated for the ledger. **Missing** describes a transfer not
provided by the inspected leaves/ledger, not a search claim about every
artifact in the repository.

| Field | ActualStorage theorem/definition | ActualShift theorem/definition | Barrier ledger | Binding status |
| --- | --- | --- | --- | --- |
| Storage value | `storageV = f*W0 + sum p_i*q_i² + h*c²`, with `W0 = kinetic M v + U-Uzero-kinetic H q + (7/75)q4²` | `W=potential(q)-potential(0)+proportionalEnergy(q)`; `actual_W_eq_storage` binds this encoded W to the 17-row Fourier storage | Labels `V` as full physical energy; does not provide a typed evaluator | Receipt for each local expression; **missing** identity to ledger V and between the two families |
| Time dependence | `synthesisV` uses coefficient polynomials in `(1-t)^j`, `j>=1` | W and its fixed shift are state functions | `horizon=1`; no coefficient family selected | **Missing** f,p,h or F,P,C selection and time-dependent identity |
| Terminal value | `synthesisV_terminal`: value at t=1 is zero for every state | No terminal-energy tube theorem | Terminal block target is `p_B<=45` | Receipt does not identify zero synthesis storage with physical terminal output |
| Potential origin / shift | `W0_source_energy` assumes H=H0, U=referencePotential(q), Uzero=3108789/400000 | `actual_shift_exact`: B=4079979/400000; constant row 8 removed exactly | No explicit shift field identifying V with W, E, or E+B | Receipt for encoded B; physical potential and ledger normalization bindings remain missing |
| `V0` meaning | Initial theorem gives `(9/400)*beta+3*f/10000+3*h`; W0 specialization gives `231/20000` | No initial-set upper-bound theorem in ActualShift | `initial_storage_upper=492033745203/25600000000000` | V0 is an **upper bound over X0**, not potential Uzero or V at the zero state. Need coefficient/budget and same-storage bindings |
| Initial set X0 | Full six-q plus six-v ball `normSq q+normSq v<=9/400`; separate `c²<=3` | None used for global configuration coercivity | `block_only_q4_q5_dq4_dq5`, remote coordinates fixed zero | Block-only set embeds into the full ball after the explicit coordinate map; that inclusion does not prove the gap premise or identify V |
| Initial gap | `storageV_initial_upper` assumes `actualSignedGap>=-3/10000` on each evaluated state | No gap theorem | No typed gap field | Receipt proves implication; actual entire-X0 gap bound remains an external premise |
| Initial coefficient conditions | f,h>=0; beta>=f/2 and beta>=p_i+(7f/75)indicator(i=4) | Imported Kp is exactly encoded, each >=2/5 | No f,p,h,beta fields | **Missing** concrete selection. p_i>=0 is not needed by the initial-upper theorem, but is needed for its positivity theorem |
| `V_BAR` | No built-in threshold 1 in storage definition | Coercivity applies to E+B | Script sets V_BAR=1; CSV stores `energy_candidate_domain=V<=1` | Must bind the same value and normalization. A constant shift requires corresponding threshold/initial-budget change |
| Positivity domain | `PDomain={0<=t<=1 and q4²<=56/15}` plus mass PSD and source equalities | `actual_W_shifted_coercivity` is global for encoded W+B | Energy sublevel V<=1, component cap 5/2 | **Missing** domain implication for ActualStorage. `(5/2)²=25/4>56/15`, so that component cap alone is insufficient |
| Mass | Actual M(q) PSD is a hypothesis; compiled M0<=I is a different statement | `actual_p45_bound` assumes mass lower bound `(9401/1000000)*sum v_i²<=v'Mv` | `mass_lower_regularized=9401/1000000` | Matching number is not a typed proof for the same matrix on the same domain |
| Block observable | Family terminal zero is not p45 | Exact `p45=(3/2)(q4²+q5²)+(4/5)(v4²+v5²)`; `p45<=(1600000/9401)*(E+B)` under mass and E identity | Same block weights; different global-PMI comparison coefficient | Observable weights match; **missing** energy/mass binding. ActualShift does not justify deleting B or replacing its comparison coefficient |
| Tube budget | No dissipation/integration result in this leaf | No energy tube | `energy_tube_upper=V0+gamma_effective+gravity_additive_defect`; scalar margin recorded positive | Need the integrated inequality for this exact storage and path; arithmetic alone is insufficient |
| Path / ODE | q,v,c are pointwise inputs; no path or source ODE in ActualStorage | q,v,M,E are pointwise inputs; no path | No typed path, solution, initial-membership or flow theorem field | **Missing** path(0) in X0, source RHS/kinematics, c'=0/ramp relation, domain/continuation and integrated bound |
| Circle lift | Not part of ActualStorage.PDomain | Trigonometric phases are real functions of q | CSV does not encode circles; companion source-to-flow document uses V<=1 plus active circles | Need the lift map and invariance for a lifted flow. Circle constraints do not supply the energy identity or path |
| Closure flags | Receipt explicitly excludes physical source, flow and coefficient feasibility | Receipt explicitly excludes physical potential, mass and tube instantiation | `descriptor_flowpipe_closed=False`, `fd_remainder_semantics_closed=False`, `formal_certificate_allowed=False` | No existing leaf or sidecar changes those flags |

The ledger inspected was
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block_energy_barrier_audit.csv`,
SHA-256 `b10f0118c3dd3e6708084421baf38624977e6b18cd77dbb93e11f5a7f183f875`.
Its provenance script sets the threshold and reads the initial scalar from
the targeted-storage comparison, as recorded in the prior origin review.

## Minimal sidecar and what it actually supplies

`StorageData` explicitly fixes the time coefficients, H, M(q), U(q) and
Uzero. `actualAt` calls the existing `storageV` definition. No free function
is relabeled as that definition without an equality.

`ActualInitialPremises` copies exactly the needed hypotheses of
`storageV_initial_upper`. `existing_initial_theorem_instance_attempt`
applies that existing theorem; it is not a new initial-gap proof.
`InitialLedgerBinding` then requires just the identity on X0 at time zero,
the initial premises there, and a scalar bound from the theorem's formula
to recorded V0. The resulting initial ledger upper bound is conditional.
The full-ball hypothesis may be used on the block-only subset once the
coordinate/ramp/gap obligations are supplied.

`PathLedgerBinding` separately requires storage identity on the comparison
domain, path membership, the actualAt tube inequality, and tube<1. Its
consumer transfers that already supplied tube to the ledger expression.
The record **does not derive the source tube or path-domain membership**.
Those are the missing dynamic/continuation obligations, not conclusions
smuggled in by the scalar ledger. To link it with the initial record one
also needs path(0) in the same X0; neither record alone claims this linkage.

`existing_shifted_comparison_instance_attempt` invokes the existing
`actual_p45_bound` with the explicit expression
`encodedShiftedEnergy=kinetic M v+W(q)+4079979/400000` and the unchanged
mass hypothesis. It offers a separate comparison adapter, not an equality
between this expression and `actualAt` or ledger V.

Three rational checks clarify the remaining work:

- `231/20000 <= ledgerV0`: W0's initial numerical bound can fit, but only
  after its ball/gap hypotheses and the ledger-storage identity are proved.
- `(5/2)^2 > 56/15`: the recorded component cap does not establish the
  positivity domain needed by ActualStorage.
- `(1600000/9401)*(4079979/400000) > 45`: inserting the shift into this
  generic block comparison already gives a baseline above the target.
  This only shows that bound is insufficient with a nonnegative unshifted
  cap; it does not prove that the actual output exceeds 45 or refute a
  sharper, correctly bound global-PMI estimate.

## Validation and final boundary

Read-only checks covered source/snapshot/object hashes, exit-code log lines,
printed axiom reports, theorem signatures, and the ledger fields above.
No dependency cache was rebuilt and no compiled receipt was created for
the sidecar. The sidecar has 114 lines and no proof-hole declarations.
SHA-256: `0de2680d048c620a05fd2e02402b24c333a63e9c768c3193c819e09e48eaeb9b`.

Final status: **OPEN_UNCOMPILED** for the new sidecar. The two old theorem
receipts are real, source-matching evidence; the current same-storage,
initial-premise and source-to-path instantiations remain open. No full
Route-B certificate or BODY6/full-system identification is asserted.
