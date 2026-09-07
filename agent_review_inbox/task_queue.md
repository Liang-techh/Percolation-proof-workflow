# Parallel agent task queue

`kind: task_plan` — this file is planning input, not proof and not a registry
entry. Agents should claim one task by adding their name and timestamp, then
write the result as a new `review_result` file in this same directory. Keep
tasks disjoint and do not edit the authoritative checkpoint or external source
without an explicit scoped request.

## Historical roundtable assignments

These assignments use the user-provided periodic worker pool. They are
independent bounded tasks; a worker must inspect this queue and the board before
claiming, then leave the authoritative result in a new inbox review.

| worker label | task | boundary |
|---|---|---|
| 封不觉 | `T-P3-007` | one concrete mass/DH entry bridge |
| 柳冠一 | `T-P4-005` | one-channel residual source binding |
| 占月方源 | `T-P8-005` | terminal-transfer interface |
| 星宿仙尊 | `T-M4-002` | block-(4,5) dependency cone |
| 苏梦辰 | `T-P0-002` | fresh receipt/provenance re-audit |
| 红莲魔尊 | `T-P7-001` | fallback tail obligation audit |
| 奥尼洛 | `T-DAG-003` | shared-lemma/DAG projection |
| 狂弓魔尊 | `T-REPAIR-001` | Lean/checker repair-loop audit |

Assignment does not imply proof progress or ownership of a theorem. A result
may be `pending`, `rejected`, or `architecture_only`; only the normal
verification and registry gates can change admission state.

For future GitHub task releases, use the current pool and role matrix in
`agent_roster.md`. Do not dispatch to labels removed from that pool. The
assignments in this section are preserved as historical coordination state;
the correction does not rewrite existing claims or review authorship.

## Current release-routing snapshot

This snapshot supersedes the historical table above for new work released
after the user's latest six-agent ring plus the 流川枫 proportional lane:

| worker label | slot | current bounded focus |
|---|---:|---|
| 柳冠一 | :00 | 数学证明：adapter 背后的实质数学与主路线瓶颈 |
| 苏梦辰 | :10 | Lean theorem decomposition、pinned 编译与 repair |
| 古月方源 | :20 | 数学证明：主路线探索与数学瓶颈 |
| 狂蛮魔尊 | :30 | 数学证明：不等式 closure、强攻难点与反例辅助 |
| 巨阳仙尊 | :40 | Lean 编译修复、typed interface 与 sidecar |
| 红莲魔尊 | :50 | 数学证明：能量法、Lyapunov 与非线性恒等式 |
| 流川枫 | batch share | 约三分之一 GitHub 批次；按任务承接数学或 Lean 独立工作 |

## Dispatch and synchronization throttle

The coordinator may integrate inbox results locally on the hourly harvest
cycle. At that same harvest/release point, it may fetch, merge, and push the
integrated batch once; outside that window, do not routinely sync to GitHub
unless there is a major mathematical breakthrough, a verified architecture
milestone, or an explicit user request, to avoid competing with scheduled
GitHub agents for the push channel.

## Next GitHub Lean validation batch

These are task plans, not proof receipts. They are reserved for the next
available `:10`/`:40` Lean slots and must return immutable review results with
exact commit, pinned toolchain, exit code, theorem names, `#print axioms`, and
placeholder scan. A green compile remains candidate evidence until independent
integration gates are satisfied.

| task | Lean owner | target | boundary |
|---|---|---|---|
| `GH-LEAN-P4-032-weighted-three-term` | 苏梦辰 | `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_WeightedThreeTerm.lean` | compile/repair only; preserve force-vs-accel types and do not claim source/coverage |
| `GH-LEAN-P4-032-relative-additive` | 巨阳仙尊 | `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_RelativeAdditive.lean` | compile/repair only; verify `rho_eff/B_eff` statements and no sqrt/source admission |
| `GH-LEAN-fixed-lambda-reserve` | 苏梦辰 | `examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_RESERVE_FINAL_BRIDGE20260907.lean` | compile/repair only; explicit shared-lambda/total equalities must remain |
| `GH-LEAN-body6-tail-minors` | 巨阳仙尊 | `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_TAILMINORS20260907.lean` | compile/repair only; tail subblock only, no full-body PSD/eigenvalue claim |
| `GH-MIXED-flowchuanfeng-schur-absorption` | 流川枫 | `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption.lean` | one proportional batch share; may compile/repair or inspect theorem boundary, never promote registry |

### 2026-09-07 — 14:24 流川枫扩展 lane

- 新增 GitHub agent 流川枫；后续每批约三分之一任务按 round-robin 分配给他，
  不另造固定分钟槽。
- 已将 P4 Schur/PMI absorption 作为其首个混合验证任务；数学与 Lean receipt
  仍必须保持分层，不能直接改变 registry。

### T-P4-012 — typed remote-action repair contract

- status: `open` (local contract scaffold added 2026-09-07)
- owner: `巨阳仙尊` for pinned Lean/statement probe; `大爱仙尊` or
  `幽魂魔尊` for source-side inequality binding when available;
- scope: consume `src/percolation_workflow/routeb_remote_contract.py` and
  bind one of the two admissible repairs for `M_BD(q)a_D`: `full_state` or
  `d_row_schur`;
- deliver: exact source/interval/Lean evidence for every named premise and a
  typed adapter to the P4 residual node.  The local conditional candidate
  `‖a_D‖² <= 90*mass` in `routeb_remote_accel_budget.py` may be consumed only
  after its full-state mass/source binding is proved;
- forbidden: block-only remote bounds, arbitrary physical reachability claims,
  or treating the structural contract as registry/formal admission.

### T-P4-013 — remote budget to scalar PMI composition

- status: `open` (isolated Lean seam added 2026-09-07)
- owner: `巨阳仙尊`
- source: `examples/routeb_remote_pmi_composition/RemotePMIComposition.lean`;
- scope: compile the two source-independent composition theorems and inspect
  exact statements, pinned toolchain, and `#print axioms`;
- deliver: immutable review with Lean exit code, theorem names, source/blob
  hashes, and a specialization note for `kappa`/`beta`;
- forbidden: treating the composition as a proof of `M_BD`, mass/source
  equality, coverage, or P4/M4 closure.

### T-P4-014 — vector remote action to PMI composition

- status: `open` (isolated Lean seam added 2026-09-07)
- owner: `巨阳仙尊`
- source: `examples/routeb_remote_vector_pmi/RemoteVectorPMI.lean`;
- scope: compile the division-free two-dimensional theorem (including its
  sharp iff form) that consumes one
  squared-norm remote bound `‖r_B‖² <= K*mass`, an explicit `0 <= K`, one scale
  bridge, and `K*beta² <= p*d`;
- deliver: immutable Lean review with exact theorem statements, axioms,
  pinned toolchain, and source/blob hashes;
- forbidden: splitting or recharging the vector operator bound per component,
  or claiming `M_BD` source binding, coverage, or P4/M4 closure.

### T-P4-015 — nominal distal descriptor bridge

- status: `open` (local exact-artifact contract added 2026-09-07)
- owner: `大爱仙尊` for source-side polynomial/interval binding; `巨阳仙尊`
  for the pinned Lean adapter;
- source: target `routeB_dense_Mq/routeB_compact_dh_nominal_distal_bridge_audit.csv`,
  `routeB_compact_nominal_descriptor_interface.csv`, and local
  `routeb_nominal_distal_contract.py`;
- scope: bind `a_D = S*y + r_hat*z/rho`, the reduced descriptor equation, and
  the retained `M_BD*S*y` port without inverse substitution or double-counting;
- deliver: exact source/interval/Lean evidence for the rational direction,
  `rho`, retained polynomial, and full `M0_BB` tail PMI;
- forbidden: replacing the retained port with a coarse `||a_D||` bound,
  treating the artifact shape as proof, or claiming global coverage.

### T-P4-016 — exact nominal-distal tail PMI positivity

- status: `open` (independent leaf split 2026-09-07)
- owner: `大爱仙尊` for exact rational/SOS tail positivity; `巨阳仙尊`
  for the pinned Lean scalar/3x3 adapter;
- source: `routeB_physical_rational_tail_pmi_scalar.csv`, its metadata,
  the complete `M0_BB` bridge metadata, and the local tail contract;
- scope: prove the square-root-free 3x3 PMI using the full off-diagonal
  `M0_BB`, or produce a precise obstruction that selects the next route;
- deliver: exact polynomial identity, circle/domain multipliers or Lean proof,
  and a receipt that distinguishes candidate Gram data from kernel verification;
- forbidden: two independent component gains, floating PSD, sampled positivity,
  or any claim of global coverage / residual / flowpipe closure.

### T-P4-017 — exact target-minus-opt Gram reconstruction

- status: `open` (separated from PMI positivity 2026-09-07)
- owner: `大爱仙尊` for exact rational expansion and residual bound;
  `巨阳仙尊` for the Lean representation/receipt adapter;
- source: rational Gram payload plus local monomial basis, scalar PMI target,
  and the recorded lower-bound candidate;
- scope: reconstruct `p_scaled - opt` exactly modulo the 12 box generators
  and three circle identities, then prove the rational residual bound and
  positive margin;
- deliver: exact `opt` provenance, expansion identity, all Gram PSD evidence,
  and a fail-closed receipt separating rational candidate from kernel proof;
- forbidden: inferring target equality from positive Gram blocks alone, using
  a decimal `opt` without exact provenance, or claiming Route-B closure.
- local progress: `check_routeb_tail_gram_reconstruction.py` now independently
  expands the rational payload and reports a positive candidate margin; the
  exact solver `opt` provenance and pinned Lean receipt remain open. The
  checker also records the solver-vs-derived constant gap; Lean adapters must
  consume the derived safe lower bound, never the raw `OPTIMAL` decimal. The
  current residual has 511 nonzero canonical coefficients with digest
  `95042f6ea7c9989174d6045383138099686c2383649b3358611a63f374bcf7cf`;
  this is a binding witness, not kernel evidence.

### T-P4-018 — reusable residual `l1` Lean seam

- status: `new` (local kernel-seam preparation)
- owner: `巨阳仙尊` for pinned Lean compilation and axiom receipt;
  `大爱仙尊` for matching the coefficient-residual contract to the exact
  Gram expansion;
- source: `examples/routeb_gram_residual_lean/GramResidual.lean`;
- scope: compile `weighted_residual_l1_bound` and
  `decomposition_nonnegative_of_abs_residual`, then bind the concrete
  T-P4-017 residual receipt without importing solver status as evidence;
- deliver: Lean compile receipt, `#print axioms`, and explicit source/hash
  binding for the concrete coefficient list;
- receipt contract: `routeb.residual_l1_lean_receipt.v1`, audited by
  `audit_routeb_residual_l1_lean_receipt`.  The handoff must include the
  pinned source/artifact hashes, both theorem names, zero `sorry`/`admit`,
  exit code `0`, coefficient term count, `residual_l1`, safe rational lower
  bound, and positive scaled margin.  Missing coordinator-owned pins remain
  `PENDING`; mismatches are `REJECTED`. The receipt must also carry
  `residual_coefficients_sha256` equal to the canonical 511-term digest
  emitted by the current reconstruction checker.
- forbidden: treating the generic seam as proof of the giant CSV identity,
  true-DH semantics, domain coverage, or Route-B closure.

## Queue: Route-B current bottlenecks

### T-P3-001 — single-entry true-DH source bridge

- status: `reviewed` (Codex, 2026-09-06T00:00:00-06:00; result: `review-T-P3-001-p3-audit.md`)
- scope: one fixed rational q-box and one `M[i,j]` entry;
- inspect: `docs/routeb-p3-next-concrete-child.md`,
  `examples/routeb_p3_mass_entry_bridge_lean/`;
- deliver: exact source/interval contract, source hashes, and focused Lean or
  checker result; distinguish conditional Float64 trace premises from proved
  Julia/DH equality;
- forbidden: more sampling, full branch-and-bound, registry promotion.

### T-P4-001 — residual source binding

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as pending)
- scope: one P4 residual/Schur channel and its exported decimal or rational
  witness;
- inspect: `examples/routeb_p4_next_child/`,
  `examples/routeb_p4_decimal_source_binding_audit/`, and the C2
  force/acceleration audit;
- deliver: exact algebraic child or a precise source-binding obstruction with
  receipt fields and exit code;
- forbidden: treating decimal reification or solver output as true-DH proof.

### T-P8-001 — 13-state/14-state reachability contract

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as pending)
- scope: bind the deployed RHS to either the existing 14-state ramp parent or a
  formally defined explicit-time 13-state parent;
- inspect: `docs/routeb-p8-flowpipe-binding-next.md`,
  `docs/routeb-p8-next-concrete-child.md`, and
  `examples/routeb_p8_contract_adapter/`;
- deliver: contract compatibility result and smallest next theorem;
- forbidden: claiming flowpipe coverage from endpoint payloads or a conditional
  adapter.

### T-WF-001 — registry/admission boundary audit

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as documentation-only)
- claimed_by: `Codex`
- claimed_at: `2026-09-06T20:20:00-06:00`
- scope: read-only audit of any proposed `review_result` against
  `model.py`, `registry.py`, `comparator.py`, and the current Route-B state;
- deliver: whether integration is documentation-only, DAG metadata, pending,
  rejected, or eligible for an existing explicit gate;
- forbidden: changing status or registry directly.

## Queue: next smallest leaves

### T-P3-002 — fixed-point IEEE trace witness

- status: `open`
- scope: one fixed q-box and one `M[i,j]`, preferably at a deterministic
  source point such as `q=0`;
- deliver: a replayable Float64 operation/rounding witness or a precise reason
  it cannot be produced with the current runtime; write only a review result;
- forbidden: infer global interval soundness from one point or from equal bits.

### T-P4-002 — one-channel true-DH residual envelope

- status: `open`
- scope: consume the exact Schur leaf for one channel and identify the smallest
  executable source-binding witness for `d`, `p`, and the actual residual;
- deliver: checker/Lean boundary, normalization map, and receipt contract;
- forbidden: using the decimal audit as DH equality or closing P4 globally.

### T-P8-002 — explicit-time 13-state parent option

- status: `open`
- scope: compare a new explicit-time 13-state parent with the existing
  14-state ramp parent, including initial-domain and terminal statement changes;
- deliver: a decision memo and minimal theorem signature, with no source edits;
- forbidden: silently changing the target theorem or claiming flowpipe coverage.

### T-M4-001 — dependency-cone closure audit

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as pending)
- scope: use the current checkpoint and DAG projection to list the exact M4
  prerequisite cone and identify which leaves can be proven independently;
- deliver: review result with deterministic node IDs, levels, and next frontier;
- forbidden: status promotion, deletion of failed history, or broad regression.

### T-P0-001 — reproducibility baseline re-audit

- status: `reviewed_pending` (integrated at Route-B revision 333; result:
  `review-T-P0-001-repro.md`)
- scope: existing P0 attempts, receipts, source hashes, and the smallest
  reproducibility checker only;
- deliver: whether P0 can enter `evidence_complete`, with missing gates and
  exact evidence paths;
- forbidden: broad reruns, status promotion, or registry mutation.

### T-P0-002 — fresh receipt/provenance re-audit

- status: `reviewed_pending` (integrated at Route-B revision 350; current
  snapshot has no stable fresh receipt/output-hash binding)
- scope: compare the historical P0 receipt against the current canonical
  `state.json` revision, Git/source snapshot, receipt path and output hashes;
  keep workflow-node completion separate from fresh provenance verification;
- deliver: exact current revision and hash evidence, a deterministic receipt
  alias/index proposal, and all unresolved freshness blockers;
- forbidden: deriving a receipt hash from a Git blob hash, reusing an old
  receipt as current evidence, status promotion, or registry mutation.

### T-DAG-002 — explicit child-DAG refinement

- status: `reviewed_pending` (integrated at Route-B revision 333; result:
  `review-T-DAG-002-child-dag.md`)
- scope: propose disjoint P3/P4/P5/P6/P8/M4 source-binding, algebra,
  coverage, and terminal-transfer child nodes;
- deliver: deterministic node names/dependencies, admission boundaries, and
  migration risks;
- forbidden: mutating the authoritative checkpoint or silently changing the
  theorem statement.

### T-DAG-003 — shared-lemma/DAG projection

- status: `reviewed_pending` (integrated at Route-B revision 351; architecture
  only; no authoritative graph migration)
- scope: project shared source-manifest, true-DH semantic, and domain-partition
  contracts separately from P3/P4/P5/P8 quantity-specific children; remove
  scheduling-only edges between independent abstract lemmas;
- deliver: deterministic shared-node projection, cross-branch dependencies,
  migration risks, and any proposal-schema requirements;
- forbidden: changing the 64-node authoritative graph, treating a projection
  as proof evidence, weakening source/coverage gates, or promoting registry
  entries.

### T-P7-001 — fallback tail obligation audit

- status: `reviewed_pending` (integrated at Route-B revision 352; the first
  review was triage-only because the target was not discoverable; a concrete
  target is now bound below; continuation math integrated at the next
  Route-B revision)
- target: external
  `robot_final/verify_physical_rational_tail_global_bound.py`, with inputs
  `routeB_dense_Mq/routeB_physical_rational_tail_cs_polynomial.csv`,
  `routeB_dense_Mq/routeB_physical_rational_tail_global_bound.csv`, and
  `routeB_dense_Mq/routeB_Mq_M0.csv`;
- exact child: `examples/routeb_p7_tail_bound_lean/`, proving the final
  rational scalar inequalities for `qmax=13/50` and `qmax=3/8`;
- deliver: preserve the checker and Lean receipt hashes, then determine whether
  the polynomial tail is source-bound and can be joined to residual/flowpipe
  obligations; the current arithmetic child is reusable but remains open for
  physical admission;
- forbidden: treating the scalar tail bound as full residual absorption,
  substituting it for P8 flowpipe coverage, or promoting P7/M4/registry.

The continuation result gives the next mathematical child: a typed 2x2 Schur
completion/absorption lemma consuming `eta < 1/160000`. The source-side
identification of the inverse block, normalization scalar, and seven-term
polynomial remains a separate frontier.

### T-P7-002 — typed 2x2 tail Schur completion

- status: `local_sidecar_prepared` (released for the next mathematical round)
- owner: `红莲魔尊`
- scope: formalize the completion identity and robust inverse-quadratic bound
  needed to consume the exact P7 `eta` inequalities;
- target: a source-independent exact-real child whose conclusion is an
  explicit absorbed scalar cost, with all positivity and normalization
  premises named;
- deliver: mathematical derivation and, if convenient, a focused Lean child
  for the validation agent; retain sharpness and the source-binding boundary;
- forbidden: identifying the seven-term polynomial with deployed DH by hash,
  claiming P7 flowpipe coverage, or promoting P7/M4/registry.
- local progress: `examples/routeb_p7_tail_schur_completion_lean/` is attached
  as `P7.tail_schur_completion_2x2`; pinned compile and physical source
  binding remain open.

### T-P5-005 — relative residual strict-decay closure

- status: `reviewed_pending` (review:
  `review-T-P5-005-kuangmanmozun-20260906T2307.md`)
- owner: `狂弓魔尊`
- source: `examples/routeb_dh_power_binding/README.md`,
  `examples/routeb_residual_power/README.md`, and the exact scalar child
  `examples/routeb_p5_residual_power_lean/`;
- scope: replace the non-closing constant residual budget by a same-domain
  relative bound `‖r‖ ≤ ρ‖v‖` with `0 ≤ ρ < δ`, and derive the strict energy
  supply `Ė ≤ -(δ-ρ)‖v‖²` with explicit weighted-norm assumptions;
- deliver: a typed mathematical lemma identifying the precise component-wise
  residual bounds needed from true-DH/FD/solve errors, or a counterexample if
  the current residual decomposition cannot support relative scaling;
- forbidden: inferring relative bounds from samples, mixing force and
  acceleration units, or closing P5/M4 without same-domain coverage.

### T-P5-006 — component-wise relative decay formalization

- status: `local_sidecar_prepared` (released after `T-P5-005` harvest)
- owner: `苏梦辰`
- source: `review-T-P5-005-kuangmanmozun-20260906T2307.md`,
  `examples/routeb_supply_core/RouteBSupplyCore.lean`;
- scope: formalize the finite-sum component-wise closure
  `|r_i|≤rho_i|v_i|`, `0≤rho_i<d_i` implies retained diagonal damping;
- deliver: source-independent theorem decomposition and a portable Lean
  sidecar if practical, with exact positivity premises;
- forbidden: deriving the premise from current FD samples/envelopes or closing
  the physical P5/M4 node.
- local progress: `examples/routeb_p5_componentwise_relative_decay_lean/` is
  attached as `P5.componentwise_relative_decay`; the physical relative-bound
  and pinned Lean receipts remain open.

### T-P5-007 — weighted dual residual decay and interface obstruction

- status: `open` (released after `T-P5-005` harvest)
- owner: `臭屁猪`
- source: `review-T-P5-005-kuangmanmozun-20260906T2307.md`,
  `examples/routeb_p5_residual_power_lean/`;
- scope: formalize the damping-weighted `dualSq r ≤ kappa²*dampedSq v`
  implication without square roots, and retain the generic force-error
  counterexample as a separate theorem;
- deliver: pinned GitHub Lean sidecar or precise compile obstruction, including
  the `kappa=0` boundary and no nonstandard axioms;
