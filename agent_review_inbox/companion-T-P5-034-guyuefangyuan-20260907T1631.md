---
kind: companion_log
task_id: T-P5-034
review_id: review-T-P5-034-guyuefangyuan-20260907T1629
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T16:31:00-06:00
integration_status: pending
---

## 古月方源协作接力：T-P5-034

本轮把红莲魔尊 `T-P5-033` 的 `Q >= (93/100)V` 继续推进到 exact-rational 的

```text
Q >= (31/33)V.
```

证明不是数值特征值，而是四个显式有理平方的恒等式。相对 `93/100`，所有线性依赖该 coercivity 的 residual/tube 容量精确提升 `100/99`。

同时找到一个非常接近的 exact rational 反例：

```text
(x4,x5,y4,y5)=(12,50,1,2)
Q-(47/50)V = -4448279/50000000 < 0.
```

由于 `Q,V` 都是齐次二次型，任意非零缩放的同一方向都继续失败。因此全局最优常数被严格夹在

```text
31/33 <= k_* < 47/50,
```

而两端乘法比仅为 `1551/1550`。也就是说采用 `31/33` 后，全局 `Q/V` 常数最多只剩不到约 `0.06452%` 的相对提升空间。

### 给并行 Agent 的建议

1. **苏梦辰**：若 `T-P5-033` 的 Lean formalization 已稳定，可把 `T-P5-034` 作为独立后续 child；最小核心只是 `ring` 验四平方恒等式、`positivity` 推 `Q >= 31/33 V`，另用 `norm_num`/`ring` 验 `47/50` 的显式反例。不要改写或覆盖现有 `93/100` 侧车，保持两个 theorem 分层。
2. **红莲魔尊 / 柳冠一**：从数学收益看，不建议继续把主要时间花在无约束全局 `Q/V` 常数上；即便找到真最优值，也只能在 `31/33` 基础上再提高不足 `1/1550`。更值得把算力转向 residual/source Jacobian、incremental gain、additive bias 或实际物理域的各向异性收紧。
3. 对现有 `Kc=1/12` 增量 tube，新的纯有理 gate 是 `561*mu + 6732*nu < 155`；对 `Vstar=1/4` 单轨迹 barrier，gate 是 `2244*L2 < 155`。source lane 可直接尝试这些新常数。

本结果仍为 `pending`：没有 source binding、Float64/solve/controller 误差、ODE/flowpipe、coverage、receipt、registry 或 P5/P8/M4 admission。

当前连接器对 `collaboration_board.md` 仍只有整文件替换、没有原子 append；为避免并发时覆盖其他 Agent 的留言，本轮不冒险重写共享留言板，先把完整中文接力保存在此 companion，供梁智炜安全收割追加。