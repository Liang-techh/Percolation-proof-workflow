---
kind: review_result
review_id: review-GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET-codex-20260908
task_id: GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET
agent: codex-block456-matching-budget-lane
source_agent: codex-block456-matching-budget-lane
created_at: 2026-09-08
status: pending
integration_status: pending
admission_label: pending
proof_status: conditional_mathematical_interface
lean_compile_status: not_run
source_binding_status: missing_current_source_to_recorded_csv_binding
registry_eligible: false
registry_mutation: false
final_integration: false
proposed_integration_target: P4.block456.matching_metric_port_budget
requested_action: consume rho2_m0_upper only with a same-cell same-reference operator witness and residual equality; transport both residual vectors through the fixed metric map before generic allocation; reconcile the recorded producer version before intake
---

# Block456 matching-metric port budget：列语义、最小接口与 intake 障碍

结论：generic allocation 所需的标量预算应为

```text
W_budget(x) = rho2_m0_upper[k] * a_C(x)' B_up[k] a_C(x),
r_C(x)' H r_C(x) ≤ W_budget(x),       H=M0_CC^-1.
```

该公式目前只是**条件接口**。必须绑定同一 cell、同一 source residual、同一固定 nominal
M0_CC 和有效的 interval/operator witness。三种 rho² 列不能互换；现有 CSV 的 producer
哈希与当前源码不匹配，当前阅读范围也不足以认证 interval rounding、source mapping 或覆盖。

本轮只读用户指定的 probe 源码及其两组现有 CSV/报告、direct block456 metric review、
generic Schur `.lean`/review。没有展开读取被 include 的 interval library、mass CSV、cover
文件或其他 source lane；没有执行 producer、全覆盖、全回归、Lean、solver 或 CI。
只新增此 review，不修改任何 source、state、registry 或旧 sidecar。

## 1. 固定对象与最小算子不等式

probe 的块序是 D=(1,2,3)、C=(4,5,6)。下文使用不同字母避免把矩阵 H 和标量 W 混淆：

```text
A(q) = M_DD(q)
G(q) = M_CC(q)
Delta(q) = M_DC(q)-M_DC(0)
R(q) = -M_CD(q)*A(q)^-1*Delta(q)
M0 = M_CC(0),   H=M0^-1
P_k = B_up[k] = diag(bdiag1_upper,bdiag2_upper,bdiag3_upper).
```

在 cell k 上，足够且直接的 budget witness 是

```text
R(q)' H R(q) ⪯ gamma_k P_k       for every q in cell k,
r_C(x)=R(q(x))*a_C(x),           q(x) in cell k,
gamma_k = rho2_m0_upper[k].
```

代入同一个 a_C 即得 `r_C' H r_C ≤ gamma_k*a_C'P_k*a_C`。
`⪯` 在这里仅表示对所有实向量的二次型不等式；消费者可以直接接收这个性质，
无需先实现完整矩阵谱 API 或再推导 Schur。

production-facing record 可采用如下最小结构（接口伪码，非已编译 Lean）：

```text
CellPortBudget(k,H,P_k,gamma_k,R) :
  gamma_nonnegative : 0 <= gamma_k
  metric_reference  : H denotes the chosen inverse M0_CC
  input_positive    : P_k is positive definite
  operator_bound    : forall q in cell k, forall a,
                     quad H (R(q)*a) <= gamma_k*quad P_k a

StatePortBinding(x,k) :
  cell_membership   : q(x) in cell k
  residual_identity : r_C(x)=R(q(x))*a_C(x).
```

记录中的同一 reference/domain/coordinate identities 是实际数学绑定，不由字符串一致代替。
在消费层，最弱必需前提甚至只是 `quad H r_C ≤ W_budget`；上述 record 是把 probe 输出
变成这个前提的可审查路径。P_k 的 Gershgorin 上界性质是 producer 的输入尺度选择，
**并不能单独推出 R 的预算**；仍需 operator_bound。

## 2. 三列精确对应三个不同的算子

当前源码中以下 C0、LB 均指 exact Cholesky 对象被 interval 程序包含的理想值，
不是任意选取区间矩阵中的一个 midpoint。

| CSV 列 | 实际构造的算子 | 条件成立时可消费的不等式 |
|---|---|---|
| `rho2_upper` | `R*P_k^(-1/2)` | `||r_C||² ≤ rho2_upper * a_C'P_k*a_C` |
| `rho2_bchol_upper` | `LB^-1*DB*R`, 其中 `LB LB'=DB G(q) DB` | `r_C'G(q)^-1 r_C ≤ rho2_bchol_upper * ||a_C||²` |
| `rho2_m0_upper` | `C0^-1*R*P_k^(-1/2)`, 其中 `C0 C0'=M0` | `r_C'H r_C ≤ rho2_m0_upper * a_C'P_k*a_C` |

第一列的 source `T[i,j]=R[i,j]/sqrt(bdiag[j])` 只对输入做对角归一化。
第二列的 `forward_interval(bchol.L,[DB[i]*R[i,j]])` **没有**右乘 `P_k^-1/2`。
第三列才同时执行固定 nominal 输出 whitening 和 P_k 输入归一化。

