# Preserved targeted attempts

1. `output/run-20260905T200606Z-34dbb987`: exact source-functional audit,
   252 linear functionals and 128 closed time cells. AUDIT_EXIT_CODE=0.
   Conditional ideal-model scalar prefix reaches 33/64, not T=1. Fixed
   hypothetical J budgets 0,1/20,1/4,1 yield Q(r0) integral upper estimates
   1.9286863712881874,15.189523165740288,92.22450353423116,778.6364802592547.
   There was no trajectory integration and no source/FD/Float64 admission.

2. `output/run-20260905T200854Z-88e7c74d`: adds exact source-inverse
   preconditioning and explicitly tests b=1 when geometric proposals jump
   past it. 648 functionals, AUDIT_EXIT_CODE=0. It closes 72 conditional
   analytic cells through 9/16, with J<=26281199249/200000000000. Every
   passed cell used the preconditioned bound. The next [9/16,73/128] gate
   remains unclosed. Whole-horizon hypothetical J=0 and J=1 bounds are
   1.8686818470799766 and 777.3175666626448, not physical lower bounds.

The second run's old Q_r_integral_upper name described a minimum that only
bounds delta'Ldelta. Current source fixes the name. A separate hash-bound
field_name_correction receipt preserves all original bytes and numeric
values without rerunning the expensive identical matrix calculation.
No audited failure, unclosed gate or original result is overwritten.
That normalization completed with NORMALIZATION_EXIT_CODE=0. Its only
data transformation renames the misleading field; current audit.py has
the corresponding field name and console label changes, with no changed
calculation. The corrected current labels were not used to relabel an old
source snapshot as newly executed code.

All executed inputs and scripts are snapshotted before each computation;
the audit runs the snapshots, not mutable originals. Complete terminal logs
are synchronously closed before the wrapper prints them. Only related
mathematics was audited; no browser work or whole-project regression ran.
