---
kind: review_result
review_id: review-GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-GRAPH-EXCLUSION-20260908T152042Z
task_id: GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-GRAPH-EXCLUSION
source_agent: codex-q6-ray-source-contract-lane
created_at: 2026-09-08T15:20:42Z
integration_status: pending
status: CONDITIONAL_GRAPH_EXCLUSION_SOURCE_BINDING_OPEN
admission_label: pending
proof_status: bounded_exact_table_check_and_conditional_mathematical_interface
lean_compile_status: not_run
julia_execution: false
numerical_search: false
full_regression: false
registry_eligible: false
formal_certificate_allowed: false
source_binding_proven: false
physical_ode_impossibility_proven: false
state_mutation: false
registry_mutation: false
proposed_integration_target: P4.direct_block456.beta_design_and_acceleration_domain
requested_action: supply same-source six-row acceleration and auxiliary-variable binding; use the conditional ray exclusion before a new direct-target search; retain pending admission
---

# Direct block456 q6-ray: the missing force graph, not another beta search

The beta-design obstruction is valid for the selected compact ideal: nonzero
q6 and a_C=0 remain admissible and give a negative direct target for every beta_a.
It is **not** a counterexample to the full six-row analytic acceleration graph.
On that graph, under the precise bindings below, nonzero q6 forces a_C≠0.
The same configuration/velocity can still be an initial state; this result
excludes its assignment of zero block acceleration, not the physical state or
the existence/stability of its ODE solution.

Only this new inbox review is submitted. External Julia/CSV sources and all
existing reviews, state and registry are untouched. No Julia, Lean, SDP,
trajectory simulation, partition search or full regression was run. One bounded
Fraction calculation evaluated the existing coefficient tables on this single
symbolic ray and solved a 6×6 rational linear system; no floating sample was used.

## 1. Which equality set admits the ray?

External filenames below are relative to
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.
Use s for ray amplitude, not ODE time, and set

```text
q=s e6, velocity=0, w=0, cs(q2..q5)=(1,0,1,0,1,0,1,0),
a_C=0, vD456=0, r_C=0,
all compact link/force auxiliaries=0,
l_total=-(43/100)s e3 in C=(4,5,6).
```

`routeB_compact_block456_descriptor_structure_audit.jl:145–148` assembles only
its link/channel equations, remote balance, port balance and total residual.
Its remote equation at lines 65–67 is
`M_DD vD456 + (M_DC−M0_DC)a_C=0`, not physical D-row force balance.
`routeB_compact_block456_manual_sparse_gram_probe.jl:32–36` selects those
equations plus circles (or their channel-eliminated version). Merely including
the factorized source does not add every polynomial defined by that source to
this selected ideal. Hence the original zero-a_C ray survives these equations.

The included `routeB_factorized_descriptor_model.jl` already defines a different,
full force interface:

| Source span | Meaning |
|---|---|
| 187–200 | Load J/M/C/G, controller parameters, g0, tau, and `rhs=tau−Cvv−G` |
| 220–239 | 36 kinematic link equations for one **full six-vector a**; mass action |
| 245–263 | 21 physical force channels and regularized row sums |
| 265–279 | Positive link Gram plus mu times squared full acceleration |
| 281–287 | Full descriptor residuals and their split substitution identity |

The physical graph equations must be set to zero explicitly. In particular,
`force_balance_aux` at 253–254 is the mass-action **left-hand side**, not a
zero balance by itself. The missing split equations are

```text
sum_{link=j..6} phi_phys(link,j) + mu*alpha_j - rhs_j(q,v,w) = 0,
j=1..6,  mu=1/1000000.
```

Setting only `force_balance_aux=0` would remove the controller torque and
incorrectly retain the zero-acceleration ray.

## 2. Exact analytic force on the ray: 2/5, not 43/100

The factorized loader rejects q6 modes in G (lines 113–123); the loaded gravity
CSV has no q6 mode and no row-6 terms. Thus on q=s e6 its G is exactly its g0.
All Coriolis terms contain two velocity factors (line 198), and the damping and
input terms vanish at v=w=0. Since Kp6=2/5 (line 192), the loaded analytic model
therefore gives

```text
R(s) := rhs(s e6,0,0) = -(2/5)s e6.
```

The compact nominal force instead adds `MGL_C456[3]=3/100`, so
`F_nom_C(s)=-(43/100)s e3` (compact source 53–64). The extra 3/100 is a nominal
restoring coefficient, not the physical q6 gravity force. Replacing R with F_nom
would be an incorrect source-contract identification.

Off this ray the two source families also need a controller audit: factorized
Kd6=3/5 while `dhport_lib.jl:15` has Kd6=3/10. Both share Kp6=2/5; damping
differences vanish on v=0 but prohibit silently equating the full force functions.

## 3. Minimal conditional exclusion theorem

Fix the same state coordinates C=(4,5,6), D=(1,2,3), the same regularized mass
M_mu, and the same force R. Let alpha be a full physical acceleration and require

```text
M_mu(q) alpha = R(q,v,w),       a_C = alpha_C.
```

At q=s e6,v=w=0, sufficient premises are only:

