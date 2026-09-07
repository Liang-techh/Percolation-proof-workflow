# Anthropic FLT P2M reusable sidecar

This is a deliberately small, standalone Lean sidecar containing the highest-value
non-number-theoretic seam from `P2M/Util.lean`: `p2m_exact_reverting`. It reverts
the local context, elaborates a proof-card term against the reverted target, rejects
remaining expression metavariables, and assigns the checked proof. It also includes
the minimal `#p2m_type_eq` declaration-level gate for statement/proof-card identity.

The sidecar is an API/architecture reuse artifact. It is not a Route-B theorem,
does not establish PDE, ODE, coverage, interval remainder, flowpipe, or terminal
transfer obligations, and is not registered in any theorem registry. Successful
compilation only proves that this sidecar compiles in its pinned Lean environment.
The probe itself imports only `Lean`, so it does not clone or build Mathlib.

Run `./verify.sh` from any shell with Bash and Lake available. The script builds
only this directory and performs a source-level forbidden-construct and declaration
axiom audit.

## Provenance and license

- Upstream: `https://github.com/anthropics/anthropic-fermats-last-theorem`
- Commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- Source: `P2M/Util.lean`
- Upstream toolchain: `leanprover/lean4:v4.33.1`
- Upstream Mathlib pin: `db584cd6d46c92f209a44c0f1c829460d327499d` (provenance only)
- License: Apache-2.0; see `ATTRIBUTION.md` and `NOTICE` in the upstream snapshot.

The copied/adapted P2M code is attributed to Anthropic's FLT repository. The
upstream repository's `NOTICE` identifies its Apache-2.0 coverage and its
third-party FLT/Mathlib provenance. This sidecar does not copy FLT number theory.