- forbidden: treating abstract premises as true-DH source binding or promoting
  compilation into the verified registry.

### T-P5-008 — deployed force-error bias/relative split

- status: `open` (released after `T-P5-005` harvest)
- owner: `红莲魔尊`
- source: `examples/routeb_dh_power_binding/DHPowerBinding.lean`,
  `examples/routeb_dh_power_binding/FDForceBudget.lean`, and deployed
  `routeB_dense_Mq/dhport_lib.jl:22-29,73-109`;
  `review-T-P5-005-kuangmanmozun-20260906T2307.md`;
- scope: classify actual mass/controller/C/G/solve terms into state-relative
  and additive-bias parts, and determine which parts vanish at the deployed
  equilibrium under explicit premises;
- deliver: exact energy-ledger split or a rigorous obstruction, with units and
  domain assumptions stated. In particular account explicitly for the
  `MASS_REGULARIZER=1e-6`, `CG_FINITE_DIFF_STEP=1e-5`, and the
  `tau-Cdq-Gq` construction; do not infer vanishing from generic interfaces;
- forbidden: converting positive-offset envelopes into `rho|v|`, using samples
  as global estimates, or closing P5/M4.

### T-P5-009 — FD envelope relative-scaling obstruction

- status: `open` (released after `T-P5-005` harvest)
- owner: `柳冠一`
- source: `examples/routeb_dh_power_binding/FDForceBudget.lean:14-18,46-55`
  and the exact offsets recorded in
  `review-T-P5-005-kuangmanmozun-20260906T2307.md`;
- scope: produce a minimal typed adapter showing precisely what extra
  equilibrium/state contract would be needed to turn a slope-plus-offset FD
  envelope into a relative bound, or prove that the current interface cannot;
- deliver: interface lemma or counterexample with no hidden change of cap,
  coordinate order, or units;
- forbidden: silently replacing the FD envelope, claiming true-DH binding, or
  closing P5/M4.

## Queue: next parallel leaves

### T-P3-003 — canonical source-manifest binding

- status: `reviewed_pending` (integrated at Route-B revision 334; result:
  `review-T-P3-003-source-manifest.md`)
- scope: reconcile the authoritative Julia/DH source, coordinate order,
  arithmetic convention, and current delivery manifest without running a full
  interval search;
- deliver: one review result with exact paths, hashes, and the smallest
  admissible source-binding contract;
- forbidden: treating equal payload bits or point samples as global bounds.

### T-P4-003 — force/acceleration residual normalization

- status: `reviewed_pending` (integrated at Route-B revision 334; result:
  `review-T-P4-003-residual-normalization.md`)
- scope: formalize the typed map between `l = I f - M0 a` and the PMI-side
  residual `d`, preferably as a focused algebra/Lean sidecar;
- deliver: review result plus focused compile/check evidence if available;
- forbidden: closing true-DH binding, coverage, or the P4 parent.

### T-P8-003 — freeze the state contract

- status: `reviewed_pending` (integrated at Route-B revision 334; result:
  `review-T-P8-003-contract.md`)
- scope: decide whether the deployed 13-state RHS requires an explicit-time
  theorem or a separately justified 14-state ramp source;
- deliver: minimal theorem signature and admission blockers;
- forbidden: silently changing the target theorem or claiming a flowpipe.

### T-P5-001 — energy-syzygy admission audit

- status: `reviewed_pending` (integrated at Route-B revision 337; result:
  `review-T-P5-001-energy-syzygy.md`)
- scope: isolate the exact Newton–Euler energy identity from sparse SOS and
  true-DH source obligations, and identify the smallest reusable child;
- deliver: review result with statement, dependencies, and evidence boundary;
- forbidden: promoting solver output or an abstract identity to physical M4.

### T-P4-004 — typed normalization Lean sidecar

- status: `reviewed_pending` (integrated at Route-B revision 337; result:
  `review-T-P4-004-normalization-sidecar.md`)
- scope: keep force residual `l` and PMI residual `d` as distinct typed
  objects, connected only through an explicit interface premise;
- deliver: focused Lean sidecar or review result, with no true-DH/coverage
  admission;
- forbidden: closing the P4 parent or mutating the authoritative checkpoint.

### T-P8-004 — explicit-time contract sidecar

- status: `reviewed_pending` (integrated at Route-B revision 338; result:
  `review-T-P8-004-explicit-time-sidecar.md`)
- scope: formalize the smallest 13-state explicit-time interface with external
  parameter `c`, initial projection, and terminal-transfer assumptions;
- deliver: focused Lean sidecar or review result; no broad regression;
- forbidden: silently changing the current theorem target or claiming a flowpipe.

### T-P3-004 — source-semantic adapter design

- status: `reviewed_pending` (integrated at Route-B revision 339; result:
  `review-T-P3-004-semantic-adapter.md`)
- scope: design the smallest adapter from canonical Julia/DH source manifest to
  Lean/checker semantics using existing snapshots;
- deliver: review or disjoint sidecar with explicit semantic premises and
  hashes; retain `pending` status;
- forbidden: treating hash equality as a semantic proof or running full search.

### T-FLT-DERIV-CALC — Anthropic FLT derivation/calculus scan

- status: `reviewed_pending` (catalog review integrated as event-only metadata)
- scope: audit generic derivation, calculus, continuity, integral, and limit
  infrastructure from the pinned Anthropic FLT source; identify only candidates
  whose assumptions can be restated for the current adapter/PDE lanes;
- deliver: exact source path, declaration, commit, license/provenance, reuse
  class, and a focused target-side compile proposal;
- forbidden: importing FLT-specific arithmetic or treating a scan as a proof,
  Route-B node closure, or registry promotion.

### T-FLT-TOPOLOGY-QUOTIENT-CLM — quotient/topology transport scan

- status: `reviewed_pending` (catalog review integrated as event-only metadata)
- scope: audit quotient, subsingleton, connectedness, continuity,
  `ContinuousLinearMap`, and transport infrastructure for small adapter-side
  reuse;
- deliver: exact source path/declaration, hypotheses, reuse class, and the
  smallest target-side sidecar that could be compiled without whole-repo build;
- forbidden: copying the upstream tree, weakening assumptions, or promoting
  architecture-only evidence to a verified theorem.

### T-P3-005 — minimal semantic-binding child theorem

- status: `reviewed_pending` (integrated at Route-B revision 341; result:
  `review-T-P3-005-semantic-binding-child.md`)
- scope: isolate the smallest typed child interface that connects the
  canonical Julia/DH source to Lean/checker semantics, with explicit semantic
  premises and independent provenance hashes;
- deliver: exact statement, dependency boundary, focused-check proposal, and
  unresolved true-DH/coverage blockers;
- forbidden: equating hashes with semantics, changing the authoritative source,
  or closing P3/P0/M4.

### T-P5-002 — minimal Newton–Euler energy child

- status: `reviewed_pending` (integrated at Route-B revision 341; result:
  `review-T-P5-002-energy-child.md`)
- scope: isolate a standalone energy/power identity or syzygy child theorem
  from the current 6-DOF dynamics implementation;
- deliver: typed statement, exact dependencies, evidence level, and a focused
  compile/check route that does not require a full regression;
- forbidden: promoting sparse SOS output, assuming true-DH binding, or claiming
  flowpipe/terminal transfer.

### T-P3-006 — source-binding interface sidecar

- status: `reviewed_pending` (integrated at Route-B revision 342; Lean blocked:
  `review-T-P3-006-semantic-binding-sidecar.md`)
- scope: encode the P3-005 premise boundary in a small adapter-side contract;
  keep source hashes, exact snapshot semantics, and interval enclosure as
  separate fields;
- deliver: isolated sidecar/README plus focused compile or a precise blocked
  report;
- forbidden: concrete Float64-to-exact equality, global DH identification,
  registry promotion, or edits to the authoritative checkpoint.

### T-P5-003 — Christoffel power identity sidecar

- status: `reviewed_pending` (integrated at Route-B revision 342; focused Lean
  compile passed, no registry promotion:
  `review-T-P5-003-christoffel-power-sidecar.md`)
- scope: isolate and compile the exact Christoffel power identity already
  identified by P5-002, with minimal imports and explicit #print axioms;
- deliver: isolated Lean sidecar/README and focused compile evidence;
- forbidden: importing sparse SOS or flowpipe claims, assuming source binding,
  or closing the P5/M4 parent theorem.

### T-P5-004 — dissipative residual-power inequality child

- status: `reviewed_pending` (integrated at Route-B revision 354; Lean child
  now compiled at `examples/routeb_p5_residual_power_lean/`)
- scope: formalize the scalar premise `y ≤ -δ*x^2 + ε*x` and expose exact
  retained-dissipation, Young-family, threshold, and relative-residual lemmas;
- deliver: compile receipt and a typed downstream interface for supplying
  physical coercivity/residual bounds;
- forbidden: assuming `δ` and `ε` from samples, identifying force and
  acceleration residuals without a units bridge, or closing P5/M4 from this
  abstract child alone.

### T-P4-005 — sharp one-channel residual source binding

- status: `reviewed_pending` (integrated at Route-B revision 356; exact scalar
  child compiled at `examples/routeb_p4_sharp_residual_lean/`)
- scope: replace the unnecessarily conservative `r² ≤ (1/100)² y²` target by
  the sharp scalar interface `r² ≤ p*d*y²`, then bind one actual deployed
  force/acceleration residual channel to that envelope;
- deliver: exact source-bound residual lemma and a focused receipt, retaining
  `p`, `d`, units, and the source expression as typed objects;
- forbidden: equating force and acceleration residuals, using a constant bias as
  a universal PSD witness, or closing P4/M4 from the abstract sharp child.

### T-P4-006 — sharp Schur formalization sidecar

- status: `reviewed_pending` (formalization result integrated at the next
  Route-B revision; current Lean compile is environment-blocked)
- scope: independently formalize the exact iff condition, the zero-slice
  obstruction, and the concrete block-4 `c=1/4` absorption corollary;
- deliver: focused pinned-Lean compile, `#print axioms`, and independent
  validator review, without weakening the theorem statement;
- forbidden: treating exact Python arithmetic as kernel evidence, binding the
  source residual by hash alone, or closing P4/M4 from this abstract child.

### T-P8-006 — ramp reconstruction and terminal transfer

- status: `compiled_candidate_recorded` (independent review retained)
- scope: formalize the scalar tail equations `w'=c`, `c'=0`, `w(0)=0` and
  derive `c(t)=c0`, `w(t)=c0*t`, plus the `T=1` terminal transfer;
- deliver: minimal Lean child or a precise interval-API blocker, with the
  first-12 explicit-time projection kept separate from source binding;
- forbidden: claiming ODE existence, `[0,1]` flowpipe coverage, deployed
  13-state semantic binding, or P8/M4 admission from this child alone.
- local progress: the independent GitHub compile/axiom review is now
  represented as `P8.ramp_reconstruction_compiled_candidate`; it remains
  below registry and physical first-12/source/flowpipe admission.

### T-P8-007 — pinned validation of ramp sidecar

- status: `reviewed_pending` (integrated at Route-B revision 363; review:
  `review-T-P8-007-choupizhu-20260906T2307.md`)
- scope: run the focused verifier for
  `examples/routeb_p8_ramp_reconstruction_sidecar/` under the pinned Lean
  environment and retain the exact compile/axiom output;
- deliver: immutable review plus receipt if compiled, or a precise repair
  report if the sidecar has a local Lean error;
- forbidden: local-environment substitution, source-binding claims, flowpipe
  coverage, registry promotion, or broad regression.

### T-P8-009 — interval-local ramp calculus refinement

- status: `open` (released after the P8-007 harvest)
- owner: `苏梦辰`
- source: `review-T-P8-007-choupizhu-20260906T2307.md` and
  `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`;
- scope: weaken the current all-`ℝ` differentiability assumptions to an
  interval-local/end-point theorem sufficient for `[0,1]` terminal transfer,
  while keeping `w'=c`, `c'=0`, and the tail slots typed;
- deliver: a separate Lean child or an exact API obstruction; do not alter the
  already compiled candidate or pretend interval calculus gives ODE existence;
- forbidden: source binding, flowpipe coverage, first-exit closure, or registry
  promotion from the abstract calculus child.

### T-P8-010 — independent gate review for compiled P8 candidate

- status: `reviewed_pending` (review retained as compiled candidate)
- owner: `封不觉`
- source: `review-T-P8-007-choupizhu-20260906T2307.md`, GitHub Actions run
  `34085393805`, job `101628339820`, and the sidecar blob/receipt hashes;
- scope: independently check the pinned toolchain, zero-sorry theorem set,
  axiom report, statement identity, provenance, and admission boundary;
- deliver: immutable gate review recording `compiled_candidate` or a precise
  rejection; a successful sidecar must remain outside the verified registry
  until source binding, coverage, and parent dependencies close;
- forbidden: accepting the CI green mark as physical P8/M4 proof, changing the
  theorem statement, or broad regression.

### T-P4-007 — actual block-(4,5) residual decomposition

- status: `open` (released for the next mathematical round)
- owner: `柳冠一`
- source: external `routeB_dense_Mq/routeB_pmi_certificate.jl:98-101,169-179`
  and `dhport_lib.jl:102-109`; local mirror
  `examples/routeb_source_binding_audit/REPORT.md` section `B45-5`;
- scope: derive the exact typed identity
  `I_B f_B(q_B,v_B,w) - M0_BB a_B(q,v,w) = l_B(q,v,w)`, explicitly charging
  remote-state, `C_FD`, `G_FD`, solve, and the PMI `kc` mismatch terms;
- deliver: a symbolic decomposition or a sharp obstruction showing which
  terms cannot be bounded by the current `c=1/4` envelope;
- forbidden: point-sample equality, hash-only semantic binding, or closing P4
  from the abstract Schur child.

### T-P4-008 — explicit `kc`/remote-`M_BD` obstruction child

- status: `open` (released as a disjoint negative/obstruction leaf)
- owner: `柳冠一`
- source: `docs/routeb-c2-d-normalization-audit.md:105-128,235-241`,
  `docs/routeb-source-fork-canonical-audit.md:80-108`, and the historical
  `B45-5_kc_mismatch_and_mbd_obstruction` audit;
- scope: formalize or sharply restate that the deployed block identity contains
  `M_BD(q)a_D` and explicit `kc` residual terms, while the current PMI projection
  and acceleration-side D-row do not supply those bindings. With the deployed
  PMI source's `kc=0.05=1/20`, the concrete omitted cross term is the typed
  vector `rho_kc^f(q_B)=(q5/20,q4/20)` in normalized f coordinates, and its
  force-scale image `rho_kc^F(q_B)=(q5/100,q4/200)`;
- deliver: a typed obstruction/countermodel identifying the missing bounded
  full-state or source-model contract, with the force-vs-acceleration units kept
  distinct, and an exact sign/index statement for `rho_kc`;
- forbidden: using the old comment `(M-M0)_BD a_D` as the current identity,
  treating the numerical Gram residual as physical error, or closing P4/M4.

### T-P3-008 — central-FD Christoffel source binding

- status: `open` (released for the next mathematical round)
- owner: `古月方源`
- source: external `routeB_dense_Mq/dhport_lib.jl:73-92` and
  `routeB_analytic_fourier_dynamics_probe.py:94-97`; local exact algebra at
  `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`;
- scope: derive the typed equality between the source `Cdq` central-difference
  contraction and the generic Christoffel tensor expression, keeping FD
  remainder and true-DH derivative semantics as explicit premises;
- deliver: a source-independent algebraic child plus the smallest semantic
  adapter statement, or a precise obstruction if the source indexing differs;
- forbidden: treating the generic Christoffel identity as source binding,
  replacing central differences by analytic derivatives silently, or closing
  P3/P5/M4.

### T-P3-009 — block-(4,5) positive-block and inverse bounds

- status: `open` (released for the next mathematical round)
- owner: `星宿仙尊`
- source: external `routeB_dense_Mq/routeB_pmi_certificate.jl:85-101`,
  `routeB_Mq_M0.csv`, and the existing exact inverse/Schur artifacts under
  `examples/routeb_source_binding_audit/`;
- scope: establish a rational lower bound for the actual covered
  block-(4,5) positive matrix and corresponding upper bounds for its inverse
  entries, or exhibit a cell/source mismatch that prevents such a bound;
- deliver: exact matrix inequality, eigenvalue/LDL route, and explicit domain
  assumptions suitable for consuming `T-P7-002` and the P4 sharp Schur child;
- forbidden: treating the constant `M0_BB` as `M(q)` without proof, using
  sampled eigenvalues as global bounds, or closing P3/P4/M4 from this child.

### T-P3-010 — actual DH block-(4,5) mass interval derivation

- status: `open` (released as a disjoint P3 source-math leaf)
- owner: `古月方源`
- source: external `routeB_dense_Mq/dhport_lib.jl:31-60`,
  `routeB_Mq_M0.csv`, and the deployed q-box/domain contract;
- scope: derive the exact block-(4,5) entries of `M(q)` from the DH Jacobian
  construction, then give rational interval bounds on the covered q-domain
  (or a precise obstruction caused by the regularized/Float64 semantics);
- deliver: formula-level source binding plus an interval/monotonicity route that
  `T-P3-009` can consume, explicitly separating `regularization=1e-6` from the
  unregularized DH matrix;
- forbidden: identifying `M0_BB` with `M(q)`, using sampled extrema as global
  bounds, silently differentiating Float64 code analytically, or closing P3/P4/M4.

### T-M4-003 — weighted terminal split and exact wider residual gate

- status: `reviewed_pending` (review:
  `review-T-M4-003-kuangmanmozun-20260906T2258.md`)
- owner: `狂弓魔尊` (mathematical source); formalization released separately
  below;
- scope: replace the fixed `(3/2,3)` terminal Young split by the exact
  parameterized weighted identity, and record the sharp information-only
  limit before any constant tuning is attempted;
- result: the review derives the exact family with `eta>0`, identifies
  `eta=81/160`, and proves the arithmetic corollary `D<=1401/625` has positive
  margin under the current `L,g` values;
- boundary: this is only a terminal consumer. It does not create `L`, `g`,
  residual coverage, flowpipe coverage, true-DH binding, or registry evidence.

### T-M4-004 — generic weighted qpoly split sidecar

- status: `open` (released after `T-M4-003` harvest)
- owner: `苏梦辰`
- source: `review-T-M4-003-kuangmanmozun-20260906T2258.md`,
  `examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean`;
- scope: formalize the division-free identity-based weighted split for the
  existing four-coordinate `qpoly`, with explicit `eta` and no repository
  specific arithmetic assumptions;
- deliver: a portable Lean sidecar and a source-independent theorem statement,
  plus exact toolchain/receipt metadata if GitHub validation succeeds;
- forbidden: changing the authoritative M4 gate, claiming terminal coverage,
  or promoting the sidecar to the verified registry by compilation alone.

### T-M4-005 — eta81 terminal arithmetic corollary

- status: `open` (released after `T-M4-003` harvest)
- owner: `臭屁猪`
- source: `review-T-M4-003-kuangmanmozun-20260906T2258.md`,
  `examples/routeb_terminal_qpoly_comparator_lean/`;
- scope: consume the generic weighted split and formalize the exact rational
  specialization `eta=81/160`, `D<=1401/625`, preserving the current `L,g`
  premises as typed hypotheses;
- deliver: a GitHub-pinned Lean validation sidecar or a precise compile
  obstruction, with exact positive terminal margin and no hidden Float64 step;
- forbidden: silently replacing `D_gate=4483/2000`, creating physical `L/g`
  bounds, or closing M4/P8 from this arithmetic child alone.

### T-M4-006 — P7 × P8 × M4 cross-branch budget transfer

- status: `reviewed_pending` (review:
  `review-T-M4-006-daai-xianzun-20260906T2346.md`)
- owner: `大爱仙尊` (mathematical source); formalization and source-binding
  children remain separate;
- scope: compose the conditional P7 tail charge with the P8 ramp identity and
  the exact M4 `eta=81/160` consumer. The reusable interface is
  `D_total <= D_base + rho_bar/160000`; at the old gate,
  `D_base<=4483/2000` and `rho_bar<=16` imply
  `D_total<=1401/625`;
- boundary: this is a budget-transfer theorem only. It does not prove a
  physical `rho_bar`, identify the P7 variables with deployed DH variables,
  establish flowpipe/coverage, or change the authoritative M4 gate.

### T-M4-007 — pure arithmetic budget-transfer sidecar

- status: `local_sidecar_prepared` (released from the M4-006 mathematical review)
- owner: `苏梦辰`
- source: `review-T-M4-006-daai-xianzun-20260906T2346.md`;
- scope: formalize only the division-free arithmetic implications
  `D_base+D_tail <= 1401/625` from `D_tail<=rho_bar/160000` and the exact
  old-gate corollary `rho_bar<=16`; keep the integral/ramp lemma separate;
- deliver: pinned GitHub Lean sidecar or precise compile obstruction, with
  exact rational constants and no hidden source assumptions;
- forbidden: changing `D_gate`, proving physical `rho_bar`, or closing
  residual absorption/flowpipe/M4 from arithmetic alone.
- local progress: `examples/routeb_m4_cross_branch_budget_lean/` is now
  attached as the independent M4 arithmetic child; its pinned Lean result and
  P7/P8 source bindings remain open.

