# Scheda: CHAPTER_VARIABLES.md
Fonte: /leonardo/home/userexternal/lmonaco0/CHAPTER/CHAPTER_VARIABLES.md (421 righe), letta il 2026-09-29

Convenzione sezioni: §0 = preambolo (r.1-23); §1-§8 = sezioni numerate del file; §7.PL = Pressure levels, §7.HAG = Height above ground, §7.MSL = Mean sea level, §7.COL = Total column, §7.SFC = Surface / single level, §7.LAKE = Entire lake, §7.TOA = Top of atmosphere / most unstable parcel; §8.tv = `tvl`/`tvh`, §8.slt = `slt`, §8.soil = `swvl1-4`/`stl1-4`.

## 1. Affermazioni

### §0 Preambolo
A001 Archivio: 90 variabili, 246 messaggi GRIB per file orario [SUPPORTATA: registro `wrf_era5_comparison.WRF_TO_ECMWF_PARAMID`] (§0, r.3)
A002 Contenuto preso dal registro del convertitore (`wrf_era5_comparison.WRF_TO_ECMWF_PARAMID`), usato dalla pipeline e dal suo sanity check [SUPPORTATA: `wrf_era5_comparison.WRF_TO_ECMWF_PARAMID`] (§0, r.3-5)
A003 Il documento descrive ciò che è effettivamente scritto [SUPPORTATA: registro del convertitore] (§0, r.5)
A004 Documento aggiornato il 2026-09-18, quando il file statico WPS `geo_em.d02` è stato recuperato da LRZ [SENZA FONTE] (§0, r.7-8)
A005 `geo_em.d02` era stato registrato come perso [SENZA FONTE] (§0, r.8)
A006 `geo_em.d02` porta la copertura del suolo FRAZIONARIA, la tessitura del suolo e i dati dei laghi che l'output orario aveva ridotto a una sola categoria dominante per cella [SUPPORTATA: `geo_em.d02`] (§0, r.8-10)
A007 `geo_em.d02` ha aggiunto quindici campi: `cvl`, `cvh`, `tvl`, `tvh`, `slt`, `cl`, `dl` e gli otto strati di suolo ERA5 [SUPPORTATA: `geo_em.d02`] (§0, r.10-11)
A008 Nulla è stato rimosso [SENZA FONTE] (§0, r.11)
A009 Ogni campo è uno che si può difendere riga per riga [SENZA FONTE] (§0, r.13)
A010 Dove la grandezza WRF non è esattamente quella ERA5, è detto sotto invece di nasconderlo [SENZA FONTE] (§0, r.13-15)
A011 Dove non si poteva far corrispondere affatto, il campo è stato scartato invece di pubblicarlo sotto un nome fuorviante (vedi §6) [SENZA FONTE] (§0, r.15-16)
A012 `MISSING_VARIABLES.md` dice cosa non c'è e perché [SUPPORTATA: `MISSING_VARIABLES.md`] (§0, r.19)
A013 `CHAPTER_KNOWN_PROPERTIES.md` enuncia proprietà note e bias di ciò che c'è, ciascuno col numero misurato; da leggere prima di confrontare l'archivio con ERA5 o con osservazioni [SUPPORTATA: `CHAPTER_KNOWN_PROPERTIES.md`] (§0, r.20-23)

### §1 What the files are
A014 Modello WRF 4.1.1, dominio d02 [SENZA FONTE] (§1, r.29)
A015 Griglia orizzontale Mercator [SENZA FONTE] (§1, r.30)
A016 Forma della Terra: sfera (`shapeOfTheEarth=1`), la sfera propria di WRF, dichiarata esplicitamente [SUPPORTATA: chiave GRIB `shapeOfTheEarth=1`] (§1, r.32)
A017 Edizione GRIB2, grid definition template 3.10 (Mercator), centro di origine `ecmf` [SUPPORTATA: chiavi GRIB citate] (§1, r.33)
A018 Packing `grid_ccsds`; i campi mascherati portano una bitmap GRIB propria [SUPPORTATA: chiave GRIB `grid_ccsds`] (§1, r.34)
A019 Identità dei parametri ECMWF paramId / shortName ovunque, quindi l'archivio è direttamente confrontabile con ERA5 [SENZA FONTE] (§1, r.35)
A020 Un file per ora; dimensione "misurata, non stimata" [SENZA FONTE] (§1, r.36)
A021 Nome file `ailam-an-cima-3km-{year}-{year}-1h-v1-{YYYYMMDD}{HH}.grib` [SENZA FONTE] (§1, r.37)
A022 Periodo: 2019, 2024 e 2025-01-01 → 2025-07-02, orario; 2020–2023 da seguire [SENZA FONTE] (§1, r.38)
A023 La fine 2025 è dove si ferma la run WRF stessa: uno scan `mmlsattr` di tutto il 2025 sulla sorgente (2026-09-29) trova un blocco contiguo che termina 2025-07-02T23 e niente dopo [SUPPORTATA: scan `mmlsattr` 2026-09-29] (§1, r.38)

### §2 Vertical levels
A024 13 livelli di pressione, gli stessi per ogni variabile 3-D [SUPPORTATA: registro] (§2, r.42-44)
A025 Sono l'insieme ERA5 troncato al top del modello [SENZA FONTE] (§2, r.46)
A026 Gli 8 livelli ERA5 sopra 50 hPa sono sopra `P_TOP` di WRF e non possono essere prodotti [SUPPORTATA: `P_TOP`] (§2, r.46-47)
A027 I campi a singolo livello stanno su `surface`, `heightAboveGround` (2, 10, 100, 200 m), `meanSea`, `entireAtmosphere` (integrali di colonna) o, per il bilancio radiativo al top dell'atmosfera, `nominalTop` [SENZA FONTE] (§2, r.47-49)

### §3 Time convention
A028 Campi istantanei: product definition template 0; `dataDate`/`dataTime` sono il tempo valido [SENZA FONTE] (§3, r.53-54)
A029 Campi accumulati (`tp`, `tirf`, `sf`, `sro`, `ssro`, `ro` e tutto il bilancio radiativo) usano template 8, come richiesto dalle loro definizioni ECMWF [SUPPORTATA: definizioni ECMWF] (§3, r.55-57)
A030 Accumulati da 00 UTC dello stesso giorno: tempo di riferimento 00 UTC, step `0–H` [SENZA FONTE] (§3, r.56-58)
A031 Sono esattamente zero nel file delle 00 UTC [SENZA FONTE] (§3, r.57-58)
A032 `10fg` è l'unica eccezione: massimo sull'ora precedente (tempo di riferimento H−1, step `0–1`) [SENZA FONTE] (§3, r.59-60)
A033 `10fg` è il massimo del vento a 10 m *risolto*, non una parametrizzazione di raffica [SENZA FONTE] (§3, r.60-61)
A034 Un file mescola tempi di riferimento di proposito [SENZA FONTE] (§3, r.62)
A035 Indicizzare sulla validità (`validityDate`/`validityTime`), mai su `dataTime` [SENZA FONTE] (§3, r.62-63)
A036 I messaggi accumulati portano `generatingProcessIdentifier = 128` come marcatore del riferimento 00 UTC [SENZA FONTE] (§3, r.64-65)

