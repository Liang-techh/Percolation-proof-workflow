# Claim — T-P4-040-RATIONAL-LAMBDA-GUARD

- agent: 狂蛮魔尊
- source_agent: 狂蛮魔尊
- status: self_claimed
- parent: T-P4-039 common-lambda interval feasibility
- scope: robust rational interval / implementation-rounding guard for one common fixed `lambda` across all rows
- non_overlap: does **not** touch DHProducerBaseBridge/source receipt/provenance/admission/coverage; does not redo T-P4-039 pairwise exact feasibility

## Goal

Convert the existence-level common-`lambda` condition into a small exact-rational certificate that remains valid under implementation rounding and conservative coefficient/source envelopes.

Work in `s = lambda - 1 > 0`.  For each row use

`q_i(s) = P_i s^2 - G_i s + A_i`.

Main target: certify a whole rational interval `[s_lo,s_hi]`, rather than one isolated witness, by endpoint inequalities only; then add a monotone coefficient-envelope version suitable for source/checker widening.
