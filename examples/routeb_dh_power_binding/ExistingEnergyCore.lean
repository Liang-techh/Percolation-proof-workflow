import Mathlib

open scoped BigOperators

namespace RobotFormalEnergy

/- Schur PMI interface for a residual vector.  The block matrix
   [[beta, lᵀ], [l, I]] is positive semidefinite whenever the scalar Schur
   complement beta - ||l||² is nonnegative.  This preserves direction
   correlation and is the exact finite-dimensional form used by the residual
   matrix certificates. -/
theorem schur_pmi_quadratic_nonneg
    {ι : Type*} [Fintype ι]
    (beta x0 : ℝ) (l x : ι → ℝ)
    (hbeta : (∑ i, l i ^ 2) ≤ beta) :
    0 ≤ beta * x0 ^ 2 +
      2 * x0 * (∑ i, l i * x i) +
      ∑ i, x i ^ 2 := by
  classical
  have hsquare :
      (∑ i, (x i + l i * x0) ^ 2) =
        (∑ i, x i ^ 2) +
          2 * x0 * (∑ i, l i * x i) +
            x0 ^ 2 * (∑ i, l i ^ 2) := by
    calc
      (∑ i, (x i + l i * x0) ^ 2) =
          ∑ i, (x i ^ 2 + 2 * x0 * (l i * x i) + x0 ^ 2 * l i ^ 2) := by
            apply Finset.sum_congr rfl
            intro i hi
            ring
      _ = (∑ i, x i ^ 2) +
            (∑ i, 2 * x0 * (l i * x i)) +
              (∑ i, x0 ^ 2 * l i ^ 2) := by
            rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      _ = (∑ i, x i ^ 2) +
            2 * x0 * (∑ i, l i * x i) +
              x0 ^ 2 * (∑ i, l i ^ 2) := by
            rw [← Finset.mul_sum, ← Finset.mul_sum]
  have hsq : 0 ≤ ∑ i, (x i + l i * x0) ^ 2 := by
    exact Finset.sum_nonneg (fun i hi => sq_nonneg _)
  have hgap : 0 ≤ (beta - ∑ i, l i ^ 2) * x0 ^ 2 := by
    exact mul_nonneg (sub_nonneg.mpr hbeta) (sq_nonneg _)
  rw [hsquare] at hsq
  nlinarith

/- A scalar Young inequality in the exact form used by the pointwise ledger. -/
theorem young_term (d g v w : ℝ) (hd : 0 < d) :
    g * v * w ≤ d * v ^ 2 + (g ^ 2 / (4 * d)) * w ^ 2 := by
  have hden : 0 < 4 * d := by positivity
  have hsq : 0 ≤ (2 * d * v - g * w) ^ 2 := sq_nonneg _
  have hdiv : 0 ≤ (2 * d * v - g * w) ^ 2 / (4 * d) :=
    div_nonneg hsq (le_of_lt hden)
  have hid : (2 * d * v - g * w) ^ 2 / (4 * d) =
      d * v ^ 2 - g * v * w + (g ^ 2 / (4 * d)) * w ^ 2 := by
    field_simp [ne_of_gt hden]
    ring
  rw [hid] at hdiv
  nlinarith

/- Finite-dimensional diagonal version; no dynamics or floating-point facts
   are hidden in this lemma. -/
theorem diagonal_young (d g v : Fin 6 → ℝ) (w : ℝ)
    (hd : ∀ i, 0 < d i) :
    (∑ i, g i * v i * w) ≤
      (∑ i, d i * v i ^ 2) +
        (∑ i, (g i ^ 2 / (4 * d i))) * w ^ 2 := by
  calc
    (∑ i, g i * v i * w) ≤
        ∑ i, (d i * v i ^ 2 + (g i ^ 2 / (4 * d i)) * w ^ 2) := by
      exact Finset.sum_le_sum (fun i _ => young_term (d i) (g i) (v i) w (hd i))
    _ = (∑ i, d i * v i ^ 2) +
          (∑ i, (g i ^ 2 / (4 * d i))) * w ^ 2 := by
      rw [Finset.sum_add_distrib]
      rw [← Finset.sum_mul]

