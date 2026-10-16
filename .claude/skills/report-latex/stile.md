# Guida di stile

Il registro è quello di un buon articolo su rivista del settore (meteorologia, modellistica
numerica, dati di rianalisi). Il lettore è un utente scientifico dei dati: conosce ERA5 e la
modellistica, non conosce questo repository e non lo leggerà.

## Principi

1. **Ogni frase porta informazione.** Se una frase si può togliere senza perdere nulla, si
   toglie. Prova: cancellarla e rileggere il paragrafo; se non manca niente, resta cancellata.

2. **Affermazioni specifiche e, quando possibile, quantificate.** "Migliora l'accordo" non
   basta: serve di quanto, su quale popolazione e rispetto a cosa. Ogni numero porta unità,
   popolazione e riferimento di confronto. Numeri e unità si scrivono con `\SI{...}{...}` e
   `\num{...}`; il separatore decimale è la virgola (impostazione di `siunitx` in italiano).

3. **La cautela si esprime una volta, dove serve, con precisione.** "Con 34 istanti
   campionati, la stima vale per l'insieme campionato" e non "sembrerebbe potenzialmente
   indicare". Se un limite ha un numero, si scrive il numero.

4. **Prosa continua, un argomento per paragrafo.** Gli elenchi si usano solo per liste davvero
   discrete: variabili di una tabella, parametri, file. Un ragionamento non si spezza in punti.
   Le liste lunghe di variabili vanno in tabella (`booktabs`), non in `itemize`.

5. **Il paragrafo finisce quando l'argomento è esaurito.** Nessuna frase di chiusura, nessun
   riassunto di ciò che si è appena detto, nessun annuncio di ciò che segue.

6. **Lunghezza delle frasi variabile, niente parallelismi costruiti.** Non si allineano tre
   frasi con la stessa struttura per effetto. Una frase breve va bene quando il contenuto è
   breve.

7. **Un termine tecnico si fissa alla prima occorrenza e poi resta uguale**, anche a costo di
   ripeterlo. Niente sinonimi per variare: se si è scritto "istante di validità", non diventa
   poi "ora di validità" o "timestep". La forma fissata di ogni termine sta nel glossario di
   `report/scaletta.md`; il `revisore` la controlla sui capitoli già scritti. I nomi di
   variabili, parametri GRIB e campi WRF vanno in `\texttt{}` e si scrivono esattamente come nel
   file (`\texttt{RAINNC}`, `\texttt{tp}`, paramId 228).

8. **Niente grassetto nel corpo del testo.** L'enfasi viene dalla posizione nella frase e dal
   contenuto. Il corsivo solo per termini alla loro definizione e per parole straniere non
   tecniche.

9. **Il testo dice il dato, non la sua storia.** Quando le fonti si contraddicono o un valore è
   stato corretto, il report scrive solo il valore risolto. Non nomina la contraddizione, la
   versione precedente, la correzione o l'errore di un altro documento. La scelta del valore sta
   in `report/scaletta.md`, non nel testo.

## Convenzioni pratiche

- Riferimenti interni con `\label{cap:...}`, `\label{sec:...}`, `\label{tab:...}`,
  `\label{eq:...}` e `\cref{...}`; mai "la sezione 3" scritto a mano.
- Riferimenti bibliografici con `\textcite`/`\parencite`. Le issue del repository si citano
  solo se sono in `riferimenti.bib` o se l'utente ha deciso come citarle.
- Affermazione senza fonte dopo la verifica: si toglie, oppure `\todo{fonte}` subito dopo.
- Le equazioni hanno ogni simbolo definito nella frase che le introduce o in quella successiva.
- Gli incisi si fanno con virgole o parentesi, non con trattini lunghi.
- I due punti introducono un elenco o una spiegazione che segue direttamente, mai una "rivelazione".
