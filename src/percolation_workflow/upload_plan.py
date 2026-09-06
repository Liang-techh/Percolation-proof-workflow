"""Stage-1/Stage-2 upload planning for the Prove2Me-compatible path.

The upstream playbook deliberately separates declaration-level reachability
from source-position facts.  This module keeps that distinction explicit and
turns the two JSONL products into a deterministic, inspectable plan.  It does
not upload anything and it never treats a generated skeleton as proof
evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping


def _position(value: Any, field: str) -> dict[str, int]:
    if not isinstance(value, dict) or any(type(value.get(k)) is not int for k in ("line", "col", "offset")):
        raise ValueError(f"{field} must contain integer line, col and offset")
    if value["line"] < 1 or value["col"] < 0 or value["offset"] < 0:
        raise ValueError(f"{field} contains an invalid position")
    return {k: value[k] for k in ("line", "col", "offset")}


def _range(value: Any, field: str, *, allow_null: bool = True) -> dict[str, Any] | None:
    if value is None and allow_null:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be a range")
    return {"start": _position(value.get("start"), f"{field}.start"),
            "end": _position(value.get("end"), f"{field}.end")}


def _safe_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for raw in rows:
        row = dict(raw)
        if not isinstance(row.get("name"), str) or not row["name"].strip():
            raise ValueError("declaration graph row has no name")
        if row.get("kind") not in {"theorem", "opaque", "def", "inductive", "ctor", "rec", "quot", "axiom"}:
            raise ValueError(f"unsupported declaration kind for {row['name']}")
        for field in ("typeDeps", "valueDeps"):
            if not isinstance(row.get(field, []), list) or any(not isinstance(x, str) for x in row[field]):
                raise ValueError(f"{field} must be a list of names")
        for field in ("startLine", "endLine"):
            if type(row.get(field)) is not int or row[field] < 0:
                raise ValueError(f"{field} must be a nonnegative integer")
        result.append(row)
    if len({row["name"] for row in result}) != len(result):
        raise ValueError("duplicate declaration graph names")
    return result


def _user_suffix(name: str) -> str:
    """Return the stable user-name suffix used to join private Stage-1/2 facts."""
    marker = name.rfind(".")
    # `_private.<file-prefix>.<user-name>` and `_private.<user-name>` both
    # occur in practice.  The project-qualified tail is the stable key; for
    # ordinary names the complete name is already the key.
    if name.startswith("_private."):
        pieces = name.split(".")
        if len(pieces) >= 3:
            return ".".join(pieces[-2:])
    return name


def _same_decl(stage1: Mapping[str, Any], stage2: Mapping[str, Any]) -> bool:
    name = stage2.get("nameText")
    if isinstance(name, str) and name:
        if name == stage1["name"] or name == stage1.get("userName"):
            return True
        if _user_suffix(name) == _user_suffix(str(stage1.get("userName", stage1["name"]))):
            return True
    line = stage1.get("startLine", 0)
    start = stage2.get("declStart", {}).get("line") if isinstance(stage2.get("declStart"), dict) else None
    end = stage2.get("declEnd", {}).get("line") if isinstance(stage2.get("declEnd"), dict) else None
    return type(line) is int and type(start) is int and type(end) is int and start <= line <= end


def join_stage_facts(graph_rows: Iterable[Mapping[str, Any]],
                     sketch_by_module: Mapping[str, Iterable[Mapping[str, Any]]]) -> dict[str, dict[str, Any]]:
    """Join Stage-1 rows to Stage-2 declaration facts by containment.

    Name matching is preferred, but line containment is authoritative for
    wrapped declarations and anonymous instances.  An ambiguous or missing
    join fails closed rather than silently generating a wrong proof cut.
    """
    rows = _safe_rows(graph_rows)
    facts: dict[str, dict[str, Any]] = {}
    for row in rows:
        module = str(row.get("module", ""))
        candidates = []
        module_facts = [fact for fact in sketch_by_module.get(module, [])
                        if isinstance(fact, dict)]
        for fact in module_facts:
            if not isinstance(fact, dict) or fact.get("kind") != "decl":
                continue
            start = _position(fact.get("declStart"), f"{module}.declStart")
            end = _position(fact.get("declEnd"), f"{module}.declEnd")
            if start["line"] <= row["startLine"] <= end["line"]:
                if _same_decl(row, fact):
                    candidates.append((fact, start, end))
        if len(candidates) != 1:
            raise ValueError(f"Stage-1 declaration has {len(candidates)} Stage-2 joins: {row['name']}")
        fact, start, end = candidates[0]
        val = _position(fact.get("valStart"), f"{row['name']}.valStart") if fact.get("valStart") is not None else None
        doc = _range(fact.get("docstring"), f"{row['name']}.docstring")
        private = _range(fact.get("privateTok"), f"{row['name']}.privateTok")
        references = []
        for reference in module_facts:
            if reference.get("kind") != "ref":
                continue
            ref_start = _position(reference.get("start"), f"{row['name']}.ref.start")
            ref_end = _position(reference.get("end"), f"{row['name']}.ref.end")
            if start["offset"] <= ref_start["offset"] and ref_end["offset"] <= end["offset"]:
                references.append(dict(reference))
        facts[row["name"]] = {"module": module, "source_fact": dict(fact),
                               "decl_start": start, "decl_end": end,
                               "val_start": val, "docstring": doc, "private_tok": private,
                               "references": references}
    return facts


def reachable_declarations(graph_rows: Iterable[Mapping[str, Any]], roots: Iterable[str]) -> set[str]:
    """Compute reachability before dropping spanless compiler companions."""
    rows = _safe_rows(graph_rows)
    by_name = {row["name"]: row for row in rows}
    roots = list(roots)
    if not roots or any(root not in by_name for root in roots):
        raise ValueError("all upload roots must occur in the declaration graph")
    instance_roots = [row["name"] for row in rows if row.get("isInstance") is True]
    reached: set[str] = set()
    work = roots + instance_roots
    while work:
        name = work.pop()
        if name in reached or name not in by_name:
            continue
        reached.add(name)
        row = by_name[name]
        work.extend(row.get("typeDeps", []))
        work.extend(row.get("valueDeps", []))
        if row.get("kind") == "inductive":
            work.extend(child["name"] for child in rows
                        if child.get("kind") == "ctor" and child["name"].startswith(name + "."))
    return reached


def _span_contains(outer: Mapping[str, Any], inner: Mapping[str, Any]) -> bool:
    return (outer["decl_start"]["offset"] <= inner["decl_start"]["offset"]
            and inner["decl_end"]["offset"] <= outer["decl_end"]["offset"])


def _proof_users(rows: list[dict[str, Any]], selected: set[str]) -> dict[str, set[str]]:
    users: dict[str, set[str]] = {name: set() for name in selected}
    for row in rows:
        for dep in row.get("valueDeps", []):
            if dep in users:
                users[dep].add(row["name"])
    return users


def build_upload_plan(graph_rows: Iterable[Mapping[str, Any]],
                      sketch_by_module: Mapping[str, Iterable[Mapping[str, Any]]],
                      roots: Iterable[str], *, force_nodes: Iterable[str] = (),
                      source_paper_names: Iterable[str] = (),
                      source_root: str | Path | None = None,
                      module_paths: Mapping[str, str | Path] | None = None) -> dict[str, Any]:
    """Build the deterministic Phase-2/3 plan consumed by a future generator."""
    rows = _safe_rows(graph_rows)
    by_name = {row["name"]: row for row in rows}
    reached = reachable_declarations(rows, roots)
    selected = {name for name in reached if by_name[name].get("startLine", 0) != 0}
    facts = join_stage_facts([row for row in rows if row["name"] in selected], sketch_by_module)
    force = set(force_nodes)
    paper = set(source_paper_names)
    users = _proof_users(rows, selected)
    def_material = {name for name in selected if by_name[name].get("kind") not in {"theorem", "opaque"}}
    node_names = set(roots) | {
        name for name in selected if by_name[name].get("kind") in {"theorem", "opaque"}
        and by_name[name].get("isPrivate") is not True
        and (name in force or name in paper or facts[name]["docstring"] is not None
             or len(users[name]) >= 2 or len(users[name] & set(by_name)) >= 1
             or (facts[name]["val_start"] is not None and
                 facts[name]["decl_end"]["line"] - facts[name]["val_start"]["line"] > 40))
    }
    # A declaration whose span is contained in Def-material belongs to that
    # bundle, even if the environment labels it theorem-like (structure field
    # accessors are the important case).
    for name in list(node_names):
        if name in def_material:
            continue
        if any(_span_contains(facts[outer], facts[name]) for outer in def_material
               if outer in facts and name in facts and outer != name):
            node_names.discard(name)
    modules: dict[str, dict[str, Any]] = {}
    for name in sorted(selected):
        fact = facts[name]
        row = by_name[name]
        if row.get("kind") in {"theorem", "opaque"}:
            destination = "theorem_node" if name in node_names else "inline_helper"
        else:
            destination = "definition_material"
        module = fact["module"]
        modules.setdefault(module, {"declarations": [], "source_digest": None,
                                    "source_path": None})["declarations"].append(name)
    source_base = Path(source_root).resolve() if source_root is not None else None
    for module, record in modules.items():
        source_value = (module_paths or {}).get(module) if module_paths is not None else None
        source_path = Path(source_value).resolve() if source_value is not None else None
        if source_path is None and source_base is not None:
            source_path = (source_base / (module.replace('.', '/') + '.lean')).resolve()
        if source_path is not None:
            if not source_path.is_file() or (source_base is not None and not source_path.is_relative_to(source_base)):
                raise ValueError(f"module source is missing or outside source_root: {module}")
            record["source_digest"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
            record["source_path"] = (source_path.relative_to(source_base).as_posix()
                                      if source_base is not None else source_path.name)
    plan_rows = []
    for name in sorted(selected):
        row = by_name[name]
        fact = facts[name]
        signals = []
        if name in roots: signals.append("target")
        if name in force: signals.append("forced")
        if name in paper: signals.append("source_paper")
        if fact["docstring"] is not None: signals.append("docstring")
        if len(users[name]) >= 2: signals.append("used_by_two_proofs")
        if len(users[name] & set(by_name)) >= 1: signals.append("used_in_project_proof")
        plan_rows.append({"name": name, "module": fact["module"], "kind": row["kind"],
                          "destination": ("theorem_node" if name in node_names else
                                          "definition_material" if name in def_material else "inline_helper"),
                          "node": name in node_names, "proof_users": sorted(users[name]),
                          "dependencies": sorted(dep for dep in row.get("valueDeps", [])
                                                   if dep in selected),
                          "promotion_signals": signals, "fact": fact})
    graph_digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    return {"schema_version": 1, "algorithm": "prove2me_upload_plan/v1",
            "graph_sha256": graph_digest, "roots": list(roots),
            "reachable": sorted(reached), "spanless_dropped": sorted(reached - selected),
            "nodes": plan_rows, "definition_modules": modules}


def _topological(names: Iterable[str], dependencies: Mapping[str, Iterable[str]]) -> list[str]:
    names = list(dict.fromkeys(names))
    known = set(names)
    incoming = {name: {dep for dep in dependencies.get(name, []) if dep in known}
                for name in names}
    result = []
    while incoming:
        ready = sorted(name for name, deps in incoming.items() if not deps)
        if not ready:
            raise ValueError("upload dependency graph contains a cycle")
        result.extend(ready)
        for name in ready:
            incoming.pop(name)
        for deps in incoming.values():
            deps.difference_update(ready)
    return result


def ordered_upload_actions(plan: Mapping[str, Any], *,
                           definition_imports: Mapping[str, Iterable[str]] | None = None) -> list[dict[str, Any]]:
    """Create the provider-neutral, leaves-first Phase-7 action order.

    Definitions are bundled by source module and ordered by their import
    dependencies.  Theorems and their solutions are then ordered over the
    selected theorem-node value edges, with every theorem stub submitted before
    any solution verification.  A remote transport/ledger can consume these
    immutable action keys and resume independently; this function performs no
    network mutation.
    """
    if plan.get("schema_version") != 1 or not isinstance(plan.get("nodes"), list):
        raise ValueError("malformed upload plan")
    rows = {row.get("name"): row for row in plan["nodes"]
            if isinstance(row, dict) and isinstance(row.get("name"), str)}
    if len(rows) != len(plan["nodes"]):
        raise ValueError("upload plan contains duplicate or malformed nodes")
    defs = sorted({row["module"] for row in rows.values()
                   if row.get("destination") == "definition_material"})
    imports = definition_imports or {}
    def_deps = {module: list(imports.get(module, [])) for module in defs}
    def_order = _topological(defs, def_deps)
    theorem_names = [name for name, row in rows.items() if row.get("destination") == "theorem_node"]
    theorem_deps = {name: [dep for dep in row.get("dependencies", [])
                           if dep in theorem_names]
                    for name, row in rows.items() if name in theorem_names}
    theorem_order = _topological(theorem_names, theorem_deps)
    actions = []
    for module in def_order:
        actions.append({"key": f"definition:{module}", "kind": "submit_definition",
                        "module": module,
                        "depends_on": [f"definition:{dep}" for dep in def_deps[module]]})
    for name in theorem_order:
        actions.append({"key": f"theorem:{name}", "kind": "submit_theorem",
                        "name": name,
                        "depends_on": [f"theorem:{dep}" for dep in theorem_deps[name]]})
    for name in theorem_order:
        # Verification is addressed by theorem_id, so the corresponding stub
        # must be published before its solution is sent.  Keep the theorem's
        # own publication in the dependency context even for a leaf.
        solution_deps = [f"theorem:{name}"]
        actions.append({"key": f"solution:{name}", "kind": "verify_solution",
                        "name": name, "depends_on": solution_deps})
    return actions


def _byte_cut(source: bytes, position: Mapping[str, Any]) -> int:
    offset = position["offset"]
    if offset > len(source):
        raise ValueError("position offset exceeds source bytes")
    return offset


def proof_stub(source: str | bytes, fact: Mapping[str, Any]) -> str:
    """Cut exactly at Stage-2 ``valStart``; never search for ``:=``."""
    raw = source.encode("utf-8") if isinstance(source, str) else source
    val = fact.get("val_start")
    if val is None:
        raise ValueError("declaration has no proof/value start")
    cut = _byte_cut(raw, val)
    return (raw[:cut] + b":= by sorry").decode("utf-8")


def _reference_edits(raw: bytes, references: Iterable[Mapping[str, Any]],
                     rename_map: Mapping[str, str], *, offset_base: int = 0) -> list[tuple[int, int, bytes]]:
    edits: list[tuple[int, int, bytes]] = []
    for reference in references:
        start = reference.get("start", {}).get("offset")
        end = reference.get("end", {}).get("offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("reference range has no integer offsets")
        start -= offset_base
        end -= offset_base
        if not (0 <= start <= end <= len(raw)):
            raise ValueError("reference range is outside source bytes")
        constant = reference.get("const")
        if not isinstance(constant, str):
            continue
        spelling = raw[start:end].decode("utf-8")
        replacement = None
        for old, new in rename_map.items():
            if not isinstance(old, str) or not isinstance(new, str) or not new:
                raise ValueError("reference rename map contains a malformed name")
            old_leaf = old.rsplit(".", 1)[-1]
            if (constant == old or constant.endswith("." + old_leaf) or
                    spelling == old or spelling == old_leaf or
                    spelling.endswith("." + old_leaf)):
                replacement = new if "." in spelling else new.rsplit(".", 1)[-1]
                break
        if replacement is not None:
            edits.append((start, end, replacement.encode("utf-8")))
    return edits


def rewrite_reference_ranges(source: str | bytes, references: Iterable[Mapping[str, Any]],
                             rename_map: Mapping[str, str]) -> str:
    """Rename elaborator-reported references without searching source text.

    Stage 2 reports the exact byte range of both binding and use occurrences.
    A qualified occurrence keeps the qualified replacement; a short occurrence
    receives only the replacement's final identifier component.  References
    that do not match ``rename_map`` are left untouched, while malformed or
    overlapping ranges fail closed.
    """
    raw = source.encode("utf-8") if isinstance(source, str) else source
    edits = _reference_edits(raw, references, rename_map)
    edits.sort(key=lambda item: item[0], reverse=True)
    previous_start = len(raw) + 1
    for start, end, replacement in edits:
        if end > previous_start:
            raise ValueError("overlapping reference ranges require disambiguation")
        raw = raw[:start] + replacement + raw[end:]
        previous_start = start
    return raw.decode("utf-8")


def skeleton_subtract(source: str | bytes, spans: Iterable[Mapping[str, Any]]) -> str:
    """Delete whole declaration spans by byte offsets, right-to-left."""
    raw = source.encode("utf-8") if isinstance(source, str) else source
    intervals = []
    for fact in spans:
        start = fact["decl_start"]["offset"]
        end = fact["decl_end"]["offset"]
        if not (0 <= start <= end <= len(raw)):
            raise ValueError("declaration span is outside source")
        intervals.append((start, end))
    intervals.sort(reverse=True)
    last = len(raw) + 1
    for start, end in intervals:
        if end > last:
            raise ValueError("overlapping declaration spans require command-level collapse")
        last = start
        raw = raw[:start] + raw[end:]
    return raw.decode("utf-8")


def _apply_byte_edits(raw: bytes, edits: Iterable[tuple[int, int, bytes]]) -> bytes:
    ordered = sorted(edits, key=lambda item: item[0], reverse=True)
    previous_start = len(raw) + 1
    for start, end, replacement in ordered:
        if not (0 <= start <= end <= len(raw)):
            raise ValueError("byte edit is outside source")
        if end > previous_start:
            raise ValueError("overlapping byte edits require command-level collapse")
        raw = raw[:start] + replacement + raw[end:]
        previous_start = start
    return raw


def _fact_span(fact: Mapping[str, Any]) -> tuple[int, int]:
    start = fact["decl_start"]["offset"]
    end = fact["decl_end"]["offset"]
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("declaration fact has malformed byte span")
    return start, end


def _top_level_facts(facts_by_name: Mapping[str, Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    """Collapse generated accessors/constructors whose command span is nested."""
    items = list(facts_by_name.items())
    groups: dict[tuple[int, int], list[tuple[str, Mapping[str, Any]]]] = {}
    for name, fact in items:
        groups.setdefault(_fact_span(fact), []).append((name, fact))
    result = {}
    for span, group in groups.items():
        if any(other_span != span and outer_start <= span[0] and span[1] <= outer_end
               for other_span in groups
               for outer_start, outer_end in [other_span]):
            continue
        # Several generated declarations can share the source command span.
        # Prefer the declaration whose Stage-2 name is the actual source name;
        # otherwise choose the shortest stable name, which keeps the outer
        # inductive/structure instead of a generated accessor.
        exact = [item for item in group
                 if item[1].get("source_fact", {}).get("nameText") == item[0].rsplit(".", 1)[-1]]
        name, fact = min(exact or group, key=lambda item: (len(item[0].split(".")), len(item[0])))
        result[name] = fact
    return result


def _docstring_edit(fact: Mapping[str, Any], *, offset_base: int = 0) -> tuple[int, int, bytes] | None:
    doc = fact.get("docstring")
    if doc is None:
        return None
    return (doc["start"]["offset"] - offset_base,
            doc["end"]["offset"] - offset_base, b"")


def _platform_theorem_keyword(raw: bytes) -> bytes:
    """Promote the source ``lemma`` command to the platform's ``theorem`` form."""
    text = raw.decode("utf-8")
    index = 0
    while index < len(text) and text[index].isspace():
        index += 1
    if text.startswith("private", index) and (index + 7 == len(text) or
                                               not (text[index + 7].isalnum() or text[index + 7] == "_")):
        index += 7
        while index < len(text) and text[index].isspace():
            index += 1
    if not (text.startswith("lemma", index) and
            (index + 5 == len(text) or not (text[index + 5].isalnum() or text[index + 5] == "_"))):
        return raw
    return raw[:index] + b"theorem" + raw[index + len("lemma"):]


