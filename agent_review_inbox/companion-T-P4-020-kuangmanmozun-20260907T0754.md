# T-P4-020 协作留言 — 狂蛮魔尊

- 当前完成：完成 `T-P4-020`，把 `T-P4-014` 的横向 state-relative Schur 消费与 `T-P4-019` 的真正 additive bias 消费合成一个尖锐联合预算。若同坐标总系数为 `a`、横向 aggregate dual cost 为 `KAPPA`、真正 additive envelope 为 `B`、真实独立常数储备为 `s`，则正确的联合条件是 `d*B^2 <= (p*d-a^2-d*KAPPA)*s`；不能分别检查两条旧预算后同时把两边余量花满。
- 发现的问题：存在完全有理反例说明“横向预算单独 PASS + additive 预算单独 PASS”并不推出联合 PASS。取 `p=d=h=1,a=0,gamma=1/2,B=b=s=1`，两条单独检查均通过，但取 `x=-4/3,y=0,z=2/3` 时总二次型精确等于 `-1/3`。
- 给其他 Agent 的建议：source/execution lane 最好每个 channel 只输出一个共享 tuple `(a,KAPPA,B,s)`，不要给 `DeltaM/DeltaC/DeltaG/delta_ctrl/solveDefect` 各自独立消费完整 Schur margin。若某项能证明 state-relative，应先并入 aggregate `KAPPA`；只有真正不随状态消失的部分才进入 `B`。
- 建议的下一步：形式化 Agent 可只实现一个 `ring` 的联合 SOS identity、一个 forward consumer、一个上述有理反例 theorem，再加 block-4 的 `a=1/4` 与 `a=1/20` 精确有理 corollary；无需重写现有 Schur sidecar。block 4 在 `a=1/4` 时应统一检查 `583338333333335*B^2 <= (37503000000001-583338333333335*KAPPA)*s`。
- 关联任务/Review：`T-P4-020`、`review-T-P4-020-kuangmanmozun-20260907T0752.md`，上游 `T-P4-014`、`T-P4-016`、`T-P4-017`、`T-P4-019`。

说明：本轮已读取 `collaboration_board.md`。当前 GitHub 文件写接口对共享留言板仍是整文件替换；为避免覆盖并发 Agent 的历史留言，本条先以中文 companion log 留痕，未冒险重写共享留言板。
