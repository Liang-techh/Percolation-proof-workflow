from __future__ import annotations

from contextlib import contextmanager
import hashlib
import hmac
import json
import os
from pathlib import Path
import time
from .model import WorkflowState


class ConcurrentStateUpdate(RuntimeError):
    """A stale coordinator attempted to overwrite a newer state revision."""


class CheckpointIntegrityError(RuntimeError):
    """A persisted workflow checkpoint failed its integrity check."""


class StateStore:
    _CHECKSUM_FIELD = 'state_checksum'

    def __init__(self, path: str | Path):
        self.path = Path(path)

    @classmethod
    def _checksum(cls, payload: dict) -> str:
        """Hash the canonical checkpoint payload without hashing the hash itself."""
        state_payload = dict(payload)
        state_payload.pop(cls._CHECKSUM_FIELD, None)
        canonical = json.dumps(
            state_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':'),
            allow_nan=False,
        ).encode('utf-8')
        return hashlib.sha256(canonical).hexdigest()

    @classmethod
    def _verify_checksum(cls, payload: object) -> dict:
        if not isinstance(payload, dict):
            raise CheckpointIntegrityError('workflow checkpoint must be a JSON object')
        # Checkpoints written before checksum support (including Route-B revision
        # 92) remain readable. Every subsequent save adds the checksum.
        if cls._CHECKSUM_FIELD not in payload:
            return payload
        actual = payload[cls._CHECKSUM_FIELD]
        if not isinstance(actual, str):
            raise CheckpointIntegrityError('workflow checkpoint checksum is malformed')
        try:
            expected = cls._checksum(payload)
        except (TypeError, ValueError) as exc:
            raise CheckpointIntegrityError(
                'workflow checkpoint cannot be checksummed canonically') from exc
        if not hmac.compare_digest(actual, expected):
            raise CheckpointIntegrityError('workflow checkpoint checksum mismatch')
        return payload

    def _read_payload(self) -> dict:
        try:
            payload = json.loads(self.path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise CheckpointIntegrityError('workflow checkpoint is not valid JSON') from exc
        return self._verify_checksum(payload)

    @contextmanager
    def _lock(self):
        """Serialize writers using a small cross-platform advisory lock file."""
        lock_path = self.path.with_suffix(self.path.suffix + '.lock')
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open('a+b') as handle:
            handle.seek(0)
            if os.name == 'nt':
                import msvcrt
                handle.write(b'0')
                handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if os.name == 'nt':
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _read_revision(self) -> int:
        if not self.path.exists():
            return 0
        revision = self._read_payload().get('revision', 0)
        if type(revision) is not int or revision < 0:
            raise CheckpointIntegrityError(
                'workflow checkpoint revision must be a nonnegative integer')
        return revision

    def load(self) -> WorkflowState:
        with self._lock():
            if not self.path.exists():
                return WorkflowState()
            return WorkflowState.from_dict(self._read_payload())

    def save(self, state: WorkflowState) -> None:
        state.validate()
        with self._lock():
            current = self._read_revision()
            if current != state.revision:
                raise ConcurrentStateUpdate(
                    f'state revision changed from {state.revision} to {current}')
            next_revision = state.revision + 1
            payload = state.to_dict()
            payload['revision'] = next_revision
            payload[self._CHECKSUM_FIELD] = self._checksum(payload)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(self.path.suffix + f'.tmp-{os.getpid()}-{time.time_ns()}')
            try:
                tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
                tmp.replace(self.path)
                state.revision = next_revision
            finally:
                if tmp.exists():
                    tmp.unlink()
