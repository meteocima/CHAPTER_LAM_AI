#!/usr/bin/env bash
# Cerca nei .tex le espressioni vietate da anti-pattern.md (senza distinzione di maiuscole).
# Uso: check_stile.sh [file.tex ...]    (default: report/capitoli/*.tex)
# Stampa file:riga: [pattern] testo; exit 1 se trova qualcosa, 0 altrimenti.
# Le righe di solo commento (% ...) sono ignorate.

set -u

# Espressioni letterali (grep -F).
FISSI=(
  # 1. riempitivi
  "è importante notare" "è interessante notare" "importante sottolineare"
  "vale la pena" "è fondamentale" "è essenziale"
  "in conclusione" "in sintesi" "in definitiva" "nel complesso" "riassumendo"
  "in altre parole" "come già detto" "come vedremo" "come accennato"
  # 2. aggettivi e avverbi gonfiati
  "cruciale" "cruciali" "fondamentale" "fondamentali" "essenziale" "essenziali"
  "robusto" "robusta" "robusti" "robuste" "solido" "solida" "affidabil"
  "innovativ" "avanzat" "all'avanguardia" "sofisticat"
  "significativ"
  "profondamente" "estremamente" "notevolmente" "fortemente" "particolarmente"
  "decisamente" "perfettamente"
  # 3. strutture
  "non solo" "non si tratta di"
  "in questa sezione" "in questo capitolo" "questo capitolo presenta" "vedremo"
  "nel seguito" "di seguito"
  # 4. calchi e burocratese
  "giocare un ruolo" "gioca un ruolo" "giocano un ruolo" "svolge un ruolo" "svolgono un ruolo"
  "ruolo chiave" "fare la differenza" "fa la differenza" "fanno la differenza"
  "in termini di"
  "a livello di" "nell'ottica" "al fine di" "risulta essere" "risultano essere"
  "effettuare" "effettua" "procedere a" "impatta" "performant"
  # 6. cautele accumulate
  "potrebbe potenzialmente" "potrebbe eventualmente" "potenzialmente"
  "sembrerebbe" "sembra indicare" "sembra suggerire" "parrebbe"
  "probabilmente" "verosimilmente" "in qualche modo" "in una certa misura" "tendenzialmente"
)

# Espressioni regolari (grep -E), con l'etichetta da stampare.
REGEX=(
  '(^|[^[:alpha:]])(va|vanno|andare|andiamo) a [[:alpha:]]|andare a + infinito'
  "—|trattino lungo"
  " --- |trattino lungo (---)"
  " – |trattino medio spaziato"
  '\\textbf|grassetto (\textbf)'
  '\\bfseries|grassetto (\bfseries)'
  '\?|punto interrogativo (domanda retorica?)'
  ':[[:space:]]*$|due punti a fine riga'
  '\\begin\{itemize\}|elenco puntato (verificare che sia una lista discreta)'
  '\\begin\{enumerate\}|elenco numerato (verificare che sia una lista discreta)'
)

if [ $# -gt 0 ]; then
  FILES=("$@")
else
  shopt -s nullglob
  FILES=(report/capitoli/*.tex)
fi
[ ${#FILES[@]} -gt 0 ] || { echo "check_stile: nessun file .tex" >&2; exit 2; }

declare -A CONTEGGIO=()
TOTALE=0

riporta() {  # $1 file, $2 etichetta, stdin: righe "n:testo" di grep -n
  local file=$1 etichetta=$2 riga
  while IFS= read -r riga; do
    [[ "${riga#*:}" =~ ^[[:space:]]*% ]] && continue
    printf '%s:%s: [%s] %s\n' "$file" "${riga%%:*}" "$etichetta" "${riga#*:}"
    CONTEGGIO[$etichetta]=$(( ${CONTEGGIO[$etichetta]:-0} + 1 ))
    TOTALE=$(( TOTALE + 1 ))
  done
}

for f in "${FILES[@]}"; do
  [ -r "$f" ] || { echo "check_stile: non leggibile: $f" >&2; continue; }
  for p in "${FISSI[@]}"; do
    riporta "$f" "$p" < <(grep -n -i -F -- "$p" "$f")
  done
  for r in "${REGEX[@]}"; do
    riporta "$f" "${r##*|}" < <(grep -n -i -E -- "${r%|*}" "$f")
  done
done

if [ "$TOTALE" -eq 0 ]; then
  echo "check_stile: nessuna occorrenza in ${#FILES[@]} file"
  exit 0
fi

echo
echo "Riepilogo ($TOTALE occorrenze):"
for k in "${!CONTEGGIO[@]}"; do printf '%5d  %s\n' "${CONTEGGIO[$k]}" "$k"; done | sort -rn
exit 1
