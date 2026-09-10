---
kind: companion_log
task_id: T-P5-239-RANKONE-TWOCAP-FIBER-SECULAR
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T11:12:00Z
review_commit: daefc28428fc4aeb2461cb70a454e4052cfa3555
status: correction_nonsemantic
admission_label: pending
---

# T-P5-239 arithmetic correction

One scalar arithmetic typo in the immutable review should be read as follows.

At `p=(3/5,4/5)`,

`grad g1(p)=(6/5,8/5)`,

`grad g2(p)=(34/15,4/5)`.

Therefore their determinant is

`(6/5)(4/5) - (8/5)(34/15) = 24/25 - 272/75 = -8/3`,

not `-4/3` as typed once in the review prose.

The only use of this determinant is to establish linear independence. Hence the correction does not change any theorem, multiplier, factorization, or verdict. Solving the exact gradient system still gives uniquely

`lambda1=lambda2=1/2`,

and the resulting quadratic matrix remains

`K=[[13/9,2],[2,3/4]]`, with `det K=-35/12<0`.

All source-binding / coverage / Float64 / Lean / independent-validation / admission / registry boundaries remain unchanged.