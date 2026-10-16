# Scaletta del report

Titolo di lavoro: *L'archivio GRIB2 CHAPTER. Downscaling dinamico a 3 km di ERA5. Contenuto e
corrispondenza con lo schema ERA5*.

Fonti di questa scaletta: le tre schede (`schede/CHAPTER_VARIABLES.md` = **CV**,
`schede/MISSING_VARIABLES.md` = **MV**, `schede/CHAPTER_KNOWN_PROPERTIES.md` = **KP**) e gli esiti
di `schede/da_verificare.md` (**DV**). Gli md originali non sono stati riaperti.
Gli identificativi sono quelli delle schede: `CV-A061` = affermazione A061 della scheda CV,
`KP-N047` = dato N047 della scheda KP, `CV-T012` = tabella T012, `CV-E002` = equazione E002.
Quando una voce è stata corretta dalla verifica, accanto c'è il valore da usare (→).

Ambito (deciso il 2026-09-29): CHAPTER in sé e la sua mappatura sullo schema ERA5. Restano fuori
la richiesta di variabili, il progetto che l'ha fatta e il confronto tra richiesto e consegnato
(MV §1 e §6, MV-A013..A027, MV-A179..A194), che vanno nel secondo report. Restano fuori anche le
vie alternative non implementate di MV §3 (MV-A045..A060), perché sono proposte e non contenuto.

Destinatari: utenti scientifici dei dati (meteorologia, clima, apprendimento automatico) che
confrontano con ERA5 e non leggono il repository.

---

## Capitolo 1 – La simulazione (`01-simulazione.tex`)

Cosa ha prodotto i dati: senza questo capitolo nessuna delle scelte successive si capisce.

### 1.1 Modello, dominio e griglia
- WRF 4.1.1, dominio d02, 49 livelli verticali, top a 50 hPa: CV-A014, CV-N006, CV-N007, MV-A028/A029.
- Griglia Mercator 1641 × 1353 punti a 3 km, 2 220 273 punti per campo: CV-A015, CV-N008..N010.
- Angoli del dominio: CV-N011 → quattro decimali, 23,4719–60,0006 N e −19,9722–42,2555 E (DV).
- Parallelo standard 44,671: CV-N012 (confermato sui dati, DV).
- Sfera di raggio 6 370 000 m: CV-A016, CV-N013 (qui come proprietà del modello; la codifica al cap. 2).
- Periodo: 2019, 2024 e 2025-01-01 → 2025-07-02, orario; la fine del 2025 è la fine della
  simulazione stessa (CV-A022 → solo la fine 2025 è attestata; CV-A023, CV-N018).
  Il totale di 21 936 ore torna per aritmetica (8760 + 8784 + 4392). Non si scrive che il 2020–2023
  seguirà (non attestato).

