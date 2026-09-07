import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic

/-!
  Route-B P7: exact rational scalar tail bound.

  The constants below are the exact rational values emitted by the independent
  physical tail checker.  This child proves only the final scalar arithmetic
  inequalities.  It does not prove that the Julia Float64 trajectory satisfies
  the polynomial model, nor does it provide P5/P8 coverage or M4 closure.
-/

set_option autoImplicit false

namespace RouteBP7Tail

abbrev R := ℚ

def eta (inv00 inv01 inv11 u1 u2 rho : R) : R :=
  (inv00 * u1 ^ 2 + 2 * |inv01| * u1 * u2 + inv11 * u2 ^ 2) / rho

def target : R := 1 / 160000

def rho0 : R :=
  10616159325566083327957 / 39062500000000000000000

def inv00 : R :=
  5974375000000000000000000000000000000000000000000000000000000 /
    697016391041668658124999999999998884107304567072387444785259

def inv01 : R :=
  -364478214031950000000000000000000000000000000000 /
    697016391041668658124999999999998884107304567072387444785259

def inv11 : R :=
  291669166666667500000000000000000000000000000000000000000000000 /
    14637344211875041820624999999999976566253395908520136340490439

def u1_eta01 : R := 4557183030309 / 62500000000000000
def u2_eta01 : R := 68513 / 500000000

def u1_eta02 : R := 6213654909 / 40960000000000
def u2_eta02 : R := 615204634373 / 2621440000000000

theorem rho0_pos : 0 < rho0 := by
  norm_num [rho0]

theorem eta01_lt_target :
    eta inv00 inv01 inv11 u1_eta01 u2_eta01 rho0 < target := by
  norm_num [eta, inv00, inv01, inv11, u1_eta01, u2_eta01, rho0, target]

theorem eta02_lt_target :
    eta inv00 inv01 inv11 u1_eta02 u2_eta02 rho0 < target := by
  norm_num [eta, inv00, inv01, inv11, u1_eta02, u2_eta02, rho0, target]

#print axioms rho0_pos
#print axioms eta01_lt_target
#print axioms eta02_lt_target

end RouteBP7Tail
