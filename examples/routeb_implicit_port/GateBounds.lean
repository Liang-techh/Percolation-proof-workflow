import ImplicitPort

namespace RouteBPortGates

open RouteBImplicitPort

theorem g_times_h (s nu k : ℝ) (hh : H nu k ≠ 0) :
    G s nu k * H nu k = s * nu - (s + nu) * k := by
  unfold H G at *
  field_simp
  ring

theorem positivity_gate (s nu k : ℝ) (hs : 0 < s) (hnu : 0 < nu) :
    (0 < H nu k ∧ 0 < G s nu k) ↔ k < s * nu / (s + nu) := by
  have hsum : 0 < s + nu := add_pos hs hnu
  constructor
  · rintro ⟨hh, hg⟩
    have hp := mul_pos hg hh
    rw [g_times_h s nu k (ne_of_gt hh)] at hp
    apply (lt_div_iff₀ hsum).2
    nlinarith
  · intro hk
    have ht := (lt_div_iff₀ hsum).1 hk
    have hh : 0 < H nu k := by
      unfold H
      nlinarith [sq_pos_of_pos hnu]
    have hp : 0 < G s nu k * H nu k := by
      rw [g_times_h s nu k (ne_of_gt hh)]
      nlinarith
    have hg : 0 < G s nu k := by
      by_contra hbad
      have hn := mul_nonpos_of_nonpos_of_nonneg (le_of_not_gt hbad) (le_of_lt hh)
      linarith
    exact ⟨hh, hg⟩

/- Exact declared induced-port candidate, not a proof of that port bound. -/
noncomputable def rho : ℝ := 234721 / 5000000
noncomputable def m44 : ℝ := 350003 / 3000000
noncomputable def m55 : ℝ := 200739 / 4000000
noncomputable def b44 : ℝ := 1402217 / 12000000
noncomputable def b55 : ℝ := 200739 / 4000000
noncomputable def k44 (lambda : ℝ) : ℝ :=
  5 * lambda / m44 ^ 2 + (1 / 6 : ℝ) * rho * b44 / m44 ^ 2
noncomputable def k55 (lambda : ℝ) : ℝ :=
  5 * lambda / m55 ^ 2 + (1 / 6 : ℝ) * rho * b55 / m55 ^ 2
noncomputable def limit : ℝ := 33638704099 / 12400000000000000

theorem actual_gate_iff (lambda : ℝ) :
    ((0 < H (1 / 6) (k44 lambda) ∧ 0 < G 5 (1 / 6) (k44 lambda)) ∧
     (0 < H (1 / 6) (k55 lambda) ∧ 0 < G 5 (1 / 6) (k55 lambda))) ↔
      lambda < limit := by
  rw [positivity_gate 5 (1 / 6) (k44 lambda) (by norm_num) (by norm_num),
      positivity_gate 5 (1 / 6) (k55 lambda) (by norm_num) (by norm_num)]
  norm_num [k44, k55, m44, m55, b44, b55, rho, limit]
  constructor
  · rintro ⟨_, h5⟩
    linarith
  · intro h
    constructor <;> linarith

theorem source_placeholder_exceeds_gate : limit < (1 / 100 : ℝ) := by
  norm_num [limit]

theorem nonzero_acceleration_charge_feasible :
    (0 < H (1 / 6) (k44 (1 / 1000000)) ∧ 0 < G 5 (1 / 6) (k44 (1 / 1000000))) ∧
    (0 < H (1 / 6) (k55 (1 / 1000000)) ∧ 0 < G 5 (1 / 6) (k55 (1 / 1000000))) := by
  rw [actual_gate_iff]
  norm_num [limit]

#print axioms g_times_h
#print axioms positivity_gate
#print axioms actual_gate_iff
#print axioms source_placeholder_exceeds_gate
#print axioms nonzero_acceleration_charge_feasible

end RouteBPortGates
