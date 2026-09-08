"""Bounded BODY6 interface audit. Stdout only; never writes Lean objects/state.

Checks the complete reassigned leaf plus explicitly extracted generic contract
and proposed adapters through Lean stdin. Does not claim to compile the complete
PATHCONTRACT module when its aligned import is unavailable. No admission path.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "examples/routeb_b45_source_comparator_lean"
PIN = ROOT / "examples/local_fkg"
LEAN = Path("C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe")
CONTRACT = BODY / "NEW_BODY6_SLICE_PATHCONTRACT20260908.lean"
REASSIGNED = BODY / "NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean"

# Proposed reusable glue, not a change to either existing Lean file.
ADAPTERS = r"""
namespace NEW_SEAM_BODY6_TYPED
noncomputable section
open NEW_BODY6_SLICE_INITIALPATHCAPS20260907
open NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907
open NEW_BODY6_SLICE_PATHCONTRACT20260908
open NEW_BODY6_SLICE_PATHREASSIGNED20260908

theorem initial_growth_to_transfer_inputs {X C : Type*}
    (project : X → C) (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (a beta B bar : ℝ) (b : ℝ → ℝ)
    (hp : DomainProjection project D Q) (hw : WholePathMembership D path)
    (hv : ShiftIdentityOnQ project Q F G B)
    (hi : InitialPathCap F path a) (hg : IntegratedGrowth F path b)
    (hu : ∀ t ∈ Set.Icc (0 : ℝ) 1, b t ≤ beta)
    (hb : (a + beta) + B ≤ bar) :
    TransferInputs project D Q path F G B (a + beta) bar :=
  ⟨hp, hw, hv, growth_supplies_full_cap_attempt F path a beta b hi hg hu, hb⟩

/- This repackages an ALREADY supplied full cap. It is not integration and
   does not recover any prescribed initial/growth certificate a,b. -/
theorem transfer_inputs_to_algebraic_path_contract {X C : Type*}
    (project : X → C) (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (B cap bar : ℝ)
    (h : TransferInputs project D Q path F G B cap bar) :
    PathContract F G path (F 0 (path 0)) B bar (fun _ => cap - F 0 (path 0)) := by
  refine ⟨le_rfl, ?_, ?_, ?_⟩
  · intro t ht
    have hs := h.sourceCap t ht
    dsimp
    linarith
  · intro t ht
    exact h.value t ht (path t) (h.projection t ht (path t) (h.wholePath t ht))
  · intro t ht
    have hb := h.budget
    dsimp
    linarith

/- A pointwise budget itself gives the uniform source cap bar-B. What
   cannot be reconstructed is the fixed-domain and off-path identity. -/
theorem path_contract_to_transfer_inputs_with_domain {X C : Type*}
    (project : X → C) (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (a B bar : ℝ) (b : ℝ → ℝ)
    (h : PathContract F G path a B bar b)
    (hp : DomainProjection project D Q) (hw : WholePathMembership D path)
    (hv : ShiftIdentityOnQ project Q F G B) :
    TransferInputs project D Q path F G B (bar - B) bar := by
  refine ⟨hp, hw, hv, ?_, ?_⟩
  · intro t ht
    have hi : F 0 (path 0) ≤ a := h.initial
    have hg := h.growth t ht
    have hb := h.budget t ht
    linarith
  · linarith

end
end NEW_SEAM_BODY6_TYPED
#print axioms NEW_BODY6_SLICE_PATHREASSIGNED20260908.repaired_contract_adapter_attempt
#print axioms NEW_BODY6_SLICE_PATHREASSIGNED20260908.pullback_projection_attempt
#print axioms NEW_BODY6_SLICE_PATHREASSIGNED20260908.pullback_membership_iff_attempt
#print axioms NEW_BODY6_SLICE_PATHREASSIGNED20260908.fixed_domain_supplies_pullback_attempt
#print axioms NEW_BODY6_SLICE_PATHREASSIGNED20260908.projected_membership_does_not_certify_fixed_domain_attempt
#print axioms NEW_BODY6_SLICE_PATHCONTRACT20260908.consume_path_contract_attempt
#print axioms NEW_SEAM_BODY6_TYPED.initial_growth_to_transfer_inputs
#print axioms NEW_SEAM_BODY6_TYPED.transfer_inputs_to_algebraic_path_contract
#print axioms NEW_SEAM_BODY6_TYPED.path_contract_to_transfer_inputs_with_domain
"""


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def environment():
    paths = [BODY, PIN / ".lake/build/lib/lean"]
    paths.extend(package / ".lake/build/lib/lean"
                 for package in sorted((PIN / ".lake/packages").iterdir()) if package.is_dir())
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(str(path) for path in paths if path.is_dir())
    return env


def check(name, arguments, env, source=None, timeout=50):
    command = [str(LEAN), "-DwarningAsError=true", *arguments]
    try:
        run = subprocess.run(command, input=source, encoding="utf-8", capture_output=True,
                             cwd=ROOT, env=env, timeout=timeout, check=False)
        return {"name": name, "command": command, "exit_code": run.returncode,
                "stdout": run.stdout, "stderr": run.stderr,
                "stdin_sha256": sha256(source.encode()).hexdigest() if source else None}
    except subprocess.TimeoutExpired as exc:
        def partial(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
        return {"name": name, "command": command, "exit_code": None, "status": "TIMEOUT",
                "timeout_seconds": timeout, "stdout": partial(exc.stdout),
                "stderr": partial(exc.stderr),
                "stdin_sha256": sha256(source.encode()).hexdigest() if source else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapters-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=50)
    args = parser.parse_args()
    original = CONTRACT.read_text(encoding="utf-8")
    start = original.index("structure PathContract ")
    end = original.index("/- The existing domain and alignment fields", start)
    fragment = original[start:end]
    stdin = ("import NEW_BODY6_SLICE_INITIALPATHCAPS20260907\n" +
             REASSIGNED.read_text(encoding="utf-8") +
             "\nnamespace NEW_BODY6_SLICE_PATHCONTRACT20260908\nnoncomputable section\n" +
             "open NEW_BODY6_SLICE_INITIALPATHCAPS20260907\n" + fragment +
             "\nend\nend NEW_BODY6_SLICE_PATHCONTRACT20260908\n" + ADAPTERS)
    env = environment()
    runs = []
    if not args.adapters_only:
        runs.append(check("full_PATHCONTRACT_import_check", [str(CONTRACT)], env))
    runs.append(check("full_PATHREASSIGNED_plus_extracted_generic_contract_and_adapters",
                      ["--stdin"], env, stdin, args.timeout))
    report = {"schema": "routeb.body6.typed_interface_audit.v1", "status": "pending",
              "scope": "bounded_Lean_invocations_no_dependency_rebuild",
              "runs": runs, "lean_path": env["LEAN_PATH"],
              "toolchain": (PIN / "lean-toolchain").read_text().strip(),
              "input_hashes": {path.relative_to(ROOT).as_posix(): digest(path) for path in
                  (CONTRACT, REASSIGNED, BODY / "NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean",
                   BODY / "NEW_BODY6_SLICE_INITIALPATHCAPS20260907.olean",
                   BODY / "NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean",
                   BODY / "NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.olean",
                   Path(__file__))},
              "generic_fragment_sha256": sha256(fragment.encode()).hexdigest(),
              "files_written_by_checker": 0, "dependencies_recompiled": False,
              "complete_PATHCONTRACT_checked": any(r["name"] == "full_PATHCONTRACT_import_check"
                                                     and r["exit_code"] == 0 for r in runs),
              "adapter_Lean_check_passed": runs[-1]["exit_code"] == 0,
              "registry_eligible": False, "source_binding_proven": False,
              "concrete_path_contract_inhabited": False}
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 3  # Diagnostics never authorize admission, including successful Lean checks.


if __name__ == "__main__":
    raise SystemExit(main())
