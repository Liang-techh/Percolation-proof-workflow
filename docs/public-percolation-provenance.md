# Public percolation provenance

The available `add-percolation` pull request is [PR #22](https://github.com/anthropics/formal-math/pull/22),
titled `wip: scaffold`. Its body is `placeholder`; GitHub's PR API reports zero commits, zero changed
files, and closure without merge. Its head is `3d3e9f83ac5b0146cf8d8a6ffb633f41e02a4280`, a merge
of the zeta23 layout PR. This is not the percolation revision replayed locally.

The successful [Lean projects run 33177803274](https://github.com/anthropics/formal-math/actions/runs/33177803274)
at that head contains `detect changed projects` and `verify (zeta23)`. The latter includes Lake build
and Palomar comparator steps, but does not verify percolation. A green workflow label alone is
insufficient; the selected project and revision must match the claimed theorem.

The local replay instead pins `795efb86f191735c5481675763537cfb4ff37e55`. Its percolation history
contains five source-addition commits, README and formalization metadata updates, then a summary
document commit. The local Linux acceptance receipt and original logs record successful verification
of that revision's Challenge/Solution targets with both kernels.

This provenance establishes public artifacts and local replay, not access to Anthropic's private
agent prompts or internal orchestration. Prove2Me's public decomposition semantics must therefore be
reconstructed from its published instructions and observed interfaces.

Machine-readable PR observations: `artifacts/percolation/pr22_observation.json`.
Read-only API sources used: `/repos/anthropics/formal-math/pulls/22`,
`/repos/anthropics/formal-math/commits/3d3e9f83ac5b0146cf8d8a6ffb633f41e02a4280`, and
`/repos/anthropics/formal-math/actions/runs/33177803274/jobs?per_page=100`.
