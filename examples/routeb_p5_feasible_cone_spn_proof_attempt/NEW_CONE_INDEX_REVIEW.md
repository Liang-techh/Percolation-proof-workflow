# P5-026 ConeIndex / 36-to-18：保留索引重数的最小接口

日期：2026-09-07。

结果：新增独立 Lean 文件已在本机 Lean 4.32.0 检查通过（exit 0），16 项公开接口
的 `#print axioms` 输出均为 `[propext, Classical.choice, Quot.sound]`，无 `sorryAx`。
这项证据仅适用于下列新增文件；不升级旧 P5 proof attempt、旧 sidecar 或 registry 状态。

本任务仅新增同目录三个文件：

- `NEW_CONE_INDEX_Core.lean`：具体索引、反号、代表选择、求和与覆盖见证等价。
- `NEW_CONE_INDEX_check.py`：只读有限精确检查和边界探针，报告仅写 stdout。
- `NEW_CONE_INDEX_REVIEW.md`：本 review。

未修改既有 P5 files、state、registry、K_path/source artifacts、Lake 配置或原 review；
未提交、注册或触发 CI。执行期间工作树出现其他路径的并发改动，本任务未修改或回退这些改动。

## 阅读依据与类型边界

已阅读同目录 `P5FeasibleConeSPN.lean`、`NEW_exact_geometry_spn.py`、
`REVIEW_exact_geometry_spn.md`，以及仓库 `agent_review_inbox/` 中：

- `review-T-P5-026-guyuefangyuan-20260907T1031.md`：六个闭锥、全局反号与 SPN 数学接口。
- `review-T-P5-026-juyangxianzun-20260907T1048.md`：已报告的通用 sidecar，以及仍开放的具体 ConeIndex/代表表。

同时检查了 `examples/routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean` 的现有通用接口。
本次不复核旧 review 所引用的远端运行结果。

新增 namespace 为 `RouteBP5ConeIndex`。其六锥枚举与 `cx/cy/reverse` 表独立定义，
不导入尚未在本轮验证的旧 `P5FeasibleConeSPN` 文件。
Python 只对照核验六锥公式、反号、代表顺序、36 个选择结果及交错坐标的受限文本；
这不是两个 Lean namespace 之间的 typed adapter。新文件自身的证明由 Lean 实际检查。

## 具体索引与代表选择

```text
Cone = pp | nn | pnPos | pnNeg | npPos | npNeg
ConeIndex = Cone × Cone                         card = 36
Representative = Fin 3 × Cone                  card = 18
representativeFirst = [pp, pnPos, pnNeg]
flip(c4,c5) = (reverse c4, reverse c5)
indexEquiv : ConeIndex ≃ Representative × Bool
```

`false` 表示代表自身；`true` 表示两个通道同时反号。代表首分量是 `Fin 3` 编号，
与旧 Python `REPS` 使用的原六锥编号 `(0,2,3)` 有明确区别：
`representative_cone((rank,c5)) = ((0,2,3)[rank],c5)`。

| 第一通道 | 所选代表首编号 | 所选代表第二通道 | Bool |
|---|---:|---|---|
| pp | 0 | c5 | false |
| nn | 0 | reverse c5 | true |
| pnPos | 1 | c5 | false |
| pnNeg | 2 | c5 | false |
| npPos | 2 | reverse c5 | true |
| npNeg | 1 | reverse c5 | true |

实际证明了：

- `flip_flip`、`flip_ne`：无不动点的 involution。
- `expand_select`、`select_expand`：双向逆，给出可计算 `indexEquiv`。
- `unique_signed_representative`：每个索引恰好对应一个 `(代表,Bool)`。
- `select_flip`：反号保留代表、切换 Bool。
- `same_representative_iff`：代表相同当且仅当两个索引相同或互为全局反号。
- `representative_fiber`、`representative_fiber_card`：每个代表纤维恰有两个索引。

这些是有限标签的定理，不依赖 K、mu、P、矩阵相异性或数值检查。

## multiplicity-preserving cover 的含义

对任意交换加法幺半群中的权重 `w`，`sum_preserving_multiplicity` 证明

```text
sum[c : ConeIndex] w(c)
  = sum[r : Representative] (w(rep(r)) + w(flip(rep(r)))).
```

该式无需反号不变性。若另外提供 `w(flip c)=w(c)`，`sum_invariant` 才将右侧写为
`sum[r] 2 • w(rep(r))`。具体对象或矩阵即使全部相同，索引重数仍然保留。
使用 `Finset.image` 按矩阵值去重不满足这个接口。

`witnessEquiv` 对任意参数类型 `U`、任意关系 `ok : ConeIndex → U → Prop` 给出

