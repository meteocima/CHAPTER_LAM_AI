# Verifica: CHAPTER_VARIABLES (N)
N003 | NON_VERIFICABILE | — | data di aggiornamento del documento (metadato)
N006 | CONFERMATA | #18 commento 2026-09-22; #12 commento 2026-09-19 | "from U, V, QVAPOR, T, P on the 49 model levels"; "present in the wrfout on all 49 mass levels"
N007 | CONFERMATA | #12 commento 2026-09-19 | "`p_top_requested = 5000`: 50 hPa is the model lid, and it is the archive's topmost pressure level"
N008 | CONFERMATA | #11 corpo | "WRF (d02 only, 3 km Mercator, 1641x1353)"
N009 | CONFERMATA | #11 corpo | "WRF (d02 only, 3 km Mercator, 1641x1353)"
N010 | CONFERMATA | #49 corpo; #34 commento 2026-09-25 | "A one-hour maximum over 2 220 273 points"; "agree on all 2 220 273 cells"
N011 | CONFERMATA_CON_DIFFERENZE | #14 commento 2026-09-21 | la fonte dà 4 decimali: "23.4719..60.0006 N and -19.9722..42.2555 E"; la scheda arrotonda a 3 senza dichiararlo
N012 | NON_TROVATA | — | nessuna fonte cita il parallelo standard 44.671 N (né TRUELAT)
N014 | CONFERMATA | #40 corpo; docs/audit/f3-column-integrals.md (tabella packing) | "a value pinned at exactly 100 comes back from 24-bit CCSDS packing"; f3: "grid_ccsds, 24 bits"
N015 | CONFERMATA_CON_DIFFERENZE | #13 commento 2026-09-19 | nessun ~747 MB; la fonte misura per il campione "615-679 MB [00Z] against 691-756 MB [12Z]"
N016 | NON_TROVATA | — | ~17.9 GB/giorno non compare in issue né in docs/audit
N017 | NON_TROVATA | — | ~6.6 TB/anno non compare in issue né in docs/audit
N021 | CONFERMATA | #19 corpo | "the 8 ERA5 levels above 50 hPa are above WRF's `P_TOP` and cannot be produced"
N022 | CONFERMATA | #20 corpo | "Near-surface state (10 variables, `heightAboveGround`): `10u` `10v` `100u` `100v` `200u` `200v` `2t` `2d` `2r`"
N024 | CONFERMATA_CON_DIFFERENZE | #53 corpo; commento 2026-09-29 | valore 128 giusto ma non marca gli accumulati: "All 246 [...] inside `grib_v3` the value discriminates nothing"
N025 | CONFERMATA | #37 corpo; #15 corpo | "`sdor` [...] of a 31 km one: the measured ratio of medians is 0.244"; "how 3 km is compared to 31 km"
N026 | CONFERMATA | #25 commento 2026-09-22; #37 commento 2026-09-29 | "`sdor` is the ERA5 quantity at our scale. Ratio of medians 0.244 = (3/31)^0.605"
N027 | CONFERMATA | #25 commento 2026-09-22; #37 commento 2026-09-29 | "Ratio of medians 0.244 = (3/31)^0.605 — a Hurst exponent inside the 0.5–0.7 range"
N028 | CONFERMATA | #56 corpo (misura); commento 2026-09-29 | "`fsr`, land [...] ratio of medians 0.32–0.48"
N029 | CONFERMATA | #56 commento 2026-09-29 (misura: #56 corpo) | "`zust` runs 1.6–2.1× ERA5's over land and 1.1× over sea"; corpo: ratio of means 1.62–2.06 / 1.08–1.12
N030 | CONFERMATA | #11 corpo; #15 corpo | "ERA5 at 31 km"; "Build the audit harness, and settle how 3 km is compared to 31 km"
N031 | CONFERMATA | #24 commento 2026-09-22; #38 corpo | "its porosity 0.435; the published value exceeds it by +0.565"; swvl "exactly 1.000"
N032 | CONFERMATA | #38 commento 2026-09-25 | "Resolution — repaired, commit `e70ddb4`" con `swvl1-4`/`stl1-4` su terra permanente; regola decisa "on 2026-09-25"
N033 | CONFERMATA | #26 commento 2026-09-25 (misura); #26 corpo | "Every category's median matches the table to 1e-7 or better, IQR ~1e-6"; corpo: "IQR 0.0000"
N034 | CONFERMATA | #26 commento 2026-09-25 | "Water is 0.98000 with IQR 1.3e-6, the independent gate"
N035 | CONFERMATA | #55 corpo e commento 2026-09-29; docs/audit/f8-surface-exchange.md §The water gate... | "99.98 % (July) … 93.05 % (January)"; invariato dopo la soglia 0.015 (f8)
N036 | CONFERMATA | docs/audit/f8-surface-exchange.md §The water gate is three times better... | "0.0012 K in July, 0.084–0.119 K in January and February"; #55 riporta i valori vecchi a soglia 0.01: 0.115–0.133 K
N037 | CONFERMATA | docs/audit/f8-surface-exchange.md §The water gate is three times better... | "p99 0.81 K, absmax 2.79 K" (a 0.015); #55 corpo/commento dà i vecchi "p99 0.85 K, absmax 2.8 K"
N038 | CONFERMATA | #26 corpo; #28 corpo | "snow switches every category to a flat 0.98"; #55 commento 2026-09-29 precisa: blend sotto soglia, piatta sopra
N042 | CONFERMATA | #57 commento 2026-09-29; #55 commento 2026-09-29 | "the derivation error over land in winter is 0.115–0.133 K, thirty times smaller than the physical bias"
N043 | CONFERMATA | #57 corpo (misura); #26 commento 2026-09-25 | "land −1.64 K, reaching −3.24 K at midday (2024-09-15T12)"
N044 | CONFERMATA | #57 corpo | "sea +0.01 K | 0.95–0.98"
N045 | CONFERMATA | #37 corpo; commento 2026-09-29 | "category (8 to 11 distinct values)"; "§4 gained the user-facing version: 8 to 11"
N046 | CONFERMATA | #37 corpo; #25 commento 2026-09-22; #37 commento 2026-09-29 | "`al` moves at 1 171 937 land points, 89.9 % of the land mask"
N047 | CONFERMATA | #37 corpo; #25 commento 2026-09-22 | "is 0.08 on water and 0.65 on sea ice, which is WRF's `seaice_albedo_default`"
N049 | CONFERMATA | #45 corpo | "an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about that much"
N050 | CONFERMATA | #45 commento 2026-09-29 | "+8.5 % clear-sky and +13.6 % all-sky at the surface"
N051 | CONFERMATA | #45 commento 2026-09-29 | "+8.5 % clear-sky and +13.6 % all-sky at the surface"
N052 | CONFERMATA | #45 corpo; commento 2026-09-29 | "the thermal fields agreeing to within 1.1 % as the control"; corpo: "0.4 to 1.1 per cent"
N053 | CONFERMATA | #48 corpo | "Total cloud cover runs 22 per cent below ERA5" (tcc ratio 0.783)
N054 | CONFERMATA | #48 corpo | "high cloud 39 per cent below" (hcc ratio 0.610)
N055 | CONFERMATA | #44 corpo | "`t` against the lowest model level max abs diff exactly 0.0 [...] `q` 1e-09 max"
N056 | CONFERMATA | #44 corpo; commento 2026-09-29 | "The number is a real model state at about 24 to 27 m above ground"
N057 | CONFERMATA | #44 corpo | "the published `z` at 1000 hPa puts it at a median of +24 to +27 m above it"
N058 | CONFERMATA | #44 corpo; #19 commento 2026-09-22 | "on 47.6 per cent of the domain at 1000 hPa and 9 per cent at 925"
N060 | CONFERMATA | #25 corpo; docs/audit/f7-static-and-surface.md §cl and dl | "`LAKE_DEPTH` is the 10 m WPS default"; f7: "10 m is the WPS default fill"
N061 | CONFERMATA | #25 corpo | "`LAKE_DEPTH` is the 10 m WPS default on 99.56% of the domain" (enunciato come claim da verificare, non rimisurato nei commenti)
N062 | CONFERMATA_CON_DIFFERENZE | docs/audit/f7-static-and-surface.md §cl and dl | la fonte dà la frazione, non il conteggio: "89.5 % of its 88 785 cells carry the 10 m default"
N067 | CONFERMATA | #34 commento 2026-09-25 (anche #36, #38) | "Component size works, with a factor of seven of slack"
N068 | CONFERMATA | #54 corpo | "`cape_2d`'s Fortran flags CIN as missing wherever CAPE < 100 J/kg"
N069 | CONFERMATA_CON_DIFFERENZE | #54 corpo; commento 2026-09-25 | la fonte dà la frazione mascherata: "constant zero on 71 to 96 per cent"; misurato "masked fraction 94.3 % [feb] / 71.2 % [lug]"
N070 | CONFERMATA_CON_DIFFERENZE | #24 corpo; commento 2026-09-22 | 0.9 confermato: "`tsn`'s bitmap is exactly `SNOWC > 0.9`"; "≈ 29 mm" non trovato
N071 | CONFERMATA | docs/audit/f7-static-and-surface.md §fal | "the model's own flux ratio `SWUPB/SWDNB` above 50 W/m² of incoming shortwave"
N073 | CONFERMATA_CON_DIFFERENZE | #25 commento 2026-09-22 | 124 672 confermato ("124 672 `tvl` masked"); 15.8 % non trovato
N074 | CONFERMATA | #25 commento 2026-09-22 | "Every count `CLAUDE.md` quotes is confirmed exactly: [...] 88 785 lake cells"
N075 | NON_VERIFICABILE | — | storia della struttura del documento (§6 fino al 2026-09-17)
N076 | CONFERMATA | #24 commento 2026-09-22; #12 commento 2026-09-19 | "Read at all 34 timesteps: one distinct value, `(0, 0.05, 0.20, 0.40, 1.60, 3.00)` m"
N077 | CONFERMATA | #24 corpo; commento 2026-09-22 | "ERA5's deepest boundary (289 cm)"; "2.89 m of ERA5 column inside a 3.00 m deepest node"
N078 | CONFERMATA | #12 commento 2026-09-19 | "The 90.1 % average dominance [...] which `CLAUDE.md` reports from geo_em" (citato, non rimisurato)
N079 | CONFERMATA_CON_DIFFERENZE | #25 commento 2026-09-22 (misura); #12 commento 2026-09-19 | misurato "233 844 (17.93 %) with both vegetation types above 5 %"; la scheda arrotonda a 17.9
N080 | NON_TROVATA | — | nessuna fonte dice che i tipi di suolo ECMWF sono 7 (solo "the FAO thresholds")
N083 | CONFERMATA | #25 commento 2026-09-22 | "88 785 lake cells, 19 309 on land"
N093 | CONFERMATA_CON_DIFFERENZE | #59 commento 2026-09-28; #62 commento 2026-09-29 | "`LU_INDEX` vs `IVGTYP`, lake recode excluded": 1.0000 (2019-07, 2025-01) ma 0.9998 su 2025-02-15T12
N094 | NON_TROVATA | — | "30–60 % tree cover" non compare; #12 cita solo le righe 'Woody Savannas' della tabella
N096 | NON_TROVATA | — | 16.2 % delle celle vegetate non compare in issue né in docs/audit
N098 | NON_TROVATA | #25 commento 2026-09-22 (solo il totale) | 1 069 456 non trovato; confermato solo il totale "1 304 109 land"
N099 | NON_TROVATA | — | 187 378 non compare
N100 | NON_TROVATA | — | 45 450 non compare
N101 | NON_TROVATA | — | 1 498 non compare
N102 | NON_TROVATA | — | 327 (slt very fine) non compare
N103 | CONFERMATA_CON_DIFFERENZE | #24 commento 2026-09-22; docs/audit/exclusions.md (TMN) | espliciti solo "the 0–7 cm average" e "`stl4` over 100-289 cm"; 7–28 e 28–100 non trovati
N104 | CONFERMATA_CON_DIFFERENZE | #24 commento 2026-09-22 | "4 × 6" non scritto; la fonte: "row sums exactly 1.0, all four", nodi "(0,1,2), (1,2,3), (2,3,4), (3,4,5)" su 6 ZS

## Conteggi
CONFERMATA: 48
CONFERMATA_CON_DIFFERENZE: 11
CONTRADDETTA: 0
NON_TROVATA: 11
NON_VERIFICABILE: 2
