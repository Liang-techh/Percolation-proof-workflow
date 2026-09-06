# Route-B full-state source manifest audit

`scripts/routeb_source_binding_manifest.py` is a fail-closed, read-only checker. It accepts an existing JSON manifest and JSON receipt, checks both copies of the exact 14-state order
`q1..q6, v1..v6, w, c`, compares domain/normalization/FD metadata, requires the literal
`float64_marker: true`, and hashes each explicitly declared source file under `--source-root`.

```powershell
python scripts/routeb_source_binding_manifest.py `
  --manifest manifest.json --receipt receipt.json --source-root C:\path\to\sources `
  --report audit-report.json
```

Each source entry must contain a relative `path` and lowercase `sha256`. Missing fields,
unsafe paths, missing files, ordering drift, metadata drift, marker drift, or hash mismatch
return exit code 1. The report is evidence of input consistency only: it deliberately contains
`"binding_conclusion": null` and never reads or modifies registry/admission state. The tool
does not create, repair, or infer a manifest or receipt.

The narrow tests are in `tests/test_routeb_source_binding_manifest.py`.
