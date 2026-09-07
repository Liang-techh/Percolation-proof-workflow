# Minimal same-source scalar consumer packet

**OPEN_UNCOMPILED.** This round creates only the companion proof attempt and this review. No local Lean/Lake, solver or regression run; no registry change. This is a typed mathematical contract, not another line-9 inventory or a completed physical certificate.

The packet separates three obligations: source identity, source allocation, and P4 normalization. All mathematical evidence refers to **one** source object, row and target through dependent parameters.

## Minimal source packet

`SourceKey` declares the controller branch and controller/storage/mass digests plus object/domain/unit contracts. `SourceFields key X` supplies one domain D and same-state functions:

| Field | Exact role |
|---|---|
| `base(x)` | The scalar b_base used in the consumer, including the selected storage/controller terms |
| `lBase(x)` | Two-component base generalized-force residual in a fixed coordinate system |
| `port(x)` | Two-component external force residual in the SAME coordinates |
| `acceleration(x)` | The two source acceleration components defining A_up |

`sqNorm(v)=v₀²+v₁²` encodes the Euclidean squared norm directly, avoiding a square root. `metric(src,x)` defines

`A_up=(1402217/12000000)*a₄²+(200739/4000000)*a₅²`.

The matrix is positive diagonal, so A_up≥0 follows algebraically. Identifying these variables with the intended physical acceleration and its domain is still a source proof, not a consequence of the coefficient values.

`RowInterpretation key` carries CSV/producer/partition identities, line, eta, theta=1, the printed charge token, and validated real quantities rhoSq and charge. It requires `rhoSq≥0` and `2*rhoSq≤charge`. `RowSourceEvidence row src` requires

`||port(x)||² ≤ rhoSq*A_up(x)` on D.

Thus `||lBase+port||² ≤ 2||lBase||²+charge*A_up`. The proof retains the cross term through the elementary vector Young inequality; it does not substitute the base residual for the total residual.

The printed token is provenance, **not** an axiom that a rounded decimal equals a validated enclosure. A conservative charge enlargement is allowed only when justified externally. The asserted source port bound is the mathematical evidence actually consumed. No CSV parser, outward-rounding proof, source authentication or completed line-9 interpretation is provided here.

## What suffices to prove allocation

The smallest direct contract is `Allocation row src target`:

`target>0` and `target+2||lBase(x)||²+charge*A_up(x)≤base(x)` for all x∈D.

This direct route can preserve correlations. It does not assert that coefficient slack establishes allocation.

A constructive sufficient route uses only three uniform bounds:

`B≤base(x)`, `||lBase(x)||²≤R`, `A_up(x)≤A`,

and the exact scalar test

`target>0`, `target+2R+charge*A≤B`.

`allocationFromUniform` derives the pointwise inequality using charge≥0. B need not be separately assumed positive, nor must the domain have a positive A_up lower bound: the allocation itself supplies the baseline. Separate cap nonnegativity is unnecessary for this proof. Independent caps can be too conservative; failing this sufficient test does not refute the correlated direct route.

The dependent pair of `RowSourceEvidence row src` and `Allocation row src target`
stores the source port evidence and allocation together. `allocated_source_floor` then yields

`target ≤ base(x)-||lBase(x)+port(x)||²` on D.

No source energy bound is mandatory in this final consumer. If an energy theorem is used to obtain R or A, that upstream proof must establish exactly these two bounds on this D.

## Required P4 adapter contract

For a fixed positive normalization nu and ONE embedding into the existing P4 domain, `P4Binding` requires:

| Equality/condition | Purpose |
|---|---|
| source D implies `f.domain(embed x)` | Same-state domain coverage for the existing comparison |
| `f.residual(embed x)=||lBase(x)+port(x)||²` | Exact total force residual; neither A_up nor an acceleration residual |
| `m.nominal(embed x)=nu*base(x)` | Same base/nominal normalization and direction |
| `m.gain(embed x)*beta(embed x)=nu` | One residual scaling, without an extra front factor |
| Existing `ScaledComparison` | Supplies `nominal-gain*(beta*q)≤m.margin` and its sign obligations |

With these conditions, `allocated_P4_target` yields

`0<nu*target` and `nu*target≤m.margin(embed x)` for every source x∈D.

Hence a separately prescribed P4 target T must be identified with `nu*target` (or justified by `0<T≤nu*target`). It is not generally the unscaled target. The conclusion holds on the embedded source domain; it does not automatically cover all of f.domain.

