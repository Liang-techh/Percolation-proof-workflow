"""A durable coordinator boundary for Codex host-agent callbacks.

The module deliberately does not call a model provider. A host adapter writes
envelopes containing the raw agent result, and this cycle ingests them, collects
already-published compiler receipts, prepares the next dispatch batch, and emits
the next durable actions. Re-running a cycle is safe because bridge transitions
are idempotent and receipts are identity-checked.
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path

from .agent_bridge import (collect_candidate, prepare_requests, record_result, start_candidate,
                           lease_expired, reclaim_expired_agent, reclaim_dead_codex,
                           reclaim_dead_compile)
from .decomposition import ChildGoal, propose_decomposition
from .manifest import bind_manifest, load_verification_manifest
from .research import next_actions
from .reduction import close_verified_reductions
from .store import StateStore
from .verification import verify_and_register


def _persist_candidate_claim(store: StateStore, request_id: str, candidate: dict,
                             event_id: str | None) -> None:
    """Persist an agent receipt as an untrusted claim before coordinator compile.

    The claim is useful provenance, but it cannot advance the evidence stage or
    registry.  A normalized pending projection is completed only after the
    coordinator consumes a successful compiler receipt.
    """
    if 'receipt' not in candidate:
        return
    receipt = candidate['receipt']
    digest = hashlib.sha256(json.dumps(receipt, ensure_ascii=False,
                                       sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    state = store.load()
    request = state.agent_requests[request_id]
    prior = request.get('candidate_ingest')
    if (isinstance(prior, dict) and prior.get('receipt_sha256') == digest and
            prior.get('event_id') == event_id):
        return
    if not isinstance(receipt, dict):
        request['candidate_ingest'] = {
            'schema_version': 1, 'event_id': event_id, 'receipt_sha256': digest,
            'audit_status': 'rejected', 'audit_reasons': ['candidate.receipt must be an object'],
            'reported_candidate_status': None, 'reported_comparator_status': None,
            'evidence_stage': state.evidence_stage(request['node_id']).value,
            'comparator_status': 'pending', 'registry_status': 'pending',
        }
        request['candidate_receipt'] = receipt
    else:
        reasons = []
        if receipt.get('status') != 'compiled_candidate':
            reasons.append('receipt status is not compiled_candidate')
        request['candidate_receipt'] = receipt
        request['candidate_ingest'] = {
            'schema_version': 1, 'event_id': event_id, 'receipt_sha256': digest,
            'audit_status': 'pending' if not reasons else 'rejected',
            'audit_reasons': reasons or ['coordinator binding and comparator audit pending'],
            'reported_candidate_status': receipt.get('status'),
            'reported_comparator_status': receipt.get('comparator_status'),
            'evidence_stage': state.evidence_stage(request['node_id']).value,
            'comparator_status': 'pending', 'registry_status': 'pending',
        }
    state.event('candidate_receipt_claim_ingested', request_id=request_id,
                node_id=request['node_id'], event_id=event_id, receipt_sha256=digest,
                audit_status=request['candidate_ingest']['audit_status'],
                registry_promoted=False)
    store.save(state)


def _promote_compiled_candidate(store: StateStore, request_id: str,
                                comparator_command: list[str] | None,
                                trusted_project_map: dict[str, str] | None) -> dict:
    """Run the explicit coordinator-owned post-compile gates.

    A successful Lean source compile is only a candidate.  Promotion is attempted
    only when the callback explicitly requests promotion *and* the host cycle
    supplies the comparator command.  The command is never accepted from the
    agent callback.  This keeps old callbacks pending while closing the
    automatic ``compiled_candidate -> verify -> registry -> reduction cascade``
    path for fully specified coordinator invocations.
    """
    state = store.load()
    request = state.agent_requests[request_id]
    node = state.nodes[request['node_id']]
    if node.id in state.registry or node.status == 'verified':
        return {'status': 'verified', 'reason': 'candidate already registered', 'closed': []}
    prior = request.get('candidate_promotion')
    if isinstance(prior, dict) and prior.get('status') in {'verified', 'rejected'}:
        return dict(prior)
    callback = request.get('raw_callback') or {}
    candidate = callback.get('candidate') if isinstance(callback, dict) else None
    context = candidate.get('verification') if isinstance(candidate, dict) else None
    if context is None or not isinstance(context, dict) or context.get('requested') is not True:
        if not any(event.get('kind') == 'candidate_promotion_pending' and
                   event.get('request_id') == request_id for event in state.events):
            state.event('candidate_promotion_pending', request_id=request_id,
                        node_id=request['node_id'], reason='explicit verification context is required',
                        registry_promoted=False)
            store.save(state)
        return {'status': 'pending', 'reason': 'explicit coordinator promotion request is required',
                'closed': []}
    if comparator_command is None:
        return {'status': 'pending', 'reason': 'coordinator comparator command is required',
                'closed': []}
    if trusted_project_map is None or request_id not in trusted_project_map:
        return {'status': 'pending', 'reason': 'coordinator trusted project binding is required',
                'closed': []}
    if (not isinstance(comparator_command, list) or not comparator_command or
            not all(isinstance(item, str) and item for item in comparator_command)):
        raise ValueError('coordinator comparator command must be a nonempty string list')
    project = request.get('candidate_project')
    if not isinstance(project, str) or not project:
        raise ValueError('candidate project is required for coordinator verification')
    expected_project = Path(trusted_project_map[request_id]).resolve()
    if Path(project).resolve() != expected_project:
        raise ValueError('candidate project does not match coordinator trusted project binding')
    project = str(expected_project)
    aliases = []
    manifest_identity = state.manifest if isinstance(state.manifest, dict) else None
    try:
        accepted = verify_and_register(
            state, request['node_id'], project, comparator_command, store=store,
            artifact_aliases=aliases, manifest_identity=manifest_identity)
    except Exception as exc:
        state = store.load()
        state.agent_requests[request_id]['candidate_promotion'] = {
            'status': 'rejected', 'reason': repr(exc), 'closed': []}
        state.event('candidate_promotion_error', request_id=request_id,
                    node_id=request['node_id'], error=repr(exc),
                    registry_promoted=False)
        store.save(state)
        return {'status': 'rejected', 'reason': repr(exc), 'closed': []}
    if not accepted:
        outcome = {'status': 'rejected', 'reason': 'verification or comparator gate rejected',
                   'closed': []}
        state = store.load()
        state.agent_requests[request_id]['candidate_promotion'] = outcome
        store.save(state)
        return outcome
    closed: list[str] = []
    while True:
        newly_closed = close_verified_reductions(store)
        if not newly_closed:
            break
        closed.extend(newly_closed)
    state = store.load()
    state.event('candidate_registry_cascade_finished', request_id=request_id,
                node_id=request['node_id'], registry_promoted=True,
                closed=closed)
    state.agent_requests[request_id]['candidate_promotion'] = {
        'status': 'verified', 'reason': None, 'closed': closed}
    store.save(state)
    return {'status': 'verified', 'reason': None, 'closed': closed}


def run_host_cycle(store: StateStore, *, callback_dir: str | Path | None = None,
                   limit: int = 4, manifest: str | Path | None = None,
                   math_lane_policy: str = 'ordinary',
                   comparator_command: list[str] | None = None,
                   trusted_project_map: dict[str, str] | None = None) -> dict:
    if limit < 1:
        raise ValueError('positive dispatch limit required')
    state = store.load()
    state.validate()
    if trusted_project_map is not None:
        if (not isinstance(trusted_project_map, dict) or
                any(not isinstance(key, str) or not isinstance(value, str) or not value
                    for key, value in trusted_project_map.items())):
            raise ValueError('trusted_project_map must map request ids to nonempty paths')
    loaded_manifest = load_verification_manifest(manifest) if manifest is not None else None
    if loaded_manifest is not None:
        bind_manifest(store, loaded_manifest)
    accepted_callbacks = []
    started_compilations = []
    reclaimed_requests = []
    reclaimed_codex = []
    reclaimed_compilations = []
    errors = []
    for request in list(store.load().agent_requests.values()):
        if request.get('status') == 'bound':
            try:
                if reclaim_dead_codex(store, request['request_id']):
                    reclaimed_codex.append(request['request_id'])
            except Exception as exc:
                errors.append({'request_id': request.get('request_id'), 'error': repr(exc)})
    for request in list(store.load().agent_requests.values()):
        if request.get('status') == 'bound' and lease_expired(request):
            try:
                reclaim_expired_agent(store, request['request_id'])
                reclaimed_requests.append(request['request_id'])
            except Exception as exc:
                errors.append({'request_id': request.get('request_id'), 'error': repr(exc)})
    if callback_dir is not None:
        directory = Path(callback_dir).resolve()
        if not directory.is_dir():
            raise ValueError('callback directory does not exist')
        for path in sorted(directory.glob('*.json')):
            try:
                envelope = json.loads(path.read_text(encoding='utf-8'))
                request_id = envelope['request_id']
                agent_id = envelope['agent_id']
                legacy = 'protocol_version' not in envelope
                result = envelope.get('result') if legacy else envelope.get('payload')
                if not isinstance(request_id, str) or not isinstance(agent_id, str) or not isinstance(result, dict):
                    raise ValueError('callback envelope requires request_id, agent_id and object payload')
                request = store.load().agent_requests[request_id]
                if envelope.get('protocol_version', 1) != 1 or envelope.get('kind', 'agent_result') != 'agent_result':
                    raise ValueError('unsupported callback protocol or kind')
                if not legacy and (not envelope.get('attempt_id') or not envelope.get('event_id')):
                    raise ValueError('version 1 callback requires attempt_id and event_id')
                if envelope.get('attempt_id') not in (None, request['attempt_id']):
                    raise ValueError('callback belongs to a different attempt')
                state = store.load()
                if (not legacy and request.get('callback_event_id') == envelope.get('event_id') and
                        request.get('raw_callback') != envelope):
                    raise ValueError('callback event_id was reused with different envelope fields')
                if legacy and any(key in envelope for key in ('candidate', 'decomposition')):
                    raise ValueError('legacy callbacks cannot carry candidate or decomposition sidecars')
                if (not legacy and state.manifest and
                        envelope.get('manifest_sha256') != state.manifest.get('sha256')):
                    raise ValueError('callback belongs to a different verification manifest')
                record_result(store, request_id, agent_id, result,
                              attempt_id=envelope.get('attempt_id'),
                              event_id=envelope.get('event_id'),
                              callback_envelope=envelope)
                decomposition = envelope.get('decomposition')
                if decomposition is not None:
                    if not isinstance(decomposition, dict) or not isinstance(
                            decomposition.get('sketch'), str) or not isinstance(
                            decomposition.get('children'), list):
                        raise ValueError('decomposition requires sketch and children')
                    comparator_gate = decomposition.get('comparator_gate')
                    if not isinstance(comparator_gate, dict):
                        raise ValueError('decomposition requires comparator_gate context')
                    children = []
                    for child in decomposition['children']:
                        if not isinstance(child, dict) or not isinstance(child.get('name'), str) \
                                or not isinstance(child.get('statement'), str):
                            raise ValueError('decomposition child requires name and statement')
                        children.append(ChildGoal(child['name'], child['statement'],
                                                   child.get('proof_sketch', '')))
                    current = store.load().agent_requests[request_id]
                    if current.get('status') == 'reported':
                        state = store.load()
                        propose_decomposition(state, request['node_id'], decomposition['sketch'],
                                              children, agent_id=agent_id, store=store,
                                              comparator_gate=comparator_gate)
                candidate = envelope.get('candidate')
                if candidate is not None:
                    if not isinstance(candidate, dict) or not isinstance(candidate.get('project'), str) \
                            or not isinstance(candidate.get('source'), str):
                        raise ValueError('candidate requires project and source paths')
                    if trusted_project_map is not None:
                        expected = trusted_project_map.get(request_id)
                        if expected is None or Path(candidate['project']).resolve() != Path(expected).resolve():
                            raise ValueError('candidate project does not match coordinator trusted project binding')
                    _persist_candidate_claim(store, request_id, candidate, envelope.get('event_id'))
                    current = store.load().agent_requests[request_id]
                    if current.get('status') == 'reported':
                        candidate_sources = candidate.get('sources')
                        if candidate_sources is None:
                            process = start_candidate(store, request_id, candidate['project'], candidate['source'])
                        else:
                            process = start_candidate(store, request_id, candidate['project'], candidate['source'],
                                                      candidate_sources)
                        started_compilations.append({
                            'request_id': request_id,
                            'pid': process.pid,
                            'compile_job': store.load().agent_requests[request_id]['compile_job'],
                            'sources': store.load().agent_requests[request_id].get(
                                'artifact_sources', [candidate['source']])})
                    elif current.get('status') not in {'checking', 'checked'}:
                        raise ValueError('candidate callback is not attached to a reported request')
                accepted_callbacks.append(path.name)
            except Exception as exc:
                errors.append({'file': str(path), 'error': repr(exc)})

    collected = []
    state = store.load()
    for request in list(state.agent_requests.values()):
        if request.get('status') != 'checking':
            continue
        try:
            result = collect_candidate(store, request['request_id'])
            if result is not None:
                item = {'request_id': request['request_id'], 'compiled': result}
                if result:
                    item['promotion'] = _promote_compiled_candidate(
                        store, request['request_id'], comparator_command, trusted_project_map)
                collected.append(item)
            elif reclaim_dead_compile(store, request['request_id']):
                reclaimed_compilations.append(request['request_id'])
        except Exception as exc:
            errors.append({'request_id': request['request_id'], 'error': repr(exc)})

    # A successful compile is checkpointed as ``checked`` before the trusted
    # comparator is necessarily available.  Revisit such candidates on later
    # cycles so a newly supplied coordinator command can resume promotion.
    if comparator_command is not None:
        state = store.load()
        for request in list(state.agent_requests.values()):
            if request.get('status') != 'checked':
                continue
            attempt_id = request.get('compile_attempt_id')
            if not attempt_id or state.attempts.get(attempt_id, None) is None:
                continue
            if state.attempts[attempt_id].status != 'compiled':
                continue
            node = state.nodes[request['node_id']]
            if node.status == 'verified' or node.id in state.registry:
                continue
            callback = request.get('raw_callback') or {}
            candidate = callback.get('candidate') if isinstance(callback, dict) else None
            context = candidate.get('verification') if isinstance(candidate, dict) else None
            if not isinstance(context, dict) or context.get('requested') is not True:
                continue
            try:
                outcome = _promote_compiled_candidate(
                    store, request['request_id'], comparator_command, trusted_project_map)
                if outcome.get('status') != 'pending':
                    collected.append({'request_id': request['request_id'], 'compiled': True,
                                      'resumed_promotion': outcome})
            except Exception as exc:
                errors.append({'request_id': request['request_id'], 'error': repr(exc)})

    dispatch = prepare_requests(store, limit=limit,
                                math_lane_policy=math_lane_policy)
    state = store.load()
    state.event('host_cycle_finished', callbacks=len(accepted_callbacks),
                collected=collected, dispatch=len(dispatch), errors=errors)
    store.save(state)
    return {'accepted_callbacks': accepted_callbacks, 'started_compilations': started_compilations,
            'reclaimed_requests': reclaimed_requests,
            'reclaimed_codex': reclaimed_codex,
            'reclaimed_compilations': reclaimed_compilations,
            'collected': collected,
            'dispatch': dispatch, 'errors': errors, 'next_actions': next_actions(store)}
