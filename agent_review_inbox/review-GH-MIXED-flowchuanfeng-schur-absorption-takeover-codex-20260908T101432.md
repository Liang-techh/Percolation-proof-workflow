---
kind: review_result
review_id: review-GH-MIXED-flowchuanfeng-schur-absorption-takeover-codex-20260908T101432
task_id: GH-MIXED-flowchuanfeng-schur-absorption
source_agent: codex-schur-absorption-takeover
created_at: 2026-09-08T10:14:32-06:00
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_CLOSURE_WITH_SOURCE_OBSTRUCTION
lean_compile_status: not_run
source_binding: false
registry_mutation: false
state_mutation: false
final_integration: false
formal_certificate_allowed: false
requested_action: consume the exact single-debit allocation and opposite-base obstruction; supply same-source actual residual, matching metric, cap and base allocation before physical handoff
---

# 流川枫 Schur/PMI absorption 遗留任务接管

## 交付判定

原任务的条件代数边界成立：relative/additive cap、Schur lower binding 与 feedback upper
binding 是不同前提，不能相互替代。当前可交付的是**最小条件闭合接口与缺失 witness 清单**，
不能交付 actual residual 的无条件 closure。

本 review 为指定遗留 task_id 的新 immutable review_result，不更改原 review。
复用已完成的数学 lane，避免重复有限锥、Lean 或全回归：

- 原任务：`review-GH-MIXED-flowchuanfeng-schur-absorption-liuchuanafeng-20260907T1823.md`。
- 数学 companion：`review-GH-MATH-P4-SCHUR-BUDGET-CLOSURE-LOCAL-codex-20260908T094926.md`，
  SHA-256 `4ac37be266ef95b551d092f6135ab8740e03e664c40ae348d62601ccbc5ed3bb`。
- source obstruction：`review-GH-MATH-P4-SCHUR-SOURCE-BINDING-LOCAL-20260908T093715.md`。

本轮不重新运行 companion 中的 Fraction 检查；不执行 Lean/Lake、producer、solver、
远端编译或回归；只新增本文件，不修改 source/state/registry。

## 1. 单次 debit 与 margin floor

设 E,Q,rho,B>=0，Q<=rho E+B，delta>0，rho+delta<=1。
只有另给同一点的 binding `E-Q<=margin`，才有

```text
delta E-B <= E-Q <= margin.
```

只消费该 floor 保证目标 t 的充分且信息层面精确的条件是 `t+B<=delta E`。
“信息层面精确”是对所有只受该 floor 限制的抽象 margin 而言，不是说每个真实 margin
都必须满足该分配。正 slack 不消除 B；E 的上界不能代替所需下界。
Q 已经在 E-Q 中扣过一次，不能再扣 Q 或同一 B 并称为原目标的等价表达式。
非负损失的重复扣除通常只会造成保守性/假阴性；漏掉实际 residual 项则可能不健全。

若使用 feedback `E<=b_fb+c_fb Q`，须另给 c_fb>=0 和 d=1-c_fb rho>0，才得
`d E<=b_fb+c_fb B`、`d Q<=rho b_fb+B`。
b_fb 与下面的 Schur beta 不是同一个对象，除非另有 source 绑定。
此上界不会自动给正 margin floor，也不能由 residual cap 本身产生。

## 2. 与 generic Schur 的精确接线

同一对称正定 H 下，定义
`L=ell'Hell`、`Q=r'Hr`、`c=ell'Hr`，并要求真正的 `l_actual=ell+r`。
则直接 margin 为 `P=beta-L-2c-Q`。

对 Q<=W、lambda>1，generic 给

```text
beta-lambda W-lambda/(lambda-1)L <= P.
```

因此 `t+lambda W+lambda/(lambda-1)L<=beta` 足够推出 t<=P，之后若要 physical margin
还需 P<=margin_actual 的同 normalization 比较。这条直接路线不必经过旧 SchurPMIBinding。
如果走 Euclidean generic API，要以同一个线性 T 同时运输 ell/r，证明 sq(Tz)=z'Hz。

