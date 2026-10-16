# Scheda: MISSING_VARIABLES.md
Fonte: /leonardo/home/userexternal/lmonaco0/CHAPTER/MISSING_VARIABLES.md (236 righe), letta il 2026-09-29

Convenzione per le sezioni: §0 = intestazione (r.1-21); §1-§6 come nell'originale; la parte
"Dropped on 2026-09-17 and reinstated on 2026-09-18" / "Still not published" (r.105-121) sta dopo
il separatore di §4 e prima di §5, senza titolo propria: è indicata come §4.

## 1. Affermazioni

### §0 Intestazione
A001 Data del documento: 2026-09-17 [SENZA FONTE] (§0, r.3)
A002 Ambito: la lista di variabili richiesta per la rianalisi regionale CHAPTER (atmosfera, statici, superficie terrestre, onde, ghiaccio marino, oceano superficiale) [SENZA FONTE] (§0, r.3-4)
A003 La nota risponde a quali variabili richieste si possono mettere nell'archivio GRIB, quali ottenere per altra via, quali non sono nei dati [SENZA FONTE] (§0, r.6-8)
A004 Da leggere prima di impegnarsi in una ri-conversione dell'intero archivio [SENZA FONTE] (§0, r.8-9)
A005 La ri-conversione costa diversi giorni di trasferimento dati e va fatta una sola volta [SENZA FONTE] (§0, r.9)
A006 Tutto è stato verificato sui file reali, non sulla documentazione [SUPPORTATA: attributi globali dei wrfout; timestep indipendenti estate 2019, estate 2024 00/06/12/13/14/18/23 UTC, marzo 2024] (§0, r.11-14)
A007 Configurazione del modello letta dagli attributi globali dei wrfout [SUPPORTATA: attributi globali wrfout] (§0, r.11-12)
A008 Ogni campo controllato per valori reali su timestep indipendenti, per non scambiare campi identicamente nulli per dati utilizzabili [SUPPORTATA: campione estate 2019, estate 2024, marzo 2024] (§0, r.12-14)
A009 Campi accumulati controllati anche per monotonia entro una run [SENZA FONTE] (§0, r.15)
A010 Ogni identificativo di parametro ECMWF passato avanti e indietro nell'encoder GRIB per confermare nome e unità [SENZA FONTE] (§0, r.15-16)
A011 `CHAPTER_VARIABLES.md` è il riferimento per ciò che l'archivio contiene [SUPPORTATA: CHAPTER_VARIABLES.md] (§0, r.18-19)
A012 `CHAPTER_KNOWN_PROPERTIES.md` raccoglie proprietà e bias misurati delle variabili fornite, inclusi i numeri dietro diversi caveat di §5 [SUPPORTATA: CHAPTER_KNOWN_PROPERTIES.md] (§0, r.19-21)

### §1 Summary (tabella T001, una voce per riga)
A013 Atmosfera, superficie (24 variabili + wind shear): 22 di 24 consegnate, più wind shear [SENZA FONTE] (§1, r.29)
A014 Atmosfera, superficie: mancano solo le due componenti della raffica, escluse per decisione [SENZA FONTE] (§1, r.29)
A015 Atmosfera, livelli di pressione (9 variabili × 13 livelli): tutte consegnate [SENZA FONTE] (§1, r.30)
A016 Livelli di pressione: in più entrambe le forme della velocità verticale (`w` in Pa/s, `wz` in m/s) [SENZA FONTE] (§1, r.30)
A017 Livelli di pressione: in più tre campi ERA5, frazione nuvolosa `cc`, contenuto d'acqua di pioggia `crwc` e di neve `cswc` [SENZA FONTE] (§1, r.30)
A018 TKE a 3 livelli di quota: non disponibile, il modello non la calcola [SENZA FONTE] (§1, r.31)
A019 Statici, orografia: consegnata [SENZA FONTE] (§1, r.32)
A020 Statici, land-use / land-cover: solo categoria dominante, mai frazioni; il file che contiene le frazioni non esiste più [SENZA FONTE] (§1, r.33)
A021 Superficie terrestre: consegnato il sottoinsieme che esiste, con nomi ERA5 [SENZA FONTE] (§1, r.34)
A022 Superficie terrestre: ora incluso bilancio radiativo completo, runoff, copertura nevosa, temperatura della neve, albedo, stress superficiale, suddivisione vegetazione alta/bassa [SENZA FONTE] (§1, r.34)
A023 Onde (SWH, periodo, direzione, Cd dipendente dalle onde): non disponibili, nessun modello d'onda [SENZA FONTE] (§1, r.35)
A024 Ghiaccio marino: concentrazione consegnata [SENZA FONTE] (§1, r.36)
A025 Ghiaccio marino: spessore, neve sul ghiaccio, temperatura del ghiaccio e albedo non disponibili [SENZA FONTE] (§1, r.36)
A026 Oceano superficiale: SST consegnata [SENZA FONTE] (§1, r.37)
A027 Oceano superficiale: SSH e correnti non disponibili [SENZA FONTE] (§1, r.37)

### §2 Why: how the archive is produced
A028 L'archivio è prodotto da output orario WRF 4.1.1 [SENZA FONTE] (§2, r.43)
A029 Dominio d02, Mercator, 1641 × 1353 punti a 3 km, 49 livelli verticali [SENZA FONTE] (§2, r.43-44)
A030 La configurazione rilevante è identica in tutti i periodi controllati (2019, marzo 2024, luglio 2024) [SUPPORTATA: periodi 2019, marzo 2024, luglio 2024] (§2, r.44-45)
A031 `BL_PBL_PHYSICS` = 1 (YSU): schema non locale, nessuna TKE prognostica [SUPPORTATA: namelist BL_PBL_PHYSICS=1] (§2, r.49)
A032 `PBLH` non è stato scritto in output [SUPPORTATA: namelist BL_PBL_PHYSICS=1 (riga di tabella)] (§2, r.49)
A033 `KM_OPT` = 4: nessun array prognostico di energia cinetica turbolenta [SUPPORTATA: namelist KM_OPT=4] (§2, r.50)
A034 `SF_OCEAN_PHYSICS` = 0: l'oceano non è simulato; niente correnti, niente altezza della superficie del mare, niente strato rimescolato [SUPPORTATA: namelist SF_OCEAN_PHYSICS=0] (§2, r.51)
A035 Nessun modello d'onda: nessun campo d'onda di alcun tipo, quindi nessun coefficiente di drag dipendente dalle onde [SENZA FONTE] (§2, r.52)
A036 `SST_UPDATE` = 0: SST costante entro ogni run di 24 h, re-inizializzata a ogni run giornaliera [SUPPORTATA: namelist SST_UPDATE=0] (§2, r.53)
A037 `CU_PHYSICS` = 0: convection-permitting; `RAINC` identicamente zero, precipitazione totale completa in `RAINNC` [SUPPORTATA: namelist CU_PHYSICS=0] (§2, r.54)
A038 `MP_PHYSICS` = 6 (WSM6): disponibili nubi, pioggia, ghiaccio, neve e graupel; nessuna categoria grandine [SUPPORTATA: namelist MP_PHYSICS=6] (§2, r.55)
A039 `ICLOUD` = 1 (Xu-Randall): frazione nuvolosa continua, non un flag 0/1 [SUPPORTATA: namelist ICLOUD=1] (§2, r.56)
A040 `SF_SURFACE_PHYSICS` = 3 (RUC): 6 livelli di suolo a 0, 5, 20, 40, 160, 300 cm; ERA5 usa 4 strati [SUPPORTATA: namelist SF_SURFACE_PHYSICS=3] (§2, r.57)
A041 `SF_LAKE_PHYSICS`, `SF_URBAN_PHYSICS` = 0, 0: nessun modello di lago, nessun canopy urbano [SUPPORTATA: namelist SF_LAKE_PHYSICS=0, SF_URBAN_PHYSICS=0] (§2, r.58)
A042 Alcuni campi presenti nei file sono identicamente zero su ogni timestep campionato, quindi non utilizzabili [SUPPORTATA: campione di timestep di §0] (§2, r.60-61)
A043 Campi identicamente zero: `ACHFX`, `ACLHF`, `ACGRDFLX`, `NOAHRES`, `SSTSK`, `SST_INPUT`, `SWNORM`, `ACSNOW`, `HAILNC`, `RAINC`, `RAINSH`, `PREC_ACC_C`, e il longwave discendente al top dell'atmosfera [SUPPORTATA: campione di timestep di §0] (§2, r.62-63)
A044 Nessuno di questi campi sarà scritto nei file GRIB [SENZA FONTE] (§2, r.63-64)

