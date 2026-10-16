# Anti-pattern

Ogni voce: il pattern, un esempio sbagliato (✗) e la correzione (✓). I numeri negli esempi sono
illustrativi e non vanno riportati nel report. Le espressioni cercate da `check_stile.sh` sono
segnate con `[grep]`.

## 1. Formule di riempimento

- "è importante notare" / "è interessante notare" `[grep]`
  ✗ È importante notare che il campo `tp` è riferito alle 00Z.
  ✓ Il campo `tp` è accumulato a partire dalle 00Z dello stesso giorno.
- "vale la pena sottolineare / ricordare" `[grep]`
  ✗ Vale la pena sottolineare che WRF usa una Terra sferica.
  ✓ WRF integra su una sfera di raggio \SI{6370}{km}.
- "è fondamentale" / "è essenziale" `[grep]`
  ✗ È fondamentale dichiarare la forma della Terra nel GRIB.
  ✓ Senza la forma della Terra dichiarata, la griglia ricostruita da eccodes si sposta di
    \SI{1,1}{km} al bordo nord.
- "in conclusione", "in sintesi", "in definitiva", "nel complesso", "riassumendo",
  "in altre parole" `[grep]`
  ✗ In sintesi, l'archivio contiene 90 variabili.
  ✓ (frase eliminata: il numero è già stato dato)
- "come già detto", "come vedremo", "come accennato" `[grep]`
  ✗ Come già detto, il vento a 10 m è risolto.
  ✓ (si usa `\cref` se il rimando serve; altrimenti si toglie)

## 2. Aggettivi e avverbi gonfiati

- "cruciale", "fondamentale", "essenziale", "chiave" come aggettivo `[grep]`
  ✗ La soglia di copertura nevosa è un parametro cruciale.
  ✓ La soglia di copertura nevosa è l'unico parametro libero della ricostruzione.
- "robusto", "solido", "affidabile" senza misura `[grep]`
  ✗ Il metodo è robusto.
  ✓ Il metodo dà lo stesso risultato per soglie comprese fra 1226 e 8583 celle.
- "innovativo", "avanzato", "all'avanguardia", "sofisticato" `[grep]`
  ✗ Un approccio innovativo alla ricostruzione della temperatura di pelle.
  ✓ La temperatura di pelle si ricava invertendo la radiazione a onda lunga uscente.
- "significativo/significativamente" senza test statistico `[grep]`
  ✗ L'errore si riduce significativamente.
  ✓ L'errore quadratico medio passa da \SI{0,12}{K} a \SI{0,08}{K}.
- "profondamente", "estremamente", "notevolmente", "fortemente", "particolarmente",
  "decisamente" `[grep]`
  ✗ Il risultato è estremamente sensibile alla stagione.
  ✓ La frazione di punti riprodotti entro 1e-4 è 99,98% a luglio e 93,05% a gennaio.
- "perfettamente", "esattamente" quando non si tratta di un'identità `[grep: perfettamente]`
  ✗ Il campo corrisponde perfettamente a ERA5.
  ✓ Il campo coincide con la definizione ERA5; il rapporto medio è 0,95–1,06 per livello.

## 3. Strutture

- Triadi di aggettivi o sostantivi
  ✗ Un archivio completo, coerente e verificato.
  ✓ Un archivio con 246 messaggi per file, verificati da un controllo di inventario.
- "non solo… ma anche" `[grep]`
  ✗ L'albedo cambia non solo con il ghiaccio ma anche con la stagione.
  ✓ L'albedo cambia con il ghiaccio marino e al passaggio fra stagione estiva e invernale.
- "non si tratta di X, ma di Y" / "non è X, è Y" `[grep: non si tratta di]`
  ✗ Non si tratta di un limite della fisica, ma del flusso di output.
  ✓ Il limite è il flusso di output: lo schema calcola il campo ma non lo scrive.
- Domande retoriche `[grep: ?]`
  ✗ Perché il campo è nullo? Perché lo schema convettivo è spento.
  ✓ Il campo è nullo perché lo schema convettivo è spento (`CU_PHYSICS=0`).
