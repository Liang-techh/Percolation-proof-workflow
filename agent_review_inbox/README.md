# Agent review inbox

This directory is the hand-off point for independent agent reviews.

Agents may add one self-contained `.md` or `.json` review result per finding.
Planning files use the `task_plan` label and are not treated as evidence.
Every `review_result` should include:

- `review_id`, `source_agent`, `created_at`, and the inspected commit/path;
- the exact question or bottleneck inspected;
- evidence, commands/checkers, exit codes, and source hashes;
- proposed integration target (DAG, frontier, receipt, theorem, documentation,
  or code) and the requested action;
- an explicit admission label: `verified`, `compiled_candidate`, `pending`,
  `rejected`, or `architecture_only`.

The hourly integration pass reads only `review_result` files not marked
`integrated`; it ignores `task_plan` files. It may update
the authoritative workflow only through the normal state/receipt APIs, and it
must preserve provenance, failed attempts, and unresolved obligations. A review
file is never proof merely because it exists or says `verified`; Lean/kernel,
comparator, source-binding, and domain-coverage gates remain authoritative.

After integration, the pass records the result in the workflow history and
writes a companion marker under `processed/` with the original review hash and
the integration result. Do not delete or rewrite the original review. If a
review requires a material mathematical scope change, leave it `pending` for
explicit user direction.