/- Dissipation allocation in the exact form used by the robust energy ledger.
   The vector `e` is the part of the physical damping spent on uncertainty. -/
theorem diagonal_dissipation_bound
    (d e g v : Fin 6 → ℝ) (w : ℝ)
    (_hd : ∀ i, 0 < d i) (he : ∀ i, 0 < e i) :
    -(∑ i, d i * v i ^ 2) + (∑ i, g i * v i * w) ≤
      -(∑ i, (d i - e i) * v i ^ 2) +
        (∑ i, (g i ^ 2 / (4 * e i))) * w ^ 2 := by
  have hy := diagonal_young e g v w he
  have hsplit :
      (∑ i, (d i - e i) * v i ^ 2) =
        (∑ i, d i * v i ^ 2) - (∑ i, e i * v i ^ 2) := by
    calc
      (∑ i, (d i - e i) * v i ^ 2) =
          ∑ i, (d i * v i ^ 2 - e i * v i ^ 2) := by
            apply Finset.sum_congr rfl
            intro i hi
            ring
      _ = (∑ i, d i * v i ^ 2) - (∑ i, e i * v i ^ 2) := by
            rw [Finset.sum_sub_distrib]
  rw [hsplit]
  nlinarith

/- Residual absorption interface.  Once the C/G power defects have been
   bounded by nonnegative scalars, this theorem inserts them into the same
   diagonal Young allocation used for the nominal closed loop. -/
theorem diagonal_dissipation_with_power_remainder
    (d e g v : Fin 6 → ℝ) (w rC rG defectC defectG : ℝ)
    (hd : ∀ i, 0 < d i) (he : ∀ i, 0 < e i)
    (hC : |rC| ≤ defectC) (hG : |rG| ≤ defectG) :
    -(∑ i, d i * v i ^ 2) + (∑ i, g i * v i * w) + rC + rG ≤
      -(∑ i, (d i - e i) * v i ^ 2) +
        (∑ i, (g i ^ 2 / (4 * e i))) * w ^ 2 + defectC + defectG := by
  have hnom := diagonal_dissipation_bound d e g v w hd he
  have hCr : rC ≤ defectC := le_trans (le_abs_self rC) hC
  have hGr : rG ≤ defectG := le_trans (le_abs_self rG) hG
  linarith

/- Six-row descriptor power cancellation.  No invertibility, truncation, or
   numerical approximation is used: substituting the descriptor equations
   turns kinetic-plus-potential power into actuator power. -/
theorem descriptor_power_identity
    (M C : Fin 6 → Fin 6 → ℝ) (v a tau G : Fin 6 → ℝ)
    (hdesc : ∀ i,
      (∑ j, M i j * a j) = tau i - (∑ j, C i j * v j) - G i) :
    (∑ i, v i * (∑ j, M i j * a j)) +
        (∑ i, v i * (∑ j, C i j * v j)) +
        (∑ i, v i * G i) =
      ∑ i, v i * tau i := by
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i hi
  rw [hdesc i]
  ring

/- Exact source-to-energy decomposition when the descriptor uses approximate
   Cfd/Gfd but the storage derivative uses analytic C/G.  The two residual
   terms are exposed explicitly, so later interval bounds can be attached
   without hiding them inside a numerical inequality. -/
