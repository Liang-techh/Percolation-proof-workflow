---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-BUDGET-CLOSURE-LOCAL-codex-20260908T094926
task_id: GH-MATH-P4-SCHUR-BUDGET-CLOSURE
source_agent: codex-schur-budget-closure-math-lane
created_at: 2026-09-08T09:49:26-06:00
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_MATHEMATICAL_INTERFACE
lean_compile_status: not_run
source_binding: false
registry_mutation: false
state_mutation: false
formal_certificate_allowed: false
final_integration: false
requested_action: choose direct margin allocation or explicitly prove the additional scalar binding; retain actual residual defects, same-metric identities and opposite-base obstruction before any source handoff
---

# Schur budget closure：单次 debit、联合阈值与 actual residual 的缺失条件

## 0. 结论

generic Schur allocation 已提供所需条件代数，但不产生 source allocation。
本轮新的最小联合条件是：在同一状态、同一对称正定 H 下，令

```text
L = ell' H ell,   Q = r' H r,   c = ell' H r,
l_actual = ell+r,  P = beta-l_actual' H l_actual.
```

那么

```text
[E_A-Q <= P  AND  t <= P]
  iff beta >= L+2c+max(E_A,t+Q).                         (J)
```

其中第一项 binding 单独恰为 `E_A<=beta-L-2c`。
若只要直接 margin，则不需要 E_A binding，只需要 `beta>=t+L+2c+Q`。
若要消费旧 absorption，binding 必须额外交付，不能由 port cap 或 generic theorem 生成。
以上是纸面实数代数，不是新 Lean 声明或 source admission。

本轮只新增本 review；不修改旧 artifacts、state、registry 或 source，不跑 Lean/Lake、
producer、solver 或全回归，不触发远端验证。

## 1. 消费的输入与证据等级

主要读取：

- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean`；
- `agent_review_inbox/review-GH-MATH-P4-SCHUR-SOURCE-BINDING-LOCAL-20260908T093715.md`；
- `agent_review_inbox/review-GH-MATH-P4-SCHUR-BUDGET-CLOSURE-codex-20260908T084204.md`；
- `agent_review_inbox/review-GH-MIXED-schur-absorption-reassigned-codex-20260908T083428.md`；
- `agent_review_inbox/review-T-P4-ACTUAL-ROW-MISSING-BASE-takeover-codex-20260908T083428.md`；
- `NEW_P4_032_SchurPMIAbsorption.lean` 中 AbsorbedAt、SchurPMIBinding、FeedbackBinding 与闭合定义段。

本轮没有重新打开外部物理源码或 CSV。关于 source 公式及 descriptor 特例的叙述，
明确消费上述 source-binding review，不当作本轮独立 source reification。
没有检查既有编译 receipt，不重述任何当前 VERIFIED 状态。

## 2. 单次 debit 的三个合法出口

固定状态 x，H 对称正定。若通过 generic Euclidean API，应提供同一个线性 T 满足
`sq(Tz)=z'H z`，并同时运输 ell 和 r。令 Q<=W、lambda>1。

### A. 直接 margin 出口：最少前提

定义

```text
D_lambda = lambda W + lambda/(lambda-1) L,
P_relaxed = beta-D_lambda,
N_lambda = (lambda-1)(beta-t-lambda W)-lambda L.
```

generic 给出 `P_relaxed<=P`。如果 `t+D_lambda<=beta`，则 `t<=P`。
若另有同 normalization 的 `P<=margin_actual`，才可进一步给 `t<=margin_actual`。

精确余项是

```text
(lambda-1)(P-t)
 = N_lambda + ||ell-(lambda-1)r||_H²
   + lambda(lambda-1)(W-Q).
```

W 只替换 port square，而 ell 的 nominal square 与交叉项由同一次 Young/Schur 组合处理。
最终表达式是 P 或 P_relaxed，不是 `P-lambda W`。
lambda W 是一次带权消费，不意味着 B 出现 lambda 倍就是重复计费。

