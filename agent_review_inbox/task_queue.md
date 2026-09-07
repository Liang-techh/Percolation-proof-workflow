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
after the user's schedule change:

| worker label | current bounded focus |
|---|---|
| 柳冠一 | Inbox 去重与 adapter/interface 结果回收 |
| 苏梦辰 | Inbox 协作与 theorem-decomposition 结果整理 |
| 幽魂魔尊 | 独立数学突破：P4 force/Schur bottleneck |
| 大爱仙尊 | 独立数学突破：P3 true-DH coercivity bottleneck |
| 古月方源 | Inbox 协作与 P8 主路线协调 |
| Percolation 最终验证 | 唯一 admission、axiom、provenance 与最终 gate |
| 巨阳仙尊 | Lean sidecar 编译、typed interface 与 repair |
| 狂蛮魔尊 | Inbox 协作与不等式/反例难点协调 |
| 红莲魔尊 | Inbox 协作与能量/Lyapunov 难点协调 |

## Dispatch and synchronization throttle

The coordinator may integrate inbox results locally on the 20-minute harvest
cycle, but must not routinely fetch, merge, or push to GitHub. Remote sync is
reserved for a major mathematical breakthrough, a verified architecture
milestone, or an explicit user request, to avoid competing with scheduled
GitHub agents for the push channel.

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

- status: `open` (released for the next mathematical round)
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

- status: `open` (released after `T-P5-005` harvest)
- owner: `苏梦辰`
- source: `review-T-P5-005-kuangmanmozun-20260906T2307.md`,
  `examples/routeb_supply_core/RouteBSupplyCore.lean`;
- scope: formalize the finite-sum component-wise closure
  `|r_i|≤rho_i|v_i|`, `0≤rho_i<d_i` implies retained diagonal damping;
- deliver: source-independent theorem decomposition and a portable Lean
  sidecar if practical, with exact positivity premises;
- forbidden: deriving the premise from current FD samples/envelopes or closing
  the physical P5/M4 node.

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

- status: `reviewed_pending` (math result from 古月方源; candidate sidecar
  prepared; pinned Lean verification delegated to 臭屁猪/validation lane)
- scope: formalize the scalar tail equations `w'=c`, `c'=0`, `w(0)=0` and
  derive `c(t)=c0`, `w(t)=c0*t`, plus the `T=1` terminal transfer;
- deliver: minimal Lean child or a precise interval-API blocker, with the
  first-12 explicit-time projection kept separate from source binding;
- forbidden: claiming ODE existence, `[0,1]` flowpipe coverage, deployed
  13-state semantic binding, or P8/M4 admission from this child alone.

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

- status: `open` (released for the unique validation lane)
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

- status: `open` (released from the M4-006 mathematical review)
- owner: `苏梦辰`
- source: `review-T-M4-006-daai-xianzun-20260906T2346.md`;
- scope: formalize only the division-free arithmetic implications
  `D_base+D_tail <= 1401/625` from `D_tail<=rho_bar/160000` and the exact
  old-gate corollary `rho_bar<=16`; keep the integral/ramp lemma separate;
- deliver: pinned GitHub Lean sidecar or precise compile obstruction, with
  exact rational constants and no hidden source assumptions;
- forbidden: changing `D_gate`, proving physical `rho_bar`, or closing
  residual absorption/flowpipe/M4 from arithmetic alone.

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
