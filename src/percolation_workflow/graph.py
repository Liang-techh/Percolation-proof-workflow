from __future__ import annotations

import json
import copy
import hashlib
from pathlib import Path
from collections.abc import Callable, Iterable
from .statements import StatementRecord
from .model import WorkflowState


def _project_edge_origins(root: str, declarations: dict, selected: set[str],
                          deps: Callable[[str], set[str]],
                          edge_origins: Callable[[str, str], set[str]]) -> list[dict]:
    """Union origin labels along all helper walks to the next selected theorem.

    Revisiting a shared helper is necessary when a later path adds an origin.
    The finite label set (type/value/constructor) grows monotonically, so helper
    cycles terminate without enumerating paths. Labels describe provenance,
    not independent proof obligations, source authentication or admission.
    """
    projected: dict[str, set[str]] = {}
    seen: dict[str, set[str]] = {}
    work = [(dep, edge_origins(root, dep)) for dep in sorted(deps(root))]
    while work:
        dep, origins = work.pop()
        if dep not in declarations or dep == root:
            continue
        if dep in seen and origins <= seen[dep]:
            continue
        seen.setdefault(dep, set()).update(origins)
        accumulated = seen[dep]
        if dep in selected:
            projected.setdefault(dep, set()).update(accumulated)
        else:
            work.extend((child, accumulated | edge_origins(dep, child))
                        for child in sorted(deps(dep)))
    return [{'name': dep, 'origins': sorted(origins)}
            for dep, origins in sorted(projected.items())]


def merge_reachable_graph(state: WorkflowState, path: str | Path,
                          roots: Iterable[str]) -> dict[str, str]:
    """Project source theorem dependencies through definitions and generated helpers.

    This is a replay dependency graph, not a newly accepted proof decomposition.
    Raw type/value edges remain in metadata. External library declarations are outside
    this extractor's scope; this routine does not produce a standalone vendored project.
    Work on a copy so malformed input never partially changes research history.
    """
    raw = Path(path).read_bytes()
    rows = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    declarations = {r['name']: r for r in rows}
    if len(declarations) != len(rows):
        raise ValueError('duplicate declaration names')
    roots = list(roots)
    missing = set(roots) - declarations.keys()
    if missing:
        raise ValueError(f'missing roots: {sorted(missing)}')

    def deps(name):
        row = declarations[name]
        result = set(row.get('typeDeps', [])) | set(row.get('valueDeps', []))
        # Lean's declaration graph does not necessarily expose the constructor
        # edge from an inductive's own constant.  Prove2Me explicitly descends
        # into constructors because structure/inductive field types can be
        # needed by a generated Definitions bundle.
        if row.get('kind') == 'inductive':
            result.update(name for name, child in declarations.items()
                          if child.get('kind') == 'ctor'
                          and str(name).startswith(str(row['name']) + '.'))
        return result

    reachable = set()
    instance_roots = sorted(name for name, row in declarations.items()
                            if row.get('isInstance') is True)
    work = roots.copy() + instance_roots
    while work:
        name = work.pop()
        if name in reachable or name not in declarations:
            continue
        reachable.add(name)
        work.extend(deps(name) - reachable)
    selected = {name for name in reachable
                if declarations[name]['kind'] in {'theorem', 'opaque'}
                and declarations[name].get('startLine', 0) > 0}
    if not set(roots) <= selected:
        raise ValueError('roots must be source-located theorems or opaque declarations')
    candidate = copy.deepcopy(state)
    ids = {node.name: node.id for node in candidate.nodes.values()}
    if len(ids) != len(candidate.nodes):
        raise ValueError('duplicate research node names')
    digest = hashlib.sha256(raw).hexdigest()
    for name in sorted(selected):
        if name not in ids:
            ids[name] = candidate.add_node(name, f'<statement pending for {name}>',
                metadata={'statement_status': 'unresolved'})
        candidate.nodes[ids[name]].metadata.update(
            source=declarations[name], declaration_graph_sha256=digest,
            dependency_origin='compiled_replay')
    def edge_origins(parent: str, child: str) -> set[str]:
        row = declarations[parent]
        origins = set()
        if child in row.get('typeDeps', []):
            origins.add('type')
        if child in row.get('valueDeps', []):
            origins.add('value')
        if (row.get('kind') == 'inductive'
                and declarations.get(child, {}).get('kind') == 'ctor'
                and child.startswith(parent + '.')):
            origins.add('constructor')
        return origins

    edge_provenance = {}
    for name in sorted(selected):
        edge_provenance[name] = _project_edge_origins(
            name, declarations, selected, deps, edge_origins)
    for name in sorted(selected):
        found, visited = set(), set()
        work = list(deps(name))
        while work:
            dep = work.pop()
            if dep in visited or dep not in declarations:
                continue
            visited.add(dep)
            if dep in selected:
                if dep != name:
                    found.add(ids[dep])
            else:
                work.extend(deps(dep))
        node = candidate.nodes[ids[name]]
        additions = found - set(node.dependencies)
        if additions and node.status == 'verified':
            raise ValueError(f'verified node requires explicit invalidation: {name}')
        node.dependencies = sorted(set(node.dependencies) | found)
    candidate.validate()
    graph_record = {
        'schema_version': 1,
        'algorithm': 'merge_reachable_graph/v2',
        'graph_sha256': digest,
        'roots': roots,
        'instance_roots': instance_roots,
        'reachable_declarations': len(reachable),
        'selected_nodes': sorted(selected),
        'edge_provenance': edge_provenance,
        'constructor_expansions': sorted(name for name in reachable
                                         if declarations[name].get('kind') == 'ctor'),
        'supporting_declarations': sorted(name for name in reachable
                                          if name not in selected),
    }
    if not any(record.get('graph_sha256') == digest and record.get('roots') == roots
               and record.get('algorithm') == graph_record['algorithm']
               for record in candidate.graph_artifacts):
        candidate.graph_artifacts.append(graph_record)
    candidate.event('reachable_graph_merged', graph_sha256=digest, roots=roots,
                    reachable_declarations=len(reachable), theorem_nodes=len(selected))
    state.nodes, state.root_id, state.events = candidate.nodes, candidate.root_id, candidate.events
    state.graph_artifacts = candidate.graph_artifacts
    return {name: ids[name] for name in sorted(selected)}