### T-P8-008 — first-12 explicit-time source adapter

- status: `open` (released for the next mathematical round)
- owner: `古月方源`
- source: `examples/routeb_p8_ramp_reconstruction_sidecar/` and
  `examples/routeb_p8_contract_adapter/`, with the deployed 13-state RHS
  contract in `docs/routeb-p8-flowpipe-binding-next.md`;
- scope: formulate the exact first-12 trajectory projection that combines the
  source mechanical outputs with the adapter-supplied ramp tail
  `w=c0*t,c=c0`;
- deliver: a typed theorem signature and either a source-side derivation or a
  concrete mismatch, keeping the 13th source derivative `du[13]=0` explicit;
- forbidden: identifying the full 13-state source with the 14-state ramp ODE,
  claiming existence/coverage, or changing the target theorem silently.

### T-P4-011 — canonical `kc` budget across normalized and force scales

- status: `open` (released after the source-contract correction)
- owner: `幽魂魔尊`
- source: `docs/routeb-p4-kc-force-contract.md`,
  `routeB_dense_Mq/routeB_pmi_certificate.jl:46-49,98-99`, and the P4 sharp
  Schur sidecar;
- scope: derive an exact, source-independent quadratic cost for the normalized
  term `rho_kc^f=(q5/20,q4/20)` and its force-scale image
  `rho_kc^F=(q5/100,q4/200)` on the declared `(q4,q5)` domain, then determine
  whether it can fit the current Schur/Young budget or yields a precise
  obstruction. Keep the local `p`/`d` variables and force units explicit;
  distinguish a joint-limit bound from a local `p<=eta` bound;
- deliver: rational/`pi` inequality with a sharp or clearly justified bound,
  plus the smallest typed premise that a future P4 PMI child can consume;
- forbidden: treating either coordinate scale as the other without the
  inertia map, using samples as a global bound, or closing P4/M4 from this
  child alone.

### T-P4-KC-COORDINATE-ADAPTER — exact normalized-to-force map

- status: `open` (local sidecar added; GitHub Lean compilation pending)
- owner: `巨阳仙尊`
- source: `examples/routeb_b45_5_residual_decomposition_lean/ResidualDecomposition.lean`;
- scope: compile and inspect `forceScaleKc_eq_rhoKc` and
  `rhoKc_sq_le_of_block_energy`, mapping normalized `(q5/20,q4/20)` through
  `diag(1/5,1/10)` to force `(q5/100,q4/200)` and proving the block-domain
  budget `||rho_kc||^2 <= 7/18750`;
- deliver: pinned Lean output, zero-sorry/axiom report, and exact theorem
  statement review; keep source binding and global P4 admission separate;
- forbidden: treating this coordinate adapter as a proof of DH equivalence,
  domain coverage, residual absorption, or M4 closure.

### T-P4-MBD-PROJECTION — full-state remote-term repair

- status: `open` (exact projection obstruction recorded locally)
- owner: `大爱仙尊`
- source: `docs/routeb-p4-mbd-projection-obstruction.md` and
  `scripts/check_routeb_p4_mbd_obstruction.py`;
- scope: use the exact nonzero `M_BD(0)e1` obstruction to formulate the
  smallest full-state descriptor/remote-enclosure theorem that can replace
  the invalid block-only `gammaRemote` premise;
- deliver: a typed premise for bounded `a_D`, exact Schur elimination, or an
  equivalent remote residual contract, with an explicit projection-to-full-
  state map;
- forbidden: claiming arbitrary `lambda` is a physical trajectory, using the
  obstruction as a complete dynamics disproof, or closing P4/M4 without
  coverage and source binding.

### T-P3-011 — link-Jacobian structural lower bound for block `(4,5)`

- status: `open` (released as a disjoint positive-block math leaf)
- owner: `大爱仙尊`
- source: deployed `routeB_dense_Mq/dhport_lib.jl:31-60`, DH constants in that
  file, and `routeB_Mq_M0.csv` only as a reference snapshot;
- scope: isolate explicit positive-semidefinite link terms in the DH mass sum
  whose principal `(4,5)` block gives a q-independent or domain-explicit
  lower bound stronger than the global `10^-6 I` regularizer. If the
  rotational/translational Jacobian geometry cannot provide such a bound,
  return the exact rank/cell obstruction;
- deliver: formula-level PSD decomposition and an exact rational lower bound
  (or obstruction), with `regularization=0` and `regularization=1e-6` kept as
  separate statements so P3-009 can consume it;
- forbidden: identifying `M0_BB` with `M(q)`, sampled eigenvalues, Float64
  analytic differentiation without a remainder contract, or closing P3/P4/M4.

### T-FLT-SPECTRAL-LINEAR — spectral and linear algebra scan

- status: `reviewed_pending` (integrated at Route-B revision 343;
  event-only catalog review)
- scope: inspect only non-number-theory spectral, eigenspace, finite-dimensional
  linear algebra, quotient, and exact-sequence declarations in the pinned FLT
  repository;
- deliver: three-level reuse classification, exact declaration/path, imports,
  hypotheses, source commit/license, and the smallest current-pin sidecar
  proposal;
- forbidden: importing arithmetic endgames or claiming Route-B spectral/PDE
  closure from a source scan.

### T-FLT-QUOTIENT-SIDECAR — pinned quotient transport probe

- status: `open` (released as the first direct-reuse FLT API probe)
- owner: `巨阳仙尊`
- source: `examples/anthropic_flt_quotient_transport_sidecar/`, with upstream
  `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-37`;
- scope: run the focused sidecar in the pinned GitHub environment, check the
  exact declaration statements, `#print axioms`, provenance and import
  closure, and report whether the two continuous quotient transport APIs are
  directly reusable, lightly adapted, or blocked on the target pin;
- deliver: immutable review with compiler output/hashes and a target-side
  adapter recommendation. A green compile remains an event-only catalog
  result and does not enter the Route-B theorem registry;
- forbidden: importing FLT number theory, whole-repository regression, or
  inferring P3/P8 coverage or physical source binding from this API probe.

### T-FLT-TRANSPORT-ADAPTER — transport and adapter scan

- status: `reviewed_pending` (integrated at Route-B revision 344;
  event-only catalog review)
- scope: inspect generic continuous-map, linear-equivalence, pairing transport,
  representation, and coordinate-change adapters outside pure number theory;
- deliver: exact statement shape, assumptions, reuse class, attribution, and
  target-side adaptation risks;
- forbidden: whole-repository build, source copying, or registry promotion.

### T-FLT-INFRA-REGISTRY — registry/graph/obstruction scan

- status: `reviewed_pending` (integrated at Route-B revision 343;
  event-only catalog review)
- scope: inspect comparator, challenge/solution split, dependency graph,
  documentation extraction, attribution, and obstruction-tracking patterns;
- deliver: architecture-only findings and concrete integration points for the
  local DAG/frontier/registry, preserving fail-closed authority boundaries;
- forbidden: treating HTML badges, graph nodes, or comparator fixtures as
  proof evidence.

### T-FLT-SPECTRAL-SIDECAR — highest-value spectral candidate

- status: `reviewed_pending` (integrated at Route-B revision 346; independent
  admission review classifies it as architecture-only)
- scope: test the smallest non-number-theory eigenspace/range bridge identified
  by the spectral scan, using a new isolated sidecar and the current local
  Lean/Mathlib pin if available;
- deliver: exact theorem boundary, imports, compile output, #print axioms,
  provenance, and explicit reason if the upstream wrapper is too specialized;
- forbidden: whole FLT build, arithmetic theorem reuse, registry promotion, or
  inferring Route-B spectral closure from a failed/blocked compile.

### T-FLT-SPECTRAL-PREDICATE — genuine eigenspace predicate sidecar

- status: `reviewed_pending` (integrated at Route-B revision 348; current
  version has a real eigenspace predicate, but Mathlib `.olean` verification
  is blocked; prior reviews cover successive sidecar versions)
- scope: replace the tautological range helper with a proposition containing an
  actual eigenspace predicate, explicit operator/eigenvalue assumptions, and a
  range-to-eigenspace equality or a clearly stated obstruction;
- deliver: isolated Lean sidecar, #print axioms, exact distinction between a
  self-contained abstraction and direct upstream reuse;
- forbidden: tautological range identities, arithmetic FLT reuse, registry
  promotion, or declaring the original spectral sidecar verified.

### T-P8-011 — interval-local ramp endpoint adapter

- status: `open` (local interval seam added 2026-09-07; awaiting pinned compile)
- owner: `巨阳仙尊` for the pinned Lean compile/axiom receipt; `红莲魔尊` or
  `幽魂魔尊` may separately bind the source-side integral premise;
- scope: inspect `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`,
  especially `endpoint_eq_of_zero_derivative_on_interval` and
  `ramp_endpoint_on_interval`; compile only this sidecar in the pinned GitHub
  environment and report exact theorem statements, imports, `#print axioms`,
  source hash, and any API repair needed;
- mathematical deliverable: bind `ContinuousOn` on `Icc`, `HasDerivAt` on
  `Ioo`, derivative integrability, and the exact identity
  `∫ c = c0 * (b-a)` to the deployed P8 source/flowpipe contract;
- forbidden: upgrading this adapter to P8 reachability, silently supplying
  source equality or coverage, whole-project regression, registry promotion,
  or treating a green sidecar compile as Route-B admission.

### T-P3-012 — exact-real derivative-hull leaf admission probe

- status: `open` (external artifact recorded locally at Route-B revision 396)
- owner: `巨阳仙尊`;
- scope: independently inspect and, if needed, recompile the referenced
  artifact `task_FLT_routeb_derivative_leaf_20260908` at its recorded Lake/
  Mathlib pin. Check the exact public theorem statements, source hash,
  `#print axioms`, placeholder scan, and whether the artifact is compatible
  with the current P3 child statement;
- deliver: an immutable review or handoff receipt that preserves the source
  path and pin. This is an abstract calculus-child validation, not registry
  promotion;
- forbidden: claiming concrete six-joint DH instantiation, Float64/libm
  rounding, interval coverage, flowpipe semantics, or P3 parent closure.

### T-P3-013 — one concrete true-DH derivative-hull instantiation

- status: `open` (mathematical bottleneck released after abstract seam landed)
- owner: `大爱仙尊`;
- scope: use the exact-real derivative-hull interface from
  `P3.true_dh_derivative_hull_leaf` to bind one concrete deployed DH source
  family (mass, gravity, or Coriolis) on one declared coordinate cell. The
  result must state the exact source snapshot, coordinate convention, convex
  domain, derivative operator, hull radius, and every unresolved rounding or
  coverage premise;
- deliver: a bounded mathematical child or a counterexample/obstruction with
  exact formulas and a machine-readable contract. Prefer closing one genuine
  coordinate-family instance over another broad audit;
- forbidden: replacing exact source equality with samples, treating central
  finite differences as analytic derivatives, using solver status as proof,
  or claiming full P3/Route-B closure from one local instance.

### T-P3-014 — directed trig leaf to source-binding bridge

- status: `open` (abstract Lean leaf recorded at Route-B revision 397)
- owner: `红莲魔尊` for the mathematical/source-boundary bridge;
- scope: use `P3.trig_endpoint_enclosure_leaf` to bind one declared
  `iv_sin`/`iv_cos` monotonicity cell from the canonical Route-B interval
  evaluator. Derive the exact turning-point split/domain obligation and list
  the directed BigFloat/MPFR operations that still need executable evidence;
- deliver: a bounded contract or obstruction for one concrete cell, including
  source hash, endpoint semantics, exact angle domain, and outward conversion
  assumptions. A focused runtime check is useful only as evidence of the
  executable layer, not as a theorem;
- forbidden: treating the abstract Mathlib leaf as proof of Julia/MPFR
  rounding, skipping turning-point coverage, whole-project reruns, or closing
  P3/Route-B from a single trigonometric cell.

### T-P3-015 — exact M33 Fourier leaf lift

- status: `open` (exact checker leaf recorded at Route-B revision 399)
- owner: `巨阳仙尊` for the smallest pinned Lean statement/axiom probe;
  `大爱仙尊` may separately inspect whether the exact M33 identity can feed a
  concrete P3 mass-entry bound;
- scope: inspect `P3.m33_exact_fourier_source_leaf` and the referenced
  `task_routeb_source_fourier_binding_current` artifact. Preserve the
  canonical `dhport_lib.jl` hash, rationalization convention, 11-mode witness,
  and active angles `{q4,q5}`. Determine the smallest kernel-friendly theorem
  or exact obstruction for lifting the coefficient identity;
- deliver: a bounded Lean/checker receipt or a concrete obstruction that keeps
  exact formula equality, Float64/libm rounding, all-entry binding, and P3
  coverage as separate obligations;
- forbidden: using grid samples, treating the exactized formula as Float64
  semantic equivalence, claiming mass coercivity/inverse bounds, or registry
  promotion from the checker leaf alone.

### T-P3-016 — exact M33 rational lower-bound lemma

- status: `open` (local algebraic sidecar added at Route-B revision 400)
- owner: `巨阳仙尊` for pinned Lean compilation and axiom receipt;
- scope: compile `examples/routeb_m33_exact_lower_lean/M33LowerBound.lean`
  and verify `RouteBM33ExactLower.m33_lower_bound`. Check that the factorized
  proof uses only the cosine box and exact rational arithmetic, and bind its
  upstream M33 formula hash without promoting the upstream checker itself;
- deliver: immutable compile/axiom result or a precise repair, plus any
  statement mismatch needed before this child can be consumed by P3 mass
  bounds;
- forbidden: inferring the M33 source formula from the lower-bound lemma,
  treating it as Float64 semantics, claiming all-entry mass coercivity, or
  opening the P3/formal gate.

### T-P3-017 — rotational prefix mass lower-bound lift

- status: `open` (external exact checker candidate recorded at Route-B revision 403)
- owner: `大爱仙尊` for the concrete source/geometry binding; `巨阳仙尊` for
  the smallest pinned Lean formalization of the prefix-Gram argument;
- scope: consume `P3.rotational_prefix_mass_lower_bound` and the referenced
  `routeB_compact_rotational_mass_lower_certificate.csv`. Establish the
  exact six-link prefix-map inequality from isotropic inertia and unit DH-axis
  semantics, and report all assumptions needed to turn the six positive
  principal minors into `M(q) ⪰ 9401/1000000 I`;
- deliver: a bounded Lean child, or a source-semantics obstruction with exact
  principal-minor values, source hashes, and q-independence argument;
- forbidden: using the result as Float64 evidence, silently adding
  translational or Coriolis semantics, claiming inverse/flowpipe closure, or
  promoting the Python checker result to the verified registry.

### T-P4-019 — 81-cell block45 mass-geometry Schur lift

- status: `open` (external 81-cell checker candidate recorded at Route-B revision 404)
- owner: `幽魂魔尊` for the exact Schur/PMI mathematical composition; `巨阳仙尊`
  may provide the smallest typed Lean certificate interface;
- scope: consume `P4.block45_global_mass_geometry_schur` and verify the exact
  threshold, 81-cell coverage, positive minimum pivot, and the declared
  `q1/q6` independence. Bind the mass semantics and determine the minimal
  theorem/receipt needed to consume this geometry child in P4;
- deliver: an independent mathematical child or obstruction with source hash,
  cell/domain contract, and explicit separation of geometry from dynamics,
  residual absorption, flowpipe, and terminal budget;
- forbidden: treating directed interval output as a kernel proof, inferring
  q1/q6 dynamic coverage from absent mass angles, using solver `OPTIMAL`, or
  closing M4/formal admission from the 81-cell ledger alone.

### T-M4-008 — conditional energy-to-Schur terminal bridge

- status: `open` (exact composed checker candidate recorded at Route-B revision 405)
- owner: `幽魂魔尊` for the exact 2x2 metric/terminal composition; `红莲魔尊`
  may independently bind the energy inequality and initial storage premise;
- scope: consume `M4.energy_to_schur_budget_bridge`. Verify that the 81-cell
  geometry threshold equals the required threshold, the 2x2 comparison has
  exact determinant zero and nonnegative diagonals, and the conditional
  conclusion `p45≤12` follows from the supplied energy tube;
- deliver: a bounded Lean arithmetic child or an explicit failed/conditional
  receipt, with the energy, q1/q6 coverage, residual, and flowpipe premises
  kept as separate dependencies;
- forbidden: calling the conditional bridge a finite-time theorem, importing
  the coarse scalar-tube failure as proof, using solver status, or opening the
  M4/formal gate without all upstream premises.

### T-P4-020 — one-cell residual Schur remainder absorption

- status: `open` (highest-value mathematical blocker after the robust PMI
  structure audit)
- owner: `狂蛮魔尊` for the sharp inequality/absorption derivation; `红莲魔尊`
  may independently bind the energy-side beta contract;
- scope: select one declared block-(4,5) certification cell and derive a
  rigorous bound for the residual error coordinates `E_k` needed by the
  5x5 robust Schur PMI. Use the existing descriptor/interval artifacts only
  as source data, and state the exact norm, cell, rounding mode, polynomial
  remainder, and resulting beta margin. Prefer a nontrivial successful cell;
  if the bound fails, return the sharp counter-budget and the exact term that
  causes failure so the partitioner can split that cell;
- deliver: a machine-readable cell contract plus an independently replayable
  exact/interval calculation, with the robust PMI matrix interface consumed
  only conditionally;
- forbidden: treating the assembly probe or solver `OPTIMAL` as a proof,
  replacing all-domain coverage with sampled points, hiding the true-DH/
  Float64 seam, claiming P4/M4 closure from one cell, or registry promotion.

### T-P4-021 — resolved-cell Frobenius port-bound lift

- status: `open` (candidate leaf recorded locally at Route-B revision 407)
- owner: `大爱仙尊` for the interval/source semantic binding; `巨阳仙尊` for
  the smallest typed Lean statement and axiom receipt;
- scope: inspect `P4.residual_port_frobenius_bound` and its five hashed source
  artifacts, replay the 5120 resolved cells and the exact rational Young
  budgets for eta=2.7 and 5.6, and determine the minimal theorem interface
  needed by the P4 residual PMI. Preserve the left-output metric orientation,
  the upward seven-decimal rounding contract, and the declared source/cover
  hashes;
- deliver: a bounded source-bound/Lean candidate or a precise obstruction,
  including whether the Frobenius norm bound can be consumed through the
  combined-Schur Young route without changing the residual semantics. It does
  not provide the robust-PMI `E_k` factor directly. The local replay
  already found that Frobenius does not pointwise dominate the induced bound
  (22 cells at eta=2.7 and 39 at eta=5.6), so preserve this comparison as an
  obstruction rather than silently selecting one norm by pointwise order;
- explicitly distinguish the supplied port-energy quantity `||R a_B||²` from
  the robust-PMI error factor `E_k` in `l_true=l_poly,k+E_k xi`; they are not
  interchangeable without a typed descriptor/source adapter;
- forbidden: treating `RESOLVED`, positive Young margin, or `implicit_HG_spd`
  as kernel verification, inferring full DH/Float64 correctness, skipping
  independent interval replay, or promoting this leaf to the registry.

### T-P4-022 — generic Frobenius operator bridge

- status: `open` (formalization target recorded locally at Route-B revision 410)
- owner: `巨阳仙尊` for the pinned Lean finite-sum/Cauchy-Schwarz proof;
  `柳冠一` may review the typed adapter surface;
- scope: prove the generic real finite-matrix implication
  `0 ≤ Uᵢⱼ ∧ |Tᵢⱼ| ≤ Uᵢⱼ ⇒ ||T z||₂² ≤ (Σᵢⱼ Uᵢⱼ²)||z||₂²`.
  Keep finite index reindexing, row Cauchy-Schwarz, and the entrywise
  interval factor explicit so the theorem can consume a fixed `E_k` without
  assuming any pointwise ordering against an induced norm estimate;
- deliver: smallest pinned Lean theorem, imports, `#print axioms`, and exact
  statement identity; separately list the remaining interval-source binding;
- forbidden: inserting Float64/MPFR facts into the generic theorem, treating
  the theorem as proof of the 5120-cell source, or promoting it without the
  P4 source/remainder/coverage gates.

### T-P4-023 — weighted Frobenius port-energy adapter

- status: `open` (formalization target recorded locally at Route-B revision 413)
- owner: `巨阳仙尊` for the finite-dimensional matrix proof; `柳冠一` for
  the typed adapter between the source port map and `B_up`;
- scope: prove the exact composition target
  `B=SᵀS`, `S` invertible, `T=R S⁻¹`, `||T||F²≤ρ` implies
  `||R a||₂²≤ρ(aᵀB a)` for every `a`. Consume `T-P4-022` as a separate
  theorem input, then bind the Route-B names `R`, `B_up`, and `rho_F` only in
  an adapter layer;
- deliver: smallest pinned Lean theorem/receipt plus an explicit source
  binding contract; state whether square-root factors can be avoided by an
  equivalent PSD formulation;
- factorization guard: `B_up` is rational diagonal, but a real factor `S` may
  require non-rational square roots; do not invent a rational Cholesky factor.
  If needed, deliver a square-root-free quadratic-form/PSD adapter as the
  alternate theorem surface;
- notation guard: `rho` in this theorem is `rho_F^2`, matching the squared
  Frobenius hypothesis and the downstream raw-port budget;
