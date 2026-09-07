# T-P4-032：defect norm budget / propagation seam

日期：2026-09-07。新增 `NEW_P4_032_DefectNormBudget.lean` 与本 review。
**未编译、source-independent skeleton**；未执行 Lean/Lake 或求解器，未修改旧文件、
state、registry 或共享脚本。没有把任何 defect 设成零。

## 新增不等式接口

`norm2` 明确经 `WithLp.toLp 2` 使用 `EuclideanSpace ℝ (Fin n)` 的 ℓ₂ 范数。
没有使用原始函数空间 `Fin n → ℝ` 的默认 Pi 范数来冒充 Euclidean norm。
本轮只读取本地 Mathlib 中的相关 API 声明，未执行证明脚本。

设 `R=Rport`、`T=MBD*MDDinv`。`defect_triangle` 从显式身份

```text
rB = R*aB + T*eD + eB
```

给出目标三角不等式：

```text
||rB||₂ ≤ ||R*aB||₂ + ||T*eD||₂ + ||eB||₂。
```

`direct_budget` 接受三项各自的真实上界，给出 `portCap+distalForceCap+localForceCap`。
这是最小接口：不要求存在全局算子范数证书，也不要求 defects 相消。

`ActionBound M k` 将需要的作用界作为证明参数：

```text
k≥0，∀v，||M*v||₂ ≤ k*||v||₂。
```

它不计算 k、不声明 k 等于精确谱范数，也不把某个数值输出当成该证明。
`transported_defect_budget` 在给定 T 的作用界 tau、`||eD||₂≤deltaD` 与
`||eB||₂≤deltaB` 后，得到

```text
||rB||₂ ≤ portCap + tau*deltaD + deltaB。
```

`operator_budget` 再接受 R 的作用界 rho 和 `||aB||₂≤alpha`，得到

```text
||rB||₂ ≤ rho*alpha + tau*deltaD + deltaB。
```

各 cap 的非负性可以从其范数上界前提推出；rho/tau 的非负性则明确存放于
`ActionBound`，保证乘法保持不等式方向。alpha、deltaD、deltaB 的物理单位不同，
不能因都是实数而交换、共用或省略。

可直接提供 T 的作用界；也可用 `ActionBound.comp` 从 MBD 的 beta 界、MDDinv
的 eta 界得到 `tau=beta*eta`。后者可能更保守，不推断矩阵良态、精确左逆或任何
数值 conditioning 事实，也不强制用户走这个分解。

## 与 defect-aware O1 的实际连接

`port_defect_norm_budget` 调用上一轮 `port_identity_with_defects`，完整保留其：

```text
MDDinv*MDD=I，
MDD*delta_a_D + DeltaMDB*aB=eD，
rB−MBD*delta_a_D=eB。
```

然后令 R 为同一个 Rport、T 为同一个 MBD*MDDinv，应用预算定理。
它同时输出范数界和安全平方界：

```text
||rB||₂² ≤ (rho*alpha + tau*deltaD + deltaB)²。
```

平方前证明右端总 cap 非负；保留交叉项，不偷换成三个预算平方的无系数和。
该界允许非零 distal defect 和 port defect；没有从此构造纯 relative-gain 结论。
常数 additive defects 是否能在某个下游能量域吸收，仍需独立前提。

`on_domain_budget` 将身份、作用界和三项 cap 放在同一个 `x∈D` 上。
统一常数的全域有效性是该定理的输入，不是从一个样本、另一个域或另一组矩阵推断。
它不证明 D 非空、source 属于 D 或轨迹留在 D。

## 精确剩余前提

- 编译本 skeleton 及所导入的上一轮 block-defect skeleton，并完成公理检查。
  所有 `#print axioms` 只是待执行命令，本轮没有输出或 kernel receipt。
- 同一 source/状态/参考模型的准确 defect identity；O1 特化还需要精确左逆。
  本轮不证明 Float64 solve、近似逆或 forcing differences 满足这些身份。
- 同域 port/distal/local 范数 cap；若使用算子传播版本，还需相应 ActionBound。
  不从矩阵数值近似、谱计算或未经认证的 sampling 自动产生这些证明。
- generalized-force 坐标和一次性 normalization 的源绑定；本文件没有再次乘
  PMI normalization，也没有把 port 分量识别成整个物理 residual。
- 若用于更下游结论，仍需其能量、absorption、source-domain/coverage、ODE 或
  continuation 前提。本轮没有 source/coverage/P4/P5/M4 closure 或 registry 声明。