def import_decl_graph(state: WorkflowState, path: str | Path, *, project_prefix: str | None = None) -> dict[str, str]:
    """Import Prove2Me's declaration-graph JSONL as a conservative theorem DAG.

    The upstream extractor exposes declaration-level type/value dependencies, instance roots, and
    source spans, but it does not expose theorem statements. Therefore imported nodes carry an
    explicit `statement_status=unresolved` marker and cannot be sent to verification until a statement
    extractor/formalization adapter fills the exact type.
    """
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    rows = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    rows = [r for r in rows if project_prefix is None or str(r.get("name", "")).startswith(project_prefix)]
    declarations = {str(row['name']): row for row in rows}
    if len(declarations) != len(rows):
        raise ValueError('duplicate declaration names')

    def source_located(row):
        # Older hand-written fixtures omit startLine; only an explicit zero is
        # the extractor's spanless/compiler-generated sentinel.
        return 'startLine' not in row or row.get('startLine') != 0

    def deps(name):
        row = declarations[name]
        result = set(row.get('typeDeps', [])) | set(row.get('valueDeps', []))
        if row.get('kind') == 'inductive':
            result.update(child_name for child_name, child in declarations.items()
                          if child.get('kind') == 'ctor'
                          and child_name.startswith(name + '.'))
        return result

    instance_roots = sorted(name for name, row in declarations.items()
                            if row.get('isInstance') is True)
    seed_names = [name for name, row in declarations.items()
                  if row.get('kind') in {'theorem', 'opaque'} and source_located(row)]
    reachable = set()
    work = seed_names + instance_roots
    while work:
        name = work.pop()
        if name in reachable or name not in declarations:
            continue
        reachable.add(name)
        work.extend(deps(name) - reachable)
    selected = {name for name in reachable
                if declarations[name].get('kind') in {'theorem', 'opaque'}
                and source_located(declarations[name])}

    candidate = copy.deepcopy(state)
    by_name: dict[str, str] = {node.name: node.id for node in candidate.nodes.values()}
    if len(by_name) != len(candidate.nodes):
        raise ValueError('ambiguous existing theorem names')
    for name in sorted(selected):
        row = declarations[name]
        if name not in by_name:
            by_name[name] = candidate.add_node(
                name, f"<statement pending for {name}>",
                metadata={"source": row, "statement_status": "unresolved"})
        node = candidate.nodes[by_name[name]]
        node.metadata.update({
            'source': row,
            'graph_kind': row.get('kind'),
            'module': row.get('module'),
            'is_private': row.get('isPrivate', False),
            'is_instance': row.get('isInstance', False),
            'user_name': row.get('userName'),
            'source_span': {'startLine': row.get('startLine'), 'endLine': row.get('endLine')},
            'statement_status': node.metadata.get('statement_status', 'unresolved'),
        })

    def edge_origins(parent: str, child: str) -> set[str]:
        row = declarations[parent]
        origins = set()
        if child in row.get('typeDeps', []):
            origins.add('type')
        if child in row.get('valueDeps', []):
            origins.add('value')
        if (row.get('kind') == 'inductive'
                and declarations.get(child, {}).get('kind') == 'ctor'
                and child.startswith(parent + '.')):
            origins.add('constructor')
        return origins

    edge_provenance = {}
    for name in sorted(selected):
        edge_provenance[name] = _project_edge_origins(
            name, declarations, selected, deps, edge_origins)
        node = candidate.nodes[by_name[name]]
        found = {by_name[entry['name']] for entry in edge_provenance[name]}
        node.dependencies = sorted(set(node.dependencies) | found)

    candidate.validate()
    graph_record = {
        'schema_version': 1,
        'algorithm': 'import_decl_graph/v3',
        'graph_sha256': digest,
        'roots': [],
        'instance_roots': instance_roots,
        'reachable_declarations': len(reachable),
        'selected_nodes': sorted(selected),
        'edge_provenance': edge_provenance,
        'constructor_expansions': sorted(name for name in reachable
                                         if declarations[name].get('kind') == 'ctor'),
        'supporting_declarations': sorted(name for name in reachable if name not in selected),
    }
    if not any(record.get('graph_sha256') == digest and
               record.get('algorithm') == graph_record['algorithm']
               for record in candidate.graph_artifacts):
        candidate.graph_artifacts.append(graph_record)
    candidate.event("decl_graph_imported", path=str(path), nodes=len(selected),
                    reachable_declarations=len(reachable), instance_roots=instance_roots)
    state.nodes, state.root_id, state.events = candidate.nodes, candidate.root_id, candidate.events
    state.graph_artifacts = candidate.graph_artifacts
    return {name: by_name[name] for name in sorted(selected)}


