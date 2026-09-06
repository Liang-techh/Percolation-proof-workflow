from __future__ import annotations

import json
from pathlib import Path

from percolation_workflow.graph import attach_statement_index
from percolation_workflow.statements import index_statements, write_index
from percolation_workflow.store import StateStore


ROOT = Path(__file__).resolve().parents[1]
CHALLENGE = ROOT / "upstream" / "formal-math" / "percolation" / "Challenge.lean"
INDEX = ROOT / "artifacts" / "percolation" / "challenge_statement_index.json"
STATE = ROOT / "artifacts" / "percolation" / "workflow_state.json"


def main() -> None:
    write_index(CHALLENGE, INDEX)
    store = StateStore(STATE)
    state = store.load()
    attached = attach_statement_index(state, index_statements(CHALLENGE))
    state.event("challenge_statement_index_persisted", index=str(INDEX.relative_to(ROOT)), attached=attached)
    state.validate()
    store.save(state)
    print(json.dumps({"attached": attached, "index": str(INDEX), "state": str(STATE)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