_EMPTY_NAMESPACE = re.compile(
    rb"(?m)^[ \t]*namespace[ \t]+[A-Za-z_][A-Za-z0-9_.]*[ \t]*\r?\n"
    rb"(?:[ \t]*\r?\n)*^[ \t]*end(?:[ \t]+[A-Za-z_][A-Za-z0-9_.]*)?[ \t]*(?:\r?\n|$)"
)


def _drop_empty_namespaces(raw: bytes) -> bytes:
    """Remove namespace commands left empty by declaration subtraction.

    This only removes a namespace whose body is whitespace.  It does not infer
    or rewrite lexical context containing declarations, variables, notation,
    or attributes; those contexts remain visible to Lean's build gate.
    """
    return _EMPTY_NAMESPACE.sub(b"", raw)


def _hoisted_section_binders(raw: bytes, target_start: int) -> str:
    """Copy active section/namespace context commands needed by an extracted target.

    Stage 2 reports declaration spans, not the lexical section context around
    them.  A solution moved outside its original ``section`` therefore needs
    the active ``variable``/``include``/``omit`` commands reintroduced before
    the top-level theorem.  This deliberately handles context commands only;
    notation and local attributes remain a Lean build-time diagnostic rather
    than an unsafe guessed rewrite.
    """
    stack: list[str] = []
    captured: list[str] = []
    seen: set[str] = set()
    for line in raw[:target_start].splitlines(keepends=True):
        text = line.decode("utf-8")
        stripped = text.strip()
        if re.match(r"^(?:section|namespace)\b", stripped):
            stack.append(stripped.split(None, 1)[0])
            continue
        if re.match(r"^end(?:\s|$)", stripped):
            if stack:
                stack.pop()
            continue
        if stack and re.match(r"^(?:variable|include|omit)\b", stripped):
            if text not in seen:
                captured.append(text)
                seen.add(text)
    return "".join(captured)


