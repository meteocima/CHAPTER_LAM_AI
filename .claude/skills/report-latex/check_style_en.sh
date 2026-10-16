#!/usr/bin/env bash
# Searches .tex files for the expressions banned by anti-patterns-en.md (case-insensitive).
# Usage: check_style_en.sh [file.tex ...]    (default: report/en/chapters/*.tex)
# Prints file:line: [pattern] text; exit 1 if anything is found, 0 otherwise.
# Comment-only lines (% ...) are skipped.

set -u

# Espressioni letterali (grep -F).
FISSI=(
  # 1. filler
  "it is important to note" "it is worth noting" "worth noting" "it should be noted" "notably"
  "in conclusion" "in summary" "to summarize" "overall" "in other words" "ultimately"
  "as mentioned" "as discussed" "as we will see" "as noted above"
  # 2. inflated adjectives and adverbs
  "crucial" "key role" "essential" "fundamental" "vital" "pivotal"
  "robust" "reliabl" "solid" "novel" "innovative" "cutting-edge" "state-of-the-art"
  "sophisticated" "significant"
  "extremely" "highly" "greatly" "deeply" "particularly" "remarkabl" "substantially"
  "dramatically" "perfectly" "seamless"
  # 3. structures
  "not only" "not just" "rather than simply"
  "in this section" "in this chapter" "this chapter presents" "below we" "we now turn"
  "the following section"
  # 4. jargon and padding
  "plays a role" "play a role" "plays a key" "makes a difference" "make a difference"
  "game changer" "in terms of" "leverag" "utiliz" "facilitat" "delve" "underscor" "showcas"
  "harness" "a wide range of" "a variety of" "in order to" "due to the fact" "landscape"
  "realm" "tapestry" "journey" "testament"
  # 5. formatting
  "so-called"
  # 6. stacked hedges
  "might potentially" "could possibly" "may potentially" "potentially"
  "seems to suggest" "appears to indicate" "arguably" "probably" "likely" "somewhat"
  "to some extent" "fairly" "relatively" "tends to" "quite"
)

# Regular expressions (grep -E), with the label to print.
REGEX=(
  "—|em dash"
  " --- |em dash (---)"
  " – |spaced en dash"
  '\\textbf|bold (\textbf)'
  '\\bfseries|bold (\bfseries)'
  '\?|question mark (rhetorical question?)'
  ':[[:space:]]*$|colon at end of line'
  '\\begin\{itemize\}|bullet list (check it is a discrete list)'
  '\\begin\{enumerate\}|numbered list (check it is a discrete list)'
)

if [ $# -gt 0 ]; then
  FILES=("$@")
else
  shopt -s nullglob
  FILES=(report/en/chapters/*.tex)
fi
[ ${#FILES[@]} -gt 0 ] || { echo "check_style_en: no .tex file" >&2; exit 2; }

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
  [ -r "$f" ] || { echo "check_style_en: unreadable: $f" >&2; continue; }
  for p in "${FISSI[@]}"; do
    riporta "$f" "$p" < <(grep -n -i -F -- "$p" "$f")
  done
  for r in "${REGEX[@]}"; do
    riporta "$f" "${r##*|}" < <(grep -n -i -E -- "${r%|*}" "$f")
  done
done

if [ "$TOTALE" -eq 0 ]; then
  echo "check_style_en: no occurrences in ${#FILES[@]} files"
  exit 0
fi

echo
echo "Summary ($TOTALE occurrences):"
for k in "${!CONTEGGIO[@]}"; do printf '%5d  %s\n' "${CONTEGGIO[$k]}" "$k"; done | sort -rn
exit 1
