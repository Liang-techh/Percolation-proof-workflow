import copy
import hashlib
import subprocess

import pytest

from percolation_workflow.advisory_reuse import (
    AdvisoryReuseError,
    SCHEMA_VERSION,
    project_advisory_reuse,
)


def _catalog(source_root, *, candidates=None):
    return {
        "repository": "https://github.com/anthropics/formal-math",
        "commit": "a" * 40,
        "license": "Apache-2.0",
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "mathlib_revision": "b" * 40,
        "candidates": candidates if candidates is not None else [
            {
                "path": "Theorems/Leaf.lean",
                "sha256": hashlib.sha256(
                    (source_root / "Theorems" / "Leaf.lean").read_bytes()
                ).hexdigest(),
                "kind": "theorem-infra",
                "classification": 1,
                "reuse_mode": "reprove-and-pin",
                "rationale": "typed reusable leaf",
                "current_routeb_use": "advisory adapter candidate",
                "attribution_ref": "formal-math source; Apache-2.0",
            }
        ],
    }


def test_projection_is_hash_bound_advisory_only_and_read_only(tmp_path):
    source = tmp_path / "Theorems" / "Leaf.lean"
    source.parent.mkdir()
    source.write_bytes(b"theorem leaf : True := by trivial\n")
    catalog = _catalog(tmp_path)
    before = copy.deepcopy(catalog)

    projection = project_advisory_reuse(catalog, tmp_path)

    assert projection["schema_version"] == SCHEMA_VERSION
    assert projection["advisory_only"] is True
    assert projection["authoritative"] is False
    assert projection["candidates"][0]["path"] == "Theorems/Leaf.lean"
    assert projection["candidates"][0]["sha256"] == catalog["candidates"][0]["sha256"]
    assert len(projection["catalog_sha256"]) == 64
    assert catalog == before
    assert source.read_bytes() == b"theorem leaf : True := by trivial\n"
    assert not any(
        forbidden in projection
        for forbidden in (
            "registry",
            "verified_registry",
            "dependencies",
            "closure",
            "formal_certificate_allowed",
        )
    )


@pytest.mark.parametrize("field", ["repository", "commit", "license", "lean_toolchain", "mathlib_revision"])
def test_missing_provenance_is_rejected(tmp_path, field):
    source = tmp_path / "Theorems" / "Leaf.lean"
    source.parent.mkdir()
    source.write_bytes(b"leaf\n")
    catalog = _catalog(tmp_path)
    catalog[field] = ""

    with pytest.raises(AdvisoryReuseError, match="missing provenance"):
        project_advisory_reuse(catalog, tmp_path)


def test_missing_source_is_rejected(tmp_path):
    catalog = _catalog(tmp_path, candidates=[{
        "path": "Theorems/Missing.lean",
        "sha256": "0" * 64,
        "attribution_ref": "source",
    }])

    with pytest.raises(AdvisoryReuseError, match="source is missing"):
        project_advisory_reuse(catalog, tmp_path)


def test_stale_source_hash_is_rejected(tmp_path):
    source = tmp_path / "Theorems" / "Leaf.lean"
    source.parent.mkdir()
    source.write_bytes(b"old\n")
    catalog = _catalog(tmp_path)
    source.write_bytes(b"changed\n")

    with pytest.raises(AdvisoryReuseError, match="source is stale"):
        project_advisory_reuse(catalog, tmp_path)


@pytest.mark.parametrize(
    "candidate",
    [
        {"path": "Theorems/Leaf.lean", "sha256": "bad", "attribution_ref": "source"},
        {"path": "../outside.lean", "sha256": "0" * 64, "attribution_ref": "source"},
        {"path": "Theorems/Leaf.lean", "sha256": "0" * 64},
    ],
)
def test_invalid_candidate_is_rejected(tmp_path, candidate):
    source = tmp_path / "Theorems" / "Leaf.lean"
    source.parent.mkdir()
    source.write_bytes(b"leaf\n")
    catalog = _catalog(tmp_path, candidates=[candidate])

    with pytest.raises(AdvisoryReuseError):
        project_advisory_reuse(catalog, tmp_path)


def test_authority_fields_are_rejected_instead_of_dropped(tmp_path):
    source = tmp_path / "Theorems" / "Leaf.lean"
    source.parent.mkdir()
    source.write_bytes(b"leaf\n")
    catalog = _catalog(tmp_path)
    catalog["formal_certificate_allowed"] = False

    with pytest.raises(AdvisoryReuseError, match="forbidden authority field"):
        project_advisory_reuse(catalog, tmp_path)


def test_projection_reads_a_no_checkout_git_head_blob(tmp_path):
    source = tmp_path / "Theorems" / "Leaf.lean"
    source.parent.mkdir()
    source.write_bytes(b"theorem leaf : True := by trivial\n")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"],
                   cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "catalog-test"],
                   cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "Theorems/Leaf.lean"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=tmp_path, check=True)
    catalog = _catalog(tmp_path)
    source.unlink()

    projection = project_advisory_reuse(catalog, tmp_path)

    assert projection["candidates"][0]["path"] == "Theorems/Leaf.lean"
    assert projection["candidates"][0]["sha256"] == catalog["candidates"][0]["sha256"]