### §4 Declared approximations
A037 Quattro campi non sono esattamente il loro omonimo ERA5, e sono pubblicati dicendolo [SENZA FONTE] (§4, r.69)
A038 `slor` per ERA5: pendenza dell'orografia **sottogriglia**, parametro dello schema di form-drag [SENZA FONTE] (§4, r.73)
A039 `slor` scritto: pendenza del terreno **risolto** a 3 km, `|grad z|` [SENZA FONTE] (§4, r.73)
A040 eccodes mostra il nome proprio del parametro, *Slope of sub-gridscale orography*, quindi nulla nel messaggio stesso dice che è la pendenza risolta [SUPPORTATA: eccodes] (§4, r.73)
A041 `sdor` **è** la grandezza ERA5, solo valutata su una cella di 3 km invece che di 31 km [SENZA FONTE] (§4, r.73)
A042 Rapporto misurato delle mediane di `sdor` 0.244 = (3/31)^0.605: un riscalamento di risoluzione, non una definizione diversa [SENZA FONTE] (§4, r.73)
A043 `10fg` per ERA5: raffica da parametrizzazione (turbolenta + convettiva); scritto: massimo orario del vento a 10 m **risolto** [SENZA FONTE] (§4, r.74)
A044 `iews`, `inss` per ERA5: le componenti di stress del modello; scritto: il modulo `rho u*^2` proiettato sulla direzione del vento a 10 m [SENZA FONTE] (§4, r.75)
A045 `fsr` per ERA5: rugosità **efficace**, che porta la resistenza orografica che l'IFS parametrizza a 31 km [SENZA FONTE] (§4, r.76)
A046 `fsr` scritto: `ZNT` **locale** di WRF, la rugosità da land-use con override della neve [SUPPORTATA: `ZNT`] (§4, r.76)
A047 `fsr` su terra: 0.32–0.48 di quello ERA5 in mediana [SENZA FONTE] (§4, r.76)
A048 `fsr` su mare: WRF ed ERA5 concordano, entrambi Charnock [SENZA FONTE] (§4, r.76)
A049 `zust` è la velocità di attrito del modello stesso; 1.6–2.1× ERA5 su terra (1.1× su mare) [SENZA FONTE] (§4, r.76)
A050 `zust` e `fsr` sono le due metà della stessa storia, perché a 3 km il vento guidato dal terreno è risolto e non smussato [SENZA FONTE] (§4, r.76)
A051 `lsm` per ERA5: maschera terra-mare **permanente**; ghiaccio marino portato separatamente in `ci` [SENZA FONTE] (§4, r.77)
A052 `lsm` scritto: `LANDMASK` di WRF, che riclassifica i punti di ghiaccio marino come terra, quindi la maschera **cresce in inverno** [SUPPORTATA: `LANDMASK`] (§4, r.77)
A053 `lsm & ~(ci > 0)` recupera esattamente il senso ERA5; `ci` è pubblicato [SENZA FONTE] (§4, r.77)
A054 `lsm` è ora l'**unico** campo che segue il modello ora per ora (con `al`, che si muove con esso) [SENZA FONTE] (§4, r.79)
A055 Le colonne di suolo seguivano anch'esse il modello ora per ora, e non più [SENZA FONTE] (§4, r.79)
A056 Sotto nuovo ghiaccio marino lo schema fa crescere una colonna che non è suolo: `swvl` raggiungeva esattamente 1.000 contro la porosità 0.435 del suo tipo di suolo [SENZA FONTE] (§4, r.79)
A057 Dal 2026-09-25 le colonne di suolo sono mascherate sulla terra **permanente** del file statico, come fa ERA5 [SENZA FONTE] (§4, r.79)
A058 Nulla è perso che non si possa recuperare: `ci` è pubblicato [SENZA FONTE] (§4, r.79)
A059 "Tre altri" meritano una nota invece di un avvertimento [SENZA FONTE] (§4, r.81)
A060 `skt` non è un output del modello qui (`TSK` non è stato scritto) [SUPPORTATA: `TSK` assente dall'output] (§4, r.83)
A061 `skt` è invertito dall'onda lunga ascendente, `LWUPB = eps sigma T^4 + (1-eps) LWDN` [SUPPORTATA: `LWUPB`] (§4, r.83-84)
A062 L'emissività non è assunta: è stata **letta dalla run stessa** [SENZA FONTE] (§4, r.84-85)
A063 Lo schema radiativo calcola una diagnostica clear-sky con la stessa emissività e la stessa temperatura di pelle, cambiando solo il flusso discendente [SENZA FONTE] (§4, r.85-87)
A064 Le due equazioni insieme eliminano la temperatura incognita e lasciano `eps = 1 - (LWUPB - LWUPBC)/(LWDN - LWDNC)` [SUPPORTATA: `LWUPB`, `LWUPBC`, `LWDN`, `LWDNC`] (§4, r.87-88)
A065 È un'identità, non un fit [SENZA FONTE] (§4, r.88)
A066 Misurata così, l'emissività è risultata identica in ogni cella di una data categoria di land-use (spread 0.0000 a quattro decimali) [SENZA FONTE] (§4, r.88-90)
A067 Il controllo è esatto: su acqua aperta, dove la temperatura di pelle del modello È la SST, restituisce 0.98000 [SENZA FONTE] (§4, r.90-91)
A068 L'accuratezza è stagionale, e contano entrambi i numeri [SENZA FONTE] (§4, r.93)
A069 La ricostruzione riproduce l'emissività del modello a 1e-4 sul 99.98 % dei punti di terra a luglio e sul 93.05 % a gennaio [SENZA FONTE] (§4, r.93-94)
A070 Errore `skt` su terra: 0.0012 K RMSE a luglio contro 0.084–0.119 K a gennaio e febbraio (p99 0.81 K, punto peggiore 2.79 K) [SENZA FONTE] (§4, r.95-96)
A071 Tutta quella dispersione è la regola della neve [SENZA FONTE] (§4, r.96)
A072 La neve alza l'emissività a 0.98 piatta in ogni categoria, applicata da 1.5 % di copertura nevosa in su, con un blend sotto [SENZA FONTE] (§4, r.96-98)
A073 Quella soglia è l'unica quantità della derivazione scelta anziché letta dalla run [SENZA FONTE] (§4, r.98-99)
A074 La soglia è stata misurata: sweep su tutti i 34 timestep campione contro l'emissività effettivamente usata dal modello; 1.5 % è il minimo dell'errore di temperatura di pelle risultante [SUPPORTATA: sweep su 34 timestep campione] (§4, r.99-101)
A075 Su acqua aperta, dove la risposta è nota indipendentemente, recupera la SST a 0.0005 K RMSE su circa 910 000 punti a ogni timestep di ogni stagione [SUPPORTATA: misura su ~910 000 punti di acqua aperta] (§4, r.101-103)
A076 L'errore di derivazione è trenta volte più piccolo del bias freddo fisico della pelle su terra [SENZA FONTE] (§4, r.103-105)
A077 `skt` su terra circa 1.6 K sotto ERA5, fino a 3.2 K a mezzogiorno; su mare esatta (+0.01 K) [SENZA FONTE] (§4, r.105-106)
A078 Quello è la run, non la derivazione; il numero su mare è il controllo che lo prova [SENZA FONTE] (§4, r.106-107)
A079 Riconciliarlo con lo shortwave in eccesso e le nuvole mancanti richiederebbe il bilancio energetico di superficie; `HFX`, `LH` e il flusso di calore al suolo sono i tre campi che l'archivio non ha [SENZA FONTE] (§4, r.107-109)
A080 `al` è un valore tabellare a due stagioni, non un campo [SENZA FONTE] (§4, r.111)
A081 Nessuna albedo satellitare mensile usata (`usemonalb = .false.`) [SUPPORTATA: `usemonalb = .false.`] (§4, r.111-112)
A082 Il fondo senza neve viene dalle colonne WINTER e SUMMER della tabella di land-use per categoria dominante [SUPPORTATA: tabella di land-use, colonne WINTER/SUMMER] (§4, r.112-113)
A083 `al` prende solo 8-11 valori distinti su tutto il dominio [SENZA FONTE] (§4, r.113-114)
A084 `al` cambia a 1 171 937 punti di terra (89.9 % della maschera di terra) al confine stagionale, che è aprile e novembre, non una transizione fisica [SENZA FONTE] (§4, r.114-116)
A085 Fuori terra `al` vale 0.08 su acqua e 0.65 su ghiaccio marino [SENZA FONTE] (§4, r.116)
A086 Non leggere `al` come albedo osservata o evolutiva; non differenziarla attraverso il confine aspettandosi un segnale [SENZA FONTE] (§4, r.116-117)
A087 `fal` è il rapporto effettivo usato dalla simulazione ed evolve [SENZA FONTE] (§4, r.117-118)
A088 Lo shortwave in superficie porta un bias alto sistematico [SENZA FONTE] (§4, r.119)
A089 RRTMG girò con una climatologia dell'ozono e **nessun aerosol** (`aer_opt = 0`) [SUPPORTATA: `aer_opt = 0`] (§4, r.119-120)
A090 ERA5 porta la climatologia aerosol Tegen [SENZA FONTE] (§4, r.121)
A091 Su questo dominio uno spessore ottico da 0.1 a 0.2 spiega l'entità del bias [SENZA FONTE] (§4, r.121-122)
A092 Misurato contro ERA5: +8.5 % in cielo sereno (`ssrdc`) e +13.6 % all-sky (`ssrd`) [SENZA FONTE] (§4, r.122)
A093 I campi termici non sono toccati e concordano entro 1.1 %: il controllo che rende credibile l'attribuzione [SENZA FONTE] (§4, r.123-124)
A094 Copertura nuvolosa totale 22 % sotto ERA5, nuvole alte 39 % sotto, il che spinge la solare in superficie nello stesso verso [SENZA FONTE] (§4, r.124-125)
A095 Entrambi sono proprietà della run e non si possono rimuovere a posteriori; con gli altri bias misurati sono enunciati in `CHAPTER_KNOWN_PROPERTIES.md` [SUPPORTATA: `CHAPTER_KNOWN_PROPERTIES.md`] (§4, r.125-127)
A096 Sotto il suolo i livelli di pressione sono clampati, non estrapolati [SENZA FONTE] (§4, r.128)
A097 Dove un livello è sotto il terreno, l'archivio ripete il valore del livello modello più basso verbatim — combaciante a 0.0 per `t`, 1e-9 per `q` [SENZA FONTE] (§4, r.128-130)
A098 È uno stato reale del modello da circa 24 a 27 m sopra il suolo, non aria sintetica, e mantiene coerente la giunzione in superficie [SENZA FONTE] (§4, r.130-131)
A099 ERA5 estrapola lì con un lapse rate, quindi i due archivi differiscono di convenzione proprio dove 1000 hPa è sotto terra, cioè la maggior parte della terra [SENZA FONTE] (§4, r.132-133)
A100 Il nostro `z` a 1000 hPa sta allora a una mediana di 24-27 m *sopra* il terreno sotto cui `sp` lo mette, sul 47.6 % del dominio a 1000 hPa e sul 9 % a 925 [SENZA FONTE] (§4, r.133-135)
A101 Mascherare i livelli contro `sp` per un confronto pulito; ogni campo necessario è nello stesso file [SENZA FONTE] (§4, r.135-136)
A102 `sst` è costante in ogni run di 24 h (`SST_UPDATE=0`), reinizializzata giornalmente [SUPPORTATA: `SST_UPDATE=0`] (§4, r.137)
A103 `dl` è il database di profondità dei laghi con cui la run è stata costruita, non uno stato del modello [SENZA FONTE] (§4, r.138-139)
A104 Fisica dei laghi spenta (`sf_lake_physics=0`): niente nella simulazione risponde a `dl` [SUPPORTATA: `sf_lake_physics=0`] (§4, r.139-140)
A105 `dl` pubblicato come dataset al contorno, mascherato fuori lago [SENZA FONTE] (§4, r.140-141)
A106 Il campo grezzo è il default WPS di 10 m sul 99.56 % del dominio, e 79 464 delle 88 785 celle di lago portano lo stesso default [SENZA FONTE] (§4, r.141-142)
A107 Il `dl` di ERA5 fa lo stesso dove il database tace [SENZA FONTE] (§4, r.142)

### §5 Masked fields
A108 I campi mascherati sono scritti con una bitmap GRIB invece di finti zeri: mancante significa mancante [SENZA FONTE] (§5, r.146)
A109 `sst`, `ci`: solo punti di **mare** [SENZA FONTE] (§5, r.150)
A110 Mare non è semplicemente "non terra": la classe di land-use WPS chiama *lago* il Mar Nero, il Mare d'Azov e parte del Baltico, quindi mascherare su quella classe avrebbe cancellato `sst` dal Mar Nero [SUPPORTATA: classe di land-use WPS] (§5, r.150)
A111 Il discriminatore è la dimensione della componente connessa, misurata: 844 431 celle (Atlantico + Mediterraneo + Baltico + Mare del Nord), 49 841 (Mar Nero + Azov), 8 583 (Mar Rosso), poi 1 225 (Vänern, il lago vero più grande) e più piccole; il taglio sta in un gap con un fattore sette di margine [SUPPORTATA: misura sulle componenti d'acqua del dominio] (§5, r.150)
A112 `cl`: zero sul mare invece che mancante, perché un punto di mare genuinamente non ha copertura lacustre [SENZA FONTE] (§5, r.151)
A113 `mucin`: definito nelle colonne dove la routine CAPE restituisce un valore, cioè dove CAPE raggiunge 100 J/kg [SENZA FONTE] (§5, r.152)
A114 Quelle colonne sono dal 4 % al 29 % del dominio, meno in inverno [SENZA FONTE] (§5, r.152)
A115 I buchi di `mucin` sono scritti come mancanti e non zero, perché zero si leggerebbe "nulla inibisce la convezione" proprio nelle colonne dove più la inibisce [SENZA FONTE] (§5, r.152)
A116 `tsn`: celle con copertura nevosa oltre 0.9 (≈ 29 mm di equivalente in acqua); fuori stagione il campo è legittimamente vuoto [SENZA FONTE] (§5, r.153)
A117 `fal`: solo di giorno (shortwave incidente sopra 50 W/m²) [SENZA FONTE] (§5, r.154)
A118 `swvl1-4`, `stl1-4`: la terra **permanente** del file statico, un contorno fisso, lo stesso in ogni file dell'archivio; il ghiaccio marino non porta quindi colonna di suolo, come fa ERA5 [SUPPORTATA: file statico] (§5, r.155)
A119 `slt`: punti di terra del file statico (1 304 109 celle) [SUPPORTATA: file statico] (§5, r.156)
A120 `tvl`: ovunque tranne le celle dove un arbusteto domina la vegetazione bassa (124 672 celle, 15.8 % di quelle con `cvl > 0`) [SENZA FONTE] (§5, r.157)
A121 MODIS non porta fenologia degli arbusti mentre la tabella ECMWF distingue arbusti sempreverdi da decidui; invece di inventarne una il campo è lasciato mancante; `cvl` dà comunque la copertura [SENZA FONTE] (§5, r.157)
A122 `dl`: solo celle di lago (88 785) [SENZA FONTE] (§5, r.158)

### §6 What is not in the archive
A123 Niente TKE e niente altezza dello strato limite (lo schema PBL è YSU, non locale) [SUPPORTATA: schema PBL YSU] (§6, r.162)
A124 Niente onde, correnti, altezza della superficie del mare o spessore del ghiaccio marino (nessun accoppiamento oceano o onde) [SENZA FONTE] (§6, r.162-163)
A125 Niente precipitazione convettiva (`CU_PHYSICS=0`, quindi è identicamente zero e sarebbe un campo morto) [SUPPORTATA: `CU_PHYSICS=0`] (§6, r.163-164)
A126 Leaf area index (`lai_lv`, `lai_hv`) scartato deliberatamente: il modello porta un solo LAI per cella, ERA5 ne vuole uno per classe di vegetazione, definito per unità di area vegetata; ogni split sarebbe una nostra assunzione, quindi nessuno dei due è scritto [SENZA FONTE] (§6, r.168-170)
A127 Il singolo campo LAI è nell'output del modello, vivo, non pubblicato solo per quella ragione; consegnabile col suo nome, `LAI` [SENZA FONTE] (§6, r.170-172)
A128 `rdlai2d = .false.`: LAI è un lookup tabellare sulla categoria dominante e non un'osservazione, seconda ragione per non dividerlo [SUPPORTATA: `rdlai2d = .false.`] (§6, r.172-174)
A129 Angolo e anisotropia dell'orografia sottogriglia (`anor`, `isor`) scartati: il file statico porta i parametri di asimmetria e lunghezza efficace di Kim-Arakawa, che non sono quelli ECMWF, e la differenza non sta in una riga [SENZA FONTE] (§6, r.175-177)
A130 Quattro voci che stavano qui fino al 2026-09-17 sono entrate nell'archivio, perché `geo_em.d02` è tornato e l'obiezione sul suolo aveva una risposta [SENZA FONTE] (§6, r.179-180)
A131 `swvl1-4` / `stl1-4` sono ora le vere medie di strato ERA5 [SENZA FONTE] (§6, r.182)
A132 Lo schema di superficie è uno schema a *livelli*: valori puntuali a 0, 5, 20, 40, 160 e 300 cm con profilo lineare fra loro [SENZA FONTE] (§6, r.182-184)
A133 L'intera colonna ERA5 sta dentro quei nodi (289 cm è sopra il più profondo, 0 cm è il primo), quindi ogni media di strato è l'integrale esatto del profilo del modello e **nulla è estrapolato** [SENZA FONTE] (§6, r.184-186)
A134 L'obiezione era contro lo scrivere i valori puntuali, non contro l'integrarli [SENZA FONTE] (§6, r.186-187)
A135 `cvl` / `cvh` sono somme della copertura frazionaria sulle classi MODIS-IGBP di vegetazione bassa e alta — la stessa grandezza che intende ERA5 [SUPPORTATA: classi MODIS-IGBP] (§6, r.188-189)
A136 La categoria dominante tiene in media solo il 90.1 % di una cella di terra; il 17.9 % delle celle di terra porta sia vegetazione alta sia bassa sopra il 5 % [SENZA FONTE] (§6, r.189-191)
A137 `tvl` / `tvh` sono la classe dominante bassa e alta tradotta nella tabella di codici ECMWF 4.234 con la tabella di §8, dove ogni riga è un'identità semantica [SUPPORTATA: tabella ECMWF 4.234; tabella di §8] (§6, r.192-193)
A138 L'unico punto in cui MODIS non risponde — arbusti sempreverdi contro decidui — è lasciato mancante invece che indovinato [SENZA FONTE] (§6, r.193-194)
A139 `slt` è calcolato con le soglie FAO argilla/sabbia che *definiscono* i sette tipi di suolo ECMWF, applicate alle frazioni di argilla e sabbia del file statico; nessun crosswalk di categorie; la grandezza è quella ERA5 per costruzione [SUPPORTATA: soglie FAO] (§6, r.195-197)
A140 eccodes risolve `slt` alla disciplina 2/3/0, che la tabella WMO 4.213 legge come una lista diversa di 11 valori [SUPPORTATA: eccodes; tabella WMO 4.213] (§6, r.197-199)
A141 L'archivio è semantica ECMWF ovunque, e così questo messaggio [SENZA FONTE] (§6, r.199)
A142 `cl` e `dl` sono arrivati con loro [SENZA FONTE] (§6, r.201)
A143 `cl` non è ridondante con la maschera terra-mare: 19 309 celle che la maschera chiama terra portano un lago sottogriglia, e il modello stesso ha scartato la classe a runtime [SENZA FONTE] (§6, r.201-202)
A144 Il ragionamento completo e le vie per ottenerne una parte sono in `MISSING_VARIABLES.pdf` [SUPPORTATA: `MISSING_VARIABLES.pdf`] (§6, r.204-205)

### §7 The variables — note generali
A145 Descrizioni e unità sono quelle ECMWF; "Time" dice come il campo è campionato [SENZA FONTE] (§7, r.209)
A146 90 righe e 89 shortName distinti, perché `z` è scritto due volte: come geopotenziale sui livelli di pressione e come geopotenziale di superficie (orografia) [SUPPORTATA: registro] (§7, r.209-211)

### §7.PL Pressure levels (13 variabili, 169 messaggi) — fonte di ogni riga: registro `wrf_era5_comparison.WRF_TO_ECMWF_PARAMID` (r.4)
A147 `cc` — paramId 248; "Fraction of cloud cover"; unità (0-1); livelli: 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (sotto terra: clamp, r.128-136) [SUPPORTATA: registro] (§7.PL, r.218)
A148 `ciwc` — paramId 247; "Specific cloud ice water content"; kg/kg; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.219)
A149 `clwc` — paramId 246; "Specific cloud liquid water content"; kg/kg; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.220)
A150 `crwc` — paramId 75; "Specific rain water content"; kg/kg; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.221)
A151 `cswc` — paramId 76; "Specific snow water content"; kg/kg; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.222)
A152 `q` — paramId 133; "Specific humidity"; kg/kg; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp, 1e-9 sotto terra, r.130) [SUPPORTATA: registro] (§7.PL, r.223)
A153 `r` — paramId 157; "Relative humidity"; %; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.224)
A154 `t` — paramId 130; "Temperature"; K; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp, 0.0 sotto terra, r.130) [SUPPORTATA: registro] (§7.PL, r.225)
A155 `u` — paramId 131; "U component of wind"; m/s; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.226)
A156 `v` — paramId 132; "V component of wind"; m/s; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.227)
A157 `w` — paramId 135; "Vertical velocity (pressure)"; Pa/s; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.228)
A158 `wz` — paramId 260238; "Geometric vertical velocity"; m/s; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (clamp r.128-136) [SUPPORTATA: registro] (§7.PL, r.229)
A159 `z` — paramId 129; "Geopotential"; m^2/s^2; 13 livelli di pressione; istantaneo; derivazione: non indicata in tabella (sotto terra a 1000 hPa sta 24-27 m sopra il terreno, r.133-135) [SUPPORTATA: registro] (§7.PL, r.230)