These equalities are the explicit requirements of this adapter, not a claim that every sound adapter must use identical equalities. Conservative one-sided comparisons can support other adapters but must be proved in the correct direction. Coordinate changes require their own norm/metric conversion; nu alone is not an arbitrary matrix coordinate transformation.

If the caller also wants to use the P4 front decomposition, the OPTIONAL `FrontFactorization` requires

`offset+alpha*(mu*frontEnergy(front))=nu*base`.

Together with nominal equality this identifies the body expression with the same nominal. No alpha=beta, sf=theta, or gamma=gain assumption is made. Front factorization alone does not supply RemainderMargin, composition/Schur normalization, front floors or PSD; those remain obligations of that separate route. The scalar consumer does not require them.

## Directed mathematical review

- `totalSq` squares the coordinatewise sum of both force vectors. It is not the sum of their separate squared norms. The Young estimate follows from the exact identity `2||u||²+2||v||²-||u+v||²=(u₀-v₀)²+(u₁-v₁)²≥0`.
- `metric` is a quadratic form on the acceleration vector, not a norm of the force residual. Its two rational coefficients are positive; multiplying `2*rhoSq≤charge` by this nonnegative metric preserves the inequality direction.
- `RowSourceEvidence.port_bound` is an UPPER bound on the squared port norm. This direction yields `totalSq≤2||lBase||²+charge*A_up`; subtracting it from base yields a LOWER bound on `base-totalSq`. Reversing the port inequality would not support the consumer.
- Uniform allocation uses a LOWER base bound and UPPER residual/metric bounds. The final P4 comparison is also in the lower-bound direction: the normalized source expression is ≤ the P4 margin. A margin upper bound cannot replace it.
- `P4Binding` uses one source object, one embed and the exact total residual at that state. Reassociating `gain*(beta*q)` gives `(gain*beta)*q=nu*q`; nominal equality then produces exactly `nu*(base-totalSq)`. No extra alpha factor is inserted.

These are source-level proof reviews, not Lean elaboration results. To use `ConsumerPacket`, pass its `row_source` and `allocation` projections to the two consumer theorems.

## Boundary with the earlier source-binding and obstruction sidecars

`NEW_P4_032_Line9SourceObstruction.review.md` explains why no concrete packet is obtained from the existing row: controller/storage selection and the consumer functions are not recorded. `RowInterpretation` now specifies the completed interface that would be needed; it does not retrospectively supply those missing values. The previous different-base counterexample remains valid because it violates the newly required allocation premise in its failing branch.

`NEW_P4_032_SourcePositiveTargetBinding.lean` uses the richer `SourceView`/`SameDomainBinding` route. Its force residual is wrapped as `PortGeneralizedForce`, and its `norm2` is explicitly Euclidean `WithLp.toLp 2`, not the default function-space sup norm. Connecting the new source to that interface requires the explicit vector identity

`oldSrc.forceResidual(x).value = fun i => newSrc.lBase(x,i)+newSrc.port(x,i)`,

and the Euclidean finite-two-coordinate identity `norm2(v)^2=sqNorm(v)`. This companion sidecar does not yet implement that library-level norm bridge or construct an old `SameDomainBinding`.

The old source nominal must match `nu*newSrc.base`; its gain/beta, scalar margin, domain and state mapping must match the new P4 adapter. The old route additionally asks for energy, remainder, front, mu, alpha, offset and their same-state equalities, as well as its composition/floor/cap/budget evidence. The new packet does not manufacture these proofs, nor does it construct old `PositiveTargetBudget` records. Conversely, the old field equalities alone do not provide the new base allocation or port bound. The two routes share P4 scalar types but have different explicit premises and require an adapter before results can be identified.

## Verification boundary

The new proofs are uncompiled attempts using the existing P4 types. The source and row keys are declared metadata; arbitrary strings do not authenticate their contents, and a caller must not label unrelated functions with a key without the source audit. No concrete source functions, row interpretation, uniform bounds, Allocation, ConsumerPacket or P4Binding have been admitted from the current external artifacts.

This contract makes the next mathematical work precise: prove the same-source port bound, obtain the direct allocation or three bounds plus its scalar test, and supply the normalization/object equalities. It does not turn the existing positive coefficient slack into any of those premises.
