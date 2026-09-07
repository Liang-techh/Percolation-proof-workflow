"""Conservative intake for Anthropic's Fermat Lean research artifact.

This module imports provenance and reusable-pattern metadata, not theorem truth.
The FLT repository is a research snapshot with a different Mathlib revision from
the Route-B environment, so every candidate is classified before reuse and no
candidate is inserted into the verified registry by this scanner.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


SCHEMA = "anthropic-fermats-intake-v1"
REPO = "https://github.com/anthropics/fermats-last-theorem"


@dataclass(frozen=True)
class ReuseCandidate:
    path: str
    kind: str
    classification: int
    reuse_mode: str
    rationale: str
    current_routeb_use: str
    attribution_ref: str
    declaration: str | None = None
    source_lines: str | None = None
    source_commit: str | None = None
    source_sha256: str | None = None
    mathlib_revision: str | None = None
    lean_toolchain: str | None = None
    admission_status: str = "pending"
    pending_reason: str = "static catalog entry; declaration-level compilation is required"


@dataclass(frozen=True)
class FermatSnapshot:
    repository: str
    commit: str
    lean_toolchain: str
    mathlib_revision: str | None
    license: str
    source_counts: dict[str, int]
    candidates: tuple[ReuseCandidate, ...]
    architecture: dict[str, Any]


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], check=True,
        capture_output=True, text=True, encoding="utf-8",
    )
    return result.stdout


def _blob(repo: Path, path: str) -> str:
    return _git(repo, "show", f"HEAD:{path}")


def _blob_bytes(repo: Path, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"HEAD:{path}"],
        check=True, capture_output=True,
    )
    return result.stdout


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _mathlib_revision(manifest: str) -> str | None:
    try:
        data = json.loads(manifest)
    except json.JSONDecodeError:
        return None
    for package in data.get("packages", []):
        if package.get("name") == "mathlib":
            return package.get("rev")
    return None


def _counts(paths: list[str]) -> dict[str, int]:
    prefixes = {"Definitions": "Definitions/", "Theorems": "Theorems/",
                "P2M/Sol": "P2M/Sol/", "P2M/Derive": "P2M/Derive/",
                "verification": "verification/", "tools": "tools/"}
    return {name: sum(path.startswith(prefix) and path.endswith(".lean")
                      for path in paths)
            for name, prefix in prefixes.items()}


def _candidate(path: str, kind: str, classification: int, mode: str,
               rationale: str, routeb: str, attribution: str) -> ReuseCandidate:
    return ReuseCandidate(path, kind, classification, mode, rationale, routeb, attribution)


def _declaration(path: str, name: str, lines: str, classification: int,
                 mode: str, rationale: str, routeb: str,
                 attribution: str) -> ReuseCandidate:
    """Add a declaration-level candidate; provenance is bound after HEAD is read."""
    return ReuseCandidate(
        path, "declaration", classification, mode, rationale, routeb, attribution,
        declaration=name, source_lines=lines,
    )


def _candidates(paths: set[str]) -> tuple[ReuseCandidate, ...]:
    known: list[ReuseCandidate] = []

    def add_declaration(path: str, *args):
        if path in paths:
            known.append(_declaration(path, *args))

    add_declaration(
        "Definitions/Def_Mathlib_IsModuleTopology.lean",
        "Module.continuous_bilinear_of_finite_free", "147-165", 1,
        "recompile-and-admit",
        "Finite-free bilinear continuity for a generic module-level coordinate or modal term; no number-theory hypotheses are required.",
        "P3/P7 finite-dimensional coordinate and bilinear continuity adapters; does not prove a PDE estimate or positivity bound.",
        "ATTRIBUTION.md §1: FLT/Mathlib/Topology/Algebra/Module/ModuleTopology.lean; Apache-2.0",
    )
    add_declaration(
        "Definitions/Def_Mathlib_IsModuleTopology.lean",
        "IsModuleTopology.continuousLinearEquiv", "362-375", 2,
        "adapt-and-recompile",
        "Builds a ContinuousLinearEquiv from a LinearEquiv under module-topology hypotheses; useful, but the FLT staging class must be reconciled with the target API.",
        "Coordinate/state-space transport only; continuity does not imply an isometry, norm constant, or flowpipe result.",
        "ATTRIBUTION.md §1: FLT/Mathlib/Topology/Algebra/Module/ModuleTopology.lean; Apache-2.0",
    )
    add_declaration(
        "Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean",
        "Submodule.Quotient.continuousLinearEquiv", "5-18", 1,
        "recompile-and-admit",
        "Continuous linear transport between submodule quotients; a precise generic interface for kernel or boundary quotient coordinates.",
        "P3/P8 quotient-level state and residual transport; it supplies no coverage or trajectory inclusion.",
        "ATTRIBUTION.md §1: FLT/Mathlib/Topology/Algebra/Module/Quotient.lean; Apache-2.0",
    )
    add_declaration(
        "Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean",
        "Submodule.quotientPiContinuousLinearEquiv", "20-37", 1,
        "recompile-and-admit",
        "Finite-product quotient transport with explicit Fintype and topological additive-group assumptions.",
        "Finite cell/product coordinate adapters only; do not generalize the finite-index topology contract.",
        "ATTRIBUTION.md §1: FLT/Mathlib/Topology/Algebra/Module/Quotient.lean; Apache-2.0",
    )
    add_declaration(
        "Definitions/Def_LinearMap_ExtPushout.lean",
        "ExtPushout (extPushoutRel, mk, inl, inr, proj, lift, hom_ext)", "12-129", 1,
        "recompile-and-admit",
        "Pure module pushout/quotient construction with kernel-range and universal-property declarations; no topology or number theory.",
        "Descriptor, constraint, or boundary quotient construction after the concrete Route-B map and semantics are supplied.",
        "Repository source; inspect ATTRIBUTION.md and NOTICE before copying; Apache-2.0",
    )

    def add(path: str, *args):
        if path in paths:
            known.append(_candidate(path, *args))

    add(
        "Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean",
        "mathlib-adapter", 2, "adapt-and-recompile",
        "Provides continuous linear equivalences on submodule quotients and finite products; useful for quotient/state-space transport, but the FLT source is pinned to a different Mathlib revision.",
        "Future quotient/transport layer for constrained function or state spaces; recompile against the Route-B pin before admission.",
        "ATTRIBUTION.md §1: FLT/Mathlib/Topology/Algebra/Module/Quotient.lean; Apache-2.0",
    )
    add(
        "P2M/Sol/S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean",
        "spectral-invariant-subspace", 1, "reprove-and-pin",
        "Proves that a continuous map commuting with a compact symmetric operator preserves a nonzero eigenspace and its orthogonal complement; this is directly relevant to Route-B spectral block selection and modal residual channels after recompilation against the current Mathlib pin.",
        "Highest-value current adapter: use as a theorem-backed template for spectral partition invariance, but admit only the independently compiled current-pin sidecar.",
        "Anthropic FLT P2M/Sol source; Apache-2.0; exact file attribution must be checked against ATTRIBUTION.md",
    )
    add(
        "P2M/Sol/S_LinearMap_exists_ker_linearEquiv_and_quotient_linearEquiv_of_surjective_of_forall_exact.lean",
        "exact-sequence-quotient", 1, "reprove-and-pin",
        "Constructs kernel and quotient linear equivalences from exactness and surjectivity; a generic typed adapter for descriptor elimination and constrained residual/state quotient interfaces.",
        "Use as a reusable exactness leaf in future Route-B descriptor reduction, only after a current-pin compilation and explicit domain semantics are supplied.",
        "Anthropic FLT P2M/Sol source; Apache-2.0; exact file attribution must be checked against ATTRIBUTION.md",
    )
    add(
        "P2M/Sol/S_TransportGlue_exists_pairing_of_linearEquiv.lean",
        "pairing-transport", 1, "reprove-and-pin",
        "Transports a scalar-compatible pairing along a linear equivalence; directly reusable for preserving quadratic/residual pairings under scaled or modal coordinates.",
        "Candidate adapter for Route-B energy/residual coordinate changes; the physical norm and positivity obligations remain separate open leaves.",
        "Anthropic FLT P2M/Sol source; Apache-2.0; exact file attribution must be checked against ATTRIBUTION.md",
    )
    add(
        "P2M/Sol/S_ContinuousLinearMap_exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous.lean",
        "representation-average", 1, "reprove-and-pin",
        "Builds a bounded continuous averaging operator represented by an integral of scalar multiples; useful for symmetry projections and modal/Fourier averages, subject to a new Route-B measure/domain contract.",
        "P7 Fourier/Krylov fallback and symmetry projection only; does not establish DH dynamics or a residual bound by itself.",
        "Anthropic FLT P2M/Sol source; Apache-2.0; exact file attribution must be checked against ATTRIBUTION.md",
    )
    add(
        "Definitions/Def_Mathlib_IsModuleTopology.lean",
        "mathlib-adapter", 2, "adapt-and-recompile",
        "Propagates topological-module structure through inducing linear maps, submodules, Pi types and a biscalar interface; a compact adapter pattern for typed continuous dynamics.",
        "Use as a template for declaring continuity of Route-B finite-dimensional maps and future quotient flowpipe spaces.",
        "ATTRIBUTION.md §1: FLT/Mathlib/Topology/Algebra/Module/ModuleTopology.lean and related FLT files; Apache-2.0",
    )
    add(
        "Definitions/Def_LinearMap_ExtPushout.lean",
        "linear-algebra-construction", 2, "adapt-definition-only",
        "Defines an explicit linear pushout quotient with membership and zero criteria; useful for composing adapters with residual constraints, but not a drop-in Route-B theorem.",
        "Candidate construction for descriptor/residual quotient interfaces after a concrete mathematical use is specified.",
        "Repository source; inspect ATTRIBUTION.md and NOTICE before copying any lines; Apache-2.0",
    )
    add(
        "Theorems/Thm_AddChar_exists_continuousLinearMap_fourierChar_eq.lean",
        "fourier-transport", 2, "adapt-hypotheses",
        "Turns a continuous additive character into a continuous real linear map; relevant to Fourier fallback, but specialized to AddChar/Circle.",
        "P7 Fourier/Krylov fallback only; must not be used to claim true-DH or PDE semantics.",
        "Repository source; exact upstream note in ATTRIBUTION.md if adapted; Apache-2.0",
    )
    add(
        "Theorems/Thm_Algebra_exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential.lean",
        "calculus-local-chart", 3, "architecture-only",
        "A local finite-dimensional coordinate/existence theorem, but its algebraic-geometry hypotheses do not match Route-B dynamics.",
        "Borrow only the pattern of separating coordinate chart hypotheses from differentiability and uniqueness obligations.",
        "Repository source; not imported into Route-B; Apache-2.0",
    )
    add(
        "Theorems/Thm_AlgebraicCurve_Differential_pullbackAlong_comp.lean",
        "derivation-transport", 3, "architecture-only",
        "A clean compositional pullback law for algebraic differentials, but the objects are algebraic-curve-specific.",
        "Borrow the explicit transport-law leaf in a future DH coordinate-change adapter; no direct theorem reuse.",
        "Repository source; exact upstream attribution in ATTRIBUTION.md; Apache-2.0",
    )
    add(
        "P2M/Util.lean",
        "proof-orchestration", 3, "architecture-only",
        "Provides exact-reverting elaboration, type-equality checks and namespace/export helpers around a theorem/solution split.",
        "Use the protocol idea for candidate statement equality and proof-solution binding; do not copy Lean metaprogramming into the Python verifier.",
        "Anthropic FLT repository; Apache-2.0",
    )
    add(
        "tools/docs-site/gen/graphdata.py",
        "dependency-graph", 3, "adapt-graph-metrics",
        "Computes import-closure size, citation edges, landmarks and route stages from extracted declaration JSONL.",
        "Integrate graph metrics as non-authoritative DAG metadata and frontier prioritization evidence.",
        "Anthropic FLT repository; Apache-2.0",
    )
    add(
        "verification/comparator/config.json",
        "statement-comparator", 3, "adapt-contract",
        "Pins challenge/solution modules, theorem names, permitted axioms and comparator settings in a small auditable contract.",
        "Use as a model for the existing Route-B comparator manifest and fail-closed admission gate.",
        "Anthropic FLT repository; Apache-2.0",
    )
    add(
        "verification/comparator/Challenge.lean",
        "statement-comparator", 3, "adapt-contract",
        "Separates the trusted challenge statement from the solution implementation; challenge proofs are intentionally sorry and never evidence.",
        "Mirror the challenge/solution separation for every generated Route-B theorem candidate.",
        "Anthropic FLT repository; Apache-2.0",
    )
    add(
        "verification/comparator/Solution.lean",
        "statement-comparator", 3, "adapt-contract",
        "Replays the exact theorem statement against the completed theorem and derives the library-facing statement through an explicit bridge.",
        "Strengthen statement comparator diagnostics and source-level theorem identity checks.",
        "Anthropic FLT repository; Apache-2.0",
    )
    add(
        "formalization.yaml",
        "provenance-contract", 3, "adapt-schema",
        "Records project, authors, license, source relationships and the precise scope of named classical inputs.",
        "Attach external theorem provenance and semantic-strength boundaries to intake manifests.",
        "Anthropic FLT repository; Apache-2.0",
    )
    return tuple(known)


def scan_fermats_repo(repo: str | Path) -> FermatSnapshot:
    """Scan a checked-out FLT repository at HEAD without running Lean."""
    root = Path(repo).resolve()
    if not (root / ".git").exists():
        raise ValueError(f"not a git repository: {root}")
    paths = [line.strip() for line in _git(root, "ls-tree", "-r", "--name-only", "HEAD").splitlines() if line.strip()]
    path_set = set(paths)
    required = {"README.md", "NOTICE", "ATTRIBUTION.md", "formalization.yaml",
                "lean-toolchain", "lake-manifest.json", "P2M/Util.lean",
                "tools/docs-site/gen/graphdata.py", "verification/comparator/config.json"}
    missing = sorted(required - path_set)
    if missing:
        raise ValueError(f"FLT snapshot missing required files: {missing}")
    commit = _git(root, "rev-parse", "HEAD").strip()
    toolchain = _blob(root, "lean-toolchain").strip()
    manifest = _blob(root, "lake-manifest.json")
    mathlib_revision = _mathlib_revision(manifest)
    candidates = _candidates(path_set)
    architecture = {
        "theorem_solution_split": {"statements": "Theorems/", "solutions": "P2M/Sol/"},
        "definition_layer": "Definitions/",
        "comparator": ["verification/comparator/Challenge.lean",
                        "verification/comparator/Solution.lean",
                        "verification/comparator/config.json"],
        "graph_pipeline": ["tools/docs-site/gen/extract.py", "tools/docs-site/gen/graphdata.py"],
        "obstruction_tracking": {
            "explicit_in_repo": False,
            "recommended_projection": "preserve every failed comparator/checker attempt as a DAG event; never infer proof from artifact presence",
        },
        "source_hashes": {
            "NOTICE": _sha_text(_blob(root, "NOTICE")),
            "ATTRIBUTION.md": _sha_text(_blob(root, "ATTRIBUTION.md")),
            "formalization.yaml": _sha_text(_blob(root, "formalization.yaml")),
        },
    }
    candidates = tuple(
        replace(candidate, source_commit=commit,
                source_sha256=hashlib.sha256(_blob_bytes(root, candidate.path)).hexdigest(),
                mathlib_revision=mathlib_revision,
                lean_toolchain=toolchain)
        for candidate in candidates
    )
    return FermatSnapshot(
        repository=REPO, commit=commit, lean_toolchain=toolchain,
        mathlib_revision=mathlib_revision, license="Apache-2.0",
        source_counts=_counts(paths), candidates=candidates, architecture=architecture,
    )


def snapshot_to_dict(snapshot: FermatSnapshot) -> dict[str, Any]:
    data = asdict(snapshot)
    data["candidates"] = [asdict(candidate) for candidate in snapshot.candidates]
    data["schema_version"] = SCHEMA
    return data


def write_snapshot(repo: str | Path, output: str | Path) -> FermatSnapshot:
    snapshot = scan_fermats_repo(repo)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot_to_dict(snapshot), ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    return snapshot
