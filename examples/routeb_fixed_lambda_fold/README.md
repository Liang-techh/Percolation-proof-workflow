# Fixed-lambda finite witness fold

`check_fold.py` constructs the canonical finite witness sets for the declared
Route-B ledger rows with `lambda=2.0` and `theta=1.0`, for `eta=2.7` and
`eta=5.6`.  It uses exact textual rationals, checks dense one-row-per-box
membership, strict `lambda_upper > 2` and positive candidate margins, and
checks the rounded ledger relation within the existing `1e-15` contract.

This is deliberately weaker than a theorem: it does not bind the source
evaluator, establish true-DH interval coverage, compile Lean, run the
comparator, or modify the verified registry.

```powershell
python -B examples/routeb_fixed_lambda_fold/check_fold.py
```
