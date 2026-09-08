---
kind: review_result
review_id: review-GH-LEAN-P4-Q6-GRAPH-EXCLUSION-REPAIR-LOCAL-codex-20260908T093620
task_id: GH-LEAN-P4-Q6-GRAPH-EXCLUSION-REPAIR
source_agent: codex-local-static-interface-review
created_at: 2026-09-08T09:36:20-06:00
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
review_method: static_text_only
local_lean_run: false
local_lake_run: false
parsed: false
elaborated: false
kernel_checked: false
axioms_checked: false
verified: false
candidate_modified: false
registry_promoted: false
formal_certificate_allowed: false
requested_action: compile the unchanged hash-bound candidate first in the approved GitHub pinned environment; apply only diagnostic-driven minimal repairs and return a new exact-source receipt
---

# Q6 graph exclusion：窄接口静态 repair 预审

## 结论与范围

只审阅 `examples/routeb_q6_graph_exclusion_lean/Q6GraphExclusionCandidate.lean`
和同目录 `REVIEW.md`，没有读取依赖、workflow、manifest、state、registry 或共享脚本。
本地没有运行 Lean/Lake，也没有调用 GitHub 编译、查询远端源码或提交修改。
本轮仅新增本 review。

**未发现可以从这两个文件单独确认的必修错误。最小首选 repair 是零改动：
先让 GitHub pinned 环境编译原候选，再根据首个真实诊断定点修复。**
以下建议是后备 elaboration 写法，不是已编译补丁，也不是已有错误日志的解释。

静态输入字节 SHA-256：

| 输入 | SHA-256 |
|---|---|
| `Q6GraphExclusionCandidate.lean` | `0538d47800ef99539af0505c60d055752e8e995fe0cc9d871d90f2377a57429b` |
| `REVIEW.md` | `8fdf7864de0211222f41e4377e3eef765aecf5636368ea4804ea64643cdc42bb` |

原 REVIEW 的 `inspected_commit=6509984f9a045c441df64e088b704ee341a1316d`
被原文明确解释为基线，不是包含新增候选的 commit；不得将它填成候选的编译 revision。
本轮没有另行查询候选所在 commit。

## 1. 数学和类型方向的静态核对

- 第 15–16 行的 Semiring / AddCommMonoid / Module 假设足以表达所用零元、加法、
  线性映射及零保持；证明不需要减法、Field、正定性或矩阵逆。
- 第 25–28 行：hD 在 hAC、hRD 下给出 `M_DD alpha_D=0`，再用
  `map_zero M_DD : M_DD 0=0` 的反向等式构造两个映像相等，交给 injectivity。
  当前 `hz.trans (map_zero M_DD).symm` 的等式方向在数学上正确。
- 第 39–40 行：hC.symm 的方向为 `R_C=M_CD alpha_D+M_CC alpha_C`；
  用 hAD、hAC、map_zero 得 `R_C=0+0`，zero_add 足够。无需将 hC 再反向一次。
- 第 50–52、80–82 行直接消去非零假设与零结论的矛盾，不需要 classical/反证自动化。
- 抽象 `zero_C_forces_zero_rhs` 参数顺序是 `alpha_D alpha_C R_C R_D`；
  Fin3 wrapper 自己的顺序是 `alpha_D alpha_C R_D R_C`。
  第 70–71 行调用抽象定理时已正确交换成前者；第 81–82 行调用 wrapper 时仍用后者。
  **不要为了表面统一而把其中一次调用改错。**
- `Vec3 K=Fin 3 → K` 上预期使用点态加法和 K 的左自模结构；没有看到缺少
  CommSemiring 或 FiniteDimensional 假设的数学理由。具体实例可见性仍须目标环境检查。
- 同一个 LinearEquiv 的 underlying map 与 injectivity 正是所需接口；
  当前写法没有声称其来自某个实际质量矩阵或物理块投影。

以上是源文本推演，不表示 Lean 已解析、elaborate 或接受这些声明。

## 2. 仅按真实诊断采用的最小后备修复

### A. import / 环境

当前只有 `Mathlib.Algebra.Module.Equiv.Defs` 和 `Mathlib.Algebra.Module.Pi`。
原 REVIEW 说在 `0df444a360eaa60ab8c11dca51a86af692955474` 看到了这两个源路径；
本轮未读取该 revision 的依赖，不能确认其等于计划中的 GitHub pin，也不能确认编译闭包。

- 若报 `unknown module prefix Mathlib` 或依赖产物缺失，先修 pinned job 的依赖/搜索路径，
  不应改数学假设，更不能用增加 `import Mathlib` 假装解决环境缺失。
- 若确实是目标 pin 下模块改名或声明缺失，在那个 pin 上查出实际定义模块，最多补入
  所需具体 import。现有两文件不足以确定替代路径，本 review 不杜撰一个已确认模块。
- 若诊断明确指向 tactic parser/elaborator 的可见性，再在同 pin 查所需 tactic import；
  当前没有证据表明 `simpa only` 必须增加某个 import。
