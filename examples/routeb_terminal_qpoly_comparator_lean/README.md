# F4 direct qpoly terminal comparator

This is an independent exact-arithmetic Lean leaf for Route-B F4.  It proves
the direct terminal interface

```text
qpoly(1) <= (3/2) * L + 3 * g * D
```

and, under `D <= D_gate` with `D_gate = 4483/2000`, proves the strict target
`qpoly(1) < 12`.

The pinned exact constants are:

```text
L = 741313139497426595085940983587251157 /
    140000000000000000000000000000000000
g = 1544607345405575083521649488080013 /
    2560000000000000000000000000000000
D_gate = 4483/2000
```

The equality threshold is

```text
D_max = 3029494884020587239312472131301990744 /
        1351531427229878198081443302070011375
```

and `D_max - D_gate` is

```text
595038157044133006671515392963951 /
21624502835678051169303092833120182000 > 0.
```

At the gate, the exact strict margin is

```text
12 - ((3/2)L + 3*g*D_gate) =
1785114471132399020014546178891853 /
35840000000000000000000000000000000 > 0.
```

This leaf deliberately has no `p <= 28/5` premise or proof path.  That bound
only gives `qpoly <= 14` in the coefficient comparison and cannot discharge
the terminal target `12`.

Boundary: this is conditional arithmetic and comparator infrastructure only.
The deployed Route-B DH/FD/Float64 trajectory proof that the actual full
residual satisfies `D <= D_gate` remains **OPEN**.  No registry promotion or
formal deployed-DH certificate is claimed here.

Run the focused strict check with `bash verify.sh` (from WSL/Ubuntu).
