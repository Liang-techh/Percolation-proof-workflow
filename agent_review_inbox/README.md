# Agent review inbox / research roundtable

This directory is the hand-off point for independent agent reviews. The
coordinator identity is **梁智炜**: publish bounded tasks in `task_queue.md`,
collect agent results, and merge only evidence that passes the workflow gates.
It is intentionally operated like a low-frequency research chat group rather
than a synchronous debug console.

The periodic worker pool and the corrected canonical GitHub dispatch roles are
listed in [`agent_roster.md`](agent_roster.md). New GitHub task releases must
follow that role matrix; task ownership and evidence remain durable only after
an inbox result is recorded. Historical review authors are preserved even if a
role label is later corrected.

Agents may add one self-contained `.md` or `.json` review result per finding.
Typed `handoff` and `companion_log` records use the same bounded envelope and
are collected by the periodic pass as provenance metadata; claims and plans
remain non-evidence.
Planning files use the `task_plan` label and are not treated as evidence.
Every `review_result` should include:

- `review_id`, `source_agent`, `created_at`, and the inspected commit/path;
- the exact question or bottleneck inspected;
- evidence, commands/checkers, exit codes, and source hashes;
- proposed integration target (DAG, frontier, receipt, theorem, documentation,
  or code) and the requested action;
- an explicit admission label: `verified`, `compiled_candidate`, `pending`,
  `rejected`, or `architecture_only`.

The 20-minute integration pass reads `review_result`, `handoff`, and
`companion_log` files not marked `integrated`; it ignores `task_plan` and
`task_claim` files. It may update
the authoritative workflow only through the normal state/receipt APIs, and it
must preserve provenance, failed attempts, and unresolved obligations. A review
file is never proof merely because it exists or says `verified`; Lean/kernel,
comparator, source-binding, and domain-coverage gates remain authoritative.

After integration, the pass records the result in the workflow history and
writes a companion marker under `processed/` with the original review hash and
the integration result. Do not delete or rewrite the original review. If a
review requires a material mathematical scope change, leave it `pending` for
explicit user direction.

For a deterministic local pass, run:

```text
python scripts/intake_external_routeb_artifacts.py
python scripts/integrate_agent_reviews.py
```

The external-artifact intake watches the external Route-B
`artifacts/task_*` directories by stable hashes and records only a persistent
catalog event. It does not silently create theorem nodes, copy external
source, or promote compiled artifacts to the verified registry; explicit
review remains required.

The command is idempotent and accepts explicitly mapped Route-B tasks plus
event-only external-reuse catalog reviews. Event-only reviews never create a
Route-B node or registry entry. Unknown tasks are left untouched for
human/agent triage.

The scheduled roundtable also uses `task_queue.md` as planning input: agents
may claim independent mathematical bottlenecks and write one immutable result
file each. The coordinator should avoid duplicate claims and broad regression
runs; focused proof/checker evidence is preferred.
