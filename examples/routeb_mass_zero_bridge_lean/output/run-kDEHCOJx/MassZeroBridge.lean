import Mathlib

set_option autoImplicit false

namespace RouteBMassZeroBridge

noncomputable section

abbrev Mat (n : ℕ) := Fin n → Fin n → ℝ

/-- The exact q=0 aggregate of all 610 real Fourier rows.

    This is a frozen finite certificate payload.  It is deliberately not a
    file reader: the external provenance checker independently re-aggregates
    the CSV bytes and checks that they produce these 36 rationals. -/
def csvQ0Mass : Mat 6 := ![
  ![4711/6000, -1481/80000, -103/16000, 7/60, -21/80000, 1/60],
  ![-1481/80000, 1397297/2400000, 677771/2400000, 0, 41827/800000, 0],
  ![-103/16000, 677771/2400000, 612881/2400000, 0, 8189/160000, 0],
  ![7/60, 0, 0, 7/60, 0, 1/60],
  ![-21/80000, 41827/800000, 8189/160000, 0, 40147/800000, 0],
  ![1/60, 0, 0, 1/60, 0, 1/60]
]

/-- The literal reference matrix used by the existing Route-B energy leaf. -/
def M0 : Mat 6 := ![
  ![2355503/3000000, -1481/80000, -103/16000, 7/60, -21/80000, 1/60],
  ![-1481/80000, 6986497/12000000, 677771/2400000, 0, 41827/800000, 0],
  ![-103/16000, 677771/2400000, 3064417/12000000, 0, 8189/160000, 0],
  ![7/60, 0, 0, 350003/3000000, 0, 1/60],
  ![-21/80000, 41827/800000, 8189/160000, 0, 200739/4000000, 0],
  ![1/60, 0, 0, 1/60, 0, 50003/3000000]
]

def addMassRegularizer (M : Mat 6) : Mat 6 :=
  fun i j => M i j + if i = j then (1 / 1000000 : ℝ) else 0

/-- The 610-row Fourier mass table, evaluated at q=0, plus the exact intended
    real regularizer, is exactly the Lean literal M0. -/
theorem csv_q0_plus_regularizer_eq_M0 :
    addMassRegularizer csvQ0Mass = M0 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [addMassRegularizer, csvQ0Mass, M0]

/-- Entrywise form used by downstream source adapters. -/
theorem csv_q0_entry_plus_regularizer (i j : Fin 6) :
    csvQ0Mass i j + if i = j then (1 / 1000000 : ℝ) else 0 = M0 i j := by
  have h := congrFun (congrFun csv_q0_plus_regularizer_eq_M0 i) j
  exact h

end
end RouteBMassZeroBridge

#print axioms RouteBMassZeroBridge.csv_q0_plus_regularizer_eq_M0
#print axioms RouteBMassZeroBridge.csv_q0_entry_plus_regularizer
