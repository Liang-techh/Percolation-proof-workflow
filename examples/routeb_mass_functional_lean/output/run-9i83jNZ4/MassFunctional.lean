import Mathlib

set_option autoImplicit false

namespace RouteBMassFunctional

noncomputable section

abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Mat (m n : ℕ) := Fin m → Fin n → ℝ

/-- The weighted Gram contribution of a Jacobian with row index `r`.

    The weight matrix is intentionally left arbitrary.  This covers the
    translational mass term (a scalar weight) and the body-frame/world-frame
    rotational inertia term without hiding either one behind a source axiom.
    The source adapter only has to prove equality of the concrete Jacobian
    rows and weights.
-/
def weightedGram {r n : ℕ} (J : Mat r n) (W : Mat r r) : Mat n n :=
  fun i j => ∑ a : Fin r, ∑ b : Fin r, J a i * W a b * J b j

def linkMass (Jv Jw : Mat 3 6) (mass : ℝ) (inertia : Mat 3 3) : Mat 6 6 :=
  fun i j =>
    mass * (∑ a : Fin 3, Jv a i * Jv a j) + weightedGram Jw inertia i j

def massFromLinks
    (mass : Fin 6 → ℝ)
    (Jv Jw : Fin 6 → Mat 3 6)
    (inertia : Fin 6 → Mat 3 3) : Mat 6 6 :=
  fun i j => ∑ k : Fin 6, linkMass (Jv k) (Jw k) (mass k) (inertia k) i j

def addDiagonal (eps : ℝ) (M : Mat 6 6) : Mat 6 6 :=
  fun i j => M i j + if i = j then eps else 0

theorem weightedGram_congruent {r n : ℕ}
    (J J' : Mat r n) (W W' : Mat r r)
    (hJ : ∀ a i, J a i = J' a i)
    (hW : ∀ a b, W a b = W' a b) :
    weightedGram J W = weightedGram J' W' := by
  funext i j
  simp only [weightedGram]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  rw [hJ a i, hW a b, hJ b j]

theorem linkMass_congruent
    (Jv Jv' Jw Jw' : Mat 3 6) (mass mass' : ℝ)
    (inertia inertia' : Mat 3 3)
    (hmass : mass = mass')
    (hJv : ∀ a i, Jv a i = Jv' a i)
    (hJw : ∀ a i, Jw a i = Jw' a i)
    (hI : ∀ a b, inertia a b = inertia' a b) :
    linkMass Jv Jw mass inertia = linkMass Jv' Jw' mass' inertia' := by
  funext i j
  simp only [linkMass]
  rw [hmass]
  have hsum :
      (∑ a : Fin 3, Jv a i * Jv a j) =
        ∑ a : Fin 3, Jv' a i * Jv' a j := by
    apply Finset.sum_congr rfl
    intro a ha
    rw [hJv a i, hJv a j]
  rw [hsum]
  exact congrFun (congrFun (weightedGram_congruent Jw Jw' inertia inertia'
      hJw hI) i) j

theorem massFromLinks_congruent
    (mass mass' : Fin 6 → ℝ)
    (Jv Jv' Jw Jw' : Fin 6 → Mat 3 6)
    (inertia inertia' : Fin 6 → Mat 3 3)
    (hmass : ∀ k, mass k = mass' k)
    (hJv : ∀ k a i, Jv k a i = Jv' k a i)
    (hJw : ∀ k a i, Jw k a i = Jw' k a i)
    (hI : ∀ k a b, inertia k a b = inertia' k a b) :
    massFromLinks mass Jv Jw inertia =
      massFromLinks mass' Jv' Jw' inertia' := by
  funext i j
  apply Finset.sum_congr rfl
  intro k hk
  exact congrFun (congrFun (linkMass_congruent
    (Jv k) (Jv' k) (Jw k) (Jw' k) (mass k) (mass' k)
    (inertia k) (inertia' k) (hmass k)
    (hJv k) (hJw k) (hI k)) i) j

/-- A source-independent functional adapter for the full Route-B mass.

    Once the deployed DH/Jacobian source proves the three pointwise equalities
    in `massFromLinks_congruent`, the whole six-link ideal mass equality is a
    kernel-level consequence.  No CSV reader, floating-point claim, or source
    identity is smuggled into this theorem.
-/
theorem ideal_mass_eq_fourier_of_linkwise
    (idealMass fourierMass : Vec 6 → Mat 6 6)
    (q : Vec 6)
    (mass mass' : Fin 6 → ℝ)
    (Jv Jv' Jw Jw' : Fin 6 → Mat 3 6)
    (inertia inertia' : Fin 6 → Mat 3 3)
    (hideal : idealMass q = massFromLinks mass Jv Jw inertia)
    (hfourier : fourierMass q = massFromLinks mass' Jv' Jw' inertia')
    (hmass : ∀ k, mass k = mass' k)
    (hJv : ∀ k a i, Jv k a i = Jv' k a i)
    (hJw : ∀ k a i, Jw k a i = Jw' k a i)
    (hI : ∀ k a b, inertia k a b = inertia' k a b) :
    idealMass q = fourierMass q := by
  rw [hideal, hfourier]
  exact massFromLinks_congruent mass mass' Jv Jv' Jw Jw' inertia inertia'
    hmass hJv hJw hI

theorem regularized_mass_eq_fourier
    (idealMass fourierMass : Vec 6 → Mat 6 6)
    (q : Vec 6)
    (h : idealMass q = fourierMass q) :
    addDiagonal (1 / 1000000 : ℝ) (idealMass q) =
      addDiagonal (1 / 1000000 : ℝ) (fourierMass q) := by
  rw [h]

theorem regularizer_entry
    (eps : ℝ) (M : Mat 6 6) (i j : Fin 6) :
    addDiagonal eps M i j - M i j = if i = j then eps else 0 := by
  simp [addDiagonal]

end
end RouteBMassFunctional

#print axioms RouteBMassFunctional.weightedGram_congruent
#print axioms RouteBMassFunctional.linkMass_congruent
#print axioms RouteBMassFunctional.massFromLinks_congruent
#print axioms RouteBMassFunctional.ideal_mass_eq_fourier_of_linkwise
#print axioms RouteBMassFunctional.regularized_mass_eq_fourier