```text
R_D=0,
R_C=-(2/5)s e3,
kernel(M_DD)={0},
the D and C rows of the above graph,
s != 0.
```

If a_C=0, the D rows give M_DD alpha_D=0, hence alpha_D=0. The C rows now
give 0=−(2/5)s e3, contradiction. This proves **a_C≠0 on that graph** without
expanding a rational inverse into the SOS target. If all six alpha are already
set to zero, the sixth force row alone suffices; if only a_C=0, omitting the D
rows/injectivity would leave an unaccounted remote acceleration.

A source-bound link Gram gives a standard way to discharge injectivity: positive
masses/inertias and mu>0 imply zᵀM_mu z≥mu||z||²; restrict to D. This requires
actual J/mass correspondence, not a boolean from a structure-audit CSV. For a
nonregularized target mu=0 this argument cannot be reused without an independent
injectivity proof.

More generally, with M_DD invertible, define

```text
Z_C = R_C - M_CD M_DD^-1 R_D.
S_C = M_CC - M_CD M_DD^-1 M_DC.
```

Every graph point satisfies S_C alpha_C=Z_C. A zero-C-acceleration graph point
exists exactly when Z_C=0: necessity follows by substitution; sufficiency takes
alpha_C=0 and alpha_D=M_DD^-1 R_D. This exact test needs no claim about reachable
states. On the current analytic ray Z_C=−(2/5)s e3, so the zero-C assignment is
excluded for every s≠0. At s=0, R=0 and the positive regularized graph admits
the unique alpha=0; the strict exclusion deliberately does not include the origin.

## 4. vD456 must remain a correction, not physical alpha_D

A compatible realization of the compact remote variable is obtained by introducing
alpha_D_ref with

```text
M_DD alpha_D_ref + M0_DC alpha_C = R_D,
vD456 = alpha_D - alpha_D_ref,
r_C = M_CD vD456.
```

Subtracting the reference equation from the physical D rows gives exactly the
existing compact equation `M_DD vD456 + (M_DC−M0_DC)alpha_C=0`.
Equivalently, after proving invertibility,
`vD456 = -M_DD^-1 (M_DC−M0_DC)alpha_C`.

On this ray M_DC=M0_DC, hence vD456=0 **even when physical alpha_D is nonzero**.
The bounded rational table solve indeed has a nonzero first remote component.
Consequently, an adapter that identifies vD456 with physical acceleration_D (or
with dq_D) would impose the wrong graph and could exclude valid graph points.
The compact `uD/rD/phiDv` channels are actions on this correction variable;
they are not the full physical D-acceleration force channels.

The smallest safe graph extension is six dense polynomial equations
`M_mu(q)alpha−R=0` with fresh alpha_D and alpha_C identified with aC456.
For a sparse alternative, use the factorized source's 36 full-alpha link equations,
21 full-alpha force-channel equations and six RHS balances with fresh physical
auxiliaries. Reuse of compact channels requires an explicit sum/reference-action
adapter; merely renaming them is unsound. Both alternatives must bind cs to the
actual q when used for a physical source (circles alone do not enforce this).

## 5. One bounded table check: corrected graph lift does not retain this failure

The rational calculation loaded the mass, body-Jacobian and gravity CSVs and
evaluated only s e6. It confirmed the absence of q6 mass/gravity modes and the
mass=weighted-J-Gram identity on this ray, then added the specified diagonal mu.
It solved

```text
A := - (2/5) M_mu(0)^-1 e6,       alpha(s)=s A,
l(s)=s L,                       L=-(43/100)e3 - M0_CC A_C,
vD456=r_C=0.
```

The computed exact nonzero coefficients include

```text
A_6 = -171239834557925784653273038800000 / 6116145213293458385672593132597,
A_1 =     36629422195560230000000000 / 6116145213293458385672593132597.
```

With W=M0_CC^-1, the same direct target on this **changed acceleration lift** is

```text
P_b(s) = [b ||A_C||² + 1/10 - LᵀW L] s².
```

The exact table calculation returned

```text
b_crit = (LᵀW L - 1/10)/||A_C||²
 = -69217332708421719364922112394704007433980630159279044298571832246450227
   /1496194642490122766843902311057615561300616477947808977911349163200000000000
 < 0.
```

Thus in this loaded-table graph, P_b(s)>0 for s≠0 and b≥0, including 1/100 and
3/25. This does not repair the original zero-a_C point in the old ideal; it
replaces that inadmissible assignment with the graph acceleration. It establishes
neither target positivity away from this ray nor a DH/Float64/ODE certificate.
No principal-minor beta origin screen was repeated. The table-to-source identity
and arbitrary-domain force/kinematic contracts remain open.

## 6. DH geometry, finite differences and the runtime boundary

`dhport_lib.jl:11,37–41` has final-link a6=0, alpha6=0 and d6=0.07. Its DH
transform's translation column is independent of q6; earlier frame origins are
also independent of q6. All midpoint COM heights used by potential (63–70) are
therefore independent of q6 in the ideal-real source interpretation. This gives
U(q+s e6)=U(q) for arbitrary q. It implies analytic G(q=s e6)=G(0), and also
the same equality for a central-difference G_h at a fixed nonzero step h, because
the q6 invariance holds at every shifted input q±h e_j. C_h(v)v vanishes at v=0.

