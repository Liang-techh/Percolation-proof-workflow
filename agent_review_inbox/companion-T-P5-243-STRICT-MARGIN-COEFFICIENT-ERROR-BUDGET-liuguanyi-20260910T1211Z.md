---
kind: companion_log
task_id: T-P5-243-STRICT-MARGIN-COEFFICIENT-ERROR-BUDGET
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T12:11:00Z
review_commit: e8ba5dc69b700621893313a4202255a98267ebef
status: pending
admission_label: pending
---

# T-P5-243 协作交接

本轮完成的是 T-P5-242 留下的 strict-margin sensitivity 数学接口，不是重新做 cubic/root partition。

核心桥接为：固定一个已经成立的 regular S-lemma multiplier `lambda`，令 `K=lambda M-G`、`d=det K`、`N=d(-A-lambda R)-l^T adj(K)l`，则 `epsilon=N/d` 是可直接消费的垂直 Lyapunov reserve。对系数误差，只要求同一 centered quotient/source branch 上给出

`Delta A<=a`, `gamma M-Delta G>=0`, `M x=Delta l`, `beta=Delta l^T x`。

任取 `theta>0`，总误差收费为

`eta(theta)=a+(gamma+theta)R+beta/theta`。

若 `eta(theta)<=epsilon`，则不需要重新求 cubic multiplier；直接把 multiplier 更新为

`lambda'=lambda+gamma+theta`

即可得到新的 PSD S-lemma certificate。

对 checker 更有用的无除法门是：定义

`E_num=N-d(a+gamma R)`，

只需检查

`d R theta^2-E_num theta+d beta<=0`。

当 `beta>0` 时，存在正 `theta` 的充要条件压缩为

`E_num>0`,

`E_num^2-4 d^2 R beta>=0`。

有理输入下即使判别式等于零也存在有理 `theta=E_num/(2dR)`，因此 strict-margin coefficient-error consumer 可以保持纯有理 packet，不必进入 T-P5-242 的代数扩张/root-isolation 分支。

还有一个重要语义边界：如果上述判别式失败，只能报告“当前 `(a,gamma,beta)` 外包络不足以证明 PASS”，不能自动报告真实数学 FAIL；只有实际同源可达状态与真实系数给出违反 witness 时才能升级为 FAIL。

建议下一步不要继续造新的抽象 trust-region 变体，而是从实际 FD/DH/support-rounding producer 中抽取同键的 `Delta A,Delta l,Delta G`，证明 `Delta A<=a` 与 `gamma M-Delta G>=0`，再由 `Mx=Delta l` 生成 `beta`。另一个独立数学扩展是 source ellipsoid `(M,R)` 本身也被向外扰动时的 domain/cap sensitivity；不要与本轮 target-coefficient perturbation 混在一起。

仍 OPEN：实际 source binding、same-key quotient/common-center、tube/cell/trajectory coverage、Float64/interval 外包、Lean/kernel、封不觉独立验证、admission/registry。