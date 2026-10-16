# Da verificare

Aggiornato il 2026-09-29. Le 541 voci [SENZA FONTE] delle tre schede sono state verificate due volte: (1) contro le 65 issue di `meteocima/CHAPTER` e `docs/audit/`; (2) le voci non trovate, contro fonti ufficiali online (ECMWF, WRF, MODIS), misure in sola lettura sui dati dell'archivio e la storia del repository. Dettaglio in `verifica/`. Quando le due verifiche danno esiti diversi, la voce sta sotto l'esito più severo e riporta entrambe.

## 0. Decisioni dell'utente e misure aggiunte (2026-09-29)

- Citazioni: nel report si citano solo le issue che parlano dei GRIB (repository pubblico, github.com/meteocima/CHAPTER). Le altre issue e i file del repository servono da verifica e non si citano.
- Maschera degli arbusteti (`CHAPTER_VARIABLES` A120, A261; md r.157 "15.8 %" e r.387 "16.2 %"): si usa il dato più recente. Rimisurato sul sidecar statico in uso (`static_v1/chapter_static_d02.npz`, 2026-09-25 17:31): 124 672 celle con `tvl` mancante (coincide con `meta_tvl_masked_points` e con #25), su 778 381 celle con `cvl > 0` = 16,02 %. Per confronto: 12,91 % delle celle con `cvl > 0` o `cvh > 0`, 9,56 % delle 1 304 109 celle di terra. Né 15,8 % né 16,2 % si riproducono.

- Ambito del report: CHAPTER in sé e la sua mappatura sullo schema ERA5, cioè cosa contengono i GRIB e come ogni campo è stato estratto in modo onesto. Fuori dal report: la richiesta originale di variabili, il progetto che l'ha fatta, la lista "richiesto/consegnato" (voci come `MISSING_VARIABLES` A013, N001-N005, A181 si scartano, non si verificano). Da `MISSING_VARIABLES` entra solo ciò che riguarda i limiti della mappatura: quali parametri ERA5 non si possono produrre da questi wrfout, e perché.

## Conteggi

- CONTRADDETTA: 15
- CONFERMATA_CON_DIFFERENZE: 85
- NON_TROVATA: 9
- NON_FATTUALE: 7
- NON_VERIFICABILE: 32
- FUORI_AMBITO: 9
- CONFERMATA: 384
- totale: 541

## 1. Contraddette (la voce dell'md è superata o sbagliata: si usa la fonte)

- `CHAPTER_VARIABLES A036` I messaggi accumulati portano `generatingProcessIdentifier = 128` come marcatore del riferimento 00 UTC [SENZA FONTE] (§3, r.64-65)
  → #53 corpo + commento 2026-09-29: "All 246" messages carry 128 (eccodes GRIB2 default): "inside `grib_v3` the value discriminates nothing". The fix (487ba14) touched only CLAUDE.md and the converter.
- `MISSING_VARIABLES A020` Statici, land-use / land-cover: solo categoria dominante, mai frazioni; il file che contiene le frazioni non esiste più [SENZA FONTE] (§1, r.33)
  → #31 [commento 2026-09-19]; #12 [corpo]: "`LANDUSEF` | recoverable, and already recovered — geo_em.d02, 21 categories, read by static_ref.py"
- `MISSING_VARIABLES A059` Altezza dello strato limite: confidenza "Reasonable", stessa classe di diagnostica che il modello applicherebbe [SENZA FONTE] (§3, r.82)
  → #18 [commento]: "a bulk-Richardson diagnosis would be **ours**, not the model's, so it fails the publication rule"
- `MISSING_VARIABLES A068` Onde: unica via, una run di modello d'onda o una rianalisi d'onda esterna (ERA5 waves a ~31 km), che perde il dettaglio costiero che motiva un prodotto a 3 km [SENZA FONTE] (§4, r.92)
  → verifica 1 NON_TROVATA — —: ERA5 waves / 31 km non discussi
  → verifica 2 (online) CONTRADDETTA — https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation "ERA5: data documentation" (last modified 2026-09-08): "The wave data are produced and archived on a different grid to that of the atmospheric model, namely a reduced latitude/longitude grid with a resolution of 0.36 degrees (HRES)"; ~31 km e' la risoluzione atmosferica ("31km, 0.28125 degrees"), non quella delle onde (0.36° ≈ 40 km in latitudine, calcolato 0.36×111 km). La via "rianalisi d'onda esterna" esiste
- `MISSING_VARIABLES A094` `blh`: una nuova run che scriva `PBLH`, o la diagnostica di Richardson bulk di §3, stessa classe di diagnostica del modello [SENZA FONTE] (§4, r.101)
  → #18 [commento]; #29 [corpo]: re-run confermata, ma "a bulk-Richardson diagnosis would be ours, not the model's, so it fails the publication rule"
- `MISSING_VARIABLES A122` Esatta dove la risposta è nota: sull'acqua la skin temperature del modello è la SST e l'inversione la recupera a 0.005 K [SENZA FONTE] (§5, r.138-139)
  → #55 [corpo e commento 2026-09-29]: la fonte dà "0.0005 K RMSE" (prima registrato 0.0015 K), non 0.005 K
- `MISSING_VARIABLES A124` Sulla neve l'emissività effettivamente usata dallo schema non può essere ricostruita: circa 0.8 K di incertezza residua [SENZA FONTE] (§5, r.140-141)
  → #55 [corpo]; #28 [corpo]: la regola neve è misurata: "It is a switch ... 0.98"; land reproduced "99.98 % (July) … 93.05 % (January)"; nessuno 0.8 K
- `MISSING_VARIABLES A129` Correzione dello 0.8 % in mediana [SENZA FONTE] (§5, r.147)
  → #41 [corpo e commento 2026-09-25]: "over the full 3-D field it is 0.011 per cent" in mediana; "2.26 % at most, 1.44 % at p99"
- `MISSING_VARIABLES A131` CAPE non definita nei pochi percento di punti senza livello di equilibrio [SENZA FONTE] (§5, r.149-150)
  → verifica 1 NON_TROVATA — —: assenza del livello di equilibrio non discussa
  → verifica 2 (dati) CONTRADDETTA — srun dcgp_usr_prod: wrf.getvar(cape_2d) su wrfout_share/2024-09-04/wrfout_d02_2024-09-04_16:00:00, gap = non finito o |x|>=1e30 come in convert_to_pressure_levels.gaps(); più lettura eccodes di mucape/mucin in grib_v3/.../2024090415.grib (misura 2026-09-29): CAPE senza risposta (nessun livello di equilibrio) sul 34.25 % del dominio alle 16Z, non "pochi percento"; nel GRIB 15Z mucape = 0 su 744 745 punti (33.5 %, i gap vi sono scritti a 0, nessun bitmap); il commento in convert_to_pressure_levels.py r.858-859 dice "half the domain on a quiet day"
- `MISSING_VARIABLES A132` In quei punti si scrive zero invece di un valore mancante, per mantenere i campi densi [SENZA FONTE] (§5, r.150-151)
  → #54 [commento 2026-09-25]: vero solo per mucape; per mucin "A GRIB bitmap where cape_2d declined ... Commit 3ad8a2d"
- `MISSING_VARIABLES A133` Zero è anche la lettura fisicamente corretta (nessuna inibizione, nessuna energia disponibile) [SENZA FONTE] (§5, r.151-152)
  → #54 [corpo]: "For mucape that reasoning is right ... For mucin it is backwards"
- `MISSING_VARIABLES N027` risoluzione ERA5 waves = ~31 km (§4, r.92) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: no issue mentions ERA5 waves or their resolution; #12 only says no waves (sf_ocean_physics = 0)
  → verifica 2 (online) CONTRADDETTA — come A068: ERA5 waves = 0.36° (HRES), non ~31 km (0.28125° e' l'atmosfera)
- `MISSING_VARIABLES N043` incertezza residua skt sulla neve = circa 0.8 K (§5, r.140-141) [SENZA FONTE]
  → #55 [corpo]; #26 [commento 2026-09-25]: the snow switch is confirmed, not unreconstructable: "the snow switch ... all survive re-measurement"; land RMSE is "0.115–0.133 K (January, February), p99 0.85 K"
- `MISSING_VARIABLES N044` correzione mixing ratio -> contenuto specifico = 0.8 % in mediana (§5, r.147) [SENZA FONTE]
  → #19 [commento 2026-09-22]: "the '0.8 % median, 2.2 % at most' ... reproduces at the top (2.26 %) and not in the middle — ... the median is 0.011 % and the p99 is 1.44 %"
- `MISSING_VARIABLES N046` punti senza livello di equilibrio = "few percent" (§5, r.149-150) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: no issue gives the share of points without an equilibrium level
  → verifica 2 (dati) CONTRADDETTA — idem: frazione di punti senza livello di equilibrio 34.25 % (16Z, 2024-09-04) contro "few percent"; mucin mascherato (bitmap) sul 62.48 % nel GRIB 15Z e CIN gap 63.30 % a 16Z

## 2. Confermate con differenze (si usa il numero o il dettaglio della fonte)

- `CHAPTER_VARIABLES A019` Identità dei parametri ECMWF paramId / shortName ovunque, quindi l'archivio è direttamente confrontabile con ERA5 [SENZA FONTE] (§1, r.35)
  → #11 corpo; #14 corpo: "GRIB2 with ECMWF paramIds"; "The harness must match on `paramId`". "Directly comparable" is not stated: #14 notes ERA5 (ed. 1) and CHAPTER (ed. 2) use different level types.
- `CHAPTER_VARIABLES A022` Periodo: 2019, 2024 e 2025-01-01 → 2025-07-02, orario; 2020–2023 da seguire [SENZA FONTE] (§1, r.38)
  → #59 corpo; #64 corpo: Only the 2025 end is attested: "it ends 2025-07-02 (`7b2e2ce`)". #64 says "2020–2024 ... are not in the target window". No source gives the 2019/2024 coverage or "2020–2023 to follow".
- `CHAPTER_VARIABLES A027` I campi a singolo livello stanno su `surface`, `heightAboveGround` (2, 10, 100, 200 m), `meanSea`, `entireAtmosphere` (integrali di colonna) o, per il bilancio radiativo al top dell'atmosfera, `nominalTop` [SENZA FONTE] (§2, r.47-49)
  → #20 corpo; #21 corpo/commento; #22 commento: `heightAboveGround` (incl. `200u`/`200v`), `entireAtmosphere`, and "`nominalTop` for the five TOA fields" are attested. `meanSea` is not found in any source.
- `CHAPTER_VARIABLES A028` Campi istantanei: product definition template 0; `dataDate`/`dataTime` sono il tempo valido [SENZA FONTE] (§3, r.53-54)
  → #15 corpo: "instantaneous ones with `dataDate`/`dataTime` = valid time". PDT 0 is not named in any source.
- `CHAPTER_VARIABLES A038` `slor` per ERA5: pendenza dell'orografia **sottogriglia**, parametro dello schema di form-drag [SENZA FONTE] (§4, r.73)
  → #37 corpo; #25 commento: "paramId 163 is defined as the slope of the **sub-grid** orography". The form-drag qualification is not in any source.
- `CHAPTER_VARIABLES A043` `10fg` per ERA5: raffica da parametrizzazione (turbolenta + convettiva); scritto: massimo orario del vento a 10 m **risolto** [SENZA FONTE] (§4, r.74)
  → #50 corpo: "ERA5's is a parameterised gust"; ours is the resolved 10 m wind maximum. The "turbulent + convective" decomposition is not found.
- `CHAPTER_VARIABLES A076` L'errore di derivazione è trenta volte più piccolo del bias freddo fisico della pelle su terra [SENZA FONTE] (§4, r.103-105)
  → #55 commento 2026-09-29T07:51; #57 commento: "thirty times smaller than the physical cold bias". Stated against 0.115–0.133 K (0.01 threshold), not the 0.084–0.119 K now in the doc.
- `CHAPTER_VARIABLES A106` Il campo grezzo è il default WPS di 10 m sul 99.56 % del dominio, e 79 464 delle 88 785 celle di lago portano lo stesso default [SENZA FONTE] (§4, r.141-142)
  → #25 corpo: "`LAKE_DEPTH` is the 10 m WPS default on 99.56% of the domain". "79 464 of 88 785" is not found in any source.
- `CHAPTER_VARIABLES A114` Quelle colonne sono dal 4 % al 29 % del dominio, meno in inverno [SENZA FONTE] (§5, r.152)
  → #54 corpo: "CIN is a real number on **3.8 %** (January) ... **28.8 %** (July)". The doc rounds to 4 %–29 % without saying so.
- `CHAPTER_VARIABLES A116` `tsn`: celle con copertura nevosa oltre 0.9 (≈ 29 mm di equivalente in acqua); fuori stagione il campo è legittimamente vuoto [SENZA FONTE] (§5, r.153)
  → #24 commento 2026-09-22: "`tsn`'s bitmap is exactly `SNOWC > 0.9`"; "entirely absent at 7 of 34 timesteps, which is the summer". "≈ 29 mm" is not found.
- `CHAPTER_VARIABLES A120` `tvl`: ovunque tranne le celle dove un arbusteto domina la vegetazione bassa (124 672 celle, 15.8 % di quelle con `cvl > 0`) [SENZA FONTE] (§5, r.157)
  → #25 corpo + commento: "`tvl` is masked on the 124672 cells where a shrubland dominates". "15.8 % of cells with `cvl > 0`" is not found; A261 of the same doc says 16.2 %.
- `CHAPTER_VARIABLES A126` Leaf area index (`lai_lv`, `lai_hv`) scartato deliberatamente: il modello porta un solo LAI per cella, ERA5 ne vuole uno per classe di vegetazione, definito per unità di area vegetata; ogni split sarebbe una nostra assunzione, quindi nessuno dei due è scritto [SENZA FONTE] (§6, r.168-170)
  → #17 corpo; docs/audit/exclusions.md: "the model carries one LAI per cell and ERA5 wants one per vegetation class, so any split is our assumption". "Per unit vegetated area" is not found.
- `CHAPTER_VARIABLES A130` Quattro voci che stavano qui fino al 2026-09-17 sono entrate nell'archivio, perché `geo_em.d02` è tornato e l'obiezione sul suolo aveva una risposta [SENZA FONTE] (§6, r.179-180)
  → #35 corpo; #11 corpo: "the four entries that moved *into* the archive in September". The 2026-09-17 date is not in any source.
- `CHAPTER_VARIABLES A259` Ogni riga tradotta è un'identità semantica: il tipo ECMWF nomina la stessa vegetazione della classe MODIS [SENZA FONTE] (§8.tv, r.383-384)
  → #25 commento 2026-09-22: "code table 4.234 exact"; only row 5→18 is explicitly called "a semantic identity in 4.234". No source asserts it for every row.
- `CHAPTER_VARIABLES A261` Sceglierne uno sarebbe stata una nostra invenzione sul 16.2 % delle celle vegetate, quindi il campo è lasciato mancante lì; `cvl` riporta ancora la copertura [SENZA FONTE] (§8.tv, r.386-388)
  → #25 corpo: The shrubland mask is attested; "16.2 % of vegetated cells" is not found (A120 of the same doc says 15.8 %).
- `CHAPTER_VARIABLES A262` Le classi che sarebbero state le altre righe ambigue, 11 e 14, non occorrono affatto in questo dominio [SENZA FONTE] (§8.tv, r.388-389)
  → #26 commento 2026-09-25; #28 corpo: "five categories never occur in this domain"; #28 names 11, 14, 19, 20 (+0) as unmeasurable. The link to "ambiguous rows" is not stated.
- `CHAPTER_VARIABLES A275` Entrambi gli insiemi (`swvl`, `stl`) sono mascherati sull'acqua [SENZA FONTE] (§8.soil, r.420)
  → #24 commento; #38 commento 2026-09-25: Masked on water, but since e70ddb4 on geo_em's **permanent** land mask, so sea-ice cells are masked too.
- `CHAPTER_VARIABLES N011` angoli del dominio = 23.472 N, 19.972 W → 60.001 N, 42.256 E (§1, r.31) [SENZA FONTE]
  → #14 commento 2026-09-21: la fonte dà 4 decimali: "23.4719..60.0006 N and -19.9722..42.2555 E"; la scheda arrotonda a 3 senza dichiararlo
- `CHAPTER_VARIABLES N015` dimensione file = ~747 MB — per ora, "misurata, non stimata" (§1, r.36) [SENZA FONTE]
  → verifica 1 CONFERMATA_CON_DIFFERENZE — #13 commento 2026-09-19: nessun ~747 MB; la fonte misura per il campione "615-679 MB [00Z] against 691-756 MB [12Z]"
  → verifica 2 (dati) CONFERMATA_CON_DIFFERENZE — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 modificati negli ultimi 20 min (campagna in corso), tenuti i 184 con esattamente 246 messaggi (header walk di hpc/grib_schema_ok.py), os.path.getsize, unità decimali (misura 2026-09-29): media 737.0 MB (voce: ~747 MB), range 643.7-773.9 MB su 184 file; 00Z: media 661.0 MB (643.7-682.7, n=8); non-00Z: media 740.5 MB (676.2-773.9, n=176); campione solo settembre 2024
- `CHAPTER_VARIABLES N016` volume = ~17.9 GB/giorno (§1, r.36) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: ~17.9 GB/giorno non compare in issue né in docs/audit
  → verifica 2 (dati) CONFERMATA_CON_DIFFERENZE — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 modificati negli ultimi 20 min (campagna in corso), tenuti i 184 con esattamente 246 messaggi (header walk di hpc/grib_schema_ok.py), os.path.getsize, unità decimali (misura 2026-09-29); somma dei 24 file per giorno completo: 17.71 GB/giorno medio (voce: ~17.9), range 17.31-18.11 su 7 giorni completi
- `CHAPTER_VARIABLES N017` volume = ~6.6 TB/anno (§1, r.36) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: ~6.6 TB/anno non compare in issue né in docs/audit
  → verifica 2 (dati) CONFERMATA_CON_DIFFERENZE — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 modificati negli ultimi 20 min (campagna in corso), tenuti i 184 con esattamente 246 messaggi (header walk di hpc/grib_schema_ok.py), os.path.getsize, unità decimali (misura 2026-09-29); media file × 8760 e media giorno × 365: 6.46 TB/anno (6.456 e 6.465; voce: ~6.6 TB); in TiB 5.87
- `CHAPTER_VARIABLES N024` `generatingProcessIdentifier` = 128 — messaggi accumulati (§3, r.64) [SENZA FONTE]
  → #53 corpo; commento 2026-09-29: valore 128 giusto ma non marca gli accumulati: "All 246 [...] inside `grib_v3` the value discriminates nothing"
- `CHAPTER_VARIABLES N069` copertura di `mucin` = 4 %–29 % del dominio — meno in inverno (§5, r.152) [SENZA FONTE]
  → #54 corpo; commento 2026-09-25: la fonte dà la frazione mascherata: "constant zero on 71 to 96 per cent"; misurato "masked fraction 94.3 % [feb] / 71.2 % [lug]"
- `CHAPTER_VARIABLES N070` soglia di copertura nevosa per `tsn` = 0.9 (≈ 29 mm di equivalente in acqua) (§5, r.153) [SENZA FONTE]
  → #24 corpo; commento 2026-09-22: 0.9 confermato: "`tsn`'s bitmap is exactly `SNOWC > 0.9`"; "≈ 29 mm" non trovato
- `CHAPTER_VARIABLES N073` celle con `tvl` mancante = 124 672 — 15.8 % di quelle con `cvl > 0` (§5, r.157) [SENZA FONTE]
  → #25 commento 2026-09-22: 124 672 confermato ("124 672 `tvl` masked"); 15.8 % non trovato
- `CHAPTER_VARIABLES N079` celle di terra con vegetazione alta e bassa entrambe > 5 % = 17.9 % (§6, r.190-191) [SENZA FONTE]
  → #25 commento 2026-09-22 (misura); #12 commento 2026-09-19: misurato "233 844 (17.93 %) with both vegetation types above 5 %"; la scheda arrotonda a 17.9
- `CHAPTER_VARIABLES N093` accordo land use statico / categoria dominante oraria = 100.00 % — esclusa la ricodifica lago→acqua (§8, r.358) [SENZA FONTE]
  → #59 commento 2026-09-28; #62 commento 2026-09-29: "`LU_INDEX` vs `IVGTYP`, lake recode excluded": 1.0000 (2019-07, 2025-01) ma 0.9998 su 2025-02-15T12
- `CHAPTER_VARIABLES N094` copertura arborea Woody Savannas / Interrupted forest = 30–60 % (§8.tv, r.373) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: "30–60 % tree cover" non compare; #12 cita solo le righe 'Woody Savannas' della tabella
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://lpdaac.usgs.gov/documents/1409/MCD12_User_Guide_V61.pdf Sulla-Menashe & Friedl, "User Guide to Collection 6 MODIS Land Cover (MCD12Q1 and MCD12C1) Product", C6.1, 20 Apr 2022, Table 3 (IGBP legend): "Woody Savannas 8 Tree cover 30-60% (canopy >2m)" confermato; per "Interrupted forest" (tvh 19) nessuna soglia di copertura arborea in IFS Cy41r2 Part IV (compare solo nelle tabelle dei parametri, es. Tab. 8.1) ne' nel param-db 30: il "both are 30-60 %" vale solo per il lato IGBP
- `CHAPTER_VARIABLES N103` strati ERA5 = 0–7, 7–28, 28–100, 100–289 cm (§8.soil, r.414) [SENZA FONTE]
  → #24 commento 2026-09-22; docs/audit/exclusions.md (TMN): espliciti solo "the 0–7 cm average" e "`stl4` over 100-289 cm"; 7–28 e 28–100 non trovati
- `CHAPTER_VARIABLES N104` matrice dei pesi = 4 × 6 — applicata ai sei livelli del modello (§8.soil, r.417) [SENZA FONTE]
  → #24 commento 2026-09-22: "4 × 6" non scritto; la fonte: "row sums exactly 1.0, all four", nodi "(0,1,2), (1,2,3), (2,3,4), (3,4,5)" su 6 ZS
- `MISSING_VARIABLES A005` La ri-conversione costa diversi giorni di trasferimento dati e va fatta una sola volta [SENZA FONTE] (§0, r.9)
  → #59 [corpo]: "the campaign costs about eleven days of datamover time"; "the regeneration should happen once" — la fonte dà ~10-11 giorni e ~152 TB, non "diversi giorni"
- `MISSING_VARIABLES A010` Ogni identificativo di parametro ECMWF passato avanti e indietro nell'encoder GRIB per confermare nome e unità [SENZA FONTE] (§0, r.15-16)
  → verifica 1 NON_TROVATA — —: nessuna fonte descrive il round trip dei paramId nell'encoder
  → verifica 2 (repo) CONFERMATA_CON_DIFFERENZE — commit f2c93cc (2026-09-17), messaggio; hpc/check_grib_sanity.py r.55-85; tests/: f2c93cc: "every paramId round-tripped through eccodes for name and units" (controllo fatto una volta, dichiarato nel commit). Nel codice non c'è un test round-trip permanente: check_grib_sanity rilegge soltanto lo shortName di ogni messaggio e conta i messaggi contro EXPECTED, quindi le unità non vengono controllate; tests/ contiene solo test_ledger.py. c1f8a2f (2026-09-16) cita un round-trip fallito: "W was written with paramId 40, which eccodes reads back as swvl2"
- `MISSING_VARIABLES A024` Ghiaccio marino: concentrazione consegnata [SENZA FONTE] (§1, r.36)
  → #25 [commento 2026-09-22]: consegnata, ma "`ci` is a flag, not a fraction — two distinct values, from FRACTIONAL_SEAICE = 0"
- `MISSING_VARIABLES A025` Ghiaccio marino: spessore, neve sul ghiaccio, temperatura del ghiaccio e albedo non disponibili [SENZA FONTE] (§1, r.36)
  → #12 [corpo]; #18 [commento]: spessore: "no ... ice thickness"; "the lake and sea-ice-layer families" impossibili; neve su ghiaccio e albedo non nominati
- `MISSING_VARIABLES A049` Il file statico `geo_em.d02`, registrato qui come irrecuperabile, è stato ottenuto da LRZ il 2026-09-18 [SENZA FONTE] (§3, r.74-75)
  → #11 [corpo]; #31 [commento 2026-09-19]: "the geo_em recovery"; data 2026-09-18 e provenienza LRZ non riportate nelle issue
- `MISSING_VARIABLES A055` Coefficiente di drag senza effetto onde: dalla lunghezza di rugosità del modello, `Cd = (κ / ln(10/z0))²` [SENZA FONTE] (§3, r.81)
  → verifica 1 NON_TROVATA — #18 [corpo]: la fonte usa `u*/κ · ln(10/z0)` solo per u10n/v10n; nessun Cd
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://raw.githubusercontent.com/wrf-model/WRF/v4.1.1/phys/module_sf_sfclayrev.F (WRF v4.1.1, righe 6, 488, 681, 874, 975): Codice: `GZ10OZ0=ALOG((10.+ZNT)/ZNT)`, `PSIX10=GZ10OZ0-PSIM10`, `Cd=(karman/psix10)*(karman/psix10)`; Charnock `CZO=0.0185`, `ZNT=CZO*UST*UST/G+0.11*1.5E-5/UST` sull'acqua. Differenze: (a) il Cd del modello include la correzione di stabilita' PSIM10, quindi `(κ/ln(10/z0))²` e' solo il limite neutro, non "precisely the drag the simulation used"; (b) il log e' ln((10+z0)/z0). Stessa forma in IFS Cy41r2 Part IV eq. 3.14 (CM con Ψ=0)
- `MISSING_VARIABLES A056` Coefficiente di drag senza onde: confidenza "Exact", è esattamente il drag usato dalla simulazione (Charnock, nessun accoppiamento d'onda) [SENZA FONTE] (§3, r.81)
  → #56 [corpo]: "Over sea ... both roughnesses are Charnock"; sulla terra ZNT "is a land-use lookup with a snow override"
- `MISSING_VARIABLES A063` `10efg`, `10nfg`: scomporre la magnitudine lungo il vento a 10 m è possibile ed economico, ma giudicato troppo debole per pubblicarlo con nomi ERA5; deciso di non produrle [SENZA FONTE] (§4, r.90)
  → #17 [commento 2026-09-22]: "by decision, only a resolved-wind maximum exists"; la scomposizione lungo il vento non è discussa
- `MISSING_VARIABLES A065` TKE: unica via, rifare la run WRF con uno schema PBL con TKE (MYNN o MYJ) [SENZA FONTE] (§4, r.91)
  → verifica 1 NON_TROVATA — —: MYNN/MYJ non nominati
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://raw.githubusercontent.com/wrf-model/WRF/v4.1.1/run/README.namelist (WRF v4.1.1); https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/physics.html WRF Users Guide, "WRF Physics", tabella PBL: README: "= 1, YSU scheme / = 2, Mellor-Yamada-Janjic TKE scheme / = 5, MYNN 2.5 level TKE scheme / = 6, MYNN 3rd level TKE scheme"; Users Guide classifica MYJ, QNSE-EDMF, MYNN2, MYNN3, BouLac, UW, GBM, EEPS, KEPS come "Turbulent kinetic energy prediction", YSU no. Differenze: MYNN/MYJ non sono le sole opzioni con TKE, e `km_opt = 2` ("1.5 order TKE closure (3D)", "not recommended for DX > 2 km") e' un'altra via
- `MISSING_VARIABLES A069` Coefficiente di drag con effetto onde: lo scambio superficiale ha usato la rugosità di Charnock senza stato del mare [SENZA FONTE] (§4, r.93)
  → #56 [corpo]: "Over sea ... both roughnesses are Charnock"; l'assenza di stato del mare è solo implicita in SF_OCEAN_PHYSICS=0
- `MISSING_VARIABLES A073` Spessore del ghiaccio marino, spessore della neve sul ghiaccio: non simulati; il ghiaccio marino entra solo come campo di concentrazione al contorno [SENZA FONTE] (§4, r.95)
  → #12 [corpo]: "no waves, currents, SSH or ice thickness"; ghiaccio "solo come concentrazione al contorno" non detto
- `MISSING_VARIABLES A074` Spessore del ghiaccio / neve sul ghiaccio: unica via, un prodotto esterno di ghiaccio marino [SENZA FONTE] (§4, r.95)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description CMEMS GLORYS12V1: Esiste un prodotto esterno con "Sea ice thickness"; lo spessore della neve sul ghiaccio non e' stato verificato in quel prodotto; "unica via" e' una valutazione
- `MISSING_VARIABLES A075` Albedo del ghiaccio marino come proprietà prognostica: non simulato [SENZA FONTE] (§4, r.96)
  → #37 [corpo]: "0.65 on sea ice, which is WRF's seaice_albedo_default and follows from SEAICE_ALBEDO_OPT = 0"
- `MISSING_VARIABLES A076` Albedo del ghiaccio marino: approssimabile radiativamente (§3), ma non come variabile di un modello di ghiaccio [SENZA FONTE] (§4, r.96)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) CONFERMATA_CON_DIFFERENZE — docs/audit/run-configuration.md r.885-898; docs/audit/f7-static-and-surface.md r.102-103: parte fattuale confermata: il ghiaccio marino viene solo dai dati di input, è binario per cella (FRACTIONAL_SEAICE=0) e ha albedo costante 0.65 (SEAICE_ALBEDO_OPT=0), quindi non esiste come variabile di un modello di ghiaccio. "Approssimabile radiativamente" è una valutazione; inoltre §3 dell'md attuale non ha più una riga sull'albedo (dice "surface albedo is now delivered", al/fal), quindi il rimando "(§3)" non trova un'approssimazione specifica per il ghiaccio
- `MISSING_VARIABLES A078` Snowmelt: non può essere riferito alle 00 UTC come le altre accumulazioni; pubblicato col nome ERA5 sarebbe sbagliato [SENZA FONTE] (§4, r.97)
  → #17 [commento 2026-09-22]; #35 [corpo]: ACSNOM "non-monotone ... confirmed: 15 of 16 days, up to 8.2 mm"; il nesso col riferimento 00Z non è scritto
- `MISSING_VARIABLES A084` Flussi di calore: solo una nuova run che li scriva [SENZA FONTE] (§4, r.98)
  → #31 [commento 2026-09-19]: "TSK, HFX, LH, QFX, GRDFLX, EMISS, PBLH | unrecoverable"; "una nuova run" non detto esplicitamente
- `MISSING_VARIABLES A085` Ricostruzione dal bilancio energetico superficiale fallisce: manca anche il flusso di calore nel suolo, due incognite in un'equazione [SENZA FONTE] (§4, r.98)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) CONFERMATA_CON_DIFFERENZE — docs/audit/run-configuration.md r.828-831; docs/audit/f8-surface-exchange.md r.301-303: confermato che manca anche il flusso di calore nel suolo: "verified absent: TSK, HFX, LH, QFX, GRDFLX ..."; f8: "HFX, LH and the ground heat flux are the three fields this archive does not have". "Due incognite in un'equazione" non compare in nessuna fonte, e f8 conta tre campi mancanti
- `MISSING_VARIABLES A097` `swvl1-4`, `stl1-4`: l'obiezione era contro il rietichettare i valori puntuali, e resta valida [SENZA FONTE] (§4, r.109)
  → #24 [corpo]: "swvl1-4 / stl1-4 are integrals, not relabellings"; l'obiezione storica non è riportata
- `MISSING_VARIABLES A100` `tvl`, `tvh`, `slt`: le categorie sono MODIS-IGBP e STATSGO di WRF, i paramId portano tabelle di codici ECMWF (motivo dell'esclusione) [SENZA FONTE] (§4, r.110)
  → verifica 1 NON_TROVATA — —: il motivo storico dell'esclusione non è nelle fonti
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://codes.ecmwf.int/parameter-database/api/v1/param/29/ , /30/ , /43/ e /api/v1/unit/ (ECMWF Parameter Database, update 2024-10-24 / 2024-06-06); https://raw.githubusercontent.com/ecmwf/eccodes/develop/definitions/grib2/tables/30/4.234.table e 4.213.table: Unita' dichiarate: tvl/tvh "(Code table 4.234)", slt "(Code table 4.213)". Differenza: 4.234 e 4.213 sono tabelle del master WMO GRIB2 (eccodes grib2/tables/30), non tabelle locali ECMWF; e la 4.213 WMO elenca 11 classi (Sand...Clay) mentre il param-db 43 descrive 7 tipi ECMWF
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.1/users_guide_chap3.html WRF User's Guide v4.1 cap. 3 (WPS); https://raw.githubusercontent.com/wrf-model/WPS/v4.1/geogrid/GEOGRID.TBL.ARW; param-db ECMWF 29/30/43: "By default, the geogrid program will interpolate land use categories from MODIS IGBP 21-category data"; suolo "16 soil categories" (Table 3), ma la guida v4.1 non nomina STATSGO; lato ECMWF vedi riga A100 (parte ECMWF): tabelle 4.234/4.213 sono WMO, non ECMWF-locali
- `MISSING_VARIABLES A105` `cvl`, `cvh`: prima poggiavano su una categoria dominante per cella, mentre ERA5 lascia coesistere vegetazione bassa e alta [SENZA FONTE] (§4, r.111)
  → #12 [corpo]: "The run reduced every cell to one dominant land-use ... cvl/cvh from geo_em are therefore more informative"; la versione precedente di cvl/cvh non è descritta
- `MISSING_VARIABLES A108` `lai_lv`, `lai_hv`: il modello porta un solo LAI per cella; ERA5 ne vuole uno per classe di vegetazione, definito per unità di area vegetata [SENZA FONTE] (§4, r.117)
  → #17 [commento 2026-09-22]: "one LAI per cell, ERA5 wants one per class | holds"; "per unità di area vegetata" non detto
- `MISSING_VARIABLES A112` `anor`, `isor`: angolo e anisotropia ECMWF vengono dall'autostruttura della covarianza del gradiente del terreno; correlati, non uguali; la differenza non sta in una riga [SENZA FONTE] (§4, r.118)
  → #17 [corpo e commento 2026-09-22]: "not ECMWF's gradient-covariance eigenstructure"; "the quantities differ" — "correlati" e "non in una riga" non detti
- `MISSING_VARIABLES A113` Se richiesti, i campi WRF sottostanti esistono e si possono consegnare coi loro nomi (`LAI`, `VEGFRA`, `OA1-4`, `OL1-4`), senza affermare equivalenza ERA5 [SENZA FONTE] (§4, r.120-121)
  → #63 [corpo]; #35 [corpo]: solo per LAI: "can be delivered under its own name"; VEGFRA/OA/OL non discussi
- `MISSING_VARIABLES A115` Copertura nuvolosa frazionaria; una bozza precedente della nota diceva binaria, ed era sbagliato [SENZA FONTE] (§5, r.127-128)
  → #12 [corpo]; #19 [corpo]: "an earlier note in CLAUDE.md claimed binary and was wrong": la nota sbagliata era in CLAUDE.md, non in questo documento
- `MISSING_VARIABLES A142` La finestra di un'ora dichiarata è giusta solo l'88 % delle volte [SENZA FONTE] (§5, r.162-163)
  → #49 [corpo]: la fonte dà il complemento: reset mancato "17 (12.3 %)" su 138 transizioni; "88 %" non scritto
- `MISSING_VARIABLES A146` Questi campi sono scritti in ogni file orario e non vanno trattati come un unico campo statico per l'archivio [SENZA FONTE] (§5, r.167-168)
  → #03 [corpo]: "Only lsm (from LANDMASK) and al (from ALBBCK) still vary"; tvl/tvh/slt ora statici dal sidecar
- `MISSING_VARIABLES A149` La temperatura della neve esiste solo dove c'è neve: è la temperatura al top della colonna neve/suolo; lontano dalla neve è una temperatura del suolo [SENZA FONTE] (§5, r.173-175)
  → #24 [corpo]; docs/audit/f6-soil-and-snow.md: "SOILT1 ... is the temperature inside snow"; "tsn is SOILT1 where SNOWC > 0.9"
- `MISSING_VARIABLES A150` Temperatura della neve scritta come mancante fuori dalla neve [SENZA FONTE] (§5, r.175)
  → #24 [commento]: "tsn's bitmap is exactly SNOWC > 0.9": mancante anche dove c'è neve con copertura ≤ 0.9
- `MISSING_VARIABLES A151` `al` è il fondo climatologico senza neve con cui il modello è stato inizializzato [SENZA FONTE] (§5, r.176-177)
  → #37 [corpo e commento 2026-09-29]: "al is a two-season table value by dominant category", cambia su 1 171 937 punti (89.9 %) tra WINTER e SUMMER
- `MISSING_VARIABLES A163` Tutte e tre pubblicate perché `ro` è il totale canonico ERA5; `ro` e `sro` sono messaggi consapevolmente duplicati [SENZA FONTE] (§5, r.189-190)
  → #51 [commento 2026-09-29]: "ro and sro are knowingly duplicate messages"; la ragione "ro totale canonico ERA5" non è scritta
- `MISSING_VARIABLES A176` Eccezione il massimo del vento a 10 m: copre solo l'ora precedente, perché il modello lo azzera a ogni output [SENZA FONTE] (§5, r.204-205)
  → #49 [corpo]: encoding 0-1 corretto, ma "on 12 per cent of hours WSPD10MAX was not reset, so it is a longer one"
- `MISSING_VARIABLES A177` La geolocalizzazione è ora esatta a ~2 m; la griglia dichiara la terra sferica di raggio 6370 km su cui WRF integra [SENZA FONTE] (§5, r.206-207)
  → #26 [commento]; docs/audit/f8-surface-exchange.md: "shapeOfTheEarth = 1 with radius = 6370000 on all 246 messages"; "~2 m" non trovato
- `MISSING_VARIABLES A178` I file GRIB1 precedenti non potevano esprimerlo ed erano sbagliati fino a ~1.1 km al bordo nord del dominio [SENZA FONTE] (§5, r.207-208)
  → #26 [corpo]: "without it eccodes derives a grid off by ~1.1 km at the northern edge"; il riferimento al GRIB1 non è nella issue
- `MISSING_VARIABLES A180` La questione del file statico `geo_em` è chiusa al contrario di quanto diceva il documento: ottenuto da LRZ il 2026-09-18, e tutto ciò che ne dipendeva è ora consegnato (§3, §4) [SENZA FONTE] (§6, r.215-217)
  → #63 [corpo]; #31 [commento 2026-09-19]: "the geo_em recovery added cvl, cvh, tvl, tvh, slt, cl, dl and the eight soil layers"; data e LRZ non riportati
- `MISSING_VARIABLES A182` Consegnati con nomi ERA5: umidità e temperatura del suolo (4 strati, vere medie di strato ERA5), profondità, densità, copertura e temperatura della neve, nevicata [SENZA FONTE] (§6, r.219-221)
  → #24 [corpo]; #63 [corpo]: soil layers come integrali ERA5, sd/snowc/rsn/tsn auditati; "nevicata" (sf) è però solo SNOWNC senza graupel (#52)
- `MISSING_VARIABLES A186` Consegnato il bilancio radiativo completo (discendente, netto e clear-sky, alla superficie e al top dell'atmosfera) [SENZA FONTE] (§6, r.224-225)
  → #22 [corpo]: famiglia radiazione auditata; l'elenco completo "netto e clear-sky, superficie e TOA" non è enunciato così
- `MISSING_VARIABLES A191` Si consegnano 13 livelli di pressione; ERA5 ne usa 37, di cui 29 dentro il dominio del modello [SENZA FONTE] (§6, r.232-233)
  → #19 [corpo]: "the 8 ERA5 levels above 50 hPa are above WRF's P_TOP"; 37 e 29 non scritti
- `MISSING_VARIABLES A193` Con 29 livelli il file orario passerebbe da ~0.8 GB a ~1.45 GB e un anno di archivio da 7.0 a 18.1 TB; per questo si sono tenuti 13 livelli [SENZA FONTE] (§6, r.233-235)
  → verifica 1 NON_TROVATA — —: dimensioni a 29 livelli non riportate
  → verifica 2 (dati) CONFERMATA_CON_DIFFERENZE — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 modificati negli ultimi 20 min (campagna in corso), tenuti i 184 con esattamente 246 messaggi (header walk di hpc/grib_schema_ok.py), os.path.getsize, unità decimali (misura 2026-09-29): solo parte misurabile: file orario a 13 livelli 0.737 GB (voce ~0.8), anno 6.46 TB (voce 7.0); archivio effettivamente a 13 livelli di pressione (13 variabili × 13 livelli nello schema a 246 messaggi); 29 livelli e la motivazione della scelta non misurabili
  → verifica 2 (repo) CONFERMATA_CON_DIFFERENZE — commit f2c93cc (2026-09-17), messaggio r.44-49 e diff di MISSING_VARIABLES.md r.208-211: fonte: f2c93cc "Day-weighted ~767 MB/hour, 19 GB/day, ~7.0 TB/year. The 37 ERA5 pressure levels were evaluated and rejected: 8 are above the model top and the 29 feasible ones would cost 1.45 GB/hour and 18.1 TB/year". Il modo in cui è stata fatta la stima a 29 livelli non è nel repo. I due numeri non tornano tra loro: 1.45 GB × 8760 h = 12.7 TB, non 18.1 (18.1 TB/anno corrisponderebbe a ~2.07 GB/ora). La base a 13 livelli è quella del 2026-09-17 (767 MB, 7.0 TB); CLAUDE.md oggi dà ~747 MB e ~6.55 TB/anno
- `MISSING_VARIABLES N014` durata di una run = 24 h (§2, r.53) [SENZA FONTE]
  → #25 [corpo]; #12 [commento 2026-09-19]: #25: "`sst` is constant within each 24 h run"; but #12 gives the spinup structure "`start_hour = 18`, `run_hours = 30`", so a run integrates 30 h
- `MISSING_VARIABLES N023` accordo land use geo_em / categoria dominante del modello = 100.00 % dei punti — escluso il recode dei laghi (§3, r.75-76) [SENZA FONTE]
  → #59 [commento 2026-09-28]; #62 [corpo]: `LU_INDEX` vs `IVGTYP`, lake recode excluded: 1.0000 (2019-07-15T12, 2025-01-15T12) but 0.9998 on 2025-02-15T12, not 100.00 % everywhere
- `MISSING_VARIABLES N041` skt vs SST sull'acqua = 0.005 K (§5, r.139) [SENZA FONTE]
  → #55 [corpo] (measured); #55 [commento 2026-09-29]: the source gives 0.0005 K RMSE, not 0.005 K (the earlier recorded value was 0.0015 K)
- `MISSING_VARIABLES N055` finestra di un'ora di `10fg` giusta = 88 % delle volte (§5, r.162-163) [SENZA FONTE]
  → #49 [corpo] (measured): the source gives the complement: reset missed on "17 (12.3 %)" of 138 transitions; 88 % is not written
- `MISSING_VARIABLES N081` file orario = ~0.8 GB a 13 livelli, ~1.45 GB a 29 livelli (§6, r.234) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: no issue gives file sizes at 13 vs 29 levels (~0.8 / ~1.45 GB)
  → verifica 2 (dati) CONFERMATA_CON_DIFFERENZE — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 modificati negli ultimi 20 min (campagna in corso), tenuti i 184 con esattamente 246 messaggi (header walk di hpc/grib_schema_ok.py), os.path.getsize, unità decimali (misura 2026-09-29): a 13 livelli media 0.737 GB/file (range 0.644-0.774; voce: ~0.8 GB); il valore a 29 livelli (~1.45 GB) è una proiezione, non misurabile sui dati
  → verifica 2 (repo) CONFERMATA_CON_DIFFERENZE — commit f2c93cc (2026-09-17), messaggio: "~767 MB/hour" (l'md arrotonda a ~0.8 GB) e "1.45 GB/hour"; il valore attuale a 13 livelli in CLAUDE.md è ~747 MB
- `MISSING_VARIABLES N082` archivio annuale = 7.0 TB a 13 livelli, 18.1 TB a 29 livelli (§6, r.234-235) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: no issue gives annual archive size at 13 vs 29 levels (7.0 / 18.1 TB)
  → verifica 2 (dati) CONFERMATA_CON_DIFFERENZE — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 modificati negli ultimi 20 min (campagna in corso), tenuti i 184 con esattamente 246 messaggi (header walk di hpc/grib_schema_ok.py), os.path.getsize, unità decimali (misura 2026-09-29): a 13 livelli 6.46 TB/anno (voce: 7.0 TB); il valore a 29 livelli (18.1 TB) è una proiezione, non misurabile
  → verifica 2 (repo) CONFERMATA_CON_DIFFERENZE — commit f2c93cc (2026-09-17), messaggio: "~7.0 TB/year" e "18.1 TB/year" come nella fonte; 18.1 non è coerente con 1.45 GB/ora (calcolo: 1.45 GB × 8760 = 12.7 TB); il valore attuale a 13 livelli in CLAUDE.md è ~6.55 TB/anno
- `CHAPTER_KNOWN_PROPERTIES A020` That change shifts `skt` over snow-covered land by about 0.05 K RMSE [SENZA FONTE] (§Which, r.36-37)
  → #55 [commento 2026-09-29]: la fonte non misura uno spostamento di 0.05 K: 0.05 K è il livello dell'RMSE (0.05766 → 0.05384 K, "6.6 % less skt derivation error"), cioè il cambio vale ~0.004 K
- `CHAPTER_KNOWN_PROPERTIES A132` Emissivity switches to a flat 0.98 under snow [SENZA FONTE] (§2.3, r.218-219)
  → #55 [commento 2026-09-29]; #28 [corpo]: flat 0.98 solo sopra soglia: "it blends below the threshold and goes flat above" (soglia SNOWC 0.015 dal 2026-09-29)
- `CHAPTER_KNOWN_PROPERTIES A134` Over water the derivation is exact [SENZA FONTE] (§2.3, r.220)
  → #55 [corpo]; #57 [corpo]: non "exact" ma "0.0005 K RMSE, bias −0.0002 K, absmax 0.002 K, on ~910 000 points"
- `CHAPTER_KNOWN_PROPERTIES A197` A 31 km model cannot see a gust: the peak happens on scales of metres and seconds it never represents [SENZA FONTE] (§5.1, r.344-345)
  → verifica 1 NON_TROVATA — —: nessuna fonte descrive le scale del gust non risolte a 31 km
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://codes.ecmwf.int/parameter-database/api/v1/param/228029/ ECMWF param-db `i10fg` (update 2022-11-14); ERA5 data documentation ("31km"): "The WMO defines a wind gust as the maximum of the wind averaged over 3 second intervals. This duration is shorter than a model time step, and so the ECMWF Integrated Forecasting System deduces the magnitude of a gust..."; la fonte parla della scala temporale (secondi vs passo), non di "metres"
- `CHAPTER_KNOWN_PROPERTIES A210` ERA5 supplies the boundary conditions (wind, temperature, humidity, pressure); a gust is not among them [SENZA FONTE] (§5.1, r.371-372)
  → verifica 1 NON_TROVATA — —: elenco delle condizioni al contorno non presente nelle fonti
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — https://raw.githubusercontent.com/wrf-model/WPS/v4.1/ungrib/Variable_Tables/Vtable.ECMWF (WPS v4.1): Codici GRIB letti: 129,130,131,132,157,165,166,167,168,172,134,151,235,31,34,141,139,170,183,236,39-42: nessun 49 (10fg) ne' 228029 (i10fg). Differenze: e' la Vtable standard, non quella effettivamente usata da CHAPTER (non verificata); le condizioni al contorno includono anche SST, ghiaccio, neve, suolo
- `CHAPTER_KNOWN_PROPERTIES A211` The gust is an output of the IFS's own boundary-layer post-processing, recomputed and discarded at every step; it never enters the nested model [SENZA FONTE] (§5.1, r.372-374)
  → verifica 1 NON_TROVATA — —: post-processing IFS del gust non descritto nelle fonti
  → verifica 2 (online) CONFERMATA_CON_DIFFERENZE — IFS Cy41r2 Part IV §3.10.4 e §3.11 (routine SPPGUST), p.54; Vtable.ECMWF WPS v4.1: "Parameter Fgust is computed every time step and its maximum since the last post-processing is written out for archiving"; "SPPGUST. This routine computes wind gusts"; il non-ingresso nel modello annidato e' confermato solo per la Vtable standard; "discarded" e' implicito, non dichiarato
- `CHAPTER_KNOWN_PROPERTIES A213` What is published is the one gust-like field the run produced [SENZA FONTE] (§5.1, r.375-376)
  → #50 [corpo]: la fonte dice "It behaves like a gust and is the best proxy available", non "the one gust-like field"
- `CHAPTER_KNOWN_PROPERTIES A254` No graupel column is published separately because ERA5 has no parameter for one [SENZA FONTE] (§6.2, r.461)
  → #47 [corpo; commento 2026-09-29]; #35: il corpo dice "ERA5 has no parameter for one"; il commento corregge: ECMWF definisce 260028 grle e 260001 tcolg, "ERA5 publishes neither"
- `CHAPTER_KNOWN_PROPERTIES A333` Publication rule: a field ships only when the WRF quantity is the ERA5 one [SENZA FONTE] (§8.4, r.624-625)
  → #50 [corpo]; #47 [corpo]: la regola completa è "published only if the WRF quantity is the ERA5 one, or the difference can be stated in one line"
- `CHAPTER_KNOWN_PROPERTIES N004` spostamento `skt` per cambio soglia neve = circa 0.05 K RMSE — over snow-covered land (§Which, r.36-37) [SENZA FONTE]
  → #55 [commento 2026-09-29]: 0.05 K è l'RMSE di derivazione pooled (0.05766 → 0.05384 K), non lo spostamento; il cambio è "6.6 %" (~0.004 K)
- `CHAPTER_KNOWN_PROPERTIES N064` errore di derivazione inverno = un decimo di kelvin ; trenta volte più piccolo del bias fisico — (§2.3, r.223-224) [fonte: #55 per il decimo; rapporto SENZA FONTE]
  → #55 [commento 2026-09-29 07:51]; #57 [commento 2026-09-29]: "thirty times smaller" riferito a 0.115–0.133 K, misurato con la soglia 0.01; docs/audit/f8 riporta 0.084–0.119 K con 0.015

## 3. Non trovate dopo due verifiche (escluse dal report, o \todo{fonte})

- `CHAPTER_VARIABLES A107` Il `dl` di ERA5 fa lo stesso dove il database tace [SENZA FONTE] (§4, r.142)
  → verifica 1 NON_TROVATA — —: No source describes ERA5's `dl` behaviour where the database is silent.
  → verifica 2 (repo) NON_TROVATA — git log -S"where the database is silent" → solo b19d506 (2026-09-18), che introduce la frase senza fonte; grep su docs/audit/, static_ref.py: nessuna fonte nel repo sul comportamento del dl di ERA5 dove il database tace; docs/audit/f7-static-and-surface.md r.160 dà solo il dl di ERA5 sul Mar Nero (1603 m medi, max 2209.8 m), che non riguarda il riempimento di default
- `CHAPTER_VARIABLES N096` celle vegetate su cui la scelta sarebbe stata inventata = 16.2 % (§8.tv, r.387) [SENZA FONTE]
  → —: 16.2 % delle celle vegetate non compare in issue né in docs/audit
- `MISSING_VARIABLES A052` Temperatura superficiale del ghiaccio marino: usare la skin temperature già derivata, ristretta ai punti con concentrazione di ghiaccio > 0 [SENZA FONTE] (§3, r.80)
  → —: nessuna fonte propone skt ristretta al ghiaccio come temperatura del ghiaccio
- `MISSING_VARIABLES A053` Temperatura del ghiaccio marino: confidenza media; è una skin temperature radiativa, coerente con l'emissione longwave del modello, non una temperatura dedicata della superficie del ghiaccio [SENZA FONTE] (§3, r.80)
  → —: —
- `MISSING_VARIABLES A058` Altezza dello strato limite: numero di Richardson bulk sul profilo di temperatura potenziale virtuale; tutti i campi necessari sono presenti [SENZA FONTE] (§3, r.82)
  → —: —
- `MISSING_VARIABLES A062` `10efg`, `10nfg`: la direzione andrebbe assunta uguale al vento medio, a un istante che non coincide col massimo [SENZA FONTE] (§4, r.90)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (conseguenza del metodo CHAPTER, non una definizione pubblicata)
- `MISSING_VARIABLES A066` TKE: una stima da teoria della similarità richiederebbe altezza dello strato limite e flusso di calore superficiale, entrambi mancanti; gli errori si compongono; sembrerebbe plausibile ma non coerente con la simulazione [SENZA FONTE] (§4, r.91)
  → —: —
- `MISSING_VARIABLES N025` soglia concentrazione ghiaccio per temperatura del ghiaccio = > 0 (§3, r.80) [SENZA FONTE]
  → —: #25/#34 mention `SEAICE > 0` only as the ice reclassification of `LANDMASK`, not as a route to a sea-ice surface temperature
- `CHAPTER_KNOWN_PROPERTIES A215` A 3 km model genuinely needs a smaller gust increment than a 31 km one — smaller, but not zero; this archive applies zero [SENZA FONTE] (§5.1, r.380-382)
  → verifica 1 NON_TROVATA — —: l'argomento dell'incremento di gust minore a 3 km non compare (solo zust 1.6–2.1x in #56)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (ragionamento fisico + fatto di progetto "applies zero")

## 4. Non fattuali (raccomandazioni, valutazioni di costo o confidenza, scelte di metodo)

- `MISSING_VARIABLES A054` Temperatura del ghiaccio marino: costo nullo [SENZA FONTE] (§3, r.80)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) NON_FATTUALE — —: stima di costo ("Free")
- `MISSING_VARIABLES A057` Coefficiente di drag senza onde: costo nullo [SENZA FONTE] (§3, r.81)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) NON_FATTUALE — —: stima di costo ("Free")
- `MISSING_VARIABLES A060` Altezza dello strato limite: costo nullo [SENZA FONTE] (§3, r.82)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) NON_FATTUALE — —: stima di costo ("Free")
- `MISSING_VARIABLES A079` Snowmelt: servirebbe la fusione diagnosticata per timestep dentro il modello [SENZA FONTE] (§4, r.97)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) NON_FATTUALE — —: dice cosa servirebbe; il fatto collegato (ACSNOM non monotono) è in docs/audit/exclusions.md r.31-38
- `MISSING_VARIABLES A190` Qualsiasi altra definizione di shear (strati fissi, per livello di pressione, bulk 0-6 km) è una modifica di una riga, da decidere prima della ri-conversione [SENZA FONTE] (§6, r.230-231)
  → verifica 1 NON_TROVATA — —: —
  → verifica 2 (repo) NON_FATTUALE — convert_to_pressure_levels.py r.903-906 (HEAD); wrf_era5_comparison.py r.107-108: stima di sforzo. La definizione attuale è verificata: vwsh = sqrt((u100-U10)^2+(v100-V10)^2)/90.0, "bulk 10-100 m", paramId 260068, scritto a 100 m. Un altro strato fisso cambia solo in r.904-906 (u/v a 100 m vengono da interplevel su [100., 200.], r.897-898); per le definizioni per livello di pressione o 0-6 km servirebbero una nuova interpolazione e nuovi livelli nel registro, quindi più di una riga
- `MISSING_VARIABLES N038` sotto-dominio di verifica CLDFRA = 500 × 600 punti (§5, r.129) [SENZA FONTE]
  → verifica 1 NON_TROVATA — —: the 500 × 600 sub-domain is not in the issues; #21 [corpo] has only "18-22% of cloudy points sit exactly at 1"
  → verifica 2 (dati) NON_FATTUALE — MISSING_VARIABLES.md §5 r.129: 500 × 600 è la dimensione del sotto-dominio scelto per il metodo di verifica di CLDFRA, non una proprietà dei dati; non misurato
- `CHAPTER_KNOWN_PROPERTIES A169` For a hard bound, clip your own reconstruction rather than reading it as an inconsistency [SENZA FONTE] (§3.3, r.284-286)
  → verifica 1 NON_TROVATA — —: nessuna fonte suggerisce di clippare la propria ricostruzione
  → verifica 2 (repo) NON_FATTUALE — —: raccomandazione all'utente ("What to do")

## 5. Non verificabili (metadati dei documenti, fuori dal report)

- `CHAPTER_VARIABLES A004` Documento aggiornato il 2026-09-18, quando il file statico WPS `geo_em.d02` è stato recuperato da LRZ [SENZA FONTE] (§0, r.7-8)
  → #31 corpo; #18 corpo: Document update date. The geo_em recovery is attested ("recoverable, and already recovered — `geo_em.d02`"), but no issue gives the 2026-09-18 date or LRZ as the source.
- `CHAPTER_VARIABLES A008` Nulla è stato rimosso [SENZA FONTE] (§0, r.11)
  → —: Statement about the document/schema history ("nothing was removed"); no issue states it in these terms.
- `CHAPTER_VARIABLES A009` Ogni campo è uno che si può difendere riga per riga [SENZA FONTE] (§0, r.13)
  → —: Editorial claim of the document, not a measurable fact.
- `CHAPTER_VARIABLES A037` Quattro campi non sono esattamente il loro omonimo ERA5, e sono pubblicati dicendolo [SENZA FONTE] (§4, r.69)
  → —: Count of rows in the document's own table of declared approximations.
- `CHAPTER_VARIABLES A059` "Tre altri" meritano una nota invece di un avvertimento [SENZA FONTE] (§4, r.81)
  → —: Structure of the document.
- `CHAPTER_VARIABLES A141` L'archivio è semantica ECMWF ovunque, e così questo messaggio [SENZA FONTE] (§6, r.199)
  → —: Editorial statement of the document.
- `CHAPTER_VARIABLES A145` Descrizioni e unità sono quelle ECMWF; "Time" dice come il campo è campionato [SENZA FONTE] (§7, r.209)
  → —: Description of the document's table columns.
- `CHAPTER_VARIABLES N003` data aggiornamento documento = 2026-09-18 — recupero di `geo_em.d02` (§0, r.7) [SENZA FONTE]
  → —: data di aggiornamento del documento (metadato)
- `CHAPTER_VARIABLES N075` data fino a cui le quattro voci stavano in §6 = 2026-09-17 (§6, r.179) [SENZA FONTE]
  → —: storia della struttura del documento (§6 fino al 2026-09-17)
- `MISSING_VARIABLES A001` Data del documento: 2026-09-17 [SENZA FONTE] (§0, r.3)
  → —: data del documento
- `MISSING_VARIABLES A002` Ambito: la lista di variabili richiesta per la rianalisi regionale CHAPTER (atmosfera, statici, superficie terrestre, onde, ghiaccio marino, oceano superficiale) [SENZA FONTE] (§0, r.3-4)
  → —: ambito del documento
- `MISSING_VARIABLES A003` La nota risponde a quali variabili richieste si possono mettere nell'archivio GRIB, quali ottenere per altra via, quali non sono nei dati [SENZA FONTE] (§0, r.6-8)
  → —: scopo della nota
- `MISSING_VARIABLES A004` Da leggere prima di impegnarsi in una ri-conversione dell'intero archivio [SENZA FONTE] (§0, r.8-9)
  → —: indicazione di lettura
- `MISSING_VARIABLES A045` Le variabili di §3 non sono nell'output del modello ma esiste un modo difendibile per ottenerle [SENZA FONTE] (§3, r.70-71)
  → —: struttura del documento (introduzione a §3)
- `MISSING_VARIABLES A070` Coefficiente di drag con onde: come sopra; il coefficiente senza onde è disponibile (§3) [SENZA FONTE] (§4, r.93)
  → —: rimando interno a §3
- `MISSING_VARIABLES A114` I caveat di §5 contano per l'uso corretto e vanno letti con la lista delle variabili [SENZA FONTE] (§5, r.125)
  → —: indicazione di lettura
- `MISSING_VARIABLES A134` Richiesta: se si preferisce il flag mancante, dirlo ora [SENZA FONTE] (§5, r.152)
  → #54 [commento 2026-09-25]: richiesta ai lettori; già decisa: "Decided — option 1, the bitmap"
- `MISSING_VARIABLES A188` Richiesta: confermare o modificare la lista land-surface [SENZA FONTE] (§6, r.228)
  → #63 [corpo]: richiesta ai lettori; #63: "The question as posed is stale in their favour and should be re-asked"
- `MISSING_VARIABLES A194` Richiesta: dirlo ora se il set più denso conta [SENZA FONTE] (§6, r.235)
  → —: richiesta ai lettori
- `CHAPTER_KNOWN_PROPERTIES A001` Third of the three documents that ship with this archive [SENZA FONTE] (§intro, r.3)
  → #58 [corpo]: metadato del documento ("beside CHAPTER_VARIABLES.md and MISSING_VARIABLES.md")
- `CHAPTER_KNOWN_PROPERTIES A004` This document answers: what is in the files that will surprise you [SENZA FONTE] (§intro, r.5)
  → —: metadato: scopo del documento
- `CHAPTER_KNOWN_PROPERTIES A005` Everything below is a property of the data as delivered [SENZA FONTE] (§intro, r.7)
  → —: metadato: perimetro del documento
- `CHAPTER_KNOWN_PROPERTIES A006` None of it is a defect awaiting repair [SENZA FONTE] (§intro, r.7-8)
  → #49 [commento 2026-09-25]: metadato; nota: #49 chiama la finestra di 10fg "the number is right and the label is wrong", documentata e non riparata
- `CHAPTER_KNOWN_PROPERTIES A009` Every number here was measured, not estimated [SENZA FONTE] (§intro, r.13)
  → —: affermazione generale sul documento
- `CHAPTER_KNOWN_PROPERTIES A012` Each entry links to the issue that holds the measurement and the method [SENZA FONTE] (§intro, r.16-17)
  → —: struttura del documento
- `CHAPTER_KNOWN_PROPERTIES A013` Section 0 is the short list: the things that change what you do, in one line each [SENZA FONTE] (§How, r.21)
  → —: struttura del documento
- `CHAPTER_KNOWN_PROPERTIES A014` Two kinds of entry are mixed together deliberately [SENZA FONTE] (§How, r.24)
  → —: struttura del documento
- `CHAPTER_KNOWN_PROPERTIES A015` Properties of the run: the model was configured a certain way and the data reflect it; nothing can be done after the fact; the run would have to be repeated [SENZA FONTE] (§How, r.27-28)
  → —: categoria redazionale del documento
- `CHAPTER_KNOWN_PROPERTIES A016` Properties of the conversion: a deliberate convention, chosen and documented; could be changed; the entry says what was chosen instead and why [SENZA FONTE] (§How, r.29-30)
  → —: categoria redazionale del documento
- `CHAPTER_KNOWN_PROPERTIES A021` That change is already reflected in the figures in section 4 [SENZA FONTE] (§Which, r.37)
  → —: rimando interno; nota: le cifre skt stanno in §2.3, non in "section 4"
- `CHAPTER_KNOWN_PROPERTIES A340` Document written 2026-09-28, from measurements made 2026-09-18 to 2026-09-25 [SENZA FONTE] (§Where, r.658)
  → #58 [commento 2026-09-28]: metadato (la data di scrittura coincide con "Written and merged" del 2026-09-28)
- `CHAPTER_KNOWN_PROPERTIES N136` periodo delle misure = 2026-09-18 a 2026-09-25 ; documento scritto 2026-09-28 — (§Where, r.658) [SENZA FONTE]
  → —: metadato del documento

## 6. Fuori ambito (richiesta originale di variabili: per il report LAM AI)

- `MISSING_VARIABLES A013` Atmosfera, superficie (24 variabili + wind shear): 22 di 24 consegnate, più wind shear [SENZA FONTE] (§1, r.29)
- `MISSING_VARIABLES A015` Atmosfera, livelli di pressione (9 variabili × 13 livelli): tutte consegnate [SENZA FONTE] (§1, r.30)
- `MISSING_VARIABLES A021` Superficie terrestre: consegnato il sottoinsieme che esiste, con nomi ERA5 [SENZA FONTE] (§1, r.34)
- `MISSING_VARIABLES A181` La proposta originale della lista land-surface è andata persa [SENZA FONTE] (§6, r.219)
- `MISSING_VARIABLES N001` variabili atmosfera superficie richieste = 24 — più wind shear (§1, r.29) [SENZA FONTE]
- `MISSING_VARIABLES N002` variabili atmosfera superficie consegnate = 22 di 24 (§1, r.29) [SENZA FONTE]
- `MISSING_VARIABLES N003` variabili richieste a livelli di pressione = 9 × 13 livelli (§1, r.30) [SENZA FONTE]
- `MISSING_VARIABLES N004` campi ERA5 extra a livelli di pressione = 3 (`cc`, `crwc`, `cswc`) (§1, r.30) [SENZA FONTE]
- `MISSING_VARIABLES N005` livelli di quota richiesti per la TKE = 3 (§1, r.31) [SENZA FONTE]

## 7. Confermate (diventano SUPPORTATE)

- `CHAPTER_VARIABLES A005` → verifica 1 NON_TROVATA — #18 corpo: No source says geo_em was "recorded as lost". #18 says instead the fields "were unlocked by a file nobody had looked for". | verifica 2 (repo) CONFERMATA — commit 0b2a707 (2026-09-17), `git show 0b2a707:MISSING_VARIABLES.md` r.83 e r.182; commit b19d506 (2026-09-18), messaggio: r.83: 
- `CHAPTER_VARIABLES A010` → #17 corpo: "a mapping is published only if the WRF quantity **is** the ERA5 one, or the difference states in one line"
- `CHAPTER_VARIABLES A011` → #17 corpo; docs/audit/exclusions.md: Same publication rule; exclusions re-tested one line each, "Reason holds".
- `CHAPTER_VARIABLES A014` → #12 corpo; #11 corpo: "Run is WRF V4.1.1 / WPS 4.1"; "WRF (d02 only, 3 km Mercator, 1641x1353)"
- `CHAPTER_VARIABLES A015` → #11 corpo; #15 corpo: "WRF (d02 only, 3 km Mercator, 1641x1353)"; "The WRF grid is Mercator"
- `CHAPTER_VARIABLES A020` → verifica 1 NON_TROVATA — —: No issue states one file per hour with a size "measured, not estimated". | verifica 2 (dati) CONFERMATA — python3 su tutti i /leonardo_work/AIFPT_AILAMIT/CHAPTER/grib_v3/*/*/*.grib (280 presenti, tutti 2024-09-01..12), esclusi i 96 mod
- `CHAPTER_VARIABLES A021` → #13 corpo: "`ailam-an-cima-3km-<yyyy>-<yyyy>-1h-v1-<yyyymmdd><hh>.grib`"
- `CHAPTER_VARIABLES A025` → #19 corpo: "The 13 levels are the ERA5 set truncated at the model top: the 8 ERA5 levels above 50 hPa are above WRF's `P_TOP`"
- `CHAPTER_VARIABLES A030` → #23 commento 2026-09-25: "Accumulations: PDT 8, `typeOfStatisticalProcessing` 1, reference 00Z, `0-H`, `lengthOfTimeRange` H."
- `CHAPTER_VARIABLES A031` → #23 commento 2026-09-25; #22 commento: "Exactly zero at 00Z, all six fields, all 16 00Z files: max 0.0, min 0.0"
- `CHAPTER_VARIABLES A032` → #23 commento 2026-09-25: "`10fg`: PDT 8, `typeOfStatisticalProcessing` 2, reference H−1 ..., `0-1`". Note #49: the declared window is wrong on 17 of 138 transit
- `CHAPTER_VARIABLES A033` → #50 corpo; #23 corpo: "It is the maximum of the *resolved* 10 m wind, not a gust parameterisation."
- `CHAPTER_VARIABLES A034` → #15 corpo; #22 corpo: accumulated "reference time = 00Z ... step `0-H`", instantaneous "`dataDate`/`dataTime` = valid time", `10fg` "reference time H-1"
- `CHAPTER_VARIABLES A035` → #22 corpo; #14 commento: "`validityDate`/`validityTime` still resolve to the timestep, so index on validity and never on `dataTime`."
- `CHAPTER_VARIABLES A039` → #37 corpo: "`slor` is published as \|∇z\| of the **resolved** 3 km terrain"
- `CHAPTER_VARIABLES A041` → #37 corpo; #25 commento: "`sdor` **is** the ERA5 quantity, evaluated on a 3 km cell instead of a 31 km one"
- `CHAPTER_VARIABLES A042` → #37 corpo; #25 commento: "the measured ratio of medians is 0.244 = (3/31)^0.605 ... only one of them is a rescaling"
- `CHAPTER_VARIABLES A044` → #26 commento 2026-09-25: "`|τ| = ρu*²` ... the stress is aligned with `U10` ... The alignment is the one thing that is ours"
- `CHAPTER_VARIABLES A045` → #56 corpo: "ERA5's `fsr` is an **effective** roughness that carries the orographic drag IFS parameterises at 31 km."
- `CHAPTER_VARIABLES A047` → #56 corpo: "Over land it runs at 0.32–0.48 of ERA5's in the median"
- `CHAPTER_VARIABLES A048` → #56 corpo: "Over sea the two archives agree: both roughnesses are Charnock"
- `CHAPTER_VARIABLES A049` → #56 corpo + commento 2026-09-29: "`zust` runs **1.6–2.1× ERA5's** over land and 1.1× over sea"
- `CHAPTER_VARIABLES A050` → #56 corpo: "The `zust` excess over land is then the other half of the same story: at 3 km the terrain-driven wind is resolved rather than smoothed"
- `CHAPTER_VARIABLES A051` → #38 corpo; #25 commento: "ERA5 has no soil at all, because its land-sea mask is permanent"; `ci` carries the ice
- `CHAPTER_VARIABLES A053` → #25 commento 2026-09-22: "So `lsm & ~(ci > 0)` recovers ERA5's permanent mask, as `CHAPTER_VARIABLES.md` §4 claims."
- `CHAPTER_VARIABLES A054` → #38 commento 2026-09-25 (resolution): "`lsm`, `al` | unchanged | still the model's own, hour by hour"
- `CHAPTER_VARIABLES A055` → #38 corpo + commento 2026-09-25: "The converter's soil mask correctly follows the **hourly** land mask"; now masked on the permanent land mask
- `CHAPTER_VARIABLES A056` → #38 corpo: "`swvl` reaches **exactly 1.000** ... its porosity ... **0.435**"
- `CHAPTER_VARIABLES A057` → #38 commento 2026-09-25 (commit e70ddb4): "`swvl1-4`, `stl1-4` | geo_em's **permanent** land | sea ice carries no soil column"
- `CHAPTER_VARIABLES A058` → #38 corpo; #27 commento: "`ci` is published so nothing is lost that cannot be recovered"
- `CHAPTER_VARIABLES A062` → #26 corpo/commento; #28 corpo: "with `eps` **measured** from the run rather than looked up"
- `CHAPTER_VARIABLES A063` → #26 corpo: "RRTMG's clear-sky diagnostic shares the all-sky equation's `eps` and `T`"
- `CHAPTER_VARIABLES A065` → #26 corpo: "an identity with no reference temperature and no fit"
- `CHAPTER_VARIABLES A066` → #26 corpo + commento 2026-09-25: "IQR 0.0000 within every land-use category"; re-measured "IQR ~1e-6"
- `CHAPTER_VARIABLES A067` → #26 corpo + commento: "exactly 0.98000 over water"; "Water is **0.98000 with IQR 1.3e-6**, the independent gate"
- `CHAPTER_VARIABLES A068` → #55 corpo + commento 2026-09-29: "replaced by the seasonal pair with the season named"
- `CHAPTER_VARIABLES A069` → #55 corpo: "**99.98 % (July) … 93.05 % (January)**"
- `CHAPTER_VARIABLES A070` → docs/audit/f8-surface-exchange.md (table, l.92): "**0.0012 K in July, 0.084–0.119 K in January and February**, p99 0.81 K, absmax 2.79 K". #55 still carries the
- `CHAPTER_VARIABLES A071` → #55 corpo + commento: "the whole of the difference is the snow rule"
- `CHAPTER_VARIABLES A072` → #55 commento 2026-09-29T08:14: "it blends below the threshold and goes flat above"; "the answer is **0.015**"
- `CHAPTER_VARIABLES A073` → #55 commento 2026-09-29T08:14: "This constant is the one free parameter in the whole `skt` reconstruction"
- `CHAPTER_VARIABLES A077` → #57 corpo: "land **−1.64 K**, reaching **−3.24 K** at midday"; "sea **+0.01 K**"
- `CHAPTER_VARIABLES A078` → #57 corpo: "The land bias is the run."; "The sea number is the control, and it clears the conversion"
- `CHAPTER_VARIABLES A079` → #57 corpo: "**`HFX`, `LH` and the ground heat flux are the three fields this archive does not have**"
- `CHAPTER_VARIABLES A080` → #37 corpo: "`al` is a two-season table value by dominant category ..., not a field"
- `CHAPTER_VARIABLES A083` → #37 corpo: "8 to 11 distinct values over the whole domain"
- `CHAPTER_VARIABLES A084` → #37 corpo + commento 2026-09-29: "**1 171 937 land points**, 89.9 % of the land mask"; "SUMMER applies April to October and WINTER November to March"
- `CHAPTER_VARIABLES A085` → #37 corpo: "Off land it is 0.08 on water and **0.65 on sea ice**"
- `CHAPTER_VARIABLES A086` → #37 commento 2026-09-29: "do not difference it across April or November expecting a signal"
- `CHAPTER_VARIABLES A087` → docs/audit/f7-static-and-surface.md §fal: "the model's own flux ratio `SWUPB/SWDNB` ... carries the zenith-angle dependence of that hour"
- `CHAPTER_VARIABLES A088` → #45 corpo: "a systematic high bias in surface shortwave"
- `CHAPTER_VARIABLES A090` → #45 corpo: "ERA5 carries the Tegen aerosol climatology."
- `CHAPTER_VARIABLES A091` → #45 corpo: "an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about that much"
- `CHAPTER_VARIABLES A092` → #45 corpo + commento 2026-09-29: "**+8.5 % clear-sky and +13.6 % all-sky**" (`ssrdc` 1.085, `ssrd` 1.136)
- `CHAPTER_VARIABLES A093` → #45 corpo: "they agree with ERA5 to 0.4 to 1.1 per cent, which is the control that makes the solar attribution credible"
- `CHAPTER_VARIABLES A094` → #48 corpo: "`tcc` ... **0.783**", "`hcc` ... **0.610**"; "no aerosol *and* too little cloud, both pushing surface solar the same way"
- `CHAPTER_VARIABLES A096` → #44 corpo: "it does not extrapolate at all — it **clamps to the lowest model level**"
- `CHAPTER_VARIABLES A097` → #44 corpo: "`t` ... **max abs diff exactly 0.0**"; "`q` ... 1e-09 max"
- `CHAPTER_VARIABLES A098` → #44 corpo: "a real model state at about 24 to 27 m above ground, not an invention"; "The archive is internally coherent down there."
- `CHAPTER_VARIABLES A099` → #44 corpo: "ERA5 extrapolates below ground with a lapse rate ... exactly where 1000 hPa is underground, which is most of the land"
- `CHAPTER_VARIABLES A100` → #44 corpo: "a median of **+24 to +27 m above** it ... **47.6 per cent of the domain** at 1000 hPa and 9 per cent at 925"
- `CHAPTER_VARIABLES A101` → #44 commento 2026-09-29: "mask the levels against `sp`, and every field required to do it is in the same file"
- `CHAPTER_VARIABLES A103` → verifica 1 NON_TROVATA — —: No source calls `dl` the run's lake-depth database rather than a model state (`LAKE_DEPTH` is listed among the geo_em fields only, # | verifica 2 (dati) CONFERMATA — confronto var_dl di chapter_static_d02.npz con LAKE_DEPTH di geo_em/2022123118/WPS/geo_em.d02.nc; attributi globali di wrfout_d02
- `CHAPTER_VARIABLES A105` → #25 corpo; #38 commento 2026-09-25: "`dl` is masked off-lake"; "`dl` | lake | follows `cl`"
- `CHAPTER_VARIABLES A108` → #54 corpo; #38 commento 2026-09-25: "the archive already writes bitmaps for the soil and ocean fields"; "`sst`, `ci` | the sea | both as a **bitmap**"
- `CHAPTER_VARIABLES A109` → #38 commento 2026-09-25: "`sst` and `ci` both bitmapped ... present exactly on the sea"
- `CHAPTER_VARIABLES A112` → #38 commento 2026-09-25: "`cl` | — | **zero** on the sea, not missing: ERA5's `cl` is defined there and is ~0"
- `CHAPTER_VARIABLES A113` → #54 commento 2026-09-25: "masked exactly where `mucape < 100` | **True**"; "the Fortran's 100 J/kg cut-off"
- `CHAPTER_VARIABLES A115` → #54 corpo + commento: "The archive writes 0, which reads as 'nothing is stopping convection', precisely where the most is."
- `CHAPTER_VARIABLES A117` → docs/audit/f7-static-and-surface.md §fal: "`SWUPB/SWDNB` above 50 W/m² of incoming shortwave ... undefined at night"
- `CHAPTER_VARIABLES A121` → #25 corpo; #63 corpo: "MODIS carries no shrub phenology while code table 4.234 splits evergreen from deciduous"
- `CHAPTER_VARIABLES A122` → #25 commento 2026-09-22: "88 785 lake cells"
- `CHAPTER_VARIABLES A124` → #12 corpo: "`sf_ocean_physics = 0` ... No ocean coupling, hence no waves, currents, SSH or ice thickness."
- `CHAPTER_VARIABLES A127` → #35 corpo + commento: "`LAI` ... is the model's own leaf area index, alive ... in the wrfout and unpublished"
- `CHAPTER_VARIABLES A129` → #17 corpo; docs/audit/exclusions.md: "`OA1-4`/`OL1-4` are Kim-Arakawa asymmetry and effective length, not ECMWF's gradient-covariance eigenstructure. Reason hol
- `CHAPTER_VARIABLES A131` → #24 corpo + commento: "each ERA5 layer is the exact integral of RUC's own piecewise-linear profile"
- `CHAPTER_VARIABLES A132` → #24 corpo + commento: "RUC has 6 nodes at 0/5/20/40/160/300 cm"; `ZS` = "(0, 0.05, 0.20, 0.40, 1.60, 3.00) m"
- `CHAPTER_VARIABLES A133` → #24 commento 2026-09-22: "extrapolation at the bottom | **none**: 2.89 m of ERA5 column inside a 3.00 m deepest node"
- `CHAPTER_VARIABLES A134` → verifica 1 NON_TROVATA — —: No source states that the old objection was to writing point values rather than integrating them. | verifica 2 (repo) CONFERMATA — commit 0b2a707 (2026-09-17), messaggio; commit b19d506 (2026-09-18), messaggio: 0b2a707 elimina il blocco perché "RUC point value
- `CHAPTER_VARIABLES A136` → #12 corpo §h; #25 commento: "The 90.1 % average dominance and the 17.9 % of land cells carrying both high and low vegetation"; #25: "233 844 (17.93 %)"
- `CHAPTER_VARIABLES A138` → #25 corpo; #63 corpo: "MODIS carries no shrub phenology while code table 4.234 splits evergreen from deciduous"
- `CHAPTER_VARIABLES A142` → #18 corpo; #11 corpo: "`cvl`/`cvh`/`tvl`/`tvh`/`slt`/`cl`/`dl` were all considered impossible until they were not"
- `CHAPTER_VARIABLES A143` → #25 corpo + commento; #38 commento: "19309 land cells hold a sub-grid lake that `lsm` does not carry, because `sf_lake_physics=0` recodes class 21 to 17" (count
- `CHAPTER_VARIABLES A229` → #25 corpo + commento: "read once from the `geo_em.d02` sidecar"; "**bitwise identical at all 34 timesteps**"
- `CHAPTER_VARIABLES A230` → #25 corpo + commento: "WRF reclassifies points with `SEAICE>0` as ice: `LANDMASK` 0->1"; "`lsm` moves at 14 timesteps"
- `CHAPTER_VARIABLES A239` → verifica 1 NON_TROVATA — —: No source says `tvl`/`tvh`/`slt` are the only coded fields or that their tables are published. | verifica 2 (repo) CONFERMATA — wrf_era5_comparison.py (WRF_TO_ECMWF_PARAMID, HEAD c5a8253); CHAPTER_VARIABLES.md §8: misura: estratte con grep le unità di tutte
- `CHAPTER_VARIABLES A241` → #59 corpo: "`LU_INDEX` vs `IVGTYP`, lake recode excluded | **1.0000**" (0.9998 at 2025-02-15, all 2735 disagreements on sea ice)
- `CHAPTER_VARIABLES A242` → #25 corpo; #12 corpo: "`sf_lake_physics=0` recodes class 21 to 17"; "WRF recodes lakes to water at init"
- `CHAPTER_VARIABLES A243` → #12 corpo: "Confirms the `cl` reasoning in `CLAUDE.md`: geogrid *did* resolve lakes"
- `CHAPTER_VARIABLES A270` → verifica 1 NON_TROVATA — —: No source says every land point classifies or that type 7 is absent. | verifica 2 (dati) CONFERMATA — np.unique(var_slt) su chapter_static_d02.npz contro var_land_mask e LANDMASK di geo_em.d02 (misura 2026-09-29): 1 304 109 punti d
- `CHAPTER_VARIABLES A271` → #24 corpo; #14 corpo: "RUC has 6 nodes at 0/5/20/40/160/300 cm"; ERA5 layer tops "0 / 7 / 28 / 100" and "289 cm" deepest boundary
- `CHAPTER_VARIABLES A272` → #24 corpo + commento: "nothing is extrapolated"; "2.89 m of ERA5 column inside a 3.00 m deepest node"
- `CHAPTER_VARIABLES A273` → #24 commento 2026-09-22: "the converter's matrix ... row sums exactly 1.0, all four"; "`SOIL_LAYER_WEIGHTS` is a compile-time constant"
- `CHAPTER_VARIABLES A274` → docs/audit/exclusions.md (SH2O row); #11 corpo: "`SH2O` ... ERA5's `swvl1-4` are total soil water; there is no separate liquid fraction"; the layers come from `
- `CHAPTER_VARIABLES N006` → #18 commento 2026-09-22; #12 commento 2026-09-19: "from U, V, QVAPOR, T, P on the 49 model levels"; "present in the wrfout on all 49 mass levels"
- `CHAPTER_VARIABLES N007` → #12 commento 2026-09-19: "`p_top_requested = 5000`: 50 hPa is the model lid, and it is the archive's topmost pressure level"
- `CHAPTER_VARIABLES N008` → #11 corpo: "WRF (d02 only, 3 km Mercator, 1641x1353)"
- `CHAPTER_VARIABLES N009` → #11 corpo: "WRF (d02 only, 3 km Mercator, 1641x1353)"
- `CHAPTER_VARIABLES N010` → #49 corpo; #34 commento 2026-09-25: "A one-hour maximum over 2 220 273 points"; "agree on all 2 220 273 cells"
- `CHAPTER_VARIABLES N012` → verifica 1 NON_TROVATA — —: nessuna fonte cita il parallelo standard 44.671 N (né TRUELAT) | verifica 2 (dati) CONFERMATA — npz meta_truelat1 di /leonardo_work/AIFPT_AILAMIT/CHAPTER/static_v1/chapter_static_d02.npz; attributo TRUELAT1 di geo_em.d02.nc e
- `CHAPTER_VARIABLES N014` → #40 corpo; docs/audit/f3-column-integrals.md (tabella packing): "a value pinned at exactly 100 comes back from 24-bit CCSDS packing"; f3: "grid_ccsds, 24 bits"
- `CHAPTER_VARIABLES N021` → #19 corpo: "the 8 ERA5 levels above 50 hPa are above WRF's `P_TOP` and cannot be produced"
- `CHAPTER_VARIABLES N022` → #20 corpo: "Near-surface state (10 variables, `heightAboveGround`): `10u` `10v` `100u` `100v` `200u` `200v` `2t` `2d` `2r`"
- `CHAPTER_VARIABLES N025` → #37 corpo; #15 corpo: "`sdor` [...] of a 31 km one: the measured ratio of medians is 0.244"; "how 3 km is compared to 31 km"
- `CHAPTER_VARIABLES N026` → #25 commento 2026-09-22; #37 commento 2026-09-29: "`sdor` is the ERA5 quantity at our scale. Ratio of medians 0.244 = (3/31)^0.605"
- `CHAPTER_VARIABLES N027` → #25 commento 2026-09-22; #37 commento 2026-09-29: "Ratio of medians 0.244 = (3/31)^0.605 — a Hurst exponent inside the 0.5–0.7 range"
- `CHAPTER_VARIABLES N028` → #56 corpo (misura); commento 2026-09-29: "`fsr`, land [...] ratio of medians 0.32–0.48"
- `CHAPTER_VARIABLES N029` → #56 commento 2026-09-29 (misura: #56 corpo): "`zust` runs 1.6–2.1× ERA5's over land and 1.1× over sea"; corpo: ratio of means 1.62–2.06 / 1.08–1.12
- `CHAPTER_VARIABLES N030` → #11 corpo; #15 corpo: "ERA5 at 31 km"; "Build the audit harness, and settle how 3 km is compared to 31 km"
- `CHAPTER_VARIABLES N031` → #24 commento 2026-09-22; #38 corpo: "its porosity 0.435; the published value exceeds it by +0.565"; swvl "exactly 1.000"
- `CHAPTER_VARIABLES N032` → #38 commento 2026-09-25: "Resolution — repaired, commit `e70ddb4`" con `swvl1-4`/`stl1-4` su terra permanente; regola decisa "on 2026-09-25"
- `CHAPTER_VARIABLES N033` → #26 commento 2026-09-25 (misura); #26 corpo: "Every category's median matches the table to 1e-7 or better, IQR ~1e-6"; corpo: "IQR 0.0000"
- `CHAPTER_VARIABLES N034` → #26 commento 2026-09-25: "Water is 0.98000 with IQR 1.3e-6, the independent gate"
- `CHAPTER_VARIABLES N035` → #55 corpo e commento 2026-09-29; docs/audit/f8-surface-exchange.md §The water gate...: "99.98 % (July) … 93.05 % (January)"; invariato dopo la soglia 0.015 (f8)
- `CHAPTER_VARIABLES N036` → docs/audit/f8-surface-exchange.md §The water gate is three times better...: "0.0012 K in July, 0.084–0.119 K in January and February"; #55 riporta i valori vecc
- `CHAPTER_VARIABLES N037` → docs/audit/f8-surface-exchange.md §The water gate is three times better...: "p99 0.81 K, absmax 2.79 K" (a 0.015); #55 corpo/commento dà i vecchi "p99 0.85 K, a
- `CHAPTER_VARIABLES N038` → #26 corpo; #28 corpo: "snow switches every category to a flat 0.98"; #55 commento 2026-09-29 precisa: blend sotto soglia, piatta sopra
- `CHAPTER_VARIABLES N042` → #57 commento 2026-09-29; #55 commento 2026-09-29: "the derivation error over land in winter is 0.115–0.133 K, thirty times smaller than the physical bias"
- `CHAPTER_VARIABLES N043` → #57 corpo (misura); #26 commento 2026-09-25: "land −1.64 K, reaching −3.24 K at midday (2024-09-15T12)"
- `CHAPTER_VARIABLES N044` → #57 corpo: "sea +0.01 K | 0.95–0.98"
- `CHAPTER_VARIABLES N045` → #37 corpo; commento 2026-09-29: "category (8 to 11 distinct values)"; "§4 gained the user-facing version: 8 to 11"
- `CHAPTER_VARIABLES N046` → #37 corpo; #25 commento 2026-09-22; #37 commento 2026-09-29: "`al` moves at 1 171 937 land points, 89.9 % of the land mask"
- `CHAPTER_VARIABLES N047` → #37 corpo; #25 commento 2026-09-22: "is 0.08 on water and 0.65 on sea ice, which is WRF's `seaice_albedo_default`"
- `CHAPTER_VARIABLES N049` → #45 corpo: "an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about that much"
- `CHAPTER_VARIABLES N050` → #45 commento 2026-09-29: "+8.5 % clear-sky and +13.6 % all-sky at the surface"
- `CHAPTER_VARIABLES N051` → #45 commento 2026-09-29: "+8.5 % clear-sky and +13.6 % all-sky at the surface"
- `CHAPTER_VARIABLES N052` → #45 corpo; commento 2026-09-29: "the thermal fields agreeing to within 1.1 % as the control"; corpo: "0.4 to 1.1 per cent"
- `CHAPTER_VARIABLES N053` → #48 corpo: "Total cloud cover runs 22 per cent below ERA5" (tcc ratio 0.783)
- `CHAPTER_VARIABLES N054` → #48 corpo: "high cloud 39 per cent below" (hcc ratio 0.610)
- `CHAPTER_VARIABLES N055` → #44 corpo: "`t` against the lowest model level max abs diff exactly 0.0 [...] `q` 1e-09 max"
- `CHAPTER_VARIABLES N056` → #44 corpo; commento 2026-09-29: "The number is a real model state at about 24 to 27 m above ground"
- `CHAPTER_VARIABLES N057` → #44 corpo: "the published `z` at 1000 hPa puts it at a median of +24 to +27 m above it"
- `CHAPTER_VARIABLES N058` → #44 corpo; #19 commento 2026-09-22: "on 47.6 per cent of the domain at 1000 hPa and 9 per cent at 925"
- `CHAPTER_VARIABLES N060` → #25 corpo; docs/audit/f7-static-and-surface.md §cl and dl: "`LAKE_DEPTH` is the 10 m WPS default"; f7: "10 m is the WPS default fill"
- `CHAPTER_VARIABLES N061` → #25 corpo: "`LAKE_DEPTH` is the 10 m WPS default on 99.56% of the domain" (enunciato come claim da verificare, non rimisurato nei commenti)
- `CHAPTER_VARIABLES N062` → verifica 1 CONFERMATA_CON_DIFFERENZE — docs/audit/f7-static-and-surface.md §cl and dl: la fonte dà la frazione, non il conteggio: "89.5 % of its 88 785 cells ca | verifica 2 (dati) CONFERMATA — conteggio su geo_em.d02.nc: celle con LANDUSEF[classe 21 lago] > 0 e, fra queste, LAKE_DEPTH == 10 (misura 2026-09-29): 79 464 su
- `CHAPTER_VARIABLES N067` → #34 commento 2026-09-25 (anche #36, #38): "Component size works, with a factor of seven of slack"
- `CHAPTER_VARIABLES N068` → #54 corpo: "`cape_2d`'s Fortran flags CIN as missing wherever CAPE < 100 J/kg"
- `CHAPTER_VARIABLES N071` → docs/audit/f7-static-and-surface.md §fal: "the model's own flux ratio `SWUPB/SWDNB` above 50 W/m² of incoming shortwave"
- `CHAPTER_VARIABLES N074` → #25 commento 2026-09-22: "Every count `CLAUDE.md` quotes is confirmed exactly: [...] 88 785 lake cells"
- `CHAPTER_VARIABLES N076` → #24 commento 2026-09-22; #12 commento 2026-09-19: "Read at all 34 timesteps: one distinct value, `(0, 0.05, 0.20, 0.40, 1.60, 3.00)` m"
- `CHAPTER_VARIABLES N077` → #24 corpo; commento 2026-09-22: "ERA5's deepest boundary (289 cm)"; "2.89 m of ERA5 column inside a 3.00 m deepest node"
- `CHAPTER_VARIABLES N078` → #12 commento 2026-09-19: "The 90.1 % average dominance [...] which `CLAUDE.md` reports from geo_em" (citato, non rimisurato)
- `CHAPTER_VARIABLES N080` → verifica 1 NON_TROVATA — —: nessuna fonte dice che i tipi di suolo ECMWF sono 7 (solo "the FAO thresholds") | verifica 2 (online) CONFERMATA — https://codes.ecmwf.int/parameter-database/api/v1/param/43/ ECMWF Parameter Database, paramId 43 `slt` (update_date 2024-06-06)
- `CHAPTER_VARIABLES N083` → #25 commento 2026-09-22: "88 785 lake cells, 19 309 on land"
- `CHAPTER_VARIABLES N098` → verifica 1 NON_TROVATA — #25 commento 2026-09-22 (solo il totale): 1 069 456 non trovato; confermato solo il totale "1 304 109 land" | verifica 2 (dati) CONFERMATA — idem: slt=2 (medium): 1 069 456; terra totale 1 304 109 (= meta_land_points e somma LANDMASK geo_em)
- `CHAPTER_VARIABLES N099` → verifica 1 NON_TROVATA — —: 187 378 non compare | verifica 2 (dati) CONFERMATA — idem: slt=1 (coarse): 187 378
- `CHAPTER_VARIABLES N100` → verifica 1 NON_TROVATA — —: 45 450 non compare | verifica 2 (dati) CONFERMATA — idem: slt=4 (fine): 45 450
- `CHAPTER_VARIABLES N101` → verifica 1 NON_TROVATA — —: 1 498 non compare | verifica 2 (dati) CONFERMATA — idem: slt=6 (organic): 1 498
- `CHAPTER_VARIABLES N102` → verifica 1 NON_TROVATA — —: 327 (slt very fine) non compare | verifica 2 (dati) CONFERMATA — idem: slt=5 (very fine): 327
- `MISSING_VARIABLES A009` → #12 [corpo]; #22 [corpo]; #23 [corpo]: "all 19 accumulators in accum_ref.ACCUMULATED_VARS are monotone within a run by configuration, not merely by observation"
- `MISSING_VARIABLES A014` → #17 [commento 2026-09-22]: "`10efg`/`10nfg` | by decision, only a resolved-wind maximum exists | holds"
- `MISSING_VARIABLES A016` → #19 [corpo]: "Both vertical-velocity conventions are published, `w` in Pa/s and `wz` in m/s"
- `MISSING_VARIABLES A017` → #19 [corpo]: "`cc` `ciwc` `clwc` `crwc` `cswc` `q` `r` `t` `u` `v` `w` `wz` `z`"
- `MISSING_VARIABLES A018` → #17 [commento 2026-09-22]: "TKE | not in the run | holds — BL_PBL_PHYSICS = 1, YSU non-local, KM_OPT = 4"
- `MISSING_VARIABLES A019` → #25 [commento 2026-09-22]: "`z` (surface), `sdor`, `slor`" ricalcolati e invarianti; z = HGT × 9.80665 a 2e-4
- `MISSING_VARIABLES A022` → #22, #24, #25, #26, #51 [commenti]: famiglie auditate: radiazione, runoff (sro/ssro/ro), snowc, tsn, al/fal, iews/inss, cvl/cvh verificati
- `MISSING_VARIABLES A023` → #12 [corpo]; #18 [commento]: "No ocean coupling, hence no waves, currents, SSH or ice thickness"
- `MISSING_VARIABLES A026` → #25 [corpo]: `sst` fra i 15 campi della famiglia 7, verificato (costante nelle 24 h)
- `MISSING_VARIABLES A027` → #12 [corpo]: "No ocean coupling, hence no waves, currents, SSH or ice thickness"
- `MISSING_VARIABLES A028` → #12 [corpo]: "TITLE = ' OUTPUT FROM WRF V4.1.1 MODEL'"
- `MISSING_VARIABLES A029` → #11 [corpo]; #46 [corpo]: "WRF (d02 only, 3 km Mercator, 1641x1353)"; "at 49 × 1353 × 1641"
- `MISSING_VARIABLES A035` → #12 [corpo]; docs/audit/inventory-sweep.md: "ocean waves (43 parameters), Stokes drift, Charnock ... SF_OCEAN_PHYSICS = 0, no wave or ocean model"
- `MISSING_VARIABLES A044` → verifica 1 NON_TROVATA — #16 [corpo]: la fonte dice solo che ACSNOW "was already excluded" e "nothing publishable joins the dead list"; nessuna frase generale | verifica 2 (repo) CONFERMATA — misura: caricato wrf_era5_comparison.WRF_TO_ECMWF_PARAMID (HEAD) con python3: 90 chiavi; nessuna delle 16 chiavi morte (ACHFX ACL
- `MISSING_VARIABLES A046` → verifica 1 NON_TROVATA — —: nessuna fonte sullo stato di implementazione delle voci di §3 | verifica 2 (repo) CONFERMATA — misura: shortName del registro (HEAD): nel registro non c'è nessuno dei tre campi di §3 (temperatura della superficie del ghiacci
- `MISSING_VARIABLES A047` → #25 [corpo]; docs/audit/f7-static-and-surface.md §fal: `al` e `fal` pubblicati; fal "the model's own flux ratio SWUPB/SWDNB"
- `MISSING_VARIABLES A048` → #31 [commento 2026-09-19]; #25 [commento]: LANDUSEF "is the source of `cvl`/`cvh`"; "LANDUSEF sums 8.6e-8"
- `MISSING_VARIABLES A050` → #59 [commento]: "`LU_INDEX` vs `IVGTYP`, lake recode excluded | 1.0000" (anche 2025-02: 0.9998)
- `MISSING_VARIABLES A051` → #63 [corpo]: "the geo_em recovery added cvl, cvh, tvl, tvh, slt, cl, dl and the eight soil layers"
- `MISSING_VARIABLES A061` → #50 [corpo]; #17 [commento 2026-09-22]: "10fg is the resolved 10 m wind with a 2 per cent premium, not a gust"
- `MISSING_VARIABLES A067` → #12 [corpo]; docs/audit/inventory-sweep.md: "SF_OCEAN_PHYSICS = 0, no wave or ocean model"
- `MISSING_VARIABLES A072` → verifica 1 NON_TROVATA — —: CMEMS non nominato | verifica 2 (online) CONFERMATA — https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description CMEMS "Global Ocean Physics Reanalysis" (GLO
- `MISSING_VARIABLES A082` → #31 [commento 2026-09-19]: "Resolved: a modified Registry. The fields were never written, and nothing upstream holds them."
- `MISSING_VARIABLES A083` → #29 [commento 2026-09-29]: "ACHFX/ACLHF/ACGRDFLX/NOAHRES are now recorded as dead because they are Noah accumulators in a RUC run" (#16 li attribuiva al Registr
- `MISSING_VARIABLES A086` → #29 [corpo]: "TSK | not written out | correct, and now known to be a Registry decision rather than an accident"
- `MISSING_VARIABLES A087` → docs/audit/f8-surface-exchange.md §skt; #31 [commento]: "the skin temperature is inverted from LWUPB = eps·σT⁴ + (1−eps)·LWDNB"
- `MISSING_VARIABLES A088` → #55 [corpo e commento 2026-09-29]: "water gate, skt vs the model's own SST | 0.0005 K RMSE, ~910 000 points, every timestep"
- `MISSING_VARIABLES A090` → #30 [corpo]: "an hourly sample of T2 is not the same quantity as the model's own within-hour extremum"
- `MISSING_VARIABLES A091` → #30 [commento 2026-09-29]: "and the only route (a re-run)"
- `MISSING_VARIABLES A093` → #29 [corpo]: "YSU does diagnose one. It was not written to the history stream."
- `MISSING_VARIABLES A095` → verifica 1 NON_TROVATA — —: le date 2026-09-17/18 di eliminazione e reintegro non compaiono | verifica 2 (repo) CONFERMATA — commit 0b2a707 (2026-09-17 19:22 +0200); commit b19d506 (2026-09-18 17:59 +0200): 0b2a707: "The soil and categorical-vegetation b
- `MISSING_VARIABLES A096` → #24 [corpo]; docs/audit/f6-soil-and-snow.md: "RUC has 6 nodes at 0/5/20/40/160/300 cm; ERA5's deepest boundary (289 cm)"; "3 (28–100 cm)"
- `MISSING_VARIABLES A098` → #24 [corpo]: "each ERA5 layer is the exact integral of RUC's own piecewise-linear profile"
- `MISSING_VARIABLES A099` → #24 [corpo]: "ERA5's deepest boundary (289 cm) falls inside the deepest node ... nothing is extrapolated"
- `MISSING_VARIABLES A101` → #12 [corpo]; #25 [commento]: "slt is ... derived in static_ref.py from geo_em's CLAYFRAC/SANDFRAC against the FAO thresholds, never from this table"
- `MISSING_VARIABLES A104` → #63 [corpo]: "tvl is masked on 124 672 shrubland cells, because MODIS carries no shrub phenology and ECMWF's table splits evergreen from deciduous"
- `MISSING_VARIABLES A106` → #31 [commento 2026-09-19]; #25 [commento]: LANDUSEF "is the source of cvl/cvh"; "LANDUSEF sums 8.6e-8"
- `MISSING_VARIABLES A107` → #12 [corpo]; #25 [commento 2026-09-22]: "The 90.1 % average dominance and the 17.9 %"; "233 844 (17.93 %) with both vegetation types above 5 %"
- `MISSING_VARIABLES A109` → #17 [commento 2026-09-22]: "the per-class split is still an assumption"
- `MISSING_VARIABLES A110` → #63 [corpo]: "The single field can be delivered under its own name if they want it."
- `MISSING_VARIABLES A111` → #17 [corpo]: "OA1-4/OL1-4 are Kim-Arakawa asymmetry and effective length"
- `MISSING_VARIABLES A117` → #21 [corpo]; #48 [corpo]: "tcc/hcc/mcc/lcc are maximum-random overlaps of CLDFRA"
- `MISSING_VARIABLES A118` → #19 [corpo]: `cc` fra le 13 variabili su livelli di pressione
- `MISSING_VARIABLES A120` → #31 [commento 2026-09-19]; docs/audit/f8-surface-exchange.md: "TSK was not written out, so the skin temperature is inverted from LWUPB"
- `MISSING_VARIABLES A123` → verifica 1 NON_TROVATA — #24 [corpo]: nessun RMSE skt vs livello 0 cm; #24: "The right soil comparison is TSLB[0]" | verifica 2 (dati) CONFERMATA — skt (eccodes) di grib_v3/2024/09/ailam-an-cima-3km-2024-2024-1h-v1-2024090416.grib (validity 20240904 1600) contro TSLB[:,0] (ZS 
- `MISSING_VARIABLES A125` → #37 [corpo]: "slor is published as |∇z| of the resolved 3 km terrain while paramId 163 is defined as the slope of the sub-grid orography"
- `MISSING_VARIABLES A126` → #37 [corpo]; docs/audit/f7-static-and-surface.md: "sdor is the ERA5 quantity, evaluated on a 3 km cell"; "sdor against √VAR_SSO ... 1.5e-5 m"
- `MISSING_VARIABLES A127` → #19 [corpo]; #41 [corpo]: "WRF's Q* are mixing ratios, per kg of dry air; these are specific contents, per kg of moist air"
- `MISSING_VARIABLES A130` → #54 [corpo]: "cape_2d's Fortran flags CIN as missing wherever CAPE < 100 J/kg"
- `MISSING_VARIABLES A135` → docs/audit/f8-surface-exchange.md §mucin: "Most unstable, mixed over 500 m, searched in the lowest 3 km" (dal Fortran rip_cape.f90)
- `MISSING_VARIABLES A136` → #50 [corpo]: "10fg is the resolved 10 m wind with a 2 per cent premium, not a gust"
- `MISSING_VARIABLES A137` → #50 [corpo]: cita MISSING_VARIABLES: "It behaves like a gust and is the best proxy available"
- `MISSING_VARIABLES A138` → #50 [corpo]: "ERA5's is a parameterised gust roughly 1.6 times the mean wind"
- `MISSING_VARIABLES A141` → #50 [corpo e commento 2026-09-29]: "under-predicts by 38 per cent ... not a bias to be corrected downstream; it is a different quantity"
- `MISSING_VARIABLES A144` → #37 [corpo]; #25 [commento]: "lsm ... moves at the sea-ice points and nowhere else, 0 false positives and 0 missed"
- `MISSING_VARIABLES A147` → docs/audit/f8-surface-exchange.md §iews/inss; #26 [commento]: "The stress is ρu*² aligned with the 10 m wind"
- `MISSING_VARIABLES A148` → #26 [commento]: "The alignment is the one thing that is ours ... priced on ERA5 itself: median 0.92–1.10°"
- `MISSING_VARIABLES A152` → docs/audit/f7-static-and-surface.md §fal: "ours is the model's own flux ratio SWUPB/SWDNB"
- `MISSING_VARIABLES A153` → docs/audit/f7-static-and-surface.md §fal; #15 [corpo]: "above 50 W/m² of incoming shortwave ... undefined at night"
- `MISSING_VARIABLES A160` → #51 [corpo]: "UDROFF barely moves within a day ... the published ssro is the accumulation since 00Z"
- `MISSING_VARIABLES A161` → #51 [corpo]: "sro | 1.0 to 4.6; ssro | 0.000 to 0.004; ro | 0.19 to 0.85"
- `MISSING_VARIABLES A162` → #51 [commento 2026-09-29]: "do not close a water budget assuming this archive carries a drainage term"
- `MISSING_VARIABLES A164` → #47 [corpo]: "There is no graupel column in the archive"; tcw costruito con QGRAUP
- `MISSING_VARIABLES A166` → #47 [commento 2026-09-29]: "ECMWF does define 260028 grle and 260001 tcolg but ERA5 publishes neither"
- `MISSING_VARIABLES A167` → #47 [commento 2026-09-29]: "reconstructing tcw from the five published component columns does not reproduce it"
- `MISSING_VARIABLES A168` → #47 [corpo]: "In the domain mean it is 0.4 % of the condensate"
- `MISSING_VARIABLES A169` → #47 [commento 2026-09-29]: "up to 26.5 kg/m² inside a July convective cell, more than the rest of the column" (corpo: 26.46)
- `MISSING_VARIABLES A171` → #52 [corpo]; #33 [commento]: "emit('tirf', RAINNC - SNOWNC - GRAUPELNC) # rain only"
- `MISSING_VARIABLES A172` → #20 [commento]: "the GRIB1 archive wrote it straight through under a paramId defined in K. The converter asks units='K'"
- `MISSING_VARIABLES A173` → verifica 1 NON_TROVATA — —: la correzione +273.15 non è scritta | verifica 2 (online) CONFERMATA — https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf BIPM, The International System of Units (SI Brochure), 9th e
- `MISSING_VARIABLES A174` → #23 [corpo]; #22 [commento]: "same day, same run)) / 1000, exactly zero at 00Z"
- `MISSING_VARIABLES A175` → #15 [corpo]; #22 [corpo]: "reference time = 00Z of the day and step 0-H (PDT 8)"
- `MISSING_VARIABLES A179` → #17 [commento 2026-09-22]: righe 10efg/10nfg e TKE: "holds"
- `MISSING_VARIABLES A183` → #51 [corpo]; #24 [corpo]: sro/ssro/ro pubblicati; "src is the same quantity with a different capacity"
- `MISSING_VARIABLES A184` → #63 [corpo]; #25 [corpo]: "cvl, cvh, tvl, tvh, slt, cl, dl"
- `MISSING_VARIABLES A185` → #56 [corpo]; #26 [commento]; #25 [corpo]: zust, fsr, al, fal, iews/inss nella famiglia 7-8
- `MISSING_VARIABLES A187` → #17 [commento 2026-09-22]; #35 [corpo]: lai_lv/lai_hv "one LAI per cell ... holds"; "ACSNOM is not monotone"
- `MISSING_VARIABLES A189` → #33 [commento 2026-09-21]: "vwsh ... sqrt((100u-10u)² + (100v-10v)²)/90"
- `MISSING_VARIABLES A192` → #19 [commento 2026-09-19]: "p_top_requested = 5000: 50 hPa is the model lid"
- `MISSING_VARIABLES N006` → #12 [commento 2026-09-19]: "Run is WRF V4.1.1 / WPS 4.1"; header "OUTPUT FROM WRF V4.1.1 MODEL"
- `MISSING_VARIABLES N007` → #11 [corpo]: "WRF (d02 only, 3 km Mercator, 1641x1353)"
- `MISSING_VARIABLES N008` → #11 [corpo]: "WRF (d02 only, 3 km Mercator, 1641x1353)"
- `MISSING_VARIABLES N009` → #18 [commento 2026-09-22]; #33 [commento 2026-09-21]: "From the 49 model levels"; #12 [commento 2026-09-19]: "present in the wrfout on all 49 mass levels"
- `MISSING_VARIABLES N019` → #12 [commento 2026-09-19]: "`sf_surface_physics = 3` (RUC), 6 soil nodes at 0/5/20/40/160/300 cm exactly as stated"; also #24 [corpo]
- `MISSING_VARIABLES N020` → docs/audit/f6-soil-and-snow.md §1 The operator: weight table lists ERA5 layers 1 (0–7 cm) to 4 (100–289 cm); #24 [corpo] names `swvl1-4`/`stl1-4`
- `MISSING_VARIABLES N024` → #11 [commento 2026-09-19]: "the archive claims exactly seven: `cvl`, `cvh`, `tvl`, `tvh`, `slt`, `cl`, `dl`, all read from the `geo_em.d02` sidecar"; verified i
- `MISSING_VARIABLES N026` → verifica 1 NON_TROVATA — —: no Cd formula in the issues; #18 [commento 2026-09-22] has `u*/κ · ln(10/z0)` only for the 10 m neutral wind `u10n`/`v10n` | verifica 2 (online) CONFERMATA — https://raw.githubusercontent.com/wrf-model/WRF/v4.1.1/phys/module_sf_sfclayrev.F riga 488: `GZ10OZ0(I)=ALOG((10.+ZNT(I))/ZNT(I
- `MISSING_VARIABLES N029` → #12 [commento 2026-09-19]; #29 [corpo]: "`isfflx = 1` — the surface fluxes exist, they are just not written"
- `MISSING_VARIABLES N030` → #55 [corpo] (measured); #55 [commento 2026-09-29]: "water gate, `skt` vs SST ... 0.0005 K RMSE, bias −0.0002 K ... on ~910 000 points, every timestep" (corrects
- `MISSING_VARIABLES N031` → #12 [commento 2026-09-19]; #30 [corpo]: "`output_diagnostics = 0` — no min/max screen-level fields, so no `mx2t`/`mn2t`"
- `MISSING_VARIABLES N032` → #12 [commento 2026-09-19] §e: "`nwp_diagnostics = 1` — seven fields are per-hour maxima, by configuration"; #49 [corpo] later says the one-hour window fails on 
- `MISSING_VARIABLES N033` → verifica 1 NON_TROVATA — —: no issue dates the removal (2026-09-17) and reinstatement (2026-09-18) of the soil/type/cover fields | verifica 2 (repo) CONFERMATA — commit 0b2a707 (2026-09-17); commit b19d506 (2026-09-18): eliminazione 2026-09-17 19:22 +0200; reintegro 2026-09-18 17:59 +0200
- `MISSING_VARIABLES N034` → docs/audit/f6-soil-and-snow.md §1 The operator: layers "1 (0–7 cm)", "2 (7–28 cm)", "3 (28–100 cm)", "4 (100–289 cm)"; #24 [corpo]: "ERA5's deepest boundary (28
- `MISSING_VARIABLES N035` → verifica 1 NON_TROVATA — —: the issues and docs/audit cite the FAO thresholds for `slt` but never the number of ECMWF soil types | verifica 2 (online) CONFERMATA — https://codes.ecmwf.int/parameter-database/api/v1/param/43/ ECMWF param-db `slt`: "The seven soil types are: ..." (1-7)
- `MISSING_VARIABLES N036` → #25 [commento 2026-09-22] (measured); #12 [commento 2026-09-19]: "233 844 (17.93 %) with both vegetation types above 5 %"
- `MISSING_VARIABLES N037` → #12 [commento 2026-09-19]: "The 90.1 % average dominance ... which `CLAUDE.md` reports from geo_em" (reported, not re-measured there)
- `MISSING_VARIABLES N042` → verifica 1 NON_TROVATA — —: no issue gives a `skt` vs 0 cm soil RMSE; #24 [commento 2026-09-22] only says `stl1` is not `TSLB[0]` | verifica 2 (dati) CONFERMATA — idem: skt vs TSLB 0 cm, terra senza neve: RMSE 0.026 K (< 1 K)
- `MISSING_VARIABLES N045` → #54 [corpo]: "`cape_2d`'s Fortran flags CIN as missing wherever CAPE < 100 J/kg. `dense()` writes zero there"
- `MISSING_VARIABLES N047` → #26 [commento 2026-09-25]: "ours a 500 m mixed parcel in the lowest 3 km"
- `MISSING_VARIABLES N048` → #50 [corpo]: "ERA5's is a parameterised gust roughly 1.6 times the mean wind"
- `MISSING_VARIABLES N053` → #50 [commento 2026-09-29]; #23 [commento 2026-09-25] (measured): "the hourly maximum adds half a per cent to three per cent"; #23: "by only 0.5 to 3.2 per cent"
- `MISSING_VARIABLES N054` → #50 [corpo]; #50 [commento 2026-09-29]: "reading it as a gust under-predicts by about 38 %"; measured ratio 0.625 of ERA5's `10fg`
- `MISSING_VARIABLES N057` → docs/audit/f7-static-and-surface.md § `fal`: "the model's own flux ratio `SWUPB/SWDNB` above 50 W/m² of incoming shortwave"
- `MISSING_VARIABLES N064` → #51 [corpo]; #23 [commento 2026-09-25]: `sro` ours / ERA5 "1.0 to 4.6"
- `MISSING_VARIABLES N065` → #51 [corpo]; #23 [commento 2026-09-25]: `ssro` ours / ERA5 "0.000 to 0.004"
- `MISSING_VARIABLES N066` → #51 [corpo]; #23 [commento 2026-09-25]: `ro` ours / ERA5 "0.19 to 0.85"
- `MISSING_VARIABLES N067` → #47 [corpo]; #47 [commento 2026-09-29]: "ECMWF defines paramId 136 `tcw` ... five species. The converter builds it from six"
- `MISSING_VARIABLES N068` → #35 [commento 2026-09-29]; #17 [commento 2026-09-22]: "`QGRAUP` (260028 `grle`, 260001 `tcolg`)"; "ERA5 does not publish them"
- `MISSING_VARIABLES N069` → #47 [corpo]; #47 [commento 2026-09-29]: "In the domain mean it is 0.4 % of the condensate and invisible"
- `MISSING_VARIABLES N070` → #47 [commento 2026-09-29]; #21 [commento 2026-09-22]: "up to 26.5 kg/m² inside a July convective cell" (#47's title rounds to 26 kg/m2)
- `MISSING_VARIABLES N071` → verifica 1 NON_TROVATA — —: issues say GRIB1 wrote `2d` in degC under a K paramId (#15, #20) but never state the +273.15 correction | verifica 2 (online) CONFERMATA — come A173: +273.15 da °C a K
- `MISSING_VARIABLES N072` → verifica 1 NON_TROVATA — —: no issue gives the current geolocation error (~2 m) | verifica 2 (dati) CONFERMATA — lat/lon da eccodes (codes_get_array latitudes/longitudes) del primo messaggio di grib_v3/2024/09/ailam-an-cima-3km-2024-2024-1h-v
- `MISSING_VARIABLES N073` → #26 [commento 2026-09-25]: "`shapeOfTheEarth = 1` with `radius = 6370000` on all 246 messages"
- `MISSING_VARIABLES N074` → #26 [corpo]: "without it eccodes derives a grid off by ~1.1 km at the northern edge" (stated in the ticket, not re-measured)
- `MISSING_VARIABLES N075` → verifica 1 NON_TROVATA — —: issues mention "the geo_em recovery" (#03, #11, #18) but never date it | verifica 2 (repo) CONFERMATA — commit b19d506 (2026-09-18 17:59 +0200), messaggio: "geo_em.d02 arrived from LRZ"
- `MISSING_VARIABLES N076` → #24 [corpo]: "`swvl1-4` / `stl1-4` are integrals, not relabellings"
- `MISSING_VARIABLES N077` → #20 [commento 2026-09-22]: "`sqrt((100u−10u)² + (100v−10v)²)/90` ... The 10–100 m layer is ours"
- `MISSING_VARIABLES N078` → #19 [corpo]; #12 [commento 2026-09-19]: "The registry writes 13 pressure levels with 50 hPa at the top"
- `MISSING_VARIABLES N079` → verifica 1 NON_TROVATA — —: 37 and 29 appear nowhere; #19 [corpo] says only "the 8 ERA5 levels above 50 hPa are above WRF's `P_TOP`" | verifica 2 (online) CONFERMATA — https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation (last modified 2026-09-08): Lista: "1000/975/950/925/900/87
- `MISSING_VARIABLES N080` → #12 [commento 2026-09-19]; #19 [commento 2026-09-19]: "50 hPa is exactly the model" lid; "`p_top_requested = 5000`: 50 hPa is the model lid"
- `CHAPTER_KNOWN_PROPERTIES A007` → #58 [corpo; commento 2026-09-28]: "Not a place for the repaired defects. A defect fixed before the rebuild does not belong in a document about the archive that 
- `CHAPTER_KNOWN_PROPERTIES A008` → #58 [corpo]: "The other kind says the archive is correct and surprising ... a user who does not know will misread the field."
- `CHAPTER_KNOWN_PROPERTIES A011` → #15 [corpo]; #48 [corpo]: "Upscale WRF to ERA5, area-weighted"; "Sample means over the 34 audit timesteps, upscaled to the ERA5 grid"
- `CHAPTER_KNOWN_PROPERTIES A017` → #53 [corpo]; #59 [corpo]: "Counted over a whole grib_v3 file ... All 246."; la data "from 2026-09-29 onward" è metadato
- `CHAPTER_KNOWN_PROPERTIES A018` → #59 [corpo]: "The repairs that block — all done, 2026-09-25"; "the other six are merged and verified"
- `CHAPTER_KNOWN_PROPERTIES A019` → #55 [commento 2026-09-29]; #59 [commento 2026-09-29]: "EMISS_SNOWC_FULL 0.01 → 0.015 ... This changes the published skt in every file."
- `CHAPTER_KNOWN_PROPERTIES A023` → #58 [commento 2026-09-28]: "files written before 2026-09-25 carry six repaired defects and should be replaced rather than reconciled"
- `CHAPTER_KNOWN_PROPERTIES A024` → #58 [commento 2026-09-28]: "should be replaced rather than reconciled"
- `CHAPTER_KNOWN_PROPERTIES A044` → #45 [commento 2026-09-25]; #57 [corpo]: "a reader given the radiation findings alone would predict a warm land surface and be wrong"
- `CHAPTER_KNOWN_PROPERTIES A045` → #12 [corpo §o]; #45 [corpo]: "RRTMG ran with a CAM ozone climatology and no aerosol at all"
- `CHAPTER_KNOWN_PROPERTIES A047` → #45 [corpo]: "ERA5 carries the Tegen aerosol climatology."
- `CHAPTER_KNOWN_PROPERTIES A048` → #45 [corpo]; #22: "an aerosol optical depth of 0.1 to 0.2 attenuates the direct beam by about that much, which is the right order for the 8.5 per cent"
- `CHAPTER_KNOWN_PROPERTIES A056` → #45 [corpo]: "ssrdc surface solar down, clear sky ... the atmosphere alone, no clouds"
- `CHAPTER_KNOWN_PROPERTIES A057` → #45 [corpo]: "The thermal fields are untouched by it"
- `CHAPTER_KNOWN_PROPERTIES A059` → #45 [corpo]: "which is the control that makes the solar attribution credible rather than a guess"
- `CHAPTER_KNOWN_PROPERTIES A061` → #45 [corpo]: "It is a property of the run, not of the conversion, and it cannot be removed after the fact."
- `CHAPTER_KNOWN_PROPERTIES A070` → #48 [corpo]: "the converter uses maximum-random"
- `CHAPTER_KNOWN_PROPERTIES A071` → #48 [corpo]: "ECMWF's is exponential-random ... which yields more cover for the same layer fractions. Right direction, wrong size."
- `CHAPTER_KNOWN_PROPERTIES A072` → #48 [corpo]: "Random overlap is the most total cover any assumption can extract from a given profile."
- `CHAPTER_KNOWN_PROPERTIES A074` → #48 [corpo]: "because CLDFRA is strongly bimodal (of 108.79 M cells ... 98.18 M below 0.09 and 5.59 M above 0.91)"
- `CHAPTER_KNOWN_PROPERTIES A079` → #48 [corpo]: "The condensate is there; the fraction the scheme assigns to it is not."
- `CHAPTER_KNOWN_PROPERTIES A080` → #48 [corpo]: "Part of the gap is resolution, not error."
- `CHAPTER_KNOWN_PROPERTIES A081` → #48 [corpo]: "Our tcc is overlapped at 3 km and then averaged to 31 km"
- `CHAPTER_KNOWN_PROPERTIES A082` → #48 [corpo]: "ERA5's is overlapped on an already-smooth 31 km profile, which yields somewhat more cover"
- `CHAPTER_KNOWN_PROPERTIES A084` → #48 [corpo; commento 2026-09-29]: "it is real and the number should not be quoted as if it were all model error"
- `CHAPTER_KNOWN_PROPERTIES A086` → #57 [corpo]: "Two other findings from this audit say the opposite" (#45, #48)
- `CHAPTER_KNOWN_PROPERTIES A090` → #57 [corpo]: "The sea number is the control, and it clears the conversion"
- `CHAPTER_KNOWN_PROPERTIES A091` → #57 [corpo]: "Over open water the model's skin temperature is the SST"
- `CHAPTER_KNOWN_PROPERTIES A092` → #57 [corpo]: "both reanalyses see nearly the same one"
- `CHAPTER_KNOWN_PROPERTIES A094` → #57 [corpo]: "More shortwave reaching the ground and less cloud overhead both put energy into the land surface, and the surface is colder"
- `CHAPTER_KNOWN_PROPERTIES A096` → #57 [corpo]: "That is not a contradiction in the measurements; it is an unexplained partition."
- `CHAPTER_KNOWN_PROPERTIES A097` → #57 [corpo]: "Reconciling it needs the surface energy budget"
- `CHAPTER_KNOWN_PROPERTIES A099` → #57 [corpo]; #45 [commento 2026-09-25]: "The partition cannot be resolved from this archive: HFX, LH and the ground heat flux are exactly what it does not carry
- `CHAPTER_KNOWN_PROPERTIES A100` → #57 [corpo]: "RUC partitioning more of the available energy into latent heat, a different soil-moisture climate, the resolved 3 km orography ..., or a genuine c
- `CHAPTER_KNOWN_PROPERTIES A105` → #56 [corpo]: "ERA5's fsr is an effective roughness that carries the orographic drag IFS parameterises at 31 km."
- `CHAPTER_KNOWN_PROPERTIES A106` → #56 [corpo; commento 2026-09-29]: "fsr is WRF's local ZNT"
- `CHAPTER_KNOWN_PROPERTIES A107` → #56 [corpo]: "WRF's ZNT is the local surface roughness of the land-use class"
- `CHAPTER_KNOWN_PROPERTIES A108` → #56 [corpo]: "the orography is resolved at 3 km instead of parameterised"
- `CHAPTER_KNOWN_PROPERTIES A109` → #56 [corpo]: "Over sea the two archives agree: both roughnesses are Charnock"
- `CHAPTER_KNOWN_PROPERTIES A113` → #56 [corpo]: "Nothing is capped, clipped or mis-scaled; leg B is exact against ZNT to 3e-8."
- `CHAPTER_KNOWN_PROPERTIES A115` → #56 [corpo]: "one who computes a drag coefficient from our fsr and compares it against ERA5's will find a discrepancy that is not there"
- `CHAPTER_KNOWN_PROPERTIES A119` → #56 [corpo]: "at 3 km the terrain-driven wind is resolved rather than smoothed, and the friction velocity responds to it"
- `CHAPTER_KNOWN_PROPERTIES A123` → #29 [corpo]: "TSK | not written out | correct, and now known to be a Registry decision rather than an accident"
- `CHAPTER_KNOWN_PROPERTIES A126` → #55 [corpo]: "The skt derivation is confirmed, and this issue is not about it being wrong."
- `CHAPTER_KNOWN_PROPERTIES A133` → #55 [corpo; commento 2026-09-29]: "The switch does fire early, as this issue said — by half of what it estimated."
- `CHAPTER_KNOWN_PROPERTIES A137` → #55 [commento 2026-09-29]; #57 [commento 2026-09-29]: "this derivation error is thirty times smaller than the physical cold bias of the land skin itself"
- `CHAPTER_KNOWN_PROPERTIES A138` → #58 [corpo]: "this is the single most likely misreading of the archive and needs the plainest sentence in the document"
- `CHAPTER_KNOWN_PROPERTIES A142` → #40 [commento 2026-09-22 13:56]: "The two conventions, and both are right ... Not an inconsistency"
- `CHAPTER_KNOWN_PROPERTIES A145` → #40 [commento 2026-09-22 13:07]: "Cy41r2 because that is the cycle ERA5 was produced with"
- `CHAPTER_KNOWN_PROPERTIES A146` → #40 [commento 2026-09-25 15:13]; #59 [corpo]: "r is now ECMWF's paramId 157"; ratio vs ERA5 "0.505 → 0.945 at 100 hPa"
- `CHAPTER_KNOWN_PROPERTIES A149` → #40 [commento 2026-09-22 13:56]: "ERA5 publishes no 2 m relative humidity at all"
- `CHAPTER_KNOWN_PROPERTIES A150` → #40 [commento 2026-09-25 15:02]: "that is the WMO convention for a screen-level humidity"
- `CHAPTER_KNOWN_PROPERTIES A152` → #58 [commento 2026-09-28]: "recompute from q, t and sp if you need them on one convention, all three being published"
- `CHAPTER_KNOWN_PROPERTIES A154` → #58 [corpo]; #40 [corpo]: "the clip is gone because supersaturation is physical and the model produces it"; "ERA5 publishes r above 100"
- `CHAPTER_KNOWN_PROPERTIES A165` → #42 [commento 2026-09-25]: "Clipping 2d to 2t removes the crossings and leaves the same 0.0133 K everywhere else"
- `CHAPTER_KNOWN_PROPERTIES A166` → #42 [commento 2026-09-25]: "with a kink in the field at exactly RH 100"
- `CHAPTER_KNOWN_PROPERTIES A175` → #44 [corpo]: "it is reading the near-surface air instead, which is a far more defensible thing to publish"
- `CHAPTER_KNOWN_PROPERTIES A181` → #44 [corpo]: "Both messages are in the same file."
- `CHAPTER_KNOWN_PROPERTIES A183` → #44 [corpo]: "ERA5 extrapolates below ground with a lapse rate."
- `CHAPTER_KNOWN_PROPERTIES A184` → #44 [corpo]: "the two archives differ in convention exactly where 1000 hPa is underground, which is most of the land"
- `CHAPTER_KNOWN_PROPERTIES A188` → #44 [commento 2026-09-29]: "mask the levels against sp, and every field required to do it is in the same file"
- `CHAPTER_KNOWN_PROPERTIES A194` → #39 [commento 2026-09-25 14:25]: "The two cannot both be honoured ... There is no third position where both hold"
- `CHAPTER_KNOWN_PROPERTIES A198` → verifica 1 NON_TROVATA — —: la formula del gust ERA5 (turbolenza, downdraught) non compare; #50 dice solo "parameterised gust" | verifica 2 (online) CONFERMATA — IFS Documentation Cy41r2 Part IV (Operational implementation 8 March 2016), §3.10.4 "Wind gusts", eq. 3.97-3.99, pp.53-54, http
- `CHAPTER_KNOWN_PROPERTIES A199` → verifica 1 NON_TROVATA — #50 [corpo]: solo "ERA5's is a parameterised gust"; non la caratterizzazione come stima di ciò che non risolve | verifica 2 (online) CONFERMATA — param-db 228029 `i10fg`; param-db 49 `10fg`; IFS Cy41r2 Part IV §3.10.4: i10fg: "the ECMWF Integrated Forecasting System deduce
- `CHAPTER_KNOWN_PROPERTIES A200` → #50 [corpo]; #23: "maximum of the resolved 10 m wind speed over the output hour ... not produced by a gust scheme"
- `CHAPTER_KNOWN_PROPERTIES A207` → #50 [corpo]: "ERA5's is a parameterised gust roughly 1.6 times the mean wind"
- `CHAPTER_KNOWN_PROPERTIES A209` → #50 [commento 2026-09-29]; #59 [commento 2026-09-28]: "a downscaling inherits the flow, not the diagnostics"
- `CHAPTER_KNOWN_PROPERTIES A212` → verifica 1 NON_TROVATA — —: nessuna fonte afferma esplicitamente che la run non scrisse un proprio gust diagnostic | verifica 2 (dati) CONFERMATA — elenco delle 200 variabili di wrfout_d02_2024-09-04_16:00:00 filtrato con /GUST|WSPD|FG|MAX|WIND|SPD/i (misura 2026-09-29): nessu
- `CHAPTER_KNOWN_PROPERTIES A217` → #50 [corpo; commento 2026-09-29]: "not a bias to be corrected downstream; it is a different quantity"
- `CHAPTER_KNOWN_PROPERTIES A219` → #59 [commento 2026-09-28 15:40]; #50 [corpo]: "ERA5's window is also one hour, so the window length is not the difference"
- `CHAPTER_KNOWN_PROPERTIES A221` → #49 [corpo]: "stepType = max, stepRange = 0-1 ... reference time H−1 ... all of which was verified correct"
- `CHAPTER_KNOWN_PROPERTIES A222` → #49 [corpo]; #60 [corpo]: "WSPD10MAX was not reset at the history write"
- `CHAPTER_KNOWN_PROPERTIES A228` → #49 [corpo]: "this makes the affected hours closer to ERA5's gust (#50) for the wrong reason ... the error is not detectable from the value"
- `CHAPTER_KNOWN_PROPERTIES A230` → #49 [commento 2026-09-25 16:18]: "The previous hour's wrfout is not on disk when the convert runs."
- `CHAPTER_KNOWN_PROPERTIES A231` → #49 [commento 2026-09-25 16:18]: "All seven nwp_diagnostics maxima reset on the same alarm ... none can witness for another."
- `CHAPTER_KNOWN_PROPERTIES A232` → #49 [corpo]: "The census correlates with timestep variability"
- `CHAPTER_KNOWN_PROPERTIES A233` → #49 [corpo]: "Establishing the mechanism ... has not been done."
- `CHAPTER_KNOWN_PROPERTIES A252` → #47 [corpo]: "the sum of water vapour, liquid water, cloud ice, rain and snow — five species"
- `CHAPTER_KNOWN_PROPERTIES A262` → #47 [corpo]: "Drop graupel from tcw, making it ECMWF's definition exactly and the closure identity hold, at the cost of the graupel mass leaving the archive"
- `CHAPTER_KNOWN_PROPERTIES A265` → #36 [commento 2026-09-25 15:41]; #54 [corpo]: "both as a bitmap"; "A masked field teaches unknown here" (cl resta zero sul mare, non mascherato)
- `CHAPTER_KNOWN_PROPERTIES A269` → #25 [corpo]; #63 [corpo]: "tvl is masked on 124 672 shrubland cells, because MODIS carries no shrub phenology"; "rather have a guess than a gap"
- `CHAPTER_KNOWN_PROPERTIES A270` → #25 [corpo]; #03: "slt is NaN off geo_em's permanent land mask"
- `CHAPTER_KNOWN_PROPERTIES A272` → #36 [commento 2026-09-25 15:41]: "'Water, minus the cells geo_em calls lake' is circular: the defect is that geo_em calls the Black Sea a lake."
- `CHAPTER_KNOWN_PROPERTIES A273` → #36 [corpo]: "The Sea of Azov (4702 cells) and part of the Baltic (3013 cells) ... Together they are 89 % of the 55 881 cells the archive calls fully lake"
- `CHAPTER_KNOWN_PROPERTIES A274` → #36 [commento 2026-09-25 15:41]: la cura per classe lago è "circular" perché geo_em chiama lago il Mar Nero
- `CHAPTER_KNOWN_PROPERTIES A275` → #36 [commento 2026-09-25 15:41]: "Component size works, with a factor of seven of slack"
- `CHAPTER_KNOWN_PROPERTIES A276` → #36 [commento 2026-09-25 15:41]: "844 431 ... 49 841 Black Sea + Sea of Azov ... 8 583 Red Sea ... 1 225 Vänern, the largest inland lake"
- `CHAPTER_KNOWN_PROPERTIES A277` → #36 [commento 2026-09-25 15:41]: "Nothing lies between 1 225 and 8 583 ... factor of seven of slack"
- `CHAPTER_KNOWN_PROPERTIES A281` → #38 [commento 2026-09-25 12:25]: "The values discarded are the model's own, but 1.000 ... is an artefact of the hourly reclassification, not a measurement"
- `CHAPTER_KNOWN_PROPERTIES A282` → #38 [corpo]: "where ERA5 has no soil at all, because its land-sea mask is permanent"
- `CHAPTER_KNOWN_PROPERTIES A283` → #38 [corpo]: "ci is published so nothing is lost that cannot be recovered"
- `CHAPTER_KNOWN_PROPERTIES A285` → #38 [corpo]: "When a water cell carries sea ice, WRF makes it land (LANDMASK 0→1)"
- `CHAPTER_KNOWN_PROPERTIES A289` → #54 [corpo]: "The archive writes 0, which reads as 'nothing is stopping convection', precisely where the most is."
- `CHAPTER_KNOWN_PROPERTIES A290` → #54 [corpo]: "A column with no CAPE is normally a column with a great deal of inhibition — that is usually why there is no CAPE."
- `CHAPTER_KNOWN_PROPERTIES A300` → #54 [corpo]: "our CIN exists only in columns with CAPE ≥ 100, i.e. the least inhibited ones, while ERA5 reports it more widely"
- `CHAPTER_KNOWN_PROPERTIES A301` → #54 [corpo]: "a model trained on it learns that low-CAPE situations have zero convective inhibition, which is the inverse of the physics"
- `CHAPTER_KNOWN_PROPERTIES A322` → #37 [corpo]: "paramId 163 is defined as the slope of the sub-grid orography"
- `CHAPTER_KNOWN_PROPERTIES A323` → #37 [corpo; commento 2026-09-29]: "eccodes shows the parameter's own name, Slope of sub-gridscale orography, so a user reading the message sees nothing"
- `CHAPTER_KNOWN_PROPERTIES A332` → #35 [corpo]: "The exclusions stand either way."
- `CHAPTER_KNOWN_PROPERTIES A337` → #17 [corpo]; #12 [corpo]: "one LAI per cell, ERA5 wants one per class"
- `CHAPTER_KNOWN_PROPERTIES N002` → #53 [corpo]: "All 246."
- `CHAPTER_KNOWN_PROPERTIES N003` → #59 [corpo]: "the other six are merged and verified"
- `CHAPTER_KNOWN_PROPERTIES N025` → #56 [corpo]; #48 [corpo]: "IFS parameterises at 31 km ... resolved at 3 km"
- `CHAPTER_KNOWN_PROPERTIES N026` → #45 [corpo]: "an aerosol optical depth of 0.1 to 0.2"
- `CHAPTER_KNOWN_PROPERTIES N063` → #28 [corpo]; #55 [commento 2026-09-29]: "flat 0.98"; "goes flat above" la soglia
- `CHAPTER_KNOWN_PROPERTIES N065` → #40 [commento 2026-09-25 15:02]: "2r is paramId 260242, not 157"
- `CHAPTER_KNOWN_PROPERTIES N089` → #50 [corpo]: "Published under paramId 49, 10fg is the 10 m wind speed with a two-per-cent premium"
- `CHAPTER_KNOWN_PROPERTIES N090` → #50 [corpo]: "a parameterised gust roughly 1.6 times the mean wind"
- `CHAPTER_KNOWN_PROPERTIES N099` → #49 [commento 2026-09-25 16:18]; #60 [corpo]: "All seven nwp_diagnostics maxima reset on the same alarm"
- `CHAPTER_KNOWN_PROPERTIES N112` → #47 [corpo]: "ECMWF defines paramId 136 tcw"
- `CHAPTER_KNOWN_PROPERTIES N119` → #36 [corpo]: "LANDUSEF fraction of MODIS class 21 ... Together they are 89 % of the 55 881 cells the archive calls fully lake"
- `CHAPTER_KNOWN_PROPERTIES N120` → #36 [commento 2026-09-25 15:41]: "844 431 | Atlantic + Mediterranean + Baltic + North Sea ... 49 841 ... 8 583 ... 1 225"
- `CHAPTER_KNOWN_PROPERTIES N121` → #36 [commento 2026-09-25 15:41]: "Component size works, with a factor of seven of slack"
- `CHAPTER_KNOWN_PROPERTIES N133` → #37 [corpo]: "paramId 163 is defined as the slope of the sub-grid orography"

## 8. Riferimenti bibliografici (tutti, come compaiono)

### CHAPTER_VARIABLES.md (18 voci)

- CHAPTER_VARIABLES.md R001 `wrf_era5_comparison.WRF_TO_ECMWF_PARAMID` (§0, r.4)
- CHAPTER_VARIABLES.md R002 [`MISSING_VARIABLES.md`](MISSING_VARIABLES.md) (§0, r.19)
- CHAPTER_VARIABLES.md R003 [`CHAPTER_KNOWN_PROPERTIES.md`](CHAPTER_KNOWN_PROPERTIES.md) (§0, r.20)
- CHAPTER_VARIABLES.md R004 WRF 4.1.1 (§1, r.29)
- CHAPTER_VARIABLES.md R005 scan `mmlsattr` of the whole of 2025 on the source (2026-09-29) (§1, r.38)
- CHAPTER_VARIABLES.md R006 "their ECMWF definitions" (§3, r.56)
- CHAPTER_VARIABLES.md R007 eccodes (§4, r.73; §6, r.198)
- CHAPTER_VARIABLES.md R008 IFS (§4, r.76)
- CHAPTER_VARIABLES.md R009 RRTMG (§4, r.120)
- CHAPTER_VARIABLES.md R010 "the Tegen aerosol climatology" (§4, r.121)
- CHAPTER_VARIABLES.md R011 `CHAPTER_KNOWN_PROPERTIES.md` (§4, r.127)
- CHAPTER_VARIABLES.md R012 "the land-use table's WINTER and SUMMER columns" (§4, r.112-113)
- CHAPTER_VARIABLES.md R013 "ECMWF's table" / "ECMWF code table 4.234" (§5, r.157; §6, r.192; §8.tv, r.362)
- CHAPTER_VARIABLES.md R014 "the FAO clay/sand thresholds" (§6, r.195)
- CHAPTER_VARIABLES.md R015 "WMO table 4.213" (§6, r.198)
- CHAPTER_VARIABLES.md R016 `MISSING_VARIABLES.pdf` (§6, r.205)
- CHAPTER_VARIABLES.md R017 MODIS-IGBP 21 classes, WPS `MMINLU=MODIFIED_IGBP_MODIS_NOAH` (§8, r.356-357)
- CHAPTER_VARIABLES.md R018 "the IGBP class definitions of tree cover" (§8.tv, r.364)

### MISSING_VARIABLES.md (10 voci)

- MISSING_VARIABLES.md R001 [`CHAPTER_VARIABLES.md`](CHAPTER_VARIABLES.md) (§0, r.18)
- MISSING_VARIABLES.md R002 [`CHAPTER_KNOWN_PROPERTIES.md`](CHAPTER_KNOWN_PROPERTIES.md) (§0, r.19)
- MISSING_VARIABLES.md R003 WRF 4.1.1 (§2, r.43)
- MISSING_VARIABLES.md R004 ERA5 waves at ~31 km (§4, r.92)
- MISSING_VARIABLES.md R005 an ocean reanalysis (e.g. CMEMS) (§4, r.94)
- MISSING_VARIABLES.md R006 `CHAPTER_VARIABLES.pdf` §8 (§4, r.110)
- MISSING_VARIABLES.md R007 VEGPARM.TBL (§5, r.137)
- MISSING_VARIABLES.md R008 ECMWF definitions ("as their ECMWF definitions require") (§5, r.146-147)
- MISSING_VARIABLES.md R009 `CHAPTER_KNOWN_PROPERTIES.md` §5 (§5, r.164)
- MISSING_VARIABLES.md R010 ECMWF defines `tcw` / `260028 grle` / `260001 tcolg` (§5, r.191-193)

### CHAPTER_KNOWN_PROPERTIES.md (37 voci)

- CHAPTER_KNOWN_PROPERTIES.md R001 `CHAPTER_VARIABLES.md` (§intro, r.3; §8.1, r.575 "§3 of `CHAPTER_VARIABLES.md`"; §8.4, r.629 "`CHAPTER_VARIABLES.md` §6")
- CHAPTER_KNOWN_PROPERTIES.md R002 `MISSING_VARIABLES.md` (§intro, r.4; §1.3, r.153)
- CHAPTER_KNOWN_PROPERTIES.md R003 `docs/audit/sample.md` (§intro, r.15; §Where, r.646)
- CHAPTER_KNOWN_PROPERTIES.md R004 `docs/audit/re-verification.md` (§Which, r.40; §Where, r.656)
- CHAPTER_KNOWN_PROPERTIES.md R005 [#45](https://github.com/meteocima/CHAPTER/issues/45) (§1.1, r.100)
- CHAPTER_KNOWN_PROPERTIES.md R006 [#48](https://github.com/meteocima/CHAPTER/issues/48) (§1.2, r.131)
- CHAPTER_KNOWN_PROPERTIES.md R007 [#57](https://github.com/meteocima/CHAPTER/issues/57) (§1.3, r.161)
- CHAPTER_KNOWN_PROPERTIES.md R008 [#56](https://github.com/meteocima/CHAPTER/issues/56) (§2.1, r.186; §2.2, r.203)
- CHAPTER_KNOWN_PROPERTIES.md R009 [#55](https://github.com/meteocima/CHAPTER/issues/55) (§2.3, r.225)
- CHAPTER_KNOWN_PROPERTIES.md R010 [#40](https://github.com/meteocima/CHAPTER/issues/40) (§3.1, r.255; §3.2, r.269)
- CHAPTER_KNOWN_PROPERTIES.md R011 [#44](https://github.com/meteocima/CHAPTER/issues/44) (§3.2, r.270; §4.1, r.320)
- CHAPTER_KNOWN_PROPERTIES.md R012 [#42](https://github.com/meteocima/CHAPTER/issues/42) (§3.3, r.286)
- CHAPTER_KNOWN_PROPERTIES.md R013 [#39](https://github.com/meteocima/CHAPTER/issues/39) (§4.2, r.336)
- CHAPTER_KNOWN_PROPERTIES.md R014 [#50](https://github.com/meteocima/CHAPTER/issues/50) (§5.1, r.388)
- CHAPTER_KNOWN_PROPERTIES.md R015 [#49](https://github.com/meteocima/CHAPTER/issues/49) (§5.2, r.422)
- CHAPTER_KNOWN_PROPERTIES.md R016 [#51](https://github.com/meteocima/CHAPTER/issues/51) (§6.1, r.455)
- CHAPTER_KNOWN_PROPERTIES.md R017 [#47](https://github.com/meteocima/CHAPTER/issues/47) (§6.2, r.482)
- CHAPTER_KNOWN_PROPERTIES.md R018 [#34](https://github.com/meteocima/CHAPTER/issues/34), [#36](https://github.com/meteocima/CHAPTER/issues/36) and [#38](https://github.com/meteocima/CHAPTER/issues/38) (§7.1, r.526-528)
- CHAPTER_KNOWN_PROPERTIES.md R019 [#54](https://github.com/meteocima/CHAPTER/issues/54) (§7.2, r.557)
- CHAPTER_KNOWN_PROPERTIES.md R020 [#53](https://github.com/meteocima/CHAPTER/issues/53) (§8.1, r.576)
- CHAPTER_KNOWN_PROPERTIES.md R021 [#37](https://github.com/meteocima/CHAPTER/issues/37) (§8.2, r.594; §8.3, r.608)
- CHAPTER_KNOWN_PROPERTIES.md R022 [#35](https://github.com/meteocima/CHAPTER/issues/35) (§8.4, r.634)
- CHAPTER_KNOWN_PROPERTIES.md R023 IFS Cy41r2's own equations (7.5, 7.6, 7.89, 7.90) (§3.1, r.243-244)
- CHAPTER_KNOWN_PROPERTIES.md R024 the Tegen aerosol climatology (§1.1, r.77)
- CHAPTER_KNOWN_PROPERTIES.md R025 a CAM ozone climatology (§1.1, r.76)
- CHAPTER_KNOWN_PROPERTIES.md R026 the WMO screen convention (§3.1, r.247)
- CHAPTER_KNOWN_PROPERTIES.md R027 `tools/audit/` of the [CHAPTER repository](https://github.com/meteocima/CHAPTER) (§Where, r.640-641)
- CHAPTER_KNOWN_PROPERTIES.md R028 `docs/audit/harness.md` (§Where, r.647)
- CHAPTER_KNOWN_PROPERTIES.md R029 `docs/audit/f1-pressure-levels.md` (§Where, r.648)
- CHAPTER_KNOWN_PROPERTIES.md R030 `docs/audit/f2-near-surface.md` (§Where, r.649)
- CHAPTER_KNOWN_PROPERTIES.md R031 `docs/audit/f3-column-integrals.md` (§Where, r.650)
- CHAPTER_KNOWN_PROPERTIES.md R032 `docs/audit/f4-radiation.md` (§Where, r.651)
- CHAPTER_KNOWN_PROPERTIES.md R033 `docs/audit/f5-water-cycle.md` (§Where, r.652)
- CHAPTER_KNOWN_PROPERTIES.md R034 `docs/audit/f6-soil-and-snow.md` (§Where, r.653)
- CHAPTER_KNOWN_PROPERTIES.md R035 `docs/audit/f7-static-and-surface.md` (§Where, r.654)
- CHAPTER_KNOWN_PROPERTIES.md R036 `docs/audit/f8-surface-exchange.md` (§Where, r.655)
- CHAPTER_KNOWN_PROPERTIES.md R037 namelist/config citati: `aer_opt = 0` (§1.1, r.77); `ICLOUD = 1` (§1.2, r.123); `usemonalb = .false.` (§8.2, r.580); `rdlai2d = .false.` (§8.4, r.632)

## 9. Riferimenti segnalati come incompleti o sospetti dagli estrattori, con l'esito della verifica online

### CHAPTER_VARIABLES.md (6 voci)

- CHAPTER_VARIABLES.md S004 [RIFERIMENTO INCOMPLETO] "the ERA5 set truncated at the model top" — quale insieme ERA5 non è detto; 13 + 8 livelli implicherebbero 21 (§2, r.46)
  → verifica 2 (online) COMPLETATO — ERA5: data documentation, https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation (2026-09-08): L'insieme e' quello dei 37 livelli di pressione ERA5; i livelli sopra 50 hPa sono 8 (30,20,10,7,5,3,2,1) come dichiarato. Nota: il troncamento dei 37 al top da' 29 livelli, non 13; i 13 sono un sottoinsieme dei 29 (tutti presenti nella lista ERA5)
- CHAPTER_VARIABLES.md S006 [RIFERIMENTO INCOMPLETO] "as their ECMWF definitions require" — nessun documento o versione (§3, r.56)
  → verifica 2 (online) COMPLETATO — eccodes 2.34.0 definitions: https://raw.githubusercontent.com/ecmwf/eccodes/2.34.0/definitions/grib2/localConcepts/ecmf/paramId.def e .../grib2/paramId.def: tp '228': "typeOfStatisticalProcessing = 1"; ssrd '169': "typeOfStatisticalProcessing = 1"; 10fg '49': "typeOfStatisticalProcessing = 2" (chiave che esiste solo nei PDT statistici, es. 4.8)
- CHAPTER_VARIABLES.md S023 [RIFERIMENTO INCOMPLETO] "the Tegen aerosol climatology" — nessuna citazione né versione (§4, r.121)
  → verifica 2 (online) COMPLETATO — Tegen, I., Hollrig, P., Chin, M., Fung, I., Jacob, D., Penner, J. (1997). Contribution of different aerosol species to the global aerosol extinction optical thickness: Estimates from model results. J. Geophys. Res. 102(D20), 23895-23915, doi:10.1029/97JD01864: IFS Cy41r2 Part IV §2 p.27: "a new climatology ... compiled by Tegen et al. (1997), which has been implemented in the ECMWF forecast system from Cy26r3 onwards"; ERA5 = Cy41r2 (ERA5 data documentation)
- CHAPTER_VARIABLES.md S031 [RIFERIMENTO INCOMPLETO] "the FAO clay/sand thresholds" — nessuna citazione né versione (§6, r.195)
  → verifica 2 (online) COMPLETATO — FAO/IIASA/ISRIC/ISSCAS/JRC, Harmonized World Soil Database v1.2, Feb 2012, p.10 (T_TEXTURE), https://esdac.jrc.ec.europa.eu/ESDB_Archive/Soil_Data/Docs_GlobalData/Harmonized_World_Soi_Database_v1.2.pdf; FAO (2003) DSMW (citato in IFS Cy41r2 Part IV §11.9); Balsamo et al. (2009) J. Hydrometeorol. 10(3), 623-643, doi:10.1175/2008JHM1068.1: HWSD: "Coarse textured: ... less than 18 percent clay and more than 65 percent sand. Medium textured: ... less than 35 % clay and less than 65 % sand; the sand fraction may be as high as 82 percent if a minimum of 18 percent of clay is present. Fine textured: ... more than 35 percent clay". Parziale: le soglie per "medium fine" e "very fine" (clay>=60) usate in static_ref.SLT_RULE non trovate in HWSD 1.2 ne' 2.0
- CHAPTER_VARIABLES.md S032 [RIFERIMENTO INCOMPLETO] "ECMWF code table 4.234" e "WMO table 4.213" — senza versione o edizione (§6, r.192, r.198)
  → verifica 2 (online) COMPLETATO — WMO GRIB2 code tables come distribuite in eccodes: https://raw.githubusercontent.com/ecmwf/eccodes/develop/definitions/grib2/tables/30/4.234.table e 4.213.table (master tables version 30; 4.234 presente gia' dalla versione 10); param-db ECMWF unita' 112 "(Code table 4.234)", 231 "(Code table 4.213)": 4.234 "Canopy cover fraction (to be used as partitioned parameter in product definition template 4.53 or 4.54)", 20 voci 1 Crops...20 Water and land mixtures; 4.213 "Soil type", 11 voci. Nota: 4.234 e' una tabella WMO, non "ECMWF code table"
- CHAPTER_VARIABLES.md S035 [RIFERIMENTO INCOMPLETO] "the IGBP class definitions of tree cover" — nessuna citazione (§8.tv, r.364)
  → verifica 2 (online) COMPLETATO — Sulla-Menashe, D., Friedl, M.A., User Guide to Collection 6 MODIS Land Cover (MCD12Q1 and MCD12C1) Product, C6.1, 20 Apr 2022, Table 3 "MCD12Q1 IGBP legend and class descriptions", https://lpdaac.usgs.gov/documents/1409/MCD12_User_Guide_V61.pdf (legenda da Loveland and Belward, 1997): classi 1-5 "Tree cover >60%", 8 "Tree cover 30-60%", 9 "Tree cover 10-30%"

### MISSING_VARIABLES.md (5 voci)

- MISSING_VARIABLES.md S007 [RIFERIMENTO SOSPETTO] "Approximable radiatively (§3)" per l'albedo del ghiaccio — §3 non contiene più una via per l'albedo, dichiarato spostato/consegnato (§4, r.96; §3, r.72-73)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (rimando interno al file)
- MISSING_VARIABLES.md S008 [RIFERIMENTO SOSPETTO] "`geo_em.d02`, recorded here as irrecoverable" — la nota fa riferimento a una sua versione precedente (§3, r.74)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (rimando interno al file)
- MISSING_VARIABLES.md S034 [RIFERIMENTO INCOMPLETO] "ECMWF definitions" citate senza documento né versione/ciclo (§5, r.146-147; r.191-193)
  → verifica 2 (online) COMPLETATO — ECMWF Parameter Database, paramId 246 `clwc`, 133 `q`, 136 `tcw` (https://codes.ecmwf.int/parameter-database/api/v1/param/246/ ecc.): 246: "mass of cloud liquid water droplets per kilogram of the total mass of moist air. The 'total mass of moist air' is the sum of the dry air, water vapour, cloud liquid, cloud ice, rain and falling snow"; 136: "sum of water vapour, liquid water, cloud ice, rain and snow"
- MISSING_VARIABLES.md S035 [RIFERIMENTO INCOMPLETO] nessuna issue o commit citati nell'intero file; le misure non sono collegate a una registrazione (intero file)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (issue/commit interni)
- MISSING_VARIABLES.md S036 [RIFERIMENTO INCOMPLETO] VEGPARM.TBL senza sezione della tabella (§5, r.137)
  → verifica 2 (online) COMPLETATO — https://raw.githubusercontent.com/wrf-model/WRF/v4.1.1/run/VEGPARM.TBL (WRF v4.1.1), sezione `MODI-RUC`, colonna LEMI; `cmp` con /leonardo_work/AIFPT_AILAMIT/CHAPTER/WPS/VEGPARM.TBL: identico: urbano (13) .880, acqua (17) e laghi (21) .980; ma il minimo della sezione e' .850 (16 Barren), quindi "0.88 urban to 0.98 water" non e' l'intervallo completo

### CHAPTER_KNOWN_PROPERTIES.md (6 voci)

- CHAPTER_KNOWN_PROPERTIES.md S007 [RIFERIMENTO INCOMPLETO] "CAM ozone climatology" e "Tegen aerosol climatology" citate senza riferimento bibliografico né versione (§1.1, r.76-77)
  → verifica 2 (online) COMPLETATO — Tegen et al. (1997) doi:10.1029/97JD01864 (vedi CV S023); CAM ozone: WRF Users Guide "WRF Physics" (https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/physics.html) e README.namelist v4.1.1: WRF: "The ozone data are adapted from CAM radiation (ra_*_physics=3), and have latitudinal (2.82 degrees), height, and temporal (monthly) variation" (`o3input = 2`, file `ozone.formatted`); "The aerosol data are based on [Tegen et al., 1997]". Nessun riferimento bibliografico per il dataset di ozono CAM nelle fonti WRF
- CHAPTER_KNOWN_PROPERTIES.md S019 [RIFERIMENTO INCOMPLETO] "IFS Cy41r2's own equations (7.5, 7.6, 7.89, 7.90)" — non indicato quale documento/parte della IFS Documentation (§3.1, r.243-244)
  → verifica 2 (online) COMPLETATO — IFS Documentation Cy41r2, Part IV: Physical Processes, cap. 7 (Operational implementation 8 March 2016), pp.94-95 e appendice A.2 pp.111-112, https://www.ecmwf.int/sites/default/files/elibrary/2016/16648-part-iv-physical-processes.pdf: (7.5) Tetens esat = a1 exp{a3 (T−T0)/(T−a4)}, acqua a1=611.21 Pa a3=17.502 a4=32.19 K, ghiaccio a3=22.587 a4=−0.7 K; (7.6) α=((T−Tice)/(T0−Tice))², Tice=250.16 K, T0=273.16 K; (7.89) RH = e/esat = p q (1/ε) / [esat (1+q(1/ε−1))], ε=0.621981; (7.90) esat = α esat(w) + (1−α) esat(i). Attenzione: nel PDF Cy43r1 (17117, quello linkato dal param-db) 7.89/7.90 sono la sorgente convettiva di nube
- CHAPTER_KNOWN_PROPERTIES.md S020 [RIFERIMENTO INCOMPLETO] "WMO screen convention" — nessun documento WMO citato (§3.1, r.247)
  → verifica 2 (online) COMPLETATO — WMO-No. 8, Guide to Instruments and Methods of Observation, Vol. I, 2023 edition, cap. 4 Annex 4.A (17) e §4.1.2, https://library.wmo.int (copia: https://amc.namem.gov.mn/wp-content/uploads/WMO/1.%208_I-2023_en.pdf): "(17) Relative humidity at temperatures less than 0 °C is to be evaluated with respect to water"; §4.1.2: "Relative humidity U. Ratio in per cent of the observed vapour pressure to the saturation vapour pressure with respect to water"
- CHAPTER_KNOWN_PROPERTIES.md S042 [RIFERIMENTO INCOMPLETO] "The threshold sits in that gap with a factor of seven of slack" — la soglia stessa non è indicata nel file (§7.1, r.512-513)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (soglia interna: CLAUDE.md la da' come static_ref.OCEAN_MIN_CELLS = 2000)
- CHAPTER_KNOWN_PROPERTIES.md S050 [RIFERIMENTO SOSPETTO] #37 citata sia per `al` (§8.2) sia per `slor`/`sdor` (§8.3); non chiaro se la stessa issue copra entrambe (§8.2, r.594; §8.3, r.608)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (issue #37 interna)
- CHAPTER_KNOWN_PROPERTIES.md S052 [RIFERIMENTO INCOMPLETO] La tabella "Where the measurements live" non assegna §8.4 (né §2.3 esplicitamente) ad alcun documento di audit, pur dicendo "Every number in this document" (§Where, r.640-656)
  → verifica 2 (online) NON_TROVATA — -: fuori ambito online (documenti di audit interni)
