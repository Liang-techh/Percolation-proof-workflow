"""Validated, portable manifests for independent theorem verification bundles."""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re


_NAME = re.compile(r'^[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_][A-Za-z_0-9]*)*$')


def _relative_lean_files(values, field: str) -> tuple[str, ...]:
    if not isinstance(values, list) or not values:
        raise ValueError(f'{field} must be a nonempty list')
    result = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f'{field} must contain strings')
        relative = PurePosixPath(value)
        if (relative.is_absolute() or '..' in relative.parts or '\\' in value
                or relative.suffix != '.lean'):
            raise ValueError(f'{field} contains an unsafe Lean path')
        normalized = relative.as_posix()
        if normalized not in result:
            result.append(normalized)
    return tuple(result)


@dataclass(frozen=True)
class NodeManifest:
    challenge_module: str
    solution_module: str
    source_files: tuple[str, ...]


@dataclass(frozen=True)
class VerificationManifest:
    path: Path
    state_path: Path
    dependency_name: str
    nodes: dict[str, NodeManifest]
    target_root: str | None = None
    contract_path: Path | None = None
    dependency_profile: str | None = None
    toolchain: str | None = None
    verification: dict = field(default_factory=dict)
    host_protocol: dict = field(default_factory=dict)
    research: dict = field(default_factory=dict)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    def identity_for_state(self) -> dict[str, str | None]:
        return {
            'path': os.path.relpath(self.path, self.state_path.parent).replace('\\', '/'),
            'sha256': self.sha256,
            'target': self.target_root,
        }

    def for_node(self, node_name: str) -> NodeManifest:
        try:
            return self.nodes[node_name]
        except KeyError as exc:
            raise ValueError(f'verification manifest has no node: {node_name}') from exc


