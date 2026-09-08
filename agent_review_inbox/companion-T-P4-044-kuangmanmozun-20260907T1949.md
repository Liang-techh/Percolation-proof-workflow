---
kind: companion_log
task_id: T-P4-044
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T19:49:00-06:00
integration_status: pending
---

## 中文协作留言

本轮沿 `T-P4-043` 再补了一个不与柳冠一 `T-P4-040` generic consumer 重复的数学 child：**共同区间已经 exact 验证后，如果 downstream 收费是 `theta*m`，midpoint 一般不是最优共享 theta，可以向左移动得到严格更大的可吸收预算。**

设所有行 `q_i(t)=A_i t^2-G_i t+P_i` 在同一 `0<a<b` 两端都 `<=0`，且 `A_i>=A0>0`。定义

```text
H = A0(a+b)-m,
D = H^2-4 A0^2 a b.
```

若 checker 给出同一个有理 `t` 并 exact 检查

```text
2 A0 t = H,
a <= t <= b,
D >= 0,
```

则每一行统一有

```text
4 A0 (q_i(t)+m t) <= -D.
```

所以 `D>0` 是显式 strict reserve；`D=0` 是 boundary-only。核心只有两个 ring identity：quadratic chord identity 与

```text
D-(2A0 t-H)^2 = 4A0[A0(t-a)(b-t)-m t].
```

一个重要 checker guard：**不能只检查 `D>=0`**，因为 discriminant 有错误的大收费分支。例如 `a=1,b=4,A0=1,m=10` 时 `D=9>0`，但中心 `t=-5/2`，正区间完全不可行。安全做法是直接检查 `a<=t<=b`，或额外要求 `0<=m<=A0(b-a)` 后使用 `t=H/(2A0)`。

精确反例说明这不是小修小补：取 `q=(t-1)(t-4)`、`m=19/20`，midpoint `t=5/2` 时

```text
q(t)+m t = 1/8 > 0
```

直接 FAIL；但 shifted rational witness `t=81/40` 时

```text
D=161/400,
q(t)+m t = -161/1600 < 0.
```

同一公共区间、同一收费，移动 theta 后严格 PASS。

并且 sharp boundary 也完全有理：同一例取 `m=1`，有

```text
q(t)+t=(t-2)^2,
```

唯一 witness 是 `t=2` 且 reserve=0；任何 `m>1` 对所有正 `t` 都失败。故在“只知道公共 endpoint + 曲率下界 A0”的信息层上，这个 shifted gate 是 sharp 的。

建议苏梦辰/巨阳仙尊若要形式化，只做四个很小的 sidecar lemma：`quadratic_chord_identity`、`shifted_charge_complete_square`、`common_interval_shifted_reserve_mul`、`shifted_witness_mem_interval`，再加 `(1,4,1,19/20)` 的 exact regression。不要把它升级成 source/coverage 结论；`T-P4-042` typed/source bridge、Float64、P8 coverage 仍完全独立。

当前状态：**pending mathematical child**，待封不觉独立验证 / 待梁智炜选择是否收割。