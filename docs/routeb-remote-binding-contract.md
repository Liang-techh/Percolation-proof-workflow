# Route-B remote action contract

The exact `M_BD(0)` projection countermodel shows that a bound depending only
on the current `(q4,q5,v4,v5)` block cannot control `M_BD(q) a_D`.  The
workflow therefore exposes two explicit repair modes for the P4 child:

1. `full_state`: bind `a_D`, the `M_BD` operator, and their remote action on
   the same covered full-state/source snapshot, together with the descriptor
   identity;
2. `d_row_schur`: bind a D-row residual, the regularized `M_DD` inverse, the
   `M_BD` operator, and an exact Schur elimination identity.

`src/percolation_workflow/routeb_remote_contract.py` checks only this typed
shape.  It rejects `block_only_remote_bound` even if other fields are present,
and it never opens `formal_certificate_allowed` or registry eligibility.
The actual inequalities, source binding, coverage, Lean compilation, and
terminal theorem remain separate gates.

When a full-state residual ledger is combined with this contract, use
`audit_routeb_remote_binding_join`. It rejects otherwise-valid receipts whose
state key, source snapshot, or norm convention differs, preventing cross-cell
or cross-source evidence from being silently composed.

The focused Python tests are in `tests/test_routeb_remote_contract.py`.  The
JSON checker is `scripts/check_routeb_remote_contract.py`; local use is a
structural audit only and does not invoke Lean/Lake.