def generate_definition_module(source: str | bytes, facts_by_name: Mapping[str, Mapping[str, Any]],
                               keep_names: Iterable[str]) -> str:
    """Delete every non-definition declaration using original Stage-2 spans."""
    keep = set(keep_names)
    unknown = keep - set(facts_by_name)
    if unknown:
        raise ValueError(f"definition bundle references unknown declarations: {sorted(unknown)}")
    raw = source.encode("utf-8") if isinstance(source, str) else source
    edits = []
    for name, fact in _top_level_facts(facts_by_name).items():
        if name not in keep:
            start, end = _fact_span(fact)
            edits.append((start, end, b""))
    return _apply_byte_edits(raw, edits).decode("utf-8")


def generate_theorem_stub(source: str | bytes, facts_by_name: Mapping[str, Mapping[str, Any]],
                          theorem_name: str) -> str:
    """Keep one theorem statement and cut its proof at Stage-2 ``valStart``."""
    if theorem_name not in facts_by_name:
        raise ValueError(f"unknown theorem declaration: {theorem_name}")
    raw = source.encode("utf-8") if isinstance(source, str) else source
    target_start, target_end = _fact_span(facts_by_name[theorem_name])
    target_raw = raw[target_start:target_end]
    target_edits: list[tuple[int, int, bytes]] = []
    val = facts_by_name[theorem_name].get("val_start")
    if val is None:
        raise ValueError(f"theorem declaration has no proof boundary: {theorem_name}")
    target_edits.append((val["offset"] - target_start,
                         target_end - target_start, b":= by sorry"))
    doc_edit = _docstring_edit(facts_by_name[theorem_name], offset_base=target_start)
    if doc_edit is not None:
        target_edits.append(doc_edit)
    # Rewrite the keyword while the target is still an isolated original-span
    # slice.  Doing this after global deletion would leave the Stage-2 offsets
    # valid only by accident, and applying it to the whole file misses a
    # `lemma` nested under imports/namespace commands.
    target_raw = _platform_theorem_keyword(_apply_byte_edits(target_raw, target_edits))
    edits = []
    for name, fact in _top_level_facts(facts_by_name).items():
        start, end = _fact_span(fact)
        if name != theorem_name:
            edits.append((start, end, b""))
    edits.append((target_start, target_end, target_raw))
    return _apply_byte_edits(raw, edits).decode("utf-8")


