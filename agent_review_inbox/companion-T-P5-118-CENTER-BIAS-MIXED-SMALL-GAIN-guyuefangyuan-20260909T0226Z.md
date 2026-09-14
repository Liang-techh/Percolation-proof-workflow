---
kind: companion_log
review_id: review-T-P5-118-center-bias-mixed-small-gain-guyuefangyuan-20260909T0224Z
task_id: T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN
source_agent: 古月方源
created_at: 2026-09-09T02:26:00Z
review_commit: d74f645aefcd7e485cd3b6df03d20b39e4e03826
admission_label: pending
---

# T-P5-118 中文协作接力

- 当前完成：承接 T-P5-117 明确留下的“anchor/storage 中心存在非零 bias 时不能走 homogeneous lane”分支，给出一个完全无根号、无除法的 mixed small-gain theorem。核心做法是保留 centered displacement 对 `V` 的同次依赖，只把真实 center bias 产生的部分路由到 additive floor，而不是把整个 second-jet anchor error 粗暴压成绝对常数。
- 核心 gate：对正有理调参 `r,s`，先用 `r s Q(x+b) <= (r+s)(s Q(x)+r Q(b))`。若 `mQ(x)<=V`、`Q(b)<=B`、`V<=R`，则 bias 后的平方项可分成 `(s^2 R+2rsmB)V + r^2m^2B^2`。接 T-P5-116 的 power packet 后，只需两个 cross-multiplied gate，就能得到 `Vdot <= -(c-alpha)V -(1-theta)Qd + beta`。
- 数学意义：bias 对 relative rate 的新增收费是 `O(B)`，不可消掉的 additive floor 是 `O(B^2)`；由于 `B=Q(b)` 本身已是偏移向量的二次量，所以这个 second-jet floor 对偏移范数是四次小量。若 source 能保留 signed cross correlation，还可能进一步减小；因此建议先形成 signed energy object，再 intervalize。
- 硬 obstruction：非零 bias 不能靠重调 homogeneous 参数变成零 floor。精确标量例 `gamma=d=h=1, V=0, Qd=1, Q(delta)=4, p_A=2` 饱和 square packet，但 nominal ledger 仍允许 `Vdot<=1`。所以如果 source 确认 center mismatch，必须走 additive/mixed lane、证明额外 signed cancellation，或重设计 anchor/storage center 三选一。
- 给 Lean Agent 的建议：优先做 `quadratic_add_weighted` 与 `biased_anchor_power_absorption` 两个纯代数叶；暂时不要碰实际 DH/source/coverage。真实 source packet 冻结后再接 `storageKey/anchorKey/biasKey`。
- 给 source/CSE lane 的建议：下一步最值钱的数据不是另找一个 cell-wide `H2`，而是同键冻结 `b`、`B=Q_Z(b)`、centered comparator `mQ_Z(x)<=V`，以及若能做到的话 `2B_Q(x,b)` 的一侧 signed enclosure。
- 当前状态：仅 `CONDITIONAL_PASS / pending mathematical child`。真实 source、same-segment coverage、最终 `(alpha,beta,theta,R0)` P5 margin、Float64/FD/controller/P8、Lean/kernel、封不觉独立验证和 admission/registry 都保持 open。
- 协作留言板：当前 GitHub contents 写接口仍只能整文件 replacement，而我读取到的 `collaboration_board.md` 内容会截断；为了不覆盖其他 Agent 历史留言，本轮没有冒险重写留言板。本 companion 已包含可由梁智炜安全 harvest 后追加到留言板的中文接力内容。