def attach_statement_index(state: WorkflowState, records: Iterable[StatementRecord]) -> int:
    """Attach trusted source statements to already imported declaration nodes."""
    by_name = {node.name: node for node in state.nodes.values()}
    attached = 0
    for record in records:
        node = by_name.get(record.qualified_name)
        if node is None:
            continue
        node.statement = record.source
        node.metadata.update({"statement_status": "indexed", "statement_file": record.source_file,
                              "statement_start_line": record.start_line, "statement_end_line": record.end_line})
        attached += 1
    state.event("statement_index_attached", attached=attached)
    return attached


def attach_elaborated_types(state: WorkflowState, path: str | Path) -> int:
    """Attach Lean's printed types and transitive axiom sets without registry promotion.

    Printed types are inspection evidence, not serialized expressions or comparator results.
    Trusted Challenge source statements remain unchanged.
    """
    raw = Path(path).read_bytes()
    rows = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    if len({row['name'] for row in rows}) != len(rows):
        raise ValueError('duplicate elaborated types')
    for row in rows:
        if not isinstance(row.get('type'), str) or not row['type'].strip():
            raise ValueError('missing elaborated type')
        if not isinstance(row.get('axioms'), list) or not all(isinstance(a, str) for a in row['axioms']):
            raise ValueError('invalid axiom evidence')
    by_name = {node.name: node for node in state.nodes.values()}
    allowed = {'propext', 'Quot.sound', 'Classical.choice'}
    digest = hashlib.sha256(raw).hexdigest()
    attached = 0
    for row in rows:
        node = by_name.get(row['name'])
        if node is None:
            continue
        node.metadata.update(elaborated_type=row['type'], level_params=row.get('levelParams', []),
            axioms=row['axioms'], unexpected_axioms=sorted(set(row['axioms']) - allowed),
            type_evidence_sha256=digest,
            type_representation='Lean pp.all; requires elaboration for reuse')
        attached += 1
    state.event('elaborated_types_attached', attached=attached,
                evidence_sha256=digest)
    return attached
