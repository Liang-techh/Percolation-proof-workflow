"""Run a prepared upload plan through the authenticated Prove2Me transport.

The plan is immutable planning output.  ``--actions`` supplies the provider
payloads and solution files separately, so accidentally publishing an
incomplete plan fails before the first network mutation.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from percolation_workflow.uploader import Prove2MeTransport, UploadLedger


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _bindings(value: object) -> dict[str, dict[str, object]]:
    if isinstance(value, dict) and isinstance(value.get("actions"), list):
        value = value["actions"]
    if isinstance(value, list):
        rows = {}
        for row in value:
            if not isinstance(row, dict) or not isinstance(row.get("key"), str):
                raise ValueError("action bindings list must contain keyed objects")
            rows[row["key"]] = dict(row)
        return rows
    if isinstance(value, dict):
        rows = {}
        for key, row in value.items():
            if not isinstance(key, str) or not isinstance(row, dict):
                raise ValueError("action bindings map values must be objects")
            rows[key] = dict(row)
        return rows
    raise ValueError("action bindings must be a keyed object or an array")


def _materialize(plan: object, bindings: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    if not isinstance(plan, dict) or not isinstance(plan.get("ordered_actions"), list):
        raise ValueError("upload plan has no ordered_actions list")
    result = []
    for base in plan["ordered_actions"]:
        if not isinstance(base, dict) or not isinstance(base.get("key"), str):
            raise ValueError("upload plan contains an invalid action")
        key = base["key"]
        extra = bindings.get(key)
        if extra is None:
            raise ValueError(f"missing provider payload binding for {key}")
        action = dict(base)
        # Plan identity and dependency edges are authoritative; bindings may
        # add payload/file metadata but cannot silently replace them.
        for immutable in ("key", "kind", "depends_on", "name", "module"):
            if immutable in extra and extra[immutable] != action.get(immutable):
                raise ValueError(f"binding attempts to change plan field {immutable}: {key}")
        action.update({field: value for field, value in extra.items()
                       if field not in {"key", "kind", "depends_on", "name", "module"}})
        result.append(action)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--actions", required=True, type=Path,
                        help="JSON map/list of payload and solution-file bindings")
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--operation-store", required=True, type=Path)
    parser.add_argument("--token-env", default="PROVE2ME_ACCESS_TOKEN")
    parser.add_argument("--api-key-env", default="PROVE2ME_API_KEY")
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--poll-timeout", type=float, default=900.0)
    args = parser.parse_args()

    plan = _load(args.plan)
    actions = _materialize(plan, _bindings(_load(args.actions)))
    token = os.environ.get(args.token_env)
    api_key = os.environ.get(args.api_key_env)
    if not token and not api_key:
        parser.error(f"set {args.token_env} or {args.api_key_env}; credentials are never read from plan files")
    transport = Prove2MeTransport(
        access_token=token, api_key=api_key,
        operation_store=args.operation_store,
        poll_interval_seconds=args.poll_interval,
        poll_timeout_seconds=args.poll_timeout)
    result = UploadLedger(args.ledger).run(actions, transport)
    print(json.dumps({"status": result["status"],
                      "actions": len(result["ordered_keys"]),
                      "ledger": str(args.ledger.resolve()),
                      "operation_store": str(args.operation_store.resolve())},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