### B. 旧 absorption 出口：另交 scalar binding

若 `E_A>=0`、`Q<=rho E_A+B`、rho,B>=0、delta>0、rho+delta<=1，且
`E_A-Q<=P`，则

```text
delta E_A-B <= E_A-Q <= P.
```

只凭这个 floor 保证 t 的分配条件是 `t+B<=delta E_A`。
它是对“所有满足此 floor 的抽象 P”的精确阈值；不是某个更大实际 P 的必要条件。
正 delta 或 rho<1 都不消除 B；E_A 的上界也不能代替此处所需的下界。
若全域包含 E_A=0 且 B>=0，单靠这个 homogeneous floor 不能得到严格正常数 t。

把 `Q=r'Hr`、`P=beta-L-2c-Q` 代入 binding，消掉的是同一个 Q，得到
`E_A<=beta-L-2c`。这一步没有再扣一遍 port debit。
若 binding 不成立，不能将 generic 的 P_relaxed 改名为 E_A-Q。

### C. total-residual budget 出口：可以改接口，但必须重证预算

也可取 E=beta、Q_total=l_actual'H l_actual，则 `E-Q_total=P` 是定义等式。
但必须独立证明 `beta>=0` 及 `Q_total<=rho_total beta+B_total`；
port-only `Q<=rho E_A+B` 不能按字段名称充当这条 total bound。

三条路线可以选择；不需要为 A 强行建立 B 的额外 binding。
已在 W 内处理的 FD/solve/controller defect 不应再次作为独立损失追加。
对非负 Q 重复扣除通常只是更保守的下界、导致假阴性；错误在于将它说成等价或必要分配。
漏掉交叉项或实际 defect 才可能产生错误正结论。

## 3. 缺失 binding 的精确阈值与可计算充分包络

由 `P=beta-L-2c-Q`，两项条件分别是

```text
binding: beta >= E_A+L+2c,
target:  beta >= t+Q+L+2c.
```

取两者最大值即 (J)，没有 Cauchy 放松。因此若 source 能控制 c 的符号或相关性，
直接交付这个联合阈值可能显著优于全方向范数预算。

若只有 `Q<=W`，H-SPD Cauchy 给 `c<=sqrt(LW)`，于是充分条件为

```text
beta >= L+2sqrt(LW)+max(E_A,t+W).                       (R)
```

在保持 ell、H、W、E_A 固定并允许 r 遍历整个 H-ball 的放大模型中，维数至少为 1：
L>0 时取与 ell 同向且 Q=W 的 r 同时达到两个最坏项；L=0 时 ell=0，
取球边界 Q=W；W=0 时仅有 r=0。因此 (R) 是这个完整球模型的精确联合 robust 阈值。
对带 source graph 相关性、更小可行集或 E_A 随 r 变化的集合，不能声称必要性。

为避免平方根，可给 lambda>1 的单个充分 allocation：

```text
beta >= lambda/(lambda-1)L
        + max(E_A+(lambda-1)W, t+lambda W).             (YJ)
```

证明只用 `2c<=L/(lambda-1)+(lambda-1)Q` 和 Q<=W。
其中 max 的第一支供应 binding，第二支恰是 generic target allocation。
两支是**替代性阈值的最大值，不相加**；相加会把同一 loss 重复分配。

令 a=lambda-1>0，(YJ) 右端等于
`L+L/a+aW+max(E_A,t+W)`。
当 L,W>0 时 a=sqrt(L/W) 达到 (R)。L=0<W 或 W=0<L 时通常只有端点极限，
不能把 robust 非负性误说成总存在有限 lambda witness。
固定 lambda 跨域可用还需逐点分配成立，不能由逐点可选最优 lambda 推出。

