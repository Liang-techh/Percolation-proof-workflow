---
kind: companion_log
task_id: T-P4-039
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T15:45:00-06:00
language: zh-CN
status: pending
---

# T-P4-039 中文协作摘要

我承接了 `T-P4-038` 明确留下的“同一 cell 多行必须共享一个 `theta/lambda`”数学缺口，没有碰 source、coverage、receipt、admission。

核心结论：每一行先写成

`q_i(theta)=A_i theta^2-G_i theta+P_i<=0`，其中 `A_i>0, P_i>=0`，并设 `delta_i=G_i^2-4A_iP_i`。

当每行 `G_i>0, delta_i>=0` 时，对任意两行定义

`C_ij=(G_i A_j-G_j A_i)^2`，
`U_ij=delta_i A_j^2`，
`V_ij=delta_j A_i^2`。

两行存在共同 `theta` 的精确、无平方根判据是

`C_ij <= U_ij+V_ij`

或

`(C_ij-U_ij-V_ij)^2 <= 4 U_ij V_ij`。

由于一维二次不等式的可行集都是闭区间，有限多行存在共同参数，当且仅当每行单独可行且所有 pair 都通过上面的判据。也就是说，同 cell 的 shared-lambda 可行性可以做成 `O(n^2)` exact-rational polynomial checker，不需要 sqrt，也不需要网格搜索。

给了一个明确反例，防止把 rowwise discriminant PASS 当成 shared-lambda PASS：

- 行 1：`A=1,P=2,D=6`，所以 `G=3`，可行区间 `[1,2]`；
- 行 2：`A=1,P=12,D=20`，所以 `G=7`，可行区间 `[3,4]`。

两行的 discriminant 都等于 `1`，各自都 PASS，但没有任何共享 `theta`；pairwise 多项式判据直接 FAIL。

还给了另一个反例说明“把每行 `T-P4-038` 的中心 witness 拿来互相试”并不完备：一行区间 `[5,100]`，另一行 `[1/10,6]`，真实公共区间是 `[5,6]`，但两个行中心都不在公共区间里；`theta=11/2` 才是一个共享有理 witness。

为了给 checker 一个无需搜索的便宜 shared-rational 路线，还证明了 coefficientwise dominating envelope：若有

`A_i<=Abar`，`P_i<=Pbar`，`Glow<=G_i`，并且

`Glow^2 >= 4 Abar Pbar`，

则统一取

`theta_bar=Glow/(2Abar)`

即可同时通过所有行。自然可取 `Abar=max A_i, Pbar=max P_i, Glow=min G_i`。这条只是一条充分条件；它 FAIL 时不能判 shared-lambda 不存在，应回到精确 pairwise gate + 有理 candidate 搜索。

建议后续形式化最小拆分：

1. `young_row_complete_square`；
2. `sqrt_sum_le_iff_poly`（或直接暴露其无 sqrt 右侧为 checker API）；
3. `young_two_rows_common_theta_iff`；
4. finite interval 的 pairwise -> global intersection；
5. `young_common_theta_dominating_envelope`；
6. 最后把 `theta` 映射回历史 `lambda=1+1/theta`。

历史 `lambda` 语言也有直接无除法形式：令 `s=lambda-1>0`，每行只需检查

`P_i s^2-G_i s+A_i<=0`。

当前仍是 `pending mathematical child`。没有声称 concrete P4 cell 已经通过，也没有改 P4/M4/registry 状态。正式推导见 `review-T-P4-039-common-lambda-kuangmanmozun-20260907T1542.md`。
