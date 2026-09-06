from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from pathlib import Path


@dataclass(frozen=True)
class StatementRecord:
    name: str
    qualified_name: str
    source_file: str
    start_line: int
    end_line: int
    source: str


_decl = re.compile(r"^\s*(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_'.]*)")
_namespace = re.compile(r"^\s*namespace\s+([A-Za-z_][A-Za-z0-9_'.]*)")


def index_statements(path: str | Path) -> list[StatementRecord]:
    """Index trusted statement declarations up to their proof boundary.

    This is a source index, not a proof checker. The returned slice is deliberately marked as source
    evidence; callers must still compile the module and run the final comparator before promotion.
    """
    file = Path(path)
    text = file.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    records: list[StatementRecord] = []
    namespace = ""
    for i, line in enumerate(lines):
        mns = _namespace.match(line)
        if mns:
            namespace = mns.group(1)
        m = _decl.match(line)
        if not m:
            continue
        name = m.group(1)
        end = i
        while end < len(lines) and ":=" not in "".join(lines[i:end + 1]):
            end += 1
        if end == len(lines):
            raise ValueError(f"proof boundary not found for {name} in {file}")
        source = "".join(lines[i:end + 1])
        source = source[:source.find(":=")].rstrip()
        records.append(StatementRecord(name, f"{namespace}.{name}" if namespace else name,
                                        str(file), i + 1, end + 1, source))
    return records


def write_index(path: str | Path, output: str | Path) -> None:
    records = index_statements(path)
    Path(output).write_text(json.dumps([asdict(r) for r in records], ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