Together with the correctly bound controller and an exact mass solve, these are
sufficient DH-source premises for the exclusion theorem. This prose derivation
is not a compiled Lean theorem or an authenticated machine execution. In
particular `exact_ddq` at lines 102–109 uses Float64 finite differences and a
linear solve; its name does not establish an exact-real graph. Loaded global
values, trig/rounding behavior, step, regularizer and solve residual need their
own source/runtime contract.

For a checked approximate implementation, absorb force and solve error into e:

```text
M_runtime alpha_returned = -(2/5)s e6 + e(s).
```

With the actual M_DD invertible, zero returned alpha_C would require

```text
-(2/5)s e3 + e_C - M_CD M_DD^-1 e_D = 0.
```

It is sufficient to prove
`abs((e_C−M_CD M_DD^-1 e_D)_3) < (2/5)*abs(s)`.
This explicitly accounts for nonzero remote force errors; a sixth-row error
bound alone is insufficient when e_D is uncontrolled. Any constant error bound
E excludes only |s|>(5/2)E. It cannot exclude every arbitrarily small nonzero s
without exact invariance or a relative vanishing-error bound. No such runtime
error witness is supplied here, and no nonzero/zero output claim is made for
all floating-point q6 inputs.

Also distinguish a ray of states from a time-parameterized solution: setting
q(t)=t e6 while asserting dq(t)=0 violates qdot=dq. A fixed q=s e6,dq=0 can be
a legitimate initial state with the nonzero acceleration above. Excluding an
equilibrium assignment does not exclude a solution starting there.

## 7. Reusable source-comparator contract and remaining work

The existing `examples/routeb_b45_5_descriptor_terms_adapter_lean/INTERFACE.md`
and `DescriptorTermsAdapter.lean:65–76` already separate two premises about the
same concrete force: `sourceBlockForce=expectedSourceForce` and
`sourceBlockForce=sourceDescriptorRhs`. Their concrete interface is Vec2=(4,5);
its force-scale anchor receipt expressly leaves deployed execution binding open.
Reuse this separation for full six-vectors / C=(4,5,6), not its two-coordinate
types or numerical cross-coupling constants.

The minimal conditional record for this ray should carry:

- source identity: exact file/table versions, controller, mu, gravity/C semantics,
  and state/coordinate ordering;
- kinematic/mass binding: cs(q), parent-before-current frames, COM/Jacobians,
  inertia normalization and M_mu, plus D-block injectivity;
- force binding: the same concrete force equals the selected tau−Cvv−G, with
  the ray identity R_D=0, R_C=−(2/5)s e3 (or its explicit error replacement);
- graph binding: that same force equals M_mu alpha, and aC456=alpha_C;
- auxiliary binding: correction/reference semantics from section 4 for vD456
  and associated force channels;
- if used along an ODE: path stays in the stated domain, qdot=dq and dqdot=alpha,
  with existence/regularity/continuation justified separately.

`SourceBodyMassExtensionalProbe.lean:45–109` provides a candidate exact-real
kinematic/extensional seam. Its mass-function correspondence does not itself
supply the force row, Float64 solve or trajectory premise. Hash equality and
source-anchor checks also do not inhabit these semantic fields.

Priority: bind the physical six-row graph and its correction-variable adapter,
then revisit the target on that graph. Increasing SOS degree or beta_a cannot
remove the old ideal's zero-a_C point. Graph exclusion by itself does not prove
any full-domain residual/energy inequality or parent admission.

## Source provenance and evidence level

All hashes below were read from current raw bytes. The six external inputs used
by the bounded rational check were also checked unchanged after that calculation.

| External source | SHA256 |
|---|---|
| routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| routeB_factorized_link_jacobians_body_cs_polynomial.csv | df3f1824a91bf9528f74054a7564946d9d76c31fa0aff63bc720698a1c67f2b3 |
| routeB_analytic_gravity_cs_polynomial.csv | 2760489cba6dc2f2d25ac8f33fa5a25e430bb92040c022004d1ef949d3e09c5d |
| dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |

Existing beta review SHA256:
`ea7e916b772347efab65d800fab09b06cab006bf89b3d17ebd4650027b0b653d`.
Its provenance correction SHA256:
`be126815de807875f1176f347169a07dd7443decf04f36b655dfd6542b2fbff8`.
Existing DescriptorTermsAdapter SHA256:
`1455d987f899102e68346a7d8d074b8aa472d721151b6992d373f005a955750a`.
Existing SourceBodyMassExtensionalProbe SHA256:
`bc2a2136576ac0a726f168492789a24703642d44865c1cce6ae9eef57955f76b`.

The bounded Fraction command exited 0 and performed exact elimination, table
mode checks and one-ray Gram comparison only. No full Julia descriptor reifier,
Lean/kernel verification, source acceptance, runtime equivalence, coverage,
flowpipe, physical ODE impossibility or registry promotion is claimed.
