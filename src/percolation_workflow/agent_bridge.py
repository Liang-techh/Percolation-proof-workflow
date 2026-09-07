"""Durable requests for the host's Codex multi-agent tools; never simulates an agent."""
import json
import uuid
import os
import subprocess
import sys
import hashlib
import re
import tempfile
from datetime import datetime, timedelta, timezone
from .store import StateStore
from .registry import audit_registry
from .model import EvidenceStage, now
from .scheduler import candidate_identity, obstruction_rank, rank_frontier
from .math_frontier import rank_formalizable_frontier
from pathlib import Path


# The host-facing repair path must have a durable finite bound.  The injected
# in-process repair helper has its own parameter, but dispatch requests need a
# default policy too so a failed node cannot generate an unbounded stream of
# identical host jobs.
DEFAULT_MAX_REPAIR_ROUNDS = 3


class _ReceiptIdentityError(ValueError):
    """A receipt is well-formed but belongs to a different execution."""



def _lease_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError('agent lease timestamp is malformed') from exc
    if parsed.tzinfo is None:
        raise ValueError('agent lease timestamp must include a timezone')
    return parsed.astimezone(timezone.utc)


def _order_compile_paths(project: Path, source_paths: list[Path], entrypoint: Path) -> list[Path]:
    """Topologically order an explicit Lean source bundle by local imports."""
    module_paths = {
        path.relative_to(project).with_suffix('').as_posix().replace('/', '.'): path
        for path in source_paths
    }
    dependencies: dict[Path, set[Path]] = {path: set() for path in source_paths}
    import_pattern = re.compile(r'^\s*import\s+(.+?)(?:\s+--.*)?$')
    for path in source_paths:
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except (OSError, UnicodeError) as exc:
            raise ValueError(f'cannot read candidate source bundle file: {path}') from exc
        for line in lines:
            match = import_pattern.match(line)
            if match is None:
                continue
            for module in match.group(1).split():
                dependency = module_paths.get(module)
                if dependency is not None and dependency != path:
                    dependencies[path].add(dependency)

    ordered: list[Path] = []
    visiting: set[Path] = set()
    visited: set[Path] = set()

    def visit(path: Path) -> None:
        if path in visiting:
            raise ValueError('candidate source bundle has cyclic local imports')
        if path in visited:
            return
        visiting.add(path)
        for dependency in sorted(dependencies[path], key=lambda value: value.as_posix()):
            visit(dependency)
        visiting.remove(path)
        visited.add(path)
        ordered.append(path)

    for path in sorted((path for path in source_paths if path != entrypoint),
                       key=lambda value: value.as_posix()):
        visit(path)
    visit(entrypoint)
    return ordered


def lease_expired(request: dict, *, at: datetime | None = None) -> bool:
    """Return whether an active request lease has elapsed; absent leases are legacy-safe."""
    lease = request.get('lease')
    if not isinstance(lease, dict) or lease.get('status') != 'active':
        return False
    return _lease_time(lease.get('expires_at')) <= (at or datetime.now(timezone.utc))


