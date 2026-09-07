---
kind: companion_log
task_id: T-P5-029
source_agent: 狂蛮魔尊
created_at: 2026-09-07T11:55:00-06:00
integration_status: pending
related_review: review-T-P5-029-kuangmanmozun-20260907T1152
---

# T-P5-029 协作摘要

本轮没有重复已经收割的 `T-P5-026-Kpath-interface`。新的数学 child 处理的是：当已有 18-cone/SPN 证书对应基础 gain `K0`，后来因为 source rational widening 或 `T-P5-028` 的参数失配出现非负增量 `E`（特别是 `E = kappa tensor gamma`）时，怎样避免重新跑整套 SPN/LDL 搜索。

核心结论：在每个物理 feasible cone 的非负坐标 `u` 中，若 `|z|=A_C u`、`|Lz|=B_C u`，则非负 gain 增量的附加功率

```text
(B_C u)^T E (A_C u)
```

对应矩阵

```text
C_C(E)=sym(B_C^T E A_C)
```

是逐项非负的。因此若旧 SPN 分解 `H_C=S_C+N_C` 满足逐项 `C_C(E)<=N_C`，可以直接复用原来的 PSD/LDL 部分 `S_C`，只把非负部分改成 `N_C-C_C(E)`。这是对固定 SPN 分解、完全不重算 PSD witness 的必要且充分 charge 条件。

对于 `T-P5-028` 的 rank-one 修正 `E=kappa gamma^T`，令

```text
alpha_C=B_C^T kappa,
beta_C=A_C^T gamma,
```

则 charge 精确为

```text
C_C(E)[i,j]=(alpha_i beta_j + beta_i alpha_j)/2,
```

所以只需检查无除法的有理不等式

```text
alpha_i beta_j + beta_i alpha_j <= 2 N_C[i,j].
```

另给了两个边界反例：第一，`E>=0` 绝不意味着原 signed coordinates 中的 correction matrix 是 PSD，因此不能走 Loewner shortcut；第二，`C<=N` 失败只表示旧 `N` slack 不够，不代表 enlarged gain 不可证，因为也可能从 PSD 部分支付或重新做 SPN 分解。

建议形式化层复用现有 T-P5-026/Kpath sidecar，只新增：`cone_gain_increment_matrix`、`spn_charge_entrywise_increment`、`rankOne_cone_charge`、`spn_charge_rankOne`，以及可选的 `spn_charge_split`。不要重写 cone cover、36→18 lift 或 source pathK。

当前仍是 `pending mathematical child`；不提供 concrete `K_path/kappa/gamma`、source/Float64、P8 coverage、ODE continuation、registry 或 parent closure。待封不觉独立验证 / 待梁智炜最终整合。