此外可给直接 residual 的相关性 cap `c<=C_cross`，则
`beta>=L+2C_cross+max(E_A,t+W)` 充分；C_cross 不要求非负，
但必须是与 Q cap 同一状态/同一 residual 的有效上界。

## 4. Actual residual：需要证明等式，不是选择相同名字

消费 source-binding review 的 block456 convention：

```text
M_DD v+DeltaM_DC a=e_D,   J M_DD=I,
r_actual=M_CD v+e_C,
R=-M_CD J DeltaM_DC,
r_actual=R a+d,   d=M_CD J e_D+e_C.
```

这个正号来自此处 balance 的定义；不能和另一 force-condensation convention 的
`e_C-M_CD J e_D` 无变换拼接。a/reference 若不同，其额外 reference defect 也必须保留。
真正要用的总残差等式是 `l_actual=ell+r_actual`；定义一个 descriptor `lT:=ell+r`
不证明它等于执行 residual。若 ell 本身与 source nominal 有差异，必须把差异显式放入
ell 或 d 一次，并保持后续全部等式使用同一拆分。

若已有 nominal matching cap `||Ra||_H²<=W0`，还需 d=0 的 source 证明或
`||d||_H²<=D`。后一情形可取

```text
W_actual=(sqrt(W0)+sqrt(D))²,
```

或对任何 eta>0 取无根号包络

```text
W_actual=(1+eta)W0+(1+1/eta)D.
```

然后在第 2–3 节**统一替换 Q、W、c 为 actual r 所对应的量**。
不能只用 actual Q，却保留 nominal c 或 nominal W。
若 W0=rho0 E_A+B0、D<=kappa E_A+B_d，则

```text
rho_actual=(1+eta)rho0+(1+1/eta)kappa,
B_actual=(1+eta)B0+(1+1/eta)B_d.
```

旧 absorption 需要对 rho_actual 而非 raw producer rho0 检查严格 slack。
generic A 不要求 rho_actual<1，但要求 beta 的完整 allocation。
W_actual 已经含 d 的费用，不能再次将同一 d 作为尚未计入误差扣除。

source-binding review 指出的 Fin2/Fin4 defect producer 不能直接实例化为 block456
Fin3/Fin3 producer；这里仅给任意维数数学接口，没有构造三维 source witness。
匹配 H 应是同一固定 M0_CC inverse，不是 Euclidean I、B_up inverse 或点态 M_CC inverse。

## 5. 保留 opposite-base 反例：缺 base 不能由 row slack 补齐

### 原有固定 row 系数反例

消费 takeover review 的精确十进制 token `charge=0.15698624457194343`，固定
ell=metric=theta=1、target=1/100。Young loss 为 `2+charge`。

| base | 精确 youngMargin | 是否达到同一 target |
|---|---|---|
| 1/5 | -195698624457194343 / 10^17 | 否 |
| 11/5 | 4301375542805657 / 10^17 | 是 |

这是同一个可见 row coefficient 的 opposite-base 对，不是两种物理状态，也不是
CSV Float64/source reification。本轮仅重新核对上述有理算术，没有读取/验证外部 CSV。
一般地，固定全部 loss=D_lambda 和 target=t，取 beta=t+D_lambda±epsilon，
epsilon>0，relaxed target 的判定相反。因此正 coefficient slack 不供应缺失的 beta。
relaxed 失败不必意味着 direct target 失败，下面给出同时达到 Young 上界的精确特例。

### 加强：同一 actual 抽象 residual、同一 absorption 前提，也可相反

在一维实数 H=1 中取 ell=r=1，L=Q=W=c=1，lambda=2，t=0。
Young loss=4 恰等于 total square。固定 E_A=1/2、rho=0、B=1、delta=1。

| beta | P=beta-4 | E_A-Q<=P | Q<=rho E_A+B | t<=P |
|---|---:|---|---|---|
| 15/4 | -1/4 | 是 | 是 | 否 |
| 17/4 | 1/4 | 是 | 是 | 是 |

