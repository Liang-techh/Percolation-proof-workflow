# Virtual frontier leaves

`math-frontier` now exposes a read-only `virtual_frontier` projection for
child obligations stored inside an open DAG node's metadata contract. This is
used by the Route-B O2 trig/Float64 contract (`o2_trig_binding`) to expose
`T-P4-036.1` through `T-P4-036.4` to coordinators and agents before they are
ready to become independently verified DAG nodes.

The projection is deliberately not a second theorem graph. Each row carries
`is_virtual=true`, `closure_effect=false`, and `registry_effect=false`.
Virtual rows therefore cannot close their parent, promote a registry entry, or
relax the ordinary scheduler obstruction gate. Only leaves attached to a
current actual frontier node are shown; malformed advisory leaves remain
visible with `kind=malformed_virtual_leaf` for audit purposes.

Use:

```powershell
$env:PYTHONPATH='src'
python -m percolation_workflow.cli math-frontier artifacts/routeb_6dof/state.json
```

The JSON result contains the existing `frontier` and `ranked_node_ids` plus
the metadata-only `virtual_frontier` list. A later implementation may promote
a leaf into the real DAG only through an explicit decomposition/admission
operation with its own evidence contract.