### §7.HAG Height above ground (11 variabili, 11 messaggi)
A160 `100u` — paramId 228246; "100m U component of wind"; m/s; 100 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.237)
A161 `100v` — paramId 228247; "100m V component of wind"; m/s; 100 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.238)
A162 `10fg` — paramId 49; "10m wind gust (hourly max of resolved wind)"; m/s; 10 m; massimo sull'ora precedente; derivazione (da Description): massimo orario del vento risolto (cfr. r.59-61, r.74) [SUPPORTATA: registro] (§7.HAG, r.239)
A163 `10u` — paramId 165; "10m U component of wind"; m/s; 10 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.240)
A164 `10v` — paramId 166; "10m V component of wind"; m/s; 10 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.241)
A165 `200u` — paramId 228239; "200m U component of wind"; m/s; 200 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.242)
A166 `200v` — paramId 228240; "200m V component of wind"; m/s; 200 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.243)
A167 `2d` — paramId 168; "2m dewpoint temperature"; K; 2 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.244)
A168 `2r` — paramId 260242; "2m relative humidity"; %; 2 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.245)
A169 `2t` — paramId 167; "2m temperature"; K; 2 m; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.HAG, r.246)
A170 `vwsh` — paramId 260068; "Vertical speed shear (bulk 10-100 m)"; s^-1; livello 100 m; istantaneo; derivazione (da Description): shear bulk fra 10 e 100 m [SUPPORTATA: registro] (§7.HAG, r.247)

