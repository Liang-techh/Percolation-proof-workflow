# Exact same-source cell/lambda consumer

**OPEN_UNCOMPILED / pending.** Mathematical proof attempt, interface and counterexample only. No Float64 realization, sampling, solver, local Lean/Lake, broad regression, registry edit or physical DH admission. No numerical line-9 coefficient is instantiated.

This joins the actual `SameSourceConsumerPacket`, `DHProducerBaseBridge` and `P4RationalLambdaGuard` interfaces through source-bound rational envelopes. It does not repeat the missing-field inventory.

## Same-source meanings

Fix one source key, branch, storage, domain X_D, source state mapping and normalized force coordinates. A cell family covers X_D by a proof, and every row refers to the SAME functions and target t.

| Object | Meaning and required relation |
|---|---|
| b_base(x) | The selected source scalar base; cannot be substituted by a similarly named Dbase polynomial |
| l_base(x) | Base generalized-force residual, with the chosen compact-DH formula/source identity |
| port(x) | The actual additive force port in the SAME coordinates; total residual is l_base+port |
| M(x)=A_up(x) | Producer acceleration quadratic, `(1402217/12000000)a4²+(200739/4000000)a5²` |
| A_i∈Q | Uniform upper bound `||l_base(x)||²≤A_i` on cell i; **not** the producer metric A_up |
| P_i∈Q | Uniform upper bound `||port(x)||²≤P_i`, BEFORE any Young multiplier |
| D_i∈Q | Remaining base budget: `t+D_i≤b_base(x)` on cell i |

`RationalCharges` stores A_i,P_i,D_i and a common rational t>0. `SameSourceCharges` stores the cell cover and these three directed inequalities. No coefficient-only object can construct it.

`chargesFromProducer` provides a narrower construction for P_i: combine the existing proof `||port||²≤rhoSq*M(x)` with the same-cell inequality `rhoSq*M(x)≤P_i`. The DH bridge can supply the first premise via `rowEvidenceFromProducer`, conditional on its source matrices, descriptor relation and operator bound. The last two source bounds for A_i and D_i remain explicit.

The line-9 theta=1 inflated charge is not P_i. In a validated theta=1 interpretation, `2*rhoSq≤charge`; hence `(charge/2)*M(x)` can conservatively bound the port square, if that product is bounded on the same cell. Using charge without M(x) drops an object and its units. Using charge*M(x) as P_i and then multiplying by lambda can be conservative but charges the inflation again; it must not be presented as the exact uninflated identity.

## Division-free derivation

Let s=lambda−1>0, so theta=1/s. For the two force vectors u=l_base and v=port,

`(s+1)||u||²+s(s+1)||v||²-s||u+v||² = ||u-sv||² ≥0`.

Using the same-cell upper bounds gives

`s||l_base+port||² ≤ (s+1)A_i+s(s+1)P_i`.

With G_i=D_i−A_i−P_i, the checker polynomial has the exact identity

`q_i(s)=P_i*s²-G_i*s+A_i = (s+1)A_i+s(s+1)P_i-sD_i`.

Thus `q_i(s)≤0` and `t+D_i≤b_base` imply

`s*t+s||l_base+port||²≤s*b_base`,

and positivity of s yields `t≤b_base-||l_base+port||²`. All proof obligations are polynomial/rational; no root search, sampled state, floating-point coefficient or division is needed in this consumer.

At s=1 (lambda=2, theta=1), q_i(1)=2A_i+2P_i−D_i, recovering the earlier two-square consumer. General-s feasibility does NOT imply the stronger fixed-theta=1 Allocation record. The new code therefore returns a source scalar floor directly.

## Common rational guard

`RationalGuard` supplies rational endpoints `0<a≤b` and the two exact rational endpoint inequalities for EVERY row. `guard_at_rational` calls the existing `RouteBP4RationalLambdaGuard.common_lambda_interval`; P_i≥0 is precisely its convexity premise. Any one rational s∈[a,b] is shared by all cells/rows, with lambda=1+s.

The common interval is supplied as evidence, not found by this sidecar. Endpoint feasibility does not prove cell coverage or any source bound. Row-specific existential lambda witnesses cannot replace a shared s. A_i/P_i/D_i are conservative same-cell envelopes, not samples. The theorem permits any index type; an actual finite checker can instantiate it with Fin n.

`source_floor_to_P4` then reuses the earlier `P4Binding` conditions: at one embed, q=||l_base+port||², nominal=nu*b_base, gain*beta=nu>0, and the existing lower comparison `nominal-gain*(beta*q)≤margin`. It yields the positive P4 target **nu*t**. It neither constructs an old `PositiveTargetBudget` nor infers alpha=beta/front normalization. No source state outside the proved cover is included.

## Exact failure if D_i does not reserve target

Take u=v=(1,0), b_base=4 and prescribed t=1. Then A=P=1 and the actual total squared norm is 4, so the available margin is 0.

If one incorrectly sets D=4, the guard at s=1 is q(1)=0 and appears to pass. The correct remaining budget is D=4−t=3, for which q(1)=1>0. `forgetting_target_counterexample` captures both exact polynomial evaluations and failure of target=1. It is an algebraic interface counterexample, not a claim that the point lies on the physical descriptor manifold.

## Real DH obligations still open

The compact-DH transcription and producer formula establish a candidate algebraic interface only. The real source must still prove that its force residual is exactly l_base+port, or explicitly charge the additional distal/local/FD defect terms. The general port theorem contains those terms; a zero-defect descriptor premise cannot be obtained from a branch label.

On the SAME full source domain and cells, the missing inequalities are precisely

`||l_base_actual(x)||²≤A_i`,
`||port_actual(x)||²≤rhoSq*M(x)≤P_i`,
`t+D_i≤b_base_actual(x)`.

The source/controller/storage identities, norm/metric conversion, positive normalization and cover must accompany these inequalities. In particular, the producer's four-angle domain is not automatically the block-p or trajectory domain. Restriction to its domain does not prove the physical trajectory remains there.

The DH acceleration-ray obstruction remains relevant: the true base must dominate the source residual/port growth on every included ray point. The lambda guard certifies an allocation AFTER the rational envelopes exist; it cannot supply that storage inequality or repair a source mismatch. Current status therefore remains pending/open, with no concrete rational envelope family, common interval or physical scalar theorem admitted.

## Dependency review

The proof attempt imports `NEW_P4_032_DHProducerBaseBridge` and the actual repository module `examples.routeb_p4_rational_lambda_guard_lean.P4RationalLambdaGuard`. The names/signatures of `RowSourceEvidence`, `P4Binding` and `common_lambda_interval` were read directly. Import-path setup and elaboration have not been executed; upstream verification reports are not verification of this new module. Text checks found no proof placeholders or trailing whitespace.