第二列的输出 metric 来自

```text
(LB^-1 DB)'(LB^-1 DB)
  = DB*(DB G DB)^-1*DB = G^-1.
```

第三列则使用 `(C0^-1)' C0^-1=M0^-1=H`。
所以第二列不仅输出 metric 与第三列不同，连输入 budget 也不同。
“同为三维”或“同为 rho²”不构成替换规则。

各列的数学 bound 机制均是 `||T||_2² ≤ ||T||_1 ||T||_infinity`，
配合逐项 interval absolute upper bounds 和正确的 outward norm sums/product。
列名已经是 **rho 的平方上界 gamma**；预算是 `gamma*A_up`，不能再平方 gamma。

报告中 B-Cholesky 数字大于 Euclidean 数字是序列化数值的比较，但由于上述规范不同，
**不能单凭这种大小关系证明 B-Cholesky 更松或更紧**。

### 若不得不从其他列转换

- 已验证 `H⪯kappa I` 时，Euclidean 列可给
  `W_budget=kappa*rho2_upper*a_C'P_k*a_C`。
- 已验证 cell 上 `H⪯kappa G(q)^-1` 时，B-Cholesky 列可给
  `W_budget=kappa*rho2_bchol_upper*||a_C||²`。
  SPD 条件下，充分且等价的矩阵 comparison 是 `G(q)⪯kappa M0`。
- 若第二种还要写成 P_k 输入形式，则额外提供 `m I⪯P_k, m>0`，得到
  `W_budget=(kappa/m)*rho2_bchol_upper*a_C'P_k*a_C`。

这些 kappa/m 都需要证明和计费，不能隐含取 1。
generic allocation 本身接受任意已证明的标量 W_budget，并不强制其必须是 P_k 形式。

## 3. 接到现有 generic Schur sidecar

指定 metric review 已给出固定实线性 map T 的候选公式，满足

```text
sq(Tz)=z'H z,
T(u+v)=Tu+Tv.
```

本轮不重做 LDL、不构造其他平方根、不宣称该 transport 已编译或 source-reified。
只需把同一 map 同时施于 ell 与 r_C，不能只转换一侧。

对同一 source state x，设 `l_total=ell+r_C`，并实例化

```text
n=3,
ell_generic=T(ell),
r_generic=T(r_C),
base=beta_C,
W=W_budget=gamma_k*a_C'P_k*a_C,
lambda>1.
```

matching budget 给出 `sq(r_generic)≤W`。若另外提供

```text
0 ≤ (lambda-1)*(beta_C-target-lambda*W)
     - lambda*(ell'H ell),
```

即可调用 `combined_of_port_budget` 得

```text
target ≤ beta_C - l_total'H l_total.
```

或直接通过 `relaxed_target_le_exact_total` 消费

```text
beta_C-lambda*W-lambda/(lambda-1)*ell'H ell
  ≤ beta_C-l_total'H l_total.
```

这是一次 port budget allocation。不得在右边的 exact total square 之外再减一遍
lambda*W，并把那一项称为已经证明的同一 target。
若直接证明 exact direct target，W/lambda 本来就不是必需输入。

该 budget 只属于 `r_C=R a_C` 这个 homogeneous port。它不自动包含 ell、FD/Float64
additive defects、其他控制残差或全部 l_total。特别是 a_C=0 时右侧为 0；
任何非零 additive residual 都需要自己的同 metric bound，而不能填进这个零预算。

generic 文件当前实际字节中，`hzero` 已经先经 `le_of_eq hzero.symm` 转成 `halloc`；
旧 metric review 的该处静态 type-mismatch 提醒不再描述当前文件。
本轮只确认文本变化，没有读取其他编译 receipt，也不据此更新编译状态。

## 4. 现有 CSV 能说明什么

只读解析两份现有 CSV 的数值/元数据，没有运行 interval 算法：

| 记录的 eta | 行数 / RESOLVED 标签数 | max rho2_upper | max rho2_bchol_upper | max rho2_m0_upper |
|---|---|---|---|---|
| 5.6 | 2560 / 2560 | 约 0.0451310853 | 约 0.0553736810 | 约 0.5895772978 |
| 2.7 | 2560 / 2560 | 约 0.0111444673 | 约 0.0165413413 | 约 0.1923526282 |

两份记录的 M0-pivot 字段均为正，matching-rho 字段均可解析为有限有理十进制。
这些是现有 artifact 的属性，**不是**本轮重新验证 interval solve、coverage 或域包含。

可给后续 exporter 的简单候选上包络为：eta=5.6 使用 `gamma_bar=589578/1000000`，
eta=2.7 使用 `gamma_bar=192353/1000000`，两者共用
`P_bar=diag(133374,50185,33335)/1000000`。
它们包住所读取的序列化数值；要成为数学预算仍须先证明各行有效、参数/metric 同一
和目标域覆盖。保留逐盒 `gamma_k P_k` 通常可避免把不同行的 worst case 相乘。