theorem descriptor_power_remainder_identity
    (M C Cfd : Fin 6 → Fin 6 → ℝ) (v a tau G Gfd : Fin 6 → ℝ)
    (hdesc : ∀ i,
      (∑ j, M i j * a j) = tau i - (∑ j, Cfd i j * v j) - Gfd i) :
    (∑ i, v i * (∑ j, M i j * a j)) +
        (∑ i, v i * (∑ j, C i j * v j)) +
        (∑ i, v i * G i) =
      (∑ i, v i * tau i) +
        (∑ i, v i * (∑ j, (C i j - Cfd i j) * v j)) +
        (∑ i, v i * (G i - Gfd i)) := by
  calc
    (∑ i, v i * (∑ j, M i j * a j)) +
          (∑ i, v i * (∑ j, C i j * v j)) +
          (∑ i, v i * G i) =
        ∑ i, (v i * (∑ j, M i j * a j) +
          v i * (∑ j, C i j * v j) + v i * G i) := by
            rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
    _ = ∑ i, (v i * tau i +
          v i * (∑ j, (C i j - Cfd i j) * v j) +
          v i * (G i - Gfd i)) := by
            apply Finset.sum_congr rfl
            intro i hi
            rw [hdesc i]
            have hinner :
                (∑ j, (C i j - Cfd i j) * v j) =
                  (∑ j, C i j * v j) - (∑ j, Cfd i j * v j) := by
              calc
                (∑ j, (C i j - Cfd i j) * v j) =
                    ∑ j, (C i j * v j - Cfd i j * v j) := by
                      apply Finset.sum_congr rfl
                      intro j hj
                      ring
                _ = (∑ j, C i j * v j) - (∑ j, Cfd i j * v j) := by
                      rw [Finset.sum_sub_distrib]
            rw [hinner]
            ring
    _ = (∑ i, v i * tau i) +
          (∑ i, v i * (∑ j, (C i j - Cfd i j) * v j)) +
          (∑ i, v i * (G i - Gfd i)) := by
            rw [Finset.sum_add_distrib, Finset.sum_add_distrib]

/- Controller-power rewrite for the storage potential whose derivative is
   `(Kp*q-G0)'v`. -/
theorem closed_loop_power_identity
    (kp d g q v tau : Fin 6 → ℝ) (G0 : Fin 6 → ℝ) (w dUc : ℝ)
    (htau : ∀ i, tau i = -kp i * q i - d i * v i + G0 i + g i * w)
    (hUc : dUc = ∑ i, (kp i * q i - G0 i) * v i) :
    (∑ i, v i * tau i) + dUc =
      -(∑ i, d i * v i ^ 2) + (∑ i, g i * v i * w) := by
  rw [hUc]
  rw [← Finset.sum_add_distrib]
  have hsum :
      -(∑ i, d i * v i ^ 2) + (∑ i, g i * v i * w) =
        ∑ i, (-d i * v i ^ 2 + g i * v i * w) := by
    simp [Finset.sum_add_distrib]
  rw [hsum]
  apply Finset.sum_congr rfl
  intro i hi
  rw [htau i]
  ring

/- The complete residual-to-dissipation composition.  The descriptor uses
   Cfd/Gfd, while the storage derivative uses analytic C/G.  Once the two
   scalar power defects are bounded, the three previously separate interfaces
   compose without an inverse-mass or free-acceleration assumption. -/
theorem descriptor_closed_loop_dissipation_with_remainder
    (M C Cfd : Fin 6 → Fin 6 → ℝ) (v a tau G Gfd : Fin 6 → ℝ)
    (kp d g q G0 : Fin 6 → ℝ) (e : Fin 6 → ℝ)
    (w dUc rC rG defectC defectG : ℝ)
    (hd : ∀ i, 0 < d i) (he : ∀ i, 0 < e i)
    (hdesc : ∀ i,
      (∑ j, M i j * a j) = tau i - (∑ j, Cfd i j * v j) - Gfd i)
    (htau : ∀ i, tau i = -kp i * q i - d i * v i + G0 i + g i * w)
    (hUc : dUc = ∑ i, (kp i * q i - G0 i) * v i)
    (hrC : rC = ∑ i, v i * (∑ j, (C i j - Cfd i j) * v j))
    (hrG : rG = ∑ i, v i * (G i - Gfd i))
    (hC : |rC| ≤ defectC) (hG : |rG| ≤ defectG) :
    (∑ i, v i * (∑ j, M i j * a j)) +
        (∑ i, v i * (∑ j, C i j * v j)) +
        (∑ i, v i * G i) + dUc ≤
      -(∑ i, (d i - e i) * v i ^ 2) +
        (∑ i, (g i ^ 2 / (4 * e i))) * w ^ 2 + defectC + defectG := by
  have hdecomp := descriptor_power_remainder_identity M C Cfd v a tau G Gfd hdesc
  rw [← hrC, ← hrG] at hdecomp
  have hctrl := closed_loop_power_identity kp d g q v tau G0 w dUc htau hUc
  have hdiss := diagonal_dissipation_with_power_remainder
    d e g v w rC rG defectC defectG hd he hC hG
  calc
    (∑ i, v i * (∑ j, M i j * a j)) +
          (∑ i, v i * (∑ j, C i j * v j)) +
          (∑ i, v i * G i) + dUc =
        (∑ i, v i * tau i) + dUc + rC + rG := by
          linarith
    _ = -(∑ i, d i * v i ^ 2) +
          (∑ i, g i * v i * w) + rC + rG := by
          rw [hctrl]
    _ ≤ -(∑ i, (d i - e i) * v i ^ 2) +
          (∑ i, (g i ^ 2 / (4 * e i))) * w ^ 2 + defectC + defectG := hdiss

