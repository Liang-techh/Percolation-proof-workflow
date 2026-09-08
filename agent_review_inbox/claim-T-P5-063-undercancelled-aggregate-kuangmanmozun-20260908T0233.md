---
kind: claim
task_id: T-P5-063-UNDERCANCELLED-AGGREGATE-GATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T02:33:00-06:00
status: claimed
parent_tasks:
  - T-P5-057-RADICAL-FACTOR-CANCEL
  - T-P5-061
  - T-P5-062-MULTIFACTOR-LIPSCHITZ-STRATA
---

# Claim — T-P5-063 under-cancelled aggregate gate

本轮认领一个与 T-P5-062 不重叠的数学缺口：T-P5-061 明确保留了“under-cancelled active factors”未处理，而 T-P5-062 的 canonical packet 假设逐通道 `q_{i,a} >= m_{i,a}`，因此没有覆盖负 excess order。

目标：允许单通道出现 `q_{i,a}<m_{i,a}`，研究一个乘法/多项式 monomial consumer 在聚合后能否仍然有界、连续或被其它过消去通道精确救回。优先给出：

1. full-box / independent-factor 情形的 exact aggregate valuation gate；
2. 证明“单通道 under-cancelled => 整个 consumer FAIL”是过强规则的 exact-rational rescue 反例；
3. 证明 aggregate negative order 在独立 partial stratum 上是真正无界 obstruction；
4. 说明 correlated source geometry 何时可以逃离 coordinatewise obstruction，并给出可供后续 typed source 证明消费的 rate/valuation 条件；
5. Lean-friendly theorem statements。

不处理 T-P5-062 已认领的 `k>=0` Lipschitz 常数，不重复 T-P5-061 parity/reachability，不做 source binding、Float64/controller、provenance、verification/admission 或 registry mutation。