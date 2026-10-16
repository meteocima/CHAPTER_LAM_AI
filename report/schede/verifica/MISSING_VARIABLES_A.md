# Verifica: MISSING_VARIABLES (A)
A001 | NON_VERIFICABILE | — | data del documento
A002 | NON_VERIFICABILE | — | ambito del documento
A003 | NON_VERIFICABILE | — | scopo della nota
A004 | NON_VERIFICABILE | — | indicazione di lettura
A005 | CONFERMATA_CON_DIFFERENZE | #59 [corpo] | "the campaign costs about eleven days of datamover time"; "the regeneration should happen once" — la fonte dà ~10-11 giorni e ~152 TB, non "diversi giorni"
A009 | CONFERMATA | #12 [corpo]; #22 [corpo]; #23 [corpo] | "all 19 accumulators in accum_ref.ACCUMULATED_VARS are monotone within a run by configuration, not merely by observation"
A010 | NON_TROVATA | — | nessuna fonte descrive il round trip dei paramId nell'encoder
A013 | NON_TROVATA | — | il conteggio "22 di 24" non compare nelle fonti
A014 | CONFERMATA | #17 [commento 2026-09-22] | "`10efg`/`10nfg` | by decision, only a resolved-wind maximum exists | holds"
A015 | CONFERMATA_CON_DIFFERENZE | #19 [corpo] | "13 variables x 13 levels = 169 messages": le fonti non elencano le 9 variabili richieste
A016 | CONFERMATA | #19 [corpo] | "Both vertical-velocity conventions are published, `w` in Pa/s and `wz` in m/s"
A017 | CONFERMATA | #19 [corpo] | "`cc` `ciwc` `clwc` `crwc` `cswc` `q` `r` `t` `u` `v` `w` `wz` `z`"
A018 | CONFERMATA | #17 [commento 2026-09-22] | "TKE | not in the run | holds — BL_PBL_PHYSICS = 1, YSU non-local, KM_OPT = 4"
A019 | CONFERMATA | #25 [commento 2026-09-22] | "`z` (surface), `sdor`, `slor`" ricalcolati e invarianti; z = HGT × 9.80665 a 2e-4
A020 | CONTRADDETTA | #31 [commento 2026-09-19]; #12 [corpo] | "`LANDUSEF` | recoverable, and already recovered — geo_em.d02, 21 categories, read by static_ref.py"
A021 | CONFERMATA_CON_DIFFERENZE | #63 [corpo] | "most of what was previously declined is now delivered"; nessuna fonte dice "il sottoinsieme che esiste"
A022 | CONFERMATA | #22, #24, #25, #26, #51 [commenti] | famiglie auditate: radiazione, runoff (sro/ssro/ro), snowc, tsn, al/fal, iews/inss, cvl/cvh verificati
A023 | CONFERMATA | #12 [corpo]; #18 [commento] | "No ocean coupling, hence no waves, currents, SSH or ice thickness"
A024 | CONFERMATA_CON_DIFFERENZE | #25 [commento 2026-09-22] | consegnata, ma "`ci` is a flag, not a fraction — two distinct values, from FRACTIONAL_SEAICE = 0"
A025 | CONFERMATA_CON_DIFFERENZE | #12 [corpo]; #18 [commento] | spessore: "no ... ice thickness"; "the lake and sea-ice-layer families" impossibili; neve su ghiaccio e albedo non nominati
A026 | CONFERMATA | #25 [corpo] | `sst` fra i 15 campi della famiglia 7, verificato (costante nelle 24 h)
A027 | CONFERMATA | #12 [corpo] | "No ocean coupling, hence no waves, currents, SSH or ice thickness"
A028 | CONFERMATA | #12 [corpo] | "TITLE = ' OUTPUT FROM WRF V4.1.1 MODEL'"
A029 | CONFERMATA | #11 [corpo]; #46 [corpo] | "WRF (d02 only, 3 km Mercator, 1641x1353)"; "at 49 × 1353 × 1641"
A035 | CONFERMATA | #12 [corpo]; docs/audit/inventory-sweep.md | "ocean waves (43 parameters), Stokes drift, Charnock ... SF_OCEAN_PHYSICS = 0, no wave or ocean model"
A044 | NON_TROVATA | #16 [corpo] | la fonte dice solo che ACSNOW "was already excluded" e "nothing publishable joins the dead list"; nessuna frase generale
A045 | NON_VERIFICABILE | — | struttura del documento (introduzione a §3)
A046 | NON_TROVATA | — | nessuna fonte sullo stato di implementazione delle voci di §3
A047 | CONFERMATA | #25 [corpo]; docs/audit/f7-static-and-surface.md §fal | `al` e `fal` pubblicati; fal "the model's own flux ratio SWUPB/SWDNB"
A048 | CONFERMATA | #31 [commento 2026-09-19]; #25 [commento] | LANDUSEF "is the source of `cvl`/`cvh`"; "LANDUSEF sums 8.6e-8"
A049 | CONFERMATA_CON_DIFFERENZE | #11 [corpo]; #31 [commento 2026-09-19] | "the geo_em recovery"; data 2026-09-18 e provenienza LRZ non riportate nelle issue
A050 | CONFERMATA | #59 [commento] | "`LU_INDEX` vs `IVGTYP`, lake recode excluded | 1.0000" (anche 2025-02: 0.9998)
A051 | CONFERMATA | #63 [corpo] | "the geo_em recovery added cvl, cvh, tvl, tvh, slt, cl, dl and the eight soil layers"
A052 | NON_TROVATA | — | nessuna fonte propone skt ristretta al ghiaccio come temperatura del ghiaccio
A053 | NON_TROVATA | — | —
A054 | NON_TROVATA | — | —
A055 | NON_TROVATA | #18 [corpo] | la fonte usa `u*/κ · ln(10/z0)` solo per u10n/v10n; nessun Cd
A056 | CONFERMATA_CON_DIFFERENZE | #56 [corpo] | "Over sea ... both roughnesses are Charnock"; sulla terra ZNT "is a land-use lookup with a snow override"
A057 | NON_TROVATA | — | —
A058 | NON_TROVATA | — | —
A059 | CONTRADDETTA | #18 [commento] | "a bulk-Richardson diagnosis would be **ours**, not the model's, so it fails the publication rule"
A060 | NON_TROVATA | — | —
A061 | CONFERMATA | #50 [corpo]; #17 [commento 2026-09-22] | "10fg is the resolved 10 m wind with a 2 per cent premium, not a gust"
A062 | NON_TROVATA | — | —
A063 | CONFERMATA_CON_DIFFERENZE | #17 [commento 2026-09-22] | "by decision, only a resolved-wind maximum exists"; la scomposizione lungo il vento non è discussa
A065 | NON_TROVATA | — | MYNN/MYJ non nominati
A066 | NON_TROVATA | — | —
A067 | CONFERMATA | #12 [corpo]; docs/audit/inventory-sweep.md | "SF_OCEAN_PHYSICS = 0, no wave or ocean model"
A068 | NON_TROVATA | — | ERA5 waves / 31 km non discussi
A069 | CONFERMATA_CON_DIFFERENZE | #56 [corpo] | "Over sea ... both roughnesses are Charnock"; l'assenza di stato del mare è solo implicita in SF_OCEAN_PHYSICS=0
A070 | NON_VERIFICABILE | — | rimando interno a §3
A072 | NON_TROVATA | — | CMEMS non nominato
A073 | CONFERMATA_CON_DIFFERENZE | #12 [corpo] | "no waves, currents, SSH or ice thickness"; ghiaccio "solo come concentrazione al contorno" non detto
A074 | NON_TROVATA | — | —
A075 | CONFERMATA_CON_DIFFERENZE | #37 [corpo] | "0.65 on sea ice, which is WRF's seaice_albedo_default and follows from SEAICE_ALBEDO_OPT = 0"
A076 | NON_TROVATA | — | —
A078 | CONFERMATA_CON_DIFFERENZE | #17 [commento 2026-09-22]; #35 [corpo] | ACSNOM "non-monotone ... confirmed: 15 of 16 days, up to 8.2 mm"; il nesso col riferimento 00Z non è scritto
A079 | NON_TROVATA | — | —
A082 | CONFERMATA | #31 [commento 2026-09-19] | "Resolved: a modified Registry. The fields were never written, and nothing upstream holds them."
A083 | CONFERMATA | #29 [commento 2026-09-29] | "ACHFX/ACLHF/ACGRDFLX/NOAHRES are now recorded as dead because they are Noah accumulators in a RUC run" (#16 li attribuiva al Registry)
A084 | CONFERMATA_CON_DIFFERENZE | #31 [commento 2026-09-19] | "TSK, HFX, LH, QFX, GRDFLX, EMISS, PBLH | unrecoverable"; "una nuova run" non detto esplicitamente
A085 | NON_TROVATA | — | —
A086 | CONFERMATA | #29 [corpo] | "TSK | not written out | correct, and now known to be a Registry decision rather than an accident"
A087 | CONFERMATA | docs/audit/f8-surface-exchange.md §skt; #31 [commento] | "the skin temperature is inverted from LWUPB = eps·σT⁴ + (1−eps)·LWDNB"
A088 | CONFERMATA | #55 [corpo e commento 2026-09-29] | "water gate, skt vs the model's own SST | 0.0005 K RMSE, ~910 000 points, every timestep"
A090 | CONFERMATA | #30 [corpo] | "an hourly sample of T2 is not the same quantity as the model's own within-hour extremum"
A091 | CONFERMATA | #30 [commento 2026-09-29] | "and the only route (a re-run)"
A093 | CONFERMATA | #29 [corpo] | "YSU does diagnose one. It was not written to the history stream."
A094 | CONTRADDETTA | #18 [commento]; #29 [corpo] | re-run confermata, ma "a bulk-Richardson diagnosis would be ours, not the model's, so it fails the publication rule"
A095 | NON_TROVATA | — | le date 2026-09-17/18 di eliminazione e reintegro non compaiono
A096 | CONFERMATA | #24 [corpo]; docs/audit/f6-soil-and-snow.md | "RUC has 6 nodes at 0/5/20/40/160/300 cm; ERA5's deepest boundary (289 cm)"; "3 (28–100 cm)"
A097 | CONFERMATA_CON_DIFFERENZE | #24 [corpo] | "swvl1-4 / stl1-4 are integrals, not relabellings"; l'obiezione storica non è riportata
A098 | CONFERMATA | #24 [corpo] | "each ERA5 layer is the exact integral of RUC's own piecewise-linear profile"
A099 | CONFERMATA | #24 [corpo] | "ERA5's deepest boundary (289 cm) falls inside the deepest node ... nothing is extrapolated"
A100 | NON_TROVATA | — | il motivo storico dell'esclusione non è nelle fonti
A101 | CONFERMATA | #12 [corpo]; #25 [commento] | "slt is ... derived in static_ref.py from geo_em's CLAYFRAC/SANDFRAC against the FAO thresholds, never from this table"
A104 | CONFERMATA | #63 [corpo] | "tvl is masked on 124 672 shrubland cells, because MODIS carries no shrub phenology and ECMWF's table splits evergreen from deciduous"
A105 | CONFERMATA_CON_DIFFERENZE | #12 [corpo] | "The run reduced every cell to one dominant land-use ... cvl/cvh from geo_em are therefore more informative"; la versione precedente di cvl/cvh non è descritta
A106 | CONFERMATA | #31 [commento 2026-09-19]; #25 [commento] | LANDUSEF "is the source of cvl/cvh"; "LANDUSEF sums 8.6e-8"
A107 | CONFERMATA | #12 [corpo]; #25 [commento 2026-09-22] | "The 90.1 % average dominance and the 17.9 %"; "233 844 (17.93 %) with both vegetation types above 5 %"
A108 | CONFERMATA_CON_DIFFERENZE | #17 [commento 2026-09-22] | "one LAI per cell, ERA5 wants one per class | holds"; "per unità di area vegetata" non detto
A109 | CONFERMATA | #17 [commento 2026-09-22] | "the per-class split is still an assumption"
A110 | CONFERMATA | #63 [corpo] | "The single field can be delivered under its own name if they want it."
A111 | CONFERMATA | #17 [corpo] | "OA1-4/OL1-4 are Kim-Arakawa asymmetry and effective length"
A112 | CONFERMATA_CON_DIFFERENZE | #17 [corpo e commento 2026-09-22] | "not ECMWF's gradient-covariance eigenstructure"; "the quantities differ" — "correlati" e "non in una riga" non detti
A113 | CONFERMATA_CON_DIFFERENZE | #63 [corpo]; #35 [corpo] | solo per LAI: "can be delivered under its own name"; VEGFRA/OA/OL non discussi
A114 | NON_VERIFICABILE | — | indicazione di lettura
A115 | CONFERMATA_CON_DIFFERENZE | #12 [corpo]; #19 [corpo] | "an earlier note in CLAUDE.md claimed binary and was wrong": la nota sbagliata era in CLAUDE.md, non in questo documento
A117 | CONFERMATA | #21 [corpo]; #48 [corpo] | "tcc/hcc/mcc/lcc are maximum-random overlaps of CLDFRA"
A118 | CONFERMATA | #19 [corpo] | `cc` fra le 13 variabili su livelli di pressione
A120 | CONFERMATA | #31 [commento 2026-09-19]; docs/audit/f8-surface-exchange.md | "TSK was not written out, so the skin temperature is inverted from LWUPB"
A122 | CONTRADDETTA | #55 [corpo e commento 2026-09-29] | la fonte dà "0.0005 K RMSE" (prima registrato 0.0015 K), non 0.005 K
A123 | NON_TROVATA | #24 [corpo] | nessun RMSE skt vs livello 0 cm; #24: "The right soil comparison is TSLB[0]"
A124 | CONTRADDETTA | #55 [corpo]; #28 [corpo] | la regola neve è misurata: "It is a switch ... 0.98"; land reproduced "99.98 % (July) … 93.05 % (January)"; nessuno 0.8 K
A125 | CONFERMATA | #37 [corpo] | "slor is published as |∇z| of the resolved 3 km terrain while paramId 163 is defined as the slope of the sub-grid orography"
A126 | CONFERMATA | #37 [corpo]; docs/audit/f7-static-and-surface.md | "sdor is the ERA5 quantity, evaluated on a 3 km cell"; "sdor against √VAR_SSO ... 1.5e-5 m"
A127 | CONFERMATA | #19 [corpo]; #41 [corpo] | "WRF's Q* are mixing ratios, per kg of dry air; these are specific contents, per kg of moist air"
A129 | CONTRADDETTA | #41 [corpo e commento 2026-09-25] | "over the full 3-D field it is 0.011 per cent" in mediana; "2.26 % at most, 1.44 % at p99"
A130 | CONFERMATA | #54 [corpo] | "cape_2d's Fortran flags CIN as missing wherever CAPE < 100 J/kg"
A131 | NON_TROVATA | — | assenza del livello di equilibrio non discussa
A132 | CONTRADDETTA | #54 [commento 2026-09-25] | vero solo per mucape; per mucin "A GRIB bitmap where cape_2d declined ... Commit 3ad8a2d"
A133 | CONTRADDETTA | #54 [corpo] | "For mucape that reasoning is right ... For mucin it is backwards"
A134 | NON_VERIFICABILE | #54 [commento 2026-09-25] | richiesta ai lettori; già decisa: "Decided — option 1, the bitmap"
A135 | CONFERMATA | docs/audit/f8-surface-exchange.md §mucin | "Most unstable, mixed over 500 m, searched in the lowest 3 km" (dal Fortran rip_cape.f90)
A136 | CONFERMATA | #50 [corpo] | "10fg is the resolved 10 m wind with a 2 per cent premium, not a gust"
A137 | CONFERMATA | #50 [corpo] | cita MISSING_VARIABLES: "It behaves like a gust and is the best proxy available"
A138 | CONFERMATA | #50 [corpo] | "ERA5's is a parameterised gust roughly 1.6 times the mean wind"
A141 | CONFERMATA | #50 [corpo e commento 2026-09-29] | "under-predicts by 38 per cent ... not a bias to be corrected downstream; it is a different quantity"
A142 | CONFERMATA_CON_DIFFERENZE | #49 [corpo] | la fonte dà il complemento: reset mancato "17 (12.3 %)" su 138 transizioni; "88 %" non scritto
A144 | CONFERMATA | #37 [corpo]; #25 [commento] | "lsm ... moves at the sea-ice points and nowhere else, 0 false positives and 0 missed"
A146 | CONFERMATA_CON_DIFFERENZE | #03 [corpo] | "Only lsm (from LANDMASK) and al (from ALBBCK) still vary"; tvl/tvh/slt ora statici dal sidecar
A147 | CONFERMATA | docs/audit/f8-surface-exchange.md §iews/inss; #26 [commento] | "The stress is ρu*² aligned with the 10 m wind"
A148 | CONFERMATA | #26 [commento] | "The alignment is the one thing that is ours ... priced on ERA5 itself: median 0.92–1.10°"
A149 | CONFERMATA_CON_DIFFERENZE | #24 [corpo]; docs/audit/f6-soil-and-snow.md | "SOILT1 ... is the temperature inside snow"; "tsn is SOILT1 where SNOWC > 0.9"
A150 | CONFERMATA_CON_DIFFERENZE | #24 [commento] | "tsn's bitmap is exactly SNOWC > 0.9": mancante anche dove c'è neve con copertura ≤ 0.9
A151 | CONFERMATA_CON_DIFFERENZE | #37 [corpo e commento 2026-09-29] | "al is a two-season table value by dominant category", cambia su 1 171 937 punti (89.9 %) tra WINTER e SUMMER
A152 | CONFERMATA | docs/audit/f7-static-and-surface.md §fal | "ours is the model's own flux ratio SWUPB/SWDNB"
A153 | CONFERMATA | docs/audit/f7-static-and-surface.md §fal; #15 [corpo] | "above 50 W/m² of incoming shortwave ... undefined at night"
A160 | CONFERMATA | #51 [corpo] | "UDROFF barely moves within a day ... the published ssro is the accumulation since 00Z"
A161 | CONFERMATA | #51 [corpo] | "sro | 1.0 to 4.6; ssro | 0.000 to 0.004; ro | 0.19 to 0.85"
A162 | CONFERMATA | #51 [commento 2026-09-29] | "do not close a water budget assuming this archive carries a drainage term"
A163 | CONFERMATA_CON_DIFFERENZE | #51 [commento 2026-09-29] | "ro and sro are knowingly duplicate messages"; la ragione "ro totale canonico ERA5" non è scritta
A164 | CONFERMATA | #47 [corpo] | "There is no graupel column in the archive"; tcw costruito con QGRAUP
A166 | CONFERMATA | #47 [commento 2026-09-29] | "ECMWF does define 260028 grle and 260001 tcolg but ERA5 publishes neither"
A167 | CONFERMATA | #47 [commento 2026-09-29] | "reconstructing tcw from the five published component columns does not reproduce it"
A168 | CONFERMATA | #47 [corpo] | "In the domain mean it is 0.4 % of the condensate"
A169 | CONFERMATA | #47 [commento 2026-09-29] | "up to 26.5 kg/m² inside a July convective cell, more than the rest of the column" (corpo: 26.46)
A171 | CONFERMATA | #52 [corpo]; #33 [commento] | "emit('tirf', RAINNC - SNOWNC - GRAUPELNC) # rain only"
A172 | CONFERMATA | #20 [commento] | "the GRIB1 archive wrote it straight through under a paramId defined in K. The converter asks units='K'"
A173 | NON_TROVATA | — | la correzione +273.15 non è scritta
A174 | CONFERMATA | #23 [corpo]; #22 [commento] | "same day, same run)) / 1000, exactly zero at 00Z"
A175 | CONFERMATA | #15 [corpo]; #22 [corpo] | "reference time = 00Z of the day and step 0-H (PDT 8)"
A176 | CONFERMATA_CON_DIFFERENZE | #49 [corpo] | encoding 0-1 corretto, ma "on 12 per cent of hours WSPD10MAX was not reset, so it is a longer one"
A177 | CONFERMATA_CON_DIFFERENZE | #26 [commento]; docs/audit/f8-surface-exchange.md | "shapeOfTheEarth = 1 with radius = 6370000 on all 246 messages"; "~2 m" non trovato
A178 | CONFERMATA_CON_DIFFERENZE | #26 [corpo] | "without it eccodes derives a grid off by ~1.1 km at the northern edge"; il riferimento al GRIB1 non è nella issue
A179 | CONFERMATA | #17 [commento 2026-09-22] | righe 10efg/10nfg e TKE: "holds"
A180 | CONFERMATA_CON_DIFFERENZE | #63 [corpo]; #31 [commento 2026-09-19] | "the geo_em recovery added cvl, cvh, tvl, tvh, slt, cl, dl and the eight soil layers"; data e LRZ non riportati
A181 | NON_TROVATA | — | —
A182 | CONFERMATA_CON_DIFFERENZE | #24 [corpo]; #63 [corpo] | soil layers come integrali ERA5, sd/snowc/rsn/tsn auditati; "nevicata" (sf) è però solo SNOWNC senza graupel (#52)
A183 | CONFERMATA | #51 [corpo]; #24 [corpo] | sro/ssro/ro pubblicati; "src is the same quantity with a different capacity"
A184 | CONFERMATA | #63 [corpo]; #25 [corpo] | "cvl, cvh, tvl, tvh, slt, cl, dl"
A185 | CONFERMATA | #56 [corpo]; #26 [commento]; #25 [corpo] | zust, fsr, al, fal, iews/inss nella famiglia 7-8
A186 | CONFERMATA_CON_DIFFERENZE | #22 [corpo] | famiglia radiazione auditata; l'elenco completo "netto e clear-sky, superficie e TOA" non è enunciato così
A187 | CONFERMATA | #17 [commento 2026-09-22]; #35 [corpo] | lai_lv/lai_hv "one LAI per cell ... holds"; "ACSNOM is not monotone"
A188 | NON_VERIFICABILE | #63 [corpo] | richiesta ai lettori; #63: "The question as posed is stale in their favour and should be re-asked"
A189 | CONFERMATA | #33 [commento 2026-09-21] | "vwsh ... sqrt((100u-10u)² + (100v-10v)²)/90"
A190 | NON_TROVATA | — | —
A191 | CONFERMATA_CON_DIFFERENZE | #19 [corpo] | "the 8 ERA5 levels above 50 hPa are above WRF's P_TOP"; 37 e 29 non scritti
A192 | CONFERMATA | #19 [commento 2026-09-19] | "p_top_requested = 5000: 50 hPa is the model lid"
A193 | NON_TROVATA | — | dimensioni a 29 livelli non riportate
A194 | NON_VERIFICABILE | — | richiesta ai lettori

## Conteggi
CONFERMATA: 73
CONFERMATA_CON_DIFFERENZE: 32
CONTRADDETTA: 8
NON_TROVATA: 28
NON_VERIFICABILE: 10
