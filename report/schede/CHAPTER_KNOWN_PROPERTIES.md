# Scheda: CHAPTER_KNOWN_PROPERTIES.md
Fonte: /leonardo/home/userexternal/lmonaco0/CHAPTER/CHAPTER_KNOWN_PROPERTIES.md (658 righe), letta il 2026-09-29

Convenzione sezioni: §intro = testo prima di "How to read" (r.1-17); §How = "How to read this document"; §Which = "Which archive this describes"; §0 = "The short list"; §1.1 ... §8.4 = sottosezioni numerate; §Where = "Where the measurements live".

## 1. Affermazioni

A001 Third of the three documents that ship with this archive [SENZA FONTE] (§intro, r.3)
A002 `CHAPTER_VARIABLES.md` says what is in the files [SUPPORTATA: CHAPTER_VARIABLES.md] (§intro, r.3)
A003 `MISSING_VARIABLES.md` says what is not and why [SUPPORTATA: MISSING_VARIABLES.md] (§intro, r.4)
A004 This document answers: what is in the files that will surprise you [SENZA FONTE] (§intro, r.5)
A005 Everything below is a property of the data as delivered [SENZA FONTE] (§intro, r.7)
A006 None of it is a defect awaiting repair [SENZA FONTE] (§intro, r.7-8)
A007 The defects the audit found were repaired before the archive was produced, and are not listed here [SENZA FONTE] (§intro, r.8-9)
A008 What is listed is the archive behaving correctly in ways a user comparing it against ERA5, observations or expectations will otherwise discover alone [SENZA FONTE] (§intro, r.9-11)
A009 Every number here was measured, not estimated [SENZA FONTE] (§intro, r.13)
A010 Numbers come from a variable-by-variable audit run in September 2026 over a 34-timestep sample spanning both sampled years and all four seasons [SUPPORTATA: docs/audit/sample.md] (§intro, r.13-15)
A011 Where a comparison against ERA5 is quoted, the 3 km field was upscaled to the ERA5 grid first [SENZA FONTE] (§intro, r.15-16)
A012 Each entry links to the issue that holds the measurement and the method [SENZA FONTE] (§intro, r.16-17)
A013 Section 0 is the short list: the things that change what you do, in one line each [SENZA FONTE] (§How, r.21)
A014 Two kinds of entry are mixed together deliberately [SENZA FONTE] (§How, r.24)
A015 Properties of the run: the model was configured a certain way and the data reflect it; nothing can be done after the fact; the run would have to be repeated [SENZA FONTE] (§How, r.27-28)
A016 Properties of the conversion: a deliberate convention, chosen and documented; could be changed; the entry says what was chosen instead and why [SENZA FONTE] (§How, r.29-30)
A017 The document describes the GRIB2 archive `grib_v3`, 246 messages per hourly file, as produced by the converter from 2026-09-29 onward [SENZA FONTE] (§Which, r.34-35)
A018 The six repairs landed on 2026-09-25 [SENZA FONTE] (§Which, r.35)
A019 One further change on 2026-09-29 moved the snow-emissivity threshold [SENZA FONTE] (§Which, r.35-36)
A020 That change shifts `skt` over snow-covered land by about 0.05 K RMSE [SENZA FONTE] (§Which, r.36-37)
A021 That change is already reflected in the figures in section 4 [SENZA FONTE] (§Which, r.37)
A022 Files written before that date carry six defects repaired on that date: relative humidity, specific humidity, the column integrals, snowfall, the water masks and convective inhibition [SUPPORTATA: docs/audit/re-verification.md] (§Which, r.37-40)
A023 Those defects are not properties of this archive [SENZA FONTE] (§Which, r.40-41)
A024 Holders of files from before the rebuild should replace them rather than reconcile them [SENZA FONTE] (§Which, r.41)
A025 Short list 1.1: surface shortwave is high under clear sky; the run carried no aerosol [SUPPORTATA: #45 (§1.1)] (§0, r.47)
A026 Short list 1.2: total cloud cover is low, high cloud lowest; it is `CLDFRA`, not the overlap [SUPPORTATA: #48 (§1.2)] (§0, r.48)
A027 Short list 1.3: land skin temperature is cold, and the archive cannot say why [SUPPORTATA: #57 (§1.3)] (§0, r.49)
A028 Short list 2.1: `fsr` is WRF's local roughness, ERA5's is effective [SUPPORTATA: #56 (§2.1)] (§0, r.50)
A029 Short list 2.2: `zust` over land responds to resolved terrain [SUPPORTATA: #56 (§2.2)] (§0, r.51)
A030 Short list 3.1: `r` and `2r` saturate differently, and each is right; mixed phase vs liquid water [SUPPORTATA: #40 (§3.1)] (§0, r.52)
A031 Short list 3.2: `r` above 100 % is normal and is not clipped [SUPPORTATA: #40, #44 (§3.2)] (§0, r.53)
A032 Short list 3.3: humidity rebuilt from `2t` and `2d` overshoots at saturation [SUPPORTATA: #42 (§3.3)] (§0, r.54)
A033 Short list 4.1: below ground the pressure levels are clamped, not extrapolated; ERA5 extrapolates [SUPPORTATA: #44 (§4.1)] (§0, r.55)
A034 Short list 4.2: `z` is exactly `9.80665 × z_WRF`; WRF integrated with 9.81 [SUPPORTATA: #39 (§4.2)] (§0, r.56)
A035 Short list 5.1: `10fg` is the resolved 10 m wind, not a gust parameterisation [SUPPORTATA: #50 (§5.1)] (§0, r.57)
A036 Short list 5.2: its declared one-hour window is right 88 % of the time [SUPPORTATA: #49 (§5.2)] (§0, r.58)
A037 Short list 6.1: three runoff variables carry one field's information [SUPPORTATA: #51 (§6.1)] (§0, r.59)
A038 Short list 6.2: `tcw` sums six species where ECMWF defines five [SUPPORTATA: #47 (§6.2)] (§0, r.60)
A039 Short list 7.1: one masking rule: a point is missing where the ERA5 parameter is undefined; bitmaps, never zeros [SUPPORTATA: #34, #36, #38 (§7.1)] (§0, r.61)
A040 Short list 7.2: `mucin` is masked, not zero-filled, where the scheme declined [SUPPORTATA: #54 (§7.2)] (§0, r.62)
A041 Short list 8.1: `generatingProcessIdentifier = 128` marks every message and discriminates nothing [SUPPORTATA: #53 (§8.1)] (§0, r.63)
A042 Short list 8.2: `al` is a two-season table value by category, not a continuous field [SUPPORTATA: #37 (§8.2)] (§0, r.64)
A043 Short list 8.3: `slor` is the slope of the resolved 3 km terrain, not of sub-grid orography; eccodes shows the ECMWF name [SUPPORTATA: #37 (§8.3)] (§0, r.65)
A044 Radiation, cloud and surface energy budget belong together; read any one alone and you will predict the other two wrongly [SENZA FONTE] (§1, r.71-72)
A045 RRTMG ran with a CAM ozone climatology [SENZA FONTE] (§1.1, r.76)
A046 RRTMG ran with no aerosol at all [SUPPORTATA: namelist aer_opt = 0] (§1.1, r.76-77)
A047 ERA5 carries the Tegen aerosol climatology [SENZA FONTE] (§1.1, r.77)
A048 Over Europe, the Mediterranean and the Saharan margin an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about the amount measured [SENZA FONTE] (§1.1, r.77-79)
A049 Clear-sky surface solar down ratio vs ERA5 is 1.085 [SUPPORTATA: #45, sample means] (§1.1, r.85)
A050 All-sky surface solar down ratio vs ERA5 is 1.136 [SUPPORTATA: #45] (§1.1, r.86)
A051 Clear-sky surface net solar ratio vs ERA5 is 1.116 [SUPPORTATA: #45] (§1.1, r.87)
A052 All-sky surface net solar ratio vs ERA5 is 1.178 [SUPPORTATA: #45] (§1.1, r.88)
A053 Top net solar clear-sky ratio vs ERA5 is 1.031 [SUPPORTATA: #45] (§1.1, r.89)
A054 Downward thermal `strd`, `strdc` ratios vs ERA5 are 0.989, 0.996 [SUPPORTATA: #45] (§1.1, r.90)
A055 Outgoing thermal `ttr`, `ttrc` ratios vs ERA5 are 1.009, 0.990 [SUPPORTATA: #45] (§1.1, r.91)
A056 The clear-sky figure isolates the atmosphere with no cloud involved [SENZA FONTE] (§1.1, r.93-94)
A057 The thermal fields are untouched by aerosol [SENZA FONTE] (§1.1, r.94)
A058 The thermal fields agree with ERA5 to within 1.1 % [SUPPORTATA: #45] (§1.1, r.94-95)
A059 This agreement is the control that makes the attribution credible rather than a guess [SENZA FONTE] (§1.1, r.95)
A060 For solar resource, energy applications or training against pyranometer observations, expect a systematic high bias in surface shortwave of about this size [SUPPORTATA: #45] (§1.1, r.97-99)
A061 The shortwave bias is a property of the run and cannot be removed after the fact [SENZA FONTE] (§1.1, r.99-100)
A062 Total cloud cover runs 22 % below ERA5, high cloud 39 % below [SUPPORTATA: #48, sample means upscaled to ERA5 grid] (§1.2, r.102-104)
A063 `tcc` ours 0.381, ERA5 0.487, ratio 0.783 [SUPPORTATA: #48] (§1.2, r.108)
A064 `hcc` ours 0.169, ERA5 0.276, ratio 0.610 [SUPPORTATA: #48] (§1.2, r.109)
A065 `mcc` ours 0.161, ERA5 0.205, ratio 0.786 [SUPPORTATA: #48] (§1.2, r.110)
A066 `lcc` ours 0.231, ERA5 0.268, ratio 0.862 [SUPPORTATA: #48] (§1.2, r.111)
A067 `tciw` ours 0.0185, ERA5 0.0166, ratio 1.109 [SUPPORTATA: #48] (§1.2, r.112)
A068 The deficit holds at every one of the 34 timesteps, both years, every month [SUPPORTATA: #48, 34-timestep sample] (§1.2, r.114)
A069 The deficit is not the overlap assumption, and that was checked first [SUPPORTATA: #48] (§1.2, r.116)
A070 The converter uses maximum-random overlap [SENZA FONTE] (§1.2, r.116-117)
A071 ECMWF uses exponential-random overlap, which would yield more cover — the right direction [SENZA FONTE] (§1.2, r.117-118)
A072 Random overlap is the most total cover any assumption can extract from a given profile [SENZA FONTE] (§1.2, r.118-119)
A073 Computed point by point on our own `CLDFRA`, the entire span of possible overlap assumptions is only 2 to 4 % wide [SUPPORTATA: #48] (§1.2, r.119-120)
A074 `CLDFRA` is strongly bimodal [SENZA FONTE] (§1.2, r.120)
A075 ERA5 is 28 % above us [SUPPORTATA: #48] (§1.2, r.120)
A076 The overlap accounts for at most a seventh of the gap [SUPPORTATA: #48] (§1.2, r.121)
A077 The gap is in `CLDFRA` itself, WRF's Xu–Randall diagnostic under `ICLOUD = 1` [SUPPORTATA: namelist ICLOUD = 1] (§1.2, r.123)
A078 We carry 11 % more cloud ice than ERA5 and diagnose 39 % less high cloud [SUPPORTATA: #48] (§1.2, r.124)
A079 The condensate is there; the fraction the scheme assigns to it is not [SENZA FONTE] (§1.2, r.124-125)
A080 Part of the gap is resolution [SENZA FONTE] (§1.2, r.127)
A081 Our `tcc` is overlapped at 3 km and then averaged to 31 km [SENZA FONTE] (§1.2, r.127-128)
A082 ERA5's `tcc` is overlapped on an already-smooth 31 km profile, which yields somewhat more cover [SENZA FONTE] (§1.2, r.128-129)
A083 The resolution effect is bounded by the same 2–4 % span, so it cannot account for 22 % [SUPPORTATA: #48] (§1.2, r.129-130)
A084 The resolution effect is real; the figure should not be quoted as if it were all model error [SENZA FONTE] (§1.2, r.130-131)
A085 Land skin temperature runs 1.6 K below ERA5, 3.2 K at midday [SUPPORTATA: #57, mean over the whole sample] (§1.3, r.133-135)
A086 The land cold bias contradicts §1.1 and §1.2 [SENZA FONTE] (§1.3, r.133)
A087 `skt` sea bias vs ERA5 +0.01 K, correlation 0.95–0.98 [SUPPORTATA: #57] (§1.3, r.139)
A088 `skt` land bias vs ERA5 −1.64 K, reaching −3.24 K at midday, correlation 0.95–0.98 [SUPPORTATA: #57] (§1.3, r.140)
A089 At 00Z the land bias is −0.5 to −1.2 K; at 12Z it is −0.8 to −3.2 K [SUPPORTATA: #57] (§1.3, r.142)
A090 The sea number is the control [SENZA FONTE] (§1.3, r.144)
A091 Over open water the model's skin temperature is the SST [SENZA FONTE] (§1.3, r.144-145)
A092 Both reanalyses see nearly the same SST [SENZA FONTE] (§1.3, r.145)
A093 A +0.01 K sea bias says the derivation, the emissivity and the encoding are not the cause of anything; the land bias is the run [SUPPORTATA: #57, rimando a §2.3] (§1.3, r.145-146)
A094 More shortwave reaching the ground and less cloud overhead both put energy into the land surface, and the surface comes out colder [SENZA FONTE] (§1.3, r.148-149)
A095 The land surface is coldest at the hour when the excess solar is largest [SUPPORTATA: #57] (§1.3, r.149-150)
A096 This is not a contradiction in the measurements; it is an unexplained partition [SENZA FONTE] (§1.3, r.150-151)
A097 Reconciling it needs the surface energy budget [SENZA FONTE] (§1.3, r.151)
A098 `HFX`, `LH` and the ground heat flux are the three fields this archive does not have [SUPPORTATA: MISSING_VARIABLES.md] (§1.3, r.151-153)
A099 The partition cannot be settled from the published data [SENZA FONTE] (§1.3, r.153)
A100 Candidates that cannot be separated: the land-surface scheme partitioning more energy into latent heat; a different soil-moisture climate; the resolved 3 km orography raising the mean elevation of an upscaled land cell; a genuine cold bias [SENZA FONTE] (§1.3, r.153-156)
A101 For `skt` over land in evaluation, bias correction or ML training against satellite LST, apply the number [SUPPORTATA: #57] (§1.3, r.158-159)
A102 Do not predict a warm land surface from the radiation findings; the archive does the opposite [SUPPORTATA: #57] (§1.3, r.159-161)
A103 `fsr` land ours 0.188–0.217 m, ERA5 0.375–0.394 m, ratio of medians 0.32–0.48 [SUPPORTATA: #56] (§2.1, r.171)
A104 `fsr` sea ours 0.0089–0.0091 m, ERA5 0.0103–0.0105 m, ratio of medians 1.5–1.9 [SUPPORTATA: #56] (§2.1, r.172)
A105 ERA5's `fsr` is an effective roughness that carries the orographic drag the IFS parameterises at 31 km [SENZA FONTE] (§2.1, r.174-175)
A106 This archive's `fsr` is WRF's `ZNT` [SENZA FONTE] (§2.1, r.175-176)
A107 `ZNT` is the local surface roughness of the land-use class [SENZA FONTE] (§2.1, r.176)
A108 The orography is resolved at 3 km instead of parameterised [SENZA FONTE] (§2.1, r.176)
A109 Over sea the two agree, because both are Charnock [SENZA FONTE] (§2.1, r.177)
A110 `ZNT` is a land-use lookup with a snow override: one value per category [SUPPORTATA: #56] (§2.1, r.179)
A111 `ZNT` values: 0.70 m for the forest classes, 0.15 for savannas and grassland, 0.065 for barren, exactly 1.00 m on the 19 867 urban points [SUPPORTATA: #56] (§2.1, r.179-181)
A112 `ZNT` has a floor of 0.011 m where snow covers the surface [SUPPORTATA: #56] (§2.1, r.181)
A113 Nothing is capped or mis-scaled [SENZA FONTE] (§2.1, r.181)
A114 Over land `fsr` of this archive and of ERA5 differ by a factor of two to three; they are not the same quantity [SUPPORTATA: #56] (§2.1, r.183-184)
A115 A drag coefficient computed from ours and compared against one from ERA5's will show a discrepancy that is not physical [SENZA FONTE] (§2.1, r.184-185)
A116 `zust` land ours 0.44–0.52 m/s, ERA5 0.23–0.28 m/s, ratio 1.62–2.06 [SUPPORTATA: #56] (§2.2, r.192)
A117 `zust` sea ours 0.21–0.34 m/s, ERA5 0.19–0.31 m/s, ratio 1.08–1.12, corr 0.85–0.90 [SUPPORTATA: #56] (§2.2, r.193)
A118 Our roughness is a third of ERA5's while our friction velocity is twice it; those cannot both be a scaling error on the same `z0` [SUPPORTATA: #56] (§2.2, r.195-197)
A119 At 3 km the terrain-driven wind is resolved rather than smoothed, and the friction velocity responds to it [SENZA FONTE] (§2.2, r.197-198)
A120 The `zust` excess is largest at midday: 1.06–1.13 at 00Z against 1.40–1.75 at 12Z, in every region [SUPPORTATA: #56] (§2.2, r.198-199)
A121 `|τ| = ρu*²` holds to 1.8e-6 N/m² at every point of every timestep checked [SUPPORTATA: #56] (§2.2, r.201-202)
A122 `zust = sqrt(|τ|/ρ)` holds to 2.7e-4 m/s at every point of every timestep checked [SUPPORTATA: #56] (§2.2, r.202)
A123 `TSK` was not written out by the run [SENZA FONTE] (§2.3, r.207)
A124 `skt` is inverted from the upward longwave flux [SUPPORTATA: #55] (§2.3, r.207)
A125 The per-category emissivity is measured from the run itself rather than looked up in a table [SUPPORTATA: #55] (§2.3, r.208-209)
A126 The derivation is verified [SENZA FONTE] (§2.3, r.209)
A127 What is seasonal is how well the derivation reproduces the model's own state [SUPPORTATA: #55] (§2.3, r.209-210)
A128 Water gate: `skt` against the model's own SST 0.0005 K RMSE, absmax 0.002 K, ~910 000 points, every timestep [SUPPORTATA: #55] (§2.3, r.214)
A129 Land points reproduced to 1e-4: 99.98 % in July, 93.05 % in January [SUPPORTATA: #55] (§2.3, r.215)
A130 Land `skt` RMSE from the emissivity table: 0.0012 K in July, 0.084–0.119 K in January and February, p99 0.81 K, absmax 2.79 K [SUPPORTATA: #55] (§2.3, r.216)
A131 The whole of the seasonal spread is the snow rule [SUPPORTATA: #55] (§2.3, r.218)
A132 Emissivity switches to a flat 0.98 under snow [SENZA FONTE] (§2.3, r.218-219)
A133 The switch is applied slightly earlier than the model's own transition completes [SENZA FONTE] (§2.3, r.219)
A134 Over water the derivation is exact [SENZA FONTE] (§2.3, r.220)
A135 Treat `skt` over water as the model's SST to a thousandth of a kelvin [SUPPORTATA: #55] (§2.3, r.222)
A136 Over land in winter allow a tenth of a kelvin of derivation error on top of the physical bias of §1.3 [SUPPORTATA: #55] (§2.3, r.222-224)
A137 The derivation error and the physical bias are unrelated; the derivation error is thirty times smaller [SENZA FONTE] (§2.3, r.224)
A138 The `r`/`2r` difference is the single most likely misreading of the archive [SENZA FONTE] (§3.1, r.233)
A139 `r` (paramId 157, pressure levels) is relative humidity over the mixed phase [SUPPORTATA: #40] (§3.1, r.236)
A140 `2r` (paramId 260242, 2 m) is relative humidity over liquid water at every temperature [SUPPORTATA: #40] (§3.1, r.237)
A141 `r` and `2r` are not the same quantity and will not agree at cold points [SUPPORTATA: #40] (§3.1, r.238)
A142 Each follows its own definition rather than a single house convention [SENZA FONTE] (§3.1, r.240)
A143 ECMWF paramId 157 saturates over ice below 250.16 K, over water above 273.16 K, and quadratically between [SUPPORTATA: IFS Cy41r2] (§3.1, r.242-243)
A144 The archive computes `r` from IFS Cy41r2's own equations (7.5, 7.6, 7.89, 7.90) with every constant taken from that cycle [SUPPORTATA: IFS Cy41r2] (§3.1, r.243-245)
A145 IFS Cy41r2 is the cycle ERA5 was produced with [SENZA FONTE] (§3.1, r.244-245)
A146 `r` is directly comparable with ERA5's `r` [SENZA FONTE] (§3.1, r.245)
A147 Over ice the mixed-phase and over-water definitions differ by up to a factor 1.8 [SUPPORTATA: #40] (§3.1, r.245-246)
A148 `2r` follows the WMO screen convention, which saturates over liquid water at all temperatures [SUPPORTATA: WMO screen convention (non citato per documento)] (§3.1, r.247-248)
A149 ERA5 publishes no 2 m relative humidity [SENZA FONTE] (§3.1, r.248)
A150 The WMO convention is the meteorological standard for a screen-level observation, which is what a 2 m humidity is compared against [SENZA FONTE] (§3.1, r.249-250)
A151 Do not build a profile that puts `2r` at the bottom of `r`; do not compute a vertical humidity gradient across the two [SUPPORTATA: #40] (§3.1, r.252-253)
A152 To have them on one convention, recompute from `q`, `t` and `sp`, all three published [SENZA FONTE] (§3.1, r.253-254)
A153 There is no clip on `r` [SUPPORTATA: #40] (§3.2, r.259)
A154 Supersaturation is physical, the model produces it, and ERA5 publishes it too [SENZA FONTE] (§3.2, r.259-260)
A155 `r` reaches 139.7 % at 300 hPa in the ice regime, measured on a single file [SUPPORTATA: #40, single file] (§3.2, r.260-261)
A156 34 785 points above 100 % at 400 hPa, measured on a single file [SUPPORTATA: #40, single file] (§3.2, r.261)
A157 Below ground `r` values reach up to about 163 % [SUPPORTATA: #44] (§3.2, r.263)
A158 The below-ground values are the clamping of §4.1 rather than the humidity: the lowest model level's moisture, from roughly 25 m above the terrain, read at a nominal 1000 hPa [SUPPORTATA: #44] (§3.2, r.263-265)
A159 An ingest pipeline that rejects RH above 100 will reject valid data from this archive [SUPPORTATA: #40, #44] (§3.2, r.268-270)
A160 At saturated points `2d` exceeds `2t` by a fixed 0.0133 K, on 6 000 to 64 000 points per timestep [SUPPORTATA: #42] (§3.3, r.274-275)
A161 Every violating point is at relative humidity 100 [SUPPORTATA: #42] (§3.3, r.275)
A162 It is the dewpoint inversion overshooting by a constant at exactly saturation [SUPPORTATA: #42] (§3.3, r.275-276)
A163 The constant is the same at every timestep in every season, which identifies it as arithmetic rather than noise [SUPPORTATA: #42] (§3.3, r.276-277)
A164 The overshoot was left in place deliberately [SUPPORTATA: #42] (§3.3, r.279)
A165 Clipping `2d` to `2t` would remove the visible crossings while leaving the same bias at every unsaturated point [SENZA FONTE] (§3.3, r.279-280)
A166 Clipping would put a kink in the field at RH 100 [SENZA FONTE] (§3.3, r.280)
A167 Clipping would break the exact consistency between `2d` and `Q2` that the audit verified at 3.6e-4 to 1.1e-2 in vapour pressure [SUPPORTATA: #42] (§3.3, r.280-282)
A168 Expect a reconstruction that peaks a tenth of a per cent above saturation [SUPPORTATA: #42] (§3.3, r.284)
A169 For a hard bound, clip your own reconstruction rather than reading it as an inconsistency [SENZA FONTE] (§3.3, r.284-286)
A170 Where a pressure level lies below the terrain, the archive publishes the lowest model level's value, verbatim [SUPPORTATA: #44] (§4.1, r.294-295)
A171 It is not an extrapolation and not a fill [SUPPORTATA: #44] (§4.1, r.295)
A172 `t` matches the lowest model level to exactly 0.0 at 100 % of below-ground points [SUPPORTATA: #44] (§4.1, r.295-296)
A173 `q` matches to 1e-9, `z` to 2.5e-4 m [SUPPORTATA: #44] (§4.1, r.296)
A174 The below-ground number is a real model state from about 24 to 27 m above the ground, not an invention [SUPPORTATA: #44] (§4.1, r.300-301)
A175 A user reading 1000 hPa over the Alps is reading near-surface air, more defensible than a synthetic lapse-rate extrapolation [SENZA FONTE] (§4.1, r.301-302)
A176 The archive is coherent across the surface join [SUPPORTATA: #44] (§4.1, r.302-303)
A177 `2t − t(1000 hPa)` below ground is −0.9 K at midnight and +1.4 K at noon in July [SUPPORTATA: #44] (§4.1, r.303-304)
A178 That is a nocturnal inversion and a superadiabatic daytime surface layer over a 22 m interval [SUPPORTATA: #44] (§4.1, r.304-305)
A179 `z` then contradicts `sp` [SUPPORTATA: #44] (§4.1, r.307)
A180 Where `sp` says 1000 hPa is underground, the published `z` at 1000 hPa puts it a median of 24 to 27 m above the terrain [SUPPORTATA: #44] (§4.1, r.307-309)
A181 Both messages are in the same file [SENZA FONTE] (§4.1, r.309)
A182 The self-contradiction affects 47.6 % of the domain at 1000 hPa and 9 % at 925 hPa [SUPPORTATA: #44] (§4.1, r.309-311)
A183 ERA5 extrapolates below ground with a lapse rate [SENZA FONTE] (§4.1, r.313)
A184 The two archives differ in convention exactly where 1000 hPa is underground, which is most of the land [SENZA FONTE] (§4.1, r.313-315)
A185 This difference is the whole of the 1000 hPa discrepancy against ERA5 [SUPPORTATA: #44] (§4.1, r.315)
A186 `t` bias vs ERA5 −1.71 K at 1000 hPa against −0.05 K at 850 hPa [SUPPORTATA: #44] (§4.1, r.316)
A187 `z` correlation vs ERA5 at 1000 hPa is 0.108 [SUPPORTATA: #44] (§4.1, r.316)
A188 Mask the pressure levels against `sp` yourself for a clean comparison against ERA5 or a thickness computation; every field needed is in the same file [SENZA FONTE] (§4.1, r.318-319)
A189 By construction the published geopotential is standard gravity times WRF's own geopotential height [SUPPORTATA: #39] (§4.2, r.326-327)
A190 Dividing `z` by 9.80665 recovers the model's height in metres, exactly, at the surface and on every pressure level, with no residual [SUPPORTATA: #39] (§4.2, r.327-328)
A191 WRF integrated the hydrostatic equation with 9.81 [SUPPORTATA: #39] (§4.2, r.329)
A192 The archive sits 0.034 % off hydrostatic balance against its own `t` and `p` [SUPPORTATA: #39] (§4.2, r.329-330)
A193 That is 1 part in 2 900: about 2 m at 500 hPa, 7 m at 50 hPa [SUPPORTATA: #39] (§4.2, r.330-331)
A194 Neither number can be removed without breaking the other [SENZA FONTE] (§4.2, r.333)
A195 The chosen convention makes `z` a correct ECMWF geopotential and makes surface and pressure-level geopotentials agree with each other exactly [SUPPORTATA: #39] (§4.2, r.333-335)
A196 Surface and pressure-level geopotentials agree, verified point by point over 1 349 910 land points [SUPPORTATA: #39] (§4.2, r.335-336)
A197 A 31 km model cannot see a gust: the peak happens on scales of metres and seconds it never represents [SENZA FONTE] (§5.1, r.344-345)
A198 ERA5 estimates the gust: mean 10 m wind plus a turbulence term sized from surface friction plus an allowance for convective downdraughts [SENZA FONTE] (§5.1, r.345-347)
A199 ERA5's gust is a calculated estimate of something the model does not resolve [SENZA FONTE] (§5.1, r.347-348)
A200 CHAPTER's `10fg` is the highest 10 m wind speed the simulation produced during the hour; no turbulence term, no estimate [SENZA FONTE] (§5.1, r.350-352)
A201 Ours vs ERA5 `10fg` (gust scheme, hourly max): ratio 0.625, corr 0.813 [SUPPORTATA: #50] (§5.1, r.356)
A202 Ours vs ERA5 `i10fg` (gust scheme, instantaneous): ratio 0.644, corr 0.820 [SUPPORTATA: #50] (§5.1, r.357)
A203 Ours vs our own instantaneous 10 m wind, same file: ratio 1.004–1.032 [SUPPORTATA: #50] (§5.1, r.358)
A204 Taking the maximum over an hour raises the value by half a per cent to three per cent and no more [SUPPORTATA: #50] (§5.1, r.360-361)
A205 The hourly max is below the instantaneous wind at zero points out of 2 220 273 [SUPPORTATA: #50] (§5.1, r.361-362)
A206 What is published under paramId 49 is, in practice, the 10 m wind speed [SUPPORTATA: #50] (§5.1, r.362-363)
A207 ERA5's gust runs at roughly 1.6 times its own mean wind [SENZA FONTE] (§5.1, r.363-364)
A208 The offset is a definition, not weather: 0.593 to 0.673 across all 34 sample timesteps, both years, every month, every hour [SUPPORTATA: #50, 34 timesteps] (§5.1, r.366-367)
A209 A downscaling inherits the flow, not the diagnostics [SENZA FONTE] (§5.1, r.370-371)
A210 ERA5 supplies the boundary conditions (wind, temperature, humidity, pressure); a gust is not among them [SENZA FONTE] (§5.1, r.371-372)
A211 The gust is an output of the IFS's own boundary-layer post-processing, recomputed and discarded at every step; it never enters the nested model [SENZA FONTE] (§5.1, r.372-374)
A212 This run did not write out a gust diagnostic of its own [SENZA FONTE] (§5.1, r.374-375)
A213 What is published is the one gust-like field the run produced [SENZA FONTE] (§5.1, r.375-376)
A214 At 3 km part of what ERA5 must parameterise is resolved; friction velocity over land runs 1.6 to 2.1 times ERA5's (§2.2) [SUPPORTATA: §2.2, #56] (§5.1, r.378-380)
A215 A 3 km model genuinely needs a smaller gust increment than a 31 km one — smaller, but not zero; this archive applies zero [SENZA FONTE] (§5.1, r.380-382)
A216 Reading `10fg` as a wind gust under-predicts by about 38 % [SUPPORTATA: #50] (§5.1, r.384)
A217 No bias correction repairs it, because it is a different quantity rather than a mis-scaled one [SENZA FONTE] (§5.1, r.384-385)
A218 The correlation of 0.81 means it ranks windy places and hours correctly; usable for ranking, patterns, and as a lower bound; it will not give a gust threshold [SUPPORTATA: #50] (§5.1, r.385-388)
A219 The length of the window is not the difference: ERA5's hourly gust is also a maximum over the preceding hour [SENZA FONTE] (§5.2, r.392-393)
A220 Our messages declare `stepType = max`, `stepRange = 0-1`, `typeOfStatisticalProcessing = 2`, reference time H−1 [SUPPORTATA: #49] (§5.2, r.393-394)
A221 That encoding was verified correct [SENZA FONTE] (§5.2, r.394)
A222 WRF resets `WSPD10MAX` at the history write [SENZA FONTE] (§5.2, r.397)
A223 Measured over six whole days, 138 hourly transitions, the reset was missed at 17 of them (12.3 %) [SUPPORTATA: #49, 6 days / 138 transitions] (§5.2, r.397-399)
A224 Those hours carry a maximum over two hours or more under a message that declares one [SUPPORTATA: #49] (§5.2, r.399-400)
A225 Mean excess over instantaneous 10 m wind: hours that reset 0.068–0.311 m/s [SUPPORTATA: #49] (§5.2, r.406)
A226 Mean excess over instantaneous 10 m wind: hours that did not reset 0.499–0.784 m/s [SUPPORTATA: #49] (§5.2, r.407)
A227 Three to eight times larger; a 10 to 17 % overstatement on a domain mean of about 4.5 m/s [SUPPORTATA: #49] (§5.2, r.409)
A228 The missed reset moves those hours closer to ERA5's gust for the wrong reason, so the error is not detectable from the value [SENZA FONTE] (§5.2, r.410-411)
A229 It was left as `0-1` and stated rather than repaired [SUPPORTATA: #49] (§5.2, r.413)
A230 Detecting the carry-over requires the previous hour's wrfout, which is not on disk when a file is converted [SENZA FONTE] (§5.2, r.413-414)
A231 No intra-file detector exists: all seven of WRF's diagnostic maxima reset on the same alarm, so when it is missed they carry over together and none can witness for another [SENZA FONTE] (§5.2, r.414-416)
A232 The hourly misses correlate with adaptive-timestep variability [SENZA FONTE] (§5.2, r.416-417)
A233 The mechanism was not established [SENZA FONTE] (§5.2, r.417)
A234 Do not treat the `10fg` time window as exact when a single hour matters [SUPPORTATA: #49] (§5.2, r.419)
A235 Over a season or distribution the effect is the 12 % contamination, which is quantified; for a specific hour there is no flag in the file [SUPPORTATA: #49] (§5.2, r.419-421)
A236 2024-02-15T12: `sro` mean 3.093e-5 m, `ssro` mean 0, `ssro` non-zero 0 of 2 220 273, `ro` mean 3.093e-5 m [SUPPORTATA: #51] (§6.1, r.432)
A237 2024-07-15T12: `sro` 2.347e-5, `ssro` 2.7e-8, non-zero 19, `ro` 2.350e-5 [SUPPORTATA: #51] (§6.1, r.433)
A238 2024-07-15T18: `sro` 1.064e-4, `ssro` 3.9e-8, non-zero 19, `ro` 1.065e-4 [SUPPORTATA: #51] (§6.1, r.434)
A239 2024-08-15T12: `sro` 1.453e-5, `ssro` 0, non-zero 0, `ro` 1.453e-5 [SUPPORTATA: #51] (§6.1, r.435)
A240 `ssro` is identically zero on five of the eighteen non-00Z sample timesteps [SUPPORTATA: #51] (§6.1, r.437)
A241 Where `ssro` is not zero, its domain mean is four to eight orders of magnitude below `sro` [SUPPORTATA: #51] (§6.1, r.437-438)
A242 `ro` equals `sro` to four significant figures at every timestep [SUPPORTATA: #51] (§6.1, r.438-439)
A243 The identity `ro = sro + ssro` holds to 3.7e-9 m; there is nothing in the second term [SUPPORTATA: #51] (§6.1, r.439-440)
A244 The cause is the time reference, not the conversion [SUPPORTATA: #51] (§6.1, r.442)
A245 The model's sub-surface drainage counter is alive: non-zero at 462 to 8 363 points, maxima 11 to 106 mm [SUPPORTATA: #51] (§6.1, r.442-443)
A246 On 2024-07-15 the same 1 647 points carry drainage at 00, 06, 12 and 18Z and only 19 of them grow [SUPPORTATA: #51] (§6.1, r.444-445)
A247 The published `ssro` is the accumulation since 00Z, so the daily field is almost always empty [SUPPORTATA: #51] (§6.1, r.445-446)
A248 Against ERA5: `sro` 1.0–4.6 of ERA5's, `ssro` 0.000–0.004, `ro` 0.19–0.85 [SUPPORTATA: #51] (§6.1, r.448-449)
A249 Do not close a water budget assuming this archive has a drainage term; it does not, at daily scale [SUPPORTATA: #51] (§6.1, r.451-452)
A250 `ro` and `sro` are, knowingly, duplicate messages [SUPPORTATA: #51] (§6.1, r.452)
A251 We are not short of surface runoff; we are missing the other half of the partition; ERA5's dominant term is the one we do not carry [SUPPORTATA: #51] (§6.1, r.452-454)
A252 ECMWF defines paramId 136 `tcw` as the sum of water vapour, liquid water, cloud ice, rain and snow: five species [SENZA FONTE] (§6.2, r.459-460)
A253 This archive builds `tcw` from six species, adding graupel [SUPPORTATA: #47] (§6.2, r.460-461)
A254 No graupel column is published separately because ERA5 has no parameter for one [SENZA FONTE] (§6.2, r.461)
A255 2024-01-15T12: residual mean 0.003525, graupel column mean 0.003396, residual max 5.69 kg/m² [SUPPORTATA: #47] (§6.2, r.468)
A256 2024-04-15T12: residual mean 0.010819, graupel column mean 0.010863, residual max 13.89 kg/m² [SUPPORTATA: #47] (§6.2, r.469)
A257 2024-07-15T12: residual mean 0.009762, graupel column mean 0.010219, residual max 26.46 kg/m² [SUPPORTATA: #47] (§6.2, r.470)
A258 2024-10-15T12: residual mean 0.007046, graupel column mean 0.007267, residual max 16.73 kg/m² [SUPPORTATA: #47] (§6.2, r.471)
A259 In the domain mean the residual is 0.4 % of the condensate and invisible [SUPPORTATA: #47] (§6.2, r.473)
A260 Inside a July convective cell it reaches 26 kg/m², larger than the whole of the rest of the column's condensate [SUPPORTATA: #47] (§6.2, r.473-474)
A261 Keeping graupel inside `tcw` was the deliberate choice [SUPPORTATA: #47] (§6.2, r.476)
A262 Dropping graupel would make `tcw` match ECMWF's definition exactly and the closure identity hold, at the cost of the graupel mass leaving the archive [SENZA FONTE] (§6.2, r.476-478)
A263 Reconstructing `tcw` from `tcwv + tclw + tciw + tcrw + tcsw` will not give `tcw`; the difference is graupel; in convective conditions it is not small [SUPPORTATA: #47] (§6.2, r.480-482)
A264 A point is masked where the ERA5 parameter is not defined there, not where the model has nothing to say, and not where the number looks wrong [SUPPORTATA: #34, #36, #38] (§7.1, r.490-491)
A265 Masked points are a GRIB bitmap, never zeros; a consumer can always tell "not defined here" from "zero here" [SENZA FONTE] (§7.1, r.491-492)
A266 `sst`, `ci` masked where not sea [SUPPORTATA: #34, #36, #38] (§7.1, r.498)
A267 `cl` (zero) and `dl` (missing) where sea [SUPPORTATA: #34, #36, #38] (§7.1, r.499)
A268 `swvl1-4`, `stl1-4` masked where not permanent land [SUPPORTATA: #38] (§7.1, r.500)
A269 `tvl` masked where shrubland dominates; MODIS carries no shrub phenology and guessing was refused [SENZA FONTE] (§7.1, r.501)
A270 `slt` masked where not permanent land [SENZA FONTE] (§7.1, r.502)
A271 `mucin` masking: see §7.2 [SUPPORTATA: #54] (§7.1, r.503)
A272 The sea/inland-water distinction is not the land-use lake class [SENZA FONTE] (§7.1, r.507)
A273 WPS's MODIS class 21 calls the Black Sea, the Sea of Azov and part of the Baltic a lake, together 89 % of the cells this domain marks fully lake [SENZA FONTE] (§7.1, r.507-509)
A274 Masking on the lake class would have deleted `sst` from the Black Sea [SENZA FONTE] (§7.1, r.509)
A275 The discriminator is connected-component size [SENZA FONTE] (§7.1, r.510)
A276 Water components: 844 431 cells (Atlantic + Mediterranean + Baltic + North Sea), 49 841 (Black Sea + Azov), 8 583 (Red Sea), then 1 225 (Vänern, the largest genuine inland lake) and smaller [SENZA FONTE] (§7.1, r.510-512)
A277 The threshold sits in that gap with a factor of seven of slack [SENZA FONTE] (§7.1, r.512-513)
A278 The soil columns are masked off sea ice, and that discards something [SUPPORTATA: #38] (§7.1, r.515)
A279 WRF reclassifies a water cell carrying sea ice as land, gives it soil type 16 and fills the column with water [SUPPORTATA: #38] (§7.1, r.515-517)
A280 `swvl` reaches exactly 1.000 against soil type 16's porosity of 0.435 [SUPPORTATA: #38] (§7.1, r.517)
A281 Those columns are the model's own state, but they are not soil [SENZA FONTE] (§7.1, r.517-518)
A282 ERA5 has no soil there because its land-sea mask is permanent [SENZA FONTE] (§7.1, r.518-519)
A283 Nothing is lost that cannot be recovered: `ci` is published, so the ice itself is in the file [SENZA FONTE] (§7.1, r.519-520)
A284 `lsm` and `al` are not constant in time; they follow the model hour by hour [SUPPORTATA: #34, #36, #38] (§7.1, r.522-523)
A285 WRF moves the land mask where sea ice appears [SENZA FONTE] (§7.1, r.524)
A286 `lsm` and `al` are written in every message and must not be treated as one-per-archive statics [SUPPORTATA: #34, #36, #38] (§7.1, r.524-528)
A287 The CAPE routine flags convective inhibition as missing wherever CAPE is below 100 J/kg [SUPPORTATA: #54] (§7.2, r.532)
A288 The archive writes a bitmap there rather than a zero [SUPPORTATA: #54] (§7.2, r.533)
A289 Zero would read as "nothing is stopping convection" at precisely the columns where the most is [SENZA FONTE] (§7.2, r.533-534)
A290 A column with no CAPE is usually a column with a great deal of inhibition, often why there is no CAPE [SENZA FONTE] (§7.2, r.534-535)
A291 2024-01-15T12: `mucin` present on 3.8 %, masked 96.2 % [SUPPORTATA: #54] (§7.2, r.541)
A292 2024-02-15T12: present 5.7 %, masked 94.3 % [SUPPORTATA: #54] (§7.2, r.542)
A293 2024-03-15T12: present 4.8 %, masked 95.2 % [SUPPORTATA: #54] (§7.2, r.543)
A294 2024-07-15T12: present 28.8 %, masked 71.2 % [SUPPORTATA: #54] (§7.2, r.544)
A295 2024-10-15T12: present 15.2 %, masked 84.8 % [SUPPORTATA: #54] (§7.2, r.545)
A296 2025-02-15T12: present 5.5 %, masked 94.5 % [SUPPORTATA: #54] (§7.2, r.546)
A297 On a winter day, 96 % of the `mucin` field is missing [SUPPORTATA: #54] (§7.2, r.548)
A298 Where we are silent, ERA5 carries an inhibition averaging 25 to 265 J/kg [SUPPORTATA: #54] (§7.2, r.548-549)
A299 Where ours is present, it is 0.03 to 0.24 of ERA5's [SUPPORTATA: #54] (§7.2, r.549-550)
A300 Ours exists only in columns with CAPE ≥ 100, the least inhibited ones, while ERA5 reports the field more widely [SENZA FONTE] (§7.2, r.550-551)
A301 Do not fill the gaps with zero: a model trained on it learns that low-CAPE situations have no convective inhibition, the inverse of the physics [SENZA FONTE] (§7.2, r.553-555)
A302 `mucape` is dense and its zeros are real [SUPPORTATA: #54] (§7.2, r.556)
A303 Within `grib_v3` `generatingProcessIdentifier` discriminates nothing: all 246 messages carry 128 [SUPPORTATA: #53] (§8.1, r.565-566)
A304 128 is eccodes' own GRIB2 sample default [SUPPORTATA: #53] (§8.1, r.566)
A305 The converter sets it explicitly only for the accumulations [SUPPORTATA: #53] (§8.1, r.566-567)
A306 Filtering on `generatingProcessIdentifier == 128` to find 00Z-referred accumulations selects the entire file [SUPPORTATA: #53] (§8.1, r.567-568)
A307 Nothing in the data is wrong: accumulations are referred to 00 UTC and 128 says so [SUPPORTATA: #53] (§8.1, r.570)
A308 The value's only real meaning is against the older GRIB1 archive, where 127 marks the run-init-referred messages [SUPPORTATA: #53] (§8.1, r.571-572)
A309 Test `stepType` / `typeOfStatisticalProcessing` and `stepRange`, which state it unambiguously and were both verified [SUPPORTATA: #53] (§8.1, r.574-575)
A310 The time convention is in §3 of `CHAPTER_VARIABLES.md` [SUPPORTATA: CHAPTER_VARIABLES.md §3] (§8.1, r.575-576)
A311 The run used no monthly satellite albedo [SUPPORTATA: namelist usemonalb = .false.] (§8.2, r.580)
A312 The background albedo comes from the land-use table's WINTER and SUMMER columns by dominant category [SUPPORTATA: #37] (§8.2, r.580-581)
A313 `al` takes only 8 to 11 distinct values over the whole domain [SUPPORTATA: #37] (§8.2, r.583)
A314 `al` changes at 1 171 937 land points, 89.9 % of the land mask, at the winter/summer boundary [SUPPORTATA: #37] (§8.2, r.584-585)
A315 Every transition is a table row with no residue: 0.20→0.17 croplands on 497 649 points, 0.23→0.25 barren on 369 219, and so on [SUPPORTATA: #37] (§8.2, r.585-586)
A316 SUMMER applies April to October and WINTER November to March [SUPPORTATA: #37] (§8.2, r.587)
A317 The field does not move within a day [SUPPORTATA: #37] (§8.2, r.587-588)
A318 Off land `al` is 0.08 on water and 0.65 on sea ice, the model's default ice albedo [SUPPORTATA: #37] (§8.2, r.589)
A319 Do not read `al` as an observed or evolving albedo; do not difference it across the seasonal boundary expecting a physical signal [SUPPORTATA: #37] (§8.2, r.591-592)
A320 `al` also moves at sea-ice points, following the land mask of §7.1 [SUPPORTATA: #37, §7.1] (§8.2, r.592-594)
A321 `slor` is published as the gradient magnitude of the resolved 3 km terrain [SUPPORTATA: #37] (§8.3, r.600-601)
A322 paramId 163 is defined as the slope of the sub-grid orography [SENZA FONTE] (§8.3, r.601)
A323 eccodes will show the parameter's own name, Slope of sub-gridscale orography, and nothing in the message says otherwise [SENZA FONTE] (§8.3, r.601-603)
A324 `sdor` is the ERA5 quantity, evaluated on a 3 km cell instead of a 31 km one [SUPPORTATA: #37] (§8.3, r.604-605)
A325 Measured ratio of medians of `sdor` against ERA5 is 0.244, which is (3/31)^0.605; a resolution rescaling, not a different definition [SUPPORTATA: #37] (§8.3, r.605-606)
A326 Several model fields are absent under a reason recorded as "no ERA5 parameter fits"; for most the accurate statement is different [SUPPORTATA: #35] (§8.4, r.612-614)
A327 `SNOALB`: ECMWF defines 260161 `mxsalb`, maximum snow albedo, exactly this quantity; ERA5 does not publish it [SUPPORTATA: #35] (§8.4, r.618)
A328 `QGRAUP`: ECMWF defines 260028 `grle` and 260001 `tcolg`; ERA5 does not publish them [SUPPORTATA: #35] (§8.4, r.619)
A329 `REFL_10CM`: ECMWF defines 260134 `bref`; ERA5 does not publish it [SUPPORTATA: #35] (§8.4, r.620)
A330 `LPI`: ECMWF defines the 228050 `litoti` family, unpublished by ERA5; `LPI` is a potential index, not a flash density, so it would not be `litoti` in any case [SUPPORTATA: #35] (§8.4, r.621)
A331 `SNOWFALLAC` is a geometric snow depth, not a water equivalent; ECMWF's 3066 `sde` is the matching parameter; ERA5 does not publish it [SUPPORTATA: #35] (§8.4, r.622)
A332 The exclusions stand either way [SENZA FONTE] (§8.4, r.624)
A333 Publication rule: a field ships only when the WRF quantity is the ERA5 one [SENZA FONTE] (§8.4, r.624-625)
A334 "No parameter exists" and "ERA5 does not publish it" are different claims, and only the second is true here [SUPPORTATA: #35] (§8.4, r.625-626)
A335 `LAI` is in the model output and is not published [SUPPORTATA: #35] (§8.4, r.628)
A336 `CHAPTER_VARIABLES.md` §6 explains why `lai_lv`/`lai_hv` are refused without mentioning that the underlying field exists [SUPPORTATA: CHAPTER_VARIABLES.md §6] (§8.4, r.629-632)
A337 The model carries one leaf area index per cell and ERA5 wants one per vegetation class; any split would be our invention [SENZA FONTE] (§8.4, r.630-631)
A338 `LAI` is a table lookup on the dominant category rather than an observed LAI, a second reason not to split it [SUPPORTATA: namelist rdlai2d = .false.; #35] (§8.4, r.632-634)
A339 Every number in this document was produced by a script in `tools/audit/` of the CHAPTER repository and is written up, with its method, in `docs/audit/` [SUPPORTATA: tools/audit/, docs/audit/] (§Where, r.640-642)
A340 Document written 2026-09-28, from measurements made 2026-09-18 to 2026-09-25 [SENZA FONTE] (§Where, r.658)

## 2. Dati numerici

N001 campione dell'audit = 34 timestep — both sampled years, all four seasons (§intro, r.14) [fonte: docs/audit/sample.md]
N002 messaggi per file orario `grib_v3` = 246 — (§Which, r.34) [SENZA FONTE]
N003 riparazioni = 6 — landed 2026-09-25 (§Which, r.35) [SENZA FONTE]
N004 spostamento `skt` per cambio soglia neve = circa 0.05 K RMSE — over snow-covered land (§Which, r.36-37) [SENZA FONTE]
N005 difetti nei file pre-rebuild = 6 — (§Which, r.37-38) [fonte: docs/audit/re-verification.md]
N006 bias SW clear-sky = +8.5 % — vs ERA5 (§0, r.47; §1.1, r.74) [fonte: #45]
N007 bias SW all-sky = +13.6 % — vs ERA5 (§0, r.47) [fonte: #45]
N008 `tcc` / ERA5 = 0.78 ; `hcc` / ERA5 = 0.61 — (§0, r.48) [fonte: #48]
N009 bias `skt` terra = −1.64 K media, −3.24 K a mezzogiorno — (§0, r.49) [fonte: #57]
N010 `fsr` / ERA5 terra = 0.32–0.48 — (§0, r.50) [fonte: #56]
N011 `zust` / ERA5 = 1.6–2.1× terra, 1.1× mare — (§0, r.51) [fonte: #56]
N012 `r` max = 139.7 % — at 300 hPa (§0, r.53; §3.2, r.260) [fonte: #40]
N013 RH ricostruita da `2t`/`2d`, picco = 100.09 % — (§0, r.54) [fonte: #42]
N014 dominio interessato dal clamp a 1000 hPa = 47.6 % — (§0, r.55) [fonte: #44]
N015 costante in `z` = 9.80665 ; g integrazione WRF = 9.81 — (§0, r.56) [fonte: #39]
N016 scostamento dal bilancio idrostatico = 0.034 % — (§0, r.56) [fonte: #39]
N017 `10fg` / raffica ERA5 = 0.625 — (§0, r.57) [fonte: #50]
N018 finestra `10fg` corretta = 88 % del tempo — (§0, r.58) [fonte: #49]
N019 eccesso ore sbagliate `10fg` = 0.499–0.784 m/s — (§0, r.58) [fonte: #49]
N020 punti `ssro` non nulli ≤ 19 — (§0, r.59) [fonte: #51]
N021 specie in `tcw` = 6 (ECMWF 5) ; residuo graupel fino a 26 kg/m² — (§0, r.60) [fonte: #47]
N022 `mucin` mancante = 71–96 % del dominio — (§0, r.62) [fonte: #54]
N023 messaggi con genproc 128 = 246 su 246 — (§0, r.63) [fonte: #53]
N024 valori distinti `al` = 8–11 — domain-wide (§0, r.64) [fonte: #37]
N025 griglia ERA5 = 31 km ; CHAPTER = 3 km — (§1.2, r.128; §2.1, r.175) [SENZA FONTE]
N026 AOD = 0.1–0.2 — over Europe, Mediterranean, Saharan margin (§1.1, r.78) [SENZA FONTE]
N027 `ssrdc`/ERA5 = 1.085 — ratio of means, sample (§1.1, r.85) [fonte: #45]
N028 `ssrd`/ERA5 = 1.136 — (§1.1, r.86) [fonte: #45]
N029 `ssrc`/ERA5 = 1.116 — (§1.1, r.87) [fonte: #45]
N030 `ssr`/ERA5 = 1.178 — (§1.1, r.88) [fonte: #45]
N031 `tsrc`/ERA5 = 1.031 — (§1.1, r.89) [fonte: #45]
N032 `strd`/ERA5 = 0.989 ; `strdc`/ERA5 = 0.996 — (§1.1, r.90) [fonte: #45]
N033 `ttr`/ERA5 = 1.009 ; `ttrc`/ERA5 = 0.990 — (§1.1, r.91) [fonte: #45]
N034 accordo campi termici con ERA5 = entro 1.1 % — (§1.1, r.94-95) [fonte: #45]
N035 deficit `tcc` = 22 % ; deficit `hcc` = 39 % — below ERA5 (§1.2, r.102) [fonte: #48]
N036 `tcc` = 0.381 ours, 0.487 ERA5, ratio 0.783 — sample means upscaled (§1.2, r.108) [fonte: #48]
N037 `hcc` = 0.169 ours, 0.276 ERA5, ratio 0.610 — (§1.2, r.109) [fonte: #48]
N038 `mcc` = 0.161 ours, 0.205 ERA5, ratio 0.786 — (§1.2, r.110) [fonte: #48]
N039 `lcc` = 0.231 ours, 0.268 ERA5, ratio 0.862 — (§1.2, r.111) [fonte: #48]
N040 `tciw` = 0.0185 ours, 0.0166 ERA5, ratio 1.109 — senza unità (§1.2, r.112) [fonte: #48]
N041 ampiezza dello spettro di assunzioni di overlap = 2–4 % — point by point on our CLDFRA (§1.2, r.119-120) [fonte: #48]
N042 ERA5 sopra di noi = 28 % — tcc (§1.2, r.120) [fonte: #48]
N043 quota del gap spiegata dall'overlap ≤ 1/7 — (§1.2, r.121) [fonte: #48]
N044 ghiaccio nubi in più = 11 % ; nubi alte in meno = 39 % — vs ERA5 (§1.2, r.124) [fonte: #48]
N045 `ICLOUD` = 1 — (§1.2, r.123) [fonte: namelist]
N046 bias `skt` mare = +0.01 K, corr 0.95–0.98 — mean over whole sample (§1.3, r.139) [fonte: #57]
N047 bias `skt` terra = −1.64 K, fino a −3.24 K a mezzogiorno, corr 0.95–0.98 — (§1.3, r.140) [fonte: #57]
N048 bias `skt` terra a 00Z = −0.5 a −1.2 K ; a 12Z = −0.8 a −3.2 K — (§1.3, r.142) [fonte: #57]
N049 `fsr` terra = 0.188–0.217 m ours, 0.375–0.394 m ERA5, ratio of medians 0.32–0.48 — (§2.1, r.171) [fonte: #56]
N050 `fsr` mare = 0.0089–0.0091 m ours, 0.0103–0.0105 m ERA5, ratio of medians 1.5–1.9 — (§2.1, r.172) [fonte: #56]
N051 `ZNT` foreste = 0.70 m ; savane e prati = 0.15 (m) ; barren = 0.065 (m) ; urbano = 1.00 m — (§2.1, r.180-181) [fonte: #56]
N052 punti urbani = 19 867 — (§2.1, r.181) [fonte: #56]
N053 floor `ZNT` sotto neve = 0.011 m — (§2.1, r.181) [fonte: #56]
N054 differenza `fsr` terra = fattore 2–3 — (§2.1, r.184) [fonte: #56]
N055 `zust` terra = 0.44–0.52 m/s ours, 0.23–0.28 m/s ERA5, ratio 1.62–2.06 — (§2.2, r.192) [fonte: #56]
N056 `zust` mare = 0.21–0.34 m/s ours, 0.19–0.31 m/s ERA5, ratio 1.08–1.12, corr 0.85–0.90 — (§2.2, r.193) [fonte: #56]
N057 rapporto `zust` a 00Z = 1.06–1.13 ; a 12Z = 1.40–1.75 — in every region (§2.2, r.198-199) [fonte: #56]
N058 residuo `|τ| = ρu*²` = 1.8e-6 N/m² — every point of every timestep checked (§2.2, r.201-202) [fonte: #56]
N059 residuo `zust = sqrt(|τ|/ρ)` = 2.7e-4 m/s — (§2.2, r.202) [fonte: #56]
N060 water gate `skt` = 0.0005 K RMSE, absmax 0.002 K — ~910 000 points, every timestep (§2.3, r.214) [fonte: #55]
N061 punti terra riprodotti a 1e-4 = 99.98 % luglio, 93.05 % gennaio — (§2.3, r.215) [fonte: #55]
N062 RMSE `skt` terra = 0.0012 K luglio ; 0.084–0.119 K gennaio e febbraio ; p99 0.81 K ; absmax 2.79 K — (§2.3, r.216) [fonte: #55]
N063 emissività sotto neve = 0.98 — flat (§2.3, r.218-219) [SENZA FONTE]
N064 errore di derivazione inverno = un decimo di kelvin ; trenta volte più piccolo del bias fisico — (§2.3, r.223-224) [fonte: #55 per il decimo; rapporto SENZA FONTE]
N065 paramId `r` = 157 ; paramId `2r` = 260242 — (§3.1, r.236-237) [SENZA FONTE]
N066 soglie di fase = 250.16 K (tutto ghiaccio sotto), 273.16 K (tutto acqua sopra) — (§3.1, r.242-243) [fonte: IFS Cy41r2]
N067 equazioni IFS Cy41r2 = 7.5, 7.6, 7.89, 7.90 — (§3.1, r.244) [fonte: IFS Cy41r2]
N068 differenza definizioni su ghiaccio = fino a fattore 1.8 — (§3.1, r.246) [fonte: #40]
N069 punti sopra 100 % a 400 hPa = 34 785 — single file (§3.2, r.261) [fonte: #40]
N070 RH sotto terra = fino a circa 163 % — (§3.2, r.263) [fonte: #44]
N071 quota del livello modello più basso = circa 25 m sopra il terreno — (§3.2, r.264-265) [fonte: #44]
N072 eccesso `2d` su `2t` a saturazione = 0.0133 K — 6 000–64 000 points per timestep (§3.3, r.274-275) [fonte: #42]
N073 consistenza `2d`–`Q2` = 3.6e-4 a 1.1e-2 in pressione di vapore (senza unità) — (§3.3, r.281-282) [fonte: #42]
N074 accordo sotto terra con livello modello più basso: `t` = 0.0 al 100 % dei punti ; `q` = 1e-9 ; `z` = 2.5e-4 m — (§4.1, r.295-296) [fonte: #44]
N075 quota dello stato modello pubblicato = 24–27 m sopra il suolo — (§4.1, r.300-301) [fonte: #44]
N076 `2t − t(1000 hPa)` sotto terra = −0.9 K mezzanotte, +1.4 K mezzogiorno — July (§4.1, r.303-304) [fonte: #44]
N077 intervallo verticale = 22 m — (§4.1, r.305) [fonte: #44]
N078 `z` a 1000 hPa sopra il terreno = mediana 24–27 m — (§4.1, r.308-309) [fonte: #44]
N079 dominio con auto-contraddizione = 47.6 % a 1000 hPa ; 9 % a 925 hPa — (§4.1, r.310-311) [fonte: #44]
N080 bias `t` vs ERA5 = −1.71 K a 1000 hPa ; −0.05 K a 850 hPa — (§4.1, r.316) [fonte: #44]
N081 correlazione `z` vs ERA5 a 1000 hPa = 0.108 — (§4.1, r.316) [fonte: #44]
N082 scostamento idrostatico = 0.034 % = 1 parte su 2 900 ; circa 2 m a 500 hPa ; 7 m a 50 hPa — (§4.2, r.330-331) [fonte: #39]
N083 punti terra verificati = 1 349 910 — surface vs pressure-level geopotential (§4.2, r.335-336) [fonte: #39]
N084 `10fg` vs ERA5 `10fg` = ratio 0.625, corr 0.813 — (§5.1, r.356) [fonte: #50]
N085 `10fg` vs ERA5 `i10fg` = ratio 0.644, corr 0.820 — (§5.1, r.357) [fonte: #50]
N086 `10fg` vs vento istantaneo 10 m stesso file = 1.004–1.032 — (§5.1, r.358) [fonte: #50]
N087 aumento per massimo orario = 0.5–3 % — (§5.1, r.360-361) [fonte: #50]
N088 punti con massimo sotto istantaneo = 0 su 2 220 273 — (§5.1, r.361-362) [fonte: #50]
N089 paramId `10fg` = 49 — (§5.1, r.363) [SENZA FONTE]
N090 raffica ERA5 / vento medio ERA5 = circa 1.6 — (§5.1, r.363-364) [SENZA FONTE]
N091 offset `10fg`/ERA5 = 0.593–0.673 — all 34 sample timesteps (§5.1, r.366-367) [fonte: #50]
N092 `zust` terra / ERA5 = 1.6–2.1 — (§5.1, r.379-380) [fonte: §2.2]
N093 sottostima come raffica = circa 38 % — (§5.1, r.384) [fonte: #50]
N094 correlazione = 0.81 — (§5.1, r.385-386) [fonte: #50]
N095 `typeOfStatisticalProcessing` = 2 ; `stepRange` = 0-1 ; riferimento H−1 — (§5.2, r.393-394) [fonte: #49]
N096 reset mancati = 17 su 138 transizioni (12.3 %) — six whole days (§5.2, r.397-399) [fonte: #49]
N097 eccesso medio ore con reset = 0.068–0.311 m/s ; ore senza reset = 0.499–0.784 m/s — (§5.2, r.406-407) [fonte: #49]
N098 rapporto eccessi = 3–8 volte ; sovrastima = 10–17 % su media di dominio circa 4.5 m/s — (§5.2, r.409) [fonte: #49]
N099 massimi diagnostici WRF sullo stesso allarme = 7 — (§5.2, r.415) [SENZA FONTE]
N100 contaminazione stagionale = 12 % — (§5.2, r.420) [fonte: #49]
N101 2024-02-15T12: `sro` 3.093e-5 m, `ssro` 0, non-zero 0 su 2 220 273, `ro` 3.093e-5 m — (§6.1, r.432) [fonte: #51]
N102 2024-07-15T12: `sro` 2.347e-5 m, `ssro` 2.7e-8 m, non-zero 19, `ro` 2.350e-5 m — (§6.1, r.433) [fonte: #51]
N103 2024-07-15T18: `sro` 1.064e-4 m, `ssro` 3.9e-8 m, non-zero 19, `ro` 1.065e-4 m — (§6.1, r.434) [fonte: #51]
N104 2024-08-15T12: `sro` 1.453e-5 m, `ssro` 0, non-zero 0, `ro` 1.453e-5 m — (§6.1, r.435) [fonte: #51]
N105 timestep con `ssro` identicamente nullo = 5 su 18 non-00Z — (§6.1, r.437) [fonte: #51]
N106 `ssro` sotto `sro` = 4–8 ordini di grandezza — domain mean (§6.1, r.437-438) [fonte: #51]
N107 `ro` = `sro` a 4 cifre significative — every timestep (§6.1, r.438-439) [fonte: #51]
N108 residuo `ro = sro + ssro` = 3.7e-9 m — (§6.1, r.439) [fonte: #51]
N109 drenaggio non nullo = 462–8 363 punti, massimi 11–106 mm — (§6.1, r.442-443) [fonte: #51]
N110 punti con drenaggio 2024-07-15 = 1 647 a 00/06/12/18Z, di cui 19 crescono — (§6.1, r.444-445) [fonte: #51]
N111 vs ERA5: `sro` 1.0–4.6 ; `ssro` 0.000–0.004 ; `ro` 0.19–0.85 — (§6.1, r.448-449) [fonte: #51]
N112 paramId `tcw` = 136 — (§6.2, r.459) [SENZA FONTE]
N113 2024-01-15T12: residuo medio 0.003525, graupel medio 0.003396 (senza unità), residuo max 5.69 kg/m² — (§6.2, r.468) [fonte: #47]
N114 2024-04-15T12: 0.010819, 0.010863, max 13.89 kg/m² — (§6.2, r.469) [fonte: #47]
N115 2024-07-15T12: 0.009762, 0.010219, max 26.46 kg/m² — (§6.2, r.470) [fonte: #47]
N116 2024-10-15T12: 0.007046, 0.007267, max 16.73 kg/m² — (§6.2, r.471) [fonte: #47]
N117 residuo in media di dominio = 0.4 % del condensato — (§6.2, r.473) [fonte: #47]
N118 residuo in cella convettiva di luglio = 26 kg/m² — (§6.2, r.474) [fonte: #47]
N119 classe MODIS lago = 21 ; quota di celle lago piene che sono Mar Nero/Azov/Baltico = 89 % — (§7.1, r.507-509) [SENZA FONTE]
N120 componenti acqua = 844 431 (Atlantico+Med+Baltico+Mare del Nord) ; 49 841 (Mar Nero+Azov) ; 8 583 (Mar Rosso) ; 1 225 (Vänern) celle — (§7.1, r.510-512) [SENZA FONTE]
N121 margine della soglia = fattore 7 — (§7.1, r.513) [SENZA FONTE]
N122 tipo di suolo del ghiaccio marino = 16 ; `swvl` = 1.000 ; porosità tipo 16 = 0.435 — (§7.1, r.516-517) [fonte: #38]
N123 soglia CAPE per `mucin` mancante = 100 J/kg — (§7.2, r.532) [fonte: #54]
N124 `mucin` presente/mascherato: 2024-01-15T12 3.8/96.2 % ; 2024-02-15T12 5.7/94.3 % ; 2024-03-15T12 4.8/95.2 % ; 2024-07-15T12 28.8/71.2 % ; 2024-10-15T12 15.2/84.8 % ; 2025-02-15T12 5.5/94.5 % — (§7.2, r.541-546) [fonte: #54]
N125 `mucin` mancante giorno invernale = 96 % — (§7.2, r.548) [fonte: #54]
N126 inibizione ERA5 dove noi mancanti = 25–265 J/kg — (§7.2, r.549) [fonte: #54]
N127 `mucin` nostro / ERA5 dove presente = 0.03–0.24 — (§7.2, r.549-550) [fonte: #54]
N128 genproc GRIB2 = 128 ; GRIB1 run-init = 127 — (§8.1, r.565-572) [fonte: #53]
N129 `al` valori distinti = 8–11 — whole domain (§8.2, r.583) [fonte: #37]
N130 punti terra che cambiano `al` al confine stagionale = 1 171 937 (89.9 % della maschera terra) — (§8.2, r.584-585) [fonte: #37]
N131 transizioni `al`: croplands 0.20→0.17 su 497 649 punti ; barren 0.23→0.25 su 369 219 — (§8.2, r.585-586) [fonte: #37]
N132 `al` acqua = 0.08 ; ghiaccio marino = 0.65 — (§8.2, r.589) [fonte: #37]
N133 paramId `slor` = 163 — (§8.3, r.601) [SENZA FONTE]
N134 `sdor` / ERA5 = 0.244 = (3/31)^0.605 — ratio of medians (§8.3, r.605-606) [fonte: #37]
N135 paramId ECMWF: `mxsalb` 260161 ; `grle` 260028 ; `tcolg` 260001 ; `bref` 260134 ; `litoti` 228050 ; `sde` 3066 — (§8.4, r.618-622) [fonte: #35]
N136 periodo delle misure = 2026-09-18 a 2026-09-25 ; documento scritto 2026-09-28 — (§Where, r.658) [SENZA FONTE]

## 3. Equazioni

E001 $z = 9.80665 \times z_{\mathrm{WRF}}$ — simboli: z = published geopotential; z_WRF = WRF's own geopotential height; 9.80665 = standard gravity (§0, r.56; §4.2, r.326-328)
E002 $\mathrm{LWUPB} = \varepsilon \sigma T^4 + (1-\varepsilon)\,\mathrm{GLW}$ — simboli: LWUPB = upward longwave flux; ε = per-category emissivity measured from the run; T = skin temperature (`skt`); σ e GLW non definiti (§2.3, r.207-208)
E003 $|\tau| = \rho u_*^2$ — simboli: τ = published stresses; ρ non definito; u* = friction velocity (`zust`) (§2.2, r.201)
E004 $\mathrm{zust} = \sqrt{|\tau|/\rho}$ — simboli: come sopra (§2.2, r.202)
E005 $\mathrm{ro} = \mathrm{sro} + \mathrm{ssro}$ — simboli: ro, sro, ssro = runoff variables (total, surface, sub-surface non esplicitati) (§6.1, r.439)
E006 $\mathrm{residual} = \mathrm{tcw} - (\mathrm{tcwv} + \mathrm{tclw} + \mathrm{tciw} + \mathrm{tcrw} + \mathrm{tcsw})$ — simboli: "tcw minus the five published components"; residual confrontato col graupel column (§6.2, r.463-464, r.480)
E007 $0.244 = (3/31)^{0.605}$ — simboli: 0.244 = ratio of medians `sdor` vs ERA5; 3 e 31 = risoluzioni in km (§8.3, r.605-606)
E008 $2t - t(1000\,\mathrm{hPa})$ — differenza sotto terra: −0.9 K mezzanotte, +1.4 K mezzogiorno in luglio (§4.1, r.303-304)
E009 $\varepsilon = 0.98$ sotto neve (flat) — (§2.3, r.218-219)

## 4. Riferimenti bibliografici

R001 `CHAPTER_VARIABLES.md` (§intro, r.3; §8.1, r.575 "§3 of `CHAPTER_VARIABLES.md`"; §8.4, r.629 "`CHAPTER_VARIABLES.md` §6")
R002 `MISSING_VARIABLES.md` (§intro, r.4; §1.3, r.153)
R003 `docs/audit/sample.md` (§intro, r.15; §Where, r.646)
R004 `docs/audit/re-verification.md` (§Which, r.40; §Where, r.656)
R005 [#45](https://github.com/meteocima/CHAPTER_LAM_AI/issues/45) (§1.1, r.100)
R006 [#48](https://github.com/meteocima/CHAPTER_LAM_AI/issues/48) (§1.2, r.131)
R007 [#57](https://github.com/meteocima/CHAPTER_LAM_AI/issues/57) (§1.3, r.161)
R008 [#56](https://github.com/meteocima/CHAPTER_LAM_AI/issues/56) (§2.1, r.186; §2.2, r.203)
R009 [#55](https://github.com/meteocima/CHAPTER_LAM_AI/issues/55) (§2.3, r.225)
R010 [#40](https://github.com/meteocima/CHAPTER_LAM_AI/issues/40) (§3.1, r.255; §3.2, r.269)
R011 [#44](https://github.com/meteocima/CHAPTER_LAM_AI/issues/44) (§3.2, r.270; §4.1, r.320)
R012 [#42](https://github.com/meteocima/CHAPTER_LAM_AI/issues/42) (§3.3, r.286)
R013 [#39](https://github.com/meteocima/CHAPTER_LAM_AI/issues/39) (§4.2, r.336)
R014 [#50](https://github.com/meteocima/CHAPTER_LAM_AI/issues/50) (§5.1, r.388)
R015 [#49](https://github.com/meteocima/CHAPTER_LAM_AI/issues/49) (§5.2, r.422)
R016 [#51](https://github.com/meteocima/CHAPTER_LAM_AI/issues/51) (§6.1, r.455)
R017 [#47](https://github.com/meteocima/CHAPTER_LAM_AI/issues/47) (§6.2, r.482)
R018 [#34](https://github.com/meteocima/CHAPTER_LAM_AI/issues/34), [#36](https://github.com/meteocima/CHAPTER_LAM_AI/issues/36) and [#38](https://github.com/meteocima/CHAPTER_LAM_AI/issues/38) (§7.1, r.526-528)
R019 [#54](https://github.com/meteocima/CHAPTER_LAM_AI/issues/54) (§7.2, r.557)
R020 [#53](https://github.com/meteocima/CHAPTER_LAM_AI/issues/53) (§8.1, r.576)
R021 [#37](https://github.com/meteocima/CHAPTER_LAM_AI/issues/37) (§8.2, r.594; §8.3, r.608)
R022 [#35](https://github.com/meteocima/CHAPTER_LAM_AI/issues/35) (§8.4, r.634)
R023 IFS Cy41r2's own equations (7.5, 7.6, 7.89, 7.90) (§3.1, r.243-244)
R024 the Tegen aerosol climatology (§1.1, r.77)
R025 a CAM ozone climatology (§1.1, r.76)
R026 the WMO screen convention (§3.1, r.247)
R027 `tools/audit/` of the [CHAPTER repository](https://github.com/meteocima/CHAPTER_LAM_AI) (§Where, r.640-641)
R028 `docs/audit/harness.md` (§Where, r.647)
R029 `docs/audit/f1-pressure-levels.md` (§Where, r.648)
R030 `docs/audit/f2-near-surface.md` (§Where, r.649)
R031 `docs/audit/f3-column-integrals.md` (§Where, r.650)
R032 `docs/audit/f4-radiation.md` (§Where, r.651)
R033 `docs/audit/f5-water-cycle.md` (§Where, r.652)
R034 `docs/audit/f6-soil-and-snow.md` (§Where, r.653)
R035 `docs/audit/f7-static-and-surface.md` (§Where, r.654)
R036 `docs/audit/f8-surface-exchange.md` (§Where, r.655)
R037 namelist/config citati: `aer_opt = 0` (§1.1, r.77); `ICLOUD = 1` (§1.2, r.123); `usemonalb = .false.` (§8.2, r.580); `rdlai2d = .false.` (§8.4, r.632)

## 5. Figure e tabelle

T001 Tabella "The short list": colonne `#` | Property | The number; 19 righe (1.1, 1.2, 1.3, 2.1, 2.2, 3.1, 3.2, 3.3, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 8.3); una riga per proprietà con il numero chiave (§0, r.45-65)
T002 Tabella rapporti radiazione: colonne field | ours / ERA5; 7 righe (`ssrdc`, `ssrd`, `ssrc`, `ssr`, `tsrc`, `strd`/`strdc`, `ttr`/`ttrc`); ratio of means against ERA5 over the sample (§1.1, r.83-91)
T003 Tabella copertura nuvolosa: colonne (campo) | ours | ERA5 | ratio; 5 righe (`tcc`, `hcc`, `mcc`, `lcc`, `tciw`); sample means upscaled to ERA5 grid (§1.2, r.106-112)
T004 Tabella bias `skt`: colonne region | bias | correlation; 2 righe (sea, land); mean over the whole sample (§1.3, r.137-140)
T005 Tabella `fsr`: colonne (campo) | ours | ERA5 | ratio of medians; 2 righe (land, sea) (§2.1, r.169-172)
T006 Tabella `zust`: colonne (campo) | ours | ERA5 | ratio; 2 righe (land, sea) (§2.2, r.190-193)
T007 Tabella accuratezza `skt`: colonne (voce) | figure; 3 righe (water gate, land points reproduced to 1e-4, land skt RMSE) (§2.3, r.212-216)
T008 Tabella confronti `10fg`: colonne comparison | ratio | corr; 3 righe (vs ERA5 `10fg`, vs ERA5 `i10fg`, vs own instantaneous 10 m wind) (§5.1, r.354-358)
T009 Tabella eccesso `10fg`: colonne (classe di ore) | mean excess; 2 righe (hours that reset, hours that did not) (§5.2, r.404-407)
T010 Tabella runoff: colonne timestep | `sro` mean (m) | `ssro` mean (m) | `ssro` non-zero points | `ro` mean (m); 4 righe (2024-02-15T12, 2024-07-15T12, 2024-07-15T18, 2024-08-15T12) (§6.1, r.430-435)
T011 Tabella residuo `tcw`: colonne timestep | residual (mean) | graupel column (mean) | residual max; 4 righe (2024-01-15T12, 2024-04-15T12, 2024-07-15T12, 2024-10-15T12) (§6.2, r.466-471)
T012 Tabella regola di mascheramento: colonne field | masked where; 6 righe (`sst`/`ci`, `cl`/`dl`, `swvl1-4`/`stl1-4`, `tvl`, `slt`, `mucin`) (§7.1, r.496-503)
T013 Tabella presenza `mucin`: colonne timestep | `mucin` present on | masked; 6 righe (2024-01-15T12, 2024-02-15T12, 2024-03-15T12, 2024-07-15T12, 2024-10-15T12, 2025-02-15T12) (§7.2, r.539-546)
T014 Tabella parametri ECMWF non pubblicati da ERA5: colonne field | the accurate reason; 5 righe (`SNOALB`, `QGRAUP`, `REFL_10CM`, `LPI`, `SNOWFALLAC`) (§8.4, r.616-622)
T015 Tabella documenti di audit: colonne document | covers; 11 righe (sample.md, harness.md, f1..f8, re-verification.md) con le sezioni coperte: f1 §3,§4; f2 §3.3; f3 §1.2,§6.2; f4 §1.1; f5 §5,§6.1,§8.1; f6 §7.1; f7 §7.1,§8.2,§8.3; f8 §1.3,§2,§7.2 (§Where, r.644-656)

## 6. Termini tecnici

G001 grib_v3 — "The GRIB2 archive, `grib_v3`, 246 messages per hourly file" (§Which, r.34)
G002 properties of the run — "the model was configured a certain way and the data reflect it" (§How, r.27)
G003 properties of the conversion — "a deliberate convention, chosen and documented" (§How, r.29)
G004 RRTMG — non definito (§1.1, r.76)
G005 `aer_opt` — non definito; `= 0` associato a "no aerosol at all" (§1.1, r.76-77)
G006 `ssrdc`, `ssrd`, `ssrc`, `ssr`, `tsrc`, `strd`, `strdc`, `ttr`, `ttrc` — surface solar down clear sky / all sky; surface net solar clear / all sky; top net solar clear sky; downward thermal; outgoing thermal (§1.1, r.85-91)
G007 `tcc`, `hcc`, `mcc`, `lcc` — total / high / medium / low cloud cover (solo `tcc` e high cloud esplicitati) (§1.2, r.102-111)
G008 `tciw` — non definito; associato a "cloud ice" (§1.2, r.112, r.124)
G009 maximum-random overlap / exponential-random overlap / random overlap — non definiti (§1.2, r.116-119)
G010 `CLDFRA` — "WRF's Xu–Randall diagnostic under `ICLOUD = 1`" (§1.2, r.123)
G011 `skt` — skin temperature, "inverted from the upward longwave flux" (§1.3, r.135; §2.3, r.207)
G012 `HFX`, `LH` — non definiti; citati con "the ground heat flux" come campi assenti (§1.3, r.151-152)
G013 `fsr` — "WRF's `ZNT`", "local surface roughness of the land-use class" (§2.1, r.175-176)
G014 effective roughness — "carries the orographic drag the IFS parameterises at 31 km" (§2.1, r.174-175)
G015 `ZNT` — "a land-use lookup with a snow override: one value per category" (§2.1, r.179)
G016 Charnock — non definito (§2.1, r.177)
G017 `zust` — friction velocity (§2.2, r.195-198)
G018 `TSK` — non definito; "not written out by the run" (§2.3, r.207)
G019 `LWUPB`, `GLW` — non definiti (§2.3, r.208)
G020 water gate — "`skt` against the model's own SST" (§2.3, r.214)
G021 snow rule — "emissivity switches to a flat 0.98 under snow" (§2.3, r.218-219)
G022 `r` — "relative humidity over the mixed phase", paramId 157, pressure levels (§3.1, r.236)
G023 `2r` — "relative humidity over liquid water at every temperature", paramId 260242, 2 m (§3.1, r.237)
G024 mixed phase — "saturates over ice below 250.16 K, over water above 273.16 K, and quadratically between" (§3.1, r.242-243)
G025 WMO screen convention — "saturates over liquid water at all temperatures" (§3.1, r.247-248)
G026 `q`, `t`, `sp` — non definiti (§3.1, r.254)
G027 `2t`, `2d`, `Q2` — non definiti (§3.3, r.274, r.281)
G028 clamp (below ground) — "publishes the lowest model level's value, verbatim"; "not an extrapolation and not a fill" (§4.1, r.294-295)
G029 surface join — non definito (§4.1, r.303)
G030 `z` — "standard gravity times WRF's own geopotential height" (§4.2, r.326-327)
G031 `10fg` — "the highest 10 m wind speed the simulation itself produced during the hour"; paramId 49 (§5.1, r.350-351, r.363)
G032 `i10fg` — "gust scheme, instantaneous" (§5.1, r.357)
G033 `WSPD10MAX` — non definito; "reset by WRF at the history write" (§5.2, r.397)
G034 `stepType`, `stepRange`, `typeOfStatisticalProcessing` — non definiti (§5.2, r.393; §8.1, r.574)
G035 history write / alarm — non definiti (§5.2, r.397, r.415)
G036 `sro`, `ssro`, `ro` — non definiti esplicitamente; `ssro` = "the accumulation since 00Z" della drenaggio sub-superficiale (§6.1, r.430-446)
G037 `tcw` — "paramId 136 ... the sum of water vapour, liquid water, cloud ice, rain and snow" (ECMWF); qui sei specie con graupel (§6.2, r.459-461)
G038 `tcwv`, `tclw`, `tciw`, `tcrw`, `tcsw` — "the five published components" (§6.2, r.463, r.480)
G039 bitmap — "Masked points are a GRIB bitmap, never zeros" (§7.1, r.491-492)
G040 `sst`, `ci`, `cl`, `dl`, `swvl1-4`, `stl1-4`, `tvl`, `slt` — non definiti (§7.1, r.498-502)
G041 permanent land — non definito (§7.1, r.500)
G042 connected-component size — il discriminante mare/acque interne (§7.1, r.510)
G043 `lsm`, `al` — non definiti; "not constant in time" (§7.1, r.522)
G044 `mucin`, `mucape` — non definiti; `mucin` = convective inhibition (§7.2, r.532, r.556)
G045 `generatingProcessIdentifier` — non definito; 128 = "eccodes' own GRIB2 sample default" (§8.1, r.565-566)
G046 `al` — background albedo "from the land-use table's WINTER and SUMMER columns by dominant category" (§8.2, r.580-581)
G047 `usemonalb` — non definito; "no monthly satellite albedo" (§8.2, r.580)
G048 `slor` — "gradient magnitude of the resolved 3 km terrain"; paramId 163 "slope of the sub-grid orography" (§8.3, r.600-601)
G049 `sdor` — "the ERA5 quantity, evaluated on a 3 km cell" (§8.3, r.604)
G050 `SNOALB`, `QGRAUP`, `REFL_10CM`, `LPI`, `SNOWFALLAC` — `LPI` "a potential index, not a flash density"; `SNOWFALLAC` "a geometric snow depth, not a water equivalent"; gli altri non definiti (§8.4, r.618-622)
G051 `mxsalb`, `grle`, `tcolg`, `bref`, `litoti`, `sde` — `mxsalb` = "maximum snow albedo"; gli altri non definiti (§8.4, r.618-622)
G052 `LAI`, `lai_lv`, `lai_hv` — leaf area index; ERA5 "one per vegetation class" (§8.4, r.628-631)
G053 `rdlai2d` — non definito; `= .false.` → "a table lookup on the dominant category" (§8.4, r.632)
G054 publication rule — "a field ships only when the WRF quantity **is** the ERA5 one" (§8.4, r.624-625)

## 7. Segnalazioni

S001 [GONFIATA] "Every number here was measured, not estimated" — il testo stesso contiene numeri non misurati (AOD 0.1-0.2, r.78; "roughly 1.6 times", r.364; "about 4.5 m/s", r.409) (§intro, r.13)
S002 [CONTRADDIZIONE INTERNA] Il documento dice di descrivere l'archivio "from 2026-09-29 onward" e un cambiamento del 2026-09-29 già riflesso nei numeri, ma chiude con "Document written 2026-09-28, from measurements made 2026-09-18 to 2026-09-25" (§Which, r.35-37; §Where, r.658)
S003 [VAGA] "Files written before that date" — non è chiaro se la data sia 2026-09-25 (riparazioni) o 2026-09-29 (soglia neve) (§Which, r.37)
S004 [CONTRADDIZIONE INTERNA] Il cambio di soglia neve è detto "already reflected in the figures in section 4", ma le cifre di `skt` sono in §2.3 (sezione 2), non in sezione 4 (§Which, r.37)
S005 [NUMERO SENZA FONTE] "about 0.05 K RMSE" di spostamento di `skt` — nessuna issue né popolazione (§Which, r.36-37)
S006 [NUMERO SENZA FONTE] AOD "0.1 to 0.2" e "attenuates the direct beam by about the amount measured" — nessuna fonte (§1.1, r.77-79)
S007 [RIFERIMENTO INCOMPLETO] "CAM ozone climatology" e "Tegen aerosol climatology" citate senza riferimento bibliografico né versione (§1.1, r.76-77)
S008 [VAGA] "`CLDFRA` is strongly bimodal" — nessun numero o misura a sostegno (§1.2, r.120)
S009 [VAGA] "which yields somewhat more cover" — effetto della risoluzione non quantificato (§1.2, r.129)
S010 [GONFIATA] "A bias of +0.01 K there says the derivation, the emissivity and the encoding are not the cause of anything" (§1.3, r.145-146)
S011 [CONTRADDIZIONE INTERNA] `fsr` sul mare: ours 0.0089–0.0091 m, ERA5 0.0103–0.0105 m danno un rapporto < 1 (circa 0.85–0.88), ma la colonna riporta "1.5–1.9"; e il testo dice "Over sea the two agree" (§2.1, r.172, r.177)
S012 [CONTRADDIZIONE INTERNA] `zust` terra: ratio 1.62–2.06 sul campione, ma il rapporto per ora è 1.06–1.13 a 00Z e 1.40–1.75 a 12Z "in every region"; il massimo del campione eccede il massimo orario dichiarato (§2.2, r.192, r.198-199)
S013 [VAGA] "at every point of every timestep checked" — non si dice quanti timestep (§2.2, r.202)
S014 [VAGA] "The derivation is verified" — senza dire su cosa (§2.3, r.209)
S015 [VAGA] "the switch is applied slightly earlier than the model's own transition completes" — non quantificato (§2.3, r.219)
S016 [GONFIATA] "Over water ... the derivation is exact" — la tabella riporta 0.0005 K RMSE, absmax 0.002 K (§2.3, r.220 vs r.214)
S017 [NUMERO SENZA FONTE] "the derivation error is thirty times smaller" — rapporto non derivato esplicitamente (0.1 K contro 1.64 / 3.24 K) (§2.3, r.224)
S018 [GONFIATA] "This is the single most likely misreading of the archive" (§3.1, r.233)
S019 [RIFERIMENTO INCOMPLETO] "IFS Cy41r2's own equations (7.5, 7.6, 7.89, 7.90)" — non indicato quale documento/parte della IFS Documentation (§3.1, r.243-244)
S020 [RIFERIMENTO INCOMPLETO] "WMO screen convention" — nessun documento WMO citato (§3.1, r.247)
S021 [NUMERO SENZA FONTE] "Measured on a single file" — file non identificato (139.7 %, 34 785 punti) (§3.2, r.260-261)
S022 [VAGA] "up to about 163 %" — "about" su un massimo (§3.2, r.263)
S023 [CONTRADDIZIONE INTERNA] quota del livello più basso data come "roughly 25 m" (r.264), "about 24 to 27 m" (r.300) e "over a 22 m interval" (r.305) (§3.2, §4.1)
S024 [NUMERO SENZA FONTE] consistenza `2d`–`Q2` "3.6e-4 to 1.1e-2 in vapour pressure" — senza unità né dire se relativa o assoluta (§3.3, r.281-282)
S025 [GONFIATA] "exactly 0.0 at 100 % of below-ground points" (§4.1, r.295-296)
S026 [VAGA] "which is most of the land" — non quantificato rispetto a 47.6 % del dominio (§4.1, r.315)
S027 [GONFIATA] "This difference, not any defect, is the whole of the 1000 hPa discrepancy against ERA5" (§4.1, r.315)
S028 [GONFIATA] "exactly — at the surface and on every pressure level, with no residual" (§4.2, r.327-328)
S029 [VAGA] "Neither number can be removed without breaking the other" — non dimostrato (§4.2, r.333)
S030 [NUMERO SENZA FONTE] "ERA5's gust runs at roughly 1.6 times its own mean wind" (§5.1, r.363-364)
S031 [VAGA] "half a per cent to three per cent" contro tabella 1.004–1.032 (0.4–3.2 %) (§5.1, r.360-361 vs r.358)
S032 [VAGA] "That encoding was verified correct" — senza dire su cosa (§5.2, r.394)
S033 [VAGA] "The hourly misses correlate with adaptive-timestep variability" — nessun numero né misura (§5.2, r.416-417)
S034 [NUMERO SENZA FONTE] "all seven of WRF's diagnostic maxima" — non elencati né citata fonte (§5.2, r.415)
S035 [NUMERO SENZA FONTE] "a domain mean of about 4.5 m/s" (§5.2, r.409)
S036 [CONTRADDIZIONE INTERNA] "four to eight orders of magnitude below `sro`": in tabella 2.347e-5 / 2.7e-8 e 1.064e-4 / 3.9e-8 sono circa tre ordini di grandezza (§6.1, r.437-438 vs r.433-434)
S037 [CONTRADDIZIONE INTERNA] "`ro` equals `sro` to four significant figures at every timestep": in tabella 2.347e-5 vs 2.350e-5 e 1.064e-4 vs 1.065e-4 differiscono alla quarta cifra (§6.1, r.438-439 vs r.433-434)
S038 [VAGA] "the daily field is almost always empty" (§6.1, r.446)
S039 [NUMERO SENZA FONTE] residuo e graupel in media (0.003525 ecc.) senza unità (§6.2, r.468-471)
S040 [VAGA] "In the domain mean it is 0.4 % of the condensate and invisible" / "larger than the whole of the rest of the column's condensate" — valori del condensato non riportati (§6.2, r.473-474)
S041 [NUMERO SENZA FONTE] componenti connesse (844 431, 49 841, 8 583, 1 225) e "89 %" delle celle lago — nessuna issue o misura citata (§7.1, r.507-512)
S042 [RIFERIMENTO INCOMPLETO] "The threshold sits in that gap with a factor of seven of slack" — la soglia stessa non è indicata nel file (§7.1, r.512-513)
S043 [GONFIATA] "Nothing is lost that cannot be recovered" — contraddice "that discards something" della stessa voce (§7.1, r.515 vs r.519)
S044 [VAGA] "usually a column with a great deal of inhibition, and that is often *why* there is no CAPE" (§7.2, r.534-535)
S045 [VAGA] "ERA5 reports the field more widely" — non quantificato (§7.2, r.551)
S046 [VAGA] "were both verified" (`stepType`, `stepRange`) — senza dire su cosa (§8.1, r.575)
S047 [CONTRADDIZIONE INTERNA] "the field does not move within a day" per `al` vs §7.1 "`lsm` and `al` ... follow the model hour by hour" e r.592-593 "it moves *twice*" ai punti di ghiaccio marino (§8.2, r.587-588 vs §7.1, r.522-523)
S048 [VAGA] "and so on" nell'elenco delle transizioni di `al` (§8.2, r.586)
S049 [VAGA] esponente 0.605 in "(3/31)^0.605" dato senza derivazione; la qualifica "a resolution rescaling" non è dimostrata (§8.3, r.605-606)
S050 [RIFERIMENTO SOSPETTO] #37 citata sia per `al` (§8.2) sia per `slor`/`sdor` (§8.3); non chiaro se la stessa issue copra entrambe (§8.2, r.594; §8.3, r.608)
S051 [VAGA] "For most of them the accurate statement is different" — non detto quante siano "several" né "most" (§8.4, r.612-614)
S052 [RIFERIMENTO INCOMPLETO] La tabella "Where the measurements live" non assegna §8.4 (né §2.3 esplicitamente) ad alcun documento di audit, pur dicendo "Every number in this document" (§Where, r.640-656)
S053 [GONFIATA] "Every number in this document was produced by a script in `tools/audit/`" — include numeri dichiaratamente non misurati (vedi S001) (§Where, r.640)
