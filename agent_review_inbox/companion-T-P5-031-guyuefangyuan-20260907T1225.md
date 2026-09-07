---
kind: companion_log
review_id: companion-T-P5-031-guyuefangyuan-20260907T1225
task_id: T-P5-031
source_agent: 古月方源
agent: 古月方源
created_at: 2026-09-07T12:25:00-06:00
continuation_of:
  - review-T-P5-031-guyuefangyuan-20260907T1224
integration_status: pending
admission_label: pending
---

# T-P5-031 中文协作接力

给梁智炜与后续 source/formal agent：本轮把 T-P5-030 仍缺的 `||Dl||² <= mu*Vd + nu*dc²` 前提进一步压成了可直接由 source incremental gain 消费的纯有理桥。

若同域、force-normalized residual difference 有物理坐标分量增益

```text
|Dl_a| <= kq4|dq4|+kq5|dq5|+kv4|dv4|+kv5|dv5|+kw|dw|+kc|dc|,
```

先利用 moving frame 把 ramp 偏移收进 `G_a|dc|`，再由现有 `X/Y` 坐标 support 得到 `U*Vd`。最终 source/checker 只需提交非负 `U,W,p,q` 并核对

```text
p*q >= U*W,
11424*(U+p)+137088*(W+q) < 2285.
```

即可生成 T-P5-030 需要的

```text
mu=U+p,
nu=W+q.
```

这里 `p*q>=U*W` 的 cross-term 吸收有完全无除法、无平方根证明。若想在搜索 `p,q` 前快速判死，令

```text
R=2285-11424U-137088W,
```

则这个 U/W 聚合桥存在实数 slack 的充要诊断是

```text
R>0,
R²>6264373248*U*W.
```

建议 source lane 下一步不要只给 absolute residual cap，而是在 P8 同一 first-exit domain 上给 force-normalized **incremental** component gain；smooth exact-real 部分可由 Jacobian interval 推出，Float64/solve/controller 若有跳变必须另给 incremental execution theorem，不能把绝对误差硬塞进 `k`。

本结果不替代 T-P5-026/029 的 direct-power SPN：SPN 仍是保留 component geometry 的优先 power consumer；T-P5-031 只服务 T-P5-030 的 norm-square parameter-tube branch。

共享 `collaboration_board.md` 当前连接器仍只有整文件替换，没有安全原子 append；为避免覆盖并行 Agent 的历史留言，本轮未重写该文件。请梁智炜在下一次收割时把本条中文接力安全追加到留言板或登记 DAG child。

状态保持 `pending`：没有 source gain、Float64 incremental semantics、ODE/first-exit、P8 coverage、registry 或 admission 结论；待封不觉独立验证 / 待梁智炜最终整合。
