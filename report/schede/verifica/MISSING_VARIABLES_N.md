# Verifica: MISSING_VARIABLES (N)
N001 | NON_TROVATA | — | no issue gives the request's count of surface variables (24 + wind shear)
N002 | NON_TROVATA | — | "22 of 24 delivered" not stated in any issue; #17 only records `10efg`/`10nfg` as excluded by decision
N003 | NON_TROVATA | — | the requested "9 variables" is not in the issues; #19 [corpo] gives the delivered set: "13 variables x 13 levels = 169 messages"
N004 | NON_TROVATA | — | #19 [corpo] lists `cc` `crwc` `cswc` among the 13 pressure-level variables but never calls them the 3 "extra" fields
N005 | NON_TROVATA | — | TKE absent is confirmed (#12, #17, #29); the requested "3 height levels" appears nowhere
N006 | CONFERMATA | #12 [commento 2026-09-19] | "Run is WRF V4.1.1 / WPS 4.1"; header "OUTPUT FROM WRF V4.1.1 MODEL"
N007 | CONFERMATA | #11 [corpo] | "WRF (d02 only, 3 km Mercator, 1641x1353)"
N008 | CONFERMATA | #11 [corpo] | "WRF (d02 only, 3 km Mercator, 1641x1353)"
N009 | CONFERMATA | #18 [commento 2026-09-22]; #33 [commento 2026-09-21] | "From the 49 model levels"; #12 [commento 2026-09-19]: "present in the wrfout on all 49 mass levels"
N014 | CONFERMATA_CON_DIFFERENZE | #25 [corpo]; #12 [commento 2026-09-19] | #25: "`sst` is constant within each 24 h run"; but #12 gives the spinup structure "`start_hour = 18`, `run_hours = 30`", so a run integrates 30 h
N019 | CONFERMATA | #12 [commento 2026-09-19] | "`sf_surface_physics = 3` (RUC), 6 soil nodes at 0/5/20/40/160/300 cm exactly as stated"; also #24 [corpo]
N020 | CONFERMATA | docs/audit/f6-soil-and-snow.md §1 The operator | weight table lists ERA5 layers 1 (0–7 cm) to 4 (100–289 cm); #24 [corpo] names `swvl1-4`/`stl1-4`
N023 | CONFERMATA_CON_DIFFERENZE | #59 [commento 2026-09-28]; #62 [corpo] | `LU_INDEX` vs `IVGTYP`, lake recode excluded: 1.0000 (2019-07-15T12, 2025-01-15T12) but 0.9998 on 2025-02-15T12, not 100.00 % everywhere
N024 | CONFERMATA | #11 [commento 2026-09-19] | "the archive claims exactly seven: `cvl`, `cvh`, `tvl`, `tvh`, `slt`, `cl`, `dl`, all read from the `geo_em.d02` sidecar"; verified invariant in docs/audit/f7 Claim A
N025 | NON_TROVATA | — | #25/#34 mention `SEAICE > 0` only as the ice reclassification of `LANDMASK`, not as a route to a sea-ice surface temperature
N026 | NON_TROVATA | — | no Cd formula in the issues; #18 [commento 2026-09-22] has `u*/κ · ln(10/z0)` only for the 10 m neutral wind `u10n`/`v10n`
N027 | NON_TROVATA | — | no issue mentions ERA5 waves or their resolution; #12 only says no waves (sf_ocean_physics = 0)
N029 | CONFERMATA | #12 [commento 2026-09-19]; #29 [corpo] | "`isfflx = 1` — the surface fluxes exist, they are just not written"
N030 | CONFERMATA | #55 [corpo] (measured); #55 [commento 2026-09-29] | "water gate, `skt` vs SST ... 0.0005 K RMSE, bias −0.0002 K ... on ~910 000 points, every timestep" (corrects the 0.0015 K recorded earlier)
N031 | CONFERMATA | #12 [commento 2026-09-19]; #30 [corpo] | "`output_diagnostics = 0` — no min/max screen-level fields, so no `mx2t`/`mn2t`"
N032 | CONFERMATA | #12 [commento 2026-09-19] §e | "`nwp_diagnostics = 1` — seven fields are per-hour maxima, by configuration"; #49 [corpo] later says the one-hour window fails on 12.3 % of hours
N033 | NON_TROVATA | — | no issue dates the removal (2026-09-17) and reinstatement (2026-09-18) of the soil/type/cover fields
N034 | CONFERMATA | docs/audit/f6-soil-and-snow.md §1 The operator | layers "1 (0–7 cm)", "2 (7–28 cm)", "3 (28–100 cm)", "4 (100–289 cm)"; #24 [corpo]: "ERA5's deepest boundary (289 cm)"
N035 | NON_TROVATA | — | the issues and docs/audit cite the FAO thresholds for `slt` but never the number of ECMWF soil types
N036 | CONFERMATA | #25 [commento 2026-09-22] (measured); #12 [commento 2026-09-19] | "233 844 (17.93 %) with both vegetation types above 5 %"
N037 | CONFERMATA | #12 [commento 2026-09-19] | "The 90.1 % average dominance ... which `CLAUDE.md` reports from geo_em" (reported, not re-measured there)
N038 | NON_TROVATA | — | the 500 × 600 sub-domain is not in the issues; #21 [corpo] has only "18-22% of cloudy points sit exactly at 1"
N041 | CONFERMATA_CON_DIFFERENZE | #55 [corpo] (measured); #55 [commento 2026-09-29] | the source gives 0.0005 K RMSE, not 0.005 K (the earlier recorded value was 0.0015 K)
N042 | NON_TROVATA | — | no issue gives a `skt` vs 0 cm soil RMSE; #24 [commento 2026-09-22] only says `stl1` is not `TSLB[0]`
N043 | CONTRADDETTA | #55 [corpo]; #26 [commento 2026-09-25] | the snow switch is confirmed, not unreconstructable: "the snow switch ... all survive re-measurement"; land RMSE is "0.115–0.133 K (January, February), p99 0.85 K"
N044 | CONTRADDETTA | #19 [commento 2026-09-22] | "the '0.8 % median, 2.2 % at most' ... reproduces at the top (2.26 %) and not in the middle — ... the median is 0.011 % and the p99 is 1.44 %"
N045 | CONFERMATA | #54 [corpo] | "`cape_2d`'s Fortran flags CIN as missing wherever CAPE < 100 J/kg. `dense()` writes zero there"
N046 | NON_TROVATA | — | no issue gives the share of points without an equilibrium level
N047 | CONFERMATA | #26 [commento 2026-09-25] | "ours a 500 m mixed parcel in the lowest 3 km"
N048 | CONFERMATA | #50 [corpo] | "ERA5's is a parameterised gust roughly 1.6 times the mean wind"
N053 | CONFERMATA | #50 [commento 2026-09-29]; #23 [commento 2026-09-25] (measured) | "the hourly maximum adds half a per cent to three per cent"; #23: "by only 0.5 to 3.2 per cent"
N054 | CONFERMATA | #50 [corpo]; #50 [commento 2026-09-29] | "reading it as a gust under-predicts by about 38 %"; measured ratio 0.625 of ERA5's `10fg`
N055 | CONFERMATA_CON_DIFFERENZE | #49 [corpo] (measured) | the source gives the complement: reset missed on "17 (12.3 %)" of 138 transitions; 88 % is not written
N057 | CONFERMATA | docs/audit/f7-static-and-surface.md § `fal` | "the model's own flux ratio `SWUPB/SWDNB` above 50 W/m² of incoming shortwave"
N064 | CONFERMATA | #51 [corpo]; #23 [commento 2026-09-25] | `sro` ours / ERA5 "1.0 to 4.6"
N065 | CONFERMATA | #51 [corpo]; #23 [commento 2026-09-25] | `ssro` ours / ERA5 "0.000 to 0.004"
N066 | CONFERMATA | #51 [corpo]; #23 [commento 2026-09-25] | `ro` ours / ERA5 "0.19 to 0.85"
N067 | CONFERMATA | #47 [corpo]; #47 [commento 2026-09-29] | "ECMWF defines paramId 136 `tcw` ... five species. The converter builds it from six"
N068 | CONFERMATA | #35 [commento 2026-09-29]; #17 [commento 2026-09-22] | "`QGRAUP` (260028 `grle`, 260001 `tcolg`)"; "ERA5 does not publish them"
N069 | CONFERMATA | #47 [corpo]; #47 [commento 2026-09-29] | "In the domain mean it is 0.4 % of the condensate and invisible"
N070 | CONFERMATA | #47 [commento 2026-09-29]; #21 [commento 2026-09-22] | "up to 26.5 kg/m² inside a July convective cell" (#47's title rounds to 26 kg/m2)
N071 | NON_TROVATA | — | issues say GRIB1 wrote `2d` in degC under a K paramId (#15, #20) but never state the +273.15 correction
N072 | NON_TROVATA | — | no issue gives the current geolocation error (~2 m)
N073 | CONFERMATA | #26 [commento 2026-09-25] | "`shapeOfTheEarth = 1` with `radius = 6370000` on all 246 messages"
N074 | CONFERMATA | #26 [corpo] | "without it eccodes derives a grid off by ~1.1 km at the northern edge" (stated in the ticket, not re-measured)
N075 | NON_TROVATA | — | issues mention "the geo_em recovery" (#03, #11, #18) but never date it
N076 | CONFERMATA | #24 [corpo] | "`swvl1-4` / `stl1-4` are integrals, not relabellings"
N077 | CONFERMATA | #20 [commento 2026-09-22] | "`sqrt((100u−10u)² + (100v−10v)²)/90` ... The 10–100 m layer is ours"
N078 | CONFERMATA | #19 [corpo]; #12 [commento 2026-09-19] | "The registry writes 13 pressure levels with 50 hPa at the top"
N079 | NON_TROVATA | — | 37 and 29 appear nowhere; #19 [corpo] says only "the 8 ERA5 levels above 50 hPa are above WRF's `P_TOP`"
N080 | CONFERMATA | #12 [commento 2026-09-19]; #19 [commento 2026-09-19] | "50 hPa is exactly the model" lid; "`p_top_requested = 5000`: 50 hPa is the model lid"
N081 | NON_TROVATA | — | no issue gives file sizes at 13 vs 29 levels (~0.8 / ~1.45 GB)
N082 | NON_TROVATA | — | no issue gives annual archive size at 13 vs 29 levels (7.0 / 18.1 TB)

## Conteggi
CONFERMATA: 33
CONFERMATA_CON_DIFFERENZE: 4
CONTRADDETTA: 2
NON_TROVATA: 19
NON_VERIFICABILE: 0