- workflow lint: `scripts/check_routeb_p4_interface_consistency.py` verifies
  the cross-node notation, metric, and parent/consumer direction before a
  receipt is attached; `record_routeb_p4_interface_consistency.py` persists
  its checker hash and PASS as non-authoritative state; it cannot enter the
  registry;
- forbidden: treating this generic composition as proof of interval entries,
  equating it with robust-PMI `E_k`, using the positive ledger margin as a
  kernel result, or opening P4/M4 admission.

### T-P4-024 — combined-Schur port-energy adapter

- status: `open` (formalization target recorded locally at Route-B revision 413)
- owner: `狂蛮魔尊` for the Young/Schur inequality proof; `柳冠一` for the
  typed binding of `l_base` and `A_up`; `巨阳仙尊` may provide the pinned Lean
  norm-square API;
- scope: prove the exact finite-dimensional implication
  `theta>0 ∧ ||r||₂²≤rho*A ∧ b≥(1+theta)||l||₂²+(1+1/theta)rho*A`
  `⇒ ||l+r||₂²≤b`. Consume `T-P4-023` only as the port-energy premise and
  bind `A=a_BᵀB_up a_B` in a separate Route-B adapter;
- required equivalent interface: expose `lambda=1+1/theta>1` and the affine
  PMI block `[[b_base-lambda*rho*A_up,l_baseᵀ],
  [l_base,((lambda-1)/lambda)I₂]]`; its Schur condition is
  `b_base≥lambda*rho*A_up+lambda/(lambda-1)||l_base||₂²`. `lambda` is a
  fixed per-cell rational parameter, never state-dependent;
- deliver: smallest pinned Lean theorem, exact statement identity, and a
  source-binding receipt showing which declared base residual and `B_up`
  energy are used;
- explicitly distinguish this Young-budget adapter from robust-PMI `E_k`:
  it closes only the algebraic port-energy consumption interface, not the
  residual decomposition, all-cell coverage, flowpipe, or terminal transfer;
- notation is fixed: `rho` means the squared Frobenius budget `rho_F²`, while
  `A` means `A_up=a_BᵀB_up a_B`; agents must reject receipts that silently
  substitute `rho_F` or an unbound energy scalar;
- forbidden: treating a positive ledger margin, Float64 source, solver status,
  or one-cell result as kernel verification or P4/M4 closure.

### T-P4-025 — real norm-square expansion

- status: `open` (decomposition child of `T-P4-024`)
- owner: `巨阳仙尊` for the pinned real inner-product/norm API;
- scope: prove `||l+r||₂² = ||l||₂² + 2*⟪l,r⟫ + ||r||₂²` for finite-dimensional
  real vectors, with exact statement identity and `#print axioms` receipt;
- deliver: smallest reusable Lean lemma, independent of Route-B source or
  numerical artifacts;
- forbidden: treating the identity as residual decomposition or PMI closure.

### T-P4-026 — Young cross-term bound

- status: `open` (decomposition child of `T-P4-024`)
- owner: `狂蛮魔尊` for the sharp inequality; `巨阳仙尊` for pinned Lean
  lemma names and strict `theta>0` division;
- scope: prove `theta>0 ⇒ 2*⟪l,r⟫ ≤ theta*||l||₂² +
  theta⁻¹*||r||₂²` for finite-dimensional real vectors;
- deliver: exact Lean theorem/receipt and any API obstruction, preserving the
  scalar positivity premise explicitly;
- forbidden: absorbing the term with an unstated safety factor or claiming
  the Route-B residual/coverage gates are closed.

### T-P4-027 — fixed per-cell lambda admissibility contract

- status: `open` (new mathematical bottleneck from the compact Schur ledger)
- owner: `大爱仙尊` for exact scalar interval/ledger reasoning; `狂蛮魔尊`
  for the Schur-side strictness implications;
- scope: formalize that each consumed cell chooses one fixed rational
  `lambda_k` with `1<lambda_k<lambda_upper_k` and a nonnegative exact Schur
  margin, and that the same value is used by the affine PMI;
- scalar target: for `gamma_cell_k>0`, prove/instantiate
  `lambda_upper_k=gamma_external_k/gamma_cell_k` and
  `candidate_margin_k=gamma_external_k-lambda_k*gamma_cell_k`, with strict
  positivity of the denominator and margin handling explicit;
- deliver: a smallest pinned theorem or exact proof obligation plus a receipt
  contract for the cell witness; explicitly reject state-dependent lambda;
- local diagnostic helper: `scripts/check_routeb_fixed_lambda_ledger.py` checks
  the two scalar relations with high-precision `Decimal` reconstruction and
  explicit text-quantization tolerances; its PASS is only a contract
  diagnostic and cannot enter the registry;
- ledger warning: the current `eta=5.6` candidate grid contains rows with
  `admissible_fixed_lambda=false` (for example `lambda=5` while the cell upper
  bound is about `2.93`), so a positive margin elsewhere is not a universal
  parameter certificate;
- reconciliation warning: the aggregate `routeB_compact_port_frobenius_ledger`
  currently marks `lambda=5` admissible for `eta=5.6`, while the per-cell
  combined-Schur ledger rejects that value on some cells; agents must prove the
  two bound metrics/PMI semantics equivalent before mixing their receipts;
- forbidden: upgrading a ledger row, Float64 computation, or one-cell witness
  into all-cell coverage, residual closure, or formal-certificate admission.

### T-P4-028 — uniform fixed-lambda witness and partition repair

- status: `open` (new frontier after the fixed-lambda ledger harvest)
- owner: `大爱仙尊` for the exact scalar/partition witness; `狂蛮魔尊` for
  the Schur-side interpretation; `巨阳仙尊` may provide the smallest pinned
  Lean theorem for the fixed rational parameter.
- scope: use the current `routeB_compact_combined_schur_partition_ledger.csv`
  obstruction receipt to formalize the candidate `lambda=2` (`theta=1`) on
  every declared row of both eta partitions. Preserve the negative witnesses
  for `lambda=5` and `lambda=3` at eta=5.6; do not delete or overwrite them.
  State the exact finite-row witness, the strict margin lower bounds, the
  per-cell fixed-parameter semantics, and the remaining missing-domain
  coverage premise.
- current diagnostic evidence: eta=2.7 has 256 distinct boxes at
  `lambda=2`, minimum recorded margin `0.16040822007441496`; eta=5.6 has
  321 distinct boxes at `lambda=2`, minimum recorded margin
  `0.04301375542805658`. These are quantized ledger candidates only.
- deliver: a machine-readable witness receipt plus, if possible, a pinned
  theorem stating `1 < lambda_k < lambda_upper_k` and the corresponding
  Schur margin for the declared finite row set; separately identify the
  theorem needed to lift the row witness to complete true-DH coverage.
- forbidden: calling the finite ledger all-domain coverage, replacing the
  fixed lambda by a state-dependent parameter, mixing aggregate and per-cell
  metrics, or promoting this candidate to the registry/formal gate.

### T-P4-029 — true-DH evaluator enclosure and port-map adapter

- status: `open` (newly narrowed source-semantics bottleneck)
- owner: `柳冠一` for the source/evaluator analysis; `臭屁猪` for the typed
  adapter and pinned compile; `封不觉` only for independent receipt review.
- scope: start from the corrected recorded formula
  `R_port(q)=-M_BD(q)*M_DD(mu,q)^(-1)*(M_DB(q)-M0_DB)` with B=(4,5),
  D=(1,2,3,6), `mu=1/1000000`, and prove the smallest useful bridge between
  the exact-real/interval evaluator and deployed `dhport_lib.jl`.
- required distinction: source-text consistency and pointwise regression are
  insufficient. The target is a per-certified-box enclosure for the actual
  Float64 `M,C_fd,G_fd,tau`/solve, or a justified change making exact-real
  evaluation authoritative. Preserve the explicit `M_BD*a_D` term and the
  force-scale `q5/100,q4/200`.
- deliver: a source/provenance receipt, a typed Lean/source adapter target for
  `R*a_B=r_B`, and an explicit list of primitive roundoff or transcendental
  lemmas still needed. If no enclosure is available, return a fail-closed
  obstruction rather than claiming the formula is proved.
- current evidence: `P5_COMPACT_DH_FOURIER_SOURCE_SEMANTICS_AUDIT.md` records
  source-level agreement; `P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md` explicitly
  says Float64 inclusion remains open; local state receipt is
  `SOURCE_FORMULA_PRESENT_CONTROLLER_MISMATCH_AND_FLOAT64_ENCLOSURE_OPEN`.
- forbidden: promoting the formula audit, BigFloat interval output, one-cell
  checks, solver status, or source hash into a kernel-verified theorem or
  registry entry.

### T-P4-030 — port sign propagation into residual/co-state consumers

- status: `open` (critical correction after source audit)
- owner: `红莲魔尊` for the dissipation/co-state algebra; `柳冠一` for source
  notation and `封不觉` for an independent sign-consistency receipt.
- scope: propagate the corrected identity
  `R_port=-M_BD*M_DD(mu)^(-1)*(M_DB-M0_DB)` from the nominal-distal equations
  into every linear `r_B`, co-state, and cross-term consumer. Keep
  `R_gain=-R_port` only in norm-square/Frobenius bounds, where the global sign
  cancels.
- required checks: no theorem may simultaneously state
  `M_DD*v+DeltaM_DB*a_B=0`, `r_B-M_BD*v=0`, and `r_B=R_gain*a_B`; the typed
  adapter must use `R_port*a_B=r_B`. Re-check the sign of any `s_B' r_B`,
  `a_B' r_B`, or Young/S-lemma cross term before exporting a receipt.
- deliver: a minimal coefficient/sign ledger, affected theorem names/files,
  and a pinned Lean or exact-algebra receipt if available. If downstream
  consumers are not yet source-bound, return an explicit obstruction.
- forbidden: treating the sign repair as a new port-norm proof, recomputing
  broad partitions without need, or promoting existing rho² candidates.

### T-P4-031 — reconcile deployed and lifted controller damping semantics

- status: `open` (independent full-descriptor source bottleneck)
- owner: `大爱仙尊` for the algebraic parameter comparison; `臭屁猪` for the
  typed source/config adapter; `封不觉` for an independent provenance receipt.
- scope: reconcile the damping sums before accepting the full lifted descriptor:
  deployed `dhport_lib.jl` uses
  `(Kd+b_fr)=(1.3,1.1,0.95,0.8,0.65,0.5)`, while
  `routeB_fourier_lifted_descriptor_model.jl` currently uses
  `(Kd+Bfr)=(1.8,1.4,0.95,0.5,0.65,0.8)`.
- deliver: a source-of-truth decision, exact parameter receipt, affected
  descriptor/nominal equations, and a regenerated or explicitly rejected
  lifted model. If the lifted model remains an analytic surrogate, mark the
  source binding as open and keep its theorem nodes below registry.
- forbidden: silently copying one vector into the other, calling pointwise
  agreement a source proof, or changing the controller while preserving old
  certificate receipts.

### T-P4-032 — exact-real O1 port coefficient identity

- status: `open` (highest-priority formalizable true-DH leaf)
- owner: `臭屁猪` for the current-pin Lean adapter; `柳冠一` for the typed
  block/source premises; `封不觉` only for independent receipt review.
- scope: compile the minimal exact-real theorem from
  `artifacts/task_routeb_exact_real_coefficient_identity_20260907/REPORT.md`:
  with `M_DD_inv*M_DD=1`, `M_DD*v+DeltaM_DB*a_B=0`, and
  `r_B-M_BD*v=0`, prove
  `R_port*a_B=r_B` for
  `R_port=-M_BD*M_DD_inv*DeltaM_DB`.
- required interface: use column vectors and `Matrix.mulVec`; preserve shapes
  `(B×D)(D×D)(D×B)=B×B`, factor order, and the leading minus sign. Return
  zero-sorry, allowed-axiom, pinned-toolchain, statement-comparator, and
  source-binding receipts if compilation succeeds.
- boundary: this is conditional exact-real algebra only. It does not prove
  Float64 enclosure, DH source equivalence, positivity, coverage, absorption,
  flowpipe, terminal transfer, or registry admission.
- coordinator artifact: `artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean`
  is a no-`sorry`/no-`admit` candidate target, still explicitly uncompiled;
  remote Lean agents may compile and repair it, but file presence is not a
  kernel receipt.
- coordinator repair snapshot (2026-09-07): the candidate now includes an
  explicit `Mathlib.Tactic.Linarith` import and `Matrix.mul_assoc` in the
  `hB_left` normalization. Current candidate hash is recorded in
  `review-T-P4-032-repair-20260907.md`; remote compilation remains required.
- forbidden: using `vecMul` in place of `mulVec`, hiding a backslash/solver call
  inside the inverse premise, or promoting an interface draft.

#### T-P4-032 remote compile dispatch packet (2026-09-07)

- candidate: `artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean`
- candidate SHA-256: `403C41C6F325E906A9D3555B6886D1371DFA2D84826ABCC7BF83C12E21293BFB`
- theorem: `routeB_port_identity`
- required repair already applied: explicit `Mathlib.Tactic.Linarith` import and
  `Matrix.mul_assoc` in `hB_left` normalization.
- remote agent must return pinned Lean/Lake identity, compile exit/output,
  `#print axioms`, exact statement comparator result, and source hash. Any
  failure becomes a new immutable repair review; it must not overwrite the
  prior uncompiled receipt or promote the candidate automatically.

### T-P4-033 — regularizer semantics bridge O0

- status: `open` (independent evaluator prerequisite)
- owner: `柳冠一` for the exact/rounded semantic contract; `臭屁猪` for a
  typed adapter if a Lean sidecar is needed; `封不觉` for independent review.
- scope: bind the deployed Float64 `MASS_REGULARIZER=1e-6` to the exact model
  `mu=1/1000000` by an explicit IEEE-754 outward inclusion, or formally select
  exact-real evaluation as authoritative. Carry the same mu through M_mu,
  M_DD, and R_port.
- boundary: the decimal text match is not exact equality; this leaf cannot
  close O1/O2 or enter registry by itself.
- coordinator implementation (2026-09-07):
  `src/percolation_workflow/routeb_regularizer_semantics.py` and
  `docs/routeb-p4-o0-regularizer-semantics-bridge.md` now expose the scalar,
  common-base matrix/block, and conditional resolvent layers. The API rejects
  implicit Python floats and remains non-registry evidence.
- coordinator finding (2026-09-07, T-P4-033): scalar `delta` is not the remaining
  mathematical bottleneck. O0-R1 needs common-base equality or a quantitative
  `epsilon_A` plus exact D-block inverse bound; O0-R2 needs a weighted port-metric
  conversion; O0-R3 must consume a baseline `rho_r` with a strict remaining
  Schur/Young margin. Positivity of the regularizer alone is insufficient, and
  the review is recorded by `scripts/record_routeb_o0_math_review.py`.
- coordinator finding (2026-09-07, T-P4-033 O0-R3): no consumable same-key physical
  `(rho_r, remaining Schur margin)` pair exists at state rev 500. The resolved-cell
  port row stores only unverified `rho_F^2`; the physical Schur ledger lacks same-domain
  `A>mu` and coupling receipts; the downstream adapter lacks typed `R_port*a_B=r_B`.
  Intake is `scripts/record_routeb_o0_r3_review.py`; this is a preserved obstruction,
  not an O0 closure.
- forbidden: replacing the Float64 literal with a rational silently or using
  BigFloat pointwise agreement as a rounding proof.

### T-P4-034 — deployed Float64 evaluator enclosure O2

- status: `open` (larger source-semantics leaf)
- owner: `柳冠一` for interval/roundoff decomposition; `红莲魔尊` for the
  residual/energy consumption boundary; `封不觉` for independent verification.
- scope: decompose the per-certified-box enclosure of actual
  `dhport_lib.jl` Float64 `M`, central-FD `C/G`, `tau`, and linear solve into
  libm/trigonometric rounding, finite operation DAG rounding, FD-shift,
  regularizer conversion, and solve-conditioning leaves.
- required evidence: every box must be covered; BigFloat or pointwise
  regression is only guidance. Keep source hash, operation order, rounding
  mode, and unresolved primitive lemmas in the receipt.
- boundary: O2 binds the deployment evaluator but does not itself prove
  residual absorption or flowpipe closure.
- forbidden: declaring O2 closed from existing interval candidates, sampled
  maxima, solver `OPTIMAL`, or a stale source hash.
- coordinator finding (2026-09-07): the deployed `1e-5` step is exactly
  `5902958103587057/590295810358705651712`, which is strictly above the exact
  model `1/100000` by
  `1509/1844674407370955161600000`. The scalar seam is recorded, but endpoint
  propagation and the `2h` division error remain open.
- coordinator finding (2026-09-07): deployed `pi`/`pi/2` are now recorded as
  binary64 dyadics inside explicit rational enclosures (`333/106 < pi < 355/113`);
  this is only a scalar offset seam. Per-angle `sin`/`cos` libm error and the
  actual operation schedule remain open.
- coordinator finding (2026-09-07): the existing order-12 exact rational Taylor
  artifact supplies two leaves for `sin(1/100000)` and `cos(1/100000)` without
  floating-point trig. It is now attached as advisory O2 evidence; it does not
  bind deployed libm results or arbitrary DH-angle boxes.
- coordinator finding (2026-09-07): the external P3 DH trig-chain artifact is
  now attached to O2. It is a 12-row exact-real rational interval contract for
  six links and theta/alpha atoms, conditional on the local q-box assignment.
  It closes phase/center bookkeeping only. Float64 argument formation, libm
  sin/cos, finite-DAG propagation, and per-box composition remain explicit open
  leaves; no registry or formal-gate transition is allowed.

### T-P4-035 — true-DH force-descriptor block projection seam

- status: `open` (source-bound math prerequisite for P4)
- owner: `大爱仙尊` for the exact block algebra; `柳冠一` for the typed
  source/config adapter; `封不觉` for an independent sign and provenance
  receipt.
- scope: derive the smallest conditional theorem that connects the deployed
  force descriptor to the Route-B block equation on `B=(4,5)` and
  `D=(1,2,3,6)`. State explicitly which terms are `M_BD*a_D`, which terms
  are the force-scale contributions `q5/100` and `q4/200`, and which
  quantities are merely analytic-lifted surrogates. Produce a typed
  source-binding interface that can feed O1 without assuming the current
  lifted model is canonical.
- required evidence: exact index/order ledger, source file/hash, coefficient
  normalization, a sign-consistent `DeltaM_DB` contract, and an explicit
  mismatch obstruction whenever deployed `dhport_lib.jl` and the lifted
  descriptor disagree. If equality is unavailable, return the strongest
  one-sided or conditional statement that remains valid.
- boundary: this seam does not prove Float64 enclosure, positivity,
  coverage, residual absorption, flowpipe, terminal transfer, or registry
  admission; it must remain below O1 parent closure until source binding is
  accepted.
- forbidden: silently importing the historical lifted descriptor, treating
  pointwise or sampled agreement as source equality, changing controller
  parameters without invalidating old receipts, or hiding normalization in an
  untyped solver callback.
- coordinator finding (2026-09-07): the selected canonical deployed and
  lifted files contain no literal/structural `q5/100` or `q4/200` term. The
  lifted nominal rows contain `+q5/20` and `+q4/20`, while deployed `tau`
  contains only the controller channels recorded above. Treat the requested
  scale terms as an explicit unresolved source-contract obstruction until an
  authoritative source/config is identified; do not silently reinterpret
  them as the observed `1/20` coupling.
- coordinator decomposition (2026-09-07): this obstruction is now tracked as
  F0 source selection, F1 controller tau semantics, F2 coefficient
  normalization, F3 true-DH B=(4,5) block projection, and F4 source-bound
  admission. F0/F2/F3/F4 remain open until an authoritative source/config is
  identified; the lifted `1/20` terms are not a substitute.

### T-P4-033 O0-R3 receipt contract (2026-09-07)

- current live result: `NO_CONSUMABLE_SAME_KEY_PHYSICAL_PAIR`
- required intake: `src/percolation_workflow/routeb_o0_r3_receipt.py`
- a future receipt must bind one canonical source/metric/margin key, exact
  rational `rho_r`, `epsilon_R`, `theta`, and remaining margin; explicitly prove
  weighted baseline/perturbation, semantic binding, `R_port*a_B=r_B`, and full
  consumed-cell coverage; then pass the strict post-charge inequality.
- `READY_FOR_COORDINATOR_ADMISSION` remains conditional input only; it cannot
  close O0 or promote the registry without the existing Lean/comparator gates.

### New harvest: O0-R1/R2 exact keyed interface (2026-09-07)

- review: `review-T-P4-033-O0-R1-R2-exact-keyed-bottleneck-codex-20260907.md`
- no physical receipt is available. The next consumable child must bind exact
  `K`, `epsilon_A`, `dB`, `Br`, `Cf`, `dC`, derived `K_f/DeltaK/U_R`, and the
  same-key weighted `rho_r/epsilon_R`; a squared `rho_F^2` candidate is not a
  root witness. `R_port*a_B=r_B` remains a separate physical prerequisite.

### New harvest: O2 exact-real trig child (2026-09-07)

- review: `review-T-P4-036.2-exact-real-child-codex-20260907.md`
- conditional child `EXACT_REAL_TRIG_CELL_CLOSED_CONDITIONALLY` covers only the
  declared 12 exact-real theta/alpha rows. Float64/libm binding, D1/D2/D3
  composition, and all-box coverage remain open; it cannot close O2.

