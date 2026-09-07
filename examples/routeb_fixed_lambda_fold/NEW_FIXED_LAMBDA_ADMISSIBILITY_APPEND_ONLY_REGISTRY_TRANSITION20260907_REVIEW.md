# Append-only verified registry transition review

## Scope and status

This sidecar maps the explicit evidence bundle to an immutable append-event
contract.  It is `OPEN_UNCOMPILED`; no Lean/Lake command was run and no real
registry was modified.

## Contract supplied

- `AppendOnlyVerifiedRegistryEvent` requires the verified-entry invariant,
  explicit promotion bundle, entry identity, expected artifact/statement
  digests, parent closure, independent authorization, evidence equality, and
  fresh entry identity relative to the parent list.
- `AppendOnlyTransitionRelation` only permits `after = before ++ [entry]`,
  preserving the append-only shape and disallowing overwrite/delete semantics.
- `AppendOnlyRegistryTransitionRequest` distinguishes explicit append from
  compiled-only, pending, rejected, overwrite, and delete requests.
  `appendOnlyTransitionDecision` returns `none` for every non-append case;
  dedicated theorems record each fail-closed counterexample.

## Remaining boundaries

The sidecar does not read or mutate a real registry, execute a comparator, run
Lean/Lake, validate external provenance or digest computation, or create a
VERIFIED status.  It defines only a typed append-event invariant and its
fail-closed transition cases.  No state, registry, receipt, or shared script
was modified.
