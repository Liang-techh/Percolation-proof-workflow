# Supplemental cached-source snapshots

These two existing source files complete the local source collection for
the nine cached leaf modules imported by the final attempt. Their oleans
were already copied and hashed before each compile. These source copies
were captured afterward; this supplement does not claim that the cached
dependencies were rebuilt in this task. All other local module sources
are in each run's `inputs/examples/` tree.

| Source path relative to workspace | SHA256 |
| --- | --- |
| examples/routeb_supply_core/RouteBSupplyCore.lean | 646c1052c10c1d8606342010c4303c0c25e40e008664ce7f1c1b1649c51f6971 |
| examples/routeb_residual_power/ResidualPower.lean | 0f74bf60dbe7473f4b7f7d78c759a6fbff03ae984bb932f203a31c8c8de7de3d |

Operation: native PowerShell Copy-Item from the named sources into this
new supplement directory, followed by Get-FileHash -Algorithm SHA256.
Source locations were read only; no registry or state was changed.