def generate_solution_module(source: str | bytes, facts_by_name: Mapping[str, Mapping[str, Any]],
                             theorem_name: str, inline_names: Iterable[str] = (), *,
                             namespace_prefix: str | None = None) -> str:
    """Keep inline helpers, move one proved declaration to top-level ``solution``.

    All deletion and renaming ranges originate in Stage 2.  The target is
    removed from its original namespace block and appended after the retained
    source, so the required top-level theorem name is never created by a text
    search.  Active section/namespace variable context is copied into the
    generated preamble; notation and local attributes remain authoritative
    Lean build diagnostics rather than guessed source rewrites.
    """
    if theorem_name not in facts_by_name:
        raise ValueError(f"unknown theorem declaration: {theorem_name}")
    inline = set(inline_names)
    unknown = inline - set(facts_by_name)
    if unknown:
        raise ValueError(f"solution references unknown inline declarations: {sorted(unknown)}")
    raw = source.encode("utf-8") if isinstance(source, str) else source
    target = facts_by_name[theorem_name]
    target_start, target_end = _fact_span(target)
    target_raw = raw[target_start:target_end]
    target_edits: list[tuple[int, int, bytes]] = []
    doc_edit = _docstring_edit(target, offset_base=target_start)
    if doc_edit is not None:
        target_edits.append(doc_edit)
    private = target.get("private_tok")
    if private is not None:
        target_edits.append((private["start"]["offset"] - target_start,
                             private["end"]["offset"] - target_start, b""))
    target_edits.extend(_reference_edits(
        target_raw, target.get("references", []), {theorem_name: "solution"},
        offset_base=target_start))
    target_raw = _apply_byte_edits(target_raw, target_edits)
    # A Stage-2 docstring range ends before its physical line ending.  Once
    # that line is removed, discard the now-leading blank line before adding
    # the platform's ``open … in`` wrapper.
    target_raw = target_raw.lstrip(b"\r\n")
    edits = []
    for name, fact in _top_level_facts(facts_by_name).items():
        if name == theorem_name or name not in inline:
            start, end = _fact_span(fact)
            edits.append((start, end, b""))
    result = _drop_empty_namespaces(_apply_byte_edits(raw, edits)).decode("utf-8")
    if result and not result.endswith("\n"):
        result += "\n"
    hoisted = _hoisted_section_binders(raw, target_start)
    prefix = f"open {namespace_prefix}\n" if namespace_prefix and hoisted else ""
    prefix += hoisted
    prefix += f"open {namespace_prefix} in\n" if namespace_prefix else ""
    target_text = _platform_theorem_keyword(target_raw).decode("utf-8")
    return result + prefix + target_text