```text
{(c,u) | ok(c,u)}
  ≃ {(r,b,u) | ok(expand(r,b),u)}.
```

映射只重编号 `c`，完整保留同一个 `u`；不假设状态所在锥唯一。
这比只给出某一个覆盖见证更强，适用于闭锥边界的多重归属。

具体几何固定状态顺序 `(x4,x5,y4,y5)`、参数顺序 `(a4,a5,b4,b5)`。
`channel_cover`、`cone_cover` 证明六锥和乘积锥覆盖所有实数状态；
`chart_flip` 证明 `chart(flip c,u) = -chart(c,u)`；
`signed_representative_cover` 将覆盖重编号到 18 个代表和两个方向。
`coverWitnessEquiv` 是上述关系等价在 `u≥0 ∧ chart(c,u)=z` 上的具体实例。

`cover_multiplicity` 将每个状态的逐索引 membership 指示函数求和保留下来。
`origin_multiplicity` 精确证明原点覆盖重数为 **36**。因此“18 代表”不表示
18 个不交区域，也不表示直接丢掉反号方向后仍覆盖原来的全部状态。

## 后续消费者需要提供的最小前提

`forall_representatives_iff`：若 `p(flip c) ↔ p(c)`，则全部 36 个索引满足 `p`
等价于全部 18 个代表满足 `p`。

`liftFamily value Cert hflip cert`：若外部提供

```text
value : ConeIndex → A
hflip : forall c, value(flip c) = value(c)
cert : forall r, Cert(value(rep(r)))
```

即可构造 `forall c, Cert(value(c))`，允许 `Cert` 为数据类型。
未来可取 `value = H K mu`、`Cert = SPNCertificate`，但必须先完成相应 typed binding
并提供真正的 `H_flip` 等式。本文件没有将该等式、18 份 SPN 证书或 concrete K_path
作为已建立事实，也未实例化上述外部消费者。

## 实际验证与复现

Lean：直接使用已有 `v4.32.0` 可执行文件与本地缓存；Mathlib 源 checkout 的 HEAD
为 `81a5d257c8e410db227a6665ed08f64fea08e997`，与既有 manifest 的固定值一致。
使用已有依赖构建产物，无 `lake update/build`、无安装、无新增 `.olean` 或日志文件。
最终 Lean exit 0，无错误或警告；16 项公理审计无 `sorryAx` 或额外公理。
这是对本地缓存环境下新增文件的直接验证，未重建或独立审计全部 Mathlib 缓存。

Python 普通模式与 `-O` 模式均 exit 0。检查包括 36 个左逆、36 个右逆、1296 对轨道关系、
18 个大小为 2 的纤维、任意索引权重的全部 36 个形式系数相等。
另用每通道 13 个 strata 代表做 169 个精确有理边界探针；覆盖重数直方图为
`{1:36, 2:72, 4:36, 6:12, 12:12, 36:1}`，见证重编号前后逐项相同。
这些探针是诊断验证，普遍实数覆盖由 Lean 定理提供。

11 个负控均拒绝：缺方向、重复索引、只反转一个通道、布尔锥编号、负编号、
超界代表、非 Bool 方向、原点丢方向、按相同对象值去重、错误 Lean 代表分支、错误锥公式。
失败仅表示本有限接口检查未通过，不是 copositivity 的反例。

从仓库根目录执行，所有输出仅到 stdout：

```powershell
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_check.py --self-test
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_check.py --self-test

$taskLeanPaths = Get-ChildItem -LiteralPath examples/local_fkg/.lake/packages -Directory |
  ForEach-Object { Join-Path $_.FullName '.lake/build/lib/lean' } |
  Where-Object { Test-Path -LiteralPath $_ }
$env:LEAN_PATH = $taskLeanPaths -join ';'
& C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_Core.lean
```

最终检查对象 SHA-256：

```text
NEW_CONE_INDEX_Core.lean
b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602
NEW_CONE_INDEX_check.py
9c2ec032f03ac12d67471de297cf13d30c0c9bc8f141a8271720669e400667e5
```

原输入字节哈希在检查前后保持一致，checker 在只读加载前锁定这两个哈希：

```text
P5FeasibleConeSPN.lean
fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824
NEW_exact_geometry_spn.py
263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42
```

## 未闭合边界

没有 concrete K_path、source/Jacobian 域绑定、18 份实际 SPN 证书、IEEE/controller
缺陷或 anchor bias 处理、P8 覆盖、ODE continuation、P5/P8/M4 closure 或 registry admission。
新 Lean 的 source-independent 索引与几何定理通过本地检查，不改变这些边界。
Python 报告的 `kernel_verified_by_this_checker=false` 专指 Python 检查器不执行 Lean，
与上面另行执行并记录的 Lean 验证不冲突。所有 admission/closure 标记继续为 false。
