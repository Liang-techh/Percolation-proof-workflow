# Implicit port reduction and original block-output budgets

This directory implements mathematical leaves, not an accepted robot certificate.
All current successful sources use pinned Lean 4.33.1 / Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`. The final statement comparator,
physical source binding, residual budgets and continuation remain open.

## Port reduction

`ImplicitPort.lean` proves the universal double-completion identity replacing
the source auditor's two rational samples. Define H=nu-k and
G=s-k-k²/(nu-k). It retains the exact centers r-kz/H and z+b/(2G), as well as
the acceleration charge k=s*lambda_A/m²+nu*rho²*B/m².

`GateBounds.lean` proves H,G>0 iff k<s*nu/(s+nu). For the declared induced
port candidate rho²=234721/5000000, the two-axis gate at s=5, nu=1/6 is exactly
lambda_A<33638704099/12400000000000000. The old 1/100 placeholder fails.
A positive 1/1000000 satisfies the algebraic gate, but no physical residual
bound with that coefficient is claimed. The port coefficient itself remains
an unadmitted external premise.

`PhysicalPortAssembly.lean` derives the eliminated identity from the explicit
force link m*a=I+r-l. It combines separate port and residual-bracket premises
with the reduced positivity hypothesis to obtain nonnegative dissipation.
It does not set lambda_A=0 or discard an unconstrained acceleration variable.
Fixed-nu port completion is separately proved by `../routeb_port_absorption`.

## Local energy strategy

`BlockTargets.lean` separates the original p<=5.6 domain from qpoly(T)<=12.
The p bound only gives qpoly<=14. A rational set witness refutes the stronger
implication; no claim of a dynamically reachable counterexample is made.

`VariableErrorTube.lean` applies the previously compiled derivative comparison
to E-R, where R is a cumulative error budget. It does not require replacing a
time-dependent total residual by a uniform pointwise 0.1 bound.

`LocalTubeAssembly.lean` composes this with the exact local reference kinetic/PD
storage, full12-ball initial projection and output comparisons from
`../routeb_local_energy_budget`. Its concrete unresolved premise is cumulative
TOTAL reference force cost R(t)<=1/10. Its energy/curve derivative and force
hypotheses are explicit; existence, source semantics, all-coordinate domain
coverage and first-exit closure are NOT conclusions of this conditional leaf.

The implied storage cap is 7251/52000, giving
p<=3867200/869869<5.6 and qpoly<=9668000/869869<12. These are conditional cap
consequences, not validated trajectory bounds. An integral/absolutely-continuous
interface may be needed instead of all-point right derivatives for a rounded RHS.

## Verification and repairs

Run `bash examples/routeb_implicit_port/verify.sh MODULE` in the existing WSL
environment. Only named modules compile; imported successful object hashes are
logged. The cached dependency directories are explicit in the script. Preserve
the output directories: they contain failed and successful source snapshots.

The first port attempt failed on sum binder precedence, a Finset API parameter
and a tactic-sequencing linter. Disabling autoImplicit exposed an accidental
free index; parenthesizing the complete sum body repaired the intended theorem
instead of accepting an unintended extra parameter. Further focused repairs
normalized a distributed scalar sum and pointwise function subtraction. No
broad regression, solver campaign or dependency rebuild was performed.

The proof DAG v3 records active local-energy obligations separately from the
alternative implicit-PMI strategy. Historical v1/v2 graphs and attempts remain
unchanged; no compiled candidate is promoted to the verified registry here.
