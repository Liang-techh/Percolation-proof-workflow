# Route-B indexed receipt materializer

`record_routeb_indexed_receipts.py` converts an existing JSON array/object or
JSONL source into sparse JSONL receipts. Each input row must already contain
`cell_index`, `source_hash`, non-empty `geometry`, `rho`, `inverse`, and the
literal marker `outward: true`.

```powershell
python scripts/record_routeb_indexed_receipts.py --input source.jsonl --output receipts.jsonl
```

The four coordinates are integers in `[0,32]`; addresses are normalized to
`cell16/a2=.../a3=.../a4=.../a5=...` and mixed-radix rank. Missing fields,
duplicates, invalid coordinates, and non-outward rows fail before output is
installed. Empty/missing input is therefore fail-closed. The tool never fills
missing records and never enumerates `33^4`.
