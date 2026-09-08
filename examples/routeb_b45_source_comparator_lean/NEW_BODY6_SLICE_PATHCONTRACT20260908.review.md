# BODY6 aligned consumer: path contract composition

Status of the new leaf: **OPEN_UNCOMPILED / pending**. This bounded review
accepts the reported dependency progress and does not repeat compilation or
the proofs of passed dependencies. It inspects the aligned consumer's interface.

## Finding and minimal sufficient interface

ALIGNEDPATHCAPCONSUMER consistently uses one source, one full mechanical
state path, one interval [0,1], and one shift B=4079979/400000. Its eight
premises can be mapped to the four fields of the new `PathContract`:

| PathContract field | Existing ConsumerPremises producer |
| --- | --- |
| initial: F(0,path(0)) <= a | initial plus startsInInitial |
| growth: F(t,path(t)) <= F(0,path(0))+b(t) | growth, with the same source and path |
| value: G(t,path(t)) = F(t,path(t))+B | wholePath plus projection plus alignment |
| budget: a+b(t)+B <= bar | uniformGrowth plus shiftedBudget |

The scalar deduction is F(t,path(t)) <= a+b(t), then
G(t,path(t)) = F(t,path(t))+B <= a+b(t)+B <= bar.
The value equality and matching budget describe the same single shift;
they are not two charges. No source cap is replaced with an already-shifted
cap. No positivity assumption on B, a or b is needed for this implication.

`consume_path_contract_attempt` formalizes that deduction.
`aligned_premises_to_path_contract_attempt` maps every existing field into
the new interface. `consume_aligned_via_path_contract_attempt` composes the
two and has the same conclusion as the existing aligned consumer.

This is a small sufficient interface, not a claim of logically irredundant
or necessary assumptions. A consumer could accept a full path cap directly;
this interface intentionally preserves initial/growth provenance. A caller
may supply the pointwise budget directly without a separate beta, but the
adapter from the existing consumer retains and uses both beta premises.

## Path/domain and growth boundaries

The domain D, configuration set Q and projection disappear only from the
final arithmetic interface. The adapter still explicitly obtains
path(t) in D(t), then (path(t)).1 in Q, then the shifted storage identity
at exactly ((path(t)).1,(path(t)).2. This does not infer whole-path inclusion
from membership at t=0, nor transfer alignment beyond Q.

InitialSetCap is applied only at the declared starting point in X0. Growth
uses the same F and path as this cap. IntegratedGrowth remains a supplied
estimate; neither a derivative identity nor a numerical ledger proves it.
UniformGrowth converts the existing constant budget into the pointwise one.
No integration, existence, continuation, invariance or first-exit theorem
is hidden in the adapter.

No new counterexample duplicates the existing ones: INITIALPATHCAPS already
records the initial/terminal hump obstruction, PATHDOMAINPROJECTION the
initial-only domain obstruction, and ALIGNEDPATHCAPCONSUMER the unpaid
shift at the normalized origin. This leaf contributes the typed composition.

## Receipt and source scope

The newer focused receipt
`agent_review_inbox/review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T082220.md`
reports exit 0 and baseline axioms for PATHDOMAINPROJECTION and INITIALPATHCAPS
under Lean 4.32.0. This supersedes the earlier failure status for those
checked snapshots. No passed dependency was rerun or edited here.
This two-file receipt does not itself cover ALIGNEDPATHCAPCONSUMER or the
new PATHCONTRACT leaf. The new leaf imports ALIGNEDPATHCAPCONSUMER and needs
its own focused compilation against available dependency objects.

Current inspected SHA-256 values:

| Leaf | SHA-256 |
| --- | --- |
| PATHCONTRACT20260908 | bd96b283accae86e695a180bfe9223e9b396b6efdd0178dac380394eac6321f2 |
| ALIGNEDPATHCAPCONSUMER20260908 | f698d8c56c83005df0e0a907452ae7a6f083eb3736e6df60db4d0190084367dd |
| PATHDOMAINPROJECTION20260907 | f55de2b76ed401e7962b1494d02826c8fc2f951d7137f02461edeb56d5757d62 |
| INITIALPATHCAPS20260907 | 5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f |
| ACTUALSTORAGEALIGN20260907 | f8da2e44f9afc4c80fc14e81a1c59626d5af98071300a009aecd33463d3bef56 |

All names above have prefix NEW_BODY6_SLICE_ and suffix .lean in this directory.
These are current source hashes, independently of historical receipt metadata.
Only bounded static inspection, placeholder scanning and artifact hashing
were performed here; none is a compilation or axiom audit of the new leaf.
Concrete source alignment, initial/growth estimates, path/domain witnesses,
ODE/coverage and admission remain open. Registry/state and old receipts are unchanged.
