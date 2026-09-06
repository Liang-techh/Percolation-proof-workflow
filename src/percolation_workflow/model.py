from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
import uuid
import re


ATTEMPT_HISTORY_SCHEMA_VERSION = 1
ATTEMPT_OUTPUT_SUMMARY_LIMIT = 4096
_ATTEMPT_OUTPUT_SUMMARY_MARKER = "\n... output truncated ...\n"
_ATTEMPT_HISTORY_FIELDS = {
    "schema_version", "sequence", "event", "attempt_id", "node_id",
    "agent_id", "source_path", "status", "exit_code", "created_at",
    "finished_at", "stdout_summary", "stderr_summary",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_attempt_timestamp(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"attempt {field_name} must be a nonempty timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"attempt {field_name} is not an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"attempt {field_name} must include a timezone")
    return parsed


def _attempt_output_summary(output: str) -> str:
    """Return a deterministic diagnostic excerpt with a hard serialized bound."""
    if not isinstance(output, str):
        raise ValueError("attempt output must be a string")
    if len(output) <= ATTEMPT_OUTPUT_SUMMARY_LIMIT:
        return output
    head_size = min(512, ATTEMPT_OUTPUT_SUMMARY_LIMIT // 4)
    tail_size = ATTEMPT_OUTPUT_SUMMARY_LIMIT - head_size - len(
        _ATTEMPT_OUTPUT_SUMMARY_MARKER)
    return (output[:head_size] + _ATTEMPT_OUTPUT_SUMMARY_MARKER +
            output[-tail_size:])


class NodeStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    # Only an explicit engineering/audit checker scope can close this way.
    # Mathematical diagnostics remain OPEN, even when the checker succeeds.
    EVIDENCE_COMPLETE = "evidence_complete"
    BLOCKED = "blocked"


class EvidenceStage(StrEnum):
    """Evidence level, orthogonal to scheduler liveness.

    ``NodeStatus`` answers whether a node can discharge DAG edges.  This enum
    records which mathematical/provenance gate has actually been crossed, so
    a compiled candidate cannot be mistaken for a comparator-accepted theorem
    or for a globally closed target.
    """
    OPEN = "open"
    COMPILED_CANDIDATE = "compiled_candidate"
    SOURCE_COMPARATOR_PENDING = "source_comparator_pending"
    LEAN_VERIFIED = "lean_verified"
    GLOBAL_CLOSED = "global_closed"


def status_is_closed(status: NodeStatus | str) -> bool:
    """Whether a node may discharge a dependency edge.

    This public scalar predicate is deliberately theorem-only.  External
    ``EVIDENCE_COMPLETE`` is contextual and must be checked by ``node_is_closed``
    (including freshness and domain), never by a generic scheduler shortcut.
    """
    return status == NodeStatus.VERIFIED


@dataclass
class Attempt:
    id: str
    node_id: str
    agent_id: str
    # Immutable provenance for the lifecycle start record. ``agent_id`` is
    # the current owner and may change when a dispatch placeholder is rebound.
    created_agent_id: str | None = None
    source_path: str | None = None
    status: str = "created"
    command: list[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    created_at: str = field(default_factory=now)
    finished_at: str | None = None

    def __post_init__(self) -> None:
        if self.created_agent_id is None:
            self.created_agent_id = self.agent_id


@dataclass
class ProofNode:
    id: str
    name: str
    statement: str
    parent_id: str | None = None
    status: NodeStatus = NodeStatus.OPEN
    proof_sketch: str | None = None
    dependencies: list[str] = field(default_factory=list)
    verified_artifact: str | None = None
    attempts: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def node_is_closed(node: ProofNode) -> bool:
    """Do not let legacy external status flags discharge dependency edges."""
    if node.metadata.get('verification_domain') == 'external-research':
        # Import lazily: external adapts this model, and also checks live hashes.
        from .external import external_evidence_staleness
        return (node.status == NodeStatus.EVIDENCE_COMPLETE and
                not external_evidence_staleness(node))
    return node.status == NodeStatus.VERIFIED


@dataclass
class WorkflowState:
    schema_version: int = 1
    revision: int = 0
    project: str = "percolation"
    root_id: str | None = None
    nodes: dict[str, ProofNode] = field(default_factory=dict)
    attempts: dict[str, Attempt] = field(default_factory=dict)
    attempt_history: list[dict[str, Any]] = field(default_factory=list)
    registry: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    agent_requests: dict[str, dict[str, Any]] = field(default_factory=dict)
    manifest: dict[str, Any] | None = None
    graph_artifacts: list[dict[str, Any]] = field(default_factory=list)
    global_closure: dict[str, Any] = field(default_factory=dict)

    def event(self, kind: str, **payload: Any) -> None:
        self.events.append({"at": now(), "kind": kind, **payload})

    @staticmethod
    def _attempt_history_entry(attempt: Attempt, *, sequence: int,
                               event: str) -> dict[str, Any]:
        if event not in {"started", "finished"}:
            raise ValueError("attempt history event must be started or finished")
        finished = event == "finished"
        return {
            "schema_version": ATTEMPT_HISTORY_SCHEMA_VERSION,
            "sequence": sequence,
            "event": event,
            "attempt_id": attempt.id,
            "node_id": attempt.node_id,
            "agent_id": (attempt.created_agent_id if event == "started"
                          else attempt.agent_id),
            "source_path": attempt.source_path,
            "status": attempt.status if finished else "created",
            "exit_code": attempt.exit_code if finished else None,
            "created_at": attempt.created_at,
            "finished_at": attempt.finished_at if finished else None,
            "stdout_summary": _attempt_output_summary(attempt.stdout) if finished else "",
            "stderr_summary": _attempt_output_summary(attempt.stderr) if finished else "",
        }

    @classmethod
    def _reconstruct_legacy_attempt_history(
            cls, attempts: dict[str, Attempt]) -> list[dict[str, Any]]:
        """Upgrade an old checkpoint in memory without rewriting it on load."""
        timeline: list[tuple[datetime, int, int, Attempt, str]] = []
        for insertion_order, attempt in enumerate(attempts.values()):
            created = _parse_attempt_timestamp(attempt.created_at, "created_at")
            timeline.append((created, 0, insertion_order, attempt, "started"))
            if attempt.finished_at is not None:
                finished = _parse_attempt_timestamp(attempt.finished_at, "finished_at")
                timeline.append((finished, 1, insertion_order, attempt, "finished"))
        timeline.sort(key=lambda item: (item[0], item[1], item[2]))
        return [cls._attempt_history_entry(attempt, sequence=sequence, event=event)
                for sequence, (_, _, _, attempt, event) in enumerate(timeline)]

    def _validate_attempt_history(self) -> None:
        if not isinstance(self.attempts, dict):
            raise ValueError("attempts must be a dictionary")
        if not isinstance(self.attempt_history, list):
            raise ValueError("attempt_history must be a list")

        for attempt_id, attempt in self.attempts.items():
            if (not isinstance(attempt_id, str) or not attempt_id or
                    not isinstance(attempt, Attempt) or attempt.id != attempt_id):
                raise ValueError("attempt identity is malformed")
            if attempt.node_id not in self.nodes:
                raise ValueError(f"attempt {attempt_id} references an unknown node")
            if not isinstance(attempt.agent_id, str) or not attempt.agent_id.strip():
                raise ValueError(f"attempt {attempt_id} has no agent_id")
            if (not isinstance(attempt.created_agent_id, str) or
                    not attempt.created_agent_id.strip()):
                raise ValueError(f"attempt {attempt_id} has no created_agent_id")
            if attempt.source_path is not None and not isinstance(attempt.source_path, str):
                raise ValueError(f"attempt {attempt_id} has an invalid source_path")
            if not isinstance(attempt.status, str) or not attempt.status.strip():
                raise ValueError(f"attempt {attempt_id} has an invalid status")
            if (not isinstance(attempt.command, list) or
                    any(not isinstance(part, str) for part in attempt.command)):
                raise ValueError(f"attempt {attempt_id} has an invalid command")
            if not isinstance(attempt.stdout, str) or not isinstance(attempt.stderr, str):
                raise ValueError(f"attempt {attempt_id} output must be text")
            created = _parse_attempt_timestamp(attempt.created_at, "created_at")
            if attempt.finished_at is None:
                if attempt.status != "created" or attempt.exit_code is not None:
                    raise ValueError(f"active attempt {attempt_id} has terminal fields")
            else:
                finished = _parse_attempt_timestamp(attempt.finished_at, "finished_at")
                if finished < created:
                    raise ValueError(f"attempt {attempt_id} finishes before it starts")
                if type(attempt.exit_code) is not int:
                    raise ValueError(f"finished attempt {attempt_id} has no integer exit_code")

        linked_attempts: set[str] = set()
        for node in self.nodes.values():
            if not isinstance(node.attempts, list) or len(node.attempts) != len(set(node.attempts)):
                raise ValueError(f"node {node.id} has malformed attempt links")
            for attempt_id in node.attempts:
                attempt = self.attempts.get(attempt_id)
                if attempt is None or attempt.node_id != node.id or attempt_id in linked_attempts:
                    raise ValueError(f"node {node.id} has an invalid attempt link")
                linked_attempts.add(attempt_id)
        if linked_attempts != set(self.attempts):
            raise ValueError("attempt history contains an unlinked attempt")

        lifecycle: dict[str, list[str]] = {attempt_id: [] for attempt_id in self.attempts}
        for sequence, entry in enumerate(self.attempt_history):
            if not isinstance(entry, dict) or set(entry) != _ATTEMPT_HISTORY_FIELDS:
                raise ValueError("attempt_history entry is malformed")
            if entry["schema_version"] != ATTEMPT_HISTORY_SCHEMA_VERSION:
                raise ValueError("unsupported attempt_history schema")
            if type(entry["sequence"]) is not int or entry["sequence"] != sequence:
                raise ValueError("attempt_history sequence is not contiguous")
            event = entry["event"]
            if event not in {"started", "finished"}:
                raise ValueError("attempt_history event is invalid")
            attempt_id = entry["attempt_id"]
            attempt = self.attempts.get(attempt_id)
            if attempt is None:
                raise ValueError("attempt_history references an unknown attempt")
            if lifecycle[attempt_id] and event == "started":
                raise ValueError("attempt_history contains a duplicate start")
            if event == "finished" and lifecycle[attempt_id] != ["started"]:
                raise ValueError("attempt_history finish has no preceding start")
            lifecycle[attempt_id].append(event)

            expected = self._attempt_history_entry(
                attempt, sequence=sequence, event=event)
            if entry != expected:
                raise ValueError(f"attempt_history {event} record does not match attempt")
            if (len(entry["stdout_summary"]) > ATTEMPT_OUTPUT_SUMMARY_LIMIT or
                    len(entry["stderr_summary"]) > ATTEMPT_OUTPUT_SUMMARY_LIMIT):
                raise ValueError("attempt_history output summary exceeds its bound")

        for attempt_id, attempt in self.attempts.items():
            expected_lifecycle = (["started"] if attempt.finished_at is None else
                                  ["started", "finished"])
            if lifecycle[attempt_id] != expected_lifecycle:
                raise ValueError(f"attempt_history lifecycle is incomplete for {attempt_id}")

    def replay_attempt_history(self) -> dict[str, dict[str, Any]]:
        """Validate and replay the compact audit log into latest attempt snapshots."""
        self._validate_attempt_history()
        replayed: dict[str, dict[str, Any]] = {}
        for entry in self.attempt_history:
            attempt_id = entry["attempt_id"]
            replayed[attempt_id] = {
                key: value for key, value in entry.items()
                if key not in {"schema_version", "sequence", "event"}
            }
        return replayed

    def evidence_stage(self, node_id: str) -> EvidenceStage:
        if node_id not in self.nodes:
            raise KeyError(node_id)
        raw = self.nodes[node_id].metadata.get("evidence_stage", EvidenceStage.OPEN)
        try:
            return EvidenceStage(raw)
        except ValueError as exc:
            raise ValueError(f"node {node_id} has invalid evidence_stage: {raw!r}") from exc

    def set_evidence_stage(self, node_id: str, stage: EvidenceStage | str) -> None:
        if node_id not in self.nodes:
            raise KeyError(node_id)
        stage = EvidenceStage(stage)
        node = self.nodes[node_id]
        node.metadata["evidence_stage"] = stage.value
        if stage != EvidenceStage.GLOBAL_CLOSED and self.global_closure.get("root_id") == node_id:
            self.global_closure = {}
        self.event("evidence_stage_changed", node_id=node_id, evidence_stage=stage.value)

    def global_closure_report(self) -> dict[str, Any]:
        """Return a fail-closed view; this never promotes a node implicitly."""
        root_id = self.root_id
        if root_id is None or root_id not in self.nodes:
            return {"status": "open", "reason": "no theorem root"}
        reachable = set()
        work = [root_id]
        while work:
            node_id = work.pop()
            if node_id in reachable:
                continue
            reachable.add(node_id)
            work.extend(self.nodes[node_id].dependencies)
        all_verified = all(self.nodes[node_id].status == NodeStatus.VERIFIED for node_id in reachable)
        receipt = self.global_closure if isinstance(self.global_closure, dict) else {}
        closed = (receipt.get("root_id") == root_id and receipt.get("status") == "global_closed"
                  and all_verified and all(self.evidence_stage(node_id) == EvidenceStage.GLOBAL_CLOSED
                                           for node_id in reachable))
        return {"status": "global_closed" if closed else
                ("verified_root_pending_global_gate" if all_verified else "open"),
                "root_id": root_id, "reachable_nodes": sorted(reachable),
                "all_reachable_verified": all_verified, "receipt": receipt}

    def close_global_theorem(self, receipt: dict[str, Any]) -> dict[str, Any]:
        """Explicit final CI/project gate; local node verification is insufficient."""
        report = self.global_closure_report()
        if report["status"] != "verified_root_pending_global_gate":
            raise ValueError("global theorem requires every reachable node to be verified")
        if not isinstance(receipt, dict) or receipt.get("ci_passed") is not True:
            raise ValueError("global theorem requires an explicit ci_passed receipt")
        root_id = report["root_id"]
        for node_id in report["reachable_nodes"]:
            self.set_evidence_stage(node_id, EvidenceStage.GLOBAL_CLOSED)
        self.global_closure = {"status": "global_closed", "root_id": root_id, **receipt}
        self.event("global_theorem_closed", root_id=root_id, receipt=receipt)
        return self.global_closure

    def add_node(self, name: str, statement: str, *, parent_id: str | None = None,
                 proof_sketch: str | None = None, dependencies: list[str] | None = None,
                 metadata: dict[str, Any] | None = None) -> str:
        node_id = uuid.uuid4().hex
        self.nodes[node_id] = ProofNode(node_id, name, statement, parent_id,
                                        proof_sketch=proof_sketch,
                                        dependencies=dependencies or [], metadata=metadata or {})
        if parent_id:
            self.nodes[parent_id].dependencies.append(node_id)
        elif self.root_id is None:
            self.root_id = node_id
        self.event("node_added", node_id=node_id, parent_id=parent_id, name=name)
        return node_id

    def frontier_closability(self, node_id: str) -> int:
        """Count open ancestors that would close after this leaf is verified.

        Prove2Me ranks open leaves by the amount of theorem-tree progress they
        unlock.  Recompute that cascade from the current statuses instead of
        storing a derived number, so stale checkpoints cannot mis-rank work.
        """
        if node_id not in self.nodes:
            raise KeyError(node_id)
        candidate = self.nodes[node_id]
        if candidate.status != NodeStatus.OPEN or any(
                not node_is_closed(self.nodes[dep]) for dep in candidate.dependencies):
            return 0
        reverse = {node.id: set() for node in self.nodes.values()}
        for node in self.nodes.values():
            for dependency in node.dependencies:
                reverse[dependency].add(node.id)
        ancestors = set()
        work = list(reverse[node_id])
        while work:
            ancestor = work.pop()
            if ancestor in ancestors:
                continue
            ancestors.add(ancestor)
            work.extend(reverse[ancestor])
        initially_closed = {node.id for node in self.nodes.values()
                            if node_is_closed(node)}
        closed = set(initially_closed)
        closed.add(node_id)
        changed = True
        while changed:
            changed = False
            for node in self.nodes.values():
                if node.id not in ancestors or node.id in closed or node.status != NodeStatus.OPEN:
                    continue
                if all(dep in closed for dep in node.dependencies):
                    closed.add(node.id)
                    changed = True
        return sum(1 for node in self.nodes.values()
                   if node.id in (closed - initially_closed) and node.id != node_id)

    def frontier(self) -> list[ProofNode]:
        candidates = [n for n in self.nodes.values()
                      if n.status == NodeStatus.OPEN and all(
                          node_is_closed(self.nodes[d]) for d in n.dependencies)]
        # dict insertion order remains the deterministic tie-breaker used by
        # the older workflow; closability is the Prove2Me-style primary key.
        return sorted(candidates, key=lambda node: -self.frontier_closability(node.id))

    def validate(self) -> None:
        """Reject dangling edges, self edges, and cycles before scheduling agents."""
        if self.root_id is not None and self.root_id not in self.nodes:
            raise ValueError('workflow root_id does not reference a node')
        if self.manifest is not None:
            if not isinstance(self.manifest, dict) or not re.fullmatch(
                    r'[0-9a-f]{64}', str(self.manifest.get('sha256', ''))):
                raise ValueError('state manifest identity is malformed')
            manifest_path = self.manifest.get('path')
            if (not isinstance(manifest_path, str) or not manifest_path or
                    manifest_path.startswith('/') or '\\' in manifest_path):
                raise ValueError('state manifest path must be portable')
            target = self.manifest.get('target')
            if target is not None and not isinstance(target, str):
                raise ValueError('state manifest target must be a string')
        if not isinstance(self.graph_artifacts, list):
            raise ValueError('graph_artifacts must be a list')
        for artifact in self.graph_artifacts:
            if not isinstance(artifact, dict) or artifact.get('schema_version') != 1:
                raise ValueError('graph artifact record is malformed')
            if (not isinstance(artifact.get('graph_sha256'), str) or
                    not re.fullmatch(r'[0-9a-f]{64}', artifact['graph_sha256'])):
                raise ValueError('graph artifact digest is malformed')
            if not isinstance(artifact.get('roots'), list) or not isinstance(
                    artifact.get('selected_nodes'), list):
                raise ValueError('graph artifact roots or selected_nodes is malformed')
        if not isinstance(self.global_closure, dict):
            raise ValueError('global_closure must be a dictionary')
        self._validate_attempt_history()
        for request_id, request in self.agent_requests.items():
            if not isinstance(request, dict):
                raise ValueError(f'agent request {request_id} is malformed')
            lease = request.get('lease')
            if lease is None:
                continue
            if not isinstance(lease, dict) or lease.get('status') not in {'active', 'released', 'expired'}:
                raise ValueError(f'agent request {request_id} has an invalid lease')
            if not isinstance(lease.get('owner'), str) or not lease['owner'].strip():
                raise ValueError(f'agent request {request_id} lease has no owner')
            for field_name in ('acquired_at', 'renewed_at', 'expires_at'):
                if not isinstance(lease.get(field_name), str) or not lease[field_name].strip():
                    raise ValueError(f'agent request {request_id} lease has no {field_name}')
        for node in self.nodes.values():
            raw_stage = node.metadata.get('evidence_stage', EvidenceStage.OPEN)
            try:
                stage = EvidenceStage(raw_stage)
            except ValueError as exc:
                raise ValueError(f'node {node.id} has invalid evidence_stage') from exc
            if stage == EvidenceStage.GLOBAL_CLOSED and node.status != NodeStatus.VERIFIED:
                raise ValueError('globally closed node must be verified')
            if node.status == NodeStatus.EVIDENCE_COMPLETE:
                if node.metadata.get('verification_domain') != 'external-research':
                    raise ValueError('evidence-complete node is not an external research node')
                if not isinstance(node.metadata.get('evidence_receipt'), dict):
                    raise ValueError('evidence-complete node has no evidence receipt')
                if node.id in self.registry:
                    raise ValueError('evidence-complete node cannot enter theorem registry')
            if node.parent_id is not None:
                if node.parent_id not in self.nodes:
                    raise ValueError(f'node {node.id} has a dangling parent_id')
                if node.id not in self.nodes[node.parent_id].dependencies:
                    raise ValueError(f'parent/dependency mismatch for node {node.id}')
            for dep in node.dependencies:
                if dep not in self.nodes or dep == node.id:
                    raise ValueError(f"invalid dependency {node.id} -> {dep}")
        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise ValueError("theorem graph contains a cycle")
            if node_id in visited:
                return
            visiting.add(node_id)
            for dep in self.nodes[node_id].dependencies:
                visit(dep)
            visiting.remove(node_id)
            visited.add(node_id)
        for node_id in self.nodes:
            visit(node_id)

    def _register_verified(self, node_id: str, artifact: str, *, receipt: dict[str, Any]) -> None:
        """Coordinator-only transition; callers use verification.verify_and_register.

        Python objects are not a security boundary against hostile in-process code.
        This validates evidence consistency and removes the boolean-only shortcut.
        """
        node = self.nodes[node_id]
        if node.metadata.get('verification_domain') == 'external-research':
            raise ValueError('external research cannot enter the verified theorem registry')
        attempt = self.attempts.get(receipt.get('attempt_id', ''))
        if attempt is None or attempt.node_id != node_id or attempt.status != 'passed' or attempt.exit_code != 0:
            raise ValueError('registry requires a successful attempt for this node')
        if not receipt.get('source_hashes') or not receipt.get('source_digest'):
            raise ValueError('registry requires source evidence')
        import hashlib
        identity = receipt.get('statement_identity', {})
        if identity.get('name') != node.name or identity.get('statement_sha256') != hashlib.sha256(node.statement.encode()).hexdigest():
            raise ValueError('registry requires matching statement identity')
        if receipt.get('verification_kind') == 'reduction':
            marker = receipt.get('reduction_marker')
            if (not isinstance(marker, str) or not marker.strip() or
                    marker not in receipt.get('reduction_stdout', '').splitlines() or
                    not receipt.get('reduction_command')):
                raise ValueError('registry requires reduction audit evidence')
            children = receipt.get('child_registries')
            if (not isinstance(children, dict) or set(children) != set(node.dependencies) or
                    any(not isinstance(value, str) or not value for value in children.values())):
                raise ValueError('registry requires verified child evidence')
        elif not receipt.get('comparator_command') or 'Your solution is okay!' not in (
                receipt.get('comparator_stdout', '') + '\n' + receipt.get('comparator_stderr', '')).splitlines():
            raise ValueError('registry requires comparator acceptance evidence')
        if self.manifest and receipt.get('manifest', {}).get('sha256') != self.manifest.get('sha256'):
            raise ValueError('registry requires matching verification manifest identity')
        if any(self.nodes[dep].status != NodeStatus.VERIFIED for dep in node.dependencies):
            raise ValueError('registry requires closed dependencies')
        stage = self.evidence_stage(node_id)
        if stage not in {EvidenceStage.LEAN_VERIFIED, EvidenceStage.GLOBAL_CLOSED}:
            raise ValueError('registry requires an explicit Lean-verified evidence stage')
        node.status = NodeStatus.VERIFIED
        node.verified_artifact = artifact
        self.registry[node_id] = {"node_id": node_id, "name": node.name,
                                  "statement": node.statement, "artifact": artifact,
                                  "verified_at": now(), "verification_receipt": receipt}
        self.event("node_verified", node_id=node_id, artifact=artifact)

    def begin_attempt(self, node_id: str, agent_id: str, source_path: str | None = None) -> str:
        node = self.nodes[node_id]
        if not isinstance(agent_id, str) or not agent_id.strip():
            raise ValueError('attempt requires a nonempty agent_id')
        if source_path is not None and not isinstance(source_path, str):
            raise ValueError('attempt source_path must be a string or None')
        if node.status in {NodeStatus.VERIFIED, NodeStatus.EVIDENCE_COMPLETE,
                           NodeStatus.IN_PROGRESS} or node_id in self.registry:
            raise ValueError('node already verified or has an active attempt')
        attempt_id = uuid.uuid4().hex
        attempt = Attempt(attempt_id, node_id, agent_id, source_path=source_path)
        self.attempts[attempt_id] = attempt
        self.nodes[node_id].status = NodeStatus.IN_PROGRESS
        self.nodes[node_id].attempts.append(attempt_id)
        self.attempt_history.append(self._attempt_history_entry(
            attempt, sequence=len(self.attempt_history), event="started"))
        self.event("attempt_started", attempt_id=attempt_id, node_id=node_id, agent_id=agent_id)
        return attempt_id

    def rebind_attempt(self, attempt_id: str, agent_id: str) -> None:
        """Bind an active dispatch attempt while preserving lifecycle consistency."""
        attempt = self.attempts[attempt_id]
        if not isinstance(agent_id, str) or not agent_id.strip():
            raise ValueError('attempt requires a nonempty agent_id')
        if attempt.finished_at is not None or attempt.status != 'created':
            raise ValueError('only an active attempt can be rebound')
        started = next((entry for entry in self.attempt_history
                        if entry['attempt_id'] == attempt_id and entry['event'] == 'started'), None)
        if started is None:
            raise ValueError('attempt history has no started record')
        # Keep the lifecycle record immutable. The current owner is stored on
        # the attempt itself and the event below records the rebind.
        attempt.agent_id = agent_id
        self.event('attempt_rebound', attempt_id=attempt_id, agent_id=agent_id)

    def finish_attempt(self, attempt_id: str, *, status: str, command: list[str], stdout: str,
                       stderr: str, exit_code: int) -> None:
        attempt = self.attempts[attempt_id]
        node = self.nodes[attempt.node_id]
        if attempt.finished_at is not None or not node.attempts or node.attempts[-1] != attempt_id:
            raise ValueError('attempt already finished or superseded')
        if not isinstance(status, str) or not status.strip():
            raise ValueError('attempt status must be a nonempty string')
        if not isinstance(command, list) or any(not isinstance(part, str) for part in command):
            raise ValueError('attempt command must be a list of strings')
        if not isinstance(stdout, str) or not isinstance(stderr, str):
            raise ValueError('attempt output must be text')
        if type(exit_code) is not int:
            raise ValueError('attempt exit_code must be an integer')
        attempt.status, attempt.command = status, command
        attempt.stdout, attempt.stderr, attempt.exit_code, attempt.finished_at = stdout, stderr, exit_code, now()
        self.attempt_history.append(self._attempt_history_entry(
            attempt, sequence=len(self.attempt_history), event="finished"))
        node = self.nodes[attempt.node_id]
        if node.status != NodeStatus.VERIFIED:
            node.status = NodeStatus.OPEN if status != "blocked" else NodeStatus.BLOCKED
        self.event("attempt_finished", attempt_id=attempt_id, node_id=attempt.node_id,
                   status=status, exit_code=exit_code)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorkflowState":
        schema_version = data.get('schema_version', 1)
        if schema_version != 1:
            raise ValueError(f'unsupported workflow state schema: {schema_version}')
        revision = data.get('revision', 0)
        if type(revision) is not int or revision < 0:
            raise ValueError('workflow state revision must be a nonnegative integer')
        state = cls(schema_version=schema_version, revision=revision,
                    project=data.get("project", "percolation"),
                    root_id=data.get("root_id"), registry=data.get("registry", {}), events=data.get("events", []),
                    manifest=data.get('manifest'), graph_artifacts=data.get('graph_artifacts', []),
                    global_closure=data.get('global_closure', {}))
        state.nodes = {k: ProofNode(**{**v, "status": NodeStatus(v["status"])}) for k, v in data.get("nodes", {}).items()}
        try:
            state.attempts = {k: Attempt(**{
                **v,
                "stdout": "" if v.get("stdout") is None else v.get("stdout", ""),
                "stderr": "" if v.get("stderr") is None else v.get("stderr", ""),
            }) for k, v in data.get("attempts", {}).items()}
        except (AttributeError, TypeError) as exc:
            raise ValueError("attempt record is malformed") from exc
        if "attempt_history" in data:
            state.attempt_history = data["attempt_history"]
        else:
            state.attempt_history = cls._reconstruct_legacy_attempt_history(state.attempts)
        state.agent_requests = data.get('agent_requests', {})
        state._validate_attempt_history()
        return state
