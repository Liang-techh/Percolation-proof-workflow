"""Correct the initial source-derived reduction without resetting research history."""
from pathlib import Path
from percolation_workflow.store import StateStore


def correct(state):
    nodes = {node.name: node for node in state.nodes.values()}
    z3 = nodes["BondPercolation.percolation_continuity_Z3"]
    general = nodes["BondPercolation.percolation_continuity"]
    library = nodes["Percolation.Continuity.CSH.percolationContinuity_allDimensions"]
    if library.id not in z3.dependencies:
        return False
    z3.dependencies = [general.id if dep == library.id else dep for dep in z3.dependencies]
    z3.dependencies = list(dict.fromkeys(z3.dependencies))
    z3.proof_sketch = "Specialize BondPercolation.percolation_continuity to d=3; norm_num proves 2 <= 3."
    state.validate()
    state.event("dependency_corrected", node_id=z3.id, old_dependency=library.id,
                new_dependency=general.id, evidence="upstream/formal-math/percolation/Solution.lean: percolation_continuity_Z3")
    return True


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1] / "artifacts/percolation/workflow_state.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    store = StateStore(path)
    state = store.load()
    if correct(state):
        store.save(state)
        print("Corrected Z3 dependency; existing nodes, attempts and registry retained.")
    else:
        print("No correction needed.")
