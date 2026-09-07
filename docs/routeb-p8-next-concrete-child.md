# Route-B P8 concrete child: 13→14 contract decision

日期：2026-09-06

## 审计范围

本 child 只审计 P8 的状态维度与时间/ramp contract：

- `docs/routeb-p8-flowpipe-binding-next.md`；
- `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean`；
- `examples/routeb_p8_rhs_receipt_lean/P8RhsReceipt.lean`；
- `examples/routeb_p8_rhs_payload_generator/receipt.template.json` 及其
  fail-closed checker；
- generator 所声明的 true-DH probe source contract。

没有修改外部 Route-B source、`artifacts/routeb_6dof/state.json`、registry，
也没有修改现有 parent 或 receipt template。

## 结论

当前 source **不能直接**实例化 `RouteBP8PicardStep.RampRhsPremise`。

父定理的 state 是

```text
Fin 14 = q1..q6, dq1..dq6, w, c
```

并要求对所有 14-state `z`：

```text
F z wSlot = z cSlot
F z cSlot = 0
```

而已审计的 Julia `full_rhs!` 是 13-state：输入只有 `u[1:13]`，并写入
`du[13] = 0`。receipt template 也明确把 `c` 标记为 sidecar、未被 source
消费。因此不是“再填 14 个 endpoint”即可修复的缺口。

### 不可直接 lift 的短证

若把 13-state source 自然补成 14-state，并令新增的 `c` 分量和 `w` 分量
导数都为 0，则在合法状态 `z`（所有分量为 0，唯 `z cSlot = 1`）上：

```text
FullX0 z       （机械能为 0，w=0，c²=1≤3）
F z wSlot = 0
z cSlot = 1
```

故 `F z wSlot = z cSlot` 失败。只有退化子族 `c=0` 能避开冲突，不能覆盖
当前 `FullX0` 的全部扰动族。这个事实已在
`examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` 的
`zeroTailLift_not_ramp` 中以 exact-real Lean 命题表达。

## 最小可修复 adapter

新增 scaffold 提供的是接口层，不是 true-DH 证明：

```text
G : time → State13 → State13
      |
      +-- timeLift G t : State14 → State14
          前 12 个分量来自 G t
          w' = z cSlot
          c' = 0
```

`timeLift_rampPremise` 证明对每个固定时间 `t`，这个 14-state field 满足父
定理的 ramp premise。它只说明如何消除维度/时间 contract mismatch；它没有
证明：

1. 真实 Julia DH `full_rhs!` 的前 12 个分量等于 `G t`；
2. Float64、FD、质量矩阵正则化和线性求解语义等于 exact-real `G`；
3. 任何 outward-rounded RHS interval containment；
4. Picard image 存在、连续延拓、全 `[0,1]` 覆盖或 terminal transfer。

因此 scaffold 的 admission 是 `conditional_interface_only`，不会进入
verified theorem registry，也不会改变 P8/M4 的 fail-closed 状态。

## Child 状态与后续最短链

```text
C13-14  zeroTailLift_not_ramp                         CLOSED (negative fact)
C13-T   timeLift_rampPremise                          COMPILED / conditional
S1      exact source-to-G first-12 semantic binding   OPEN
S2      time-dependent ODE solution adapter           OPEN
S3      outward RHS interval containment              OPEN
S4      Picard image existence and local flowpipe     OPEN
S5      partition continuation and [0,1] coverage     OPEN
S6      true-DH flowpipe theorem                      OPEN
```

这里的 `C13-T` 不能关闭 `S1`：它只是在一个抽象 `G` 已给定的情况下展示
contract 形状。下一项高价值工作应是建立 source body 的前 12 分量语义
binding（包括 DH/FD/solve provenance），而不是运行更长的 rollout 或填充
当前 pending receipt。

## 编译状态

新增目录中的 `verify.sh` 使用与现有 P8 sidecar 相同的 pinned
`/home/z5242/sos_lean` 环境，并设置 `-DwarningAsError=true`。本轮已运行：

```text
P8_CONTRACT_ADAPTER_COMPILE=PASSED
SOURCE_RESTRICTION_CHECK=PASSED
```

若该 pinned 环境不存在，脚本会明确输出 `BUILD_ENV_BLOCKED` 并返回非零；
这不构成 Lean VERIFIED。无 `sorry`、`admit` 或非标准 `axiom`。

## Admission boundary

```text
source_binding       = OPEN
ramp_binding         = OPEN for the deployed 13-state source
adapter_contract     = COMPILED / conditional_interface_only
rhs_endpoint_receipt = PENDING
flowpipe_coverage    = OPEN
formal_certificate_allowed = false
registry              = unchanged
```

