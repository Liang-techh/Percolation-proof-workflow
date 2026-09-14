---
kind: companion_log
review_id: companion-T-P5-278-structured-quadratic-graph-reserve-kuangmanmozun-20260910T2032Z
task_id: T-P5-278-STRUCTURED-QUADRATIC-GRAPH-RESERVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T20:32:00Z
inspected_commit: 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94
review_commit: d6c44a2fda8af5f197bd2a0032ab982cce577be6
status: pending
admission_label: pending
---

# T-P5-278 协作摘要 — 狂蛮魔尊

本轮接住 T-P5-277 留下的 structured perturbation graph seam，没有去做 provenance / receipt / admission / re-audit，也没有重复 root solver。

## 当前完成

把扰动写成

`e(y+s)-e(y)=a s+b s^2+w(s)`，

只对真正未解析的二阶 remainder 使用

`4 w(s)^2 <= K s^4`。

若 nominal strong-convex support 是

`p(y+s)>=p(y)+(mu/2)s^2`

且 anchor reserve 至少为 `R`，令

`m=mu+2b`，

`H(s)=2R+2as+ms^2`。

那么 graph-tube robust safety 在任意 fiber 上精确等价于同时验证

1. `H(s)>=0`；
2. `H(s)^2-Ks^4>=0`。

所以 bounded rational fiber 只剩一个二次和一个四次的一元非负性问题；strict-margin 可走 Bernstein，touching/zero-margin 可直接复用 T-P5-266 的 Sturm/multiplicity packet。

如果要求对所有 `s in R` 都成立且 `R>0`，定义

`A=2Rm-a^2`，

则得到完全 fraction-free 的必要充分门：

`A>=0` 且 `A^2>=4R^2K`。

`R=0` 时单独精确分支是

`a=0, m>=0, m^2>=K`。

## 发现的问题

T-P5-277 的 scalar secant cone 会把有利的 signed slope / positive curvature 一起按绝对值收费。精确反例：

`mu=2, R=1, e(s)=2s+s^2, s in [-1,1]`。

真实 structured lower support `1+2s+2s^2` 的最小值是 `1/2`，因此严格安全；但同一 interval 上最优 secant constant 已经是 `D=9`，而旧 gate 需要 `D<=4`，所以即使不是 derivative-bound 松弛，direction-forgetting 本身也会产生 false negative。

另一个容易出错的点是 square elimination：不能只检查 `H^2-Ks^4>=0` 而漏掉 `H>=0`；全实线 closed form 也不能只检查 `A^2>=4R^2K` 而漏掉 `A>=0`。

## 给其他 Agent 的建议

- 如果 source producer 能给同一 key 下的 `a,b,K`，优先保留 `a,b` 的符号，不要先压成一个 `D`。
- `K` 可以由同一 collar 上 `(e''-2b)^2<=K` 推出；结论是 `4w^2<=Ks^4`，checker 无需存平方根。
- 若 bounded fiber 是 clamp 后的一侧区间，尤其不要把它重新对称化；有利的一阶符号可能完全免费。
- 若 graph-tube 只是 actual error 的外包络，则 gate 失败只能算 `CERTIFICATE_NOT_FOUND`；除非能重构真实 same-key witness，否则不能升级成物理 FAIL。
- Lean 槽若后续形式化，最小叶子应是 `quadraticGraphTube_robust_iff_polynomialPair` 与正 reserve 的 `A/A^2` fraction-free gate，不要夹带 source admission。

## 建议的下一步

优先从 actual P5 quartic/FD perturbation 中找一个同源 `a,b,K` 实例，测试本 route 是否真正避免 atlas rebuild。只有 actual packet 仍失败时，再开 signed cubic remainder lane；目前继续抽象泛化的边际价值低于 source binding。

关联正式 review：`review-T-P5-278-STRUCTURED-QUADRATIC-GRAPH-RESERVE-kuangmanmozun-20260910T2031Z.md`。
