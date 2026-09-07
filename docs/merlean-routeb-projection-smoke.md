# MerLean-style Route-B projection smoke

Date: 2026-09-06

This is a read-only focused smoke against the real Route-B checkpoint
`artifacts/routeb_6dof/state.json`.  It loads the checkpoint through
`StateStore`, calls `merlean_plan_projection.export_views`, and writes the
three derived views only to a temporary directory.  The authoritative
checkpoint, registry, and frontier are not written.

Command (from the workflow repository):

```powershell
$env:PYTHONPATH='src'
python - <<'PY'
# equivalent local smoke: StateStore.load -> project -> export_views
PY
```

## Observed checkpoint

- revision: `328`
- root: `b85f1ee1ef03426eaa1197ff39c6c026`
- formal node count: `64`
- frontier count: `54`
- notes emitted by the projection: `65`
- graph cycles: none (export completed successfully)

## Status boundary

All 64 formal records were projected as:

```text
status=pending, admission_status=pending: 64
```

No `completed_axiom` record was produced.  No node entered the verified
registry; the projection is a derived interoperability view and does not
alter eligibility or evidence admission.

## Mutation check

The checkpoint bytes were hashed before and after projection:

```text
before SHA-256: 97fbba67d0facfb349bd41d9fc34c7229a440a263f19c4c211b97ef7ad7a4b7d
after  SHA-256: 97fbba67d0facfb349bd41d9fc34c7229a440a263f19c4c211b97ef7ad7a4b7d
mutation: false
```

## Derived view hashes

The temporary export produced all three expected files:

| view | bytes | SHA-256 |
|---|---:|---|
| `statements.json` | 1,105,164 | `07122c9e6d675205492de35d70c5091878d41734b0fbecee133cee11b7c17198` |
| `progress.json` | 13,345 | `88ba78f9149e596b1fe92149253db3abfd3f2f66052ae2132ef88c74a7bdaf81` |
| `analytics.json` | 8,152 | `dc7e101f254664fe943ea7bd952b48257e6d90cb330ada4792dea79bdb82e7be` |

The export directory was temporary and was removed automatically after the
smoke.  This run verifies projection compatibility with the actual Route-B
state, not mathematical closure of P3/P4/P8 or M4.