- Frase a effetto a fine paragrafo
  ✗ … Un dettaglio che fa tutta la differenza.
  ✓ (frase eliminata)
- Riassunto a fine sezione
  ✗ Abbiamo quindi visto come l'archivio tratta le accumulazioni.
  ✓ (frase eliminata)
- Anticipazioni: "in questa sezione vedremo", "nel seguito", "di seguito descriviamo",
  "questo capitolo presenta" `[grep]`
  ✗ In questa sezione vedremo come sono codificati i campi accumulati.
  ✓ I campi accumulati usano il template di prodotto 4.8.
- Parallelismi costruiti (tre frasi con la stessa struttura)
  ✗ Il vento è risolto. La pressione è diagnosticata. L'umidità è ricalcolata.
  ✓ Il vento è quello risolto dal modello; pressione e umidità relativa sono ricalcolate
    in post-elaborazione.

## 4. Calchi e burocratese

- "giocare / svolgere un ruolo" `[grep]`
  ✗ L'emissività gioca un ruolo chiave nell'inversione.
  ✓ L'inversione richiede l'emissività di ogni categoria di uso del suolo.
- "fare la differenza" `[grep]`
  ✗ La correzione fa la differenza sul ghiaccio.
  ✓ Sul ghiaccio la correzione cambia l'umidità relativa di un fattore fino a 1,8.
- "in termini di" come connettivo generico `[grep]`
  ✗ Il file è più grande in termini di dimensioni.
  ✓ Il file pesa \SI{39}{MB} in più.
- "andare a + infinito" `[grep: va a / vanno a / andare a / andiamo a]`
  ✗ Il convertitore va a calcolare l'umidità specifica.
  ✓ Il convertitore calcola l'umidità specifica.
- "a livello di", "nell'ottica di", "al fine di", "risulta essere", "effettuare",
  "procedere a" `[grep]`
  ✗ Si è proceduto ad effettuare una misura a livello di dominio.
  ✓ La misura copre l'intero dominio.
- Anglicismi e calchi evitabili: "implementare" per "realizzare", "performante",
  "impattare", "andare a vedere" `[grep: impatta, performant]`
  ✗ La soglia impatta la stima.
  ✓ La soglia cambia la stima.

## 5. Punteggiatura e formattazione

- Trattini lunghi come incisi (`—`, `---`, `–` spaziato) `[grep]`
  ✗ La maschera — come detto — cambia nel tempo.
  ✓ La maschera cambia nel tempo.
- Due punti per creare attesa `[grep: riga che finisce con ":"]`
  ✗ Il motivo è semplice: il campo non è stato scritto.
  ✓ Il campo non è stato scritto nel flusso di output.
- Grassetto nel corpo `[grep: \textbf, \bfseries]`
  ✗ Il campo è \textbf{sempre} nullo.
  ✓ Il campo è nullo in tutti i 34 istanti campionati.
- Elenchi al posto della prosa `[grep: \begin{itemize} segnalato per controllo manuale]`
  ✗ `\begin{itemize}\item il campo è nullo \item perché CU\_PHYSICS=0 \item quindi non si pubblica\end{itemize}`
  ✓ Il campo è nullo perché `CU_PHYSICS=0` e per questo non viene pubblicato.
- Virgolette di enfasi ("cosiddetto", termini fra virgolette per ironia)
  ✗ Il campo "morto".
  ✓ Il campo identicamente nullo.

## 6. Cautele accumulate

- "potrebbe potenzialmente", "potrebbe eventualmente" `[grep]`
  ✗ La soglia potrebbe potenzialmente influire.
  ✓ La soglia modifica l'errore su 55 000 punti a gennaio.
- "sembrerebbe suggerire", "sembra indicare", "parrebbe" `[grep]`
  ✗ Il dato sembrerebbe suggerire un bias freddo.
  ✓ La temperatura di pelle è più fredda di ERA5 di \SI{2}{K} sulla terra in media.
- Avverbi di cautela sparsi: "probabilmente", "verosimilmente", "in qualche modo",
  "in una certa misura", "tendenzialmente" `[grep]`
  ✗ Il campo è in una certa misura sottostimato.
  ✓ Il campo vale 0,625 di quello ERA5.