若有逐盒证明和目标状态的 cell membership，只需要选择一个包含该状态的有效 cell；
边界可被多个闭盒覆盖，不必累加各盒 budget。数量 2560 或 `LIMIT=0` 都不能替代覆盖证明。

## 5. 当前 intake 的具体阻塞

### A. 当前 producer 版本与保存结果不相同

当前 probe 源码 SHA-256：
`62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129`。

两份 CSV 和两份报告均记录 producer SHA-256：
`29710d03c34b8ef7362132a062888b84b17bb92a16a79e37a44818addbe9c90f`。

因此不能接受“当前源码已经产生/验证这些 CSV”的绑定。
这不证明历史 CSV 数值错误；需要旧版本 source/运行证据及到当前语义的对应，
或新的已授权、独立可验同版本 receipt。本任务没有为补齐该证据重跑 producer。

### B. RESOLVED 不是 matching metric 完整证书

source 在 A-Cholesky、solve、bdiag 检查失败时返回 UNKNOWN；但是 optional M0-Cholesky
失败时仅保留 `rho2_m0=Inf,m0_pivot_lower=-Inf`，最终仍可返回 `status="RESOLVED"`。
因此 intake 至少还须要求 matching-rho 为有限非负数、M0-pivot 为正，并有真正的
factor/enclosure witness。这是返回分支的性质，不是在声称现有 5120 行发生了这种失败。

### C. outward arithmetic、reference 和 domain 尚未证明

- `norm1/norminf`、`n1m0/nim0` 的源码累加没有各自显式包在 `up` 中；只在最终乘积上
  调 `up`。须说明实际 rounding context 或提供整个 sum/max/product 的外包证明；
  最后一次乘积向上舍入不能一般地补救上游累加低估。本轮按授权不读取 include library，
  因而不推断其全局 rounding mode，也不声称已证实某次运行舍入错误。
- 区间 Cholesky、forward solve、M0 enclosure、decimal serialization 到接受的实数上界
  都需要对应正确性。把打印出的十进制解析为 Fraction 并不自动证明它是 outward endpoint。
- `Mzero[C,C]` 必须包含同一 exact M0、regularizer 和 C 排列；一个区间 reference
  的 midpoint inverse 不可代替固定 H。被 include 的常数/库未在本任务内审计。
- `qfull` 实际使用 q1=q6=0，仅填入四个 q2–q5 box。推广到全配置需要该 source mass/
  residual 的相应坐标独立性或明确的 slice 域前提，不能仅凭目标也是 block456 推广。
- 行只携带 `(eta,depth,box_id)`，不是完整的 typed cell predicate；cover hash
  `85b907bf8d12f46ee003731c5518a00a9a106c8f5a12e492037ae8fc52b04fdf` 也不证明目标域包含。
  本轮没有读取 cover 或认证 first-exit/source-to-flow。

## 6. 两个最小接口反例

下列都是线性代数接口反例，不是 robot 可达状态。

1. `R=I,P=I,H=4I,a=e1`。Euclidean 列允许 gamma=1，`||r||²=1`；
   实际 `r'Hr=4>1`。所以 `rho2_upper` 不能原样填入 matching cap。
2. `R=I,G=H=I,P=I/100,a=e1`。B-Cholesky 列允许 gamma_b=1，
   `r'G^-1r=||a||²=1`；若误写为 `gamma_b*a'Pa`，右侧只有 1/100。
   即使输出 metric 恰相同，漏掉输入归一化差别也会错误接受。

缺一个关键绑定就已足够阻止当前预算入场：仅有 row scalar 和 RESOLVED 标签，
没有同 reference、同 cell 的 `R'HR⪯gamma P` witness，无法构造 generic theorem 的 hport。
T 的 metric identity 也不会凭空制造这个 inequality。

## 7. 读取版本与最终交付

| 文件 | SHA-256 |
|---|---|
| 当前 partition probe `.jl` | `62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129` |
| eta=5.6 CSV | `1af8d59bf7253f992f13ad9318ea16ad5adb8cfa387dc5866b2f41ca4836dce4` |
| eta=2.7 CSV | `35549e624dba0417fc48314a327ba4211f9c3aae39b8bce97924830cd2568df7` |
| direct metric review `...METRIC-TRANSPORT-codex-20260908T090216.md` | `3a6a5c87109cd54beeb71ff fca70fde9876ebf05186a09160a86daa0cd520eea` |
| 当前 `NEW_P4_032_GenericSchurAllocation20260908.lean` | `a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648` |

数值解析和哈希检查使用 Python 标准库 Fraction/csv/hashlib，脚本由 stdin 执行且禁用
字节码写入。没有新增 checker/Lean 文件，也没有查询或更新 state/registry。
最终可收割内容是第 1–3 节的 matching operator budget 与 generic allocation 接口，
以及第 5–6 节的 intake/替换障碍；保持 **pending / conditional / fail-closed**。