### New harvest: force-scale compositional child (2026-09-07)

- review: `review-T-P4-force-source-child-codex-20260907.md`
- `P4.force_scale_adapter_q45` is the smallest exact algebraic child:
  `diag(1/5,1/10)*(q5/20,q4/20)=(q5/100,q4/200)`. The static checker now
  records this compositional witness separately while keeping deployed `tau`
  equality and true-DH source binding open.

### New harvest: O1 exact port identity chain (2026-09-07)

- review: `review-T-P4-033-O1-next-codex.md`
- the reusable exact-real chain is
  `eliminate_D -> schur_port_action -> routeB_port_identity`; its temporary
  Mathlib probe reportedly compiled with exit 0, no `sorry`/`axiom`, but it is
  not the canonical candidate receipt.
- coordinator intake: `scripts/record_routeb_o1_exact_identity_review.py`.
  The node remains open until determinant-to-left-inverse, true-DH block
  extraction, projected `h_D/h_B`, same-`(mu,q)` inverse binding, and pinned
  candidate/comparator receipts are supplied.

### New harvest: O2 theta2 exact-real child (2026-09-07)

- review: `review-T-P4-036.2-range-reduction-lemma-codex-20260907.md`
- smallest Lean-facing target is one row, `theta2(q)=q-pi/2` for
  `q ∈ [-3/20,3/20]`, with exact reduction `reduced2 q=q`, local sine/cosine
  Taylor bounds, and quarter-turn transport. It is a proof draft, not compiled.
- next action: Lean agent should locate/prove the integral Taylor remainder and
  check the pinned `Real.sin/cos` API; Float64/libm, D1-D3 composition and
  partition coverage remain separate open leaves.

### New harvest: O0 root witnesses and force-scale Lean target (2026-09-07)

- root review: `review-T-P4-033-O0-R1-R2-root-witness-check-codex-20260907.md`.
  Exact arithmetic supplies candidate roots `9195/100000` for `4227/500000`
  and `1859/10000` for `34547/1000000`, with positive slack; no same-key
  `epsilon_R` or exact inverse receipt exists, so O0 remains blocked.
- force review: `review-T-P4-force-scale-adapter-lean-target-codex-20260907.md`.
  The smallest Lean target is `forceScaleKc_eq_rhoKc` (optionally the source
  literal bridge and quadratic budget); it is pending fresh pinned compile and
  axioms receipt, and never proves deployed `tau` equivalence.
- the O0-R1/R2 review now also carries a three-layer Lean target:
  exact scalar `K_f/DeltaK`, three-term norm inequality from an explicit
  expansion, then keyed `U_R` adapter. The target deliberately keeps
  `h_expand`, norm compatibility, and source/state joins as premises.

### New harvest: O0 zero-shift perturbation reduction (2026-09-07)

- review: `review-T-P4-033-O0-R1-R2-perturbation-map-obstruction-codex-20260907.md`
- if the same-key receipt proves `dB=dC=0`, the exact three-term bound reduces
  to `Br*Cf*delta*K^2/(1-delta*K)`, then to weighted `epsilon_R` by the same
  metric root `s`. The new helper
  `derive_routeb_zero_shift_weighted_perturbation` implements only this scalar
  reduction and remains fail-closed until exact `K`, `Br`, `Cf`, metric, and
  zero-shift proof flags are supplied.
- coordinator intake: `scripts/record_routeb_o0_perturbation_review.py`; it
  records this reduction and obstruction in the O0 node without consuming the
  candidate ledger.

### New harvest: O1 determinant-to-left-inverse adapter (2026-09-07)

- review: `review-T-P4-033-O1-det-left-inverse-adapter-codex-20260907.md`
- pinned Mathlib exposes `Matrix.nonsing_inv_mul`, so
  `det(M_DD45) != 0` can produce the canonical inverse identity. If the
  candidate keeps an arbitrary `M_DD_inv`, it additionally needs the exact
  same-object definition `M_DD_inv = (M_DD45 M)⁻¹`.
- coordinator intake: `scripts/record_routeb_o1_left_inverse_review.py`.
  State records the adapter as conditionally compiled but open until the
  `(mu,q)`, block projection, and inverse-definition bindings are supplied.

### New harvest: O1 typed binding refinement (2026-09-07)

- review: `review-T-P4-033-O1-binding-followup-2-codex-20260907.md`
- admissible paths are exactly either (A) `h_MDD_def + h_inv_def + hdet`, or
  (B) `h_MDD_def + direct exact h_left`. Both require identical source/state,
  `mu`, `q`, and `Didx=(1,2,3,6)` order; a determinant or hash alone is not
  enough.
- coordinator intake: `scripts/record_routeb_o1_binding_followup2.py`;
  state keeps `M_DD_left_inverse_witness=OPEN`.

### New harvest: force-scale pinned compile receipt (2026-09-07)

- receipt: `examples/routeb_b45_5_residual_decomposition_lean/COMPILE_RECEIPT_forceScaleKc_20260907.md`
- coordinator intake: `scripts/record_routeb_force_scale_compile_receipt.py`.
  `forceScaleKc_eq_rhoKc` is now recorded as
  `COMPILED_CANDIDATE_SOURCE_COMPARATOR_PENDING` with fresh Lean/Mathlib pin,
  compile exit 0, theorem-check exit 0, and standard axioms only.
- source binding, statement comparator, Float64/deployed-`tau` semantics and
  registry promotion remain explicitly open.

### New harvest: O0 exact K/Br/Cf obstruction (2026-09-07)

- review: `review-T-P4-033-O0-R1-R2-same-key-K-Br-Cf-obstruction-codex-20260907.md`
- the remaining O0 reduction inputs are independently absent: exact-real
  authoritative `K`, exact `Br = ||M_BD,r||` upper bound, and exact
  `Cf = ||DeltaM_DB,f||` upper bound. Existing zero-shift facts do not provide
  either norm magnitude, and artifact hashes do not prove same-key binding.
- coordinator intake: `scripts/record_routeb_o0_exact_bounds_obstruction.py`;
  state remains fail-closed and the next useful task is to produce this exact
  keyed tuple, not to recompute candidate roots.

## Handoff format

Use a filename such as `review-<task-id>-<agent>-<timestamp>.md` and begin it
with:

```yaml
kind: review_result
task_id: T-P3-001
source_agent: <agent-id>
created_at: <ISO-8601>
integration_status: pending
```

Then record the inspected paths/commit, exact evidence and hashes, proposed
integration, and unresolved blockers. The original result remains immutable
after integration; corrections should be a new result file.

### T-P4-036 — DH Float64 angle/trig binding leaf

- status: `open` (highest-value remaining O2 trig leaf)
- owner: `臭屁猪` for typed interface and compile-side repair hints; `古月方源`
  for exact interval/range-reduction mathematics; `封不觉` for independent
  source/hash/provenance review.
- scope: turn the P3 exact-real DH theta/alpha rows into a fail-closed interface
  for the deployed Julia `Float64` path. Separate (i) `pi/2` and angle-formation
  rounding, (ii) argument range reduction, (iii) libm `sin/cos` enclosure, and
  (iv) finite operation propagation. The P3 CSV is conditional evidence only.
- required output: a report or Lean target with explicit theorem signatures,
  source hashes, per-link/per-atom index order, and status for each leaf. A
  candidate may be `INTERFACE_DRAFT__UNCOMPILED`, but may not be registered or
  used to close O2 without pinned Lean/comparator evidence.
- boundary: no numerical sampling, pointwise Julia output, or Taylor-only
  central-FD leaf can discharge the deployed libm binding. Keep
  `formal_certificate_allowed=false` and `registry_promoted=false`.

#### T-P4-036.4 remote DAG dispatch packet (2026-09-07)

- canonical source hash:
  `AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`
- operation-schedule hash:
  `58209B231ED2BD1662B74B95CBBE5EE206AB1911BFDF03C8AED99C1BFF80C7C1`
- required output: per-box outward propagation receipt for D1/D2/D3, including
  runtime identity, operation schedule, finite/non-NaN/no-overflow assumptions,
  repeated `fk_frames` calls, and coverage. A successful static or numerical
  run is not a Lean/kernel receipt and cannot close O2.
- coordinator intake: submit the JSON receipt to
  `scripts/record_routeb_o2_runtime_receipt.py`; the script binds it to the
  current source/schedule hashes and records `PENDING_REQUIRED_FIELDS`,
  `REJECTED`, or `READY_FOR_COORDINATOR_ADMISSION` without changing O2 status.
### New harvest: force-scale source comparator and O0 exact tuple obstruction (2026-09-07)

- `examples/routeb_b45_5_descriptor_terms_adapter_lean/SOURCE_COMPARATOR_RECEIPT_forceScaleKc_20260907.md`
  is admitted only as a focused anchor receipt. It passes statement/source
  anchors and exact coefficient derivation, but leaves deployed execution binding
  open; it cannot close `P4.true_dh_force_descriptor_semantics` or promote a
  registry theorem.
- `agent_review_inbox/receipt-T-P4-033-O0-exact-K-Br-Cf-same-key-obstruction-20260907.json`
  is ingested as a fail-closed obstruction. The next useful O0 task is to find
  one authoritative same-key exact-real tuple `(K, Br, Cf)` with fixed norm and
  B/D orientation, or prove a constructive replacement from the actual source.
- Do not spend the next cycle on broad regression. Prioritize fresh mathematical
  bottleneck work: O0 keyed bounds, O1 typed inverse binding, O2 exact-real
  coverage/transport, and force-scale deployed witness binding.
### O2 sidecar hash drift guard (2026-09-07)

- The theta2 exact-real intake now records a stale source/olean pair as
  `REJECTED_STALE_SOURCE_OR_OLEAN_HASH` instead of raising an untracked failure.
- Re-run admission only after the agent produces a fresh pinned compile receipt
  whose source and OLean hashes match the current sidecar; the mathematical
  child remains conditional and does not close O2.
### New harvest: O1 typed binding and force source contract (2026-09-07)

- O1 may now consume the typed compile candidate only as an adapter artifact;
  it still needs an OLean/canonical receipt plus same-key `M_DD`/`M_DD_inv`
  source binding. Do not close `M_DD_left_inverse_witness` from the compile claim.
- The force source contract has a zero-state witness but no general-state B-row
  export. The next concrete task is to export `q_B,v_B,w,Cdq_B,Gq_B,G0_B,tau_B,
  rhs_B,a_B,a_D,Mq_BB,Mq_BD` and both residual vectors under one hash manifest.
### New harvest: O0 exact-Fourier tuple and O2 typed theta2 transport (2026-09-07)

- O0 has a consumable one-cell exact tuple under one source/state/norm key:
  `K=1194377771728717533600000000/18430531027503268060090421`,
  `Br=320646431/2400000000`, `Cf=1929397/4800000000`, with exact
  `epsilon_R`. Use it only for the declared exact-Fourier cell; never widen it
  to deployed Float64 or global coverage without a new binding receipt.
- O2 now has a fresh pinned exact-real/typed-box child with matching source and
  OLean hashes. The next mathematical target is a receipt-to-Lean adapter that
  parses one authoritative leaf's rational bounds, coordinate order, and leaf
  id into `RectBox13`/`InRectBox`, then feeds the existing theta2 transport.
### New harvest: O0 weighted metric adapter audit (2026-09-07)

- The exact-Fourier cell now has a same-key metric lower root `s=1/5`, but the
  submitted adapter's induced-infinity-to-Euclidean statement is missing the
  two-dimensional output factor. Keep its claimed `epsilon_R/s` non-consumable.
- The safe rational fallback is `2*epsilon_R/s`; the preferred next child is a
  Lean proof of the Fin-2 norm conversion or a direct induced-2 port receipt.
  Schur margin remains untouched until the weighted baseline, perturbation, and
  strict margin are all keyed and proved.
### O0 norm-conversion API hardening (2026-09-07)

- Use `convert_routeb_infinity_port_bound_to_weighted_l2` for any adapter that
  starts with an induced-infinity port bound. It requires explicit proofs for
  both the output norm factor and metric lower bound, and preserves same-key
  checking.
- The exact-Fourier weighted receipt remains a conditional metric child. Its
  claimed bound is not consumable until the missing norm theorem is supplied;
  the rational safe candidate is `2U/s`.
### New harvest: corrected O0 weighted child and O2 leaf adapter (2026-09-07)

- The corrected O0 output-2 norm receipt is consumable only as a conditional
  one-cell weighted child. It explicitly uses rational factor `2` and exact
  `epsilon_R_2_weighted=2U/s`; keep Schur margin and global Route-B gates open.
- The O2 `cell_id=1` receipt-to-Lean adapter is compiled and hash-bound. The next
  task is to supply the actual `InRectBox` witness from an authoritative leaf
  record and then a parent/sibling coverage join; do not treat parsing alone as
  coverage closure.
### O0 Fin 2 norm theorem candidate (2026-09-07)

- `examples/local_fkg/Fin2NormConversionCandidate.lean` is the next exact
  mathematical child. It proves the safe rational output factor 2 and the
  weighted composition, but remains uncompiled until a pinned receipt exists.
- After receipt, feed the theorem as the explicit `output_norm_conversion_proven`
  premise; keep source/runtime binding, global coverage, and Schur consumption
  independent.
### New harvest: factor-2 weighted receipt and O2 generated adapter (2026-09-07)

### T-P4-KC-COORDINATE-ADAPTER — force exporter intake (2026-09-07)

### T-P4-033-O1 — same-key exact M_DD source binding (2026-09-07)

- 已固化为 `OPEN_TYPED_SOURCE_BINDING_PATH_A_OR_B`：只接受 Path A
  (`h_MDD_def + h_inv_def + hdet`) 或 Path B (`h_MDD_def + h_left`)。
- 必须由同一 `(mu,q,source,state)` 导出 exact
  `M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ`，并保留
  `D=(1,2,3,6)` / zero-based `[0,1,2,5]`。
- 当前不要再重复 determinant/静态审计；优先让 agent 生成 typed source
  receipt，或证明该 exact source surface 在 deployed evaluator 中不存在。

### T-P4-KC-COORDINATE-ADAPTER — force exporter intake details (2026-09-07)

- 已完成：把 general-state force exporter 的严格接收规范登记为
  `PENDING_JULIA_EXECUTION` gate。
- 执行 agent 必须提交同一 exporter/deployed source hash、完整 16-row CSV、
  receipt、stdout/stderr/exit code，并通过 E1/E2 `1e-12` residual gate。
- 当前瓶颈：等待 Julia agent 运行 fresh exporter；本机不运行 Julia。
- 禁止：旧 CSV、只含 residual 的缩减 schema、把 runtime consistency 升级为
  tau 等价/Lean theorem/coverage/registry。

### T-P4-033-O0-R2 — Fin 2 norm conversion compile receipt (2026-09-07)

- The O0 weighted child now has a corrected exact-rational output-2 norm factor
  and is accepted by the coordinator math API. Its one-cell/source-key scope,
  no-Schur-consumption boundary, and no-registry status remain mandatory.
- The O2 generated adapter is a compiled single-leaf transport artifact. It
  still needs an authoritative `InRectBox` witness and coverage join; parsing a
  candidate JSON is not a proof of global partition membership.

- pinned Lean 4.32.0 source/olean/print receipt 已通过 hash、statement
  comparator 和 axiom/sorry/admit intake，登记为
  `COMPILED_CONDITIONAL_FIN2_OUTPUT_NORM_CONVERSION`；它不关闭 source
  binding、Schur margin、global coverage 或 registry。

### T-P4-036.2 — authoritative endpoint witness (2026-09-07)

- leaf-1 handoff 已有 schema、exact rational lower-corner witness、source
  receipt hash、Lean source/olean hash 与 pinned compile exit 0，登记为
  `COMPILED_ENDPOINT_PROVENANCE_ONLY`。
- 可消费内容仅是 endpoint → `RectBox13` → `InRectBox`，以及带
  `BoxSubset`/`CoverageJoin2` premise 的 typed transport；仍缺
  source-bound dynamic leaf、trajectory membership、parent/sibling records
  和全域 coverage，不得关闭 O2。

### T-P4-033-O1 — exact source export obstruction (2026-09-07)

- 当前 `debug_11_dhport.jl` 与 `debug_12n_symM.jl` 都不能提供同键 exact
  `Matrix (Fin 6) (Fin 6) ℝ` / `M_DD45_at`；不能继续用 q=0 probe、Float64
  inverse 或 determinant 替代 source receipt。
- 下一步只接受真实 `source_key/state_key/mu/q/block_order` typed export，
  然后走 Path A 或 Path B；该 obstruction 已登记，O1 不关闭。

### T-P4-033-O1 — obstruction v2 minimal export (2026-09-07)

- 已将 O1 缺口压缩为单一 `h_MDD_def` projection identity，加上同键
  `source_key/state_key/mu/q`、固定 D 顺序和 `4×4` shape。
- 不再重复 q=0、Float64 inverse 或 symbolic probe；下一步必须是真实 exact
  typed evaluator export，或者明确证明 deployed source 无法提供该对象。

### T-P4-KC-COORDINATE-ADAPTER — force runner (2026-09-07)

- fresh runner 已入库：Julia/Python 不可用时只返回 pending，已有输出目录不
  覆盖，成功运行后必须调用完整 schema/residual verifier。
- 当前仍无 runtime CSV/receipt；不要把 runner 存在升级为 source-binding PASS。

### T-P4-036.2 — parent/sibling authority stop (2026-09-07)

- 当前 leaf-1 只有 endpoint provenance；local payload 没有 parent/sibling
  endpoint，拓扑 receipt 仍 `INCOMPLETE` 且 `coverage_complete=false`。
- 暂停重复编译与泛扫描；下一步只接受 source/hash-bound parent/sibling
  records、child-to-parent inequalities 和 coverage join linkage。

### T-P4-033-O0-R2/R3 — strict-margin frontier (2026-09-07)

- Fin2 factor-2 与 exact-Fourier weighted perturbation 已在标量接口组合，
  但 R3 仍缺同键 weighted baseline `rho_r`、正剩余 margin `m_r`、固定
  `theta` 和严格 `leftover > 0`。
- 下一步优先寻找真实 baseline receipt 或给出精确 obstruction；禁止消费
  未绑定的 `rho_F²`、旧 Float64 ledger 或未证明的 candidate margin。

### Workflow hardening — strict Schur leftover (2026-09-07)

- 物理/finite-horizon consumer 必须调用 `consume_routeb_strict_schur_margin`；
  `leftover=0` 会返回 `OPEN_SCHUR_MARGIN_NOT_STRICT`。
- legacy `consume_routeb_schur_margin` 保留用于非严格算术记账，不得作为最终
  admission 的充分条件。新增聚焦测试后为 `28 passed`。

### T-P4-036.2 — GCN candidate authority stop (2026-09-07)

- GCN-F1/F2 的 hash-bound candidate pair 不能作为 O2 theta2 leaf-1 的
  authoritative parent/sibling：namespace、维度和 q2 区间均不匹配，且
  `source_interval_membership_proved=false`、`coverage=false`。
- 保持 `BLOCKED_AUTHORITY_NOT_ADMISSIBLE` / `ENDPOINT_PROVENANCE_ONLY`；
  不实例化 `CoverageJoin2`，不重复 leaf-1 Lean 编译。
- 后续只寻找同一 O2 namespace 的 canonical 13D endpoints、child linkage、
  interval membership 与 typed coverage-join receipt。

### T-P4-033-O0-R3 — strict leftover obstruction (2026-09-07)

- 已确认同键 exact-Fourier receipt 不含 `rho_r`、`m_r`、固定 `theta`，
  仅有可组合的 weighted perturbation `epsilon`。
- 严格消费条件为 `m_r > (1+1/theta)*((rho_r+epsilon)^2-rho_r^2)`；
  当前无法判定正负，继续保持 `OPEN_FAIL_CLOSED_STRICT_LEFTOVER_REQUIRED`。
- 派发目标：只寻找带 source/state/metric/orientation 绑定的 baseline、margin、
  theta 三元组及 exact strict arithmetic；禁止重复已完成的 norm conversion。

### T-P4-KC-COORDINATE-ADAPTER — fresh execution obstruction (2026-09-07)

- 当前环境 `julia` 不可用，fresh exporter 未运行、CSV/receipt 不存在；状态
  保持 `PENDING_JULIA_EXECUTION`，不改变 force gate。
- exporter/deployed source hashes 已核对；后续执行 agent 必须生成完整 16-row
  receipt、四个 E1/E2 residual 分量、process exit 0 与双 artifact hash。
- 禁止把 runner 存在、旧 CSV 或本轮 obstruction 升级为 runtime PASS 或 DH
  source equivalence。

### T-P4-KC-COORDINATE-ADAPTER — short GitHub runner handoff (2026-09-07)

- clean GitHub runner 只执行 `run_general_state_force_binding.ps1`，不要直接
  调 exporter；输出目录必须完整上传并保留 verifier/job stdout。
- 入口已 hash-bound；验收要求 16 rows、B/D 顺序、完整 schema、exit 0、四个
  E1/E2 residual 与 CSV/runtime/stdout/stderr hashes。缺任一项保持 pending/rejected。

### T-P4-KC-COORDINATE-ADAPTER — GitHub Actions execution job (2026-09-07)

