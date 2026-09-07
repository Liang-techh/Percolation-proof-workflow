---
kind: review_result
review_id: T-P4-032-liuguanyi-typed-source-bridge-20260907T1210
source_agent: 柳冠一
task_id: T-P4-032
created_at: 2026-09-07T12:10:00-06:00
integration_status: pending
admission: pending
---

# T-P4-032 typed block/source premises for the O1 port identity

## Question inspected

Give the smallest mathematical bridge from the six-axis Route-B source variables to the abstract exact-real O1 theorem

`R_port a_B = r_B`,  `R_port = -M_BD M_DD^{-1} DeltaM_DB`,

without silently changing axis order, treating the theorem variable `v` as the deployed physical velocity, applying force normalization twice, or deleting timer/ramp/distal forcing terms that do not satisfy the zero-defect O1 premises.

This is only the typed/source mathematics assigned to 柳冠一. It does not perform the remote Lean compile owned by 臭屁猪 and does not perform the independent receipt/admission review owned by 封不觉.

## Inspected inputs

- `agent_review_inbox/task_queue.md`, blob `35c5b3fb8a06780b70dcb1142bdb0583f92993fa`, T-P4-032 dispatch.
- `artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean`, blob `c9bd41c4e18d6581bf899958b4d06d64cf165d23`; task queue records candidate SHA-256 `403C41C6F325E906A9D3555B6886D1371DFA2D84826ABCC7BF83C12E21293BFB`.
- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`, blob `27cf497b6f27919eb5b554369fb1444f4314c942`.
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_pmi_certificate.jl`, blob `207b6b361eeb465aee8933cff8b9f41a1b17a89f`.
- `examples/routeb_source_binding_audit/REPORT.md`, blob `8bc5cd5444473396caa13af107428f0350cca742`, especially B45-5.

No Lean/Lake compile or provenance/admission audit was run in this review. The result below is exact finite-dimensional algebra plus an explicit source-typing contract.

## 1. Exact axis/order contract

The deployed Julia state and mass matrix use physical axis order `(1,2,3,4,5,6)`. For the Route-B port split, freeze

`B = (4,5)`,  `D = (1,2,3,6)`.

In Lean zero-based `Fin 6`, the embeddings must therefore be

- `bIdx : Fin 2 -> Fin 6`, `bIdx(0)=3`, `bIdx(1)=4`;
- `dIdx : Fin 4 -> Fin 6`, `dIdx(0)=0`, `dIdx(1)=1`, `dIdx(2)=2`, `dIdx(3)=5`.

For a six-vector `x` and six-by-six matrix `M`, define

`projB(x)_i = x_{bIdx(i)}`, `projD(x)_j = x_{dIdx(j)}`,

and

`M_BD[i,j] = M[bIdx(i),dIdx(j)]`,
`M_DB[j,i] = M[dIdx(j),bIdx(i)]`,
`M_DD[j,k] = M[dIdx(j),dIdx(k)]`.

These shapes are exactly

`M_BD : 2x4`, `M_DD : 4x4`, `M_DB : 4x2`.

Hence

`(2x4)(4x4)(4x2) = 2x2`,

and for `a_B : R^2` the chain

`a_B -> DeltaM_DB a_B -> M_DD_inv(DeltaM_DB a_B) -> M_BD(...)`

has dimensions `2 -> 4 -> 4 -> 2`. This is the source-level reason the candidate theorem must use column vectors / `Matrix.mulVec`.

A useful source projection lemma, independent of any dynamics, is

`projD(M a) = M_DD projD(a) + M_DB projB(a)`

and similarly

`projB(M a) = M_BB projB(a) + M_BD projD(a)`.

Because `B` and `D` are a disjoint ordered partition of the six axes, this is just a finite-sum partition identity. No symmetry of `M` is needed for O1.

## 2. The theorem variable `v` is not the deployed velocity `dq_D`

This is the most important typed alias.

The candidate theorem assumes

`M_DD v + DeltaM_DB a_B = 0`.

Dimensionally, if `M_*` are mass blocks and `a_B` is an acceleration-like block variable, then `v` has the same units as acceleration. In the source adapter it should therefore be named something like

`delta_a_D : DVec 4`

and only passed to the generic O1 theorem as `v := delta_a_D`.

It must **not** be identified by name with the deployed physical velocity `dq_D` appearing in `arm_MCG(q,dq)`. The Julia `dq` enters the Christoffel/controller force; it is not the Schur-elimination correction variable of O1.