def generate_skeleton(source: str | bytes, facts_by_name: Mapping[str, Mapping[str, Any]],
                     keep_names: Iterable[str], *, stub_names: Iterable[str] = ()) -> str:
    """Generate a source skeleton using only Stage-2 byte ranges.

    ``keep_names`` are retained declarations; every other declaration fact is
    removed as a whole command.  A retained name in ``stub_names`` keeps its
    statement and replaces everything from ``valStart`` through ``declEnd``
    with ``:= by sorry``.  Offsets are all measured against the original bytes,
    so edits are applied right-to-left and cannot drift after a UTF-8 edit.
    """
    raw = source.encode("utf-8") if isinstance(source, str) else source
    keep = set(keep_names)
    stubs = set(stub_names)
    unknown = (keep | stubs) - set(facts_by_name)
    if unknown:
        raise ValueError(f"skeleton references unknown declaration facts: {sorted(unknown)}")
    edits: list[tuple[int, int, bytes]] = []
    for name, fact in facts_by_name.items():
        start = fact["decl_start"]["offset"]
        end = fact["decl_end"]["offset"]
        if name not in keep:
            edits.append((start, end, b""))
        elif name in stubs:
            val = fact.get("val_start")
            if val is None:
                raise ValueError(f"stub declaration has no Stage-2 valStart: {name}")
            edits.append((val["offset"], end, b":= by sorry"))
    edits.sort(key=lambda item: item[0], reverse=True)
    previous_start = len(raw) + 1
    for start, end, replacement in edits:
        if not (0 <= start <= end <= len(raw)):
            raise ValueError("skeleton edit is outside source")
        if end > previous_start:
            raise ValueError("overlapping Stage-2 declaration edits")
        raw = raw[:start] + replacement + raw[end:]
        previous_start = start
    return raw.decode("utf-8")


