# T-P5-118 center-bias mixed small-gain Lean sidecar

Owner/source_agent: **巨阳仙尊**.

This sidecar formalizes the source-independent algebraic core of `review-T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN-guyuefangyuan-20260909T0224Z.md`:

- weighted PSD quadratic bias identity and root-free two-block inequality;
- centered comparator + bias cap -> cross-multiplied displacement packet;
- sublevel squaring with `V^2 <= R V`;
- relative/additive coefficient gates -> mixed power absorption;
- Lyapunov-ledger specialization and strict retained reserves;
- division-free ultimate-radius inward boundary gate;
- the exact nonzero-bias zero-floor counterexample.

The trusted theorem layer does **not** bind the deployed `storageKey`, `anchorKey`, center offset, physical metric/source coefficients, same-domain coverage, Float64/FD/controller semantics, P8 flowpipe, admission, or registry. These remain external hypotheses/open obligations.

Portable verification is `CI_PORTABLE=1 bash verify.sh`. It obtains `lake`/`lean` from `PATH`, checks the local `lean-toolchain` against `../local_fkg/lean-toolchain`, consumes the pinned `../local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, scans placeholders, and audits every public theorem's `#print axioms` output.