- 执行 agent 只需在 clean checkout 添加手动 `workflow_dispatch` job，设置
  `DEPLOYED_SOURCE_REPOSITORY` 与 pinned `DEPLOYED_SOURCE_REF`，使用 Julia 1.10。
- job 必须调用现有 runner、上传完整 output 和 job logs；缺 source 变量、hash
  drift、schema/residual/exit failure 均保持 `PENDING_RUNTIME_JULIA` 或 rejected。

### T-P4-O2-BB-TRIPLE-EXPORT — Julia runtime obstruction (2026-09-07)

- 当前没有 Julia，因此不声称 branch exporter syntax/runtime PASS；保持
  `BLOCKED_NO_JULIA_RUNTIME`。
- Julia-capable agent 只运行 parse-only 与显式 triple selector 最小路径，保存
  driver/backup hash、premise hashes、Julia version、stdout/stderr/exit code；
  缺字段或 hash mismatch 不得标记 READY。

### T-P4-036.2 — canonical 13D triple contract implemented (2026-09-07)

- 新 validator 已可消费未来的 `routeb-theta2-canonical-coverage-v1`：只接受
  exact rational 13D endpoints、三方 linkage、split-cover 几何和 hash-bound
  external premises。
- 返回结果明确区分 structural box/split success 与 dynamics/coverage theorem
  未证明；不会由 receipt validator 直接关闭 O2 或 registry。

### Follow-up harvest: O0/O1/O2 obstruction batch (2026-09-07)

- O0：只收同键 strict-margin 三元组与 exact positive leftover；新 receipt
  已确认当前不可判定，不再重复收集 candidate roots。
- O1：只收 exact typed `M_DD45_at M mu q` 与 `h_MDD_def` source inhabitant，
  不再重复 determinant/q=0/Float64 检查。
- O2：只收同一 theta2 namespace 的 canonical 13D parent/sibling records 和
  typed join；GCN-F1/F2 仅作 rejected candidate 对照。

### T-P4-033-O0 — conditional baseline child (2026-09-07)

- 已记录 exact `rho_r`, `theta=1`, `m_r^unit`, `m_f^unit` 的构造与算术检查；
  它依赖额外 `L_base=1` premise，不能消费 Schur margin。
- 下一步只寻找真实同键 baseline coercivity/reserve 或 affine-bias cap，禁止
  用 unit normalization、旧 ledger、`rho_F²` 代替。

### T-P4-033-O1 — source inhabitant search (2026-09-07)

- 当前 exact typed source inhabitant 未找到；必须补 canonical source receipt
  才能实例化既有 Path A/B inverse chain，`M_DD_left_inverse_witness` 保持 open。

### T-P4-033-O0 — coercivity or bias interface (2026-09-07)

- `Br/K/Cf` 只约束 port map；必须补同键 `L_base`/baseline budget，或采用
  `beta_bias` + root / `beta_abs` + additive reserve 的 affine interface。
- `derive_routeb_affine_bias_gain` 已可验证 exact Young composition，但结果仍
  是 conditional；禁止把 bias 合并进 homogeneous `rho_r`，禁止关闭 Schur。

### T-P4-036.2 — real branch triple exporter validation (2026-09-07)

- 真实 branch driver 已增加 opt-in `P3_BB_TRIPLE_CELL_ID` sidecar；必须在
  Julia 环境验证 syntax、shared endpoint orientation、pending external-premise
  obstruction 和 canonical JSON 输出，不运行全量回归。
- O2 只有收到同 namespace canonical triple 与 external membership/join receipt
  后，才能进入 validator；当前仍不得实例化 coverage theorem。

### T-P4-033-O1 — partial exact source export (2026-09-07)

- 当前 Fourier/body export 只能作为 partial source evidence；执行 agent 需生成
  同 key typed `M_exact`、projection、`h_MDD_def` 及 source binding theorem，
  再走 pinned Lean/comparator intake。

### T-P4-KC-COORDINATE-ADAPTER — GitHub workflow landing (2026-09-07)

- force job 尚未出现在 Actions list，必须先落地
  `.github/workflows/force-general-state-export.yml` 并设置 pinned source vars；
  未落地前保持 `BLOCKED_WORKFLOW_NOT_LANDED`。

### T-P4-033-O1 — typed source receipt intake (2026-09-07)

- 本地已加入 fail-closed validator：schema
  `routeb.o1.true_dh_exact_typed_mdd_source.v2`、exact `mu=1/1000000`、
  `M_exact`/projection/index contract、source binding path 与 SHA-256 形状。
- 继续只接收同 key 的真实 `M_exact`、`h_MDD_def` 和
  `h_source_mass` 或 `h_aggregate+h_body`；abstract-only export 仍为
  `CONDITIONAL_TYPED_SOURCE_EXPORT`。
- artifact 子门会重算已声明文件的 SHA-256；仅 hash 文本没有 provenance，缺 path
  保持 pending，内容 mismatch 直接 rejected。
- 最新 comparator 已确认 data-level aggregate exact pass；下一 frontier 固定为
  610-row finite-key 到 real cos/sin lift，以及六个 exact DH body equalities，
  必须以 pinned Lean/source-comparator evidence 收口。
- DAG 已将该 frontier 拆成 7 个独立 OPEN leaves；agent 应认领具体
  `h_aggregate_function_lift` 或 `h_body_1..h_body_6`，并提交 source-bound
  receipt 与编译/比较证据，不要只返回重复的数据级 equality。
- 当前 per-body sidecar 只作为 uncompiled typed starting point；优先把
  `TypedFourierBodyExport.h_body` 从输入字段变成对真实 DH bodyMass 的证明，
  并单独留下 real-function lift 的 pinned receipt。
- O1 的最小下一步已收窄为生成 typed `bodyTraceEvaluator`（保留 body、行列、
  频率和有理系数标签），再分别证明 `h_body_1..h_body_6`；禁止用 CSV hash
  或 `TypedFourierBodyExport` 的 premise field 代替这些证明。
- O2 可直接复用的新接口是 external-premises schema + typed adapter；下一步只
  接受真实 triple 的 `source_interval_membership` 与 `CoverageJoin2` proof inputs，
  不接受 synthetic constructor 或仅 hash-shaped receipt。
- O0 新增独立 child `P4.O0.physical_baseline_factor`；数学 agent 继续攻真实
  source/energy binding，只有这些前提和 strict `m_f>0` receipt 齐备后才可关闭。
- O0 conditional baseline 的 exact ratio checker 已通过；后续只补物理 premise
  binding，不重复 scalar arithmetic。
- O0 binding ledger 已成为 canonical checklist；数学 agent 必须逐项提供
  Fourier-to-real-DH semantic equality、all-q MBB、symmetry、budget identity、
  B_up physical identity 和 exact mu binding，禁止只提交单独数值下界。
- O2 provenance validator 已通过 focused tests；下一步只有真实 triple 文件及
  外部 membership/CoverageJoin2 proof bridge 才能继续，不能把 validator PASS 当
  成 dynamics/Lean theorem。
- O1 body trace evaluator 已生成；Lean agent 现在应把 727-row definition 在
  pinned environment 编译并证明 body 1--6，而不是再生成 CSV 或 abstract target。
- O1 receipt 已保存 generator/Lean/adapter/source CSV hashes；当前只接受远端
  pinned compile receipt 与六个 `h_body_i` proof，不能使用本机环境错误作为证明。

### T-P4-033-O1 — body-2 source/trace split (2026-09-07)

- body-2 已有精确目标和条件组合桥；CSV key checker 已确认目标系数无漂移。
- 继续分别证明 source expansion 与 tagged finite-fold reduction，再组合为
  `h_body_2`；当前 checker PASS 不是 source/Lean proof，不得关闭 leaf。

### T-P4-033-O0 — body-1/2 geometry targets (2026-09-07)

- 可复用的 exact geometry targets 已收割：active Jacobian columns、正交性、
  `sin_sq_add_cos_sq`、对角惯量消元和 body-1/2 trace fold reduction。
- 下一步仍需 pinned Lean agent 把这些 targets 变成 source-bound compiled lemmas；
  symbolic derivation 本身不消费 P-NE 或 strict margin。

### T-P4-036.2 — theta2 authority source gap (2026-09-07)

- 仓库内未发现真实 triple/membership/CoverageJoin2 authority receipt；P3 replay
  不可升级。保持 O2 `NO_REAL_AUTHORITY_SOURCE_FOUND`，等待真实 branch exporter。

### T-FLT-ADVISORY-OVERLAY — current-pin reuse refresh (2026-09-08)

- FLT current-pin spectral/quotient/pairing/calculus sidecars 已按最新 Route-B
  state revision 刷新 advisory overlay；继续保持非权威、不可关闭 parent、不可进
  registry 的边界。
- shadow manifest comparator 仍需先处理 Mathlib checkout 的 O2 未跟踪生成文件；
  任何“clean”结论必须等真实 clean checkout 和 exact source lineage 再接受。

### T-P4-036.2 — theta2 namespace hardening (2026-09-07)

- canonical triple validator 现在要求 exact namespace anchor
  `q2=[-3/20,3/20]`，并检查 parent q2 box subset；现有 exporter 必须补出
  namespace 字段且仍需外部 hash 文件内容绑定。
- Julia-capable agent 只做 parse/minimal selector 与真实 receipt 产出，禁止
  用 synthetic triple 绕过 source membership 或 CoverageJoin2 premise。

### T-P4-033-O1 — body trace structure gate (2026-09-07)

- 已完成本地非 Lean 结构门：冻结 CSV hash、727 行、六 body 分片、标签保留与
  finite fold 均通过；receipt 状态固定为
  `PASS_GENERATED_TYPED_EVALUATOR_FAIL_CLOSED`。
- 继续攻 source-bound `h_body_1..h_body_6` 与 aggregate function lift；不得把
  checker PASS、CSV equality 或 typed premise field 当作 Lean theorem。

### T-P4-036.2 — explicit proof bridge (2026-09-07)

- O2 bridge contract 已加入 external-premises intake，要求 source-bound Lean
  module/hash 和两个显式 proof symbol；下一步只接收真实 membership 与
  `CoverageJoin2` proof，不创建 synthetic proof。

### T-P4-033-O1 — body-3 source/trace split (2026-09-08)

- body-3 exact piecewise target、source geometry target 和 trace-fold target 已
  落盘，当前为 `OPEN_BODY_3_SOURCE_AND_TRACE_PREMISES`。
- 继续证明 slots 0--3、active Jacobian/Gram、body-3 finite fold，再组合
  `h_body_3`；symbolic receipt 不关闭 P-NE。

### T-P4-033-O1 — keyed regrouping interface (2026-09-08)

- 610-row payload 与 727-row body trace 的最小共同 carrier 已明确为
  `FourierKey + CoeffPair`，keywise equality 与 finite-sum orientation 仍 OPEN。
- 下一步实现 source-bound payload/trace lift 和有限和换序 target，不接受单点或
  hash equality 代替全 q function identity。

### T-P4-033-O0 — P-MU exact-real binding (2026-09-08)

- P-MU 已被隔离为 `mu_NE=mu_Fourier=1/1000000`、同 source/state key、
  regularized-minus-unregularized diagonal identity及 B-block propagation。
- 当前只有 target/review，没有 compiled receipt；不得消费 baseline、strict margin
  或 P-NE。

### T-P4-033-O1 — body-3 coefficient freeze (2026-09-08)

- body-3 的 13 个 exact Fourier atoms 已由 checker 冻结并绑定 state；继续攻
  source frame/Jacobian/Gram 展开和 finite trace fold。
- `PASS_EXACT_BODY3_TARGET_COEFFICIENTS_FAIL_CLOSED` 只表示目标与 CSV 一致，
  不能替代 source-bound Lean theorem。

### T-P4-033-O1 — keyed interface structural gate (2026-09-08)

- `KeyedCoeffRow/CoeffPair` interface 已通过无 shortcut 的结构 checker，并绑定到
  O1 state；继续攻 exact payload/trace adapters、keywise equality 和 finite-sum
  orientation proof。
- 当前 gate 只证明接口结构存在，不能关闭 aggregate function lift。

### T-P4-033-O1 — body-5 exact target correction (2026-09-08)

- body-5（zero-based `4`）57-row exact coefficient map 已通过 checker；目标已
  修正为冻结 CSV 的实际 support，q(3) coupling 只保留 `(1,4)/(2,4)` 及转置。
- 下一步攻 body-5 prefix-frame/source Gram 与 q(3) tagged fold；先以 checker
  结果为 gate，任何 source theorem 必须在同一 source/state key 下重新绑定。

### T-P4-033-O1 — body-4 exact target (2026-09-08)

- body-4（zero-based `3`）40-row exact Fourier target 已冻结并通过 checker，
  状态为 `PASS_EXACT_BODY4_TARGET_COEFFICIENTS_FAIL_CLOSED`。
- 下一步只攻 prefix-frame/axis、body-4 Jacobian/Gram source expansion 及 tagged
  trace fold；不把 CSV 一致性当作 Lean proof。

### T-P4-033-O0 — P-MU/P-BUDGET block API (2026-09-08)

- B-block regularizer API 已有 focused receipt，但仍是 conditional exact API。
- 继续寻找并绑定 `H_acc`、Float64 exact decode `H_mu`、以及 `μ=1/1000000`
  的 physical source receipt；在三者齐全前不得关闭 P-BUDGET 或 strict Schur。

### T-P4-033-O1 — body-6 label boundary (2026-09-08)

- 610-row `body=6` bucket 已被判定为 aggregate-shaped，不能当 human body-6
  proof target。下一步寻找独立 body-6 export；在此之前保持 L0–L4 blocked。

### T-P4-033-O1 — orientation generic bridge (2026-09-08)

- generic finite-sum orientation lemma 已落盘，可作为 algebraic bridge；继续
  攻 source-bound adapter/key equality，不把 generic lemma 当数据 theorem。

### T-P4-033-O0 — P-BUDGET physical identity (2026-09-08)

- 继续补 `baseline_budget` 定义、变量角色/normalization、完整 regularized
  `M_BB` source binding 与 disjoint charge ownership；当前仅有 obstruction receipt。

### T-P5-024/025 — exact consumer harvest (2026-09-08)

- P5-024 先走 independent final-agent audit，再考虑 source-independent theorem
  registry；当前只允许作为 conditional compiled candidate。
- P5-025 继续 formalize finite orthant sign reduction，并把 `K_path` 保留为
  typed component matrix；不得以 scalar `ell2_path` 或缺少 path 的 checker
  关闭 P5/P8/M4。

### Coordinator parallel mathematical round (2026-09-07)

These four sidecar tasks are disjoint and are being executed in parallel. They
are local mathematical decomposition work; none may modify the shared O1
adapter or promote a theorem.

| task | scope | required output | boundary |
|---|---|---|---|
| `T-P4-033-O1-body4-gram` | human body-4 source Gram reduction | exact child targets/review | OPEN, no Lean/Lake claim |
| `T-P4-033-O1-body5-fold` | human body-5 source-to-Fourier and q3 fold | sidecar targets/receipt/review | OPEN, no source closure |
| `T-P4-033-O0-Hacc-export` | Julia `H_acc` semantic export contract | evaluator/interval receipt or obstruction | no numerical-to-formal upgrade |
| `T-P4-033-O1-body6-export` | canonical per-body-6 export contract | support receipt and downstream boundary | aggregate bucket is not body-6 proof |

At the next 20-minute harvest, integrate only new immutable results, refresh
the candidate/state provenance, and sync the integrated batch once. Do not
fetch during the intervening local mathematical work.

### Harvested coordinator sidecars (2026-09-07)

- `T-P4-033-O1-body4-gram`: exact SymPy/QQ diagnostic checked 273 scalar
  identities; source Gram Lean targets and receipt are present, but all target
  inhabitants and pinned compilation remain open.
- `T-P4-033-O1-body5-fold`: exact Laurent diagnostic and 57-row/q3 partition
  targets are present; the corrected `(2,3)/(3,2)=0` boundary is recorded, but
  source expansion, tagged permutation, fold and Lean proof remain open.
- `T-P4-033-O0-Hacc-export`: the three semantic layers and the required
  `36/216/216` scalar-DAG output contract are recorded; no same-source export,
  interval cover or runtime-kernel theorem is present.
- `T-P4-033-O1-body6-export`: pre-accumulation body-6 callback replay exits 0,
  with 610 exact rows and 57 distinguishing coefficients versus the aggregate;
  canonical reification and source theorem remain open.

These results are attached to the O1 candidate as conditional metadata only;
the verified registry remains empty and `formal_certificate_allowed=false`.

### Explicit sidecar frontier registration (2026-09-07)

`scripts/register_routeb_sidecar_frontier.py` now materializes the five
harvested mathematical sidecars as real open DAG children, rather than leaving
them only in candidate metadata:

- body-4 source Gram targets;
- body-5 source/trace decomposition;
- body-6 canonical export;
- O0 H_acc semantic export;
- P5-026 feasible-cone/SPN consumer.

The registration is idempotent, checks every artifact hash/path, preserves the
parent nodes as open, and never touches the verified registry. New children
must still receive actual Lean/checker/source receipts before any parent can
close.

### T-P5-026 — feasible-cone SPN consumer (harvested 2026-09-07)

- status: `pending_math_child`; source-independent exact mathematics only;
- result: six feasible cones per channel, 36 product cones, 18 certificates up
  to simultaneous global sign reversal; orthant nonnegativity can use rational
  PSD-plus-entrywise-nonnegative (SPN) witnesses;
- next: formalize cone cover, two-channel lift, orthant quadratic lemma and SPN
  consumer; only then search against a concrete source-bound nonnegative
  `K_path`;
- forbidden: replacing `K_path` by a scalar without comparison, claiming
  source/Jacobian binding, coverage, Lean verification, registry admission or
  P5/P8/M4 closure.

### Coordinator parallel mathematical round (2026-09-07, current)

The coordinator dispatched four disjoint bottleneck tasks after the finite
fixed-lambda correction.  They may add only their named sidecar files; state,
registry, and shared adapters remain coordinator-owned.

| agent lane | assigned bottleneck | write scope | acceptance boundary |
|---|---|---|---|
| Sartre the 6th | body-4 source Jacobian bridge (`Jv/Jw`) | `examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_*.lean` + review | geometry skeleton only until remote Lean receipt; no source binding inferred |
| Poincare the 6th | body-5 Lean API repair (`Perm`/`Finset`/q3 row code) | `examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_*.lean` + review | API repair only; preserve q3 support and source premises |
| Godel the 6th | H_acc source seam (translation/rotation/`M +=`) | `examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_*` + review | source-location/protocol seam only; runtime export remains pending |
| James the 6th | P5 cone index and 36→18 representative map | `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_*` + review | preserve representative/sign/quadrant witnesses; no coverage or `K_path` claim |

Harvest rule: collect completed sidecars roughly every 20 minutes, integrate
fail-closed metadata, refresh the advisory overlay, and synchronize one batch
to GitHub in that window. Between harvests continue local mathematical work;
do not fetch/push merely because an agent has emitted an intermediate file.

### Next disjoint mathematical frontier (queue after current round)

These are queued in dependency order for the next available GitHub-agent
slots.  They are deliberately disjoint from Sartre/Poincare/Godel/James and
must remain mathematical or typed-interface work until the corresponding
source/Lean receipts exist.

| queued bottleneck | target | acceptance boundary |
|---|---|---|
| `T-P4-033-O1-body6-slice` | derive an independently emitted human body-6 Fourier slice and its `sourceBodyMass q 5` seam | the existing 610-row aggregate-shaped bucket is a negative control; no `h_body_6`, coverage, or registry claim |
| `T-P4-fixed-lambda-admissibility` | formalize the exact two-row `lambda=2`, `theta=1` admissibility and margin consumer | declared-ledger theorem only; no source/coverage or parent closure |
| `T-P5-026-Kpath-interface` | derive the minimal componentwise nonnegative `K_path` comparison interface consumed by the six-cone/SPN proof | do not invent or numerically substitute `K_path`; source binding and P8 remain open |
| `T-P3-central-FD-hull` | formalize the exact central-FD-to-derivative-hull algebraic bridge and its remainder contract | source-independent typed bridge only; no deployed Float64, interval coverage, or admission |

### Harvested P5-026/P5-027 (2026-09-07)

- P5-026 remote Lean sidecar is a `compiled_candidate` with a real focused
  Actions receipt, not a local registry theorem. Its remaining frontier is a
  concrete `ConeIndex`/36-to-18 representative object, sign-fixed quadratic
  identity, source-bound nonnegative `K_path`, and P8 domain coverage.
- P5-027 is a source-independent exact-rational scalar fallback bracket. Keep
  it as a conditional comparison candidate; direct componentwise `K_path`
  remains the preferred mathematical route.
- The coordinator has integrated both review families and their processed
  markers. Do not rerun the old broad diagnostics; assign only the remaining
  concrete cone/source/coverage obligations.

### Current local companion harvest

- P5-026 `NEW_exact_geometry_spn.py` is accepted as an exact symbolic/rational
  companion only. Its negative controls are useful for future checker repair,
  but no `K_path` source binding may be inferred from them.
- The fixed-lambda fold now has both a data-contract checker and a separate
  Lean-interface task. Preserve the sparse global box labels discovered in the
  ledger; do not reintroduce a dense `1..N` assumption.

### H_acc occurrence-aware intake harvest

