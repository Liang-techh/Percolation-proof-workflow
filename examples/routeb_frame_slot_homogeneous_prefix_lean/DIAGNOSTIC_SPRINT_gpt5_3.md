## 诊断报告（gpt-5.3-codex-spark, resource-constrained）

目标路径：
`examples/routeb_frame_slot_homogeneous_prefix_lean/FrameSlotHomogeneousPrefix.lean`

### 现状判断

1. 当前窄定理 `routeBFrameSlot_eq_routeBHomogeneousPrefix` 在一条
`fin_cases i <;> simp [...]` 里同时展开了：
   - `routeBFrameSlot`
   - `routeBHomogeneousPrefix`
   - `prefixFrame`
   - `routeBStepFunction`
   - `routeB_step_is_homogeneous`

   这会在 `simpa`/`simp` 时把七槽 `prefix` 与 4x4 矩阵乘法结构连同 `step` 展开成较重的重写链，造成时延波动。

2. 历史 run 日志显示过两类“非数学瓶颈”型错误：
   - `unknown module prefix 'RealDHStep'` / `HomogeneousRotationProjection`
   - `unknown module prefix 'FrameRecursion'`
   这类是上游 olean/`LEAN_PATH` 缺失导致的中断，不是该文件本身逻辑错误。

3. 文件层面的 dependency set 已经很短，核心外部依赖应维持在三层：
   - `ConcreteStepHomogeneous`（提供 `stepRotation/stepTranslation` 和
     `routeB_step_is_homogeneous`）
   - `HomogeneousPrefixProjection`（提供 `homogeneousPrefix` 与
     `rotationPrefix`）
   - `FrameSlotAccessor`（提供 `routeBFrameSlot` 与 `prefixFrame`）

   更大影响是 proof script 的展开策略，不是 import 数量本身。

### 建议修复（优先级高）

1. **采用“逐槽运输”重写骨架**（已在 `routeb_frame_slot_homogeneous_prefix_v2_lean`
   实现过）：新增局部 lemma：
   - 对任意 `s、r、p` 和逐槽等式 `h : ∀ k, s k = homogeneous (r k) (p k)`，
     证明 `prefixFrame s i = homogeneousPrefix r p i`。
   - 每个 `Fin` 情况只做 `rw [h 0, h 1, ...]` + `simp [prefixFrame, homogeneousPrefix, one_mul]`。

2. **减少可回避的 `simp` 展开**：
   - 避免在单条 `simp` 里同时展开
     `routeBHomogeneousPrefix` + `routeBStepFunction` + `homogeneousPrefix`。
   - 先做 `rw`/`simpa` 的结构等价变换，再按槽次序逐个替换 `h k`，而不是一次性全展开。

3. **建议替换为**：
   - 直接用 `exact prefixFrame_eq_homogeneousPrefix_of_step ... (fun k => routeB_step_is_homogeneous k (q k)) i`
   的形状，既保留可读性又显式控制展开边界。

4. **最小 import 观察**：
   目前不建议再删更多 import；真正收益在于 proof 内部重写策略。
   如果后续实测仍卡，下一步再做 namespace 局部裁剪（保留 `FrameSlotAccessor` 与
   `HomogeneousPrefixProjection`，尝试去掉 `ConcreteStepHomogeneous` 的全部打开命名空间改为
   局部限定调用）。

### 立即可执行的一步（无全量回归）

用 `v2` 逻辑替换当前定理，不改 verifier 体系结构，先做一次该文件单测编译并记录
`--stats --profile`（只跑该文件）确认是否恢复到可控时延。
