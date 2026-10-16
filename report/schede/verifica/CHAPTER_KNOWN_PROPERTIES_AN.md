# Verifica: CHAPTER_KNOWN_PROPERTIES (A e N)
A001 | NON_VERIFICABILE | #58 [corpo] | metadato del documento ("beside CHAPTER_VARIABLES.md and MISSING_VARIABLES.md")
A004 | NON_VERIFICABILE | — | metadato: scopo del documento
A005 | NON_VERIFICABILE | — | metadato: perimetro del documento
A006 | NON_VERIFICABILE | #49 [commento 2026-09-25] | metadato; nota: #49 chiama la finestra di 10fg "the number is right and the label is wrong", documentata e non riparata
A007 | CONFERMATA | #58 [corpo; commento 2026-09-28] | "Not a place for the repaired defects. A defect fixed before the rebuild does not belong in a document about the archive that ships."
A008 | CONFERMATA | #58 [corpo] | "The other kind says the archive is correct and surprising ... a user who does not know will misread the field."
A009 | NON_VERIFICABILE | — | affermazione generale sul documento
A011 | CONFERMATA | #15 [corpo]; #48 [corpo] | "Upscale WRF to ERA5, area-weighted"; "Sample means over the 34 audit timesteps, upscaled to the ERA5 grid"
A012 | NON_VERIFICABILE | — | struttura del documento
A013 | NON_VERIFICABILE | — | struttura del documento
A014 | NON_VERIFICABILE | — | struttura del documento
A015 | NON_VERIFICABILE | — | categoria redazionale del documento
A016 | NON_VERIFICABILE | — | categoria redazionale del documento
A017 | CONFERMATA | #53 [corpo]; #59 [corpo] | "Counted over a whole grib_v3 file ... All 246."; la data "from 2026-09-29 onward" è metadato
A018 | CONFERMATA | #59 [corpo] | "The repairs that block — all done, 2026-09-25"; "the other six are merged and verified"
A019 | CONFERMATA | #55 [commento 2026-09-29]; #59 [commento 2026-09-29] | "EMISS_SNOWC_FULL 0.01 → 0.015 ... This changes the published skt in every file."
A020 | CONFERMATA_CON_DIFFERENZE | #55 [commento 2026-09-29] | la fonte non misura uno spostamento di 0.05 K: 0.05 K è il livello dell'RMSE (0.05766 → 0.05384 K, "6.6 % less skt derivation error"), cioè il cambio vale ~0.004 K
A021 | NON_VERIFICABILE | — | rimando interno; nota: le cifre skt stanno in §2.3, non in "section 4"
A023 | CONFERMATA | #58 [commento 2026-09-28] | "files written before 2026-09-25 carry six repaired defects and should be replaced rather than reconciled"
A024 | CONFERMATA | #58 [commento 2026-09-28] | "should be replaced rather than reconciled"
A044 | CONFERMATA | #45 [commento 2026-09-25]; #57 [corpo] | "a reader given the radiation findings alone would predict a warm land surface and be wrong"
A045 | CONFERMATA | #12 [corpo §o]; #45 [corpo] | "RRTMG ran with a CAM ozone climatology and no aerosol at all"
A047 | CONFERMATA | #45 [corpo] | "ERA5 carries the Tegen aerosol climatology."
A048 | CONFERMATA | #45 [corpo]; #22 | "an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about that much, which is the right order for the 8.5 per cent"
A056 | CONFERMATA | #45 [corpo] | "ssrdc surface solar down, clear sky ... the atmosphere alone, no clouds"
A057 | CONFERMATA | #45 [corpo] | "The thermal fields are untouched by it"
A059 | CONFERMATA | #45 [corpo] | "which is the control that makes the solar attribution credible rather than a guess"
A061 | CONFERMATA | #45 [corpo] | "It is a property of the run, not of the conversion, and it cannot be removed after the fact."
A070 | CONFERMATA | #48 [corpo] | "the converter uses maximum-random"
A071 | CONFERMATA | #48 [corpo] | "ECMWF's is exponential-random ... which yields more cover for the same layer fractions. Right direction, wrong size."
A072 | CONFERMATA | #48 [corpo] | "Random overlap is the most total cover any assumption can extract from a given profile."
A074 | CONFERMATA | #48 [corpo] | "because CLDFRA is strongly bimodal (of 108.79 M cells ... 98.18 M below 0.09 and 5.59 M above 0.91)"
A079 | CONFERMATA | #48 [corpo] | "The condensate is there; the fraction the scheme assigns to it is not."
A080 | CONFERMATA | #48 [corpo] | "Part of the gap is resolution, not error."
A081 | CONFERMATA | #48 [corpo] | "Our tcc is overlapped at 3 km and then averaged to 31 km"
A082 | CONFERMATA | #48 [corpo] | "ERA5's is overlapped on an already-smooth 31 km profile, which yields somewhat more cover"
A084 | CONFERMATA | #48 [corpo; commento 2026-09-29] | "it is real and the number should not be quoted as if it were all model error"
A086 | CONFERMATA | #57 [corpo] | "Two other findings from this audit say the opposite" (#45, #48)
A090 | CONFERMATA | #57 [corpo] | "The sea number is the control, and it clears the conversion"
A091 | CONFERMATA | #57 [corpo] | "Over open water the model's skin temperature is the SST"
A092 | CONFERMATA | #57 [corpo] | "both reanalyses see nearly the same one"
A094 | CONFERMATA | #57 [corpo] | "More shortwave reaching the ground and less cloud overhead both put energy into the land surface, and the surface is colder"
A096 | CONFERMATA | #57 [corpo] | "That is not a contradiction in the measurements; it is an unexplained partition."
A097 | CONFERMATA | #57 [corpo] | "Reconciling it needs the surface energy budget"
A099 | CONFERMATA | #57 [corpo]; #45 [commento 2026-09-25] | "The partition cannot be resolved from this archive: HFX, LH and the ground heat flux are exactly what it does not carry."
A100 | CONFERMATA | #57 [corpo] | "RUC partitioning more of the available energy into latent heat, a different soil-moisture climate, the resolved 3 km orography ..., or a genuine cold bias"
A105 | CONFERMATA | #56 [corpo] | "ERA5's fsr is an effective roughness that carries the orographic drag IFS parameterises at 31 km."
A106 | CONFERMATA | #56 [corpo; commento 2026-09-29] | "fsr is WRF's local ZNT"
A107 | CONFERMATA | #56 [corpo] | "WRF's ZNT is the local surface roughness of the land-use class"
A108 | CONFERMATA | #56 [corpo] | "the orography is resolved at 3 km instead of parameterised"
A109 | CONFERMATA | #56 [corpo] | "Over sea the two archives agree: both roughnesses are Charnock"
A113 | CONFERMATA | #56 [corpo] | "Nothing is capped, clipped or mis-scaled; leg B is exact against ZNT to 3e-8."
A115 | CONFERMATA | #56 [corpo] | "one who computes a drag coefficient from our fsr and compares it against ERA5's will find a discrepancy that is not there"
A119 | CONFERMATA | #56 [corpo] | "at 3 km the terrain-driven wind is resolved rather than smoothed, and the friction velocity responds to it"
A123 | CONFERMATA | #29 [corpo] | "TSK | not written out | correct, and now known to be a Registry decision rather than an accident"
A126 | CONFERMATA | #55 [corpo] | "The skt derivation is confirmed, and this issue is not about it being wrong."
A132 | CONFERMATA_CON_DIFFERENZE | #55 [commento 2026-09-29]; #28 [corpo] | flat 0.98 solo sopra soglia: "it blends below the threshold and goes flat above" (soglia SNOWC 0.015 dal 2026-09-29)
A133 | CONFERMATA | #55 [corpo; commento 2026-09-29] | "The switch does fire early, as this issue said — by half of what it estimated."
A134 | CONFERMATA_CON_DIFFERENZE | #55 [corpo]; #57 [corpo] | non "exact" ma "0.0005 K RMSE, bias −0.0002 K, absmax 0.002 K, on ~910 000 points"
A137 | CONFERMATA | #55 [commento 2026-09-29]; #57 [commento 2026-09-29] | "this derivation error is thirty times smaller than the physical cold bias of the land skin itself"
A138 | CONFERMATA | #58 [corpo] | "this is the single most likely misreading of the archive and needs the plainest sentence in the document"
A142 | CONFERMATA | #40 [commento 2026-09-22 13:56] | "The two conventions, and both are right ... Not an inconsistency"
A145 | CONFERMATA | #40 [commento 2026-09-22 13:07] | "Cy41r2 because that is the cycle ERA5 was produced with"
A146 | CONFERMATA | #40 [commento 2026-09-25 15:13]; #59 [corpo] | "r is now ECMWF's paramId 157"; ratio vs ERA5 "0.505 → 0.945 at 100 hPa"
A149 | CONFERMATA | #40 [commento 2026-09-22 13:56] | "ERA5 publishes no 2 m relative humidity at all"
A150 | CONFERMATA | #40 [commento 2026-09-25 15:02] | "that is the WMO convention for a screen-level humidity"
A152 | CONFERMATA | #58 [commento 2026-09-28] | "recompute from q, t and sp if you need them on one convention, all three being published"
A154 | CONFERMATA | #58 [corpo]; #40 [corpo] | "the clip is gone because supersaturation is physical and the model produces it"; "ERA5 publishes r above 100"
A165 | CONFERMATA | #42 [commento 2026-09-25] | "Clipping 2d to 2t removes the crossings and leaves the same 0.0133 K everywhere else"
A166 | CONFERMATA | #42 [commento 2026-09-25] | "with a kink in the field at exactly RH 100"
A169 | NON_TROVATA | — | nessuna fonte suggerisce di clippare la propria ricostruzione
A175 | CONFERMATA | #44 [corpo] | "it is reading the near-surface air instead, which is a far more defensible thing to publish"
A181 | CONFERMATA | #44 [corpo] | "Both messages are in the same file."
A183 | CONFERMATA | #44 [corpo] | "ERA5 extrapolates below ground with a lapse rate."
A184 | CONFERMATA | #44 [corpo] | "the two archives differ in convention exactly where 1000 hPa is underground, which is most of the land"
A188 | CONFERMATA | #44 [commento 2026-09-29] | "mask the levels against sp, and every field required to do it is in the same file"
A194 | CONFERMATA | #39 [commento 2026-09-25 14:25] | "The two cannot both be honoured ... There is no third position where both hold"
A197 | NON_TROVATA | — | nessuna fonte descrive le scale del gust non risolte a 31 km
A198 | NON_TROVATA | — | la formula del gust ERA5 (turbolenza, downdraught) non compare; #50 dice solo "parameterised gust"
A199 | NON_TROVATA | #50 [corpo] | solo "ERA5's is a parameterised gust"; non la caratterizzazione come stima di ciò che non risolve
A200 | CONFERMATA | #50 [corpo]; #23 | "maximum of the resolved 10 m wind speed over the output hour ... not produced by a gust scheme"
A207 | CONFERMATA | #50 [corpo] | "ERA5's is a parameterised gust roughly 1.6 times the mean wind"
A209 | CONFERMATA | #50 [commento 2026-09-29]; #59 [commento 2026-09-28] | "a downscaling inherits the flow, not the diagnostics"
A210 | NON_TROVATA | — | elenco delle condizioni al contorno non presente nelle fonti
A211 | NON_TROVATA | — | post-processing IFS del gust non descritto nelle fonti
A212 | NON_TROVATA | — | nessuna fonte afferma esplicitamente che la run non scrisse un proprio gust diagnostic
A213 | CONFERMATA_CON_DIFFERENZE | #50 [corpo] | la fonte dice "It behaves like a gust and is the best proxy available", non "the one gust-like field"
A215 | NON_TROVATA | — | l'argomento dell'incremento di gust minore a 3 km non compare (solo zust 1.6–2.1x in #56)
A217 | CONFERMATA | #50 [corpo; commento 2026-09-29] | "not a bias to be corrected downstream; it is a different quantity"
A219 | CONFERMATA | #59 [commento 2026-09-28 15:40]; #50 [corpo] | "ERA5's window is also one hour, so the window length is not the difference"
A221 | CONFERMATA | #49 [corpo] | "stepType = max, stepRange = 0-1 ... reference time H−1 ... all of which was verified correct"
A222 | CONFERMATA | #49 [corpo]; #60 [corpo] | "WSPD10MAX was not reset at the history write"
A228 | CONFERMATA | #49 [corpo] | "this makes the affected hours closer to ERA5's gust (#50) for the wrong reason ... the error is not detectable from the value"
A230 | CONFERMATA | #49 [commento 2026-09-25 16:18] | "The previous hour's wrfout is not on disk when the convert runs."
A231 | CONFERMATA | #49 [commento 2026-09-25 16:18] | "All seven nwp_diagnostics maxima reset on the same alarm ... none can witness for another."
A232 | CONFERMATA | #49 [corpo] | "The census correlates with timestep variability"
A233 | CONFERMATA | #49 [corpo] | "Establishing the mechanism ... has not been done."
A252 | CONFERMATA | #47 [corpo] | "the sum of water vapour, liquid water, cloud ice, rain and snow — five species"
A254 | CONFERMATA_CON_DIFFERENZE | #47 [corpo; commento 2026-09-29]; #35 | il corpo dice "ERA5 has no parameter for one"; il commento corregge: ECMWF definisce 260028 grle e 260001 tcolg, "ERA5 publishes neither"
A262 | CONFERMATA | #47 [corpo] | "Drop graupel from tcw, making it ECMWF's definition exactly and the closure identity hold, at the cost of the graupel mass leaving the archive"
A265 | CONFERMATA | #36 [commento 2026-09-25 15:41]; #54 [corpo] | "both as a bitmap"; "A masked field teaches unknown here" (cl resta zero sul mare, non mascherato)
A269 | CONFERMATA | #25 [corpo]; #63 [corpo] | "tvl is masked on 124 672 shrubland cells, because MODIS carries no shrub phenology"; "rather have a guess than a gap"
A270 | CONFERMATA | #25 [corpo]; #03 | "slt is NaN off geo_em's permanent land mask"
A272 | CONFERMATA | #36 [commento 2026-09-25 15:41] | "'Water, minus the cells geo_em calls lake' is circular: the defect is that geo_em calls the Black Sea a lake."
A273 | CONFERMATA | #36 [corpo] | "The Sea of Azov (4702 cells) and part of the Baltic (3013 cells) ... Together they are 89 % of the 55 881 cells the archive calls fully lake"
A274 | CONFERMATA | #36 [commento 2026-09-25 15:41] | la cura per classe lago è "circular" perché geo_em chiama lago il Mar Nero
A275 | CONFERMATA | #36 [commento 2026-09-25 15:41] | "Component size works, with a factor of seven of slack"
A276 | CONFERMATA | #36 [commento 2026-09-25 15:41] | "844 431 ... 49 841 Black Sea + Sea of Azov ... 8 583 Red Sea ... 1 225 Vänern, the largest inland lake"
A277 | CONFERMATA | #36 [commento 2026-09-25 15:41] | "Nothing lies between 1 225 and 8 583 ... factor of seven of slack"
A281 | CONFERMATA | #38 [commento 2026-09-25 12:25] | "The values discarded are the model's own, but 1.000 ... is an artefact of the hourly reclassification, not a measurement"
A282 | CONFERMATA | #38 [corpo] | "where ERA5 has no soil at all, because its land-sea mask is permanent"
A283 | CONFERMATA | #38 [corpo] | "ci is published so nothing is lost that cannot be recovered"
A285 | CONFERMATA | #38 [corpo] | "When a water cell carries sea ice, WRF makes it land (LANDMASK 0→1)"
A289 | CONFERMATA | #54 [corpo] | "The archive writes 0, which reads as 'nothing is stopping convection', precisely where the most is."
A290 | CONFERMATA | #54 [corpo] | "A column with no CAPE is normally a column with a great deal of inhibition — that is usually why there is no CAPE."
A300 | CONFERMATA | #54 [corpo] | "our CIN exists only in columns with CAPE ≥ 100, i.e. the least inhibited ones, while ERA5 reports it more widely"
A301 | CONFERMATA | #54 [corpo] | "a model trained on it learns that low-CAPE situations have zero convective inhibition, which is the inverse of the physics"
A322 | CONFERMATA | #37 [corpo] | "paramId 163 is defined as the slope of the sub-grid orography"
A323 | CONFERMATA | #37 [corpo; commento 2026-09-29] | "eccodes shows the parameter's own name, Slope of sub-gridscale orography, so a user reading the message sees nothing"
A332 | CONFERMATA | #35 [corpo] | "The exclusions stand either way."
A333 | CONFERMATA_CON_DIFFERENZE | #50 [corpo]; #47 [corpo] | la regola completa è "published only if the WRF quantity is the ERA5 one, or the difference can be stated in one line"
A337 | CONFERMATA | #17 [corpo]; #12 [corpo] | "one LAI per cell, ERA5 wants one per class"
A340 | NON_VERIFICABILE | #58 [commento 2026-09-28] | metadato (la data di scrittura coincide con "Written and merged" del 2026-09-28)
N002 | CONFERMATA | #53 [corpo] | "All 246."
N003 | CONFERMATA | #59 [corpo] | "the other six are merged and verified"
N004 | CONFERMATA_CON_DIFFERENZE | #55 [commento 2026-09-29] | 0.05 K è l'RMSE di derivazione pooled (0.05766 → 0.05384 K), non lo spostamento; il cambio è "6.6 %" (~0.004 K)
N025 | CONFERMATA | #56 [corpo]; #48 [corpo] | "IFS parameterises at 31 km ... resolved at 3 km"
N026 | CONFERMATA | #45 [corpo] | "an aerosol optical depth of 0.1 to 0.2"
N063 | CONFERMATA | #28 [corpo]; #55 [commento 2026-09-29] | "flat 0.98"; "goes flat above" la soglia
N064 | CONFERMATA_CON_DIFFERENZE | #55 [commento 2026-09-29 07:51]; #57 [commento 2026-09-29] | "thirty times smaller" riferito a 0.115–0.133 K, misurato con la soglia 0.01; docs/audit/f8 riporta 0.084–0.119 K con 0.015
N065 | CONFERMATA | #40 [commento 2026-09-25 15:02] | "2r is paramId 260242, not 157"
N089 | CONFERMATA | #50 [corpo] | "Published under paramId 49, 10fg is the 10 m wind speed with a two-per-cent premium"
N090 | CONFERMATA | #50 [corpo] | "a parameterised gust roughly 1.6 times the mean wind"
N099 | CONFERMATA | #49 [commento 2026-09-25 16:18]; #60 [corpo] | "All seven nwp_diagnostics maxima reset on the same alarm"
N112 | CONFERMATA | #47 [corpo] | "ECMWF defines paramId 136 tcw"
N119 | CONFERMATA | #36 [corpo] | "LANDUSEF fraction of MODIS class 21 ... Together they are 89 % of the 55 881 cells the archive calls fully lake"
N120 | CONFERMATA | #36 [commento 2026-09-25 15:41] | "844 431 | Atlantic + Mediterranean + Baltic + North Sea ... 49 841 ... 8 583 ... 1 225"
N121 | CONFERMATA | #36 [commento 2026-09-25 15:41] | "Component size works, with a factor of seven of slack"
N133 | CONFERMATA | #37 [corpo] | "paramId 163 is defined as the slope of the sub-grid orography"
N136 | NON_VERIFICABILE | — | metadato del documento

## Conteggi
CONFERMATA: 111
CONFERMATA_CON_DIFFERENZE: 8
CONTRADDETTA: 0
NON_TROVATA: 8
NON_VERIFICABILE: 13
