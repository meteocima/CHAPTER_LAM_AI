# Glossary (English fixed forms)

The English fixed form of every term in the Italian glossary (`report/scaletta.md`). Use exactly
these forms; no synonyms.

| Italian fixed form | English fixed form | definition |
|---|---|---|
| archivio GRIB2 CHAPTER | CHAPTER GRIB2 archive | the set of hourly GRIB2 files of 246 messages |
| file orario | hourly file | one GRIB2 file per validity time |
| messaggio GRIB | GRIB message | one field on one level |
| file wrfout | wrfout files | the hourly WRF output the archive is made from |
| file statico `geo_em.d02` | static file `geo_em.d02` | the run's WPS static file |
| istante di validità | validity time | `validityDate`/`validityTime` |
| tempo di riferimento | reference time | `dataDate`/`dataTime` |
| campo istantaneo | instantaneous field | product definition template 4.0 |
| campo accumulato | accumulated field (over the hour ending at the validity time) | template 4.8, reference time H−1, interval 0–1 |
| intervallo di accumulazione | accumulation interval | `stepRange` 0–1 |
| run giornaliera | daily run, the run started at 18 UTC on D−1 | 30 h; the first 6 h of spin-up are not published |
| spin-up | spin-up | the first 6 h of a run |
| cambio di run | run switch | the step from 00 UTC (run of D−2, hour 30) to 01 UTC (run of D−1, hour 7) |
| campo statico | static field | identical in every hourly file |
| terra permanente | permanent land | land mask of the static file, fixed |
| maschera terra–mare oraria (`lsm`) | hourly land–sea mask (`lsm`) | WRF's `LANDMASK`, grows with sea ice |
| punto mancante (bitmap) | missing point (bitmap) | never a zero |
| regola di pubblicazione | publication rule | ERA5 name only if the quantity is the ERA5 one, or the difference fits in one line |
| regola di mascheratura | masking rule | missing where the ERA5 parameter is not defined |
| livello di pressione | pressure level | one of the 13 isobaric levels |
| livello del modello | model level | WRF's native vertical level |
| clamping | clamping | value of the lowest model level repeated below ground |
| rapporto di mescolanza | mixing ratio | per kg of dry air (WRF) |
| contenuto specifico | specific content | per kg of moist air (ECMWF) |
| umidità relativa sulla fase mista | relative humidity over the mixed phase | IFS Cy41r2 saturation, ice below 250.16 K, water above 273.16 K |
| temperatura di pelle (`skt`) | skin temperature (`skt`) | reconstructed from `LWUPB` |
| emissività di categoria | category emissivity | ε measured per land-use category |
| soglia di copertura nevosa | snow-cover threshold | 1.5 %, the only free parameter |
| vento risolto | resolved wind | model 10 m wind, no gust parameterization |
| raffica parametrizzata | parameterized gust | ERA5's `10fg`/`i10fg` |
| componente connessa | connected component | set of contiguous water cells |
| campo identicamente nullo | identically zero field | zero at every sampled time (never "dead field") |
| campione di verifica | verification sample | 34 validity times: 4 in 2019, 26 in 2024 (every month), 4 in 2025 |
| rapporto delle medie / delle mediane | ratio of means, ratio of medians | never "ratio" alone |
| categoria dominante | dominant category | land-use class with the largest fraction |

Other recurring terms:

| Italian | English |
|---|---|
| paramId, shortName, template di prodotto 4.0/4.8 | paramId, shortName, product definition template 4.0/4.8 |
| top dell'atmosfera | top of the atmosphere |
| radiazione solare / termica (a onda corta / lunga) | solar / thermal radiation, as in the ECMWF parameter names |
| cielo sereno | clear sky |
| copertura nuvolosa | cloud cover |
| velocità d'attrito | friction velocity |
| rugosità | roughness length |
| deflusso superficiale / sotterraneo | surface runoff / subsurface runoff |
| acqua equivalente (a.e.) | water equivalent (w.e.) |
| uso del suolo | land use |
| vegetazione bassa / alta | low / high vegetation |
| tipo di suolo | soil type |
| orografia sottogriglia | sub-grid orography |
| ghiaccio marino | sea ice |
| acque interne | inland water |
| accumulatore | accumulator |
| azzeramento (di `WSPD10MAX`) | reset |
| volte (0,625 volte ERA5) | times (0.625 times ERA5) |
| CHAPTER / riferimento (intestazione) | CHAPTER / reference |