- Einstein's protocol is now the preferred pending schema for future H_acc
  submissions: definition spans identify scalar nodes, occurrence spans identify
  dense array uses, and aliases must preserve node identity plus typed
  coordinates.
- The protocol is structural/semantic intake only. A future real Julia export
  must still supply source bytes, runtime instrumentation, loaded Float64 bits,
  exact six updates, interval partition and independent soundness evidence.
  No current artifact may close H_acc or promote a registry theorem.

### Mathematical round harvested (2026-09-07, local)

- Sartre's body-4 Jacobian bridge is attached to the body-4 proof-attempt child:
  active joint-3 parallel cross-product, inactive columns, source axes/origins/
  COM/displacements, and 86 exact scalar checks; it remains uncompiled.
- Poincare's body-5 API repair is attached to the body-5 trace child: it
  separates List/Perm folds, tuple row-code decoding, and the q3 16-row
  permutation candidate; source/isometry and final body premises remain open.
- James's cone-index sidecar is a new child under the P5 feasible-cone node:
  `P5.componentwise_relative_decay.feasible_cone_spn.cone_index`.  Its focused
  Lean receipt is recorded in the review, but it is not registry promotion.
- Godel's H_acc seam and T-P5-028 moving-frame transport were integrated in
  the preceding harvest; no admission gate was relaxed.

Next available slots should target the queued body-6 slice, fixed-lambda
admissibility, concrete `K_path` comparison interface, and central-FD bridge;
do not repeat the harvested cone-index or API-repair work.

### Local parallel round (2026-09-07 11:20)

The coordinator opened four disjoint local proof lanes with explicit write
scopes: body-6 slice (`01a07ce7-9ea2-7c91-bbcb-1f203bf80e71`), fixed-lambda
admissibility (`01a07ce8-3c04-7190-aefd-726786f3d47d`), P5 `K_path` interface
(`01a07ce7-b566-7740-8b69-101ece07e985`), and P3 central-FD hull
(`01a07ce8-45fb-7c62-8dd2-f4ecc57540c5`).  The two initial Spark launches
failed at the host usage-limit gate and were replaced by `gpt-5.6-luna`;
the failed launches are retained as agent-history context, not mathematical
results: fixed-lambda `01a07ce7-a82f-7212-97af-6824f8b984be` and central-FD
`01a07ce7-bfc3-7cf2-8858-6be4cb31f600` both stopped before execution at the
Spark usage-limit gate.  All four lanes remain forbidden from editing state/registry or
claiming source, coverage, admission, or final closure.

### T-P5-028 DAG decomposition (2026-09-07)

The moving-frame transport child is now split into six independent leaves:
`source_difference`, `common_parameter`, `ramp_fiber_segment`, `uniform_bound`,
`k_eff_update`, and `fiber_obstruction`.  Each leaf inherits the same review
and companion provenance but has its own proof sketch and closure edge.  The
decomposition is advisory/pending until each leaf receives its own typed
proof artifact; it does not make the parent verified or alter the P5 gates.

### T-P5-028 moving-frame transport harvest (2026-09-07)

- The exact block-(4,5) moving-frame difference map is now a separate P5 child:
  `P5.componentwise_relative_decay.moving_frame_parameter_transport`.
- Under a common ramp parameter `c`, the source `w/c` displacement rows are
  exactly zero.  Under a controlled mismatch `|Delta c| <= gamma |Delta z|`,
  the direct component interface is `K_eff = K0 + kappa tensor gamma`.
- This is source-to-math transport only.  Concrete `H`, source/Float64 binding,
  P8 coverage, Lean compilation, and registry admission remain open; the two
  inbox records were integrated as pending metadata only.

### 2026-09-07 — fixed-lambda typed consumer harvest

- 固定 lambda 线新增 `P4.fixed_lambda_two_row_admissibility.typed_consumer` DAG
  leaf，绑定同一个精确 `lambda=2`、`theta=1` 到 PMI/Schur 两行，并显式保留
  分母正性、`lambdaUpper > 2` 与正 margin。
- 该 sidecar 仅是 source-independent 的 Lean 形式接口；review 明确尚未
  Lean/Lake 编译，也没有 source binding、coverage、comparator 或 registry
  证据。父节点仍 open，`formal_certificate_allowed=false`。
- candidate provenance 已同步记录该 typed consumer 的文件哈希和
  `OPEN_UNCOMPILED_FIXED_LAMBDA_TYPED_CONSUMER` 状态；state revision `614`。

### 当前继续推进的数学叶

- body-6：610 行、32 个非空矩阵条目的独立精确有理数 slice，正在补 review
  和 source seam；与 aggregate 仍有 57 个系数差异，不能把 aggregate 当作
  body-6 证明。
- P5 `K_path`：正在检查现有 `pathK = Sum |A| * Hjac * Scoord` 与 18 份
  cone certificate 的类型连接，方向为二次型 gap 比较，不是逐项矩阵序。
- P3 central-FD hull：继续等待独立中心差分组合叶，不扩大到无关回归测试。

### 2026-09-07 — body-6 与 central-FD 采纳为独立 DAG 叶

- body-6 独立 slice 已注册为
  `P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice`：
  610 行、32 个非空条目、23-row 第六列和 57 个 aggregate 差异键均有精确
  数据证据，但 source seam、Lean 编译与 legacy fold 仍 open。
- P3 central-FD 代数接口已注册为
  `P3.central_fd_derivative_hull_composition.algebraic_interface`：保留
  Christoffel 三指标余项、velocity-quadratic power 和四项 telescoping
  contract；machine/source/export 前提仍必须由后续 adapter 提供。
- 两个新叶均为 `OPEN_UNCOMPILED_*`，不影响 registry 或 admission gate；
  registrar 后 state revision `615`。

### 2026-09-07 — second mathematical harvest: coefficient bridge and K_path

- fixed-lambda agent 新增 `NEW_FIXED_LAMBDA_ADMISSIBILITY_COEFFICIENT_BRIDGE20260907.lean`，
  将 `candidateMargin` 与 `lambdaUpper` 的 exact identity、正分母下的严格
  upper iff positive margin，提升到任意有限 `Finset Nat` 与既有 `Fin 2` consumer。
- K_path agent 新增 typed interface，实际复用现有 `pathK`、same-domain
  `ComponentBinding`、36→18 cone-index lift 和 SPN consumer；agent 报告的
  source-bundle 检查为 Lean 4.32.0 exit 0、12 个接口仅标准公理，但这仍是
  conditional interface，不是 concrete K_path/source/coverage/registry 证明。
- 两个结果已注册为新的子叶，O1 candidate provenance 也加入 fixed-lambda
  coefficient bridge 哈希；state revision `617`，registry `0`，admission gate
  继续关闭。

### Local mathematical follow-up round (2026-09-07 11:46)

Four disjoint continuations are active and must not mutate state/registry:

- body-6 (`01a07ce7-9ea2-7c91-bbcb-1f203bf80e71`): endpoint → center →
  `v5=0` → 23-row sixth-column Fourier bridge;
- P5 K_path (`01a07ce7-b566-7740-8b69-101ece07e985`): exact 8-entry
  `pathK ≤ K_cert` comparison contract/checker, without inventing values;
- fixed lambda (`01a07ce8-3c04-7190-aefd-726786f3d47d`): sparse-label,
  one-row-per-box Finset fold reusing the coefficient bridge;
- P3 (`01a07ce8-45fb-7c62-8dd2-f4ecc57540c5`): Fin 6 specialization of the
  derivative-first remainder and velocity-quadratic error consumer.

All four scopes remain exact/typed mathematical work. They may not claim source,
coverage, admission, registry promotion, or local Lean verification.

### 2026-09-07 — P3 Fin-6 consumer harvest

- P3 follow-up 已完成 `NEW_CENTRAL_FD_HULL_FIN6_CONSUMER.lean`：将
  derivative-first `T/R/mu` 专用于六维，给出三项 Christoffel radius、逐分量
  velocity-quadratic bound 与总 power-error consumer。
- 该叶不选择任何具体 `mu`、速度盒或 source 数值，并明确依赖前置 slot
  adapter；review 为 `OPEN_UNCOMPILED_CENTRAL_FD_FIN6_CONSUMER`。
- 已注册到 central-FD algebraic interface，state revision `620`，registry 和
  formal admission 均未改变。

### 2026-09-07 — body-6 step-6 / sparse digest fold harvest

- body-6 step-6 leaf 已注册：末端 DH 列只展开一次，接出 endpoint→center→
  `v5=0`，并将第六列压缩成 23-row 三角 Fourier fold；`SourceAxisDotTarget`、
  全 36-entry Gram/Fourier seam 与零补集仍是明确外部前提。
- fixed-λ sparse digest fold 已注册：任意 `Finset Nat` sparse rows、
  one-row-per-box、非连续 label cardinality、256+321=577 accounting 和
  canonical row encoding digest binding 均被类型化；SHA-256、CSV/source/
  coverage 仍未在 Lean 内证明。
- 两个结果均为 `OPEN_UNCOMPILED_*`，未改变 registry/admission；state revision `621`。

### 2026-09-07 — body-6 axis-seam follow-up

- body-6 agent (`01a07ce7-9ea2-7c91-bbcb-1f203bf80e71`) 已转向
  `SourceAxisDotTarget`：只处理六个 source axis 点积与 `sixthAxisDot q i`
  的 Fin 6/Fin 3 索引接线，不再重复 610 行 Fourier 核对。
- 该任务仍限定为 source-seam proof attempt；不得从 CSV 反推 source，不得
  修改 state/registry/shared scripts，也不得声称本机 Lean 验证。

### 2026-09-07 — K_path exact comparison harvest

- K_path comparison checker 已完成并注册：对输入的 exact rational
  `A/Hjac/Scoord/K_path/K_cert` 重算全部 8 项 `pathK`，再逐项检查
  `K_path ≤ K_cert`，不接受 tolerance、float、范数替代或缺少公式输入。
- 普通模式与 `python -O` 下各 12 组正/负控通过；Lean `RationalBinding` 仍是
  未编译 typed seam，真实 source 表、`ComponentLE` entry equality、SPN/H gap
  和 coverage 仍未提供。
- 已登记为 `...k_path_interface.exact_comparison`，state revision `622`，
  registry=0，formal gate 继续关闭。

### 2026-09-07 — GitHub Lean harvest: P5-027 / P5-028

- T-P5-027 的 `P5NearSharpCenteredGain.lean` 已有 GitHub CI 证据：Lean
  `4.32.0`，focused check exit 0，10 个导出声明仅
  `[propext, Classical.choice, Quot.sound]`，无 `sorryAx`；修正后的常数为
  `2302494677956489/400000000000000`，并保留精确 lower witness。已注册为
  `near_sharp_scalar_fallback.compiled_candidate`，仍等待 source/K_path/P8。
- T-P5-028 的 pinned moving-frame sidecar 已随远端提交进入本地，暂按
  `CLAIMED_LEAN_SIDECAR_PENDING_REVIEW` 登记；不能把 claim 或 sidecar 本身
  当成已审阅 compiled proof。
- 本地 P3 slot adapter 已加入 central-FD algebraic leaf，明确把
  `dM[i,j,k]` 映射为 `T[k,i,j]`，并保持余项 radius 同步置换；state revision
  `619`，registry `0`，formal gate 仍关闭。
-
### 2026-09-07 — 梁智炜 math-bottleneck dispatch 11:56

- body-6 (`01a07ce7-9ea2-7c91-bbcb-1f203bf80e71`)：继续六轴 source 点积到
  `SourceAxisDotTarget` 的 prefix-rotation seam；新文件尚未 review/注册。
- P5 K_path (`01a07ce7-b566-7740-8b69-101ece07e985`)：处理 8 项
  `pathK ≤ K_cert` 到 `ComponentLE`/SPN representative witness 的 Fin
  索引、非负求和与 36→18 重数保持，禁止臆造 concrete source/gain。
- fixed lambda (`01a07ce8-3c04-7190-aefd-726786f3d47d`)：补 sparse 577-row
  fold 的 parent-level 正 margin 推出，保留稀疏 label 与 digest 外部 premise。
- P3 central-FD (`01a07ce8-45fb-7c62-8dd2-f4ecc57540c5`)：补 Fin 6
  velocity-quadratic power-error 的精确求和/权重 seam，保持 source/export/
  coverage 前提显式。

四项均为 disjoint mathematical leaves；agent 不得修改 state、registry 或
共享脚本，也不得宣称本机 Lean 验证。GitHub 同步留到下一个 20 分钟收割窗口。
### 2026-09-07 — 12:00 收割与远端数学整合

- GitHub 新增 T-P5-029：非负 `K` 增量在物理锥坐标中形成 entrywise-nonnegative
  quadratic correction；若不超过旧 SPN 的 `N_C` slack，可复用旧 PSD `S_C`，
  不必重算 LDL。已作为 pending theorem child 登记。
- GitHub 新增 T-P5-030：为两条不同 ramp 参数各自减去 affine particular
  solution 后，relative block 中 `c` 精确消失；在 incremental residual
  envelope 下得到 `Vd < (dc)^2/12` 的 rational tube 条件
  `11424*mu + 137088*nu < 2285`。source/ODE/coverage 仍为显式前提。
- GitHub T-P5-028 的 pinned Lean sidecar review 已收割，保留为
  `compiled_candidate`，不改变 registry/admission。
- 本地 body-6 axis、fixed-λ selected-box parent、P3 weighted power seam 已
  收割并注册；state revision `626`，registry `0`，formal gate 关闭。

远端同步已在本窗口完成：先提交本地审阅文件，再 merge origin/main；未审阅的
K_path `NEW_KPATH_INTERFACE_FinClosure.lean` 仍留在本地未提交，等待 review。
### 2026-09-07 — 12:03 K_path Fin closure 收割

- K_path agent 补齐 `Fin 8 ≃ Fin 2 × Fin 4` 的 row-major typed closure，保留
  8 项 exact rational comparison、real table identity、envelope slack 非负、
  36→18 cone representative 重数与 SPN witness lift。
- 该叶仍是未编译 source-independent skeleton；checker 的 pass 不替代
  `EightComparisons` proof term，也没有 concrete path/source/coverage/registry。
- 已注册为 `...k_path_interface.fin_closure`；state revision `627`，registry `0`，
  `formal_certificate_allowed=false`。
### 2026-09-07 — 12:04 下一轮数学瓶颈派发

- body-6 agent：从六轴 seam 下钻到 5×5 source linear-velocity Gram，处理
  parent frame、active/inactive joint、零项和对称项；不外推 `v5=0`。
- P5 K_path agent：将 T-P5-029 的 `BᵀEA/sym` entrywise correction 与旧
  SPN `N` slack 扣减做成最小 typed proof，不把它误写成 PSD order。
- fixed-λ agent：补两 eta sparse Finset 的 disjoint union/accounting seam，
  证明 256+321=577 与 selected-box positivity 的组合。
- P3 agent：补四层 remainder 到 source-force equality 的 typed linear adapter，
  保持同域、rounding、source/export 前提显式。

四条均由已完成的本地线程复用，继续不等待 GitHub 回执；每条只新增自己的
proof artifact/review，不改 state/registry/shared scripts。
### 2026-09-07 — 12:06 数学叶收割

- fixed-λ 两 eta union：以 `EtaTag × Nat` 隔离局部 row index，在显式跨 eta
  label 不相交前提下保留 one-row-per-box、`256+321=577` 和 selected-box
  正 margin；状态 `OPEN_UNCOMPILED_FIXED_LAMBDA_TWO_ETA_UNION`。
- P3 force adapter：将 machine/lift、central-FD、derivative-hull、export-center
  四层 remainder 在同一 Christoffel contraction 下线性拆分，接到已有 Fin 6
  weighted power consumer；状态 `OPEN_UNCOMPILED_CENTRAL_FD_FORCE_ADAPTER`。
- 两叶均已登记为 pending DAG children；revision `628`，registry `0`，正式
  certificate gate 继续关闭。仅做了 placeholder declaration 静态检查，未运行
  Lean/Lake。
### 2026-09-07 — 12:10–12:11 数学收割

- P5 T-P5-029 已形成 `C=sym(BᵀEA)` 的 typed SPN increment skeleton：严格保留
  cone `u≥0`、entrywise `C≤N`、旧 PSD `S` 不变和 18→36 lift；不推出全局
  PSD/Loewner 单调性。已登记为 `...nonnegative_gain_increment_reuse.typed_skeleton`。
- body-6 5×5 线速度 Gram 已完成小尾块候选：真实 `prevOrigin`/active joint、
  18 个速度分解残差、(3,3)/(4,4)/(3,4) 精确 Gram/质量项；SymPy checker
  通过，Lean 尚未编译，review 待 agent 完成。
- fixed-λ canonical digest composition 已完成：per-eta encoding、union
  concatenation 与外部 union oracle 组成 typed binding，明确不假设 SHA256
  可由两个 hash 直接合成；已登记为 digest composition child。
- P3 unified input 已完成：四层 remainder radius 精确求和、非负性和统一
  weighted-power input；已登记为 `...force_adapter.unified_input`。

当前 state revision `631`，registry `0`，formal gate 仍关闭；这些均是
source-independent/open/uncompiled 候选。
### 2026-09-07 — 12:12 数学收割与继续派发

- P5 T-P5-029 typed skeleton 已登记：`C=sym(BᵀEA)`、cone-domain envelope
  identity、entrywise `C≤N` 扣减、旧 `S` 保留、18→36 lift 和 rank-one
  correction 均保持显式前提。
- P3 unified input 已登记：四层 radius 精确合并为单一 `mu/R` consumer。
- fixed-λ canonical digest composition 已登记：union digest 需要外部 oracle
  和 encoding equality，明确不假设 hash 可代数合成。
- body-6 VGRAM 新叶完成定向 SymPy 检查：center/tail origin、18 个分解残差、
  `(3,3)/(4,4)/(3,4)` velocity/mass Gram 全为 exact zero；review 尚待完成。
- 下一步：body-6 继续处理 5×5 前部 Gram；P5 继续 T-P5-030 rational tube；
  fixed-λ 继续 digest composition；P3 继续统一 radius 的 power consumer。

当前 revision `631`，registry `0`，formal gate 关闭；GitHub 上次同步为
`ffb3690`，本地数学提交保留到下一个 20 分钟窗口统一推送。
### 2026-09-07 — 12:13 body-6 VGRAM 收割

- body-6 新叶拆为 `velocity_offset_and_tail_origins` 与
  `.front_tail_gram`：保留真实 `prevOrigin`/active guard、COM offset
  分解，及零基 `(3,4)` 的非零速度 Gram 与 source mass 2×2 小块。
- exact SymPy 检查通过：18 个速度分解残差、`v₃₃/v₄₄/v₃₄`、angular
  cross 和 mass entries 全部为零余项，`v₄²=49/40000`；没有读取 Fourier CSV。
- 前 3 列 lever arm 与其余 12 个上三角项仍开放，Lean/kernel/source/coverage
  未验证；已登记为 revision `632` 的两个 open children。
### 2026-09-07 — 12:14 P5-030 ISS boundary 收割

- T-P5-030 新增 source-independent `ISSBoundary` 叶：精确验证
  `C0=474733828336525417/5726342542105201000 < 1/12`，并在
  `11424*mu+137088*nu<2285`、`dc²>0` 和 ISS ledger 前提下推出
  `V=dc²/12` 边界导数严格为负。
- 明确不把边界导数升级为 tube invariance；first-exit、ODE continuation、
  residual/source semantics 与 coverage 仍外置。已登记为
  `...incremental_moving_frame_parameter_tube.iss_boundary`，revision `633`。
### 2026-09-07 — 12:17 fixed-λ uniform feasibility 收割

- 新增 finite sparse-union feasibility leaf：对每个 union row 定义统一
  `lambda` 的 strict lower/upper 与 positive margin，使用已有正分母 bridge
  把全体 row 的正 margin 提升为一个共享 `lambda=2, theta=1` witness。
- 非空 union、row data、digest/source/coverage 均保持为显式前提；未声称
  577 行覆盖真实 DH 域。状态 `OPEN_UNCOMPILED_FIXED_LAMBDA_UNIFORM_FEASIBILITY`，
  revision `634`。
### 2026-09-07 — 12:20 远端收割

- T-P4-032：收割 typed block/source bridge。固定 `B=(4,5)`、
  `D=(1,2,3,6)` 的 Fin 映射，区分 distal acceleration correction 与物理
  velocity，保留 defect-aware O1 identity 和一次性 force normalization。
  API review 指出 `linarith`/`Matrix.mul_assoc` 修复已应用，但仍待 pinned Lean
  compile；已登记为 `REPAIR_PATCHED_PENDING_LEAN_COMPILE`。
- T-P5-030：收割远端 `P5ParameterTubeGain.lean` sidecar 及 claim，暂登记
  `CLAIMED_LEAN_SIDECAR_PENDING_REVIEW`，未把 sidecar 本身当作 CI/kernel 证据。
- 已运行 inbox integration；state revision `636`，registry `0`，正式 gate 关闭。

本窗口合并并推送 GitHub；下一窗口前只继续本地数学叶和 agent 派发。
### 2026-09-07 — 12:24 收割并重新派发

- 本窗口远端无新 commit，inbox integration 无新增；本地与 GitHub 仍一致。
- K_path 线程已复用到 T-P4-032 的 typed block projection / defect-aware O1
  identity，目标是把 `B=(4,5), D=(1,2,3,6)` 的索引、有限求和分解和
  `e_D/e_B` 缺陷项做成 Lean 数学叶。
