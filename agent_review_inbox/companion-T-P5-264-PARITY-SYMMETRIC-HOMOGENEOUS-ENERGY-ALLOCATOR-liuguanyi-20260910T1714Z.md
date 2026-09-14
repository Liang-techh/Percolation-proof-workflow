---
kind: companion_log
review_id: review-T-P5-264-parity-symmetric-homogeneous-energy-allocator-liuguanyi-20260910T1712Z
task_id: T-P5-264-PARITY-SYMMETRIC-HOMOGENEOUS-ENERGY-ALLOCATOR
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T17:14:00Z
inspected_commit: c2bc716919d62ba984a02eda8e16c4bcced824ca
result_commit: 32dbdb379152b48355b110682cfc1314c0ff231a
admission_label: pending
---

# 柳冠一 — T-P5-264 协作交接

- 当前完成：承接 T-P5-263 的非齐次求和 seam。对 `P=sum_d P_d` 建立了总次数能量层 `H_n=sum_{d+e=n}<P_d,P_e>`，并证明 `H_n(-u)=(-1)^n H_n(u)`；因此 centered symmetric source ball 上 even/odd cross energy 的负号不能作为 uniform reserve。
- 精确反射式：令 `E=sum_{d even}P_d`、`O=sum_{d odd}P_d`，则 `max(||P(u)||²,||P(-u)||²)=||E||²+||O||²+2|<E,O>|`。允许先在完整 cross term 内做结构性消去，但不能只消费某一侧的负号。
- 最小常数：若唯一输入是逐次数 `||P_d||²<=κ_d Q^d` 与 `Q<=R`，则 `K_*=(sum_d sqrt(κ_d R^(d-1)))²` 是 minimax sharp 的统一二次 debit；一维同向 homogeneous packet 在正边界精确达到它，因此仅凭逐次数常数不可能再改进。
- 有理 fallback：任取正有理 `ω_d` 且 `sum ω_d=1`，都有 `||sum P_d||²<=Q sum_d κ_d R^(d-1)/ω_d`。该族的下确界正是 `K_*`；只要下游有 strict margin，就一定能选到纯有理权重保持 PASS，无需序列化平方根。
- 保留的 cancellation：同奇偶块内部的 cross terms 不会因反射翻号，应先聚合；更规范的是先按总次数 `n` 聚合 `H_n`，因为同 `n` 的项具有完全相同的径向缩放。已给出 `P1=x,P2=x²,P3=-x³/2` 导致 `H4≡0` 的精确例子。
- 边界提醒：同奇偶但不同总次数的外边界抵消仍不能直接当全球 reserve；`P1=x,P3=-x³` 在 `|x|=1` 抵消，但内部仍有 `x²(1-x²)²` 正 debit。若保留这类 signed cancellation，必须验证整个 `Q∈[0,R]` 的径向多项式。
- 给其他 Agent 的建议：下一步应对真实 P5 polynomial packet 做同一 chart/output metric 下的 homogeneous split，直接算 `H_n` 并寻找 exact same-total-degree identity；若 source cell 实际是平移/单侧而非 centered，则另做 affine-cell/one-sided theorem，不要套用反射结论。
- 未闭合：actual source split、cell symmetry、parameter/domain/trajectory/FD-halo coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry 全部保持 open。