Likewise, the O1 `r_B` should be typed as the **port generalized-force component**

`r_port_B := M_BD delta_a_D`,

not as the entire P4 residual and not as the raw PMI block polynomial.

## 3. Exact source comparison lemma producing the O1 distal premise

The clean way to obtain the zero-defect premise is to compare an actual and a reference distal block equation rather than postulate an untyped `v`.

Let

`M_DD a_D + M_DB a_B = F_D`,

`M0_DD a_D0 + M0_DB a_B = F0_D`.

Define

`delta_a_D = a_D - a_D0`,
`DeltaM_DD = M_DD - M0_DD`,
`DeltaM_DB = M_DB - M0_DB`.

Subtracting the two equations and collecting terms gives the exact identity

`M_DD delta_a_D + DeltaM_DB a_B`
`  = (F_D - F0_D) - DeltaM_DD a_D0`.                 (1)

Therefore the O1 premise

`M_DD delta_a_D + DeltaM_DB a_B = 0`                 (2)

is valid precisely under the compatibility condition

`F_D - F0_D = DeltaM_DD a_D0`.                       (3)

A stronger but easy sufficient condition is `F_D=F0_D` and `M_DD=M0_DD`.

Equation (1) is the correct place to keep controller, `C_FD`, `G_FD`, timer/ramp, external-distal, or reference-model differences. They may cancel under a separately proved common-reference/common-ramp contract, but they cannot be deleted merely because the O1 coefficient formula itself contains only `DeltaM_DB`.

For the deployed `exact_ddq` source, the ideal exact-real full equation would be

`M(q) a = tau(q,dq,w) - C_FD(q,dq) - G_FD(q)`.

Projecting that equation to `D` gives the `F_D` above. However the deployed Julia uses a Float64 backslash solve, so the exact equality is an O2/source-semantic premise, not something T-P4-032 proves.

## 4. Leading minus sign and exact O1 identity

Assume the candidate hypotheses with the typed substitution `v := delta_a_D`:

`M_DD_inv M_DD = I`,
`M_DD delta_a_D + DeltaM_DB a_B = 0`,
`r_port_B - M_BD delta_a_D = 0`.

Left-multiplying the distal relation by `M_DD_inv` gives

`delta_a_D = - M_DD_inv DeltaM_DB a_B`.

Then

`r_port_B`
` = M_BD delta_a_D`
` = - M_BD M_DD_inv DeltaM_DB a_B`
` = R_port a_B`.

Thus the leading minus sign is forced by the distal balance; it is not a convention that can be moved into `DeltaM_DB` without changing the source contract.

Only a **left inverse** `M_DD_inv M_DD=I` is used. O1 itself does not need symmetry, positive definiteness, a right-inverse theorem, or a hidden numerical solver call. Those are separate source/existence obligations.

## 5. Defect identity: strongest safe fallback when the source premises do not reduce to zero

The zero-defect theorem is too brittle to use as a source adapter if any forcing/reference mismatch survives. Introduce explicit defects

`e_D : R^4`, `e_B : R^2`

through

`M_DD delta_a_D + DeltaM_DB a_B = e_D`,             (4)

`r_B - M_BD delta_a_D = e_B`.                        (5)

With only the same left-inverse hypothesis,

`r_B`
` = R_port a_B + M_BD M_DD_inv e_D + e_B`.          (6)

Proof: (4) gives

`delta_a_D = -M_DD_inv DeltaM_DB a_B + M_DD_inv e_D`;

insert this into (5).

This is the exact bridge needed if timer/ramp terms, distal forcing, `DeltaM_DD`, controller/C/G differences, a solve defect, or a source-model mismatch do not vanish. In particular, from (1) the canonical distal defect is

`e_D = (F_D-F0_D) - DeltaM_DD a_D0`.                 (7)

Equation (6) shows precisely what must be charged downstream rather than silently pretending that the pure coefficient `R_port` is the whole physical residual.

There is also an immediate obstruction: if two admissible source states have the same `a_B` but produce different nonzero `e_D` or `e_B`, then no theorem identifying the **full** residual with `R_port a_B` can hold on that domain. One must either prove those defects vanish, bound/absorb the extra term in (6), or enlarge the consumer contract.

## 6. One-time generalized-force normalization