若坚持使用 E=E_A、Q=port square 的旧 binding，它额外恰需

```text
E_A <= beta-L-2c.
```

结合直接目标，两者同时成立当且仅当

```text
beta >= L+2c+max(E_A,t+Q).
```

只知 Q<=W 时，一个可用的无根号联合充分阈值是

```text
beta >= lambda/(lambda-1)L
        + max(E_A+(lambda-1)W, t+lambda W).
```

两支取 max，不相加。完整 H-ball 放大模型的精确联合 robust 阈值为
`L+2sqrt(LW)+max(E_A,t+W)`；这不是 source graph 上的必要条件。
W=0 或 L=0 的边界可能需要 lambda 的端点极限，不能把有限 lambda 失败当作真实不可能。

## 3. Opposite-base 反例必须保留

固定所有 loss=D 和 t，beta=t+D±epsilon 给 opposite relaxed margins。
原 row-token 例固定 ell=metric=theta=1、charge=0.15698624457194343、t=1/100：
base=1/5 的 Young margin 为 `-195698624457194343/10^17`，
base=11/5 时为 `4301375542805657/10^17`，一败一成。
这些是 companion 已核对的十进制 token 算术，不是 Float64/source receipt。

更强的精确抽象例：H=1，ell=r=1，L=Q=W=c=1，lambda=2，t=0。
固定 E_A=1/2、rho=0、B=1、delta=1：

| beta | P=beta-4 | binding E_A-Q<=P | relative cap | target 0<=P |
|---|---:|---|---|---|
| 15/4 | -1/4 | 成立 | 成立 | 失败 |
| 17/4 | 1/4 | 成立 | 成立 | 成立 |

两者共同 floor=-1/2；即使 binding、strict slack 与实际抽象 total square 都存在，
也不能省略 base/target 分配。反例不声称任何机器人状态可达。

## 4. Actual residual 连接判定：仍是 conditional

消费 source-binding review 的 block456 convention：若
`M_DD v+DeltaM_DC a=e_D`、`J M_DD=I`、`r_actual=M_CD v+e_C`，则

```text
r_actual=R a+d,
R=-M_CD J DeltaM_DC,
d=M_CD J e_D+e_C.
```

这个 sign 属于指定 convention，不能与 force-condensation 的另一个 sign 按名字拼接。
若 reference a 不同、ell 含 controller/FD 偏差，都须在 residual identity 中明示其去向。

nominal cap `||Ra||_H²<=W0` 不控制 d。若另证 `||d||_H²<=D`，可取
`W_actual=(sqrt(W0)+sqrt(D))²`，或 eta>0 时取
`W_actual=(1+eta)W0+(1+1/eta)D`。
然后所有 Q、W、cross term 一起改用 actual r；已进入 W_actual 的 defect 只计一次。
旧二维 typed force/accel producer 不能直接充当三维 block456 witness。

当前消费的 source review 尚缺：

1. 执行 residual 与 ell+r_actual 的同源恒等式，以及全部非零 defects 的唯一分配。
2. 同一 H/reference/regularizer/块顺序及 metric transport 身份。
3. actual cap 的同 cell、source、domain 证明，不只是 nominal CSV 系数。
4. beta 的 target allocation；若选旧 absorption，另给 E_A<=beta-L-2c。
5. 同 normalization 的 physical margin comparison 及全域/轨迹使用所需覆盖。

它还保留 descriptor-only 测试族 r=0 而 P<0：按该 review 的对称/逆解释，
`P=-(320003/3000000)t²`。这阻止“零 port 足以闭合 nominal budget”的推论，
不是 source trajectory 反例。本轮没有重新认证其外部矩阵数据或 source 图可达性。

## 5. 最终边界

数学 companion 已给出条件路线；本次完成的是旧 task_id 下的接管结论，不宣称物理闭合。
下一项应攻同源 residual identity 与 beta/cross-term 分配，或证明真实 graph 排除自由
descriptor 反例；重复 absorption 代数不会补齐这些证据。

pending / obstruction；无 Lean 编译声明、无 source/registry admission、无 P4/P5 closure。
