# Verifica: CHAPTER_VARIABLES (A)
A004 | NON_VERIFICABILE | #31 corpo; #18 corpo | Document update date. The geo_em recovery is attested ("recoverable, and already recovered — `geo_em.d02`"), but no issue gives the 2026-09-18 date or LRZ as the source.
A005 | NON_TROVATA | #18 corpo | No source says geo_em was "recorded as lost". #18 says instead the fields "were unlocked by a file nobody had looked for".
A008 | NON_VERIFICABILE | — | Statement about the document/schema history ("nothing was removed"); no issue states it in these terms.
A009 | NON_VERIFICABILE | — | Editorial claim of the document, not a measurable fact.
A010 | CONFERMATA | #17 corpo | "a mapping is published only if the WRF quantity **is** the ERA5 one, or the difference states in one line"
A011 | CONFERMATA | #17 corpo; docs/audit/exclusions.md | Same publication rule; exclusions re-tested one line each, "Reason holds".
A014 | CONFERMATA | #12 corpo; #11 corpo | "Run is WRF V4.1.1 / WPS 4.1"; "WRF (d02 only, 3 km Mercator, 1641x1353)"
A015 | CONFERMATA | #11 corpo; #15 corpo | "WRF (d02 only, 3 km Mercator, 1641x1353)"; "The WRF grid is Mercator"
A019 | CONFERMATA_CON_DIFFERENZE | #11 corpo; #14 corpo | "GRIB2 with ECMWF paramIds"; "The harness must match on `paramId`". "Directly comparable" is not stated: #14 notes ERA5 (ed. 1) and CHAPTER (ed. 2) use different level types.
A020 | NON_TROVATA | — | No issue states one file per hour with a size "measured, not estimated".
A021 | CONFERMATA | #13 corpo | "`ailam-an-cima-3km-<yyyy>-<yyyy>-1h-v1-<yyyymmdd><hh>.grib`"
A022 | CONFERMATA_CON_DIFFERENZE | #59 corpo; #64 corpo | Only the 2025 end is attested: "it ends 2025-07-02 (`7b2e2ce`)". #64 says "2020–2024 ... are not in the target window". No source gives the 2019/2024 coverage or "2020–2023 to follow".
A025 | CONFERMATA | #19 corpo | "The 13 levels are the ERA5 set truncated at the model top: the 8 ERA5 levels above 50 hPa are above WRF's `P_TOP`"
A027 | CONFERMATA_CON_DIFFERENZE | #20 corpo; #21 corpo/commento; #22 commento | `heightAboveGround` (incl. `200u`/`200v`), `entireAtmosphere`, and "`nominalTop` for the five TOA fields" are attested. `meanSea` is not found in any source.
A028 | CONFERMATA_CON_DIFFERENZE | #15 corpo | "instantaneous ones with `dataDate`/`dataTime` = valid time". PDT 0 is not named in any source.
A030 | CONFERMATA | #23 commento 2026-09-25 | "Accumulations: PDT 8, `typeOfStatisticalProcessing` 1, reference 00Z, `0-H`, `lengthOfTimeRange` H."
A031 | CONFERMATA | #23 commento 2026-09-25; #22 commento | "Exactly zero at 00Z, all six fields, all 16 00Z files: max 0.0, min 0.0"
A032 | CONFERMATA | #23 commento 2026-09-25 | "`10fg`: PDT 8, `typeOfStatisticalProcessing` 2, reference H−1 ..., `0-1`". Note #49: the declared window is wrong on 17 of 138 transitions (12 %).
A033 | CONFERMATA | #50 corpo; #23 corpo | "It is the maximum of the *resolved* 10 m wind, not a gust parameterisation."
A034 | CONFERMATA | #15 corpo; #22 corpo | accumulated "reference time = 00Z ... step `0-H`", instantaneous "`dataDate`/`dataTime` = valid time", `10fg` "reference time H-1"
A035 | CONFERMATA | #22 corpo; #14 commento | "`validityDate`/`validityTime` still resolve to the timestep, so index on validity and never on `dataTime`."
A036 | CONTRADDETTA | #53 corpo + commento 2026-09-29 | "All 246" messages carry 128 (eccodes GRIB2 default): "inside `grib_v3` the value discriminates nothing". The fix (487ba14) touched only CLAUDE.md and the converter.
A037 | NON_VERIFICABILE | — | Count of rows in the document's own table of declared approximations.
A038 | CONFERMATA_CON_DIFFERENZE | #37 corpo; #25 commento | "paramId 163 is defined as the slope of the **sub-grid** orography". The form-drag qualification is not in any source.
A039 | CONFERMATA | #37 corpo | "`slor` is published as \|∇z\| of the **resolved** 3 km terrain"
A041 | CONFERMATA | #37 corpo; #25 commento | "`sdor` **is** the ERA5 quantity, evaluated on a 3 km cell instead of a 31 km one"
A042 | CONFERMATA | #37 corpo; #25 commento | "the measured ratio of medians is 0.244 = (3/31)^0.605 ... only one of them is a rescaling"
A043 | CONFERMATA_CON_DIFFERENZE | #50 corpo | "ERA5's is a parameterised gust"; ours is the resolved 10 m wind maximum. The "turbulent + convective" decomposition is not found.
A044 | CONFERMATA | #26 commento 2026-09-25 | "`|τ| = ρu*²` ... the stress is aligned with `U10` ... The alignment is the one thing that is ours"
A045 | CONFERMATA | #56 corpo | "ERA5's `fsr` is an **effective** roughness that carries the orographic drag IFS parameterises at 31 km."
A047 | CONFERMATA | #56 corpo | "Over land it runs at 0.32–0.48 of ERA5's in the median"
A048 | CONFERMATA | #56 corpo | "Over sea the two archives agree: both roughnesses are Charnock"
A049 | CONFERMATA | #56 corpo + commento 2026-09-29 | "`zust` runs **1.6–2.1× ERA5's** over land and 1.1× over sea"
A050 | CONFERMATA | #56 corpo | "The `zust` excess over land is then the other half of the same story: at 3 km the terrain-driven wind is resolved rather than smoothed"
A051 | CONFERMATA | #38 corpo; #25 commento | "ERA5 has no soil at all, because its land-sea mask is permanent"; `ci` carries the ice
A053 | CONFERMATA | #25 commento 2026-09-22 | "So `lsm & ~(ci > 0)` recovers ERA5's permanent mask, as `CHAPTER_VARIABLES.md` §4 claims."
A054 | CONFERMATA | #38 commento 2026-09-25 (resolution) | "`lsm`, `al` | unchanged | still the model's own, hour by hour"
A055 | CONFERMATA | #38 corpo + commento 2026-09-25 | "The converter's soil mask correctly follows the **hourly** land mask"; now masked on the permanent land mask
A056 | CONFERMATA | #38 corpo | "`swvl` reaches **exactly 1.000** ... its porosity ... **0.435**"
A057 | CONFERMATA | #38 commento 2026-09-25 (commit e70ddb4) | "`swvl1-4`, `stl1-4` | geo_em's **permanent** land | sea ice carries no soil column"
A058 | CONFERMATA | #38 corpo; #27 commento | "`ci` is published so nothing is lost that cannot be recovered"
A059 | NON_VERIFICABILE | — | Structure of the document.
A062 | CONFERMATA | #26 corpo/commento; #28 corpo | "with `eps` **measured** from the run rather than looked up"
A063 | CONFERMATA | #26 corpo | "RRTMG's clear-sky diagnostic shares the all-sky equation's `eps` and `T`"
A065 | CONFERMATA | #26 corpo | "an identity with no reference temperature and no fit"
A066 | CONFERMATA | #26 corpo + commento 2026-09-25 | "IQR 0.0000 within every land-use category"; re-measured "IQR ~1e-6"
A067 | CONFERMATA | #26 corpo + commento | "exactly 0.98000 over water"; "Water is **0.98000 with IQR 1.3e-6**, the independent gate"
A068 | CONFERMATA | #55 corpo + commento 2026-09-29 | "replaced by the seasonal pair with the season named"
A069 | CONFERMATA | #55 corpo | "**99.98 % (July) … 93.05 % (January)**"
A070 | CONFERMATA | docs/audit/f8-surface-exchange.md (table, l.92) | "**0.0012 K in July, 0.084–0.119 K in January and February**, p99 0.81 K, absmax 2.79 K". #55 still carries the pre-sweep 0.115–0.133 K / 0.85 / 2.8 (0.01 threshold).
A071 | CONFERMATA | #55 corpo + commento | "the whole of the difference is the snow rule"
A072 | CONFERMATA | #55 commento 2026-09-29T08:14 | "it blends below the threshold and goes flat above"; "the answer is **0.015**"
A073 | CONFERMATA | #55 commento 2026-09-29T08:14 | "This constant is the one free parameter in the whole `skt` reconstruction"
A076 | CONFERMATA_CON_DIFFERENZE | #55 commento 2026-09-29T07:51; #57 commento | "thirty times smaller than the physical cold bias". Stated against 0.115–0.133 K (0.01 threshold), not the 0.084–0.119 K now in the doc.
A077 | CONFERMATA | #57 corpo | "land **−1.64 K**, reaching **−3.24 K** at midday"; "sea **+0.01 K**"
A078 | CONFERMATA | #57 corpo | "The land bias is the run."; "The sea number is the control, and it clears the conversion"
A079 | CONFERMATA | #57 corpo | "**`HFX`, `LH` and the ground heat flux are the three fields this archive does not have**"
A080 | CONFERMATA | #37 corpo | "`al` is a two-season table value by dominant category ..., not a field"
A083 | CONFERMATA | #37 corpo | "8 to 11 distinct values over the whole domain"
A084 | CONFERMATA | #37 corpo + commento 2026-09-29 | "**1 171 937 land points**, 89.9 % of the land mask"; "SUMMER applies April to October and WINTER November to March"
A085 | CONFERMATA | #37 corpo | "Off land it is 0.08 on water and **0.65 on sea ice**"
A086 | CONFERMATA | #37 commento 2026-09-29 | "do not difference it across April or November expecting a signal"
A087 | CONFERMATA | docs/audit/f7-static-and-surface.md §fal | "the model's own flux ratio `SWUPB/SWDNB` ... carries the zenith-angle dependence of that hour"
A088 | CONFERMATA | #45 corpo | "a systematic high bias in surface shortwave"
A090 | CONFERMATA | #45 corpo | "ERA5 carries the Tegen aerosol climatology."
A091 | CONFERMATA | #45 corpo | "an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about that much"
A092 | CONFERMATA | #45 corpo + commento 2026-09-29 | "**+8.5 % clear-sky and +13.6 % all-sky**" (`ssrdc` 1.085, `ssrd` 1.136)
A093 | CONFERMATA | #45 corpo | "they agree with ERA5 to 0.4 to 1.1 per cent, which is the control that makes the solar attribution credible"
A094 | CONFERMATA | #48 corpo | "`tcc` ... **0.783**", "`hcc` ... **0.610**"; "no aerosol *and* too little cloud, both pushing surface solar the same way"
A096 | CONFERMATA | #44 corpo | "it does not extrapolate at all — it **clamps to the lowest model level**"
A097 | CONFERMATA | #44 corpo | "`t` ... **max abs diff exactly 0.0**"; "`q` ... 1e-09 max"
A098 | CONFERMATA | #44 corpo | "a real model state at about 24 to 27 m above ground, not an invention"; "The archive is internally coherent down there."
A099 | CONFERMATA | #44 corpo | "ERA5 extrapolates below ground with a lapse rate ... exactly where 1000 hPa is underground, which is most of the land"
A100 | CONFERMATA | #44 corpo | "a median of **+24 to +27 m above** it ... **47.6 per cent of the domain** at 1000 hPa and 9 per cent at 925"
A101 | CONFERMATA | #44 commento 2026-09-29 | "mask the levels against `sp`, and every field required to do it is in the same file"
A103 | NON_TROVATA | — | No source calls `dl` the run's lake-depth database rather than a model state (`LAKE_DEPTH` is listed among the geo_em fields only, #18/#31).
A105 | CONFERMATA | #25 corpo; #38 commento 2026-09-25 | "`dl` is masked off-lake"; "`dl` | lake | follows `cl`"
A106 | CONFERMATA_CON_DIFFERENZE | #25 corpo | "`LAKE_DEPTH` is the 10 m WPS default on 99.56% of the domain". "79 464 of 88 785" is not found in any source.
A107 | NON_TROVATA | — | No source describes ERA5's `dl` behaviour where the database is silent.
A108 | CONFERMATA | #54 corpo; #38 commento 2026-09-25 | "the archive already writes bitmaps for the soil and ocean fields"; "`sst`, `ci` | the sea | both as a **bitmap**"
A109 | CONFERMATA | #38 commento 2026-09-25 | "`sst` and `ci` both bitmapped ... present exactly on the sea"
A112 | CONFERMATA | #38 commento 2026-09-25 | "`cl` | — | **zero** on the sea, not missing: ERA5's `cl` is defined there and is ~0"
A113 | CONFERMATA | #54 commento 2026-09-25 | "masked exactly where `mucape < 100` | **True**"; "the Fortran's 100 J/kg cut-off"
A114 | CONFERMATA_CON_DIFFERENZE | #54 corpo | "CIN is a real number on **3.8 %** (January) ... **28.8 %** (July)". The doc rounds to 4 %–29 % without saying so.
A115 | CONFERMATA | #54 corpo + commento | "The archive writes 0, which reads as 'nothing is stopping convection', precisely where the most is."
A116 | CONFERMATA_CON_DIFFERENZE | #24 commento 2026-09-22 | "`tsn`'s bitmap is exactly `SNOWC > 0.9`"; "entirely absent at 7 of 34 timesteps, which is the summer". "≈ 29 mm" is not found.
A117 | CONFERMATA | docs/audit/f7-static-and-surface.md §fal | "`SWUPB/SWDNB` above 50 W/m² of incoming shortwave ... undefined at night"
A120 | CONFERMATA_CON_DIFFERENZE | #25 corpo + commento | "`tvl` is masked on the 124672 cells where a shrubland dominates". "15.8 % of cells with `cvl > 0`" is not found; A261 of the same doc says 16.2 %.
A121 | CONFERMATA | #25 corpo; #63 corpo | "MODIS carries no shrub phenology while code table 4.234 splits evergreen from deciduous"
A122 | CONFERMATA | #25 commento 2026-09-22 | "88 785 lake cells"
A124 | CONFERMATA | #12 corpo | "`sf_ocean_physics = 0` ... No ocean coupling, hence no waves, currents, SSH or ice thickness."
A126 | CONFERMATA_CON_DIFFERENZE | #17 corpo; docs/audit/exclusions.md | "the model carries one LAI per cell and ERA5 wants one per vegetation class, so any split is our assumption". "Per unit vegetated area" is not found.
A127 | CONFERMATA | #35 corpo + commento | "`LAI` ... is the model's own leaf area index, alive ... in the wrfout and unpublished"
A129 | CONFERMATA | #17 corpo; docs/audit/exclusions.md | "`OA1-4`/`OL1-4` are Kim-Arakawa asymmetry and effective length, not ECMWF's gradient-covariance eigenstructure. Reason holds."
A130 | CONFERMATA_CON_DIFFERENZE | #35 corpo; #11 corpo | "the four entries that moved *into* the archive in September". The 2026-09-17 date is not in any source.
A131 | CONFERMATA | #24 corpo + commento | "each ERA5 layer is the exact integral of RUC's own piecewise-linear profile"
A132 | CONFERMATA | #24 corpo + commento | "RUC has 6 nodes at 0/5/20/40/160/300 cm"; `ZS` = "(0, 0.05, 0.20, 0.40, 1.60, 3.00) m"
A133 | CONFERMATA | #24 commento 2026-09-22 | "extrapolation at the bottom | **none**: 2.89 m of ERA5 column inside a 3.00 m deepest node"
A134 | NON_TROVATA | — | No source states that the old objection was to writing point values rather than integrating them.
A136 | CONFERMATA | #12 corpo §h; #25 commento | "The 90.1 % average dominance and the 17.9 % of land cells carrying both high and low vegetation"; #25: "233 844 (17.93 %)"
A138 | CONFERMATA | #25 corpo; #63 corpo | "MODIS carries no shrub phenology while code table 4.234 splits evergreen from deciduous"
A141 | NON_VERIFICABILE | — | Editorial statement of the document.
A142 | CONFERMATA | #18 corpo; #11 corpo | "`cvl`/`cvh`/`tvl`/`tvh`/`slt`/`cl`/`dl` were all considered impossible until they were not"
A143 | CONFERMATA | #25 corpo + commento; #38 commento | "19309 land cells hold a sub-grid lake that `lsm` does not carry, because `sf_lake_physics=0` recodes class 21 to 17" (count confirmed)
A145 | NON_VERIFICABILE | — | Description of the document's table columns.
A229 | CONFERMATA | #25 corpo + commento | "read once from the `geo_em.d02` sidecar"; "**bitwise identical at all 34 timesteps**"
A230 | CONFERMATA | #25 corpo + commento | "WRF reclassifies points with `SEAICE>0` as ice: `LANDMASK` 0->1"; "`lsm` moves at 14 timesteps"
A239 | NON_TROVATA | — | No source says `tvl`/`tvh`/`slt` are the only coded fields or that their tables are published.
A241 | CONFERMATA | #59 corpo | "`LU_INDEX` vs `IVGTYP`, lake recode excluded | **1.0000**" (0.9998 at 2025-02-15, all 2735 disagreements on sea ice)
A242 | CONFERMATA | #25 corpo; #12 corpo | "`sf_lake_physics=0` recodes class 21 to 17"; "WRF recodes lakes to water at init"
A243 | CONFERMATA | #12 corpo | "Confirms the `cl` reasoning in `CLAUDE.md`: geogrid *did* resolve lakes"
A259 | CONFERMATA_CON_DIFFERENZE | #25 commento 2026-09-22 | "code table 4.234 exact"; only row 5→18 is explicitly called "a semantic identity in 4.234". No source asserts it for every row.
A261 | CONFERMATA_CON_DIFFERENZE | #25 corpo | The shrubland mask is attested; "16.2 % of vegetated cells" is not found (A120 of the same doc says 15.8 %).
A262 | CONFERMATA_CON_DIFFERENZE | #26 commento 2026-09-25; #28 corpo | "five categories never occur in this domain"; #28 names 11, 14, 19, 20 (+0) as unmeasurable. The link to "ambiguous rows" is not stated.
A270 | NON_TROVATA | — | No source says every land point classifies or that type 7 is absent.
A271 | CONFERMATA | #24 corpo; #14 corpo | "RUC has 6 nodes at 0/5/20/40/160/300 cm"; ERA5 layer tops "0 / 7 / 28 / 100" and "289 cm" deepest boundary
A272 | CONFERMATA | #24 corpo + commento | "nothing is extrapolated"; "2.89 m of ERA5 column inside a 3.00 m deepest node"
A273 | CONFERMATA | #24 commento 2026-09-22 | "the converter's matrix ... row sums exactly 1.0, all four"; "`SOIL_LAYER_WEIGHTS` is a compile-time constant"
A274 | CONFERMATA | docs/audit/exclusions.md (SH2O row); #11 corpo | "`SH2O` ... ERA5's `swvl1-4` are total soil water; there is no separate liquid fraction"; the layers come from `TSLB`/`SMOIS`
A275 | CONFERMATA_CON_DIFFERENZE | #24 commento; #38 commento 2026-09-25 | Masked on water, but since e70ddb4 on geo_em's **permanent** land mask, so sea-ice cells are masked too.

## Conteggi
CONFERMATA: 88
CONFERMATA_CON_DIFFERENZE: 17
CONTRADDETTA: 1
NON_TROVATA: 7
NON_VERIFICABILE: 7
