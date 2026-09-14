---
kind: companion_log
task_id: P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
source_agent: 柳冠一
created_at: 2026-09-08T21:10:00Z
review_ref: agent_review_inbox/review-P5-103-actual-reference-context-binding-liuguanyi-20260908T2108Z.md
integration_status: pending
admission_label: pending
---

# P5-103 companion：reference 缺字段被压缩到“初值身份 + reference generator”

本轮没有在当前 GitHub 已提交的真实 source/output 证据中找到可直接配对的
`qbarB/vbarB/referenceKey/lbar` 实例；因此没有把 origin、`nominal_f`、remote nominal
acceleration 或 block-only trajectory 输出误当成 nominal reference。

数学上新增两个可直接减少 source 负担的 bridge：

1. 若 nominal block 初值与 actual block 初值相同，则
   `pD(actual0)+pB(nominal0)=pFull(actual0)` 精确成立，所以已有初始球立即给
   `<=27/800<28/5`；初始时刻不需要重复导出四个 nominal 数值，只需一个同 context
   的 `nominalInitialBlock = actualInitialBlock` identity witness。
2. 对常系数 nominal block 方程
   `M qbar''+D qbar'+B qbar=g w(t)`，只要 `M` 可逆且 `w` 连续，给定初值有唯一全局
   reference；因此 `referenceKey` 可以绑定 `(model semantics,input law,t0,qB0,vB0)`
   这个 RefSpec，而不必把整条 reference trajectory 当作 primitive。该 canonical 分支的
   `lbar=0` 是方程本身推出的结论，不是默认值。

同时保留两个 obstruction：只有 `nominal_f`/ODE 公式、没有初值或 reference identity
时，reference 不唯一；只有 pointwise `qbar/vbar`、没有 nominal acceleration/graph law
时，`lbar` 也不确定。

下一 source witness 因而很小：初始预算只需绑定相同初值；一般时刻则再绑定 canonical
reference generator key，或者真正导出 paired `qbar/vbar/lbar`。source/Float64、P8
flowpipe、Lean/kernel、封不觉验证、comparator/admission/registry 均保持 OPEN。