_IMPORT_LINE = re.compile(r"^(?P<indent>[ \t]*)import[ \t]+(?P<module>[A-Za-z_][A-Za-z0-9_.]*)(?P<tail>[ \t]*(?:--.*)?)\r?\n?$")


def rewrite_imports(source: str, replacements: Mapping[str, str | Iterable[str]], *,
                    extra_imports: Iterable[str] = ()) -> str:
    """Rewrite only complete Lean import lines, preserving all other text.

    The caller supplies the project-module mapping produced by the upload
    plan.  ``extra_imports`` is inserted immediately before the first
    non-import line, which is the safe place for the transitive non-project
    import union required by the upstream playbook.
    """
    normalized: dict[str, list[str]] = {}
    for old, new in replacements.items():
        values = [new] if isinstance(new, str) else list(new)
        if (not isinstance(old, str) or not old.strip() or not values or
                any(not isinstance(value, str) or not value.strip() for value in values)):
            raise ValueError("import replacement names must be nonempty strings")
        normalized[old] = values
    extras = []
    for value in extra_imports:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("extra import names must be nonempty strings")
        if value not in extras:
            extras.append(value)
    lines = source.splitlines(keepends=True)
    present = set()
    for line in lines:
        match = _IMPORT_LINE.match(line)
        if match is not None:
            present.add(match.group("module"))
            present.update(normalized.get(match.group("module"), ()))
    extras = [module for module in extras if module not in present]
    output: list[str] = []
    inserted = False
    for line in lines:
        match = _IMPORT_LINE.match(line)
        if match is None and not inserted:
            for module in extras:
                output.append(f"import {module}\n")
            inserted = True
        if match is not None and match.group("module") in normalized:
            newline = "\n" if line.endswith("\n") else ""
            for module in normalized[match.group("module")]:
                output.append(f"{match.group('indent')}import {module}{match.group('tail')}{newline}")
        else:
            output.append(line)
    if not inserted:
        for module in extras:
            output.append(f"import {module}\n")
    return "".join(output)


