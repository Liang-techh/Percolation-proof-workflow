# Implementation report

Implemented the minimal sparse materializer and narrow tests. It accepts only
pre-existing source evidence, validates the EI cell16 address contract, and
writes atomically after the complete input validates. It rejects missing
source/geometry/rho/inverse fields, duplicate addresses, out-of-range
coordinates, and `outward != true`; argparse also rejects an omitted input.

No admission or registry file was changed. This utility reports only the
number of records written; sparse record count is not coverage and does not
promote any Route-B claim.
