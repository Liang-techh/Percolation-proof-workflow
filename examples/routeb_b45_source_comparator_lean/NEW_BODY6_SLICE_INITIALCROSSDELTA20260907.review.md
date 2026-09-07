# Block-only initial cross-term delta

Status: **OPEN_UNCOMPILED**. This new proof attempt and review were the only
files written. No Lean/Lake, source-script execution, broad regression or
registry update occurred. The imported KEYEDSTORAGETRANSFER leaf also
remains uncompiled. No parity or scalar-match counterexample is repeated.

## Exact domain, norms and constant

The typed state is `(q,v)` with both vectors `Fin 6 -> Real`. The initial
set fixes every coordinate outside zero-based indices 3,4 to zero in both
vectors and requires

```text
normSq(q)+normSq(v) <= (3/20)^2,
normSq(u) := sum_i u_i^2.
```

Thus this is the recorded block-only q4,q5,v4,v5 ball, not a box of radius
3/20 in every coordinate and not two independent balls each of radius3/20.
The combined radius is what supplies the factor 1/2 in the bound.
`sqrt(normSq(u))` is explicitly the Euclidean norm. The default norm of a
Lean function space is not used or silently interpreted as Euclidean.

The configuration domain `Q : Set Vec` of the mass certificate is separate
from the state set X0. `configsInDomain` requires the configuration of every
initial state to lie in Q. No global or full-torus certificate is assumed.
The mass-bound predicate quantifies all test vectors u,v at each q in Q;
the initial state restriction is applied only when consuming it.

Use the recorded exact values

```text
eps = 1/1000,
L = 163847401/96000000,
r = 3/20,
delta_X0 = eps*L*r^2/2
         = 491542203/25600000000000.
```

This is a sufficient common delta under the stated norm bound. No claim
that it is the optimal constant for the actual DH mass is made.

## Mathematical derivation

`EuclideanMassBound M Q` is the bilinear form of the induced Euclidean
operator bound:

```text
forall q in Q, forall u,v,
  |u' M(q) v| <= L*sqrt(normSq(u))*sqrt(normSq(v)).
```

It is a supplied theorem for the specified evaluator, not a conclusion
obtained from reading L in a CSV. The derivation then uses

```text
2*sqrt(normSq(q))*sqrt(normSq(v)) <= normSq(q)+normSq(v) <= r^2
```

to prove `|eps*q'M(q)v|<=delta_X0`. The first inequality is proved in the
leaf from a nonnegative square and the exact square-root identities; the
second is the initial-set predicate. The rational delta equality is a
separate exact arithmetic proof attempt.

## When a matrix l1/row-sum certificate can supply the premise

The producer's Mmax was traced in V0PARAMETERMAP to a coefficient l1 row-sum
calculation in the targeted nonlinear strictification source. To use that
result here one must first prove, on the same Q and for the same M(q), the
actual entrywise bounds implied by the coefficient/phase evaluator.

The optional `RowColumnL1Bound` records both
`sum_j |M_ij(q)|<=L` for every row and
`sum_i |M_ij(q)|<=L` for every column. These bounds imply the required
Euclidean operator bound: weighted Cauchy-Schwarz gives

```text
sum_i (sum_j M_ij*v_j)^2
 <= sum_i (sum_j |M_ij|)*(sum_j |M_ij|*v_j^2)
 <= L^2 * sum_j v_j^2.
```

Ordinary Cauchy-Schwarz then gives the bilinear bound. If the exact mass
matrix is proved symmetric on Q, its column sums equal the corresponding
row sums, so a row certificate plus that symmetry suffices. A row bound
alone is an induced-infinity-norm bound and is not automatically the same
Euclidean bound. Coefficient l1 sums also require the actual trigonometric
phase/entry identity before they bound matrix row sums.

This leaf deliberately consumes the explicit Euclidean bound. It records
the alternative row/column contract but **does not implement or assert its
conversion**, the source Fourier identity, or a current mass-bound instance.
Those are precisely the extra obligations if the existing l1 CSV is the
chosen evidence route. There is no silent l1-to-Euclidean conversion.

## Minimal consumable binding

`InitialCrossBinding` has four independent fields:

1. `configsInDomain`: projection of block-only X0 is inside the certified Q.
2. `sameMass`: the source mass used by the actual cross term equals the
   bounded evaluator at every q in Q. This includes the same regularizer,
   DH parameters, index order and units; a bound for M(0) alone does not fit.
3. `massBound`: the Euclidean bilinear bound for that bounded evaluator on Q.
4. `difference`: on X0, `|dst.V-src.V|<=|eps*q'Msource(q)v|`.

The last field is the actual storage-value binding. If the two expressions
differ exactly by plus or minus this cross term, it follows algebraically.
If there are additional gain, potential, normalization, coordinate or
time-dependent differences, they must vanish on X0 or receive their own
budget; they cannot be omitted. The source and target Candidate records
retain their separate candidate and parameter digests.

`initial_one_sided_delta_attempt` concludes
`dst.V(x)<=src.V(x)+delta_X0` on X0. The direction permits transferring a
source upper bound to the target. `keyed_initial_transfer_contract_attempt`
packages it into the existing `TransferContract`, using a scope whose
initial set and comparison domain are both exactly X0. It requires the
receipt-key equality rather than inventing digest values.

The associated mass-bound receipt must identify Mbound, Q and L; the
candidate/parameter manifests must identify Msource, eps, the stored values
and the state map. Hash/key agreement is still provenance metadata and
does not prove `sameMass`, domain inclusion or the difference inequality.

## Initial-only use and remaining work

The contract gives target initial upper bound `source_upper+delta_X0`.
Keeping the old upper value requires an additional budget/comparison
argument; it is not automatic. On a different domain with combined radius
R, the same calculation gives `eps*L*R^2/2`, provided the same source norm
bound and difference identity hold there.

In particular, the existing active path is not known to stay in X0.
Initial-only delta_X0 cannot be inserted as a whole-path comparison error.
A path application needs its own domain/radius bound, mass certificate,
storage comparison and compatible receipt key. This leaf supplies neither
trajectory existence nor first-exit/continuation.

Validation consisted only of static premise/definition review and file
hashing; the constants were taken from the already traced exact producer
formula. The 102-line leaf has no proof-hole declarations. SHA-256:
`ea5d43d00b83e614799a54525ffe1879fcc4ab4b5ed82e0ee760a2924076ec3c`.
Final status: **OPEN_UNCOMPILED**, with the source/domain/operator/difference
contracts explicitly uninstantiated.
