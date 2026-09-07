# Route-B P8 explicit-time 13-state sidecar

This leaf freezes the smallest explicit-time interface for the deployed
13-state source.

It deliberately keeps `c` outside the state vector and records only the
assumptions needed for a later source-authenticated child theorem:

1. the 13-state coordinate order `q₁…q₆, dq₁…dq₆, w`;
2. an external parameter `c`;
3. an initial projection lemma from the 14-state parent to the 13-state family;
4. a terminal-transfer predicate that is rewritten through `w = c`.

The file does not alter `RouteBP8PicardStep`, does not claim a flowpipe, and
does not bind the deployed RHS.  It is just a minimal theorem/interface
sidecar that makes the contract boundary explicit.

Verification is intentionally local and pinned to the imported parent leaf:

```text
./verify.sh
```

Only this directory is compiled.  No broad regression is run.
