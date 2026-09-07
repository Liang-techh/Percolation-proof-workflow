import Mathlib

set_option autoImplicit false

namespace RouteBB45ResidualDecomposition

noncomputable section

abbrev Vec2 := ℝ × ℝ

def vadd (x y : Vec2) : Vec2 := (x.1 + y.1, x.2 + y.2)

def vsub (x y : Vec2) : Vec2 := (x.1 - y.1, x.2 - y.2)

def pmiForce (q v : Vec2) (w : ℝ) : Vec2 :=
  ( -(3 / 5 : ℝ) * q.1 - (4 / 5 : ℝ) * v.1
      - (3 / 20 : ℝ) * q.1 + (1 / 100 : ℝ) * q.2
      + (1 / 5 : ℝ) * w,
    -(1 / 2 : ℝ) * q.2 - (13 / 20 : ℝ) * v.2
      - (2 / 25 : ℝ) * q.2 + (1 / 200 : ℝ) * q.1
      + (1 / 10 : ℝ) * w )

def sourceForce (q v : Vec2) (w : ℝ) (c g g0 : Vec2) : Vec2 :=
  ( -(3 / 5 : ℝ) * q.1 - (4 / 5 : ℝ) * v.1 + (1 / 5 : ℝ) * w
      + g0.1 - c.1 - g.1,
    -(1 / 2 : ℝ) * q.2 - (13 / 20 : ℝ) * v.2 + (1 / 10 : ℝ) * w
      + g0.2 - c.2 - g.2 )

def blockResidual (q v : Vec2) (w : ℝ) (aB : Vec2) : Vec2 :=
  vsub (pmiForce q v w) ((1 / 5 : ℝ) * aB.1, (1 / 10 : ℝ) * aB.2)

def rhoC (c : Vec2) : Vec2 := c

def rhoG (g g0 : Vec2) : Vec2 := (g.1 - g0.1, g.2 - g0.2)

def rhoMgl (q : Vec2) : Vec2 :=
  ( -(3 / 20 : ℝ) * q.1, -(2 / 25 : ℝ) * q.2 )

def rhoKc (q : Vec2) : Vec2 :=
  ( q.2 / 100, q.1 / 200 )

/- The canonical PMI source writes the cross term in normalized f coordinates
   and restores force coordinates by multiplying the two block equations by
   I4=1/5 and I5=1/10.  This is a coordinate adapter only. -/
def rhoKcNormalized (q : Vec2) : Vec2 :=
  (q.2 / 20, q.1 / 20)

def forceScaleKc (q : Vec2) : Vec2 :=
  ((1 / 5 : ℝ) * (rhoKcNormalized q).1,
    (1 / 10 : ℝ) * (rhoKcNormalized q).2)

theorem forceScaleKc_eq_rhoKc (q : Vec2) :
    forceScaleKc q = rhoKc q := by
  rcases q with ⟨q4, q5⟩
  apply Prod.ext <;>
    dsimp [forceScaleKc, rhoKcNormalized, rhoKc] <;>
    ring

def rhoKcSq (q : Vec2) : ℝ :=
  (rhoKc q).1 ^ 2 + (rhoKc q).2 ^ 2

theorem rhoKc_sq_le_of_block_energy
    (q : Vec2)
    (hp : (3 / 2 : ℝ) * (q.1 ^ 2 + q.2 ^ 2) ≤ 28 / 5) :
    rhoKcSq q ≤ 7 / 18750 := by
  rcases q with ⟨q4, q5⟩
  dsimp [rhoKcSq, rhoKc]
  nlinarith [sq_nonneg q4, sq_nonneg q5]

def rhoMass (massBB : Vec2 → Vec2) (aB : Vec2) : Vec2 :=
  ( (massBB aB).1 - (1 / 5 : ℝ) * aB.1,
    (massBB aB).2 - (1 / 10 : ℝ) * aB.2 )

def rhoRemote (remote : Vec2) : Vec2 := remote

theorem rhoKc_exact (q : Vec2) :
    rhoKc q = (q.2 / 100, q.1 / 200) := by
  rfl

theorem residual_decomposition
    (q v : Vec2) (w : ℝ) (c g g0 : Vec2)
    (massBB : Vec2 → Vec2) (aB remote : Vec2)
    (hdesc : sourceForce q v w c g g0 = vadd (massBB aB) remote) :
    blockResidual q v w aB =
      vadd (rhoC c)
        (vadd (rhoG g g0)
          (vadd (rhoMgl q)
            (vadd (rhoKc q)
              (vadd (rhoMass massBB aB) (rhoRemote remote))))) := by
  rcases q with ⟨q4, q5⟩
  rcases v with ⟨v4, v5⟩
  rcases c with ⟨c4, c5⟩
  rcases g with ⟨g4, g5⟩
  rcases g0 with ⟨g04, g05⟩
  rcases aB with ⟨a4, a5⟩
  rcases remote with ⟨r4, r5⟩
  rcases massBB (a4, a5) with ⟨m4, m5⟩
  apply Prod.ext <;> dsimp [blockResidual, pmiForce, vsub, vadd,
    rhoC, rhoG, rhoMgl, rhoKc, rhoMass, rhoRemote, sourceForce] at hdesc ⊢
  · linarith [congrArg Prod.fst hdesc]
  · linarith [congrArg Prod.snd hdesc]

theorem residual_decomposition_with_explicit_kc
    (q v : Vec2) (w : ℝ) (c g g0 : Vec2)
    (massBB : Vec2 → Vec2) (aB remote : Vec2)
    (hdesc : sourceForce q v w c g g0 = vadd (massBB aB) remote) :
    blockResidual q v w aB =
      vadd (rhoC c)
        (vadd (rhoG g g0)
          (vadd (rhoMgl q)
            (vadd (q.2 / 100, q.1 / 200)
              (vadd (rhoMass massBB aB) (rhoRemote remote))))) := by
  simpa [rhoKc] using residual_decomposition q v w c g g0 massBB aB remote hdesc

#print axioms rhoKc_exact
#print axioms forceScaleKc_eq_rhoKc
#print axioms rhoKc_sq_le_of_block_energy
#print axioms residual_decomposition
#print axioms residual_decomposition_with_explicit_kc

end
end RouteBB45ResidualDecomposition