`M_BD delta_a_D` is already in generalized-force coordinates because a mass block multiplies an acceleration-like vector. Therefore the O1 `r_port_B` is a generalized-force quantity.

The historical PMI block uses a separate raw/normalized convention; previous P4 interface work identifies the force-side map `I_B = diag(1/5,1/10)` when converting the raw PMI block to generalized force. That map belongs **upstream and at most once**:

`raw PMI quantity --I_B--> generalized-force residual`.

Do not apply `I_B` again to `M_BD delta_a_D` or to an already generalized-force `r_port_B`. Doing so would change the O1 coefficient and would duplicate the normalization. Conversely, if a future source adapter starts from a raw PMI force-like row, it must perform and type that conversion before adding it to the O1 port-force component.

`DeltaM_DB` itself is a mass-block difference; it is not a force-normalization object and must not absorb `I_B`.

## 7. Minimal Lean-facing theorem package

I recommend keeping the already dispatched `routeB_port_identity` unchanged and adding source-facing lemmas around it rather than enlarging its proof.

### A. Fixed block projections

```lean
-- bIdx = [3,4], dIdx = [0,1,2,5] in Fin 6.
theorem routeB_D_mulVec_split
    (M : Matrix (Fin 6) (Fin 6) R) (a : Fin 6 -> R) :
    projD (M *ᵥ a) =
      (blockDD M) *ᵥ projD a + (blockDB M) *ᵥ projB a
```

and the analogous B-row statement. This pins ordering once and prevents later accidental `(5,4)` or `(1,2,3,6)` permutation changes.

### B. Distal comparison / compatibility

```lean
theorem distal_difference_identity
    (hAct : MDD *ᵥ aD + MDB *ᵥ aB = FD)
    (hRef : M0DD *ᵥ aD0 + M0DB *ᵥ aB = F0D) :
    MDD *ᵥ (aD - aD0) + (MDB - M0DB) *ᵥ aB =
      (FD - F0D) - (MDD - M0DD) *ᵥ aD0
```

with a corollary obtaining the zero O1 premise from

`FD-F0D = (MDD-M0DD) *ᵥ aD0`.

### C. Defect-aware O1 theorem

```lean
theorem routeB_port_identity_with_defects
    (hInv : MDDinv * MDD = 1)
    (hD : MDD *ᵥ daD + DeltaMDB *ᵥ aB = eD)
    (hB : rB - MBD *ᵥ daD = eB) :
    rB =
      (R_port MBD MDDinv DeltaMDB) *ᵥ aB +
      (MBD * MDDinv) *ᵥ eD + eB
```

The present `routeB_port_identity` is exactly the `eD=0`, `eB=0` corollary.

### D. Source type aliases, not new mathematics

At the source adapter layer, use semantic names such as

`BlockAccel`, `DistalAccelCorrection`, `PortGeneralizedForce`

(or structures carrying these roles) so the generic Lean variable named `v` cannot be accidentally fed the deployed `dq_D` physical velocity.

## 8. What is and is not closed

Mathematically closed in this review:

1. exact B/D order and matrix shapes for the declared Route-B split;
2. the source block-projection identity needed to obtain typed D/B equations;
3. the exact compatibility condition that turns two source block equations into the zero-defect O1 premise;
4. the defect-aware port identity (6), including its sign;
5. the semantic rule that O1 `v` is a distal acceleration correction and O1 `r_B` is a generalized-force port component;
6. the one-time normalization boundary.

Still open and intentionally not claimed:

- pinned Lean compile / `#print axioms` / statement comparator for the current candidate;
- proof that the deployed Float64 `\` solve realizes the exact-real D equation;
- true-DH / reference-source equality needed to make (3) or `e_D=0` hold on the target domain;
- O0 regularizer semantics, O2 Float64 enclosure, P4/P5 absorption, coverage, flowpipe, terminal transfer, or registry admission;
- identification of the O1 port component with the **entire** P4 residual when other source terms are present.

## Requested integration action

Keep `T-P4-032` below registry and source binding `pending`. The current pure algebra theorem may be compiled independently as dispatched. For physical/source instantiation, require the fixed B/D projection contract plus either:

1. a proof of the compatibility condition (3) and `e_B=0`, allowing the zero-defect O1 theorem; or
2. the explicit defect theorem (6), with `e_D/e_B` routed to an additive/transverse/other certified consumer.

This prevents O1 from being over-read as a proof of the full deployed residual while preserving the exact coefficient identity as a reusable conditional lemma.