### §7.MSL Mean sea level (1 variabile, 1 messaggio)
A171 `msl` — paramId 151; "Mean sea level pressure"; Pa; mean sea level; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.MSL, r.254)

### §7.COL Total column (10 variabili, 10 messaggi)
A172 `hcc` — paramId 188; "High cloud cover"; (0-1); colonna; istantaneo; derivazione: non indicata in tabella (39 % sotto ERA5, r.125) [SUPPORTATA: registro] (§7.COL, r.261)
A173 `lcc` — paramId 186; "Low cloud cover"; (0-1); colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.262)
A174 `mcc` — paramId 187; "Medium cloud cover"; (0-1); colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.263)
A175 `tcc` — paramId 164; "Total cloud cover"; (0-1); colonna; istantaneo; derivazione: non indicata in tabella (22 % sotto ERA5, r.124) [SUPPORTATA: registro] (§7.COL, r.264)
A176 `tciw` — paramId 79; "Total column cloud ice water"; kg/m^2; colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.265)
A177 `tclw` — paramId 78; "Total column cloud liquid water"; kg/m^2; colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.266)
A178 `tcrw` — paramId 228089; "Total column rain water"; kg/m^2; colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.267)
A179 `tcsw` — paramId 228090; "Total column snow water"; kg/m^2; colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.268)
A180 `tcw` — paramId 136; "Total column water"; kg/m^2; colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.269)
A181 `tcwv` — paramId 137; "Total column water vapour"; kg/m^2; colonna; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.COL, r.270)

### §7.SFC Surface / single level (47 variabili, 47 messaggi)
A182 `al` — paramId 174; "Albedo (climatological, snow-free background)"; (0-1); surface; istantaneo; derivazione: valore tabellare a due stagioni (cfr. r.111-118) [SUPPORTATA: registro] (§7.SFC, r.277)
A183 `ci` — paramId 31; "Sea ice area fraction"; (0-1); surface; istantaneo; derivazione: non indicata in tabella; mascherato fuori mare (r.150) [SUPPORTATA: registro] (§7.SFC, r.278)
A184 `cl` — paramId 26; "Lake cover"; (0-1); surface; istantaneo, static; derivazione: non indicata in tabella; da `geo_em.d02` (r.10, r.201-202); zero sul mare (r.151) [SUPPORTATA: registro] (§7.SFC, r.279)
A185 `cvh` — paramId 28; "High vegetation cover"; (0-1); surface; istantaneo, static; derivazione: somma della copertura frazionaria sulle classi MODIS-IGBP alte (r.188-189) [SUPPORTATA: registro] (§7.SFC, r.280)
A186 `cvl` — paramId 27; "Low vegetation cover"; (0-1); surface; istantaneo, static; derivazione: somma della copertura frazionaria sulle classi MODIS-IGBP basse (r.188-189) [SUPPORTATA: registro] (§7.SFC, r.281)
A187 `fal` — paramId 243; "Forecast albedo (upward/downward SW at surface)"; (0-1); surface; istantaneo; derivazione (da Description): rapporto SW ascendente/discendente in superficie; solo di giorno (r.154) [SUPPORTATA: registro] (§7.SFC, r.282)
A188 `fsr` — paramId 244; "Forecast surface roughness"; m; surface; istantaneo; derivazione: `ZNT` locale di WRF (r.76) [SUPPORTATA: registro] (§7.SFC, r.283)
A189 `iews` — paramId 229; "Instantaneous eastward turbulent surface stress"; N/m^2; surface; istantaneo; derivazione: `rho u*^2` proiettato sulla direzione del vento a 10 m (r.75) [SUPPORTATA: registro] (§7.SFC, r.284)
A190 `inss` — paramId 230; "Instantaneous northward turbulent surface stress"; N/m^2; surface; istantaneo; derivazione: `rho u*^2` proiettato sulla direzione del vento a 10 m (r.75) [SUPPORTATA: registro] (§7.SFC, r.285)
A191 `lsm` — paramId 172; "Land-sea mask"; (0-1); surface; istantaneo; derivazione: `LANDMASK` di WRF (r.77); non static (r.326-329) [SUPPORTATA: registro] (§7.SFC, r.286)
A192 `ro` — paramId 205; "Runoff (surface + sub-surface)"; m; surface; accumulato da 00 UTC; derivazione (da Description): superficiale + sotto-superficiale [SUPPORTATA: registro] (§7.SFC, r.287)
A193 `rsn` — paramId 33; "Snow density"; kg/m^3; surface; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.288)
A194 `sd` — paramId 141; "Snow depth (water equivalent)"; m; surface; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.289)
A195 `sdor` — paramId 160; "Standard deviation of orography"; m; surface; istantaneo; derivazione: non indicata in tabella; grandezza ERA5 su cella 3 km (r.73) [SUPPORTATA: registro] (§7.SFC, r.290)
A196 `sf` — paramId 144; "Snowfall (water equivalent)"; m; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.291)
A197 `skt` — paramId 235; "Skin temperature (inverted from upward longwave)"; K; surface; istantaneo; derivazione (da Description): invertita dall'onda lunga ascendente (cfr. r.83-109) [SUPPORTATA: registro] (§7.SFC, r.292)
A198 `slor` — paramId 163; "Slope of orography (resolved, 3 km)"; unità Numeric; surface; istantaneo; derivazione: pendenza del terreno risolto, `|grad z|` (r.73) [SUPPORTATA: registro] (§7.SFC, r.293)
A199 `slt` — paramId 43; "Soil type (ECMWF 7 classes)"; unità ~; surface; istantaneo, static; derivazione: soglie FAO argilla/sabbia (r.195-197, r.391-408) [SUPPORTATA: registro] (§7.SFC, r.294)
A200 `snowc` — paramId 260038; "Snow cover"; %; surface; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.295)
A201 `sp` — paramId 134; "Surface pressure"; Pa; surface; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.296)
A202 `src` — paramId 198; "Skin reservoir content"; m; surface; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.297)
A203 `sro` — paramId 8; "Surface runoff"; m; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.298)
A204 `ssr` — paramId 176; "Surface net solar radiation"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.299)
A205 `ssrc` — paramId 210; "Surface net solar radiation, clear sky"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.300)
A206 `ssrd` — paramId 169; "Surface solar radiation downwards"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella (+13.6 % contro ERA5, r.122) [SUPPORTATA: registro] (§7.SFC, r.301)
A207 `ssrdc` — paramId 228129; "Surface solar radiation downwards, clear sky"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella (+8.5 % contro ERA5, r.122) [SUPPORTATA: registro] (§7.SFC, r.302)
A208 `ssro` — paramId 9; "Sub-surface runoff"; m; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.303)
A209 `sst` — paramId 34; "Sea surface temperature"; K; surface; istantaneo; derivazione: non indicata in tabella; costante nella run (r.137), mascherata fuori mare (r.150) [SUPPORTATA: registro] (§7.SFC, r.304)
A210 `stl1` — paramId 139; "Soil temperature level 1 (0-7 cm)"; K; surface; istantaneo; derivazione: integrale esatto del profilo del modello (r.182-186, r.410-417) [SUPPORTATA: registro] (§7.SFC, r.305)
A211 `stl2` — paramId 170; "Soil temperature level 2 (7-28 cm)"; K; surface; istantaneo; derivazione: integrale esatto del profilo (r.410-417) [SUPPORTATA: registro] (§7.SFC, r.306)
A212 `stl3` — paramId 183; "Soil temperature level 3 (28-100 cm)"; K; surface; istantaneo; derivazione: integrale esatto del profilo (r.410-417) [SUPPORTATA: registro] (§7.SFC, r.307)
A213 `stl4` — paramId 236; "Soil temperature level 4 (100-289 cm)"; K; surface; istantaneo; derivazione: integrale esatto del profilo (r.410-417) [SUPPORTATA: registro] (§7.SFC, r.308)
A214 `str` — paramId 177; "Surface net thermal radiation"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.309)
A215 `strc` — paramId 211; "Surface net thermal radiation, clear sky"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.310)
A216 `strd` — paramId 175; "Surface thermal radiation downwards"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.311)
A217 `strdc` — paramId 228130; "Surface thermal radiation downwards, clear sky"; J/m^2; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.312)
A218 `swvl1` — paramId 39; "Volumetric soil water layer 1 (0-7 cm)"; m^3/m^3; surface; istantaneo; derivazione: integrale esatto del profilo, umidità totale liquido + ghiaccio (r.410-420) [SUPPORTATA: registro] (§7.SFC, r.313)
A219 `swvl2` — paramId 40; "Volumetric soil water layer 2 (7-28 cm)"; m^3/m^3; surface; istantaneo; derivazione: come `swvl1` (r.410-420) [SUPPORTATA: registro] (§7.SFC, r.314)
A220 `swvl3` — paramId 41; "Volumetric soil water layer 3 (28-100 cm)"; m^3/m^3; surface; istantaneo; derivazione: come `swvl1` (r.410-420) [SUPPORTATA: registro] (§7.SFC, r.315)
A221 `swvl4` — paramId 42; "Volumetric soil water layer 4 (100-289 cm)"; m^3/m^3; surface; istantaneo; derivazione: come `swvl1` (r.410-420) [SUPPORTATA: registro] (§7.SFC, r.316)
A222 `tirf` — paramId 235015; "Time integral of rain flux (rain only)"; kg/m^2; surface; accumulato da 00 UTC; derivazione (da Description): solo pioggia [SUPPORTATA: registro] (§7.SFC, r.317)
A223 `tp` — paramId 228; "Total precipitation"; m; surface; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.SFC, r.318)
A224 `tsn` — paramId 238; "Temperature of snow layer"; K; surface; istantaneo; derivazione: non indicata in tabella; mascherato sotto copertura nevosa 0.9 (r.153) [SUPPORTATA: registro] (§7.SFC, r.319)
A225 `tvh` — paramId 30; "Type of high vegetation (ECMWF code table 4.234)"; unità ~; surface; istantaneo, static; derivazione: classe dominante alta tradotta con la tabella di §8 (r.362-381) [SUPPORTATA: registro] (§7.SFC, r.320)
A226 `tvl` — paramId 29; "Type of low vegetation (ECMWF code table 4.234)"; unità ~; surface; istantaneo, static; derivazione: classe dominante bassa tradotta con la tabella di §8 (r.362-381); mancante sugli arbusteti (r.157) [SUPPORTATA: registro] (§7.SFC, r.321)
A227 `z` — paramId 129; "Geopotential (surface)"; m^2/s^2; surface; istantaneo; derivazione: non indicata in tabella; orografia (r.211) [SUPPORTATA: registro] (§7.SFC, r.322)
A228 `zust` — paramId 228003; "Friction velocity"; m/s; surface; istantaneo; derivazione: velocità di attrito del modello stesso (r.76) [SUPPORTATA: registro] (§7.SFC, r.323)
A229 "static" nella colonna Time significa che il campo è identico in ogni file dell'archivio: viene dall'input statico della run, non dallo stato orario [SENZA FONTE] (§7.SFC, r.326-327)
A230 `lsm` è deliberatamente NON static: il modello riclassifica punti di mare come terra dove appare ghiaccio marino, quindi cambia con la stagione [SENZA FONTE] (§7.SFC, r.327-329)

