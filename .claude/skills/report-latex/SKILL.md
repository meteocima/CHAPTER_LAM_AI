---
name: report-latex
description: Unisce documenti Markdown in un report tecnico-scientifico LaTeX in italiano, riscritto da zero a partire dai fatti estratti e non dalla prosa di partenza. Usala quando si deve trasformare documentazione md (tipicamente generata da un'AI) in un report di registro da rivista, con estrazione dei fatti, verifica delle fonti, scaletta, stesura capitolo per capitolo e revisione stilistica.
---

# report-latex

Il report si costruisce dai fatti, mai dalla prosa degli md. Gli md si leggono una sola volta,
in fase 1, dal subagent `estrattore`; dopo quella fase nessuno li riapre.

File della skill:
- `stile.md`: la guida di stile. Vincolante per ogni riga scritta in `.tex`.
- `anti-pattern.md`: i pattern vietati, con esempio e correzione.
- `check_stile.sh`: grep dei pattern vietati nei `.tex`.

Subagent (in `.claude/agents/`):
- `estrattore`: un md in ingresso, una scheda senza prosa in uscita.
- `revisore`: un `.tex` in ingresso, un elenco di problemi in uscita; non modifica nulla.

Percorsi (radice `report/`):
- `schede/<nome>.md`: una scheda per md; `schede/da_verificare.md`: affermazioni senza fonte e
  riferimenti.
- `scaletta.md`: struttura, affermazioni per sezione, contraddizioni, glossario dei termini.
- `main.tex`: preambolo e `\include` dei capitoli.
- `capitoli/<nn>-<nome>.tex`: un file per capitolo (`01-archivio.tex`, ...).
- `bib/riferimenti.bib`: bibliografia BibLaTeX, compilata con biber.

## Flusso

Ogni fase finisce con uno STOP: si mostra il risultato all'utente e si aspetta il via esplicito.

### Fase 0 – Preparazione
Skill e subagent esistono. Se mancano, crearli. STOP.

### Fase 1 – Estrazione
1. Un subagent `estrattore` per ciascun md, lanciati in parallelo. Prompt: il percorso dell'md e
   il percorso della scheda da scrivere.
2. Controllare che ogni scheda abbia tutte le sezioni previste da `estrattore.md`.
3. Scrivere `schede/da_verificare.md`: ogni affermazione `[SENZA FONTE]` e ogni riferimento
   bibliografico, uno per riga, con il file di provenienza. Non completare e non correggere i
   riferimenti: quelli incompleti restano come sono, con la segnalazione accanto.
4. `git status` deve mostrare invariati gli md di partenza.
STOP: l'utente verifica riferimenti e affermazioni.

### Fase 2 – Scaletta
Lavorare solo sulle schede. `scaletta.md` contiene:
- capitoli e sezioni, e per ogni sezione gli identificativi delle affermazioni che usa;
- le duplicazioni fra schede, con l'affermazione tenuta;
- le contraddizioni fra schede, citate entrambe, senza sceglierne una se le schede non la
  risolvono;
- il glossario: ogni termine tecnico con la forma fissata e la sua definizione.
STOP: approvazione dell'utente.

### Fase 3 – Stesura
1. Scrivere `main.tex` (classe `report`, pdflatex, `babel[italian]`, `biblatex` con
   `backend=biber`, `todonotes`, `cleveref`, `booktabs`, `siunitx`).
2. Un capitolo alla volta, solo da schede e scaletta:
   - scrivere `capitoli/<nn>-<nome>.tex` seguendo `stile.md`;
   - affermazioni rimaste senza fonte dopo la verifica dell'utente: escluse, oppure marcate
     `\todo{fonte}`;
   - riferimenti interni con `\label` e `\cref`, mai numeri scritti a mano;
   - eseguire `bash .claude/skills/report-latex/check_stile.sh report/capitoli/<file>.tex`;
   - lanciare il `revisore` sul capitolo;
   - applicare solo le correzioni coerenti con `stile.md` e `anti-pattern.md`; le altre si
     scartano e si dice perché;
   - passare al capitolo successivo.
3. Compilare con `latexmk -pdf main.tex` in `report/` e correggere errori e riferimenti
   indefiniti (cercare `undefined` nel log).

## Regole generali
- Non inventare dati, numeri o riferimenti.
- Un'informazione mancante si segnala (`\todo{...}` nel `.tex`, una riga nella scheda), non si
  colma.
- Nessuna introduzione o conclusione generica. Un capitolo di conclusioni, se c'è, riporta
  risultati e limiti concreti presi dalle schede.
- Gli md di partenza non si modificano.