- 若只报 Pi module instance 缺失，先确认 Module.Pi 真正载入及 K 的自模实例可用，
  不把 Semiring 擅自加强成 Field 来绕过问题。

### B. 第 27–28 行：把 injectivity 应用写得更显式

若真实诊断指向 `apply hDD` 或 `map_zero` 的元变量推断，可试以下等价 proof fragment：

```lean
  have hmap0 : M_DD (0 : D) = (0 : D) := map_zero M_DD
  exact hDD (hz.trans hmap0.symm)
```

只替换当前的两行收尾，保留 hz 和定理 statement。预期作用是给零元/映射应用明确类型，
不是增加新公理或改变 injectivity 的含义。此片段本轮未编译。

### C. 第 70–71 行：显式指定泛型参数与 coercion 目标

只有在真实诊断定位到 wrapper 推断时，可试：

```lean
  have hDD' : Function.Injective M_DD.toLinearMap := by
    intro x y hxy
    exact M_DD.injective hxy
  exact zero_C_forces_zero_rhs
    (K := K) (D := Vec3 K) (C := Vec3 K)
    M_DD.toLinearMap M_DC M_CD M_CC
    alpha_D alpha_C R_C R_D hDD' hD hC hRD hAC
```

若实际错误在 hD 的 map application coercion，可另外用与目标行方程相同的显式类型
建立 `hD'`，在其 proof 中 `change` 到原 hD 的形状并 `exact hD`。
这只适用于 coercion 两端确实 definitionally equal 的情形；若不相等，不能通过
假设一个新等式掩盖问题。上面的候选片段同样未经编译。

不建议提前批量重写五个定理、换 umbrella import、添加 classical、加强 scalar
假设或转用矩阵逆 API。一次只对真实首错做最小编辑，再对精确新字节产生新 receipt。

## 3. 待 GitHub pinned compile 的 receipt 字段

以下是待填字段，不是本轮已有证明。未执行者一律 missing/pending，不填 true 或虚构 URL。

| 字段组 | 最小应记录内容 |
|---|---|
| 候选身份 | repo URL、包含候选的完整 commit、实际 checkout SHA、路径、原始文件 SHA-256；如修复则附 before/after SHA 与精确 diff |
| 固定环境 | lean-toolchain 原文与 SHA、实际 `lean --version`、确切 Mathlib commit、lake-manifest SHA、全部解析依赖 pins、使用的 cache/build 来源及匹配情况 |
| 执行身份 | GitHub run URL/id/attempt、job 名称、workflow 路径和定义 revision、runner/container 标识、UTC 时间、实际 cwd 与命令/参数 |
| 编译产物 | 对这个候选的实际检查命令、退出码、完整 stdout/stderr artifact URL 与 SHA、生成时的 .olean 路径与 SHA（若产出）、警告与错误情况 |
| 定理审计 | 下列五个完整名称逐项 `#check` / `#print axioms` 的实际输出、审计命令退出码、审计 driver 的内容/hash、输出 artifact/hash |
| admission 边界 | parsed/elaborated/kernel_checked/axioms_checked 按实际结果分别记；abstract_interface_checked 与 physical_source_bound 分开；registry_promoted=false，closure=false，禁止自动注册 |

目标五个完整名称：

```text
Q6GraphExclusionCandidate.zero_C_forces_zero_D
Q6GraphExclusionCandidate.zero_C_forces_zero_rhs
Q6GraphExclusionCandidate.nonzero_rhs_forces_nonzero_C
Q6GraphExclusionCandidate.fin3_zero_C_forces_zero_rhs
Q6GraphExclusionCandidate.fin3_nonzero_rhs_forces_nonzero_C
```

不得仅凭 GitHub overall green 判定这五项已检查：job 必须没有跳过候选，必须检查
预期源码哈希，不能只复用别的版本 .olean。审计输出须没有 `sorryAx` 或未批准的
自定义公理；允许的基础公理集合由采用的 admission policy 明确，不能把本轮预期当实测。
如果编译失败，保存第一个实际 diagnostic 和完整日志；保持 pending。
如果 repair 改变 statement/假设而非仅 elaboration，须返回数学复审，不能只靠编译接受。

即使后续 pinned compile 全通过，也只说明这五个抽象块方程引理在记录环境下通过检查。
Q6 物理 graph exclusion 仍需同源 block maps/projections、两行真实方程、R_D=0、
同一个 M_DD 的 injectivity/invertibility 与 R_C 非零绑定。结论只是 C 向量非零，
不是每个坐标非零、正的统一 norm floor、轨迹存在性或 P4/P5 closure。

## 4. 本轮 disposition

STATIC_REVIEW_ONLY / OPEN_UNCOMPILED / pending。候选和原 REVIEW 保持原样；
无本地 Lean/Lake、无 GitHub dispatch、无 state/registry/shared-script 修改。