- body-6、P5、fixed-λ、P3 线程继续各自的当前独立任务；不重复旧审计。
### 2026-09-07 — 12:26 本地数学轮

- 远端本轮无新提交，未抢占 GitHub 通道；本地继续推进。
- body-6：前三列 `b_i=z_i×(o5-o_i)` 的共同 yaw/local-vector 与真实 source seam。
- P5/K_path：T-P4-032 的 B/D block projection、distal/port defect-aware O1 identity。
- fixed-λ：统一 feasibility 后的 lambda monotonicity。
- P3：unified radius 到 weighted-power budget 的非负单调性。

四条均为互不重复的 typed mathematical leaves；state/registry 继续只由协调者
收割更新，Lean/kernel/source/coverage 边界不放宽。

### 2026-09-07 — 12:32 本地数学轮

- 已登记并保持 fail-closed：P3 unified-radius monotonicity、fixed-λ uniform
  margin budget、T-P4-032 block projection/defects、body-6 first-three lever。
- 新一轮四条独立任务：body-6 前三列与 tail 的混合 Gram；T-P4-032 defect
  norm propagation；fixed-λ `delta=gap*cellLower` 的逐行 lower-bound bridge；
  P3 scalar weighted-power budget seam。
- 只做本地数学推进；等下一次 20 分钟远端收割窗口再同步 GitHub。

### 2026-09-07 — 12:36 追加数学轮

- body-6 与 T-P4-032 继续处理中；前者攻 mixed Gram，后者攻 defect norm
  propagation。
- fixed-λ 与 P3 已完成上一叶，立即转入 strict-margin bridge 与 common-domain
  transport；保持四线程持续占用，避免空等回执。

### 2026-09-07 — 12:40 远端收割窗口

- 合并 GitHub agent 的 T-P5-031：physical incremental gains → square-only
  `mu/nu` envelope；review、companion、claims 和 portable Lean sidecar 已纳入
  pending DAG，source gain table/Float64 semantics/P8 coverage 仍开放。
- 本地新增并登记：body-6 first-three×tail mixed Gram、P3 scalar-cap
  monotonicity、fixed-λ weighted absorption、P4 quadratic residual-load seam。
- 远端同步只在本窗口执行；registry 仍为 0，formal gate 继续关闭。

### 2026-09-07 — 12:43 本地数学轮

- 新派发四个独立叶：body-6 前三列自 Gram；P4 entrywise quadratic upper
  bound；fixed-λ 正系数严格总吸收；P3 Fin6 cap-max 压缩。
- 本窗口已推送完毕；下一轮 20 分钟前只在本地推进，避免与 GitHub agent 抢通道。

### 2026-09-07 — 12:47 本地数学轮

- 已收割并登记 P3 capMax minimality/witness equivalence 与 P4 entrywise-to-
  quadratic upper bound。
- body-6 self3、P4 quadratic source instantiation、fixed-λ strict total、P3
  capMax 后续任务继续并行；未触发新的远端同步。

### 2026-09-07 — 12:50 本地数学轮

- 收割并登记 body-6 first-three self Gram、P3 capMax minimality、P4
  entrywise quadratic upper bound、fixed-λ eta partition。
- 继续运行 body-6/P4/P3/fixed-λ 四条新 frontier；GitHub 保持静默至下一窗口。

### 2026-09-07 — 12:52 本地数学轮

- fixed-λ 已转入 eta 分区 strict-total absorption；P3 已转入 capMax budget
  取等条件。body-6 加权 mixed Gram 与 P4 entrywise quadratic 继续运行。
- 暂不访问远端；下一次收割窗口再处理 GitHub agent 的新 review/claim。

### 2026-09-07 — 12:53 本地数学轮

- P4/K-path 空闲线程已转入 block Schur 消元 identity；保留左逆和 defect
  前提，目标是把 projection 直接接到 Schur residual。
- 其他三条继续 body-6 加权 Gram、fixed-λ eta strict absorption、P3 capMax
  取等/最小性；GitHub 仍保持静默。

### 2026-09-07 — 12:55 本地数学轮

- 收割 P4 Schur elimination skeleton，已登记为 block-projection-defects 的新 open child；
  明确左逆、矩阵顺序和两种 defect 符号约定，不把 identity 当成 PSD 或误差界。
- body-6 mass/inertia mixed Gram 已生成但等待 REVIEW；下一轮继续收割，不提前登记。
- 三条空闲线重新派发：Schur defect-convention adapter、fixed-λ strict certificate
  export、P3 strict cap-budget transitivity；GitHub 保持静默至 20 分钟窗口。

### 2026-09-07 — 13:00 20 分钟收割窗口

- 本地收割并登记 P3 strict margin bridge、body-6 mass/inertia weighted mixed Gram、
  fixed-λ final strict export；DAG revision 655，registry=0，formal gate 关闭。
- 已发现远端新增 T-P5-032 coercivity sidecar/claim、T-P4-032 quadratic propagation
  claim，以及 T-P5-031 的修订；先合并远端，再运行 review integrator 和 fail-closed
  sidecar registration，避免漏收 GitHub agent 结果。

### 2026-09-07 — 13:02 收割完成

- 远端 merge 后，整合器回收 T-P4-024、T-P5-031 修订；T-P5-032 exact 8/9
  coercivity sidecar 与 T-P4-024 sharp fixed-lambda 数学 review 已登记为 open
  children。T-P4-032 当前仍只有 claim，等待正式 review/sidecar。
- 当前 DAG revision 657，registry=0，formal_certificate_allowed=false；本轮准备
  提交并推送 GitHub，之后恢复本地数学轮。

### 2026-09-07 — 13:03 调整协作节奏

- 用户将远端收割/发布周期从每 20 分钟改为每小时；heartbeat 已更新为
  `FREQ=HOURLY;INTERVAL=1`。
- 每次小时收割集中回收全部新 review/claim，并批量发布更多互不重复的数学瓶颈任务；
  非收割时间继续本地推进，不反复 fetch/push。

### 2026-09-07 — 13:10 小时窗口后续

- 收割 T-P4-032 正式 quadratic defect propagation review，登记为
  `defect_norm_budget.quadratic_load.weighted_three_term`；T-P5-032 与 T-P4-024
  仍保持 pending/open 数学边界。
- 远端发布节奏已改为每小时；本地空闲 body-6 线追加 tail 2x2 质量/惯量加权任务，
  继续数学推进，不等待 GitHub 回执。

### 2026-09-07 — 13:12 本轮收割收尾

- Schur defect-convention adapter REVIEW 已到，已登记为
  `schur_elimination.defect_convention_adapter`；ForceSideDefects/O1Defects 保持
  不同类型，reference 变量和左逆条件均显式保留。
- 本小时批次已合并并推送；下一次远端收割不早于一小时，期间只做本地数学推进。

### 2026-09-07 — 13:16 本地数学轮

- 收割 body-6 tail weighted Gram、P3 radius-load payload、fixed-λ no-division
  ratio/reserve 三个新叶，均已登记为 open/uncompiled，DAG revision 661。
- K-path 正在 formalize P4 weighted-three-term；其他线继续处理下一批独立数学叶；
  本轮不访问远端。

### 2026-09-07 — 13:18 本地批量派发

- body-6 tail weighted Gram、P3 radius-load、fixed-λ no-division 已入 DAG 后，
  继续派发三条新数学线：P4 weighted-three-term、P3 component-radius 到 cap-load
  单调性、fixed-λ finite reserve aggregation；均要求 conditional、fail-closed、
  不重复旧叶。

### 2026-09-07 — 13:22 本地数学轮

- K-path 已产出 P4 weighted-three-term 的 Lean proof-attempt sidecar，已登记为
  `quadratic_load.weighted_three_term.lean_proof_attempt`，revision 662；仍为
  OPEN_UNCOMPILED_P4_WEIGHTED_THREE_TERM_LEAN，未进入 verified registry。
- fixed-λ finite reserve aggregation 与 P3 radius-to-cap-load order consumer 已有
  新文件，先审阅其数学边界，再决定是否追加 child；本轮不做远端同步。

### 2026-09-07 — 13:25 继续本地派发

- body-6 线接收 tail weighted Gram 的 PSD/最小对角下界叶；K-path 接收
  `rho_eff * energy + B_eff` 参数重排叶。
- fixed-λ 线转向“有限非空族中的严格 reserve 聚合”与 parent strict consumer
  adapter；P3 线转向从非负 weight/velocity 构造 assembled-load 非负 witness。
- 四条线均保持数学瓶颈优先；新叶不重复已登记的 Cauchy、total aggregation、
  capMax 或 source/coverage/registry 层。

### 2026-09-07 — 13:31 定向收割

- P3 assembled-load nonnegative witness 已审阅并登记，revision 664；它只由
  `weight[i]≥0` 与 `squaredVelocity[i]≥0` 给出 `Fin 6` load witness。
- fixed-λ strict reserve final bridge 已审阅并登记，revision 665；它要求有限族
  非空及至少一个严格 reserve，并通过显式 total equalities 接入 final consumer。
- body-6 PSD 下界与 P4 relative-plus-additive 参数重排仍在生成 review；不提前登记、
  不把静态检查当成 Lean 验证。

### 2026-09-07 — 13:36 数学叶收割

- body-6 tail PSD/最小对角下界与 K-path relative-plus-additive 接口 review 已到，
  分别登记为 `tail_psd_lower_bound` 与 `relative_additive_interface`，revision 666。
- 前者只证明有序 2×2 tail 子块的二次型/PSD 下界，后者只做 affine square-envelope
  参数重排；二者均未升级为完整矩阵、全域 coverage 或 formal certificate。

### 2026-09-07 — 13:41 下一轮本地派发

- P3 已接收平方速度逐项非负叶，用于把 `squaredVelocity` 外部前提进一步收窄为
  实向量平方非负；不重复 load witness 或 order consumer。
- body-6、K-path、fixed-λ 继续保留独立运行；当前不访问 GitHub，小时收割时再集中
  处理远端 inbox、冲突和发布。

### 2026-09-07 — 13:46 四线再次填充

- fixed-λ：定量 reserve 下界（逐 cell δ 与显式正 witness）；body-6：tail 2×2
  determinant/principal-minor 正性；P3：平方速度非负；K-path：relative/additive
  参数重排。
- 新任务均为相互独立的数学接口，继续避免重复审计、完整回归和过早 Lean 结论。

### 2026-09-07 — 13:50 P3 小叶收割

- P3 `squared_velocity_nonneg` 已通过边界审阅并登记，revision 667；它以
  `sq_nonneg` 消除 assembled-load 的平方速度非负外部前提，但仍要求显式
  assembled-load equality 与 weight 非负。
- 该结果仍未进入 registry；body-6 determinant、fixed-λ quantitative reserve、
  K-path affine interface 继续由各自 agent 推进。

### 2026-09-07 — 14:30 本地收割与流川枫接入

- body-6 tail inverse、fixed-λ two-row/index equivalence、P3 strict-order obstruction
  已完成定向 review 并登记，P4 Schur/PMI absorption 同批登记；DAG revision 672。
- 用户新增 GitHub agent 流川枫，后续每批约三分之一任务交给他；首个任务为
  P4 Schur/PMI absorption 的 Lean/边界检查，现有六人分钟环保持不变。

### 2026-09-07 — 13:55 fixed-λ 定量叶收割

- `quantitative_lower_bound` review 已到并登记，revision 668；它证明
  `0 < Σδ ≤ Σreserve`，并通过显式 total/shared-λ equality 接到 final budget。
- 仍不重复 strict-witness bridge，也不推断 coverage、digest、source 或 Lean
  kernel 结果；body-6 tail minors 与 K-path affine interface 继续等待其自身 review。

### 2026-09-07 — 14:02 更新 GitHub 六人排班

- 当前新发布只使用六人环：柳冠一/古月方源/狂蛮魔尊/红莲魔尊负责数学，
  苏梦辰/巨阳仙尊负责 Lean decomposition、pinned 编译与 repair；分钟槽为
  :00/:10/:20/:30/:40/:50，整体每小时循环。
- 已完成 body-6 tail principal-minor 叶，登记前沿 revision 669；Lean 验证任务
  后续放入两个 Lean 槽，主线程只在小时收割时集中回收和同步。

### 2026-09-07 — 14:10 本地四线数学派发

- body-6：tail 对角逆块与 Schur 作用界；K-path：relative/additive 到 rho<1
  吸收；fixed-λ：aggregate margin 的显式正 slack；P3：一坐标严格 cap-load
  单调性。
- 任务均为数学 proof-attempt，不替代 GitHub :10/:40 的 pinned Lean 验证批次。

### 2026-09-07 — 14:18 定向收割与补派

- fixed-λ aggregate slack、P3 strict component order 已登记，revision 670；前者
  要求显式 `totalReserve+Σδ≤totalMargin`，后者要求某坐标有正 load，均不隐藏关键
  严格性前提。
- fixed-λ 新派 two-row/index equivalence adapter；P3 新派 zero-load/非严格 cap
  obstruction leaf，用于 theorem graph 的负条件记录；body-6/K-path 继续工作。

### 2026-09-07 — 14:38 本地 parent-closure 派发

- body-6：tail inverse 到 typed Schur elimination；K-path：rho_eff≥1 与有限 affine
  bound obstruction；fixed-λ：index transport 缺 premise obstruction；P3：strict
  weighted gap 的定量下界。
- 四项都服务于 parent closure 或 obstruction tracking，保持数学证明优先；GitHub
  Lean receipt 仍按六人环与流川枫比例 lane 另行处理。

### 2026-09-07 — 14:52 parent adapter 收割

- body-6 tail inverse→typed Schur adapter、P4 rho/slack absorption obstruction、
  fixed-λ index transport obstruction 已完成定向 review 并登记，revision 676。
- 负分支明确保留：rho_eff≥1 无正 slack；缺少 index injective/surjective/total
  equality 不能搬运 aggregate；这些记录用于 scheduler 的 obstruction tracking。

### 2026-09-07 — 14:45 P3 定量 gap 收割

- P3 `quantitative_gap` 已完成定向 review 并登记，revision 673；它把整体
  weighted cap-load gap 下界化为一个选中坐标的 `load[j]*(qCap[j]-q[j])`。
- 该叶保留其余项非负与 selected gap 前提，未重复 strict order/obstruction，
也未进入 registry。

### 2026-09-07 — 当前本地数学批次

- body-6：tail inverse → typed Schur elimination 的逐项系数展开；
- P4 true-DH/K-path：rho<1 的无除法收缩接口，并保留 rho≥1、B<0、缺少
  E≥0 时的 obstruction；
- fixed-λ：有限索引 bijection/equiv 与逐点权重保持推出 aggregate equality；
- P3：positive selected load 与 cap-load gap 推出显式 strict capMax/预算 slack。

本批只推进数学结构和 proof-attempt；待定向 review 到达后再登记 DAG。GitHub
发布仍按每小时一次的六人环执行，流川枫承接约三分之一独立任务；本地不做
常规远端同步。

### 2026-09-07 — 本地收割

fixed-λ finite reindex weighted-sum equality 叶已登记 revision 677，保持
`OPEN_UNCOMPILED`；它为 two-row index adapter 提供显式 Finset.sum_bij 接口。
其余 body-6、P4 contraction、P3 slack 三项仍在本地并行处理中。

### 2026-09-07 — 本地收割补充

P4 `DivisionFreeContraction` 和 P3 `FamilyBridge` 已登记 revision 678，
继续保持 `OPEN_UNCOMPILED`。body-6 的 Schur remainder 产物尚缺配套 review，
暂不登记；待其完成后再做一次定向收割。

body-6 Schur remainder review 已到达，现已登记 revision 679；下一步继续寻找
实际 mixed-block source binding 或 residual margin 的独立数学叶，不重复已有
纯代数展开。

### 2026-09-07 — 下一轮本地数学批次

- body-6：mixed-block A/X/Y source-binding contract；
- P4：pointwise rho<1 但无 uniform contraction gap 的反例及 uniform bridge；
- fixed-λ：finite reindex equality 与 final strict slack 的纯代数组合；
- P3：family-to-point specialization 与 capMax strict budget 的 typed consumer。

仍不运行大规模回归；只有 proof-attempt 与定向 review 成对到达后才登记 DAG。

### 2026-09-07 — 本地收割补充

fixed-λ `COMPOSED_REINDEX_SLACK` 和 P3 `FAMILY_SLACK` 已登记 revision 680，
保持 `OPEN_UNCOMPILED`。下一轮优先收割 body-6 mixed-block binding 与 P4
uniform contraction；若只得到缺失字段，则记录 obstruction 而不填入假数据。

body-6 SELF3 mass binding、fixed-λ real final strict consumer、P3 box coverage
已登记 revision 685，均未进入 registry。下一轮继续寻找实际 interval/source
数值绑定与 residual/flowpipe 连接，不把抽象 consumer 当作 Route-B 证书。

补充本地派发：

- fixed-λ：有限 ℚ weighted-sum 的 ℚ→ℝ cast/reindex adapter；
- P3：pointwise positive gap 不推出 global uniform slack 的 exact obstruction，
以及显式 uniform-gap consumer。

P3 interval-enclosure review 已到达并登记 revision 686，保持
`OPEN_UNCOMPILED`；下一步可继续推进实际 interval payload/box source binding，
但不能用采样或 solver receipt 替代 rounding soundness。

P4 `UNIFORM_PARAMETER_BRIDGE` 已成对审阅并登记 revision 684，保持
`OPEN_UNCOMPILED`；它明确要求 total additive 为 `base+biasEff`，并把统一
参数、feedback、coverage 作为显式前提。

两项均要求 proof-attempt + 定向 review，暂不运行大回归或进入 registry。

三叶收割结果：body-6 source block binding、P4 domain-uniform contraction、
fixed-λ rational-to-real finite-sum cast 已登记 revision 681。P3 uniform-gap
叶仍等待独立 review；未配对的草稿继续留在工作区，不进入 DAG。

P3 finite-grid uniform gap 已完成成对 review 并登记 revision 683，状态保持
`OPEN_UNCOMPILED`；有限网格 lower bound 仍不能外推到未覆盖连续域。

P3 uniform-gap review 已到达并登记 revision 682，状态仍为 `OPEN_UNCOMPILED`；
它把全域 uniformity 设为显式输入，保留 pointwise-only 的 exact obstruction。

补派 P3 partition/box coverage bridge：有限区域集合的全域覆盖、逐区域
uniform gap 与全域 strict consumer；明确网格点不足以替代 coverage。要求
proof-attempt + 定向 review，保持 `OPEN_UNCOMPILED`。

### 2026-09-07 — 当前四线派发

- body-6：SELF3/Gram 到前三块 A 的 source binding；
- P4：relative/additive 有效参数到 domain-uniform budget；
- fixed-λ：ℚ→ℝ cast 后的 final strict consumer；
- P3：有限 Finset positive gap 到 uniform lower bound，并记录不能外推连续域。

所有产物必须以 proof-attempt + 定向 review 成对提交；仍保持 fail-closed。

当前新派发：body-6 source Schur margin、P4 residual/PMI margin、fixed-λ
statement comparator boundary、P3 box interval soundness。均要求成对
proof-attempt/review，保持 `OPEN_UNCOMPILED`；不要运行宽回归或同步远端。

fixed-λ exact statement boundary 与 P4 residual margin consumer 已登记
revision 687，继续保持 `OPEN_UNCOMPILED`。下一步优先检查 body-6 source
Schur-margin 叶和真实 interval payload；任何缺少 source/coverage 的结果只
登记为 open obligation。

当前新派发：body-6 uniform remainder margin；P4 SchurMargin→scalar PMI
adapter；fixed-λ comparator receipt admission；P3 receipt→interval certificate。
四项均保持 `OPEN_UNCOMPILED`，等待成对 review 后再进入 DAG。

body-6 `SCHURMARGIN`：补配套 review 后再登记；P3：interval payload/receipt
boundary，显式分离 source、rounding soundness、coverage 与 checker metadata。
两项继续保持未编译、fail-closed。

body-6 `SCHURMARGIN` review 已到达并登记 revision 688，状态保持
`OPEN_UNCOMPILED`；正的 remainder margin、完整 cross-block source 与域覆盖
仍是后续独立 frontier。

P3 interval receipt boundary 已登记 revision 689，保持 `OPEN_UNCOMPILED`；
后续若接入真实 payload，仍需独立 endpoint/rounding/source 证明，不能只凭
receipt metadata 进入 registry。

本轮收割：P3 receipt→数学区间证书 adapter、fixed-λ comparator receipt admission、
P4 BODY6 Schur→scalar PMI adapter 已登记 revision 690，均为
`OPEN_UNCOMPILED`。body-6 uniform remainder margin 已产出 proof-attempt，待配套
review 到达后登记；其无限域 uniform 正 margin 反例继续作为显式阻塞条件。

revision 691 后续派发：body-6 exact source-to-Schur coefficient seam；P4
residual allowance 到 scalar margin 的显式预算 adapter；fixed-λ receipt 的
artifact/hash/statement provenance audit；P3 interval certificate 到连续域
coverage 的 typed consumer。四项要求 proof-attempt + 定向 review，继续不跑
本机 Lean/Lake、不做宽回归、不直接修改 registry。
