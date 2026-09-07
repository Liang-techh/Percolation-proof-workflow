# Keyed storage identity and one-sided barrier transfer

Status: **OPEN_UNCOMPILED**. The new 97-line leaf imports only Mathlib.
No Lean/Lake, source-script execution, broad regression or registry change
was performed. This is a consumable contract and proof attempt, not an
instance for the current Route-B candidate.

## Boundary with the existing leaves

- **STORAGE_IDENTITY_TRANSFER / STORAGEIDENTITY:** the prior interface
  isolates mathematical storage equality and initial/barrier transfer.
  This leaf adds an explicit receipt key and a charged one-sided comparison;
  it does not discharge the prior identity or turn scalar metadata into it.
- **COMPILED_LEDGER_BINDING / COMPILEDLEDGERBINDING:** that sidecar invokes
  the existing ActualStorage and ActualShift theorem interfaces and records
  their historical compiled receipts. This leaf imports neither sidecar nor
  compiled storage module; its functions are abstract. It neither inherits
  a compiled status nor instantiates those theorems' gap, mass, parameter,
  normalization, initial-set or source-to-path hypotheses.
- **V0PARAMETERMAP:** that leaf establishes the exact V0 generating formula
  at the arithmetic/source-text level and states the velocity-parity
  obstruction to a same-coordinate identity. This leaf consumes none of
  those facts as a proved current candidate binding. Its illustrative
  delta_X0 still requires the actual same-source norm and difference bounds.

The keys organize these separate obligations; they do not replace or
strengthen any of them. No existing file or interface was modified.

## Objects that must be bound

| Contract field | Required concrete binding |
| --- | --- |
| `src.V`, `src.candidateDigest` | The exact exported storage evaluator and its definition/source receipt: for the targeted branch this includes its value-level normalization, not just the derivative of K+Uctrl+Ugrav+eps*q'Mv |
| `dst.V`, `dst.candidateDigest` | The precise ledger/ActualStorage/ActualShift expression being claimed, with all shifts, corrections and time dependence retained |
| Both `parameterDigest` fields | Separate canonical parameter manifests for the two functions. Include source DH/mass/potential identities, mass regularizer, gains, eps/cross convention, Uzero/additive constant, and the chosen f,p,h,H or F,P,C when used. Include state order, units and any changed velocity/coordinate map in the candidate/parameter manifest |
| `scope.initial`, `initialDigest` | Exact X0 predicate and state embedding: the recorded block-only q4,q5,v4,v5 ball has radius3/20 and remote coordinates zero; c²<=3 must also be bound if the chosen storage contains the disturbance slope |
| `scope.domain`, `domainDigest` | Exact comparison domain, normalization and lift/time map. An initial-only bound is not a bound on the whole active energy domain or along a path |
| `receipt` | The six ordered candidate/parameter/initial/domain digest labels expected by the consuming receipt |
| `comparison` | A proved function equality or pointwise one-sided inequality on the stated domain, independently of matching labels |
| Path and budget arguments | The same path inside that domain, a source tube bound, and room for the comparison error in the target threshold |

`ReceiptKey` stores the six ordered labels; `TransferContract.keyMatches`
requires them to agree with the actual typed candidate/scope arguments.
This exposes stale or differently scoped receipt substitution at the
interface. Strings are **metadata**, however: Lean equality of digest strings
does not prove a hash was computed correctly or that the typed evaluator
denotes those bytes. The source-to-definition and canonical-manifest
validation remain external obligations. No concrete digest labels or
current candidate instances are invented in this leaf.

For time-dependent synthesis storage, use an extended state such as
`X = Real × PhysicalState`, and bind the time/state embedding. This keeps
the comparison pointwise without identifying a time-dependent synthesis
storage with a time-independent physical energy by name.

## Mathematical contracts and consumers

`SameStorageIdentity src dst scope` is
`forall x in domain, dst.V(x)=src.V(x)`. Its consumer supplies the zero-error
case of `OneSidedComparison`, which is

```text
forall x in domain, dst.V(x) <= src.V(x) + delta.
```

This direction is intentional: an upper bound on src transfers to dst.
Source and target parameters need not be identical if this inequality is
actually proved. Their manifests must still be separately identified.

`initial_bound_transfer_attempt` requires X0 contained in the comparison
domain and an actual source upper bound on X0. Its conclusion is a target
bound `upper+delta`; it does not silently retain `upper` for positive delta.
`barrier_transfer_attempt` similarly requires path-domain membership,
`src.V(path(t))<=cap` on [0,1], and `cap+delta<=bar`. It transfers that
already-proved sublevel conclusion. It does not derive a first-exit,
integration or source-to-flow theorem from scalar arithmetic.

## Targeted cross term versus the two compiled storage families

The previous `V0PARAMETERMAP` leaf records the concrete targeted derivative
expression with eps=1/1000 and cross term `q'M(q)v`. It also records the
exact producer formula

```text
V0 = ((1+eps)*Mmax/2)*(3/20)^2
   = 492033745203/25600000000000.
```

With fixed source fields and the same state coordinates, ActualStorage and
the ActualShift kinetic+W+B expression are even in v. The targeted cross
term is odd in v. The earlier structural lemma therefore requires the cross
term to vanish at velocity-paired points if an exact identity to an even
storage is claimed. This new leaf does not assume that vanishing condition.

A one-sided comparison offers another route: if the difference is only
eps*q'Mv, a verified absolute bound on that term gives delta. On the
recorded initial ball, the same-source norm estimate would give

```text
delta_X0 = eps*Mmax*(3/20)^2/2
         = 491542203/25600000000000.
```

This remains conditional on the actual mass norm bound, value-level storage
identity and initial-set map. It cannot be reused as a whole-path delta
without a bound on the path's comparison domain. Any potential/gain/shift
difference must be included as well. In particular, ActualShift's exact
constant `4079979/400000` cannot disappear from this comparison. The targeted
gain correction vanishes on the block-only initial configurations but
does not automatically vanish on the active domain.

## Exact scalar-match counterexample

Let b be the actual recorded V0 and define, on path x(t)=t,

```text
V(x)=b,  W(x)=b+2x,  X0={0},  0<=t<=1.
```

Both functions have initial value exactly b, so they share the same valid
initial upper bound b. The source barrier V<=1 holds because b<1, while
W(1)=b+2>1. `exact_v0_match_no_barrier_transfer_attempt` encodes these
facts with exact rational arithmetic. This is an abstract mathematical
counterexample to transfer from a scalar match, not a proposed DH trajectory
or a statement about actual controller failure. It supplies no valid
comparison budget small enough for the claimed target barrier.

## Completion boundary

To consume this interface, supply the two candidate definitions/manifests,
initial and domain predicates, their receipt keys, and either the scoped
identity or a one-sided comparison with a charged delta. Then supply the
source initial/tube proofs and compatible path. Those fields are currently
uninstantiated; equality of the V0 number alone fills none of them.

Only static inspection and file hashing were performed. The new leaf has
no `sorry`, `admit` or `axiom` declarations and is not kernel-verified.
It remains OPEN_UNCOMPILED because Lean/Lake execution was excluded from
this work, no elaboration or new compiler receipt was produced, and the
concrete candidate/domain/path contracts are uninstantiated. Existing
compiled receipts for other files do not cover this source file.
SHA-256: `58629ebaa0939d1584c16f62bcecef3e0ba4e7d6b8cfd9d8f7cfc7939c8decf3`.
Final status: **OPEN_UNCOMPILED**.