/- Mechanical storage decomposition.  This keeps the trajectory-facing
   `henergy` premise modular: a backend can certify the kinetic derivative,
   the Christoffel/metric relation, and the potential derivative separately,
   then obtain the descriptor power identity by pure ring arithmetic. -/
theorem mechanical_energy_power_identity
    (M Mdot C : Fin 6 → Fin 6 → ℝ) (v a G : Fin 6 → ℝ)
    (dK dU dE : ℝ)
    (hK : dK =
      (∑ i, v i * (∑ j, M i j * a j)) +
        (1 / 2 : ℝ) * (∑ i, v i * (∑ j, Mdot i j * v j)))
    (hC : (1 / 2 : ℝ) * (∑ i, v i * (∑ j, Mdot i j * v j)) =
      ∑ i, v i * (∑ j, C i j * v j))
    (hU : dU = ∑ i, v i * G i)
    (hE : dE = dK + dU) :
    dE =
      (∑ i, v i * (∑ j, M i j * a j)) +
        (∑ i, v i * (∑ j, C i j * v j)) +
        (∑ i, v i * G i) := by
  calc
    dE = dK + dU := hE
    _ = ((∑ i, v i * (∑ j, M i j * a j)) +
          (1 / 2 : ℝ) * (∑ i, v i * (∑ j, Mdot i j * v j))) +
          (∑ i, v i * G i) := by rw [hK, hU]
    _ = (∑ i, v i * (∑ j, M i j * a j)) +
          (∑ i, v i * (∑ j, C i j * v j)) +
          (∑ i, v i * G i) := by rw [hC]

/- Source-to-storage derivative seam.  The descriptor theorem above is an
   algebraic power inequality; this wrapper makes the only trajectory-level
   premise explicit: `dE` must equal the kinetic-plus-potential power on the
   left.  No inverse-mass or discretization fact is smuggled into the bridge. -/
theorem descriptor_energy_derivative_bound
    (M C Cfd : Fin 6 → Fin 6 → ℝ) (v a tau G Gfd : Fin 6 → ℝ)
    (kp d g q G0 : Fin 6 → ℝ) (e : Fin 6 → ℝ)
    (dE w dUc rC rG defectC defectG : ℝ)
    (hd : ∀ i, 0 < d i) (he : ∀ i, 0 < e i)
    (hdesc : ∀ i,
      (∑ j, M i j * a j) = tau i - (∑ j, Cfd i j * v j) - Gfd i)
    (htau : ∀ i, tau i = -kp i * q i - d i * v i + G0 i + g i * w)
    (hUc : dUc = ∑ i, (kp i * q i - G0 i) * v i)
    (hrC : rC = ∑ i, v i * (∑ j, (C i j - Cfd i j) * v j))
    (hrG : rG = ∑ i, v i * (G i - Gfd i))
    (hC : |rC| ≤ defectC) (hG : |rG| ≤ defectG)
    (henergy : dE =
      (∑ i, v i * (∑ j, M i j * a j)) +
        (∑ i, v i * (∑ j, C i j * v j)) +
        (∑ i, v i * G i) + dUc) :
    dE ≤ -(∑ i, (d i - e i) * v i ^ 2) +
      (∑ i, (g i ^ 2 / (4 * e i))) * w ^ 2 + defectC + defectG := by
  rw [henergy]
  exact descriptor_closed_loop_dissipation_with_remainder
    M C Cfd v a tau G Gfd kp d g q G0 e w dUc rC rG defectC defectG
    hd he hdesc htau hUc hrC hrG hC hG

