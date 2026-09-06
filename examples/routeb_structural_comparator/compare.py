"""Conservative statement comparator for compiled Route-B sidecars.

This checks declaration identity, source/snapshot identity and required
semantic surface fragments. It is deliberately weaker than Lean elaboration
and the upstream physical comparator, so acceptance here cannot promote a
registry theorem.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'src'))
from percolation_workflow.statements import index_statements


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    return re.sub(r'\s+', ' ', text).strip()


def main():
    side = Path(__file__).resolve().parent
    config = json.loads((side/'comparator.json').read_text(encoding='utf-8'))
    results = []
    for target in config['targets']:
        source = (side/target['source']).resolve()
        snapshot = (side/target['successful_snapshot']).resolve()
        assert source.is_file() and snapshot.is_file()
        current = {d.qualified_name: d for d in index_statements(source)}
        frozen = {d.qualified_name: d for d in index_statements(snapshot)}
        names = target['declarations']
        assert set(names) <= current.keys() and set(names) <= frozen.keys()
        surface = normalized('\n'.join(current[name].source for name in names))
        required_ok = all(fragment in surface for fragment in target['required_statement_fragments'])
        checks = []
        for name in names:
            left, right = normalized(current[name].source), normalized(frozen[name].source)
            checks.append(dict(name=name, current_equals_snapshot=left == right,
                              statement_sha256=hashlib.sha256(left.encode()).hexdigest(),
                              required_fragments=required_ok,
                              current_lines=[current[name].start_line, current[name].end_line]))
        assert all(x['current_equals_snapshot'] and x['required_fragments'] for x in checks)
        results.append(dict(id=target['id'], source=str(source), source_sha256=digest(source),
                            snapshot=str(snapshot), snapshot_sha256=digest(snapshot), checks=checks,
                            structural_match=True))
    result = dict(schema='routeb-structural-statement-comparator-v1',
                  accepted=True, comparator_strength='pre_comparator_only',
                  physical_source_binding=False, upstream_comparator=False,
                  registry_promotion=False, timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  targets=results)
    output = side/'output'
    output.mkdir(exist_ok=True)
    run = output/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    run.mkdir(exist_ok=False)
    (run/'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