### §7.LAKE Entire lake (1 variabile, 1 messaggio)
A231 `dl` — paramId 228007; "Lake total depth"; m; entireLake; istantaneo, static; derivazione: database di profondità dei laghi (r.138-142), mascherato fuori lago [SUPPORTATA: registro] (§7.LAKE, r.335)

### §7.TOA Top of atmosphere / most unstable parcel (7 variabili, 7 messaggi)
A232 `mucape` — paramId 228235; "Most-unstable CAPE"; J/kg; most unstable parcel; istantaneo; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.TOA, r.341)
A233 `mucin` — paramId 228236; "Most-unstable CIN"; J/kg; most unstable parcel; istantaneo; derivazione: non indicata in tabella; bitmap dove CAPE < 100 J/kg (r.152) [SUPPORTATA: registro] (§7.TOA, r.342)
A234 `tisr` — paramId 212; "TOA incident solar radiation"; J/m^2; top of atmosphere; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.TOA, r.343)
A235 `tsr` — paramId 178; "Top net solar radiation"; J/m^2; top of atmosphere; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.TOA, r.344)
A236 `tsrc` — paramId 208; "Top net solar radiation, clear sky"; J/m^2; top of atmosphere; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.TOA, r.345)
A237 `ttr` — paramId 179; "Top net thermal radiation"; J/m^2; top of atmosphere; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.TOA, r.346)
A238 `ttrc` — paramId 209; "Top net thermal radiation, clear sky"; J/m^2; top of atmosphere; accumulato da 00 UTC; derivazione: non indicata in tabella [SUPPORTATA: registro] (§7.TOA, r.347)

### §8 How the land-surface categories were translated
A239 `tvl`, `tvh` e `slt` sono gli unici campi dell'archivio che portano un *codice* invece di un numero; le tabelle che li hanno prodotti sono pubblicate perché senza di esse i codici non si leggono e la mappatura non si può controllare [SENZA FONTE] (§8, r.352-354)
A240 Sorgente: il file statico della run `geo_em.d02` (MODIS-IGBP 21 classi, WPS `MMINLU=MODIFIED_IGBP_MODIS_NOAH`) [SUPPORTATA: `geo_em.d02`, `MMINLU`] (§8, r.356-357)
A241 Il suo land use è stato verificato contro l'output orario: concorda con la categoria dominante del modello sul 100.00 % dei punti esclusa una differenza attesa [SENZA FONTE] (§8, r.357-359)
A242 La differenza attesa: il modello ricodifica il lago in acqua a runtime, perché la fisica dei laghi era spenta [SENZA FONTE] (§8, r.359-360)
A243 È ciò che rende `cl` recuperabile [SENZA FONTE] (§8, r.360)
A244 Alta e bassa seguono le definizioni IGBP di copertura arborea, non una tabella di altezza della chioma [SUPPORTATA: definizioni IGBP] (§8.tv, r.364)
A245 MODIS-IGBP 1 Evergreen Needleleaf Forest → insieme high → ECMWF 4.234 codice 3 Evergreen needleleaf trees [SUPPORTATA: tabella di traduzione §8] (§8.tv, r.368)
A246 MODIS-IGBP 2 Evergreen Broadleaf Forest → high → 6 Evergreen broadleaf trees [SUPPORTATA: tabella §8] (§8.tv, r.369)
A247 MODIS-IGBP 3 Deciduous Needleleaf Forest → high → 4 Deciduous needleleaf trees [SUPPORTATA: tabella §8] (§8.tv, r.370)
A248 MODIS-IGBP 4 Deciduous Broadleaf Forest → high → 5 Deciduous broadleaf trees [SUPPORTATA: tabella §8] (§8.tv, r.371)
A249 MODIS-IGBP 5 Mixed Forests → high → 18 Mixed forest/woodland [SUPPORTATA: tabella §8] (§8.tv, r.372)
A250 MODIS-IGBP 8 Woody Savannas → high → 19 Interrupted forest (entrambi 30–60 % di copertura arborea) [SUPPORTATA: tabella §8] (§8.tv, r.373)
A251 MODIS-IGBP 9 Savannas → low → 7 Tall grass [SUPPORTATA: tabella §8] (§8.tv, r.374)
A252 MODIS-IGBP 10 Grasslands → low → 2 Short grass [SUPPORTATA: tabella §8] (§8.tv, r.375)
A253 MODIS-IGBP 11 Permanent Wetlands → low → 13 Bogs and marshes (assente da questo dominio) [SUPPORTATA: tabella §8] (§8.tv, r.376)
A254 MODIS-IGBP 12 Croplands → low → 1 Crops, mixed farming [SUPPORTATA: tabella §8] (§8.tv, r.377)
A255 MODIS-IGBP 14 Cropland/Natural Mosaic → low → 1 Crops, mixed farming (assente da questo dominio) [SUPPORTATA: tabella §8] (§8.tv, r.378)
A256 MODIS-IGBP 18 Wooded Tundra, 19 Mixed Tundra, 20 Barren Tundra → low → 9 Tundra [SUPPORTATA: tabella §8] (§8.tv, r.379)
A257 MODIS-IGBP 6 Closed Shrublands, 7 Open Shrublands → low → non tradotte, `tvl` mancante lì [SUPPORTATA: tabella §8] (§8.tv, r.380)
A258 MODIS-IGBP 13 Urban, 15 Snow and Ice, 16 Barren, 17 Water, 21 Lake → né alta né bassa → nessun codice (non vegetazione; sono il resto di `1 − cvl − cvh`) [SUPPORTATA: tabella §8] (§8.tv, r.381)
A259 Ogni riga tradotta è un'identità semantica: il tipo ECMWF nomina la stessa vegetazione della classe MODIS [SENZA FONTE] (§8.tv, r.383-384)
A260 Le due classi di arbusteto sono l'eccezione e la ragione per cui `tvl` porta una maschera: MODIS non registra se un arbusteto è sempreverde o deciduo, mentre la tabella 4.234 ha codici separati per i due (16 e 17) [SUPPORTATA: tabella ECMWF 4.234] (§8.tv, r.384-386)
A261 Sceglierne uno sarebbe stata una nostra invenzione sul 16.2 % delle celle vegetate, quindi il campo è lasciato mancante lì; `cvl` riporta ancora la copertura [SENZA FONTE] (§8.tv, r.386-388)
A262 Le classi che sarebbero state le altre righe ambigue, 11 e 14, non occorrono affatto in questo dominio [SENZA FONTE] (§8.tv, r.388-389)
A263 `slt`: nessun crosswalk di categorie; i sette tipi di suolo ECMWF sono *definiti* da soglie percentuali di argilla e sabbia, il file statico porta frazioni di argilla e sabbia, quindi la definizione è applicata direttamente [SUPPORTATA: definizione ECMWF dei tipi di suolo] (§8.slt, r.393-395)
A264 clay ≥ 60 → tipo ECMWF 5 very fine [SUPPORTATA: tabella §8.slt] (§8.slt, r.399)
A265 35 ≤ clay < 60 → 4 fine [SUPPORTATA: tabella §8.slt] (§8.slt, r.400)
A266 clay < 35 e sand ≤ 15 → 3 medium fine [SUPPORTATA: tabella §8.slt] (§8.slt, r.401)
A267 (18 ≤ clay < 35 e sand > 15) oppure (clay < 18 e 15 < sand ≤ 65) → 2 medium [SUPPORTATA: tabella §8.slt] (§8.slt, r.402)
A268 clay < 18 e sand > 65 → 1 coarse [SUPPORTATA: tabella §8.slt] (§8.slt, r.403)
A269 categoria di suolo dominante *organic material* → 6 organic [SUPPORTATA: tabella §8.slt] (§8.slt, r.404)
A270 Ogni punto di terra si classifica; il tipo 7 (tropical organic) non occorre qui [SENZA FONTE] (§8.slt, r.406)
A271 Lo schema di superficie porta valori puntuali a 0, 5, 20, 40, 160 e 300 cm con profilo lineare fra loro; ERA5 vuole medie su 0–7, 7–28, 28–100 e 100–289 cm [SENZA FONTE] (§8.soil, r.412-414)
A272 I quattro intervalli stanno interamente dentro i nodi del modello (289 cm sopra il più profondo, 0 cm il primo), quindi ogni strato ERA5 è l'**integrale esatto** del profilo del modello e nulla è estrapolato a nessuna delle due estremità [SENZA FONTE] (§8.soil, r.414-416)
A273 In pratica è una matrice fissa 4 × 6 di pesi applicata ai sei livelli del modello [SENZA FONTE] (§8.soil, r.416-417)
A274 `swvl` usa l'umidità totale del suolo (liquido più ghiaccio), che è ciò che significa il nome ERA5; il campo solo-liquido non è usato [SENZA FONTE] (§8.soil, r.419-420)
A275 Entrambi gli insiemi (`swvl`, `stl`) sono mascherati sull'acqua [SENZA FONTE] (§8.soil, r.420)