def _canonical_type(value: str) -> str:
    """Canonicalize only Lean's printed universe display names."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("elaborated type must be a nonempty string")
    names: dict[str, str] = {}
    next_id = 0
    def replace(match: re.Match[str]) -> str:
        nonlocal next_id
        token = match.group(0)
        if token not in names:
            names[token] = f"u_{next_id}"
            next_id += 1
        return names[token]
    return re.sub(r"\bu_[0-9]+\b", replace, value)


def compare_elaborated_types(original_rows: Iterable[Mapping[str, Any]],
                             staged_rows: Iterable[Mapping[str, Any]], *,
                             rename_map: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Compare the exact elaborated types required by the upload playbook.

    The comparison is intentionally narrower than a pretty-printer diff:
    universe display names are alpha-renamed by occurrence, while every other
    character in the elaborated type must agree.  The result is a report, not
    proof evidence, and callers must gate generation/upload on ``ok``.
    """
    def collect(rows: Iterable[Mapping[str, Any]]) -> dict[str, str]:
        result = {}
        for row in rows:
            name = row.get("name")
            if not isinstance(name, str) or not name.strip() or name in result:
                raise ValueError("elaborated type rows have duplicate or missing names")
            result[name] = _canonical_type(row.get("type"))
        return result
    original = collect(original_rows)
    staged = collect(staged_rows)
    mapping = dict(rename_map or {})
    expected_names = {mapping.get(name, name) for name in original}
    missing = sorted(expected_names - set(staged))
    unexpected = sorted(set(staged) - expected_names)
    mismatches = []
    for source_name in sorted(original):
        staged_name = mapping.get(source_name, source_name)
        if staged_name in staged and original[source_name] != staged[staged_name]:
            mismatches.append({"name": source_name, "staged_name": staged_name,
                               "original": original[source_name], "staged": staged[staged_name]})
    return {"schema_version": 1, "algorithm": "elaborated_type_diff/v1", "ok": not (missing or unexpected or mismatches),
            "missing": missing, "unexpected": unexpected, "mismatches": mismatches,
            "original_sha256": hashlib.sha256(json.dumps(original, sort_keys=True).encode()).hexdigest(),
            "staged_sha256": hashlib.sha256(json.dumps(staged, sort_keys=True).encode()).hexdigest()}


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"JSONL row is not an object: {path}")
            rows.append(value)
    return rows


__all__ = ["build_upload_plan", "compare_elaborated_types", "generate_definition_module",
           "generate_solution_module", "generate_skeleton", "generate_theorem_stub",
           "join_stage_facts", "load_jsonl", "ordered_upload_actions", "proof_stub",
           "reachable_declarations", "rewrite_imports", "rewrite_reference_ranges",
           "skeleton_subtract"]