def load_verification_manifest(path: str | Path) -> VerificationManifest:
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('verification manifest schema_version must be 1')
    state_value = data.get('state_path')
    if not isinstance(state_value, str):
        raise ValueError('verification manifest requires state_path')
    state_relative = PurePosixPath(state_value)
    if state_relative.is_absolute() or '\\' in state_value:
        raise ValueError('verification manifest state_path must be portable and relative')
    workspace_value = data.get('workspace_root', '.')
    if not isinstance(workspace_value, str):
        raise ValueError('verification manifest workspace_root must be a string')
    workspace_relative = PurePosixPath(workspace_value)
    if workspace_relative.is_absolute() or '\\' in workspace_value:
        raise ValueError('verification manifest workspace_root must be portable and relative')
    workspace_root = (path.parent / workspace_relative).resolve()
    state_path = (path.parent / state_relative).resolve()
    if not state_path.is_relative_to(workspace_root):
        raise ValueError('verification manifest state_path escapes workspace_root')
    dependency = data.get('dependency')
    dependency_name = dependency.get('name') if isinstance(dependency, dict) else None
    if not isinstance(dependency_name, str) or not _NAME.fullmatch(dependency_name):
        raise ValueError('verification manifest requires a valid dependency.name')
    target = data.get('target', {})
    if not isinstance(target, dict):
        raise ValueError('verification manifest target must be an object')
    target_root = target.get('root')
    if target_root is not None and (not isinstance(target_root, str) or not target_root.strip()):
        raise ValueError('verification manifest target.root must be a nonempty string')
    contract_path = None
    contract = target.get('contract')
    if contract is not None:
        if not isinstance(contract, str):
            raise ValueError('verification manifest target.contract must be a string')
        contract_relative = PurePosixPath(contract)
        if contract_relative.is_absolute() or '..' in contract_relative.parts or '\\' in contract:
            raise ValueError('verification manifest target.contract must be a safe relative path')
        contract_path = (path.parent / contract_relative).resolve()
        if not contract_path.is_relative_to(workspace_root):
            raise ValueError('verification manifest target.contract escapes workspace_root')
    dependency_profile = dependency.get('profile')
    toolchain = dependency.get('toolchain')
    if dependency_profile is not None and not isinstance(dependency_profile, str):
        raise ValueError('verification manifest dependency.profile must be a string')
    if toolchain is not None and not isinstance(toolchain, str):
        raise ValueError('verification manifest dependency.toolchain must be a string')
    verification = data.get('verification', {})
    host_protocol = data.get('host_protocol', {'name': 'codex-agent-callback', 'version': 1})
    if not isinstance(verification, dict) or not isinstance(host_protocol, dict):
        raise ValueError('verification and host_protocol must be objects')
    acceptance_line = verification.get('acceptance_line', 'Your solution is okay!')
    if acceptance_line != 'Your solution is okay!':
        raise ValueError('verification.acceptance_line must match the pinned comparator')
    permitted = verification.get('permitted_axioms',
                                 ['propext', 'Quot.sound', 'Classical.choice'])
    if not isinstance(permitted, list) or any(item not in {
            'propext', 'Quot.sound', 'Classical.choice'} for item in permitted):
        raise ValueError('verification.permitted_axioms contains a nonstandard axiom')
    if verification.get('enable_nanoda', True) is not True:
        raise ValueError('verification.enable_nanoda must be true')
    bundle_root = verification.get('bundle_root')
    if bundle_root is not None:
        if not isinstance(bundle_root, str) or not bundle_root.strip():
            raise ValueError('verification.bundle_root must be a nonempty string')
        bundle_relative = PurePosixPath(bundle_root)
        if bundle_relative.is_absolute() or '\\' in bundle_root:
            raise ValueError('verification.bundle_root must be portable and relative')
    if host_protocol.get('version') != 1:
        raise ValueError('unsupported host_protocol version')
    research = data.get('research', {})
    if not isinstance(research, dict):
        raise ValueError('verification manifest research must be an object')
    if research:
        if research.get('project') is not None and not isinstance(research.get('project'), str):
            raise ValueError('research.project must be a string')
        research_root = research.get('root', target_root)
        if research_root is not None and (not isinstance(research_root, str) or not research_root.strip()):
            raise ValueError('research.root must be a nonempty string')
        raw_research_nodes = research.get('nodes')
        if not isinstance(raw_research_nodes, list) or not raw_research_nodes:
            raise ValueError('research.nodes must be a nonempty list')
        research_names = set()
        for raw_node in raw_research_nodes:
            if not isinstance(raw_node, dict) or not isinstance(raw_node.get('name'), str) \
                    or not raw_node['name'].strip() or raw_node['name'] in research_names:
                raise ValueError('research node entries are malformed or duplicated')
            research_names.add(raw_node['name'])
            if not isinstance(raw_node.get('statement'), str) or not raw_node['statement'].strip():
                raise ValueError(f'research statement missing for {raw_node.get("name")}')
            parent = raw_node.get('parent')
            if parent is not None and (not isinstance(parent, str) or not parent.strip()):
                raise ValueError(f'research parent is malformed for {raw_node["name"]}')
            dependencies = raw_node.get('dependencies', [])
            if not isinstance(dependencies, list) or any(
                    not isinstance(dep, str) or not dep.strip() for dep in dependencies):
                raise ValueError(f'research dependencies are malformed for {raw_node["name"]}')
            if raw_node['name'] in dependencies or raw_node['name'] == parent:
                raise ValueError(f'research node has a self edge: {raw_node["name"]}')
            if raw_node.get('proof_sketch') is not None and not isinstance(raw_node['proof_sketch'], str):
                raise ValueError(f'research proof_sketch is malformed for {raw_node["name"]}')
            if raw_node.get('metadata') is not None and not isinstance(raw_node['metadata'], dict):
                raise ValueError(f'research metadata is malformed for {raw_node["name"]}')
        if research_root is not None and research_root not in research_names:
            raise ValueError('research.root is not listed in research.nodes')
        for raw_node in raw_research_nodes:
            refs = ([raw_node['parent']] if raw_node.get('parent') else []) + raw_node.get('dependencies', [])
            if any(ref not in research_names for ref in refs):
                raise ValueError(f'research node has an unknown edge target: {raw_node["name"]}')
    raw_nodes = data.get('nodes')
    if not isinstance(raw_nodes, dict) or not raw_nodes:
        raise ValueError('verification manifest requires nonempty nodes')
    nodes = {}
    for theorem_name, raw in raw_nodes.items():
        if not isinstance(theorem_name, str) or not theorem_name.strip() or not isinstance(raw, dict):
            raise ValueError('verification manifest node entries are malformed')
        challenge = raw.get('challenge_module')
        solution = raw.get('solution_module')
        if not isinstance(challenge, str) or not _NAME.fullmatch(challenge):
            raise ValueError(f'invalid challenge_module for {theorem_name}')
        if not isinstance(solution, str) or not _NAME.fullmatch(solution):
            raise ValueError(f'invalid solution_module for {theorem_name}')
        files = list(_relative_lean_files(raw.get('source_files'), f'source_files[{theorem_name}]'))
        required = {challenge.replace('.', '/') + '.lean', solution.replace('.', '/') + '.lean'}
        if not required.issubset(files):
            raise ValueError(f'source_files[{theorem_name}] must include comparator modules')
        nodes[theorem_name] = NodeManifest(challenge, solution, tuple(files))
    return VerificationManifest(path, state_path, dependency_name, nodes, target_root,
                                contract_path, dependency_profile, toolchain,
                                verification, host_protocol, research)