两者有相同 residual、strict slack、有效 scalar binding，且所有这些抽象前提成立。
共同 floor 是 `delta E_A-B=-1/2`，不保证 t=0；真实 P 则可以在 floor 之上分别落于
零的两侧。它同时说明“binding 存在”不等于“target allocation 已闭合”。
这不是机器人轨迹反例；将一维向量嵌入三维第一坐标也只得到抽象接口例子。

## 6. Source obstruction 保留，feedback 不混用

source-binding review 给出的 q_conf=dq=w=0、a=t e1、v=r=0 特例，只满足其所查
九条 descriptor 约束，不宣称完整 graph/轨迹可达。按该 review 的同 metric 解释，

```text
K11=350003/3000000,
E_A=(66687/500000)t²,
P_direct=-(320003/3000000)t².
```

非零 t 时 nominal port cap 即使为零，margin 仍负。此例作为**被消费的条件 obstruction**
保留；本轮不重证 K 的 source/SPD/inverse 身份。
补救只能是证明真实 graph 排除该自由 a 点、改变并证明 beta allocation，或采用另一个
真实成立的比较接口，不能只加强 port rho 或重跑同一代数。

FeedbackBinding 的 `E_A<=b_fb+c_fb Q` 是独立 upper comparison。
b_fb 不自动等于 beta；若使用它，须 c_fb>=0 且 `d_fb=1-c_fb rho_actual>0`，才得

```text
d_fb E_A <= b_fb+c_fb B_actual,
d_fb Q <= rho_actual b_fb+B_actual.
```

这些是能量/残差上界，不提供第 2.B 的正 energy floor，也不自动证明 beta allocation。
本轮的 direct margin 路线不需要 feedback；不要增加不必要的闭环前提。

## 7. 当前最小缺失包与下一步

对明确域 X 的每个 x，必须交付：

1. **Source equality:** 同一 controller/reference/regularizer/块顺序的
   `l_actual=ell+r_actual`，全部执行、solve、FD 与 reference defects 的唯一去向。
2. **Metric identity:** H 的对称正定/同一 inverse 身份，或等价 T 的线性与平方恒等式。
3. **Actual cap:** `Q_actual<=W_actual` 的同 cell/source/域证据；历史 nominal row 不能填充。
4. **选择 allocation:** A 路线交 `t+D_lambda<=beta` 或直接相关性阈值；
   B 路线额外交 binding 和 `t+B_actual<=delta E_A`；若同时需要 binding 和 direct target，
   可交 (J) 或 (YJ)。这是数学替代路线，不必全都证明。
5. **Physical comparison:** 若 P 不是最终物理 margin，交 `P<=margin_actual`，含单位和
   normalization。全域/轨迹使用还需域覆盖、状态落域与适用正则性等独立义务。

在所消费的 reviews 中以上缺口仍被列为 missing，当前 generic 文件没有填充它们。
这不是对全仓库所有结果不存在的断言。最有辨别力的下一项工作是给出同源 beta 下界
与 cross-term 上界，或真正的 graph 排除证据；重复 scalar absorption 不会产生它们。

## 8. 检查与快照

只用一次 Python 标准库 Fraction stdin 检查上述两类 opposite-base 数值和若干 (J)
实例，全部通过；这不代替普遍实数代数推导，也不是 Lean/source 检验。

| 输入 | 本轮 SHA-256 |
|---|---|
| generic Schur `.lean` | `a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648` |
| source-binding LOCAL review | `64844ebc45c1ab45bdd8a7d45bdb8661801aac176505887aee76172e54762241` |
| opposite-base takeover review | `3348ea4ac2dea29f5e993f63a0449c3aac8da3d90d36506cbf518403e4f71d49` |

Disposition: conditional mathematics / pending；无 Lean/source admission、无 registry promotion、
无 actual trajectory bound 或 P4/P5 closure。只新增本 review，不修改共享文件。