### 1.2 Configurazione fisica
Tabella: opzione, valore, conseguenza per i campi (da MV-T002, senza la colonna "per la lista
richiesta").
- `BL_PBL_PHYSICS=1` (YSU), `KM_OPT=4`: MV-A031, MV-A033, MV-A064.
- `SF_OCEAN_PHYSICS=0`, nessun modello d'onda: MV-A034, MV-A035.
- `SST_UPDATE=0`, run giornaliere: MV-A036, CV-A102. La run integra 30 h con 6 h di spin-up
  (MV-N014 → DV: `start_hour=18`, `run_hours=30`), non 24 h.
- `CU_PHYSICS=0`: MV-A037, CV-A125.
- `MP_PHYSICS=6` (WSM6), nessuna grandine: MV-A038, MV-A170.
- `ICLOUD=1` (Xu–Randall), frazione nuvolosa continua: MV-A039, MV-A116, KP-A077.
- `SF_SURFACE_PHYSICS=3` (RUC), nodi a 0, 5, 20, 40, 160, 300 cm: MV-A040, CV-A132.
- `SF_LAKE_PHYSICS=0`, `SF_URBAN_PHYSICS=0`: MV-A041, CV-A104.
- Radiazione RRTMG, `aer_opt=0`, ozono climatologico CAM (`o3input=2`): KP-A045, KP-A046, CV-A089.
- `usemonalb=.false.`, `rdlai2d=.false.`: CV-A081, CV-A128, KP-A311, KP-A338.
- `isfflx=1`, `output_diagnostics=0`, `nwp_diagnostics=1`: MV-A081, MV-A089, MV-A092.
- La configurazione è la stessa in tutti i periodi controllati: MV-A030, MV-A007.

### 1.3 Il file statico `geo_em.d02`
- È il file statico della run: MV-A050, CV-A240, CV-A241 → accordo col land use orario 100,00 % a
  luglio 2019 e gennaio 2025, 99,98 % il 2025-02-15 12Z, e i 2735 punti diversi sono tutti ghiaccio
  marino (DV, #59/#62).
- Porta copertura frazionaria, tessitura, laghi: CV-A006, CV-A007, CV-N004, CV-N005.
- La categoria dominante tiene in media il 90,1 % di una cella di terra; il 17,93 % delle celle di
  terra ha sia vegetazione alta sia bassa sopra il 5 %: CV-A136, CV-N078, CV-N079 (→ 17,93 %).
- 21 classi MODIS-IGBP, `MMINLU=MODIFIED_IGBP_MODIS_NOAH`: CV-N092, CV-R017.

## Capitolo 2 – Il formato dell'archivio (`02-formato.tex`)

### 2.1 File e messaggi
- 90 variabili, 246 messaggi per file orario, prese dal registro del convertitore:
  CV-A001..A003, CV-N001, CV-N002.
- GRIB2, template di griglia 3.10, centro `ecmf`, packing `grid_ccsds` a 24 bit: CV-A017, CV-A018, CV-N014.
- Nome dei file: CV-A021.
- paramId e shortName ECMWF: CV-A019 → "direttamente confrontabile" non si scrive: ERA5 (edizione 1)
  e CHAPTER (edizione 2) usano tipi di livello diversi (DV, #14).
- Dimensioni: CV-N015..N017 → media 737 MB su 184 file di settembre 2024 (661 MB alle 00Z),
  765 MB su 476 file di febbraio–marzo 2024; 17,7–18,4 GB al giorno, 6,5–6,7 TB all'anno (DV, misure 2026-09-29).
- Sanity check dell'inventario: CV-A002.

### 2.2 Geometria
- `shapeOfTheEarth=1`, raggio 6 370 000 m: CV-A016, MV-A177.
- Errore di geolocalizzazione massimo 2,009 m (misurato, DV); senza la sfera dichiarata eccodes
  ricostruisce una griglia spostata di ~1,1 km al bordo nord (MV-A178 → #26).

### 2.3 Livelli verticali
- 13 livelli di pressione, gli stessi per ogni variabile 3D (1000 … 50 hPa): CV-A024, CV-N019, CV-N020.
- Sottoinsieme dei 37 livelli ERA5; gli 8 sopra 50 hPa sono sopra `P_TOP`: CV-A025, CV-A026, CV-N021
  (→ l'insieme ERA5 troncato al top dà 29 livelli; i 13 ne sono un sottoinsieme, DV online).
- Tipi di livello a singolo livello: CV-A027 (→ `meanSea` non attestato: verificare sul file in fase 3,
  altrimenti non nominarlo), CV-N022; più `entireLake` e *most unstable parcel* (CV-S005).
- Perché 13 e non 29 livelli: MV-A191..A193 → solo "il file a 13 livelli pesa 0,74 GB; la proiezione
  a 29 livelli è 1,45 GB" (proiezione, non misura). **Da decidere**: se tenerlo (vedi Domande).

### 2.4 Convenzione temporale
- Campi istantanei: template di prodotto 0, `dataDate`/`dataTime` = istante di validità: CV-A028, CV-N023.
- Campi accumulati: template 8 (le definizioni ECMWF richiedono `typeOfStatisticalProcessing`),
  riferimento 00 UTC, intervallo 0–H, nulli alle 00 UTC: CV-A029..A031, MV-A174, MV-A175
  (fonte della regola del template: definizioni eccodes 2.34.0, DV).
- Un file mescola tempi di riferimento; indicizzare sulla validità: CV-A034, CV-A035.
- `10fg`: riferimento H−1, intervallo 0–1, `stepType=max`: CV-A032, KP-A220. La finestra dichiarata
  al cap. 5.
- Per riconoscere gli accumulati si usano `stepType` e `stepRange`; `generatingProcessIdentifier`
  vale 128 in tutti i 246 messaggi: KP-A303..A309, KP-N023, KP-N128 (CV-A036 contraddetta, DV).

## Capitolo 3 – Regole di corrispondenza con ERA5 (`03-regole.tex`)

Le due regole che governano tutto il resto, dette una volta qui e poi solo richiamate con `\cref`.

### 3.1 Regola di pubblicazione
- Un campo si pubblica sotto un nome ERA5 solo se la grandezza WRF è quella ERA5, o se la differenza
  si dice in una riga: KP-A333 (→ formulazione completa, DV #47/#50), CV-A010, CV-A011.
- "Nessun parametro esiste" e "ERA5 non lo pubblica" sono affermazioni diverse: KP-A334.
- Approssimazioni dichiarate, tabella (cinque righe, sei campi): CV-T003, CV-A037 (→ sei campi in
  cinque righe), dettaglio nei capitoli di dominio.

### 3.2 Regola di mascheratura
- Un punto è mancante dove il parametro ERA5 non è definito; bitmap, mai zeri: KP-A264, KP-A265, CV-A108.
- Tabella dei campi mascherati e dominio di definizione: CV-T004 unita a KP-T012
  (`sst`/`ci`, `cl`/`dl`, `swvl`/`stl`, `slt`, `tvl`, `mucin`, `tsn`, `fal`).
- Distinzione mare / acque interne per dimensione della componente connessa, non per classe lago:
  CV-A110, CV-A111, KP-A272..A277, CV-N063..N067 (il Mar Nero chiamato lago; 89 % delle celle di lago
  piene sono Mar Nero, Azov e Baltico, KP-N119). Il valore della soglia (2000 celle) non è nelle
  schede: **va aggiunto** solo se confermato (vedi Domande).

### 3.3 Campi statici e campi orari
- Statico = identico in ogni file, dall'input statico: CV-A229.
- `lsm` segue il modello ora per ora, perché WRF riclassifica il ghiaccio marino come terra: CV-A052,
  CV-A230, KP-A284..A286; `lsm ∧ ¬(ci>0)` dà il senso ERA5 (CV-A053, CV-E006).
- `al` cambia in due modi (tabella stagionale e punti di ghiaccio): rimando a 7.5.
- `tvl`, `tvh`, `slt` sono statici (MV-A145/A146 contraddette in questa parte, DV #03).
- 2469 punti riclassificati il 2024-03-20, esattamente i punti di ghiaccio: MV-A145, MV-N056.

## Capitolo 4 – Atmosfera (`04-atmosfera.tex`)

### 4.1 Le 13 variabili sui livelli di pressione
Tabella da CV-T005 (13 righe): CV-A147..A159.
- Contenuti specifici, non rapporti di mescolanza, con lo stesso denominatore per `q` e idrometeore:
  MV-A127, MV-A128; correzione 0,011 % in mediana, 1,44 % al 99° percentile, 2,26 % al massimo
  (MV-A129/N044 contraddette → #41). Definizione ECMWF della massa di aria umida: param-db 246 (DV).
- `cc` è continuo: MV-A116 (18–22 % dei punti nuvolosi esattamente a 1, sottodominio 500 × 600).
- `r` sulla fase mista (IFS Cy41r2, eq. 7.5, 7.6, 7.89, 7.90), non troncata a 100:
  KP-A139, KP-A143, KP-A144, KP-N066, KP-N067, KP-A147; fattore fino a 1,8 sul ghiaccio.
  IFS Cy41r2 è il ciclo di ERA5 (KP-A145 → confermato online).
- `r` sopra 100 % è normale: 139,7 % a 300 hPa, 34 785 punti a 400 hPa (un file): KP-A153..A156, KP-A159.
- `z = 9,80665 · z_WRF`; scarto idrostatico 0,034 % (1 su 2900; ~2 m a 500 hPa, 7 m a 50 hPa);
  accordo esatto superficie–livelli su 1 349 910 punti di terra: KP-A189..A196, KP-E001, KP-N082, KP-N083.

### 4.2 Sotto il terreno
- Clamping al livello modello più basso, non estrapolazione: KP-A170..A174, CV-A096..A098,
  KP-N074; quota 24–27 m sopra il suolo (KP-N071 "circa 25 m" e KP-N077 "22 m" vanno riportati a
  questa: 22 m è la distanza tra 2 m e il livello più basso).
- Coerenza con la superficie: `2t − t(1000 hPa)` −0,9 K a mezzanotte, +1,4 K a mezzogiorno (luglio): KP-A177, KP-A178.
- `z` contraddice `sp` sul 47,6 % del dominio a 1000 hPa e sul 9 % a 925: KP-A179..A182, CV-A100.
- ERA5 estrapola: differenza di convenzione, bias `t` −1,71 K a 1000 hPa contro −0,05 K a 850,
  correlazione di `z` 0,108: KP-A183..A187.
- `r` sotto terra fino a ~163 %: KP-A157, KP-A158.
- Indicazione all'utente: mascherare i livelli contro `sp` (KP-A188, CV-A101).

### 4.3 Campi vicino alla superficie
Tabella da CV-T006 e CV-T007 (12 righe): CV-A160..A171.
- `2r` sull'acqua liquida (convenzione WMO): KP-A140, KP-A141, KP-A148 (WMO-No. 8, 2023, All. 4.A),
  ERA5 non pubblica una `2r` (KP-A149); non costruire un profilo con `2r` in fondo a `r` (KP-A151).
- `2d` supera `2t` di 0,0133 K nei punti saturi (6000–64 000 punti per istante), lasciato così:
  KP-A160..A168, KP-N072.
- `2d` è in kelvin: CV-A167 (il confronto con il GRIB1 va in "versioni precedenti", vedi Domande).
- `vwsh` shear bulk 10–100 m: CV-A170.

### 4.4 Colonne e nubi
Tabella da CV-T008 (10 righe): CV-A172..A181.
- `tcw` somma sei specie (graupel incluso), ECMWF ne definisce cinque: KP-A252, KP-A253, MV-A164..A167;
  residuo = colonna di graupel, 0,4 % in media, fino a 26,46 kg/m² in una cella di luglio: KP-T011,
  KP-A255..A263 (MV-N070 "26,5" → 26,46). ECMWF definisce `grle` e `tcolg`, ERA5 non li pubblica (KP-A328).
- Nubi: `tcc` 22 % sotto ERA5, `hcc` 39 % sotto: KP-T003, KP-A062..A068 (tutti i 34 istanti).
- Il deficit non è l'overlap (intervallo delle assunzioni 2–4 %, al più un settimo del divario):
  KP-A069..A076, KP-A083; è `CLDFRA` (11 % di ghiaccio in più, 39 % di nubi alte in meno): KP-A077, KP-A078.
- Parte del divario è risoluzione, limitata dallo stesso 2–4 %: KP-A080..A084.
- `tcc`, `hcc`, `mcc`, `lcc` sono overlap maximum-random di `CLDFRA`: MV-A117, KP-A070.

### 4.5 Instabilità
- `mucape`, `mucin` most-unstable (particella di 500 m, massima θe nei 3 km più bassi): MV-A135, CV-A232, CV-A233.
- `mucin` definito solo dove CAPE ≥ 100 J/kg, altrove bitmap: KP-A287..A290, CV-A113, CV-A115;
  presente dal 3,8 % (gennaio) al 28,8 % (luglio), tabella KP-T013 (CV-A114 → decimali di #54).
- Dove noi siamo mancanti ERA5 porta 25–265 J/kg; dove presenti siamo 0,03–0,24 di ERA5: KP-A298..A300.
- `mucape` denso, i suoi zeri sono reali: KP-A302; zero sul 46 % (luglio) – 69 % (febbraio) del
  dominio (#54), 34 % il 2024-09-04 16Z (misura, DV). MV-A131..A133 contraddette.

## Capitolo 5 – Radiazione, pelle e scambi di superficie (`05-superficie-energia.tex`)

### 5.1 Radiazione
Campi radiativi accumulati da CV-T009/T011: CV-A204..A207, CV-A214..A217, CV-A234..A238.
- Onda corta in superficie alta: +8,5 % in cielo sereno, +13,6 % con nubi; tabella KP-T002
  (KP-A049..A055); nessun aerosol (`aer_opt=0`), ERA5 usa la climatologia di Tegen et al. (1997):
  KP-A046, KP-A047, CV-A089..A092. Campi termici entro 1,1 %: KP-A057, KP-A058.
- Lo spessore ottico 0,1–0,2 che "spiega" il bias: KP-A048, CV-N049 → **senza fonte**: si esclude
  o `\todo{fonte}`.
- `LWDNT` & C. identicamente nulli (non pubblicati): rimando al cap. 8.

### 5.2 Temperatura di pelle
- `TSK` non scritto; `skt` invertita da `LWUPB = ε σ T⁴ + (1−ε) GLW`: CV-A060, CV-A061, KP-A123,
  KP-A124, CV-E001/KP-E002 (unificare il simbolo del flusso discendente: `GLW`).
- Emissività misurata dalla run: `ε = 1 − (LWUPB − LWUPBC)/(LWDN − LWDNC)`, identità, spread 0,0000
  per categoria, 0,98000 sull'acqua: CV-A062..A067, CV-E002; tabella `VEGPARM.TBL` sezione `MODI-RUC`,
  LEMI da 0,850 (suolo nudo) a 0,980 (acqua) (MV-A121 → DV online).
- Neve: 0,98 sopra la soglia di copertura nevosa, raccordo sotto; soglia 1,5 % scelta con uno sweep
  sui 34 istanti: CV-A072..A074, CV-N039, CV-N040 (KP-A132 → "piatta solo sopra la soglia").
- Accuratezza stagionale: 99,98 % dei punti di terra a luglio, 93,05 % a gennaio; RMSE 0,0012 K a
  luglio, 0,084–0,119 K a gennaio e febbraio (p99 0,81 K, max 2,79 K): tabella KP-T007, CV-A069..A071.
- Sull'acqua 0,0005 K RMSE (max 0,002 K) su ~910 000 punti: CV-A075, KP-A128 (MV-A122/N041 contraddette).
- Sulla terra senza neve rispetto al primo livello di suolo: 0,026 K RMSE su un istante di settembre
  (MV-A123 → misura DV).
- Bias freddo sulla terra: −1,64 K rispetto a ERA5, −3,24 K a mezzogiorno; mare +0,01 K; tabella
  KP-T004, KP-A085..A089, KP-N048.
- L'errore di derivazione è più di dieci volte più piccolo del bias fisico (CV-A076, KP-A137 → non "trenta").
- Il bias contraddice radiazione e nubi; la ripartizione non si decide dai dati pubblicati perché mancano
  `HFX`, `LH` e il flusso nel suolo: KP-A094..A100, CV-A079.

### 5.3 Rugosità, velocità d'attrito, sforzo
- `fsr` è `ZNT` locale (valori per categoria, 1,00 m sui 19 867 punti urbani, 0,011 m sotto neve),
  ERA5 una rugosità efficace: KP-A105..A114, CV-A045..A048; tabella KP-T005 con **rapporto delle
  medie e rapporto delle mediane in colonne distinte** (vedi contraddizione 9).
- `zust` 1,62–2,06 volte ERA5 sulla terra, 1,08–1,12 sul mare: KP-A116..A119, KP-T006. Il dato
  per ora (1,06–1,13 alle 00Z, 1,40–1,75 alle 12Z) **si esclude** (vedi contraddizione 10).
- `iews`, `inss` = `ρu*²` proiettato sul vento a 10 m (allineamento assunto): CV-A044, MV-A147, MV-A148;
  identità verificate a 1,8e-6 N/m² e 2,7e-4 m/s: KP-A121, KP-A122.

## Capitolo 6 – Vento a 10 m e raffica (`06-raffica.tex`)

- `10fg` è il massimo orario del vento a 10 m risolto: KP-A200, CV-A033, CV-A162.
- ERA5 stima la raffica (vento medio + termine turbolento da u* + termine convettivo proporzionale allo
  shear 850–950 hPa, IFS Cy41r2 §3.10.4, eq. 3.99): KP-A197..A199 (→ DV online; il termine convettivo
  non è "correnti discendenti"). La raffica WMO come media su 3 s (param-db `i10fg`, DV).
- Confronto: 0,625 di `10fg` ERA5, 0,644 di `i10fg`, correlazione 0,81; 1,004–1,032 del proprio vento
  istantaneo; tabella KP-T008, KP-A201..A208, KP-N091.
- La raffica non entra nelle condizioni al contorno (Vtable ECMWF standard senza codici 49/228029;
  la Vtable effettiva della run non è verificata → formulare con cautela): KP-A210, KP-A211.
- La run non scrive un diagnostico di raffica: nessuna variabile di raffica nel wrfout oltre
  `WSPD10MAX` (KP-A212 → misura DV).
- Uso: sottostima del 38 % come raffica; buono per classificare, non per soglie: KP-A216..A218.
- Finestra dichiarata: 17 reset mancati su 138 transizioni (12,3 %), eccesso 0,499–0,784 m/s contro
  0,068–0,311; tabella KP-T009, KP-A222..A235, KP-N096..N098. Non rilevabile dal file: KP-A230, KP-A231.
- KP-A215 (il 3 km "ha bisogno" di un incremento minore) → **non trovata**: si esclude.

## Capitolo 7 – Acqua, suolo, neve e campi statici (`07-suolo-statici.tex`)

### 7.1 Precipitazione e deflusso
Da CV-T009: CV-A196, CV-A203, CV-A208, CV-A192, CV-A222, CV-A223.
- `tp` completo in `RAINNC` (`RAINC` nullo): MV-A037; pioggia = totale − neve − graupel: MV-A171, MV-E006.
- `sf` è solo `SNOWNC`, senza graupel (MV-A182 → DV #52): verificare in fase 3 come #52 è stata chiusa.
- Deflusso: tre variabili, un campo; tabella KP-T010; `ssro` nullo su 5 dei 18 istanti non-00Z,
  al più 19 punti non nulli; causa il riferimento alle 00 UTC; contro ERA5 la ripartizione è opposta:
  KP-A236..A251, MV-A154..A163. Formulazioni da correggere: vedi contraddizione 11.
- Snowmelt (`ACSNOM`) non monotono: al cap. 8.

### 7.2 Suolo
- `swvl1-4`, `stl1-4` come integrali esatti del profilo lineare RUC sugli strati ERA5 0–7, 7–28,
  28–100, 100–289 cm; niente estrapolazione: CV-A131..A133, CV-A271..A273, MV-A096..A099
  (CV-N103 → verificare 7–28 e 28–100 sul registro in fase 3). Nodi usati per strato:
  (0,1,2), (1,2,3), (2,3,4), (3,4,5), somme di riga 1,0 (CV-N104 → DV #24).
- `swvl` usa l'umidità totale (liquido + ghiaccio): CV-A274.
- Maschera sulla terra permanente, quindi anche fuori dal ghiaccio marino (CV-A275 → DV); sotto il ghiaccio
  il modello riempie la colonna fino a 1,000 contro porosità 0,435: CV-A056, KP-A278..A283.

### 7.3 Neve
Da CV-T009: `sd`, `rsn`, `snowc`, `tsn`: CV-A193, CV-A194, CV-A200, CV-A224.
- `tsn` è `SOILT1` dove `SNOWC > 0,9`, mancante altrove (anche con neve sotto 0,9): CV-A116 (→ "≈ 29 mm"
  non trovato, si omette), MV-A149, MV-A150 (→ DV #24); assente in 7 dei 34 istanti (estate).

### 7.4 Vegetazione e suolo: le tabelle di traduzione
- `cvl`, `cvh` = somme della copertura frazionaria sulle classi basse e alte: CV-A135, MV-A106.
- `tvl`, `tvh`: classe dominante tradotta nella tabella WMO 4.234 (non "tabella ECMWF", DV online);
  tabella CV-T012 (CV-A244..A258); definizioni IGBP della copertura arborea (Sulla-Menashe e Friedl 2022,
  Tab. 3). "Ogni riga è un'identità semantica" (CV-A259) → attestata solo per 5→18: riformulare.
- Arbusteti: `tvl` mancante su 124 672 celle, 16,02 % delle 778 381 con `cvl > 0` (misura DV, sostituisce
  15,8 % e 16,2 %): CV-A120, CV-A121, CV-A257, CV-A260, CV-A261.
- Classi 11 e 14 assenti dal dominio: CV-A253, CV-A255, CV-A262.
- `slt`: soglie FAO di argilla e sabbia applicate alle frazioni del file statico; tabella CV-T013
  (CV-E008..E012); conteggi per tipo sui 1 304 109 punti di terra (CV-N098..N102, confermati sui dati),
  tipi 3 e 7 assenti. Le soglie di "medium fine" e "very fine" non hanno fonte esterna (DV online):
  si dice. eccodes decodifica `slt` sulla tabella WMO 4.213 a 11 classi: CV-A140.
- `cl`, `dl`: `cl` porta 19 309 laghi sottogriglia su celle di terra (CV-A143); `dl` è `LAKE_DEPTH`
  del file statico, non uno stato del modello, default 10 m sul 99,56 % del dominio e su 79 464 delle
  88 785 celle di lago (CV-A103..A106, confermato sui dati); CV-A107 (ERA5 "fa lo stesso") → non trovata, si esclude.

### 7.5 Albedo, orografia
- `al` è un valore tabellare a due stagioni per categoria dominante: 8–11 valori, cambia su 1 171 937
  punti di terra (89,9 %) tra WINTER (novembre–marzo) e SUMMER (aprile–ottobre); 0,08 sull'acqua,
  0,65 sul ghiaccio: KP-A311..A320, CV-A080..A086, KP-N131. MV-A151 ("fondo con cui è stato
  inizializzato") → contraddetta.
- `fal` rapporto effettivo, solo di giorno (sopra 50 W/m²): CV-A087, CV-A117, MV-A152, MV-A153.
- `slor` pendenza del terreno risolto, `sdor` grandezza ERA5 su cella di 3 km (rapporto delle mediane
  0,244 = (3/31)^0,605): KP-A321..A325, CV-A038..A042. "Parametro dello schema di form-drag" → non attestato.
- `z` di superficie: CV-A227.

## Capitolo 8 – Limiti della corrispondenza (`08-limiti.tex`)

Solo ciò che riguarda lo schema ERA5 e questi wrfout. Tabella: parametro ERA5, motivo, se il limite è
la fisica o il flusso di output.

- Il limite è il flusso di output, non la fisica: `blh` (YSU la diagnostica, `PBLH` non scritto),
  flussi sensibile e latente (`isfflx=1`), `skt` come variabile del modello: MV-A080..A082, MV-A086, MV-A093.
  `blh` con Richardson bulk non si pubblica perché la diagnosi sarebbe nostra (MV-A094 contraddetta).
  Ricostruire i flussi dal bilancio non si può: mancano `HFX`, `LH` e il flusso nel suolo (MV-A085 → tre incognite).
- Il limite è la configurazione: TKE (YSU, `KM_OPT=4`): MV-A064, CV-A123; `mx2t`/`mn2t`
  (`output_diagnostics=0`): MV-A089..A091; onde, correnti, SSH (`SF_OCEAN_PHYSICS=0`, nessun modello
  d'onda): MV-A067, MV-A071, CV-A124; spessore del ghiaccio, neve sul ghiaccio, albedo del ghiaccio
  (ghiaccio solo come flag binario in ingresso, albedo 0,65): MV-A073, MV-A075 (→ DV).
- Scelte di pubblicazione: `10efg`/`10nfg` (MV-A061, MV-A063), `lai_lv`/`lai_hv` (CV-A126..A128,
  KP-A335..A338), `anor`/`isor` (CV-A129, MV-A111, MV-A112), snowmelt `ACSNOM` non monotono
  (MV-A077, -7,26 mm; 15 giorni su 16, fino a 8,2 mm, DV #35).
- Campi presenti ma identicamente nulli: MV-A042, MV-A043 (elenco), CV-A125; `ACHFX`/`ACLHF` sono
  accumulatori Noah in una run RUC (MV-A083).
- Campi vivi non pubblicati di cui esiste un parametro ECMWF non pubblicato da ERA5: tabella KP-T014,
  KP-A326..A331, KP-N135.
- Le vie esterne (ERA5 waves a 0,36°, CMEMS) **si escludono**: sono indicazioni per l'utente, non
  contenuto dell'archivio (MV-A068, MV-A072, MV-A074). Da decidere (vedi Domande).

## Capitolo 9 – Conclusioni (`09-conclusioni.tex`)

Solo se l'utente lo vuole. Contenuto: la tabella delle 19 proprietà che cambiano l'uso dei dati
(KP-T001, con i numeri corretti), senza prosa di sintesi. In alternativa la tabella va in appendice
e il capitolo non esiste.

## Appendici

- A. Tabella completa delle 90 variabili (CV-T005..T011), con shortName, paramId, unità, livello,
  campionamento, maschera.
- B. Metodo di verifica: campione di 34 istanti su due anni e quattro stagioni, confronto con ERA5
  dopo aggregazione sulla griglia ERA5 (KP-A010, KP-A011, KP-N001); solo la descrizione, senza file interni.

---

## Duplicazioni eliminate

Ogni argomento sta in una sezione sola; le altre occorrenze diventano `\cref`.

| argomento | occorrenze | sezione |
|---|---|---|
| inversione di `skt` e emissività | CV §4, MV §4-§5, KP §1.3, §2.3 | 5.2 |
| `10fg` e finestra | CV §3-§4, MV §4-§5, KP §5.1-5.2 | 6 (codifica in 2.4) |
| clamping sotto il terreno | CV §4, KP §3.2, §4.1 | 4.2 |
| maschere e regola di mascheratura | CV §5, KP §7.1, MV §5 | 3.2 |
| mare / acque interne | CV §5, KP §7.1 | 3.2 |
| `lsm` orario | CV §4, §7, MV §5, KP §7.1 | 3.3 |
| `al` | CV §4, MV §5, KP §7.1, §8.2 | 7.5 |
| `mucin` | CV §5, MV §5, KP §7.2 | 4.5 |
| deflusso | MV §5, KP §6.1 | 7.1 |
| `tcw` e graupel | MV §5, KP §6.2, §8.4 | 4.4 |
| onda corta e aerosol | CV §4, KP §1.1 | 5.1 |
| nubi | CV §4, KP §1.2, MV §5 | 4.4 |
| `fsr`, `zust` | CV §4, KP §2.1-2.2, §5.1 | 5.3 |
| `slor`, `sdor` | CV §4, MV §5, KP §8.3 | 7.5 |
| suolo come integrali | CV §6, §8, MV §4 | 7.2 |
| `cvl`/`cvh`, 90,1 % e 17,93 % | CV §6, MV §4 | 1.3 e 7.4 (numeri solo in 1.3) |
| `lai` | CV §6, MV §4, KP §8.4 | 8 |
| `generatingProcessIdentifier` | CV §3, KP §8.1 | 2.4 |
| geo_em e accordo 100 % | CV §8, MV §3 | 1.3 |

## Contraddizioni

Tra file e dentro lo stesso file, con la risoluzione presa dalla verifica (DV). Servono solo a
scegliere il dato: **il report scrive il dato risolto e non nomina mai la contraddizione, la
correzione o il valore superato** (decisione dell'utente, 2026-09-29). Le due aperte (10 e 11) sono
chiuse come proposto: valori orari di `zust` esclusi, deflusso con i soli valori della tabella.

1. Errore di `skt` sull'acqua: 0,0005 K (CV, KP, MV §4) contro 0,005 K (MV §5) → 0,0005 K (#55).
2. Emissività sotto la neve: ricostruita e misurata (CV, KP) contro "non ricostruibile, ~0,8 K" (MV §5) → ricostruita (#28, #55).
3. Correzione mescolanza → specifico: 0,8 % in mediana (MV) contro 0,011 % / 1,44 % / 2,26 % → la seconda (#41).
4. Land use: "solo categoria dominante" (MV §1) contro frazioni consegnate (MV §3, CV) → frazioni.
5. `blh` via Richardson: "stessa classe della diagnostica del modello" (MV) contro regola di pubblicazione → non pubblicabile (#18, #29).
6. CAPE indefinita su "pochi percento" (MV) contro 34 % misurato; zeri di `mucape` 46–69 % (#54).
7. `mucin` a zero (MV) contro bitmap (CV, KP) → bitmap (#54).
8. `generatingProcessIdentifier=128` come marcatore (CV §3) contro "non distingue niente" (KP §8.1) → KP (#53).
9. `fsr` sul mare: medie 0,0089 contro 0,0103 m (rapporto delle medie 0,85–0,88) e colonna "1,5–1,9" (KP-S011) → non è una contraddizione: 1,5–1,9 è il rapporto delle mediane (#56). Si pubblicano entrambe le colonne.
10. `zust` sulla terra: 1,62–2,06 sul campione contro 1,06–1,13 (00Z) e 1,40–1,75 (12Z) "per ora" (KP-S012). Chiusa: i valori orari vengono dalle righe del report di confronto, che fino al 2026-09-29 calcolava la media dei rapporti invece del rapporto delle medie. Si escludono i valori orari salvo rimisura.
11. Deflusso: "da quattro a otto ordini di grandezza" e "`ro` = `sro` a quattro cifre significative" (KP §6.1, MV §5) contro la tabella (2,347e-5 / 2,7e-8 ≈ tre ordini; 2,347 contro 2,350 differiscono alla quarta cifra) (KP-S036, S037). Chiusa: si pubblicano i valori della tabella e non le due frasi.
12. Quota del livello modello più basso: 22 m, ~25 m, 24–27 m (KP) → 24–27 m; 22 m è l'intervallo 2 m → livello più basso.
13. `al` "si muove con `lsm`" (CV r.79) contro cambio stagionale (CV r.111-116, KP §8.2), e "non si muove nel giorno" (KP §8.2) contro "segue il modello ora per ora" (KP §7.1) → tabella stagionale fissa nel giorno, più i punti di ghiaccio che seguono la maschera oraria.
14. `tvl`/`tvh`/`slt` cambiano col ghiaccio (MV §5) contro statici dal file statico (CV) → statici.
15. Maschera del suolo "sull'acqua" (CV §8) contro "terra permanente" (CV §5, KP §7.1) → terra permanente (#38).
16. Maschera arbusteti 15,8 % (CV r.157) contro 16,2 % (CV r.387) → 16,02 % delle celle con `cvl > 0` (misura).
17. Onde ERA5 a ~31 km (MV) contro 0,36° (~40 km, documentazione ERA5).
18. Dimensioni: ~747 MB / 17,9 GB / 6,6 TB (CV) contro ~0,8 GB / 7,0 TB (MV) → misure 2026-09-29 (vedi 2.1).
19. Proiezione a 29 livelli: 1,45 GB/ora contro 18,1 TB/anno (1,45 × 8760 = 12,7 TB) (MV-S005).
20. Errore di derivazione "trenta volte" più piccolo del bias (CV, KP) contro i numeri (1,64 / 0,119 ≈ 14) → "più di dieci volte".
21. Soglia della regola della neve: nelle schede 1,5 % (CV §4) e "applicata un po' prima della transizione del modello" (KP §2.3, vaga) → 1,5 %, la frase vaga si omette.
22. Spostamento di `skt` per il cambio di soglia: "circa 0,05 K RMSE" (KP) contro #55: 0,05 K è il livello dell'RMSE (0,05766 → 0,05384 K), il cambio vale ~0,004 K → non si riporta, è storia del prodotto.
23. "Ogni riga della tabella MODIS → 4.234 è un'identità semantica" (CV, MV) → attestato solo per 5 → 18: si riformula.
24. `tcw` e graupel: "ERA5 non ha un parametro" (KP §6.2 corpo) contro "ECMWF definisce `grle` e `tcolg`, ERA5 non li pubblica" (KP §8.4, MV §5) → la seconda.

## Glossario (forme fissate)

| termine | forma fissata nel report | definizione |
|---|---|---|
| CHAPTER | downscaling dinamico a convezione esplicita di ERA5 (EN: convection-permitting dynamical downscaling of ERA5), mai "rianalisi" | il prodotto di WRF descritto da Bernini et al. 2025 |
| archivio | archivio GRIB2 CHAPTER | l'insieme dei file orari GRIB2 a 246 messaggi |
| file orario | file orario | un file GRIB2 per istante di validità |
| messaggio | messaggio GRIB | un campo su un livello |
| output del modello | file wrfout | l'output orario di WRF da cui si parte |
| file statico | file statico `geo_em.d02` | il file statico WPS della run |
| istante di validità | istante di validità | `validityDate`/`validityTime` |
| tempo di riferimento | tempo di riferimento | `dataDate`/`dataTime` |
| campo istantaneo | campo istantaneo | template di prodotto 4.0 |
| campo accumulato | campo accumulato (sull'ora che termina all'istante di validità) | template 4.8, tempo di riferimento H−1, intervallo 0–1 |
| intervallo di accumulazione | intervallo di accumulazione | `stepRange` 0–1 |
| run giornaliera | run giornaliera, run partita alle 18 UTC di D−1 | 30 h; le prime 6 h di spin-up non pubblicate |
| spin-up | spin-up | le prime 6 h di una run |
| cambio di run | cambio di run | il passaggio fra le 00 UTC (run di D−2, trentesima ora) e le 01 UTC (run di D−1, settima ora) |
| campo statico | campo statico | identico in ogni file orario |
| terra permanente | terra permanente | maschera di terra del file statico, fissa |
| maschera oraria | maschera terra–mare oraria (`lsm`) | `LANDMASK` di WRF, cresce col ghiaccio |
| punto mancante | punto mancante (bitmap) | mai uno zero |
| regola di pubblicazione | regola di pubblicazione | nome ERA5 solo se la grandezza è quella, o la differenza sta in una riga |
| regola di mascheratura | regola di mascheratura | mancante dove il parametro ERA5 non è definito |
| livello di pressione | livello di pressione | uno dei 13 livelli isobarici |
| livello del modello | livello del modello | livello verticale nativo di WRF |
| clamping | clamping | valore del livello del modello più basso ripetuto sotto il terreno |
| rapporto di mescolanza | rapporto di mescolanza | per kg di aria secca (WRF) |
| contenuto specifico | contenuto specifico | per kg di aria umida (ECMWF) |
| fase mista | umidità relativa sulla fase mista | saturazione IFS Cy41r2, ghiaccio sotto 250,16 K, acqua sopra 273,16 K |
| temperatura di pelle | temperatura di pelle (`skt`) | ricostruita da `LWUPB` |
| emissività | emissività di categoria | ε misurata per categoria di uso del suolo |
| soglia di copertura nevosa | soglia di copertura nevosa | 1,5 %, unico parametro libero |
| vento risolto | vento risolto | vento a 10 m del modello, senza parametrizzazione di raffica |
| raffica parametrizzata | raffica parametrizzata | `10fg`/`i10fg` di ERA5 |
| componente connessa | componente connessa | insieme di celle d'acqua contigue |
| campo nullo | campo identicamente nullo | nullo in tutti gli istanti campionati (non "campo morto") |
| campione di verifica | campione di verifica | 34 istanti: 4 del 2019, 26 del 2024 (tutti i mesi), 4 del 2025 |
| rapporto delle medie / delle mediane | rapporto delle medie, rapporto delle mediane | mai "rapporto" da solo |
| categoria dominante | categoria dominante | classe di uso del suolo con la frazione maggiore |

## Riferimenti (candidati per `bib/riferimenti.bib`)

Verificati online (DV, verifica 2):
- Tegen et al. (1997), J. Geophys. Res. 102(D20), 23895–23915, doi:10.1029/97JD01864.
- ECMWF (2016), IFS Documentation Cy41r2, Part IV: Physical Processes (cap. 3.10.4, eq. 3.99; cap. 7, eq. 7.5, 7.6, 7.89, 7.90).
- WMO-No. 8 (2023), Guide to Instruments and Methods of Observation, Vol. I, cap. 4, All. 4.A.
- Sulla-Menashe e Friedl (2022), User Guide to Collection 6 MODIS Land Cover (MCD12Q1/MCD12C1), C6.1.
- FAO/IIASA/ISRIC/ISSCAS/JRC (2012), Harmonized World Soil Database v1.2.
- Balsamo et al. (2009), J. Hydrometeorol. 10(3), 623–643, doi:10.1175/2008JHM1068.1 (solo se si cita la tessitura dei suoli IFS).
- ERA5: data documentation (Copernicus Knowledge Base), per i 37 livelli e la risoluzione.
- ECMWF Parameter Database (paramId citati).
- WRF v4.1.1 (codice, `VEGPARM.TBL`, `README.namelist`).
Non presenti nelle schede e **non aggiunti**: l'articolo di riferimento di ERA5 e la nota tecnica WRF;
vanno aggiunti solo se li indichi tu.

Issue citabili (parlano del contenuto o della codifica dei GRIB): #34, #36, #37, #38, #39, #40, #41,
#42, #44, #45, #46, #47, #48, #49, #50, #51, #52, #53, #54, #55, #56, #57. Non citabili: pipeline e
infrastruttura (#1–#10, #32, #59–#66), processo di audit (#11–#18, #27–#31, #33).

## Decisioni prese (2026-09-29)

1. Niente sezione sul vecchio archivio GRIB1: il report descrive solo l'archivio GRIB2 attuale.
   Ogni confronto con il GRIB1 (MV-A172, MV-A173, MV-A178, KP-A308) resta fuori.
2. Livelli (2.3): 13 livelli di pressione, **scelti perché richiesti dal progetto LAM AI** (unica
   menzione del progetto consentita); sottoinsieme dei 37 livelli ERA5; gli 8 sopra 50 hPa non si
   possono produrre. Nessuna proiezione a 29 livelli.
3. Cap. 8: solo il motivo per cui un parametro manca, nessun prodotto esterno.
4. Cap. 9: capitolo finale con la sola tabella delle 19 proprietà, con rimandi alle sezioni.
5. Soglia della componente connessa (3.2): **2000 celle**, verificata sul file statico il 2026-09-29:
   902 855 celle di mare; componenti d'acqua 844 431, 49 841, 8 583, poi 1 225; ogni soglia tra
   1 226 e 8 583 dà lo stesso mare (margine di un fattore sette).
6. Issue citabili: le 22 dell'elenco sopra.
7. Contraddizioni: si scrive solo il dato risolto (regola 9 di `stile.md`).

## Misure del 2026-10-14 (#71, #72), fonti

- Cambio di run (cap. 2, sec:cambio-run, tab:cambio-run): `docs/audit/f5-water-cycle.md`, sezione
  "The whole 00Z from the previous day's run", script `tools/audit/run_switch.py`, 2024-01-18/19.
- Livello di 50 hPa (cap. 4, sec:livello-50): `docs/audit/f1-pressure-levels.md`, sezione "50 hPa is
  the highest model level, copied", script `tools/audit/f1_top_level.py`, 2024-01-19 00 UTC; 5,4 % =
  227/(4009+227); 25 m = 239 − 214.
- Deflussi orari (cap. 7, tab:deflusso, otto istanti): `docs/audit/f5-water-cycle.md`, sezione "The
  runoff triplet, hourly"; sostituiscono KP-T010 e KP-N101..N104, misurati sullo schema 0–H.
- Schema temporale (cap. 1 e 2): issue #70, #71, #72.