def _durable_json(path: Path, value: dict) -> None:
    """Write a small process marker atomically before exposing its phase."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            json.dump(value, output, ensure_ascii=False, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
def prepare_requests(store: StateStore, *, limit: int = 4,
                     max_repair_rounds: int = DEFAULT_MAX_REPAIR_ROUNDS,
                     math_lane_policy: str = 'ordinary') -> list[dict]:
    if not store.path.is_file() or limit < 1:
        raise ValueError('existing research state and positive limit required')
    if type(max_repair_rounds) is not int or max_repair_rounds < 1:
        raise ValueError('max_repair_rounds must be a positive integer')
    if math_lane_policy not in {'ordinary', 'formalizable'}:
        raise ValueError("math_lane_policy must be 'ordinary' or 'formalizable'")
    state = store.load()
    state.validate()
    if any(r['status'] != 'current' for r in audit_registry(state).values()):
        raise ValueError('registry must be checked in its artifact environment before dispatch')
    # Use the obstruction-aware scheduler on the actual host-dispatch path.
    # Candidate de-duplication happens after completed/pending attempts are
    # filtered, so a finished representative cannot hide a live duplicate.
    eligible = {}
    repair_statuses = {'compile_error', 'verification_error', 'provenance_rejected',
                       'verification_rejected', 'strict_admission_rejected',
                       'agent_error', 'agent_timeout'}
    exhausted_now = []
    for node in state.frontier():
        if node.metadata.get('repair_exhausted'):
            continue
        if node.metadata.get('statement_status') != 'indexed':
            continue
        if node.metadata.get('proposed_by') and not any(
            proposal.get('status') == 'sketch_checked' and node.id in proposal['children']
            for parent in state.nodes.values()
            for proposal in parent.metadata.get('reduction_proposals', [])):
            continue
        repair_round = sum(1 for attempt_id in node.attempts
                           if state.attempts[attempt_id].status in repair_statuses)
        latest_attempt = state.attempts[node.attempts[-1]] if node.attempts else None
        if (latest_attempt is not None and latest_attempt.status in repair_statuses and
                repair_round >= max_repair_rounds):
            node.metadata.update({
                'repair_exhausted': True,
                'repair_exhausted_round': repair_round,
                'repair_max_rounds': max_repair_rounds,
            })
            exhausted_now.append({'node_id': node.id, 'round': repair_round,
                                  'max_rounds': max_repair_rounds})
            continue
        if node.attempts:
            latest = node.attempts[-1]
            if state.attempts[latest].status == 'compiled' or (
                state.attempts[latest].status == 'candidate_ready' and any(
                r['attempt_id'] == latest and r['status'] == 'reported'
                    for r in state.agent_requests.values())):
                continue
        eligible[node.id] = lambda _: None

    requests = []
    ordered = rank_frontier(state, eligible)
    if math_lane_policy == 'formalizable':
        formalizable = set(rank_formalizable_frontier(state, eligible))
        ordered = [node_id for node_id in ordered if node_id in formalizable]
    for node_id in ordered:
        node = state.nodes[node_id]
        request_id = uuid.uuid4().hex
        diagnostics = [{'status': state.attempts[a].status, 'stdout': state.attempts[a].stdout,
                        'stderr': state.attempts[a].stderr} for a in node.attempts]
        diagnostics.extend({'status': 'agent_reported_compile', 'stdout': event['report']['stdout'],
                            'stderr': event['report']['stderr'], 'exit_code': event['report']['exit_code'],
                            'evidence_kind': 'agent-owned execution log, not coordinator verification'}
                           for event in state.events if event['kind'] == 'agent_compile_log_ingested'
                           and event['node_id'] == node.id)
        proposals = node.metadata.get('reduction_proposals', [])
        accepted_reduction = next((proposal for proposal in reversed(proposals)
                                   if proposal.get('status') in {'sketch_checked', 'sketch_accepted'}
                                   and proposal.get('reduction_status') == 'accepted'), None)
        repair_of = None
        if node.attempts:
            latest_attempt = state.attempts[node.attempts[-1]]
            if latest_attempt.status in repair_statuses:
                repair_of = latest_attempt
        work_kind = ('repair_parent_assembly' if accepted_reduction else 'repair') if repair_of else (
            'parent_assembly' if accepted_reduction else 'direct_proof')
        repair_context = None
        if repair_of is not None:
            repair_context = {
                'attempt_id': repair_of.id,
                'status': repair_of.status,
                'command': repair_of.command,
                'stdout': repair_of.stdout,
                'stderr': repair_of.stderr,
                'exit_code': repair_of.exit_code,
            }
        request = {'request_id': request_id, 'node_id': node.id, 'name': node.name,
                   'statement': node.statement, 'proof_sketch': node.proof_sketch,
                   'closability': state.frontier_closability(node.id),
                   'work_kind': work_kind,
                   'reduction_proposal_id': (accepted_reduction.get('proposal_id')
                                             if accepted_reduction else None),
                   'repair_of_attempt_id': repair_of.id if repair_of else None,
                   'repair_round': repair_round,
                   'repair_policy': {'max_rounds': max_repair_rounds,
                                    'policy': 'bounded-host-repair-v1'},
                   'repair_context': repair_context,
                   'frontier_repair_contract': node.metadata.get(
                       'frontier_repair_contract'),
                   'decomposition_contract': {
                       'required_fields': ['sketch', 'children', 'comparator_gate'],
                       'comparator_gate_fields_per_child': [
                           'source_identity', 'source_statement', 'covered_source',
                           'target_theorem_identity'],
                       'admission': 'fail_closed_before_child_creation',
                   },
                   'dependencies': [state.registry[d] for d in node.dependencies],
                   'required_node_ids': list(node.metadata.get('required_node_ids', [])),
                   # Cross-branch inputs are deliberately separate from the
                   # ordinary parent dependency list.  Include the exact
                   # coordinator-owned receipts in the dispatch packet so an
                   # agent can bind the already-verified input without
                   # reconstructing it from a mutable global state file.
                   'required_inputs': {
                       required_id: state.registry[required_id]
                       for required_id in node.metadata.get('required_node_ids', [])
                   },
                   'diagnostics': diagnostics, 'status': 'awaiting_dispatch', 'agent_id': None}
        request['scheduler'] = {
            'obstruction_rank': obstruction_rank(node),
            'candidate_identity': candidate_identity(node),
            'policy': 'obstruction-aware-v1',
            'math_lane_policy': math_lane_policy,
        }
        request['attempt_id'] = state.begin_attempt(node.id, 'dispatch-pending:' + request_id)
        request.update(protocol_version=1, action='dispatch_agent',
                       manifest_sha256=(state.manifest or {}).get('sha256'))
        state.agent_requests[request_id] = request
        requests.append(request)
        if len(requests) >= limit:
            break
    if exhausted_now:
        for exhausted in exhausted_now:
            state.event('repair_loop_exhausted', **exhausted)
    state.event('agent_requests_prepared', request_ids=[r['request_id'] for r in requests],
                max_repair_rounds=max_repair_rounds)
    store.save(state)
    return requests


def bind_agent(store: StateStore, request_id: str, agent_id: str, *, lease_seconds: int = 3600,
               host_run_dir: str | None = None) -> None:
    if type(lease_seconds) is not int or lease_seconds < 1:
        raise ValueError('agent lease_seconds must be a positive integer')
    state = store.load()
    request = state.agent_requests[request_id]
    if not agent_id.strip():
        raise ValueError('real host agent id required')
    if request['status'] == 'bound' and request['agent_id'] == agent_id:
        return
    if request['status'] != 'awaiting_dispatch':
        raise ValueError('request already bound or finished')
    if any(r.get('agent_id') == agent_id for r in state.agent_requests.values()):
        raise ValueError('a fresh host agent is required for each request to reject old callbacks')
    acquired = datetime.now(timezone.utc)
    request.update(status='bound', agent_id=agent_id, lease={
        'owner': agent_id,
        'status': 'active',
        'acquired_at': acquired.isoformat(),
        'renewed_at': acquired.isoformat(),
        'expires_at': (acquired + timedelta(seconds=lease_seconds)).isoformat(),
    })
    if host_run_dir is not None:
        if not isinstance(host_run_dir, str) or not host_run_dir.strip():
            raise ValueError('host_run_dir must be a nonempty string')
        request['host_run_dir'] = host_run_dir
    state.rebind_attempt(request['attempt_id'], agent_id)
    state.event('host_agent_bound', request_id=request_id, agent_id=agent_id)
    store.save(state)


def renew_agent(store: StateStore, request_id: str, agent_id: str, *, lease_seconds: int = 3600) -> None:
    """Extend a live agent lease; an expired lease must be explicitly reclaimed first."""
    if type(lease_seconds) is not int or lease_seconds < 1:
        raise ValueError('agent lease_seconds must be a positive integer')
    state = store.load()
    request = state.agent_requests[request_id]
    if request.get('status') != 'bound' or request.get('agent_id') != agent_id:
        raise ValueError('only the bound host agent can renew a lease')
    lease = request.get('lease')
    if not isinstance(lease, dict) or lease.get('owner') != agent_id or lease.get('status') != 'active':
        raise ValueError('request has no active agent lease')
    current = datetime.now(timezone.utc)
    if lease_expired(request, at=current):
        raise ValueError('agent lease has expired; reclaim it before renewal')
    lease.update(renewed_at=current.isoformat(),
                 expires_at=(current + timedelta(seconds=lease_seconds)).isoformat())
    state.event('host_agent_lease_renewed', request_id=request_id, agent_id=agent_id,
                expires_at=lease['expires_at'])
    store.save(state)


def reclaim_expired_agent(store: StateStore, request_id: str) -> None:
    """Close an expired bound attempt and make the node dispatchable again."""
    state = store.load()
    request = state.agent_requests[request_id]
    if request.get('status') != 'bound' or not lease_expired(request):
        raise ValueError('request does not have an expired bound lease')
    attempt_id = request.get('attempt_id')
    node = state.nodes[request['node_id']]
    if not attempt_id or not node.attempts or node.attempts[-1] != attempt_id:
        raise ValueError('expired request attempt was superseded')
    state.finish_attempt(attempt_id, status='agent_timeout', command=[], stdout='',
                         stderr='host-agent lease expired', exit_code=124)
    request['status'] = 'expired'
    request['lease'].update(status='expired', expired_at=now())
    state.event('host_agent_lease_expired', request_id=request_id,
                agent_id=request.get('agent_id'), attempt_id=attempt_id)
    store.save(state)


def reclaim_dead_codex(store: StateStore, request_id: str) -> bool | None:
    """Reclaim a Codex host process proven dead by its durable start marker.

    ``None`` means there is no trustworthy marker, the process is still alive,
    or a finished marker exists and the callback may still be in flight.  A
    reclaimed request is recorded as ``agent_timeout`` so the ordinary repair
    scheduler, rather than this recovery helper, creates the next attempt.
    """
    state = store.load()
    request = state.agent_requests[request_id]
    if request.get('status') != 'bound' or not request.get('host_run_dir'):
        return None
    run_dir = Path(request['host_run_dir']).resolve()
    started_path = run_dir / 'started.json'
    finished_path = run_dir / 'finished.json'
    if not started_path.is_file() or finished_path.is_file():
        return None
    marker = json.loads(started_path.read_text(encoding='utf-8'))
    if (marker.get('request_id') != request_id or
            marker.get('attempt_id') != request.get('attempt_id') or
            marker.get('agent_id') != request.get('agent_id') or
            type(marker.get('pid')) is not int):
        raise ValueError('Codex start marker does not match the bound request')
    if _process_alive(marker['pid']):
        return None
    attempt_id = request.get('attempt_id')
    node = state.nodes[request['node_id']]
    if not attempt_id or not node.attempts or node.attempts[-1] != attempt_id:
        raise ValueError('dead Codex attempt was superseded')
    state.finish_attempt(attempt_id, status='agent_timeout', command=[], stdout='',
                         stderr=f"Codex host process {marker['pid']} exited before callback",
                         exit_code=124)
    request['status'] = 'expired'
    lease = request.get('lease')
    if isinstance(lease, dict):
        lease.update(status='expired', expired_at=now())
    state.event('codex_process_reclaimed', request_id=request_id, attempt_id=attempt_id,
                agent_id=request.get('agent_id'), pid=marker['pid'])
    store.save(state)
    return True


def ingest_compile_log(store: StateStore, request_id: str, path: str | Path) -> None:
    """Preserve an agent-owned raw compile log without terminating its live request.

    These reports are not trusted coordinator receipts and cannot promote any node.
    Hash identity is idempotent; changed log bytes are retained as a separate observation.
    """
    path = Path(path).resolve()
    raw = path.read_bytes()
    report = json.loads(raw.decode('utf-8-sig'))
    if report.get('request_id') != request_id:
        raise ValueError('compile log belongs to another request')
    if not isinstance(report.get('command'), (str, list)) or not all(
        isinstance(report.get(field), str) for field in ('stdout', 'stderr')) or type(report.get('exit_code')) is not int:
        raise ValueError('compile log must include raw command, output streams and exit code')
    state = store.load()
    request = state.agent_requests[request_id]
    if not request.get('agent_id'):
        raise ValueError('compile log requires a bound host agent')
    if report.get('agent_id') not in (None, request.get('agent_id')):
        raise ValueError('compile log belongs to another host agent')
    digest = hashlib.sha256(raw).hexdigest()
    if any(event['kind'] == 'agent_compile_log_ingested' and event['request_id'] == request_id
           and event['sha256'] == digest for event in state.events):
        return
    state.event('agent_compile_log_ingested', request_id=request_id, node_id=request['node_id'],
                agent_id=request['agent_id'], path=str(path), sha256=digest, report=report,
                evidence_kind='agent-owned execution log, not coordinator verification')
    store.save(state)


def record_result(store: StateStore, request_id: str, agent_id: str, result: dict, *,
                  attempt_id: str | None = None, event_id: str | None = None,
                  callback_envelope: dict | None = None) -> None:
    """Preserve the exact terminal tool payload; completion is not Lean verification."""
    state = store.load()
    request = state.agent_requests[request_id]
    if request['agent_id'] != agent_id:
        raise ValueError('result belongs to a different host agent')
    if request.get('status') == 'bound' and lease_expired(request):
        raise ValueError('agent lease has expired; reclaim it before recording a result')
    if attempt_id is not None and request['attempt_id'] != attempt_id:
        raise ValueError('result belongs to a different attempt')
    if event_id is not None and not event_id.strip():
        raise ValueError('callback event_id must be nonempty')
    if event_id:
        prior = any(event.get('kind') == 'host_agent_result_recorded'
                    and event.get('request_id') == request_id
                    and event.get('event_id') == event_id for event in state.events)
        if prior:
            if request.get('raw_result') != result:
                raise ValueError('callback event_id was reused with different payload')
            return
    if request['status'] in {'reported', 'checking', 'checked', 'decomposed'} and request.get('raw_result') == result:
        return
    if request['status'] != 'bound' or not isinstance(result, dict):
        raise ValueError('expected terminal result for a bound request')
    terminal = result.get('status', {}).get(agent_id)
    if not isinstance(terminal, dict) or not ({'completed', 'errored'} & terminal.keys()):
        raise ValueError('tool result does not establish agent completion')
    success = 'completed' in terminal
    state.finish_attempt(request['attempt_id'], status='candidate_ready' if success else 'agent_error',
                         command=[], stdout=json.dumps(result, ensure_ascii=False), stderr='',
                         exit_code=0 if success else 1)
    request.update(status='reported', raw_result=result, callback_event_id=event_id)
    lease = request.get('lease')
    if isinstance(lease, dict) and lease.get('status') == 'active':
        lease.update(status='released', released_at=now())
    if callback_envelope is not None:
        request['raw_callback'] = callback_envelope
    state.event('host_agent_result_recorded', request_id=request_id, agent_id=agent_id,
                attempt_id=request['attempt_id'], event_id=event_id)
    store.save(state)


def _start_coordinator_compile(store: StateStore, request_id: str,
                               project: Path, source: Path, *, event_kind: str,
                               sources: list[str | Path] | None = None) -> subprocess.Popen:
    """Checkpoint one coordinator compile and launch its receipt-producing worker."""
    state = store.load()
    request = state.agent_requests[request_id]
    project, source = Path(project).resolve(), Path(source).resolve()
    if not source.is_file() or not source.is_relative_to(project) or source.suffix != '.lean':
        raise ValueError('candidate must be a Lean source inside its assigned project')
    source_paths = [source]
    if sources is not None:
        if not isinstance(sources, (list, tuple)) or not sources:
            raise ValueError('candidate source bundle must be a nonempty list')
        source_paths = []
        for value in sources:
            path = Path(value).resolve()
            if (path.suffix != '.lean' or not path.is_file() or
                    not path.is_relative_to(project) or path in source_paths):
                raise ValueError('candidate source bundle contains an invalid or duplicate Lean source')
            source_paths.append(path)
        if source not in source_paths:
            raise ValueError('candidate entrypoint is missing from its source bundle')
    attempt = state.begin_attempt(request['node_id'], 'compiler-coordinator', str(source))
    directory = store.path.resolve().parent / (store.path.name + '.jobs') / attempt
    directory.mkdir(parents=True)
    compile_paths = _order_compile_paths(project, source_paths, source)
    commands = [['lake', 'env', 'lean', '-R', str(project), '-o',
                 str(path.with_suffix('.olean')), str(path)]
                for path in compile_paths]
    command = commands[-1]
    job = {'attempt_id': attempt, 'request_id': request_id, 'project': str(project),
           'command': command, 'commands': commands,
           'sources': [str(path) for path in source_paths],
           'compile_sources': [str(path) for path in compile_paths]}
    _durable_json(directory / 'job.json', job)
    _durable_json(directory / 'coordinator-intent.json', {
        'schema_version': 1, 'phase': 'launching', 'attempt_id': attempt,
        'request_id': request_id, 'coordinator_pid': os.getpid(),
        'created_at': now(),
    })
    request.update(status='checking', compile_attempt_id=attempt, artifact=str(source),
                   artifact_sources=[str(path) for path in source_paths],
                   artifact_compile_commands=commands,
                   compile_job=str(directory), candidate_project=str(project))
    state.event(event_kind, request_id=request_id, attempt_id=attempt,
                node_id=request['node_id'], source=str(source),
                sources=[str(path) for path in source_paths])
    store.save(state)
    env = dict(os.environ)
    env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1]) + os.pathsep + env.get('PYTHONPATH', '')
    with (directory / 'worker.log').open('ab') as output:
        process = subprocess.Popen([sys.executable, '-m', 'percolation_workflow.compile_worker', str(directory)],
            env=env, stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    _durable_json(directory / 'spawned.json', {
        'schema_version': 1, 'phase': 'spawned', 'attempt_id': attempt,
        'request_id': request_id, 'coordinator_pid': os.getpid(),
        'worker_pid': process.pid, 'created_at': now(),
    })
    return process


def start_candidate(store: StateStore, request_id: str, project: str | Path,
                    source: str | Path, sources: list[str | Path] | None = None) -> subprocess.Popen:
    """Checkpoint ownership before dispatch; the worker persists its own result.

    A single coordinator is required. Missing receipts never trigger an automatic
    restart: use the returned live process handle or inspect worker.log.
    """
    state = store.load()
    request = state.agent_requests[request_id]
    if request['status'] != 'reported':
        raise ValueError('candidate must be reported and not already checked')
    original = state.attempts[request['attempt_id']]
    if original.status != 'candidate_ready':
        raise ValueError('failed agent has no successful candidate report')
    node = state.nodes[request['node_id']]
    if not node.attempts or node.attempts[-1] != request['attempt_id']:
        raise ValueError('candidate report was superseded by a newer attempt')
    return _start_coordinator_compile(store, request_id, Path(project), Path(source),
                                      event_kind='candidate_compile_started', sources=sources)


def retry_candidate(store: StateStore, request_id: str, project: str | Path | None = None,
                    source: str | Path | None = None) -> subprocess.Popen:
    """Explicitly retry a failed coordinator compile while retaining its diagnostics."""
    state = store.load()
    request = state.agent_requests[request_id]
    if request.get('status') != 'checked':
        raise ValueError('candidate request is not at a checked checkpoint')
    failed_id = request.get('compile_attempt_id')
    if not failed_id or state.attempts[failed_id].status != 'compile_error':
        raise ValueError('candidate has no failed coordinator compile to retry')
    callback = request.get('raw_callback') or {}
    candidate = callback.get('candidate') if isinstance(callback, dict) else None
    project = project or request.get('candidate_project') or (candidate or {}).get('project')
    source = source or request.get('artifact') or (candidate or {}).get('source')
    sources = request.get('artifact_sources') or (candidate or {}).get('sources')
    if not project or not source:
        raise ValueError('retry requires the original candidate project and source')
    return _start_coordinator_compile(store, request_id, Path(project), Path(source),
                                      event_kind='candidate_compile_retry_started', sources=sources)


def collect_candidate(store: StateStore, request_id: str) -> bool | None:
    """Resume by consuming an atomic result; absence means unknown, never failed."""
    state = store.load()  # Do not overwrite callbacks saved while compilation ran.
    request = state.agent_requests[request_id]
    if request['status'] == 'checked':
        return state.attempts[request['compile_attempt_id']].status == 'compiled'
    if request['status'] != 'checking':
        raise ValueError('request has no checkpointed compiler job')
    receipt_path = Path(request['compile_job']) / 'result.json'
    if not receipt_path.is_file():
        return None
    attempt = request['compile_attempt_id']
    root = request.get('candidate_project') or str(Path(request['artifact']).parent)
    commands = request.get('artifact_compile_commands')
    command = commands[-1] if isinstance(commands, list) and commands else (
        ['lake', 'env', 'lean', '-R', root, request['artifact']])
    try:
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        if not isinstance(receipt, dict):
            raise TypeError('receipt must be an object')
        if receipt.get('attempt_id') != attempt or receipt.get('request_id') != request_id:
            raise _ReceiptIdentityError('compiler receipt belongs to another execution')
        result = receipt['result']
        if not isinstance(result, dict):
            raise TypeError('receipt result must be an object')
        if result['command'] != command or result['ok'] != (result['exit_code'] == 0):
            raise ValueError('inconsistent compiler receipt')
        expected_steps = request.get('artifact_compile_commands')
        steps = receipt.get('steps')
        if expected_steps is not None:
            if not isinstance(steps, list) or [step.get('command') for step in steps] != expected_steps:
                raise ValueError('inconsistent compiler bundle receipt')
    except _ReceiptIdentityError:
        # A receipt from a different execution is a stale/foreign artifact,
        # not evidence about this attempt.  Keep the historic fail-closed API
        # for callers that need to investigate the identity violation.
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        # A published but unreadable receipt must not leave the request in
        # ``checking`` forever.  Finish the coordinator attempt with the raw
        # failure reason; the original file remains in place for forensic
        # inspection and a normal repair request can now be scheduled.
        state = store.load()
        current_request = state.agent_requests[request_id]
        current_attempt = state.attempts[attempt]
        node = state.nodes[current_request['node_id']]
        if (current_request.get('status') != 'checking' or
                node.attempts[-1] != attempt or current_attempt.finished_at is not None):
            raise ValueError('corrupt compiler receipt belongs to a superseded attempt') from exc
        detail = f'invalid compiler receipt: {type(exc).__name__}: {exc}'
        state.finish_attempt(attempt, status='compile_error', command=command,
                             stdout='', stderr=detail, exit_code=124)
        current_request.update(status='checked', receipt_status='invalid',
                               receipt_error=detail, receipt_path=str(receipt_path))
        state.event('candidate_receipt_rejected', request_id=request_id,
                    attempt_id=attempt, path=str(receipt_path), reason=detail)
        store.save(state)
        return False
    state.finish_attempt(attempt, status='compiled' if result['ok'] else 'compile_error',
                         command=command, stdout=result['stdout'], stderr=result['stderr'],
                         exit_code=result['exit_code'])
    if result['ok']:
        # A coordinator-verified Lean compile is enough for the evidence stage,
        # but never for theorem closure.  Comparator and registry remain
        # explicit downstream gates.
        state.set_evidence_stage(request['node_id'], EvidenceStage.COMPILED_CANDIDATE)
        ingest = request.get('candidate_ingest')
        if isinstance(ingest, dict):
            ingest.update(evidence_stage=EvidenceStage.COMPILED_CANDIDATE.value,
                          candidate_status='compiled_candidate',
                          comparator_status='pending', registry_status='pending')
            request['candidate_manifest'] = {
                'schema_version': 1,
                'status': 'compiled_candidate',
                'candidate_status': 'compiled_candidate',
                'comparator_status': 'pending',
                'registry_status': 'pending',
                'receipt_sha256': ingest.get('receipt_sha256'),
            }
    request.update(status='checked')
    state.event('candidate_checked', request_id=request_id, attempt_id=attempt, compiled=result['ok'])
    store.save(state)
    return result['ok']


def _process_alive(pid: int) -> bool:
    """Best-effort liveness check for a durable compiler-worker marker."""
    if type(pid) is not int or pid <= 0:
        raise ValueError('compiler worker pid is malformed')
    if os.name == 'nt':
        # ``os.kill(pid, 0)`` is not a reliable liveness test on Windows: it
        # can continue to succeed for a child process after the parent has
        # already reaped it.  Query the process exit code instead, so launch
        # recovery can distinguish a live worker from a dead one.
        import ctypes

        process_query_limited_information = 0x1000
        still_active = 259
        error_access_denied = 5
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
        kernel32.OpenProcess.restype = ctypes.c_void_p
        kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
        kernel32.GetExitCodeProcess.restype = ctypes.c_int
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_int
        handle = kernel32.OpenProcess(process_query_limited_information, 0, pid)
        if not handle:
            # Access denial is conservatively treated as live; an invalid PID
            # or another lookup failure is treated as dead.
            return ctypes.get_last_error() == error_access_denied
        try:
            exit_code = ctypes.c_uint32()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                return ctypes.get_last_error() == error_access_denied
            return exit_code.value == still_active
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def reclaim_dead_compile(store: StateStore, request_id: str) -> bool | None:
    """Close a compiler attempt whose worker died before publishing a receipt.

    ``None`` means the worker is still live, the durable start marker is not yet
    available, or a receipt should be collected first.  A reclaimed attempt is
    deliberately recorded as a compile error so the ordinary frontier scheduler
    creates a fresh repair request with the exact failure context.
    """
    state = store.load()
    request = state.agent_requests[request_id]
    if request.get('status') != 'checking':
        return None
    receipt_path = Path(request['compile_job']) / 'result.json'
    if receipt_path.is_file():
        return None
    marker_path = Path(request['compile_job']) / 'started.json'
    if marker_path.is_file():
        marker = json.loads(marker_path.read_text(encoding='utf-8'))
        pid = marker.get('pid')
        if marker.get('attempt_id') != request.get('compile_attempt_id'):
            raise ValueError('compiler start marker belongs to another execution')
        if _process_alive(pid):
            return None
        recovery_reason = 'worker exited without publishing a receipt'
        dead_pid = pid
    else:
        intent_path = Path(request['compile_job']) / 'coordinator-intent.json'
        if not intent_path.is_file():
            return None
        intent = json.loads(intent_path.read_text(encoding='utf-8'))
        if (intent.get('attempt_id') != request.get('compile_attempt_id') or
                intent.get('request_id') != request_id):
            raise ValueError('coordinator launch intent belongs to another execution')
        spawned_path = Path(request['compile_job']) / 'spawned.json'
        if spawned_path.is_file():
            spawned = json.loads(spawned_path.read_text(encoding='utf-8'))
            if (spawned.get('attempt_id') != request.get('compile_attempt_id') or
                    spawned.get('request_id') != request_id):
                raise ValueError('compiler spawn marker belongs to another execution')
            worker_pid = spawned.get('worker_pid')
            if _process_alive(worker_pid):
                return None
            dead_pid = worker_pid
            recovery_reason = 'worker exited before publishing its start marker or receipt'
        else:
            coordinator_pid = intent.get('coordinator_pid')
            if _process_alive(coordinator_pid):
                return None
            dead_pid = coordinator_pid
            recovery_reason = 'coordinator exited before launching compiler worker'
    attempt_id = request['compile_attempt_id']
    node = state.nodes[request['node_id']]
    if not node.attempts or node.attempts[-1] != attempt_id:
        raise ValueError('dead compiler attempt was superseded')
    root = request.get('candidate_project') or str(Path(request['artifact']).parent)
    commands = request.get('artifact_compile_commands')
    command = commands[-1] if isinstance(commands, list) and commands else (
        ['lake', 'env', 'lean', '-R', root, request['artifact']])
    state.finish_attempt(attempt_id, status='compile_error', command=command, stdout='',
                         stderr=f'{recovery_reason}; dead pid {dead_pid}',
                         exit_code=125)
    request.update(status='checked')
    state.event('compiler_worker_reclaimed', request_id=request_id, attempt_id=attempt_id,
                pid=dead_pid, reason=recovery_reason)
    store.save(state)
    return True


def check_candidate(store: StateStore, request_id: str, project: str | Path, source: str | Path) -> bool:
    process = start_candidate(store, request_id, project, source)
    process.wait()
    result = collect_candidate(store, request_id)
    if result is None:
        raise RuntimeError('compiler worker terminated without a receipt; inspect worker.log; no automatic retry')
    return result
