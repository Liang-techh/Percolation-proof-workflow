# routeb_frame_slot_homogeneous_prefix_lean 依赖诊断（短时版）

时间：2026-09-06

1) 路径映射
- 按文件名在当前工作流中未发现 `examples/routeb_frame_slot_homogeneous_prefix_lean`。
- 与该目标最接近的文件是：
  - `examples/routeb_concrete_homogeneous_prefix_lean/ConcreteHomogeneousPrefix.lean`
  - 该文件在多个 run 产物中的 compile 日志中频繁出现。

2) 可复现失败模式
- `run-RUJLBr4n` 与若干 run：`ConcreteHomogeneousPrefix_COMPILE_EXIT_CODE=143`（外部 `Terminated`），说明该文件在某些配置下会卡住/超时。
- `run-0GExomL2` 给出明确 proof 失败：`
  Tactic 'rewrite' failed: Did not find an occurrence of pattern
    routeBRealStepMatrix ?k (?q ?k)`
  in goal containing only `routeBStepFunction`。

3) 根因定位
- 关键瓶颈在 `routeB_frame_slot_eq_homogeneousPrefix`：
  每个 `i` 分支里用 `rw [routeB_step_is_homogeneous q n]`。
- `routeB_step_is_homogeneous` 的 lhs 是 `routeBRealStepMatrix k (q k)`，但目标是链式乘积中的 `routeBStepFunction q k`。
- `routeBStepFunction` 定义为 `fun k => routeBRealStepMatrix k (q k)`，但当前 `rw` 目标没有先 `simp [routeBStepFunction]`，导致重写失败并触发大量 `case` 展开（见日志中大量 `case «2».«3»` 展开），有时表现为中断或超时。

4) 最小 import 评估
- 当前文件直接依赖：
  - `FrameSlotAccessor`
  - `HomogeneousPrefixProjection`
- 这两个已经是较轻量的“专用层”。它们内部固定了 `Mat4` 结构和 7-slot 递推，不建议再扩张。
- 依赖路径中若需完整编译，必须在运行时确保 `LEAN_PATH` 包含：
  - `routeb_frame_slot_accessor_lean`
  - `routeb_homogeneous_prefix_projection_lean`
  - 以及它们的递归依赖（`FramePrefixIndex`、`FrameOriginAxis`、`RealDHStep`、`FrameRecursion`、`HomogeneousRotationProjection`、`RotationPrefixOrthogonality`、`MatrixOrthogonalityClosure`）。
- 不建议再新增 import 以缩短编译体量；若想最小化，按功能反而是减少该文件自己的展开语句（`simp`/`rw`）而不是删 import。

5) 可避免的 simp/展开点
- 不要在同一引理里反复 `simp [routeBFrameSlot, prefixFrame, homogeneousPrefix, routeBStepFunction, Matrix.one_mul]` 后再逐个 `rw ...`。
- 避免在大目标上 `fin_cases i` 后手工 `rw` 线性展开多个分支（当前每个分支会触发独立的 `routeBStepFunction` 归约）。
- 更稳妥：
  - 对每个分支使用单条 `simpa`，例如
    `simpa [routeBFrameSlot, routeBStepFunction, homogeneousPrefix, routeB_step_is_homogeneous]`
  - 先把 `routeBStepFunction` 展开，再应用同一重写定理。

6) 具体修复建议（只改该文件）
- 在 `routeB_frame_slot_eq_homogeneousPrefix` 中把 `rw [...]` 替换为先 `simp`/`simpa` 风格，例如：
  - `simp only [routeBFrameSlot, routeBStepFunction, Matrix.one_mul, homogeneousPrefix]` 先收敛形状。
  - 每个分支再 `simpa [routeB_step_is_homogeneous]`。
- 如需强约束，可在入口加上辅助 lemma：
  - `routeBStepFunction (q)` 与 `routeBRealStepMatrix` 的等价性局部展开（或局部 `dsimp [routeBStepFunction]`）避免重写方向不一致。
- 先单点验证：
  1) 单独验证 `routeB_frame_slot_eq_homogeneousPrefix`。
  2) 再跑 `routeB_frame_slot_rotationBlock_eq_rotationPrefix`。
  3) 保持其他定理不变。

7) 额外风险
- `#print axioms` 显示此文件依赖到 `Classical.choice`, `Quot.sound`, `propext`（来自上游），这是现状可接受的稳定事实，不是当前卡住主因；
  真正的卡住来自目标重写/归约不匹配。