def initialize_state_from_manifest(manifest: VerificationManifest, store) -> object:
    """Create a durable research DAG from the optional manifest research section.

    This is an intake operation, not proof evidence.  It refuses to replace an
    existing checkpoint and requires every initialized theorem to have a
    verification-manifest node entry, keeping intake and later staging aligned.
    """
    from .model import WorkflowState

    if not manifest.research:
        raise ValueError('manifest has no research graph section')
    if store.path.exists():
        raise FileExistsError(f'research state already exists: {store.path}')
    raw_nodes = manifest.research['nodes']
    names = {raw['name'] for raw in raw_nodes}
    if names != set(manifest.nodes):
        raise ValueError('research.nodes must exactly match verification manifest nodes')
    root_name = manifest.research.get('root', manifest.target_root)
    if root_name is None:
        raise ValueError('research root is required for manifest intake')
    state = WorkflowState(project=manifest.research.get('project', 'percolation'))
    by_name = {}
    for raw in raw_nodes:
        metadata = dict(raw.get('metadata') or {})
        metadata.setdefault('statement_status', 'indexed')
        by_name[raw['name']] = state.add_node(
            raw['name'], raw['statement'], proof_sketch=raw.get('proof_sketch'), metadata=metadata)
    state.root_id = by_name[root_name]
    for raw in raw_nodes:
        node = state.nodes[by_name[raw['name']]]
        parent = raw.get('parent')
        if parent:
            node.parent_id = by_name[parent]
            parent_node = state.nodes[by_name[parent]]
            if node.id not in parent_node.dependencies:
                parent_node.dependencies.append(node.id)
        node.dependencies = list(dict.fromkeys(by_name[edge]
                                               for edge in raw.get('dependencies', [])))
    if manifest.contract_path is not None:
        contract = json.loads(manifest.contract_path.read_text(encoding='utf-8'))
        if not isinstance(contract, dict) or (manifest.target_root and
                                               contract.get('target') != manifest.target_root):
            raise ValueError('manifest contract does not match the research target')
        state.nodes[state.root_id].metadata['contract'] = contract
        state.nodes[state.root_id].metadata['contract_path'] = manifest.contract_path.name
    state.manifest = manifest.identity_for_state()
    state.event('manifest_research_initialized', manifest=state.manifest,
                root=root_name, nodes=len(raw_nodes))
    state.validate()
    store.save(state)
    return state


def bind_manifest(store, manifest: VerificationManifest):
    """Bind a manifest identity to state, refusing silent source-plan drift."""
    state = store.load()
    identity = manifest.identity_for_state()
    if state.manifest and state.manifest != identity:
        raise ValueError('state is bound to a different verification manifest')
    if not state.manifest:
        state.manifest = identity
        state.event('manifest_bound', manifest=identity)
        store.save(state)
    return state