## 2. Dati numerici

N001 variabili = 90 — per file orario (§0, r.3) [fonte: registro `wrf_era5_comparison.WRF_TO_ECMWF_PARAMID`]
N002 messaggi GRIB = 246 — per file orario (§0, r.3) [fonte: registro]
N003 data aggiornamento documento = 2026-09-18 — recupero di `geo_em.d02` (§0, r.7) [SENZA FONTE]
N004 campi aggiunti da `geo_em.d02` = 15 (§0, r.10) [fonte: `geo_em.d02`]
N005 strati di suolo ERA5 aggiunti = 8 (§0, r.10-11) [fonte: `geo_em.d02`]
N006 livelli verticali del modello = 49 (§1, r.29) [SENZA FONTE]
N007 top del modello = 50 hPa (§1, r.29) [SENZA FONTE]
N008 punti di griglia = 1641 × 1353 (§1, r.30) [SENZA FONTE]
N009 spaziatura = 3 km (§1, r.30) [SENZA FONTE]
N010 punti per campo = 2 220 273 (§1, r.30) [SENZA FONTE]
N011 angoli del dominio = 23.472 N, 19.972 W → 60.001 N, 42.256 E (§1, r.31) [SENZA FONTE]
N012 parallelo standard = 44.671 N (§1, r.31) [SENZA FONTE]
N013 raggio della sfera = 6 370 000 m — `shapeOfTheEarth=1` (§1, r.32) [fonte: chiave GRIB]
N014 bit per valore = 24 — packing `grid_ccsds` (§1, r.34) [SENZA FONTE]
N015 dimensione file = ~747 MB — per ora, "misurata, non stimata" (§1, r.36) [SENZA FONTE]
N016 volume = ~17.9 GB/giorno (§1, r.36) [SENZA FONTE]
N017 volume = ~6.6 TB/anno (§1, r.36) [SENZA FONTE]
N018 blocco contiguo 2025 = 4392 ore — termina 2025-07-02T23, niente dopo (§1, r.38) [fonte: scan `mmlsattr` 2026-09-29]
N019 livelli di pressione = 13 — gli stessi per ogni variabile 3-D (§2, r.42) [fonte: registro]
N020 valori dei livelli = 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50 hPa (§2, r.44) [fonte: registro]
N021 livelli ERA5 sopra 50 hPa = 8 — sopra `P_TOP` (§2, r.46) [SENZA FONTE]
N022 altezze `heightAboveGround` = 2, 10, 100, 200 m (§2, r.48) [SENZA FONTE]
N023 product definition template = 0 (istantanei), 8 (accumulati) (§3, r.53, r.56) [fonte: definizioni ECMWF]
N024 `generatingProcessIdentifier` = 128 — messaggi accumulati (§3, r.64) [SENZA FONTE]
N025 risoluzione di confronto `sdor` = 3 km contro 31 km (§4, r.73) [SENZA FONTE]
N026 rapporto delle mediane `sdor` = 0.244 — CHAPTER/ERA5 (§4, r.73) [SENZA FONTE]
N027 esponente del riscalamento = 0.605 — (3/31)^0.605 (§4, r.73) [SENZA FONTE]
N028 `fsr` CHAPTER/ERA5 su terra = 0.32–0.48 — in mediana (§4, r.76) [SENZA FONTE]
N029 `zust` CHAPTER/ERA5 = 1.6–2.1× su terra, 1.1× su mare (§4, r.76) [SENZA FONTE]
N030 risoluzione IFS citata = 31 km (§4, r.76) [SENZA FONTE]
N031 `swvl` sotto nuovo ghiaccio = 1.000 — contro porosità 0.435 del tipo di suolo (§4, r.79) [SENZA FONTE]
N032 data mascheratura colonne di suolo su terra permanente = 2026-09-25 (§4, r.79) [SENZA FONTE]
N033 spread dell'emissività per categoria = 0.0000 — a quattro decimali (§4, r.90) [SENZA FONTE]
N034 emissività su acqua aperta = 0.98000 (§4, r.91) [SENZA FONTE]
N035 frazione di punti di terra con emissività entro 1e-4 = 99.98 % luglio, 93.05 % gennaio (§4, r.94) [SENZA FONTE]
N036 RMSE `skt` su terra = 0.0012 K luglio; 0.084–0.119 K gennaio e febbraio (§4, r.95-96) [SENZA FONTE]
N037 p99 errore `skt` = 0.81 K; punto peggiore 2.79 K — inverno (§4, r.96) [SENZA FONTE]
N038 emissività sotto neve = 0.98 — piatta in ogni categoria (§4, r.97) [SENZA FONTE]
N039 soglia di copertura nevosa = 1.5 % — sopra: 0.98 piatta; sotto: blend (§4, r.97) [fonte: sweep su 34 timestep]
N040 timestep dello sweep = 34 (§4, r.99) [fonte: sweep]
N041 RMSE SST su acqua aperta = 0.0005 K — su circa 910 000 punti, ogni timestep (§4, r.102-103) [fonte: misura su acqua aperta]
N042 rapporto bias fisico / errore di derivazione = 30 (§4, r.103-104) [SENZA FONTE]
N043 bias `skt` su terra contro ERA5 = −1.6 K circa; −3.2 K a mezzogiorno (§4, r.105) [SENZA FONTE]
N044 bias `skt` su mare contro ERA5 = +0.01 K (§4, r.106) [SENZA FONTE]
N045 valori distinti di `al` = 8 a 11 — tutto il dominio (§4, r.113) [SENZA FONTE]
N046 punti di terra dove `al` cambia al confine stagionale = 1 171 937 — 89.9 % della maschera di terra (§4, r.114-115) [SENZA FONTE]
N047 `al` fuori terra = 0.08 su acqua, 0.65 su ghiaccio marino (§4, r.116) [SENZA FONTE]
N048 `aer_opt` = 0 (§4, r.120) [fonte: namelist]
N049 spessore ottico aerosol che spiega il bias = 0.1–0.2 — su questo dominio (§4, r.121) [SENZA FONTE]
N050 bias `ssrdc` contro ERA5 = +8.5 % (§4, r.122) [SENZA FONTE]
N051 bias `ssrd` contro ERA5 = +13.6 % (§4, r.122) [SENZA FONTE]
N052 accordo campi termici con ERA5 = entro 1.1 % (§4, r.123-124) [SENZA FONTE]
N053 copertura nuvolosa totale contro ERA5 = −22 % (§4, r.124) [SENZA FONTE]
N054 nuvole alte contro ERA5 = −39 % (§4, r.125) [SENZA FONTE]
N055 accordo del clamp con il livello più basso = 0.0 per `t`, 1e-9 per `q` (§4, r.130) [SENZA FONTE]
N056 quota del livello modello più basso = circa 24–27 m sopra il suolo (§4, r.130-131) [SENZA FONTE]
N057 quota mediana di `z` a 1000 hPa sopra il terreno = 24–27 m (§4, r.134) [SENZA FONTE]
N058 frazione di dominio con livello sotto terra = 47.6 % a 1000 hPa, 9 % a 925 hPa (§4, r.134-135) [SENZA FONTE]
N059 durata della run con `sst` costante = 24 h (§4, r.137) [fonte: `SST_UPDATE=0`]
N060 default WPS di profondità lacustre = 10 m (§4, r.141) [SENZA FONTE]
N061 frazione di dominio col default = 99.56 % (§4, r.141) [SENZA FONTE]
N062 celle di lago col default = 79 464 su 88 785 (§4, r.141-142) [SENZA FONTE]
N063 componente d'acqua Atlantico + Mediterraneo + Baltico + Mare del Nord = 844 431 celle (§5, r.150) [fonte: misura sul dominio]
N064 componente Mar Nero + Azov = 49 841 celle (§5, r.150) [fonte: misura sul dominio]
N065 componente Mar Rosso = 8 583 celle (§5, r.150) [fonte: misura sul dominio]
N066 componente Vänern = 1 225 celle — il lago vero più grande (§5, r.150) [fonte: misura sul dominio]
N067 margine della soglia = fattore sette (§5, r.150) [SENZA FONTE]
N068 soglia CAPE per `mucin` = 100 J/kg (§5, r.152) [SENZA FONTE]
N069 copertura di `mucin` = 4 %–29 % del dominio — meno in inverno (§5, r.152) [SENZA FONTE]
N070 soglia di copertura nevosa per `tsn` = 0.9 (≈ 29 mm di equivalente in acqua) (§5, r.153) [SENZA FONTE]
N071 soglia di SW incidente per `fal` = 50 W/m² (§5, r.154) [SENZA FONTE]
N072 celle di terra del file statico (`slt`) = 1 304 109 (§5, r.156; §8.slt, r.407) [fonte: file statico]
N073 celle con `tvl` mancante = 124 672 — 15.8 % di quelle con `cvl > 0` (§5, r.157) [SENZA FONTE]
N074 celle di lago (`dl`) = 88 785 (§5, r.158) [SENZA FONTE]
N075 data fino a cui le quattro voci stavano in §6 = 2026-09-17 (§6, r.179) [SENZA FONTE]
N076 nodi dello schema di superficie = 0, 5, 20, 40, 160, 300 cm (§6, r.183; §8.soil, r.412-413) [SENZA FONTE]
N077 fondo della colonna ERA5 = 289 cm (§6, r.184) [SENZA FONTE]
N078 frazione media di cella di terra tenuta dalla categoria dominante = 90.1 % (§6, r.190) [SENZA FONTE]
N079 celle di terra con vegetazione alta e bassa entrambe > 5 % = 17.9 % (§6, r.190-191) [SENZA FONTE]
N080 tipi di suolo ECMWF = 7 (§6, r.196) [SENZA FONTE]
N081 disciplina eccodes per `slt` = 2/3/0 (§6, r.198) [fonte: eccodes]
N082 valori della tabella WMO 4.213 = 11 (§6, r.199) [fonte: tabella WMO 4.213]
N083 celle marcate terra con lago sottogriglia = 19 309 (§6, r.201) [SENZA FONTE]
N084 righe della tabella variabili = 90; shortName distinti = 89 (§7, r.209-210) [fonte: registro]
N085 Pressure levels = 13 variabili, 169 messaggi (§7.PL, r.214) [fonte: registro]
N086 Height above ground = 11 variabili, 11 messaggi (§7.HAG, r.233) [fonte: registro]
N087 Mean sea level = 1 variabile, 1 messaggio (§7.MSL, r.250) [fonte: registro]
N088 Total column = 10 variabili, 10 messaggi (§7.COL, r.257) [fonte: registro]
N089 Surface / single level = 47 variabili, 47 messaggi (§7.SFC, r.273) [fonte: registro]
N090 Entire lake = 1 variabile, 1 messaggio (§7.LAKE, r.331) [fonte: registro]
N091 Top of atmosphere / most unstable parcel = 7 variabili, 7 messaggi (§7.TOA, r.337) [fonte: registro]
N092 classi MODIS-IGBP = 21 (§8, r.356) [fonte: `geo_em.d02`]
N093 accordo land use statico / categoria dominante oraria = 100.00 % — esclusa la ricodifica lago→acqua (§8, r.358) [SENZA FONTE]
N094 copertura arborea Woody Savannas / Interrupted forest = 30–60 % (§8.tv, r.373) [SENZA FONTE]
N095 codici 4.234 per arbusti sempreverdi/decidui = 16 e 17 (§8.tv, r.386) [fonte: tabella ECMWF 4.234]
N096 celle vegetate su cui la scelta sarebbe stata inventata = 16.2 % (§8.tv, r.387) [SENZA FONTE]
N097 soglie `slt` = clay 18, 35, 60 %; sand 15, 65 % (§8.slt, r.399-403) [fonte: soglie FAO]
N098 punti di terra `slt` medium = 1 069 456 — su 1 304 109 (§8.slt, r.407) [SENZA FONTE]
N099 punti `slt` coarse = 187 378 (§8.slt, r.407) [SENZA FONTE]
N100 punti `slt` fine = 45 450 (§8.slt, r.407) [SENZA FONTE]
N101 punti `slt` organic = 1 498 (§8.slt, r.407) [SENZA FONTE]
N102 punti `slt` very fine = 327 (§8.slt, r.407-408) [SENZA FONTE]
N103 strati ERA5 = 0–7, 7–28, 28–100, 100–289 cm (§8.soil, r.414) [SENZA FONTE]
N104 matrice dei pesi = 4 × 6 — applicata ai sei livelli del modello (§8.soil, r.417) [SENZA FONTE]

