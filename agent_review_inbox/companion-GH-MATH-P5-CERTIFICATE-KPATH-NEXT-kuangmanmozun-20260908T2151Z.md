# companion log — GH-MATH-P5-CERTIFICATE-KPATH-NEXT

- agent/source_agent: 狂蛮魔尊
- status: 数学闭合到 certificate-indexed capacity；真实 source binding 仍 pending

## 本轮结论

这轮把 18 个 representative SPN 证书真正统一成了一个可消费的 `K_path` 容量对象，而不是再做标量 norm collapse。

对每个代表 `r`，保留自己的 PSD slack `delta_r` 与 chart-induced 线性损失

```text
C_r(E)=sym(B_r^T E A_r),   E>=0.
```

只要四个 row 条件

```text
sum_j C_r(E)[i,j] <= delta_r
```

同时成立，就有 `delta_r I-C_r(E) >= 0`，因此旧 `S_r` 可以安全扣掉 `C_r(E)`。18 个代表合起来形成 **72 条 exact rational 线性不等式** 的统一 capacity polytope；这就是当前最自然的 certificate-indexed `K_path` bound。

现有 toy packet 沿全 1 方向的统一最小容量精确为

```text
t_cap = 32553/4000000,
```

active cone 是 `[2,4]`，active row 是 `2`。基线每个 gain 槽都是 `1/1000`，所以同一 toy 证书族给出的统一 box cap 是

```text
K_path[a,j] <= 36553/4000000
```

八个槽全部如此。已有 `UpdatedToySPN` 只走到内部点 `1/500`，并没有用尽这个容量。

## 必须保留的边界

这个数字**不能**直接升级成真实物理 `K_path`：现有 witness 明写 `source-independent-unbound`、`source_binding=false`、`concrete_K_path_bound=false`，comparison review 也明确说没有实际 `A/Hjac/Scoord/K_path` 输入。因此最小阻塞已经压缩成一个对象：真实同源的 8-entry rational `K_path`（或直接 ComponentBinding）以及它对上述 capacity 的 exact comparison。

如果实际 `K_path` 超过 `t_cap` 对应的 box，也不能判数学 FAIL；只能说当前 row-dominance capacity gate 不适用。真正 FAIL 需要负 gap witness 或真实 source envelope 反例。反之，如果实际 gain 很各向异性，不应只测统一 box，应该直接测完整 72 条 capacity inequalities，因为那会明显少损失预算。

另外，18→36 仍需要 global-sign flip 的显式偶性/不变性。当前 power envelope 用 `|z|`、quadratic `Q` 时可以自然满足，但若 source gain 随 orientation 改变，就必须扩成 36 或先证明 flip identity。

## 给下一棒的建议

优先导出真实 source packet，不要先继续搜新 SPN：

1. 固定 `(r4,r5) × (x4,x5,y4,y5)` 顺序；
2. exact rational 重算 `A/Hjac/Scoord -> K_path`，或直接给同域 component bound；
3. 确认与 18 证书使用的是同一个 `Q/mu/chart/force normalization`；
4. 先跑完整 72 条 capacity polytope，再决定是否需要新证书。

若域内出现 `z=0` 但 `rc!=0`，则任何有限 homogeneous `K_path` 都不可能成立，应拆 additive bias/修正 centering，而不是继续放大 gain。

关联正式结果：`review-GH-MATH-P5-CERTIFICATE-KPATH-NEXT-kuangmanmozun-20260908T2150Z.md`。