### §3 Variables we can obtain by another route
A045 Le variabili di §3 non sono nell'output del modello ma esiste un modo difendibile per ottenerle [SENZA FONTE] (§3, r.70-71)
A046 Nessuna di esse è implementata; ciascuna richiede prima una decisione [SENZA FONTE] (§3, r.71)
A047 L'albedo superficiale è ora consegnato: `al` (fondo senza neve) e `fal` (rapporto effettivo all-sky) [SENZA FONTE] (§3, r.72-73)
A048 La copertura del suolo frazionaria è ora consegnata [SENZA FONTE] (§3, r.73-74)
A049 Il file statico `geo_em.d02`, registrato qui come irrecuperabile, è stato ottenuto da LRZ il 2026-09-18 [SENZA FONTE] (§3, r.74-75)
A050 `geo_em.d02` è quello della run stessa: il suo land use concorda con la categoria dominante del modello sul 100.00 % dei punti, escluso il recode dei laghi [SENZA FONTE] (§3, r.75-76)
A051 `geo_em.d02` ha portato `cvl`, `cvh`, `tvl`, `tvh`, `slt`, `cl` e `dl` [SENZA FONTE] (§3, r.76)
A052 Temperatura superficiale del ghiaccio marino: usare la skin temperature già derivata, ristretta ai punti con concentrazione di ghiaccio > 0 [SENZA FONTE] (§3, r.80)
A053 Temperatura del ghiaccio marino: confidenza media; è una skin temperature radiativa, coerente con l'emissione longwave del modello, non una temperatura dedicata della superficie del ghiaccio [SENZA FONTE] (§3, r.80)
A054 Temperatura del ghiaccio marino: costo nullo [SENZA FONTE] (§3, r.80)
A055 Coefficiente di drag senza effetto onde: dalla lunghezza di rugosità del modello, `Cd = (κ / ln(10/z0))²` [SENZA FONTE] (§3, r.81)
A056 Coefficiente di drag senza onde: confidenza "Exact", è esattamente il drag usato dalla simulazione (Charnock, nessun accoppiamento d'onda) [SENZA FONTE] (§3, r.81)
A057 Coefficiente di drag senza onde: costo nullo [SENZA FONTE] (§3, r.81)
A058 Altezza dello strato limite: numero di Richardson bulk sul profilo di temperatura potenziale virtuale; tutti i campi necessari sono presenti [SENZA FONTE] (§3, r.82)
A059 Altezza dello strato limite: confidenza "Reasonable", stessa classe di diagnostica che il modello applicherebbe [SENZA FONTE] (§3, r.82)
A060 Altezza dello strato limite: costo nullo [SENZA FONTE] (§3, r.82)

### §4 Variables we cannot provide (tabella T004, una voce per riga)
A061 `10efg`, `10nfg`: esiste solo un proxy della magnitudine della raffica, ed è il massimo del vento risolto, non uno schema di raffica [SENZA FONTE] (§4, r.90)
A062 `10efg`, `10nfg`: la direzione andrebbe assunta uguale al vento medio, a un istante che non coincide col massimo [SENZA FONTE] (§4, r.90)
A063 `10efg`, `10nfg`: scomporre la magnitudine lungo il vento a 10 m è possibile ed economico, ma giudicato troppo debole per pubblicarlo con nomi ERA5; deciso di non produrle [SENZA FONTE] (§4, r.90)
A064 TKE: lo schema PBL è YSU, non locale, senza energia cinetica turbolenta; nemmeno l'opzione di diffusione ne produce una; il campo non esiste a nessuna quota [SUPPORTATA: namelist BL_PBL_PHYSICS=1, KM_OPT=4 (tabella §2)] (§4, r.91)
A065 TKE: unica via, rifare la run WRF con uno schema PBL con TKE (MYNN o MYJ) [SENZA FONTE] (§4, r.91)
A066 TKE: una stima da teoria della similarità richiederebbe altezza dello strato limite e flusso di calore superficiale, entrambi mancanti; gli errori si compongono; sembrerebbe plausibile ma non coerente con la simulazione [SENZA FONTE] (§4, r.91)
A067 Altezza significativa d'onda, periodo medio, direzione: nessun modello d'onda accoppiato all'atmosfera [SENZA FONTE] (§4, r.92)
A068 Onde: unica via, una run di modello d'onda o una rianalisi d'onda esterna (ERA5 waves a ~31 km), che perde il dettaglio costiero che motiva un prodotto a 3 km [SENZA FONTE] (§4, r.92)
A069 Coefficiente di drag con effetto onde: lo scambio superficiale ha usato la rugosità di Charnock senza stato del mare [SENZA FONTE] (§4, r.93)
A070 Coefficiente di drag con onde: come sopra; il coefficiente senza onde è disponibile (§3) [SENZA FONTE] (§4, r.93)
A071 Altezza della superficie del mare, correnti (u, v): l'oceano non è simulato [SUPPORTATA: namelist SF_OCEAN_PHYSICS=0 (tabella §2)] (§4, r.94)
A072 SSH e correnti: unica via, una rianalisi oceanica (es. CMEMS), rigrigliata [SENZA FONTE] (§4, r.94)
A073 Spessore del ghiaccio marino, spessore della neve sul ghiaccio: non simulati; il ghiaccio marino entra solo come campo di concentrazione al contorno [SENZA FONTE] (§4, r.95)
A074 Spessore del ghiaccio / neve sul ghiaccio: unica via, un prodotto esterno di ghiaccio marino [SENZA FONTE] (§4, r.95)
A075 Albedo del ghiaccio marino come proprietà prognostica: non simulato [SENZA FONTE] (§4, r.96)
A076 Albedo del ghiaccio marino: approssimabile radiativamente (§3), ma non come variabile di un modello di ghiaccio [SENZA FONTE] (§4, r.96)
A077 Snowmelt: il campo esiste (`ACSNOM`) ma non è un accumulatore monotono; singoli punti tornano a zero entro una run [SUPPORTATA: misura -7.26 mm rispetto alle 00 UTC del 2024-07-01] (§4, r.97)
A078 Snowmelt: non può essere riferito alle 00 UTC come le altre accumulazioni; pubblicato col nome ERA5 sarebbe sbagliato [SENZA FONTE] (§4, r.97)
A079 Snowmelt: servirebbe la fusione diagnosticata per timestep dentro il modello [SENZA FONTE] (§4, r.97)
A080 Flussi di calore sensibile e latente: il modello li ha calcolati e l'output non li contiene [SUPPORTATA: namelist isfflx = 1] (§4, r.98)
A081 `isfflx = 1`: i flussi sono stati prodotti a ogni timestep; non scritti nello stream di history [SUPPORTATA: namelist isfflx = 1] (§4, r.98)
A082 Non esiste da nessuna parte un output non ridotto [SENZA FONTE] (§4, r.98)
A083 `ACHFX`/`ACLHF` identicamente zero perché accumulatori Noah in una run RUC, non per un'impostazione di bucket [SENZA FONTE] (§4, r.98)
A084 Flussi di calore: solo una nuova run che li scriva [SENZA FONTE] (§4, r.98)
A085 Ricostruzione dal bilancio energetico superficiale fallisce: manca anche il flusso di calore nel suolo, due incognite in un'equazione [SENZA FONTE] (§4, r.98)
A086 Skin temperature come variabile del modello: `TSK` non scritto, taglio deliberato dello stream di output, non un incidente [SENZA FONTE] (§4, r.99)
A087 Si fornisce già `skt`, ottenuta invertendo il flusso longwave ascendente (§5) [SENZA FONTE] (§4, r.99)
A088 `skt` sull'acqua recupera la SST del modello a 0.0005 K [SENZA FONTE] (§4, r.99)
A089 `mx2t`, `mn2t`: `output_diagnostics = 0`, WRF non ha mai scritto `T2MAX`/`T2MIN` [SUPPORTATA: namelist output_diagnostics = 0] (§4, r.100)
A090 Un campionamento orario di `T2` non è l'estremo entro l'ora del modello; nessun lavoro sul converter li produce [SENZA FONTE] (§4, r.100)
A091 `mx2t`, `mn2t`: solo una nuova run con `output_diagnostics = 1` [SENZA FONTE] (§4, r.100)
A092 `nwp_diagnostics = 1` è attivo e dà `WSPD10MAX` e altri sei massimi orari; la run porta estremi entro l'ora, non per la temperatura [SUPPORTATA: namelist nwp_diagnostics = 1] (§4, r.100)
A093 `blh`: YSU ne diagnostica una; non è stata scritta nello stream di history; il limite è l'output, non lo schema [SENZA FONTE] (§4, r.101)
A094 `blh`: una nuova run che scriva `PBLH`, o la diagnostica di Richardson bulk di §3, stessa classe di diagnostica del modello [SENZA FONTE] (§4, r.101)

### §4 Dropped / reinstated (tabella T005, una voce per riga)
A095 Suolo, tvl/tvh/slt e cvl/cvh eliminati il 2026-09-17 e reintegrati il 2026-09-18, quando l'obiezione ha avuto risposta [SENZA FONTE] (§4, r.105)
A096 `swvl1-4`, `stl1-4`: lo schema porta valori puntuali a 0, 5, 20, 40, 160 e 300 cm; i quattro strati ERA5 sono medie su 0-7, 7-28, 28-100 e 100-289 cm [SENZA FONTE] (§4, r.109)
A097 `swvl1-4`, `stl1-4`: l'obiezione era contro il rietichettare i valori puntuali, e resta valida [SENZA FONTE] (§4, r.109)
A098 `swvl1-4`, `stl1-4`: si possono integrare; schema a livelli con profilo lineare tra i nodi [SENZA FONTE] (§4, r.109)
A099 La colonna ERA5 sta dentro i nodi (289 cm sopra il più profondo, 0 cm è il primo): ogni strato è l'integrale esatto, nulla è estrapolato [SENZA FONTE] (§4, r.109)
A100 `tvl`, `tvh`, `slt`: le categorie sono MODIS-IGBP e STATSGO di WRF, i paramId portano tabelle di codici ECMWF (motivo dell'esclusione) [SENZA FONTE] (§4, r.110)
A101 `slt` non è più una traduzione: i sette tipi ECMWF sono definiti da soglie di argilla/sabbia, il file statico porta le frazioni di argilla e sabbia, la definizione è applicata direttamente [SENZA FONTE] (§4, r.110)
A102 `tvl`/`tvh` usano una tabella, pubblicata per intero in `CHAPTER_VARIABLES.pdf` §8 [SUPPORTATA: CHAPTER_VARIABLES.pdf §8] (§4, r.110)
A103 Ogni riga della tabella `tvl`/`tvh` è un'identità semantica [SUPPORTATA: CHAPTER_VARIABLES.pdf §8] (§4, r.110)
A104 L'unica domanda a cui MODIS non risponde (arbusti sempreverdi vs decidui) è lasciata mancante invece che indovinata [SENZA FONTE] (§4, r.110)
A105 `cvl`, `cvh`: prima poggiavano su una categoria dominante per cella, mentre ERA5 lascia coesistere vegetazione bassa e alta [SENZA FONTE] (§4, r.111)
A106 `cvl`, `cvh`: il file statico ha la copertura frazionaria, sono somme sulle classi basse e alte, la stessa quantità intesa da ERA5 [SENZA FONTE] (§4, r.111)
A107 `cvl`, `cvh`: era l'obiezione giusta; il 17.9 % delle celle di terra ha entrambe sopra il 5 %, la categoria dominante tiene in media solo il 90.1 % di una cella [SENZA FONTE] (§4, r.111)

### §4 Still not published (tabella T006, una voce per riga)
A108 `lai_lv`, `lai_hv`: il modello porta un solo LAI per cella; ERA5 ne vuole uno per classe di vegetazione, definito per unità di area vegetata [SENZA FONTE] (§4, r.117)
A109 `lai_lv`, `lai_hv`: ogni suddivisione tra i due sarebbe un'assunzione nostra [SENZA FONTE] (§4, r.117)
A110 Il LAI del modello si può consegnare col suo nome se richiesto [SENZA FONTE] (§4, r.117)
A111 `anor`, `isor`: il file statico porta i parametri di asimmetria e lunghezza efficace di Kim-Arakawa [SENZA FONTE] (§4, r.118)
A112 `anor`, `isor`: angolo e anisotropia ECMWF vengono dall'autostruttura della covarianza del gradiente del terreno; correlati, non uguali; la differenza non sta in una riga [SENZA FONTE] (§4, r.118)
A113 Se richiesti, i campi WRF sottostanti esistono e si possono consegnare coi loro nomi (`LAI`, `VEGFRA`, `OA1-4`, `OL1-4`), senza affermare equivalenza ERA5 [SENZA FONTE] (§4, r.120-121)

### §5 Caveats
A114 I caveat di §5 contano per l'uso corretto e vanno letti con la lista delle variabili [SENZA FONTE] (§5, r.125)
A115 Copertura nuvolosa frazionaria; una bozza precedente della nota diceva binaria, ed era sbagliato [SENZA FONTE] (§5, r.127-128)
A116 Schema Xu-Randall, campo genuinamente continuo: su un sotto-dominio 500 × 600 solo il 18-22 % dei punti nuvolosi è esattamente a 1, il resto sull'intervallo 0-1 [SUPPORTATA: sotto-dominio 500 × 600] (§5, r.129-130)
A117 Copertura nuvolosa totale, alta, media e bassa sono sovrapposizioni maximum-random di quel campo [SENZA FONTE] (§5, r.130-131)
A118 La frazione nuvolosa è consegnata anche per livello di pressione come `cc` [SENZA FONTE] (§5, r.131-132)
A119 SST costante entro ogni giorno: ogni run giornaliera è inizializzata con SST fissa e non la aggiorna; risoluzione temporale giornaliera, non oraria [SUPPORTATA: namelist SST_UPDATE=0 (tabella §2)] (§5, r.133-134)
A120 Skin temperature derivata, non modellata: `TSK` non scritto, ottenuta invertendo il flusso longwave ascendente [SENZA FONTE] (§5, r.135-136)
A121 Emissività della categoria di land-use dominante (VEGPARM.TBL, da 0.88 urbano a 0.98 acqua) [SUPPORTATA: VEGPARM.TBL] (§5, r.136-138)
A122 Esatta dove la risposta è nota: sull'acqua la skin temperature del modello è la SST e l'inversione la recupera a 0.005 K [SENZA FONTE] (§5, r.138-139)
A123 Coincide col livello di suolo a 0 cm a meno di 1 K RMSE sulla terra senza neve [SENZA FONTE] (§5, r.139-140)
A124 Sulla neve l'emissività effettivamente usata dallo schema non può essere ricostruita: circa 0.8 K di incertezza residua [SENZA FONTE] (§5, r.140-141)
A125 La pendenza dell'orografia è quella risolta; `slor` ERA5 è un parametro sub-griglia dello schema di form-drag; si scrive la pendenza del terreno risolto a 3 km [SENZA FONTE] (§5, r.142-143)
A126 `sdor` è invece una genuina deviazione standard sub-griglia, calcolata dal pre-processore [SENZA FONTE] (§5, r.143-144)
A127 Contenuti d'acqua specifici, non rapporti di mescolanza: WRF porta rapporti di mescolanza per kg di aria secca [SENZA FONTE] (§5, r.145-146)
A128 `clwc`, `ciwc`, `crwc`, `cswc` e gli integrali di colonna convertiti in contenuti specifici, per kg di aria umida, come richiesto dalle definizioni ECMWF [SUPPORTATA: definizioni ECMWF (senza versione)] (§5, r.146-147)
A129 Correzione dello 0.8 % in mediana [SENZA FONTE] (§5, r.147)
A130 CIN calcolata per costruzione solo dove CAPE supera 100 J/kg [SENZA FONTE] (§5, r.148-149)
A131 CAPE non definita nei pochi percento di punti senza livello di equilibrio [SENZA FONTE] (§5, r.149-150)
A132 In quei punti si scrive zero invece di un valore mancante, per mantenere i campi densi [SENZA FONTE] (§5, r.150-151)
A133 Zero è anche la lettura fisicamente corretta (nessuna inibizione, nessuna energia disponibile) [SENZA FONTE] (§5, r.151-152)
A134 Richiesta: se si preferisce il flag mancante, dirlo ora [SENZA FONTE] (§5, r.152)
A135 CAPE e CIN sono most-unstable, dalla particella di 500 m di spessore con la massima temperatura potenziale equivalente nei 3 km più bassi, non surface-based [SENZA FONTE] (§5, r.153-154)
A136 Il campo raffica non è una parametrizzazione di raffica: massimo della velocità del vento risolto a 10 m sull'ora di output [SENZA FONTE] (§5, r.155-156)
A137 È il miglior proxy che la run possa dare [SENZA FONTE] (§5, r.157)
A138 `10fg` ERA5 è una raffica parametrizzata, circa 1.6 volte il proprio vento medio [SENZA FONTE] (§5, r.157)
A139 Sul campione di audit: il nostro è 0.625 del `10fg` ERA5 e 0.644 del suo `i10fg` istantaneo, correlazione 0.81 [SUPPORTATA: campione di audit (non descritto)] (§5, r.158-159)
A140 Rispetto al nostro vento istantaneo a 10 m nello stesso file sta a 1.004-1.032: il massimo orario aggiunge da mezzo a tre per cento [SUPPORTATA: campione di audit (non descritto)] (§5, r.159-161)
A141 Letto come raffica sottostima di circa il 38 %; differenza di grandezza, non bias da correggere [SENZA FONTE] (§5, r.161-162)
A142 La finestra di un'ora dichiarata è giusta solo l'88 % delle volte [SENZA FONTE] (§5, r.162-163)
A143 Entrambi descritti per intero, coi numeri, in `CHAPTER_KNOWN_PROPERTIES.md` §5 [SUPPORTATA: CHAPTER_KNOWN_PROPERTIES.md §5] (§5, r.163-164)
A144 La maschera terra/mare cambia con la stagione: dove si forma ghiaccio marino il modello riclassifica il punto come ghiaccio [SENZA FONTE] (§5, r.165-166)
A145 Lì cambiano maschera di terra, tipi di vegetazione e suolo, albedo di fondo (2469 punti il 20 marzo 2024, esattamente i punti di ghiaccio marino) [SUPPORTATA: file del 20 marzo 2024] (§5, r.166-167)
A146 Questi campi sono scritti in ogni file orario e non vanno trattati come un unico campo statico per l'archivio [SENZA FONTE] (§5, r.167-168)
A147 Stress superficiale è un diagnostico, non un output del modello: componenti est e nord ricostruite come densità × velocità d'attrito al quadrato, allineate al vento a 10 m [SENZA FONTE] (§5, r.169-171)
A148 La velocità d'attrito è quella del modello, stessa teoria di similarità della simulazione; l'allineamento col vento medio è un'assunzione [SENZA FONTE] (§5, r.171-172)
A149 La temperatura della neve esiste solo dove c'è neve: è la temperatura al top della colonna neve/suolo; lontano dalla neve è una temperatura del suolo [SENZA FONTE] (§5, r.173-175)
A150 Temperatura della neve scritta come mancante fuori dalla neve [SENZA FONTE] (§5, r.175)
A151 `al` è il fondo climatologico senza neve con cui il modello è stato inizializzato [SENZA FONTE] (§5, r.176-177)
A152 `fal` è il rapporto effettivo tra shortwave ascendente e discendente, quello usato dalla simulazione [SENZA FONTE] (§5, r.177-178)
A153 `fal` indefinito di notte, scritto come mancante sotto 50 W/m² di shortwave incidente [SENZA FONTE] (§5, r.178-179)
A154 Tre variabili di runoff portano l'informazione di un solo campo; la componente sub-superficiale è essenzialmente vuota a scala giornaliera [SUPPORTATA: campione di audit, 18 ore] (§5, r.180-181)
A155 `ssro` identicamente zero su cinque delle diciotto ore campionate [SUPPORTATA: campione di audit, 18 ore] (§5, r.181-182)
A156 Dove non è zero, `ssro` è non nullo al massimo in 19 punti su 2 220 273 [SUPPORTATA: campione di audit, 18 ore] (§5, r.182-183)
A157 Media di dominio di `ssro` da quattro a otto ordini di grandezza sotto `sro` [SUPPORTATA: campione di audit, 18 ore] (§5, r.183)
A158 `ro` uguale a `sro` a quattro cifre significative a ogni timestep [SUPPORTATA: campione di audit, 18 ore] (§5, r.184)
A159 L'identità `ro = sro + ssro` vale a 3.7e-9 m; nel secondo termine non c'è niente [SUPPORTATA: campione di audit, 18 ore] (§5, r.184-185)
A160 La causa è il riferimento temporale, non la conversione: il contatore di drenaggio è vivo ma si muove appena entro un giorno, e `ssro` è accumulato dalle 00 UTC [SENZA FONTE] (§5, r.185-187)
A161 Rispetto a ERA5 la ripartizione è opposta: `sro` 1.0–4.6× ERA5, `ssro` 0.000–0.004×, `ro` 0.19–0.85× [SENZA FONTE] (§5, r.187-188)
A162 Non chiudere un bilancio idrico assumendo che l'archivio porti un termine di drenaggio [SENZA FONTE] (§5, r.188-189)
A163 Tutte e tre pubblicate perché `ro` è il totale canonico ERA5; `ro` e `sro` sono messaggi consapevolmente duplicati [SENZA FONTE] (§5, r.189-190)
A164 Nessun campo graupel, e `tcw` lo contiene comunque [SENZA FONTE] (§5, r.191)
A165 ECMWF definisce `tcw` come somma di cinque specie (vapore, liquido, ghiaccio, pioggia, neve); il nostro è la somma di sei, graupel incluso [SUPPORTATA: definizione ECMWF (senza versione)] (§5, r.191-193)
A166 ECMWF definisce `260028 grle` e `260001 tcolg`, ma ERA5 non pubblica nessuno dei due; quindi il graupel va solo dentro `tcw` [SENZA FONTE] (§5, r.193-194)
A167 Ricostruire `tcw` dalle cinque colonne componenti pubblicate non lo riproduce; la differenza è il graupel [SENZA FONTE] (§5, r.194-196)
A168 Graupel: 0.4 % del condensato nella media di dominio [SENZA FONTE] (§5, r.196)
A169 Graupel: fino a 26.5 kg/m² dentro una cella convettiva di luglio, più del resto del condensato della colonna messo insieme [SENZA FONTE] (§5, r.196-197)
A170 La pioggia esclude neve e graupel, non la grandine; la microfisica non ha categoria grandine [SUPPORTATA: namelist MP_PHYSICS=6 (tabella §2)] (§5, r.198-199)
A171 La pioggia è precipitazione totale meno neve meno graupel [SENZA FONTE] (§5, r.199)
A172 Il dewpoint a 2 m è ora in kelvin; l'archivio GRIB1 precedente lo scriveva in gradi Celsius sotto un parametro che ECMWF definisce in kelvin [SENZA FONTE] (§5, r.200-201)
A173 Chi legge `2d` dai vecchi file deve aggiungere +273.15 [SENZA FONTE] (§5, r.201)
A174 Campi accumulati riferiti alle 00 UTC dello stesso giorno, non all'inizio della run; esattamente zero alle 00 UTC [SENZA FONTE] (§5, r.202-203)
A175 Nei GRIB hanno step di accumulazione 0-H con tempo di riferimento 00 UTC; la validità è il timestep stesso [SENZA FONTE] (§5, r.203-204)
A176 Eccezione il massimo del vento a 10 m: copre solo l'ora precedente, perché il modello lo azzera a ogni output [SENZA FONTE] (§5, r.204-205)
A177 La geolocalizzazione è ora esatta a ~2 m; la griglia dichiara la terra sferica di raggio 6370 km su cui WRF integra [SENZA FONTE] (§5, r.206-207)
A178 I file GRIB1 precedenti non potevano esprimerlo ed erano sbagliati fino a ~1.1 km al bordo nord del dominio [SENZA FONTE] (§5, r.207-208)

### §6 What we need from you
A179 Le questioni su componenti della raffica e TKE sono chiuse: nessuna delle due è prodotta [SENZA FONTE] (§6, r.214-215)
A180 La questione del file statico `geo_em` è chiusa al contrario di quanto diceva il documento: ottenuto da LRZ il 2026-09-18, e tutto ciò che ne dipendeva è ora consegnato (§3, §4) [SENZA FONTE] (§6, r.215-217)
A181 La proposta originale della lista land-surface è andata persa [SENZA FONTE] (§6, r.219)
A182 Consegnati con nomi ERA5: umidità e temperatura del suolo (4 strati, vere medie di strato ERA5), profondità, densità, copertura e temperatura della neve, nevicata [SENZA FONTE] (§6, r.219-221)
A183 Consegnati: runoff superficiale, sub-superficiale e totale, contenuto del serbatoio di pelle [SENZA FONTE] (§6, r.221-222)
A184 Consegnati: copertura e tipo di vegetazione alta e bassa, tipo di suolo, copertura e profondità dei laghi [SENZA FONTE] (§6, r.222)
A185 Consegnati: velocità d'attrito, rugosità superficiale, i due albedo, le due componenti dello stress superficiale [SENZA FONTE] (§6, r.223-224)
A186 Consegnato il bilancio radiativo completo (discendente, netto e clear-sky, alla superficie e al top dell'atmosfera) [SENZA FONTE] (§6, r.224-225)
A187 Non consegnati della lista originale: leaf area index (una sola per cella vs una per classe ERA5) e snowmelt (non accumulatore monotono) [SENZA FONTE] (§6, r.225-227)
A188 Richiesta: confermare o modificare la lista land-surface [SENZA FONTE] (§6, r.228)
A189 Wind shear: si consegna attualmente lo shear bulk tra 10 m e 100 m [SENZA FONTE] (§6, r.229-230)
A190 Qualsiasi altra definizione di shear (strati fissi, per livello di pressione, bulk 0-6 km) è una modifica di una riga, da decidere prima della ri-conversione [SENZA FONTE] (§6, r.230-231)
A191 Si consegnano 13 livelli di pressione; ERA5 ne usa 37, di cui 29 dentro il dominio del modello [SENZA FONTE] (§6, r.232-233)
A192 Il top del modello è a 50 hPa, nulla sopra si può produrre [SENZA FONTE] (§6, r.233)
A193 Con 29 livelli il file orario passerebbe da ~0.8 GB a ~1.45 GB e un anno di archivio da 7.0 a 18.1 TB; per questo si sono tenuti 13 livelli [SENZA FONTE] (§6, r.233-235)
A194 Richiesta: dirlo ora se il set più denso conta [SENZA FONTE] (§6, r.235)

## 2. Dati numerici
N001 variabili atmosfera superficie richieste = 24 — più wind shear (§1, r.29) [SENZA FONTE]
N002 variabili atmosfera superficie consegnate = 22 di 24 (§1, r.29) [SENZA FONTE]
N003 variabili richieste a livelli di pressione = 9 × 13 livelli (§1, r.30) [SENZA FONTE]
N004 campi ERA5 extra a livelli di pressione = 3 (`cc`, `crwc`, `cswc`) (§1, r.30) [SENZA FONTE]
N005 livelli di quota richiesti per la TKE = 3 (§1, r.31) [SENZA FONTE]
N006 versione WRF = 4.1.1 (§2, r.43) [SENZA FONTE]
N007 dimensione griglia = 1641 × 1353 punti — dominio d02, Mercator (§2, r.43) [SENZA FONTE]
N008 risoluzione orizzontale = 3 km (§2, r.44) [SENZA FONTE]
N009 livelli verticali = 49 (§2, r.44) [SENZA FONTE]
N010 BL_PBL_PHYSICS = 1 (YSU) (§2, r.49) [fonte: attributi globali wrfout, r.11-12]
N011 KM_OPT = 4 (§2, r.50) [fonte: attributi globali wrfout]
N012 SF_OCEAN_PHYSICS = 0 (§2, r.51) [fonte: attributi globali wrfout]
N013 SST_UPDATE = 0 (§2, r.53) [fonte: attributi globali wrfout]
N014 durata di una run = 24 h (§2, r.53) [SENZA FONTE]
N015 CU_PHYSICS = 0 (§2, r.54) [fonte: attributi globali wrfout]
N016 MP_PHYSICS = 6 (WSM6) (§2, r.55) [fonte: attributi globali wrfout]
N017 ICLOUD = 1 (Xu-Randall) (§2, r.56) [fonte: attributi globali wrfout]
N018 SF_SURFACE_PHYSICS = 3 (RUC) (§2, r.57) [fonte: attributi globali wrfout]
N019 livelli di suolo RUC = 6, a 0, 5, 20, 40, 160, 300 cm (§2, r.57; ripetuto §4, r.109) [SENZA FONTE]
N020 strati di suolo ERA5 = 4 (§2, r.57) [SENZA FONTE]
N021 SF_LAKE_PHYSICS = 0, SF_URBAN_PHYSICS = 0 (§2, r.58) [fonte: attributi globali wrfout]
N022 campi identicamente zero elencati = 12 nominati + longwave discendente al top (§2, r.62-63) [fonte: campione di timestep di §0]
N023 accordo land use geo_em / categoria dominante del modello = 100.00 % dei punti — escluso il recode dei laghi (§3, r.75-76) [SENZA FONTE]
N024 campi portati da geo_em = 7 (`cvl`, `cvh`, `tvl`, `tvh`, `slt`, `cl`, `dl`) (§3, r.76) [SENZA FONTE]
N025 soglia concentrazione ghiaccio per temperatura del ghiaccio = > 0 (§3, r.80) [SENZA FONTE]
N026 quota nella formula di Cd = 10 (m, implicito in ln(10/z0)) (§3, r.81) [SENZA FONTE]
N027 risoluzione ERA5 waves = ~31 km (§4, r.92) [SENZA FONTE]
N028 decremento `ACSNOM` = -7.26 mm — rispetto alle 00 UTC del 2024-07-01 (§4, r.97) [fonte: misura sul 2024-07-01]
N029 isfflx = 1 (§4, r.98) [SENZA FONTE]
N030 skt vs SST sull'acqua = 0.0005 K (§4, r.99) [SENZA FONTE]
N031 output_diagnostics = 0 (§4, r.100) [SENZA FONTE]
N032 nwp_diagnostics = 1 — dà `WSPD10MAX` e altri sei massimi orari (§4, r.100) [SENZA FONTE]
N033 data eliminazione suolo/tipi/copertura = 2026-09-17; reintegro = 2026-09-18 (§4, r.105) [SENZA FONTE]
N034 strati ERA5 = 0-7, 7-28, 28-100, 100-289 cm (§4, r.109) [SENZA FONTE]
N035 tipi di suolo ECMWF = 7 (§4, r.110) [SENZA FONTE]
N036 celle di terra con vegetazione alta e bassa entrambe sopra il 5 % = 17.9 % (§4, r.111) [SENZA FONTE]
N037 quota media di cella tenuta dalla categoria dominante = 90.1 % (§4, r.111) [SENZA FONTE]
N038 sotto-dominio di verifica CLDFRA = 500 × 600 punti (§5, r.129) [SENZA FONTE]
N039 punti nuvolosi esattamente a 1 = 18-22 % — sotto-dominio 500 × 600 (§5, r.129-130) [fonte: sotto-dominio 500 × 600]
N040 emissività VEGPARM.TBL = da 0.88 (urbano) a 0.98 (acqua) (§5, r.137) [fonte: VEGPARM.TBL]
N041 skt vs SST sull'acqua = 0.005 K (§5, r.139) [SENZA FONTE]
N042 skt vs livello di suolo 0 cm = < 1 K RMSE — terra senza neve (§5, r.139-140) [SENZA FONTE]
N043 incertezza residua skt sulla neve = circa 0.8 K (§5, r.140-141) [SENZA FONTE]
N044 correzione mixing ratio -> contenuto specifico = 0.8 % in mediana (§5, r.147) [SENZA FONTE]
N045 soglia CAPE per il calcolo della CIN = 100 J/kg (§5, r.149) [SENZA FONTE]
N046 punti senza livello di equilibrio = "few percent" (§5, r.149-150) [SENZA FONTE]
N047 spessore particella most-unstable = 500 m; ricerca nei 3 km più bassi (§5, r.153-154) [SENZA FONTE]
N048 `10fg` ERA5 / proprio vento medio = circa 1.6 (§5, r.157) [SENZA FONTE]
N049 raffica CHAPTER / `10fg` ERA5 = 0.625 — campione di audit (§5, r.158) [fonte: campione di audit, non descritto]
N050 raffica CHAPTER / `i10fg` ERA5 = 0.644 — campione di audit (§5, r.159) [fonte: campione di audit, non descritto]
N051 correlazione raffica CHAPTER vs ERA5 = 0.81 (§5, r.159) [fonte: campione di audit, non descritto]
N052 raffica CHAPTER / vento istantaneo a 10 m CHAPTER = 1.004-1.032 — stesso file (§5, r.160) [fonte: campione di audit, non descritto]
N053 aggiunta del massimo orario = da mezzo a tre per cento (§5, r.160-161) [SENZA FONTE]
N054 sottostima della raffica letta come gust = circa 38 % (§5, r.161-162) [SENZA FONTE]
N055 finestra di un'ora di `10fg` giusta = 88 % delle volte (§5, r.162-163) [SENZA FONTE]
N056 punti riclassificati come ghiaccio = 2469 — 20 marzo 2024 (§5, r.167) [fonte: file del 20 marzo 2024]
N057 soglia shortwave incidente per `fal` = 50 W/m² (§5, r.179) [SENZA FONTE]
N058 ore campionate per il runoff = 18 (§5, r.182) [fonte: campione di audit]
N059 ore con `ssro` identicamente zero = 5 su 18 (§5, r.181-182) [fonte: campione di audit]
N060 punti con `ssro` non nullo = al massimo 19 su 2 220 273 (§5, r.182-183) [fonte: campione di audit]
N061 media di dominio `ssro` / `sro` = da quattro a otto ordini di grandezza sotto (§5, r.183) [fonte: campione di audit]
N062 accordo `ro` = `sro` = quattro cifre significative — ogni timestep (§5, r.184) [fonte: campione di audit]
N063 scarto identità `ro = sro + ssro` = 3.7e-9 m (§5, r.184-185) [fonte: campione di audit]
N064 `sro` / ERA5 = 1.0–4.6× (§5, r.188) [SENZA FONTE]
N065 `ssro` / ERA5 = 0.000–0.004× (§5, r.188) [SENZA FONTE]
N066 `ro` / ERA5 = 0.19–0.85× (§5, r.188) [SENZA FONTE]
N067 specie in `tcw` ECMWF = 5; in `tcw` CHAPTER = 6 (§5, r.192-193) [SENZA FONTE]
N068 paramId graupel = 260028 `grle`; colonna graupel = 260001 `tcolg` (§5, r.193) [SENZA FONTE]
N069 graupel / condensato = 0.4 % — media di dominio (§5, r.196) [SENZA FONTE]
N070 graupel massimo in colonna = 26.5 kg/m² — cella convettiva di luglio (§5, r.196-197) [SENZA FONTE]
N071 correzione dewpoint vecchi file = +273.15 (§5, r.201) [SENZA FONTE]
N072 errore di geolocalizzazione attuale = ~2 m (§5, r.206) [SENZA FONTE]
N073 raggio della terra sferica = 6370 km (§5, r.207) [SENZA FONTE]
N074 errore di geolocalizzazione GRIB1 = fino a ~1.1 km — bordo nord del dominio (§5, r.207-208) [SENZA FONTE]
N075 data ottenimento geo_em da LRZ = 2026-09-18 (§3, r.74-75; §6, r.216-217) [SENZA FONTE]
N076 numero strati suolo consegnati = 4 (§6, r.220) [SENZA FONTE]
N077 shear bulk = tra 10 m e 100 m (§6, r.230) [SENZA FONTE]
N078 livelli di pressione consegnati = 13 (§6, r.232) [SENZA FONTE]
N079 livelli ERA5 = 37, di cui 29 nel dominio del modello (§6, r.232-233) [SENZA FONTE]
N080 top del modello = 50 hPa (§6, r.233) [SENZA FONTE]
N081 file orario = ~0.8 GB a 13 livelli, ~1.45 GB a 29 livelli (§6, r.234) [SENZA FONTE]
N082 archivio annuale = 7.0 TB a 13 livelli, 18.1 TB a 29 livelli (§6, r.234-235) [SENZA FONTE]
N083 ore campionate estate 2024 = 00/06/12/13/14/18/23 UTC (§0, r.13) [fonte: descrizione del campione]

## 3. Equazioni
E001 $C_d = \left(\kappa / \ln(10/z_0)\right)^2$ — simboli: Cd = drag coefficient without wave effect; κ = non definito (costante di von Kármán, non nominata); z0 = the model's own roughness length (§3, r.81)
E002 $\mathrm{LWUPB} = \varepsilon \sigma T^4 + (1-\varepsilon)\,\mathrm{LWDN}$ — simboli: LWUPB = upward longwave flux; eps = emissivity of the dominant land-use category; sigma = non definito; T = skin temperature; LWDN = non definito (longwave discendente) (§5, r.136)
E003 $\tau = \rho\, u_*^2$ (componenti est/nord allineate al vento a 10 m) — simboli: "density × friction velocity squared" (§5, r.170-171)
E004 $ro = sro + ssro$ — simboli: ro = total runoff; sro = surface runoff; ssro = sub-surface runoff (§5, r.184-185)
E005 $tcw_{\mathrm{ECMWF}} = q_v + q_l + q_i + q_r + q_s$; $tcw_{\mathrm{CHAPTER}} = q_v + q_l + q_i + q_r + q_s + q_g$ — simboli: vapour, liquid, ice, rain, snow, graupel (colonne) (§5, r.192-193)
E006 $\mathrm{rain} = tp - \mathrm{snow} - \mathrm{graupel}$ — simboli: "total precipitation minus snow minus graupel" (§5, r.199)
E007 $2d_{\mathrm{K}} = 2d_{^\circ\mathrm{C}} + 273.15$ — simboli: 2d = 2 m dewpoint dai vecchi file GRIB1 (§5, r.201)

## 4. Riferimenti bibliografici
R001 [`CHAPTER_VARIABLES.md`](CHAPTER_VARIABLES.md) (§0, r.18)
R002 [`CHAPTER_KNOWN_PROPERTIES.md`](CHAPTER_KNOWN_PROPERTIES.md) (§0, r.19)
R003 WRF 4.1.1 (§2, r.43)
R004 ERA5 waves at ~31 km (§4, r.92)
R005 an ocean reanalysis (e.g. CMEMS) (§4, r.94)
R006 `CHAPTER_VARIABLES.pdf` §8 (§4, r.110)
R007 VEGPARM.TBL (§5, r.137)
R008 ECMWF definitions ("as their ECMWF definitions require") (§5, r.146-147)
R009 `CHAPTER_KNOWN_PROPERTIES.md` §5 (§5, r.164)
R010 ECMWF defines `tcw` / `260028 grle` / `260001 tcolg` (§5, r.191-193)

## 5. Figure e tabelle
T001 Tabella "Summary": colonne `requested block` | `verdict`; 9 righe (atmosfera superficie; livelli di pressione; TKE; orografia; land-use/land-cover; land-surface; onde; ghiaccio marino; oceano superficiale); verdetto di consegna per blocco richiesto (§1, r.27-37)
T002 Tabella configurazione: colonne `option` | `value` | `consequence for this list`; 10 righe (BL_PBL_PHYSICS, KM_OPT, SF_OCEAN_PHYSICS, nessun modello d'onda, SST_UPDATE, CU_PHYSICS, MP_PHYSICS, ICLOUD, SF_SURFACE_PHYSICS, SF_LAKE/URBAN_PHYSICS); opzioni WRF e conseguenze (§2, r.47-58)
T003 Tabella variabili ottenibili per altra via: colonne `variable` | `route` | `confidence` | `cost`; 3 righe (temperatura superficie ghiaccio marino, drag senza onde, altezza PBL) (§3, r.78-82)
T004 Tabella variabili non fornibili: colonne `variable` | `why` | `the only way to get it`; 12 righe (10efg/10nfg, TKE, onde, drag con onde, SSH/correnti, spessore ghiaccio/neve sul ghiaccio, albedo ghiaccio, snowmelt, flussi sensibile/latente, TSK, mx2t/mn2t, blh) (§4, r.88-101)
T005 Tabella eliminati e reintegrati: colonne `Variable` | `Why it was dropped` | `Why it is now published`; 3 righe (swvl1-4/stl1-4, tvl/tvh/slt, cvl/cvh) (§4, r.107-111)
T006 Tabella "Still not published": colonne `Variable` | `Why`; 2 righe (lai_lv/lai_hv, anor/isor) (§4, r.115-118)

## 6. Termini tecnici
G001 GRIB archive — non definito (§0, r.7)
G002 wrfout — non definito (§0, r.12)
G003 TKE — turbulent kinetic energy (§1, r.31; §2, r.50)
G004 wind shear — bulk 10 m to 100 m shear (§6, r.229-230)
G005 `w`, `wz` — vertical velocity in Pa/s e in m/s (§1, r.30)
G006 `cc`, `crwc`, `cswc` — cloud fraction, rain water content, snow water content (§1, r.30)
G007 SWH — significant wave height (§1, r.35; §4, r.92)
G008 wave-dependent Cd — drag coefficient including wave effect (§1, r.35; §4, r.93)
G009 SSH — sea surface height (§1, r.37; §4, r.94)
G010 d02 — dominio del modello; non definito oltre (§2, r.43)
G011 YSU — schema PBL non locale, senza TKE prognostica (§2, r.49; §4, r.91)
G012 `PBLH` / `blh` — planetary boundary layer height (§2, r.49; §4, r.101)
G013 `KM_OPT` — opzione di diffusione ("the diffusion option") (§2, r.50; §4, r.91)
G014 convection-permitting — `CU_PHYSICS` = 0 (§2, r.54)
G015 WSM6 — microfisica con nubi, pioggia, ghiaccio, neve e graupel, senza grandine (§2, r.55)
G016 Xu-Randall — schema di frazione nuvolosa continua (§2, r.56; §5, r.129)
G017 RUC — schema di superficie con 6 livelli di suolo (§2, r.57)
G018 maximum-random overlap — non definito (§5, r.131)
G019 bulk Richardson number — diagnostica PBL sul profilo di temperatura potenziale virtuale (§3, r.82)
G020 Charnock — rugosità senza stato del mare (§3, r.81; §4, r.93)
G021 `geo_em.d02` — il file statico della run (§3, r.74-76)
G022 LRZ — non definito (§3, r.74)
G023 recode dei laghi — non definito (§3, r.76)
G024 `al` — the snow-free climatological background albedo (§3, r.72; §5, r.176-177)
G025 `fal` — actual all-sky ratio of upward to downward shortwave (§3, r.73; §5, r.177-178)
G026 `cvl`, `cvh` — copertura vegetazione bassa/alta, somme sulle classi basse e alte (§4, r.111)
G027 `tvl`, `tvh` — tipo di vegetazione basso/alto (§4, r.110)
G028 `slt` — tipo di suolo, sette tipi ECMWF definiti da soglie argilla/sabbia (§4, r.110)
G029 `cl`, `dl` — copertura e profondità dei laghi (§3, r.76; §6, r.222)
G030 `10efg`, `10nfg` — eastward / northward gust components (§4, r.90)
G031 MYNN, MYJ — schemi PBL che portano TKE (§4, r.91)
G032 CMEMS — ocean reanalysis (esempio) (§4, r.94)
G033 `ACSNOM` — il campo di snowmelt, non accumulatore monotono (§4, r.97)
G034 accumulatore monotono — non definito (§4, r.97)
G035 `isfflx` — opzione con cui i flussi sono calcolati a ogni timestep (§4, r.98)
G036 history stream / output stream — non definito (§4, r.98)
G037 Noah accumulators — `ACHFX`/`ACLHF` (§4, r.98)
G038 `TSK`, `skt` — skin temperature; `skt` ottenuta invertendo il longwave ascendente (§4, r.99; §5, r.135-136)
G039 `mx2t`, `mn2t` — maximum and minimum 2 m temperature (§4, r.100)
G040 `output_diagnostics`, `nwp_diagnostics` — opzioni che scrivono `T2MAX`/`T2MIN` e `WSPD10MAX` + sei massimi orari rispettivamente (§4, r.100)
G041 MODIS-IGBP, STATSGO — categorie WRF di vegetazione e suolo (§4, r.110)
G042 `swvl1-4`, `stl1-4` — soil moisture and soil temperature, 4 strati ERA5 (§4, r.109)
G043 `lai_lv`, `lai_hv` — LAI per classe di vegetazione, per unità di area vegetata (§4, r.117)
G044 `anor`, `isor` — angolo e anisotropia ECMWF dall'autostruttura della covarianza del gradiente del terreno (§4, r.118)
G045 Kim-Arakawa — parametri di asimmetria e lunghezza efficace (§4, r.118)
G046 `LAI`, `VEGFRA`, `OA1-4`, `OL1-4` — campi WRF sottostanti (§4, r.121)
G047 `slor` — sub-grid parameter of the form-drag scheme (ERA5) (§5, r.142-143)
G048 `sdor` — genuine sub-grid standard deviation, computed by the pre-processor (§5, r.143-144)
G049 mixing ratio / specific content — per kg di aria secca / per kg di aria umida (§5, r.145-147)
G050 `clwc`, `ciwc` — non definito (contenuti d'acqua liquida/ghiaccio implicito) (§5, r.146)
G051 CAPE, CIN — most-unstable, particella di 500 m con massima temperatura potenziale equivalente nei 3 km più bassi (§5, r.148-154)
G052 equilibrium level — non definito (§5, r.150)
G053 `10fg` — ERA5: raffica parametrizzata; CHAPTER: massimo del vento risolto a 10 m sull'ora (§5, r.155-157)
G054 `i10fg` — instantaneous (gust) ERA5 (§5, r.159)
G055 `sro`, `ssro`, `ro` — runoff superficiale, sub-superficiale, totale (§5, r.180-190)
G056 `tcw` — somma delle colonne di cinque specie (ECMWF), sei in CHAPTER (§5, r.191-193)
G057 `grle`, `tcolg` — paramId ECMWF 260028 e 260001 per il graupel (§5, r.193)
G058 `2d` — 2 m dewpoint (§5, r.200-201)
G059 audit sample — non definito (§5, r.158; r.181)
G060 skin reservoir content — non definito (§6, r.222)

## 7. Segnalazioni
S001 [CONTRADDIZIONE INTERNA] data del documento 2026-09-17 (A001) — il testo riporta eventi del 2026-09-18 (ottenimento geo_em, reintegro di variabili) (§0, r.3; §3, r.74-75; §4, r.105)
S002 [CONTRADDIZIONE INTERNA] "dominant category only, never fractions — the file that holds the fractions no longer exists (see §4)" (A020) — §3 dice che la copertura frazionaria è consegnata e geo_em.d02 è stato ottenuto; §4 non tratta il land-use come non fornibile (§1, r.33; §3, r.73-76; §4, r.111)
S003 [CONTRADDIZIONE INTERNA] skt vs SST sull'acqua: 0.0005 K in §4 (N030) contro 0.005 K in §5 (N041) (§4, r.99; §5, r.139)
S004 [CONTRADDIZIONE INTERNA] "Only the two gust components are missing" (A014) — §4 elenca come non fornibili anche `mx2t`, `mn2t`, `blh`; non si sa se fossero nella lista dei 24 (§1, r.29; §4, r.100-101)
S005 [CONTRADDIZIONE INTERNA] 13 -> 29 livelli: file ×1.81 (0.8 -> 1.45 GB) ma archivio ×2.59 (7.0 -> 18.1 TB); 1.45 GB × ore di un anno non dà 18.1 TB (§6, r.233-235)
S006 [CONTRADDIZIONE INTERNA] "the land mask, the vegetation and soil types ... all change there ... must not be treated as a single static field" (A145-A146) — §4 dice `tvl`/`tvh`/`slt` ricavati dal file statico geo_em (§5, r.166-168; §4, r.110)
S007 [RIFERIMENTO SOSPETTO] "Approximable radiatively (§3)" per l'albedo del ghiaccio — §3 non contiene più una via per l'albedo, dichiarato spostato/consegnato (§4, r.96; §3, r.72-73)
S008 [RIFERIMENTO SOSPETTO] "`geo_em.d02`, recorded here as irrecoverable" — la nota fa riferimento a una sua versione precedente (§3, r.74)
S009 [GONFIATA] "Everything below was verified against the actual files" — molte voci (N064-N070, A138, A161) non indicano misura né popolazione (§0, r.11)
S010 [VAGA] "Accumulated fields were additionally checked for monotonicity within a run" — non dice quali run né quanti istanti (§0, r.15)
S011 [GONFIATA] "Exact — this is precisely the drag the simulation used" per Cd senza onde — nessuna verifica descritta (§3, r.81)
S012 [VAGA] confidenza "Medium" / "Reasonable" senza criterio (§3, r.80, r.82)
S013 [NUMERO SENZA FONTE] accordo 100.00 % geo_em / categoria dominante — nessun metodo o file indicato (§3, r.75-76)
S014 [NUMERO SENZA FONTE] 17.9 % e 90.1 % — nessuna popolazione o metodo (§4, r.111)
S015 [GONFIATA] "no untrimmed output exists anywhere" — non dimostrato (§4, r.98)
S016 [SENZA FONTE / VAGA] "a deliberate trimming of the output stream, not an accident" — nessuna fonte (§4, r.99)
S017 [GONFIATA] "the dominant land-use category (VEGPARM.TBL...)... It is exact where the answer is known" — "exact" con un errore dichiarato di 0.005 K (§5, r.138-139)
S018 [NUMERO SENZA FONTE] skt < 1 K RMSE sul suolo 0 cm e ~0.8 K sulla neve — nessuna popolazione (§5, r.139-141)
S019 [NUMERO SENZA FONTE] "a 0.8 % correction in the median" — nessuna popolazione né metodo (§5, r.147)
S020 [VAGA] "the few percent of points with no equilibrium level" — nessun numero (§5, r.149-150)
S021 [GONFIATA] "zero is also the physically correct reading" — affermazione non dimostrata (§5, r.151-152)
S022 [NUMERO SENZA FONTE] "roughly 1.6 times its own mean wind" per `10fg` ERA5 (§5, r.157)
S023 [VAGA] "Measured over the audit sample" — campione non descritto (quanti istanti, quali date) (§5, r.158; r.181)
S024 [VAGA] "the hourly maximum adds half a per cent to three per cent" — il minimo 1.004 corrisponde a 0.4 %, non mezzo per cento (§5, r.160-161)
S025 [NUMERO SENZA FONTE] "right only 88 % of the time" — nessuna popolazione in questo file (rimanda a CHAPTER_KNOWN_PROPERTIES.md §5) (§5, r.162-163)
S026 [NUMERO SENZA FONTE] ripartizione runoff vs ERA5 (1.0–4.6×, 0.000–0.004×, 0.19–0.85×) — nessuna popolazione (§5, r.188)
S027 [NUMERO SENZA FONTE] graupel 0.4 % e 26.5 kg/m² — nessuna data né file (solo "a July convective cell") (§5, r.196-197)
S028 [GONFIATA] "invisible" per lo 0.4 % del graupel (§5, r.196)
S029 [GONFIATA] "exactly zero at 00 UTC" — nessuna verifica descritta (§5, r.203)
S030 [GONFIATA] "Geolocation is now exact to ~2 m" — "exact" con numero approssimato e senza fonte (§5, r.206)
S031 [NUMERO SENZA FONTE] errore GRIB1 fino a ~1.1 km al bordo nord (§5, r.207-208)
S032 [GONFIATA] "the complete radiation budget ... at the top of the atmosphere" — §2 dice che il longwave discendente al top è identicamente zero e non sarà scritto (§6, r.224-225; §2, r.62-64)
S033 [VAGA] "several days of data transfer" — nessun numero (§0, r.9)
S034 [RIFERIMENTO INCOMPLETO] "ECMWF definitions" citate senza documento né versione/ciclo (§5, r.146-147; r.191-193)
S035 [RIFERIMENTO INCOMPLETO] nessuna issue o commit citati nell'intero file; le misure non sono collegate a una registrazione (intero file)
S036 [RIFERIMENTO INCOMPLETO] VEGPARM.TBL senza sezione della tabella (§5, r.137)
S037 [VAGA] "Any other definition ... is a one-line change" (§6, r.230)
S038 [NUMERO SENZA FONTE] dimensioni file ~0.8/~1.45 GB e archivio 7.0/18.1 TB — nessuna misura indicata (§6, r.234-235)
S039 [VAGA] "Only a gust magnitude proxy exists ... judged too weak to publish" — criterio del giudizio non dato (§4, r.90)
S040 [VAGA] "The land/sea mask changes with the season" — il testo la lega al ghiaccio marino, non alla stagione in sé (§5, r.165-166)
