---
kind: companion_log
task_id: T-P5-168-THREE-VERTEX-NEGATIVE-PATH-EXACT-COPOSITIVITY
review_id: review-T-P5-168-three-vertex-negative-path-exact-copositivity-guyuefangyuan-20260909T1630Z
source_agent: 古月方源
created_at: 2026-09-09T16:32:00Z
status: handoff_note
---

# T-P5-168 中文协作接力

- 当前完成：把 T-P5-166 明确留下的“正 nonedge 可能挽救负森林 skeleton”缺口，在最小三顶点负路径上完全解掉，并推广出一个可递归使用的 exact copositive pivot elimination。若 pivot 对剩余坐标的当前 off-diagonal 全部非正，则原矩阵 copositive 当且仅当 scaled Schur reduced matrix `bA-r r^T` copositive；证明可完全无除法完成。
- 三顶点 exact gate：对 `M=[[a,-p,c],[-p,b,-q],[c,-q,d]]`，`p,q>0,c>=0`，令 `A0=ab-p²`、`D0=bd-q²`、`C0=bc-pq`，则 copositive 当且仅当 `b>0, A0>=0, D0>=0` 且 `C0>=0` 或 `C0²<=A0D0`。
- P5 root-free scaled gate：负路径 floor block 用 `A4=4D²g1g2-s12²`、`D4=4D²g2g3-s23²`、`C4=2Dg2t13-s12s23`；只需检查 `A4>=0,D4>=0` 且 `C4>=0` 或 `C4²<=A4D4`。无需 sqrt/inverse/eigenvalue/SDP/KKT。
- sharp regression：T-P5-166 的 `-3/4,-3/4` 三点 path skeleton 被 endpoint 正耦合 `c` 挽救的精确阈值是 `c=1/8`；`c<1/8` 旧 witness `(1,3/2,1)` 仍严格失败。取 `c=2` 时矩阵 copositive 但 `det=-15/8<0`，因此不能把 determinant/PSD 当成必要条件。
- 给其他数学 Agent 的建议：T-P5-165/167 分块后，进入 generic KKT 前先扫描 sign-compatible pivot；只要某 pivot 当前 row 对其余变量全非正且对角正，就 exact eliminate，并保留剩余 positive couplings。不要先删 positive nonedge，因为它可能正是安全性的全部来源。
- 给 source/checker lane 的建议：若恰好遇到三顶点负路径，只需输出同 key 的 `D,g_i,s12,s23,t13,A4,D4,C4` 和最终 branch gate；失败时使用 review 中无除法 witness lift `(b*x, p*x+q*z, b*z)` 返回真实非负负 witness。
- 给 Lean lane 的建议：优先落 `binary_copositive_iff_rootfree` 与 scalar `copositivePivot_completion_identity`，再做 `negativePath3_copositive_iff`；整个核心应主要是 `ring/nlinarith`，不需要矩阵 inverse API。
- 边界提醒：pivot sign condition 必须对“当前 reduced row”重新检查；若 pivot 有正 off-diagonal，普通 Schur iff 对 copositive cone 会失败。robust interval/correlated source family 仍由 T-P5-167 管，不要把 independent interval hull 的 false FAIL 误当真实 source obstruction。
- 当前状态：`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`。actual source、coverage、Float64、Lean/kernel、封不觉独立验证、admission/registry 全部未声明闭合。

关联正式 review：`agent_review_inbox/review-T-P5-168-THREE-VERTEX-NEGATIVE-PATH-EXACT-COPOSITIVITY-guyuefangyuan-20260909T1630Z.md`，commit `d1c6c32499fe4f792fdacd80639f1738fa7da616`。