/- Chain rule needed to turn a state-space Lie derivative bound into the
   scalar energy derivative consumed by the fencing theorem. -/
theorem energy_chain_rule
    {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {V : X → ℝ} {dV : X →L[ℝ] ℝ} {alpha : ℝ → X}
    {s : Set ℝ} {t : ℝ} {x' : X}
    (hV : HasFDerivAt V dV (alpha t))
    (halpha : HasDerivWithinAt alpha x' s t) :
    HasDerivWithinAt (fun u => V (alpha u)) (dV x') s t := by
  exact hV.comp_hasDerivWithinAt t halpha

/- Algebraic first-exit core.  The differential inequality is supplied by
   the pointwise ledger; this theorem consumes only its integrated tube. -/
theorem invariant_of_energy_tube
    {V p : ℝ → ℝ} {tube kappa : ℝ}
    (hk : 0 ≤ kappa)
    (hV : ∀ t, V t ≤ tube)
    (hp : ∀ t, p t ≤ kappa * V t)
    (hstrict : kappa * tube < 45) :
    ∀ t, p t < 45 := by
  intro t
  have h1 := hp t
  have h2 := hV t
  nlinarith

/- Integrated-energy interface.  An ODE/interval backend only needs to
   provide `hInt`; the remaining tube and first-exit arithmetic is exact. -/
theorem integrated_energy_tube
    {E : ℝ → ℝ} {e0 beta T : ℝ}
    (he0 : E 0 ≤ e0) (hbeta : 0 ≤ beta)
    (hInt : ∀ t, 0 ≤ t → t ≤ T → E t - E 0 ≤ beta * t) :
    ∀ t, 0 ≤ t → t ≤ T → E t ≤ e0 + beta * T := by
  intro t ht0 htT
  have hi := hInt t ht0 htT
  have hprod : 0 ≤ beta * (T - t) :=
    mul_nonneg hbeta (sub_nonneg.mpr htT)
  nlinarith

/- Unit-horizon version matching the declared disturbance convention
   `w(t)=c*t`, `|c|^2<=3`: the supply integral is bounded by `gamma`, while
   an additive defect integrates to `defect`. -/
theorem unit_horizon_cubic_energy_tube
    {E : ℝ → ℝ} {e0 gamma defect : ℝ}
    (he0 : E 0 ≤ e0) (hgamma : 0 ≤ gamma) (hdefect : 0 ≤ defect)
    (hInt : ∀ t, 0 ≤ t → t ≤ 1 →
      E t - E 0 ≤ gamma * t ^ 3 + defect * t) :
    ∀ t, 0 ≤ t → t ≤ 1 → E t ≤ e0 + gamma + defect := by
  intro t ht0 ht1
  have hprod : 0 ≤ t * (1 - t) :=
    mul_nonneg ht0 (sub_nonneg.mpr ht1)
  have ht2 : t ^ 2 ≤ t := by
    nlinarith
  have ht2_one : t ^ 2 ≤ 1 := by
    nlinarith
  have hmul := mul_le_mul_of_nonneg_right ht2 ht0
  have ht3 : t ^ 3 ≤ 1 := by
    nlinarith
  have hpow := mul_le_mul_of_nonneg_left ht3 hgamma
  have hlin := mul_le_mul_of_nonneg_left ht1 hdefect
  have hi := hInt t ht0 ht1
  nlinarith

/- Differential version of the same tube.  This uses Mathlib's one-sided
   derivative fencing theorem, so an ODE backend can supply a pointwise Lie
   derivative bound directly instead of separately exporting an integral. -/
theorem cubic_derivative_energy_tube
    {E : ℝ → ℝ} {e0 gamma defect : ℝ} {eprime : ℝ → ℝ}
    (he0 : E 0 ≤ e0) (_hgamma : 0 ≤ gamma) (_hdefect : 0 ≤ defect)
    (hcont : ContinuousOn E (Set.Icc 0 1))
    (hderiv : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt E (eprime t) (Set.Ici t) t)
    (hbound : ∀ t ∈ Set.Ico 0 1,
      eprime t ≤ 3 * gamma * t ^ 2 + defect) :
    ∀ t ∈ Set.Icc 0 1,
      E t ≤ e0 + gamma * t ^ 3 + defect * t := by
  let B : ℝ → ℝ := fun t => e0 + gamma * t ^ 3 + defect * t
  have hB : ∀ t, HasDerivAt B (3 * gamma * t ^ 2 + defect) t := by
    intro t
    dsimp [B]
    convert ((hasDerivAt_const t e0).add
      (((hasDerivAt_const t gamma).mul ((hasDerivAt_id t).pow 3)).add
        ((hasDerivAt_const t defect).mul (hasDerivAt_id t)))) using 1
    · funext x
      simp [id]
      ring
    · simp [id]
      ring
  have hBcont : ContinuousOn B (Set.Icc 0 1) := by
    dsimp [B]
    fun_prop
  have hres := image_le_of_deriv_right_le_deriv_boundary
    (a := (0 : ℝ)) (b := 1) hcont hderiv (by simpa [B] using he0)
    hBcont (fun t _ => (hB t).hasDerivWithinAt) hbound
  intro t ht
  exact hres ht

/- Direct state-space interface: an ODE trajectory plus a Lie derivative
   inequality yields the scalar derivative bound consumed by fencing. -/
theorem lie_derivative_cubic_energy_tube
    {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {V : X → ℝ} {dV : X →L[ℝ] ℝ} {alpha : ℝ → X}
    {f : ℝ → X → X} {e0 gamma defect : ℝ}
    (he0 : V (alpha 0) ≤ e0) (_hgamma : 0 ≤ gamma) (_hdefect : 0 ≤ defect)
    (hcont : ContinuousOn (fun t => V (alpha t)) (Set.Icc 0 1))
    (hV : ∀ t ∈ Set.Ico 0 1, HasFDerivAt V dV (alpha t))
    (halpha : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt alpha (f t (alpha t)) (Set.Ici t) t)
    (hLie : ∀ t ∈ Set.Ico 0 1,
      dV (f t (alpha t)) ≤ 3 * gamma * t ^ 2 + defect) :
    ∀ t ∈ Set.Icc 0 1,
      V (alpha t) ≤ e0 + gamma * t ^ 3 + defect * t := by
  have hderiv : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt (fun u => V (alpha u))
        (dV (f t (alpha t))) (Set.Ici t) t := by
    intro t ht
    exact energy_chain_rule (hV t ht) (halpha t ht)
  exact cubic_derivative_energy_tube he0 _hgamma _hdefect hcont hderiv hLie

/- The lifted trigonometric graph is an invariant, not a static relaxation:
   if c=cos(q), s=sin(q) is propagated by c'=-s*v and s'=c*v, the circle
   equation is preserved exactly.  This scalar lemma is the componentwise
   building block for the six-joint torus lift. -/
theorem circle_lift_invariant
    {c s v : ℝ → ℝ}
    (hc : ∀ t, HasDerivAt c (-s t * v t) t)
    (hs : ∀ t, HasDerivAt s (c t * v t) t)
    (h0 : c 0 ^ 2 + s 0 ^ 2 = 1) :
    ∀ t, c t ^ 2 + s t ^ 2 = 1 := by
  let r : ℝ → ℝ := fun t => c t ^ 2 + s t ^ 2
  have hc_diff : Differentiable ℝ c := fun t => (hc t).differentiableAt
  have hs_diff : Differentiable ℝ s := fun t => (hs t).differentiableAt
  have hr_diff : Differentiable ℝ r := by
    dsimp [r]
    exact (hc_diff.pow 2).add (hs_diff.pow 2)
  have hr_deriv : ∀ t, deriv r t = 0 := by
    intro t
    have hcp := (hc t).pow 2
    have hsp := (hs t).pow 2
    have hr_at : HasDerivAt r
        (2 * c t * (-s t * v t) + 2 * s t * (c t * v t)) t := by
      dsimp [r]
      (convert hcp.add hsp using 1; ring)
    rw [hr_at.deriv]
    ring
  have hconst : ∀ t, r t = r 0 := by
    intro t
    exact is_const_of_deriv_eq_zero hr_diff hr_deriv t 0
  intro t
  have ht := hconst t
  dsimp [r] at ht
  nlinarith

/- Pointwise coordinate bounds supplied by the lifted circle constraint.  This
   is the small but useful continuation fact that keeps the auxiliary c/s
   states from introducing a new blow-up channel. -/
theorem circle_lift_coordinate_bounds
    {c s : ℝ} (hcircle : c ^ 2 + s ^ 2 = 1) :
    |c| ≤ 1 ∧ |s| ≤ 1 := by
  constructor
  · apply (abs_le_one_iff_mul_self_le_one).2
    nlinarith [sq_nonneg s]
  · apply (abs_le_one_iff_mul_self_le_one).2
    nlinarith [sq_nonneg c]

/- Six-joint packaging of the scalar invariant. -/
theorem finite_torus_lift_invariant
    {c s v : ℝ → Fin 6 → ℝ}
    (hc : ∀ i t, HasDerivAt (fun u => c u i) (-s t i * v t i) t)
    (hs : ∀ i t, HasDerivAt (fun u => s u i) (c t i * v t i) t)
    (h0 : ∀ i, c 0 i ^ 2 + s 0 i ^ 2 = 1) :
    ∀ t i, c t i ^ 2 + s t i ^ 2 = 1 := by
  intro t i
  exact circle_lift_invariant
    (c := fun u => c u i) (s := fun u => s u i) (v := fun u => v u i)
    (fun u => hc i u) (fun u => hs i u) (h0 i) t

/- Complete arithmetic bridge from an integrated energy estimate to the
   strict candidate-domain barrier. -/
theorem integrated_energy_barrier
    {E p : ℝ → ℝ} {e0 beta T kappa : ℝ}
    (_hT : 0 ≤ T) (he0 : E 0 ≤ e0) (hbeta : 0 ≤ beta)
    (hInt : ∀ t, 0 ≤ t → t ≤ T → E t - E 0 ≤ beta * t)
    (hk : 0 ≤ kappa)
    (hp : ∀ t, p t ≤ kappa * E t)
    (hstrict : kappa * (e0 + beta * T) < 45) :
    ∀ t, 0 ≤ t → t ≤ T → p t < 45 := by
  intro t ht0 htT
  have hE := integrated_energy_tube he0 hbeta hInt t ht0 htT
  have hscaled : kappa * E t ≤ kappa * (e0 + beta * T) :=
    mul_le_mul_of_nonneg_left hE hk
  have hp_t := hp t
  nlinarith

/- The exact rational equality used by the terminal bridge. -/
theorem terminal_budget_identity :
    ((4780339200000000000 : ℚ) / 100014029109103883) *
      ((100014029109103883 : ℚ) / 398361600000000000) = 12 := by
  norm_num

/- Historical scalar arithmetic from the superseded full-state p<=45 audit.
   These lemmas are retained for reproducibility only; the corrected
   authoritative damping vector rejects that first-exit loop. -/
theorem compact_initial_energy_margin :
    ((27 : ℝ) / 800) < 45 := by
  norm_num

theorem compact_global_energy_margin :
    ((1600000 : ℝ) / 9401) *
        ((18205736938030765206360603515581841115615869237530557400570808358562167888209181498675468895591120178441202187859904026019841963 : ℝ) /
          72447523497288130995060527095158620884622032447514300830505560717160696258048784576426829695592540064000000000000000000000000000) <
      45 := by
  norm_num

/- Exact scalar remainder arithmetic from the proof-grade FD ledger.  The
   first term is the cubic C remainder evaluated at |v_i|<=15/2; the second
   is the Young-allocated gravity remainder. -/
theorem compact_fd_residual_scalar_margin :
    ((12390647 : ℝ) / 192000000000000000) * ((15 : ℝ) / 2) ^ 3 +
        (316707628602951 : ℝ) /
          55328000000000000000000000000000 <
      (1 : ℝ) / 1000000 := by
  norm_num

/- Corrected active-domain scalar remainder budget.  The larger V<=1 velocity
   cap is still small enough for the cubic C remainder plus weighted gravity
   term to remain below 10^-6. -/
theorem compact_active_V1_fd_residual_scalar_margin :
    ((12390647 : ℝ) / 192000000000000000) * (15 : ℝ) ^ 3 +
        (90362741420079 : ℝ) /
          12646400000000000000000000000000000 <
      (1 : ℝ) / 1000000 := by
  norm_num

theorem compact_global_energy_margin_with_fd_residual :
    ((1600000 : ℝ) / 9401) *
        (((18205736938030765206360603515581841115615869237530557400570808358562167888209181498675468895591120178441202187859904026019841963 : ℝ) /
          72447523497288130995060527095158620884622032447514300830505560717160696258048784576426829695592540064000000000000000000000000000) +
          (1 : ℝ) / 1000000) <
      45 := by
  norm_num

/- Exact continuation arithmetic from the rational full-DH growth ledger.
   These identities only bind the numerical cap to the analytic continuation
   interface; they do not instantiate the vector-field or energy premises. -/
theorem compact_full_dh_growth_bound_identity :
    (3 : ℝ) *
        ((87839445001755279 : ℝ) / 1280000000000000) /
          ((9401 : ℝ) / 1000000) =
      (37645476429323691 : ℝ) / 1719040000000 := by
  norm_num

theorem compact_full_dh_state_derivative_cap_dominates_velocity :
    (15 : ℝ) / 2 ≤
      (37645476429323691 : ℝ) / 1719040000000 := by
  norm_num

/- Corrected continuation arithmetic on the active V<=1 domain. -/
theorem compact_block_energy_growth_bound_identity :
    (3 : ℝ) *
        ((73439445001755279 : ℝ) / 320000000000000) /
          ((9401 : ℝ) / 1000000) =
      (220318335005265837 : ℝ) / 3008320000000 := by
  norm_num

theorem compact_block_energy_state_derivative_cap_dominates_velocity :
    (15 : ℝ) ≤
      (220318335005265837 : ℝ) / 3008320000000 := by
  norm_num

/- Corrected block-(4,5) energy barrier arithmetic.  The large rational
   numerators are imported from the exact Python ledger; these theorems bind
   only its strict scalar margins, not the source-to-flow or Float64 premises. -/
theorem compact_block_energy_tube_margin :
    ((318525681001915974636384401406082767039818942121625862513363336470653748461802541940931089966927804213070928276770940133357989 : ℝ) /
      1027777363126911112376109662596405595016026412337446488875345857972461858572374519620674968948064102400000000000000000000000000) <
      1 := by
  norm_num

theorem compact_block_p45_margin :
    ((4944589620281612983892674839175557861584203990718107085231560432194170786624537835686916656373280202661870321123433150728133337985040433298506757 : ℝ) /
      334364084556777374502174341278247938397987225094846087238274560040082603562896690967741712234286805576372817106610969074207533750500000000000000) <
      45 := by
  norm_num

end RobotFormalEnergy