## 3. Equazioni

E001 $LWUPB = \varepsilon\,\sigma\,T^4 + (1-\varepsilon)\,LWDN$ — simboli: LWUPB = upward longwave; eps = emissività; sigma = non definito nel testo; T = temperatura di pelle (skin temperature); LWDN = flusso longwave discendente (§4, r.84)
E002 $\varepsilon = 1 - \dfrac{LWUPB - LWUPBC}{LWDN - LWDNC}$ — simboli: LWUPBC, LWDNC = diagnostica clear-sky "con la stessa emissività e la stessa temperatura di pelle, cambiando solo il flusso discendente" (§4, r.88)
E003 $slor = |\nabla z|$ — simboli: z = terreno risolto a 3 km (§4, r.73)
E004 $0.244 = (3/31)^{0.605}$ — simboli: 0.244 = rapporto delle mediane di `sdor`; 3 e 31 = km di cella CHAPTER ed ERA5 (§4, r.73)
E005 $\tau = \rho\,u_*^2$ (proiettato sulla direzione del vento a 10 m) — simboli: rho, u* non definiti nel testo; componenti = `iews`, `inss` (§4, r.75)
E006 $lsm \wedge \neg(ci > 0)$ — simboli: `lsm` = `LANDMASK` di WRF; `ci` = frazione di ghiaccio marino; risultato = senso ERA5 della maschera (§4, r.77)
E007 $1 - cvl - cvh$ — simboli: resto della cella non vegetato (classi 13, 15, 16, 17, 21) (§8.tv, r.381)
E008 $clay \ge 60 \Rightarrow slt = 5$ — simboli: clay = percentuale di argilla; 5 = very fine (§8.slt, r.399)
E009 $35 \le clay < 60 \Rightarrow slt = 4$ — 4 = fine (§8.slt, r.400)
E010 $clay < 35 \wedge sand \le 15 \Rightarrow slt = 3$ — sand = percentuale di sabbia; 3 = medium fine (§8.slt, r.401)
E011 $(18 \le clay < 35 \wedge sand > 15) \vee (clay < 18 \wedge 15 < sand \le 65) \Rightarrow slt = 2$ — 2 = medium (§8.slt, r.402)
E012 $clay < 18 \wedge sand > 65 \Rightarrow slt = 1$ — 1 = coarse (§8.slt, r.403)

## 4. Riferimenti bibliografici

R001 `wrf_era5_comparison.WRF_TO_ECMWF_PARAMID` (§0, r.4)
R002 [`MISSING_VARIABLES.md`](MISSING_VARIABLES.md) (§0, r.19)
R003 [`CHAPTER_KNOWN_PROPERTIES.md`](CHAPTER_KNOWN_PROPERTIES.md) (§0, r.20)
R004 WRF 4.1.1 (§1, r.29)
R005 scan `mmlsattr` of the whole of 2025 on the source (2026-09-29) (§1, r.38)
R006 "their ECMWF definitions" (§3, r.56)
R007 eccodes (§4, r.73; §6, r.198)
R008 IFS (§4, r.76)
R009 RRTMG (§4, r.120)
R010 "the Tegen aerosol climatology" (§4, r.121)
R011 `CHAPTER_KNOWN_PROPERTIES.md` (§4, r.127)
R012 "the land-use table's WINTER and SUMMER columns" (§4, r.112-113)
R013 "ECMWF's table" / "ECMWF code table 4.234" (§5, r.157; §6, r.192; §8.tv, r.362)
R014 "the FAO clay/sand thresholds" (§6, r.195)
R015 "WMO table 4.213" (§6, r.198)
R016 `MISSING_VARIABLES.pdf` (§6, r.205)
R017 MODIS-IGBP 21 classes, WPS `MMINLU=MODIFIED_IGBP_MODIS_NOAH` (§8, r.356-357)
R018 "the IGBP class definitions of tree cover" (§8.tv, r.364)

## 5. Figure e tabelle

T001 Tabella senza intestazione (2 colonne: voce, valore), 10 righe: Model, Horizontal grid, Domain corners, Earth shape, GRIB edition, Packing, Parameter identity, File, Naming, Period — caratteristiche dei file (§1, r.27-38)
T002 Blocco citato: elenco dei 13 livelli di pressione (§2, r.44)
T003 Tabella "field | what ERA5 means | what we write", 5 righe (`slor`, `10fg`, `iews`/`inss`, `fsr`, `lsm`) — approssimazioni dichiarate (§4, r.71-77)
T004 Tabella "field | defined where", 9 righe (`sst`/`ci`, `cl`, `mucin`, `tsn`, `fal`, `swvl1-4`/`stl1-4`, `slt`, `tvl`, `dl`) — campi mascherati e dominio di definizione (§5, r.148-158)
T005 Tabella "shortName | paramId | Description | Units | Level | Time", Pressure levels, 13 righe (§7.PL, r.216-230)
T006 Stessa intestazione, Height above ground, 11 righe (§7.HAG, r.235-247)
T007 Stessa intestazione, Mean sea level, 1 riga (§7.MSL, r.252-254)
T008 Stessa intestazione, Total column, 10 righe (§7.COL, r.259-270)
T009 Stessa intestazione, Surface / single level, 47 righe (§7.SFC, r.275-323)
T010 Stessa intestazione, Entire lake, 1 riga (§7.LAKE, r.333-335)
T011 Stessa intestazione, Top of atmosphere / most unstable parcel, 7 righe (§7.TOA, r.339-347)
T012 Tabella "MODIS-IGBP class | set | ECMWF 4.234", 14 righe — traduzione delle classi di land use in `tvl`/`tvh` (§8.tv, r.366-381)
T013 Tabella "condition (percent) | ECMWF soil type", 6 righe — soglie argilla/sabbia per `slt` (§8.slt, r.397-404)

## 6. Termini tecnici

