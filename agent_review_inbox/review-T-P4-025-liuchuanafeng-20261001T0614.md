---
kind: review_result
review_id: T-P4-025-LIUCHUANAFENG-20261001T0614
task_id: T-P4-025
source_agent: 流川枫
created_at: 2026-10-01T06:14:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 87c21dcc1f3ca368ffb8e635796fc92e581a80f8
---

# T-P4-025 audit: real norm-square expansion is an algebraic leaf, not a residual gate

## Exact question

For finite-dimensional real vectors, is
`||l+r||_₂² = ||l||_₂² + 2*⟨l,r⟩ + ||r||_₂²`
available as an exact statement identity, and does that identity discharge any Route-B residual decomposition or PMI gate?

## Inspected commit / paths

- Claim commit: `87c21dcc1f3ca368ffb8e635796fc92e581a80f8`.
- Queue commit before this claim: `4d622b04b99addad6e6834905d6177674a85519e`.
- `agent_review_inbox/task_queue.md` — `T-P4-025` still `status: open`; parent interface is `T-P4-024`; sibling Young leaf is `T-P4-026`.
- Inbox tree at the queue commit: no prior `claim-T-P4-025-*` or `review-T-P4-025-*`.
- Sibling already harvested as pending, not repeated: `review-T-P4-026-liuchuanafeng-20261001T0514.md`.
- No Lean file, `#print axioms`, or repo checker was run. This is not a compile receipt.

## Exact statement retained

Let `l,r ∈ ℝ^n` with the standard real inner product. Expand the squared Euclidean norm by bilinearity and symmetry:

```text
||l+r||_₂² = ⟨l+r, l+r⟩
            = ⟨l,l⟩ + ⟨l,r⟩ + ⟨r,l⟩ + ⟨r,r⟩
            = ||l||_₂² + 2*⟨l,r⟩ + ||r||_₂².
```

The identity is unconditional on `l` and `r`. It does not require `theta>0`, a safety factor, or a sign on the cross term. The polarization form is the same fact:

```text
2*⟨l,r⟩ = ||l+r||_₂² - ||l||_₂² - ||r||_₂².
```

Coordinate form, if a later Lean adapter needs an explicit basis: for `l=(l_i)`, `r=(r_i)`,

```text
sum_i (l_i+r_i)^2 = sum_i l_i^2 + 2*sum_i l_i*r_i + sum_i r_i^2.
```

## Diagnostic only

Local exact `Fraction` check, not a repository checker:

```text
python3 -c '... three rational vector pairs, including a zero vector and a four-dimensional pair ...'
exit 0
all three expansions equal as Fractions
```

This does not authenticate Mathlib, Lean, or a source packet.

## Interface boundary toward T-P4-024 / T-P4-026

The parent adapter may compose this identity with the already-recorded Young leaf only after both premises stay explicit:

```text
||l+r||_₂² = ||l||_₂² + 2*⟨l,r⟩ + ||r||_₂²
            ≤ (1+theta)*||l||_₂² + (1+theta⁻¹)*||r||_₂²,
```

where the inequality step is `T-P4-026` and requires `theta>0`. Substituting `||r||_₂² ≤ rho*A` is a separate premise. Notation stays fixed: `rho` is `rho_F²`, and `A` is `A_up=a_Bᵀ B_up a_B`. This review does not bind either object, and it does not import the Young coefficient into the expansion.

## Explicit non-admissions

- Not proved in Lean. No theorem name, axiom list, or pinned toolchain receipt.
- Not proved: residual decomposition, all-cell coverage, flowpipe, terminal transfer, or PMI closure.
- Not proved: any positive ledger margin, Float64 source, or solver status.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: source-independent real norm-square identity. The Route-B consumption interface remains open until a pinned Lean receipt exists and the `theta>0` Young step plus the `rho*A` premise are supplied separately.

## Proposed integration (coordinator only)

1. Harvest as a pending algebra sidecar on `T-P4-025`. Do not close `T-P4-024` or P4.
2. Do not write `state.json`, the verified registry, or Lean sources from this file.
3. Leave the pinned real inner-product/norm API slot with 巨阳仙尊. A later receipt must keep the statement identity and must not treat it as residual or PMI closure.

## Unresolved blockers

1. No Lean elaboration or `#print axioms`.
2. Composition with `T-P4-026` is an interface note only; the parent adapter is not discharged.
3. No source binding of `l`, `r`, `rho`, or `A_up`.

## Response / handoff

流川枫 claimed open `T-P4-025` and recorded a pending exact norm-square expansion. It does not close the parent adapter, coverage, or registry.
