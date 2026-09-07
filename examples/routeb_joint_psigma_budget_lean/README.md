# Route-B joint `p`/`sigma` budget Lean leaf

This is a small, reusable Lean 4.33.1 / Mathlib interface for the M4
abstract joint momentum budget.  It is intentionally not a DH source binding:
there are no robot constants, source imports, coordinate conventions, or
claims about a compiled trajectory.

The formal layers are:

* `MomentumSplit`: the explicit identity `p = m * v + sigma`;
* `NormalizedState`: `xq = q` and `xp = p / m`, i.e. `x = (q,p/m)`;
* `FilterDynamics` and `EnergyDerivative`: an abstract linear filter and its
  supplied chain-rule expression;
* `ForcingBudget` and `SigmaTerminalBound`: finite external budget facts;
* `IntegratedEnergySeam`: the one conditional premise that summarizes the
  required integration/trajectory argument;
* `energy_budget_propagation`: `V(t) <= V(0) + B`;
* `velocity_sq_downstream_bound`: the resulting bound on `v^2`.

The local filter calculation is elementary.  From

```text
xq' = xp,
xp' = -kappa*xq - lambda*xp + forcing,
V = kappa*xq^2/2 + xp^2/2,
```

Lean proves `V' <= forcing^2/(4*lambda)` by an explicit square completion.
The file does not integrate this pointwise inequality.  Instead, an external
proof must provide `IntegratedEnergySeam`, which can encode a genuine
integral, a discrete telescoping ledger, or a verified flowpipe argument.
The seam is therefore open by design and is not evidence of DH source
binding.

## Focused verification

From WSL/Git Bash, run:

```bash
bash verify.sh
```

The verifier is offline, checks Lean 4.33.1 and Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`, rejects proof-escape tokens, and
audits the printed theorem axiom reports.  It does not run a repository-wide
test suite.
