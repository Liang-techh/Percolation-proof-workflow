"""Correct a result-field name without rerunning or modifying its math audit.

The preconditioned combined bound is for delta'Ldelta, NOT necessarily r'Qr.
The original mislabelled receipt and exact audited source remain untouched.
"""
import hashlib
import json
from pathlib import Path
import shutil
import sys

run=Path(sys.argv[1]).resolve()
assert 'AUDIT_EXIT_CODE=0' in (run/'terminal.log').read_text(encoding='utf-8')
source=run/'results.json'
result=json.loads(source.read_text(encoding='utf-8'))
assert result['status']=='RATIONAL_CONDITIONAL_PREFIX_SOURCE_ENVELOPE_AUDIT'
assert 'inertia_preconditioning' in result
out=run/'field_name_correction'
out.mkdir(exist_ok=False)
shutil.copy2(Path(__file__),out/'normalize_receipt.py')
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        (source,run/'audit.py',run/'terminal.log',out/'normalize_receipt.py')}
(out/'before_run.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
for record in result['fixed_hypothetical_caps']:
    assert 'delta_energy_integral_upper' not in record
    record['delta_energy_integral_upper']=record.pop('Q_r_integral_upper')
result['receipt_semantics_correction']={
    'original_receipt':str(source),'original_sha256':before[str(source)],
    'reason':'Combined minimum uses preconditioned delta energy and cannot be called a Q(r) upper bound.',
    'numeric_values_recomputed':False,'audit_rerun':False,
    'original_receipt_preserved':True}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(out/'terminal.log').write_text('Only result field name corrected; no numerical value changed.\nNORMALIZATION_EXIT_CODE=0\n',encoding='utf-8')
print('NORMALIZED_RECEIPT',out/'results.json')
