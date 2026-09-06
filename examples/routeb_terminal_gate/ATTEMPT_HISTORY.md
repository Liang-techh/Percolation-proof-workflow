# Exact terminal gate audit history

`verify.py` creates a unique snapshot and runs one Fraction-only audit. The
test state and terminal offset are fixed before execution. There is no solver,
ODE integration, trajectory, search, or broad regression. The result rejects
only the second LP candidate's zero-supply gate and leaves positive supply,
other coefficients and the physical J<=1 theorem open.
