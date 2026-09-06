"""Run the real Prove2Me HTTP transport against a local protocol fixture.

The transport is still configured with its production HTTPS origin; the
injected opener forwards requests to a loopback HTTP server so no credentialed
or remote mutation occurs.  This exercises actual HTTP parsing, auth and
idempotency headers, queued polling, multipart solutions, theorem-id context,
and a ledger/operation-store restart.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import uuid
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.uploader import Prove2MeTransport, UploadLedger


DISCLAIMER = "Loopback HTTP protocol fixture only; no live Prove2Me mutation or proof claim."


class FixtureState:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.jobs: dict[str, dict] = {}
        self.submissions: dict[str, dict] = {}
        self.idempotent: dict[str, dict] = {}
        self.requests: list[dict] = []
        self.polls: Counter[str] = Counter()
        self.verify_bodies: list[bytes] = []
        self.next_job = 0
        self.next_submission = 0

    def new_job(self, kind: str, name: str | None) -> dict:
        with self.lock:
            self.next_job += 1
            job_id = f"job-{self.next_job}"
            response = {"job_id": job_id, "status": "QUEUED"}
            self.jobs[job_id] = {"kind": kind, "name": name,
                                 "response": response,
                                 "theorem_id": f"T-{name}" if kind == "theorem" else None}
            return response


def _handler(state: FixtureState):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def log_message(self, *_args) -> None:
            return

        def _respond(self, status: int, value: dict) -> None:
            data = json.dumps(value).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _record_common(self, body: bytes) -> tuple[str, dict]:
            authorization = self.headers.get("Authorization", "")
            idempotency = self.headers.get("Idempotency-Key", "")
            state.requests.append({"method": self.command, "path": self.path,
                                   "authorization": authorization,
                                   "idempotency_key": idempotency,
                                   "content_type": self.headers.get("Content-Type", ""),
                                   "body_bytes": len(body)})
            if authorization != "Bearer fixture-token":
                raise ValueError("missing or incorrect bearer token")
            if not idempotency:
                raise ValueError("mutation has no idempotency key")
            payload = (json.loads(body.decode("utf-8")) if body
                       and self.headers.get("Content-Type", "").startswith("application/json") else {})
            return idempotency, payload

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            try:
                key, payload = self._record_common(body)
                path = urlsplit(self.path).path
                if path in {"/api/v1/submit-definition", "/api/v1/submit-problem"}:
                    prior = state.idempotent.get(key)
                    if prior is not None:
                        self._respond(202, prior)
                        return
                    kind = "definition" if path.endswith("definition") else "theorem"
                    name = payload.get("theorem_name") or payload.get("definition_name")
                    response = state.new_job(kind, name)
                    state.idempotent[key] = response
                    self._respond(202, response)
                    return
                if path == "/api/v1/verify":
                    with state.lock:
                        state.next_submission += 1
                        submission_id = f"submission-{state.next_submission}"
                        state.submissions[submission_id] = {"polls": 0}
                        state.verify_bodies.append(body)
                    self._respond(202, {"submission_id": submission_id, "status": "QUEUED"})
                    return
                self._respond(404, {"error": "unknown path"})
            except (ValueError, json.JSONDecodeError) as exc:
                self._respond(400, {"error": str(exc)})

        def do_GET(self) -> None:
            parsed = urlsplit(self.path)
            if parsed.path.startswith("/api/v1/publish-jobs/"):
                job_id = parsed.path.rsplit("/", 1)[-1]
                job = state.jobs.get(job_id)
                if job is None:
                    self._respond(404, {"error": "unknown job"})
                    return
                state.polls[job_id] += 1
                if state.polls[job_id] == 1:
                    self._respond(200, {"job_id": job_id, "status": "QUEUED"})
                else:
                    response = {"job_id": job_id, "status": "PUBLISHED"}
                    if job["theorem_id"]:
                        response["theorem_id"] = job["theorem_id"]
                    self._respond(200, response)
                return
            if parsed.path == "/api/v1/verify":
                submission_id = parse_qs(parsed.query).get("submission_id", [""])[0]
                submission = state.submissions.get(submission_id)
                if submission is None:
                    self._respond(404, {"error": "unknown submission"})
                    return
                submission["polls"] += 1
                status = "PENDING" if submission["polls"] == 1 else "ACCEPTED"
                self._respond(200, {"submission_id": submission_id, "status": status,
                                    "theorem_id": "unused"})
                return
            self._respond(404, {"error": "unknown path"})

    return Handler


def _forwarding_opener(port: int):
    production_prefix = "https://prove2.me/api/v1"
    local_prefix = f"http://127.0.0.1:{port}/api/v1"

    def opener(request: Request, *, timeout: float):
        forwarded_url = request.full_url.replace(production_prefix, local_prefix, 1)
        forwarded = Request(forwarded_url, data=request.data,
                            headers=dict(request.header_items()),
                            method=request.get_method())
        return urlopen(forwarded, timeout=timeout)

    return opener


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(output: Path | None = None) -> dict:
    run_dir = ROOT / "artifacts" / "prove2me_transport" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    )
    with tempfile.TemporaryDirectory(prefix="prove2me-transport-") as directory:
        root = Path(directory)
        state = FixtureState()
        server = ThreadingHTTPServer(("127.0.0.1", 0), _handler(state))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            solution_leaf = root / "leaf.lean"
            solution_parent = root / "parent.lean"
            solution_leaf.write_text("theorem solution : True := by trivial\n", encoding="utf-8")
            solution_parent.write_text("theorem solution : True := by trivial\n", encoding="utf-8")
            operation_store = root / "operations.json"
            actions = [
                {"key": "definition:P.Defs", "kind": "submit_definition", "module": "P.Defs",
                 "payload": {"definition_name": "P.Defs", "formal_statement": "def x : Nat := 0"}},
                {"key": "theorem:P.leaf", "kind": "submit_theorem", "name": "P.leaf",
                 "depends_on": ["definition:P.Defs"],
                 "payload": {"theorem_name": "P.leaf", "formal_statement": "theorem leaf : True"}},
                {"key": "theorem:P.parent", "kind": "submit_theorem", "name": "P.parent",
                 "depends_on": ["theorem:P.leaf"],
                 "payload": {"theorem_name": "P.parent", "formal_statement": "theorem parent : True"}},
                {"key": "solution:P.leaf", "kind": "verify_solution", "name": "P.leaf",
                 "depends_on": ["theorem:P.leaf"], "solution_path": str(solution_leaf)},
                {"key": "solution:P.parent", "kind": "verify_solution", "name": "P.parent",
                 "depends_on": ["theorem:P.parent"], "solution_path": str(solution_parent)},
            ]
            transport = Prove2MeTransport(
                access_token="fixture-token", operation_store=operation_store,
                opener=_forwarding_opener(server.server_port), poll_interval_seconds=0,
                sleep=lambda _seconds: None,
            )
            first = UploadLedger(root / "ledger.json").run(actions, transport)
            second = UploadLedger(root / "ledger.json").run(
                actions,
                Prove2MeTransport(
                    access_token="fixture-token", operation_store=operation_store,
                    opener=_forwarding_opener(server.server_port), poll_interval_seconds=0,
                    sleep=lambda _seconds: None,
                ),
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        mutation_requests = [item for item in state.requests if item["method"] == "POST"]
        mutation_keys = [item["idempotency_key"] for item in mutation_requests]
        required_keys = [action["key"] for action in actions]
        report = {
            "status": "passed",
            "disclaimer": DISCLAIMER,
            "run_directory": str(run_dir),
            "first_ledger_status": first["status"],
            "second_ledger_status": second["status"],
            "action_order": required_keys,
            "mutation_request_count": len(mutation_requests),
            "mutation_idempotency_keys": mutation_keys,
            "all_mutations_authenticated": all(
                item["authorization"] == "Bearer fixture-token" for item in mutation_requests
            ),
            "all_mutations_idempotent": mutation_keys == required_keys,
            "publish_poll_count": sum(state.polls.values()),
            "verify_poll_count": sum(item["polls"] for item in state.submissions.values()),
            "theorem_ids": sorted(job["theorem_id"] for job in state.jobs.values() if job["theorem_id"]),
            "multipart_solution_seen": all(
                b'filename="leaf.lean"' in body or b'filename="parent.lean"' in body
                for body in state.verify_bodies
            ) and len(state.verify_bodies) == 2,
            "operation_store_operations": len(
                json.loads(operation_store.read_text(encoding="utf-8"))["operations"]
            ),
        }
        if not (
            report["first_ledger_status"] == "complete"
            and report["second_ledger_status"] == "complete"
            and report["mutation_request_count"] == 5
            and report["mutation_idempotency_keys"] == required_keys
            and report["all_mutations_authenticated"]
            and report["all_mutations_idempotent"]
            and report["publish_poll_count"] == 6
            and report["verify_poll_count"] == 4
            and report["theorem_ids"] == ["T-P.leaf", "T-P.parent"]
            and report["multipart_solution_seen"]
            and report["operation_store_operations"] == 5
        ):
            report["status"] = "failed"
            _write_json(run_dir / "report.json", report)
            raise RuntimeError(f"Prove2Me transport invariant failed: {report}")
        _write_json(run_dir / "report.json", report)
        if output is not None:
            _write_json(output, report)
        return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = run(args.output)
    except Exception as exc:
        print(f"failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
