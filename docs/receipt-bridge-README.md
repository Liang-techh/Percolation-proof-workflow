# Receipt to frontier outcome bridge

`receipt_to_frontier_outcome(receipt)` is a small pure-function adapter for
scheduler consumers. It reads `receipt["status"]` and returns a new advisory
dictionary for the statuses `validated`, `failed`, `missing`, and
`needs_manual_review`.

The result includes an `outcome`, the original `receipt_status`, and scheduler
flags (`dispatchable` and `requires_manual_review`). `advisory` is always true
and `verified` is always false. A receipt is therefore never promoted to formal
verification, registry admission, `NodeStatus`, or `EvidenceStage` by this
module. Unknown statuses fail closed with `ValueError`.

Example:

```python
from percolation_workflow.receipt_bridge import receipt_to_frontier_outcome

receipt_to_frontier_outcome({"status": "missing"})
# {
#   "schema_version": 1,
#   "outcome": "advisory_missing",
#   "receipt_status": "missing",
#   "advisory": True,
#   "verified": False,
#   "dispatchable": True,
#   "requires_manual_review": False,
# }
```