G001 paramId / shortName — identità dei parametri ECMWF, usata ovunque "so the archive is directly comparable with ERA5" (§1, r.35)
G002 `geo_em.d02` — il file statico WPS della run, porta copertura frazionaria, tessitura del suolo e dati dei laghi (§0, r.7-10; §8, r.356)
G003 registro (`WRF_TO_ECMWF_PARAMID`) — "the converter's own registry", usato dalla pipeline e dal sanity check (§0, r.3-4)
G004 `shapeOfTheEarth=1` — sfera di raggio 6 370 000 m, la sfera propria di WRF (§1, r.32)
G005 grid definition template 3.10 — Mercator (§1, r.33)
G006 `grid_ccsds` — packing, 24 bit per valore (§1, r.34)
G007 bitmap GRIB — maschera dei campi mascherati; "missing means missing" (§1, r.34; §5, r.146)
G008 `P_TOP` — top del modello WRF (50 hPa) (§2, r.47)
G009 `heightAboveGround`, `meanSea`, `entireAtmosphere`, `nominalTop`, `surface` — tipi di livello; `entireAtmosphere` = integrali di colonna; `nominalTop` = bilancio radiativo al top (§2, r.47-49)
G010 `entireLake` — tipo di livello di `dl`; non definito (§7.LAKE, r.335)
G011 most unstable parcel — livello di `mucape`/`mucin`; non definito (§7.TOA, r.341-342)
G012 product definition template 0 / 8 — 0 per campi istantanei, 8 per accumulati (§3, r.53-56)
G013 `validityDate`/`validityTime` — chiavi su cui indicizzare; non definite oltre (§3, r.62-63)
G014 `dataDate`/`dataTime` — tempo valido per i campi istantanei (§3, r.53-54)
G015 `generatingProcessIdentifier` — 128 = marcatore del riferimento 00 UTC (§3, r.64-65)
G016 accumulato da 00 UTC — riferimento 00 UTC, step `0–H`, zero nel file delle 00 UTC (§3, r.56-58)
G017 vento risolto — `10fg` è il massimo del vento a 10 m risolto, non una parametrizzazione di raffica (§3, r.60-61)
G018 form-drag — schema di cui `slor` ERA5 è parametro; non definito (§4, r.73)
G019 `ZNT` — rugosità locale di WRF: rugosità da land-use con override della neve (§4, r.76)
G020 Charnock — non definito; ERA5 e WRF su mare "both being Charnock" (§4, r.76)
G021 `LANDMASK` — maschera di WRF che riclassifica il ghiaccio marino come terra (§4, r.77)
G022 terra permanente — maschera di terra del file statico, contorno fisso (§4, r.79; §5, r.155)
G023 `TSK` — non definito; non scritto nell'output (§4, r.83)
G024 `LWUPB`, `LWUPBC`, `LWDN`, `LWDNC` — onda lunga ascendente/discendente, all-sky e clear-sky (§4, r.84-88)
G025 diagnostica clear-sky — calcolata dallo schema radiativo con la stessa emissività e temperatura di pelle, cambia solo il flusso discendente (§4, r.85-87)
G026 regola della neve — emissività 0.98 piatta da 1.5 % di copertura nevosa, blend sotto (§4, r.96-98)
G027 `usemonalb` — `.false.`: nessuna albedo satellitare mensile (§4, r.111-112)
G028 RRTMG — schema radiativo; non definito (§4, r.120)
G029 `aer_opt` — `= 0`: nessun aerosol (§4, r.120)
G030 climatologia aerosol Tegen — portata da ERA5; non definita (§4, r.121)
G031 clamp sotto terra — ripetere il valore del livello modello più basso verbatim invece di estrapolare (§4, r.128-130)
G032 lapse rate — con cui ERA5 estrapola sotto terra; non definito (§4, r.132)
G033 `SST_UPDATE` — `=0`: `sst` costante in ogni run di 24 h (§4, r.137)
G034 `sf_lake_physics` — `=0`: fisica dei laghi spenta (§4, r.139)
G035 componente connessa — discriminatore mare/acqua interna per dimensione (§5, r.150)
G036 static — "the field is identical in every file of the archive", dall'input statico della run (§7.SFC, r.326-327)
G037 YSU — schema PBL, "non-local" (§6, r.162)
G038 `CU_PHYSICS` — `=0`: precipitazione convettiva identicamente zero (§6, r.164)
G039 campo morto — "identically zero ... would be a dead field" (§6, r.164)
G040 `rdlai2d` — `.false.`: LAI è lookup tabellare sulla categoria dominante (§6, r.172-174)
G041 Kim-Arakawa — parametri di asimmetria e lunghezza efficace nel file statico; non quelli ECMWF (§6, r.176)
G042 schema a livelli — valori puntuali a 0, 5, 20, 40, 160, 300 cm con profilo lineare (§6, r.182-184; §8.soil, r.412-413)
G043 MODIS-IGBP — 21 classi del file statico (§8, r.356)
G044 `MMINLU` — `MODIFIED_IGBP_MODIS_NOAH` (§8, r.357)
G045 tabella di codici ECMWF 4.234 — codici dei tipi di vegetazione per `tvl`/`tvh` (§6, r.192; §8.tv, r.362-381)
G046 identità semantica — "the ECMWF type names the same vegetation as the MODIS class" (§8.tv, r.383-384)
G047 crosswalk di categorie — non definito; escluso per `slt` (§6, r.196; §8.slt, r.393)
G048 soglie FAO — soglie argilla/sabbia che definiscono i 7 tipi ECMWF (§6, r.195)
G049 tabella WMO 4.213 — legge la disciplina 2/3/0 come lista di 11 valori (§6, r.198-199)
G050 lago sottogriglia — portato da 19 309 celle che la maschera chiama terra (§6, r.201-202)
G051 umidità totale del suolo — liquido più ghiaccio (§8.soil, r.419)
G052 TKE — non definito; assente (§6, r.162)

## 7. Segnalazioni

S001 [VAGA] "~747 MB ... measured, not estimated" — non dice su quali file né quanti (§1, r.36)
S002 [GONFIATA] "Every field here is one we can defend row by row" — non dimostrato (§0, r.13)
S003 [GONFIATA] "directly comparable with ERA5" — contrasta con le approssimazioni dichiarate in §4 (§1, r.35)
S004 [RIFERIMENTO INCOMPLETO] "the ERA5 set truncated at the model top" — quale insieme ERA5 non è detto; 13 + 8 livelli implicherebbero 21 (§2, r.46)
S005 [CONTRADDIZIONE INTERNA] elenco dei tipi di livello a singolo livello (surface, heightAboveGround, meanSea, entireAtmosphere, nominalTop) non include `entireLake` (r.335) né "most unstable parcel" (r.341-342); la tabella usa "top of atmosphere" e "column" invece di `nominalTop` ed `entireAtmosphere` (§2, r.47-49; §7, r.261, r.343)
S006 [RIFERIMENTO INCOMPLETO] "as their ECMWF definitions require" — nessun documento o versione (§3, r.56)
S007 [GONFIATA] "They are exactly zero in the 00 UTC file" — non dimostrato nel file (§3, r.57-58)
S008 [CONTRADDIZIONE INTERNA] "Four fields are not exactly their ERA5 namesake" — la tabella ha 5 righe e 6 campi (`slor`, `10fg`, `iews`, `inss`, `fsr`, `lsm`) (§4, r.69-77)
S009 [NUMERO SENZA FONTE] rapporto delle mediane `sdor` 0.244 — "measured" senza periodo né popolazione (§4, r.73)
S010 [NUMERO SENZA FONTE] `fsr` 0.32–0.48 di ERA5, `zust` 1.6–2.1× (1.1× su mare) — senza periodo né popolazione (§4, r.76)
S011 [VAGA] "the other half of the same story" (§4, r.76)
S012 [GONFIATA] "`lsm & ~(ci > 0)` recovers the ERA5 sense exactly" — non dimostrato (§4, r.77)
S013 [CONTRADDIZIONE INTERNA] "`lsm` is now the only field that follows the model hour by hour (with `al`, which moves with it)" — r.113-116 dice che `al` cambia al confine stagionale su 89.9 % della terra, cioè non si muove solo con `lsm` (§4, r.79; r.113-116)
S014 [NUMERO SENZA FONTE] `swvl` 1.000 contro porosità 0.435 — non dice dove né quando (§4, r.79)
S015 [CONTRADDIZIONE INTERNA] "Three more deserve a note" — seguono sei punti (`skt`, `al`, shortwave, livelli sotto terra, `sst`, `dl`) (§4, r.81-142)
S016 [VAGA] "Measured this way the emissivity came out identical in every cell" (spread 0.0000) — nessun timestep né popolazione (§4, r.88-90)
S017 [NUMERO SENZA FONTE] 99.98 % / 93.05 %, RMSE 0.0012 K / 0.084–0.119 K, p99 0.81 K, 2.79 K — non dice quali anni né quanti timestep per mese (§4, r.93-96)
S018 [GONFIATA] "at every timestep of every season" — la popolazione dei timestep (34, r.99) non è ripetuta per questo numero (§4, r.103)
S019 [NUMERO SENZA FONTE] "thirty times smaller than the physical cold bias" — con i numeri del file 1.6 K / 0.084–0.119 K ≈ 13–19, 1.6 K / 0.0012 K ≈ 1300; il fattore trenta non si ricava (§4, r.103-105)
S020 [NUMERO SENZA FONTE] bias `skt` −1.6 K, −3.2 K a mezzogiorno, +0.01 K su mare — senza periodo né popolazione (§4, r.105-106)
S021 [NUMERO SENZA FONTE] `al` 8–11 valori distinti, 1 171 937 punti (89.9 %) — non dice su quali file (§4, r.113-115)
S022 [VAGA] "an optical depth of 0.1 to 0.2 accounts for the size" — nessun calcolo o fonte (§4, r.121-122)
S023 [RIFERIMENTO INCOMPLETO] "the Tegen aerosol climatology" — nessuna citazione né versione (§4, r.121)
S024 [NUMERO SENZA FONTE] +8.5 %, +13.6 %, 1.1 %, −22 %, −39 % contro ERA5 — "Measured against ERA5" senza periodo né dominio di confronto (§4, r.122-125)
S025 [NUMERO SENZA FONTE] clamp 0.0 / 1e-9, 24–27 m, 47.6 % / 9 % — senza file né timestep (§4, r.129-135)
S026 [VAGA] "which is most of the land" — senza numero (§4, r.133)
S027 [VAGA] "ERA5's own `dl` does the same where the database is silent" — senza fonte (§4, r.142)
S028 [NUMERO SENZA FONTE] `mucin` 4 %–29 % del dominio, "least in winter" — senza periodo né campione (§5, r.152)
S029 [CONTRADDIZIONE INTERNA] celle con `tvl` mancante = 15.8 % di quelle con `cvl > 0` (r.157) contro 16.2 % delle celle vegetate (r.387) per la stessa esclusione degli arbusteti; popolazioni non chiarite (§5, r.157; §8.tv, r.387)
S030 [VAGA] "no boundary-layer height (the PBL scheme is YSU, non-local)" — la parentesi è data come ragione senza dire perché ne impedisca l'altezza (§6, r.162)
S031 [RIFERIMENTO INCOMPLETO] "the FAO clay/sand thresholds" — nessuna citazione né versione (§6, r.195)
S032 [RIFERIMENTO INCOMPLETO] "ECMWF code table 4.234" e "WMO table 4.213" — senza versione o edizione (§6, r.192, r.198)
S033 [VAGA] "Its land use was verified against the hourly output ... 100.00 %" — non dice su quali file né quanti timestep (§8, r.357-358)
S034 [VAGA] riga *organic material* → 6: la precedenza rispetto alle soglie di argilla/sabbia non è detta (§8.slt, r.404)
S035 [RIFERIMENTO INCOMPLETO] "the IGBP class definitions of tree cover" — nessuna citazione (§8.tv, r.364)
