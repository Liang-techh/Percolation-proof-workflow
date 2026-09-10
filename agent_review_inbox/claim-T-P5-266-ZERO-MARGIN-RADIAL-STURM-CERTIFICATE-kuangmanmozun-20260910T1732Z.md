---
kind: task_claim
task_id: T-P5-266-ZERO-MARGIN-RADIAL-STURM-CERTIFICATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T17:32:00Z
inspected_commit: f027ff66827c872da510b17df3467d44d7c2459f
status: completed
admission_label: pending
result_commit: d062e528bc248cd24f09973dcde7cfcf7c00ffae
companion_commit: 032ae9418d1304d7dee65443b2edc2c806611709
---

# Claim — T-P5-266 zero-margin radial Sturm certificate

认领 T-P5-265 明确保留的 zero-margin fallback：当 rational radial polynomial `p(q)=K-A(q)` 只满足非严格 `p>=0`、允许在 `[0,R]` 内接触零点时，Bernstein subdivision 的 strict-margin completeness 不再够用。

目标：构造一个完全 exact-rational、对非严格 univariate interval nonnegativity 也完备的 squarefree-parity + Sturm certificate；区分 interior odd-multiplicity roots 与 endpoint contacts，给出 PASS 的有限 theorem packet、FAIL 时的 rational negative witness extraction，并钉死“只看 squarefree roots / 把端点奇重根也拒绝 / 只查无奇重根不查整体符号”等错误路线。该 child 只做数学 closure；不做 provenance/receipt/admission/re-audit，不声称 actual P5 polynomial/source/coverage、Float64、Lean/kernel 或 parent closure。

完成：正式数学 review 已写入 commit `d062e528bc248cd24f09973dcde7cfcf7c00ffae`；中文 companion 已写入 commit `032ae9418d1304d7dee65443b2edc2c806611709`。