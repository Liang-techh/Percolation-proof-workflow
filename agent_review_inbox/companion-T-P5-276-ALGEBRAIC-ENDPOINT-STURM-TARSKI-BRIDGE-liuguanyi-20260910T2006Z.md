---
kind: companion_log
review_id: companion-T-P5-276-algebraic-endpoint-sturm-tarski-bridge-liuguanyi-20260910T2006Z
task_id: T-P5-276-ALGEBRAIC-ENDPOINT-STURM-TARSKI-BRIDGE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T20:06:00Z
inspected_commit: 39fa033206a1caadf489f146923b58e3f087735c
review_commit: 20817a3e4dea7e68dcc1c02b52667b9ef995c115
status: completed_math_child
admission_label: pending
---

# 柳冠一协作留言 — T-P5-276

- 当前完成：闭合 T-P5-275 留下的 algebraic moving-endpoint seam。关键不是再给临界根 `tau` 建 Thom selector，而是证明在同一 active fiber 上 `p''>=0` 且 `g(ell)<0<g(r)` 时，代数区间本身就唯一选择 `tau`；`ell<tau<r` 被压成两个 T-P5-270 selected-root sign query。
- 数学桥接：固定外参数时，`TaQ_(ell,r)(K_eta,g)` 的 signed Sturm/Habicht 端点符号都只是多项式在 selected algebraic endpoint 上的符号，因此可直接复用 T-P5-270 的 isolating interval / Thom sign primitive，不需要 cubic radical、浮点根或三套 root matching。
- 新的 transport lemma：唯一 bracketed derivative root 即使是重根也随外参数连续；只要 active reserve 不发生 common-root contact，其符号在连通 `q` cell 上恒定。因此 generic open cell 可只做一次 exact algebraic-endpoint Tarski query，再用 resultant/contact 非零性传播，不必携带整套 parametric PRS。
- 重要边界：`Res(g,K_eta)=0` 不能解释成 active contact；它可能只是区间外的 derivative root 接触。正式 review 给出严格有理 quartic 反例。处理方式是先对 `g` 做 squarefree，再以 `D=gcd(g_sf,K_eta)` 区分 active persistent-zero branch 与 coprime branch；后者只对 `G=g_sf/D` 使用 reduced resultant。projection 零点全部保留为 exact algebraic point cell。
- 给其他 Agent 的建议：后续若接 actual source，不要为 `tau` 另外构造 root selector；先绑定真实 algebraic endpoints、同键 convexity 与 endpoint branch selectors。若 source 根本没有 quartic/algebraic endpoint 结构，应停止抽象延伸并回到实际 packet。
- 建议的下一步：数学上可做 strict convexity `p''>=mu>0` + strict reserve `rho>0` 的 perturbation/root-displacement budget，把 coefficient/FD/bracket 扰动直接收费到 `rho`，避免每次重建完整 algebraic atlas。
- 仍未闭合：actual P5 source binding、state/trajectory realization、cell/flowpipe/FD/reference-halo coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry/parent propagation。
- 关联 Review：`review-T-P5-276-ALGEBRAIC-ENDPOINT-STURM-TARSKI-BRIDGE-liuguanyi-20260910T2004Z.md`；正式数学 commit `20817a3e4dea7e68dcc1c02b52667b9ef995c115`。
