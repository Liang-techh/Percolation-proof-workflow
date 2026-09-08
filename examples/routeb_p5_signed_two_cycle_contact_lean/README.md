# T-P5-071 signed two-cycle contact — Lean sidecar

Agent/source_agent: 苏梦辰

This sidecar formalizes the source-independent cyclic-contact core from 狂蛮魔尊's `T-P5-071-SIGNED-TWO-CYCLE-CONTACT` review.

Formalized boundaries:

- opposite root orientation makes the scalar two-cycle composition antitone;
- `Id - Phi` has unit absolute coercivity and is injective;
- fixed-base negative-feedback inverse bounds have no `1-a*b` denominator;
- the source-cleared unsigned two-cycle elimination has exact reserve `mu1*mu2-C12*C21`;
- exact source cross-sign lemmas transport active strict monotonicity to root orientation;
- `a*b=1` identity-cycle nonuniqueness and the `99/100` near-boundary equality are regression leaves.

The sidecar deliberately does **not** claim a deployed contact graph, concrete source-factor binding, Float64/libm/FD/controller semantics, ODE/P8 coverage, parent closure, admission, provenance, or registry mutation. The interval self-map existence leaf and base-parameter `D` transport are left as explicit follow-up interfaces rather than being hidden in an oversized theorem.

Pinned execution uses the repository `examples/local_fkg/lake-manifest.json` and the sidecar `lean-toolchain`. `verify.sh` resolves `lake`/`lean` from `PATH` and is registered with `CI_PORTABLE=1`.

Status after compilation must remain `compiled_candidate`: 待封不觉独立验证 / 待梁智炜最终整合。
