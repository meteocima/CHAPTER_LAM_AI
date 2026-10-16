# Style guide (English)

The register is that of a good paper in a journal of the field (meteorology, numerical modelling,
reanalysis data). The reader is a scientific user of the data: knows ERA5 and numerical modelling,
does not know this repository and will not read it. US spelling throughout (`parameterization`,
`modeling`, `color`, `gray`).

## Principles

1. **Every sentence carries information.** If a sentence can be removed without losing anything,
   it is removed. Test: delete it and reread the paragraph; if nothing is missing, it stays deleted.

2. **Claims are specific and, where possible, quantified.** "Improves the agreement" is not
   enough: by how much, over which population, against what. Every number carries its unit, its
   population and its reference of comparison. Numbers and units are written with `\SI{...}{...}`
   and `\num{...}`; the decimal separator is the point (`siunitx` with `locale=UK`).

3. **Caution is stated once, where it applies, precisely.** "With 34 sampled timesteps the
   estimate holds for the sampled set", not "might potentially suggest". If a limit has a number,
   write the number.

4. **Continuous prose, one topic per paragraph.** Lists only for genuinely discrete items:
   variables of a table, parameters, files. An argument is not broken into bullet points. Long
   lists of variables go in a `booktabs` table, not in `itemize`.

5. **The paragraph ends when the topic is exhausted.** No closing sentence, no summary of what
   was just said, no announcement of what follows.

6. **Varied sentence length, no constructed parallelisms.** Three sentences with the same
   structure are not lined up for effect. A short sentence is fine when the content is short.

7. **A technical term is fixed at its first occurrence and then stays the same**, even at the
   cost of repeating it. No synonyms for variety: once "validity time" is written it does not
   become "valid hour" or "timestep". The fixed form of every term is in `glossary-en.md`. Names
   of variables, GRIB parameters and WRF fields go in `\campo{}` and are written exactly as in the
   file (`\campo{RAINNC}`, `\campo{tp}`, paramId 228).

8. **No bold in the body text.** Emphasis comes from position in the sentence and from content.
   Italics only for terms at their definition and for non-technical foreign words.

9. **The text states the value, not its history.** Where sources disagreed or a value was
   corrected, the report writes only the resolved value. It does not name the contradiction, the
   earlier version, the correction or another document's error.

## Practical conventions

- Internal references with `\label{cap:...}`, `\label{sec:...}`, `\label{tab:...}`,
  `\label{eq:...}` and `\cref{...}`; never "Section 3" typed by hand.
- Citations with `\textcite`/`\parencite`. Repository issues are cited only through
  `riferimenti.bib`.
- Equations have every symbol defined in the sentence that introduces them or the next one.
- Asides with commas or parentheses, not with em dashes.
- A colon introduces a list or an explanation that follows directly, never a "reveal".
- Active voice where the agent matters ("WRF resets the field"); passive is fine where it does
  not ("the field is encoded with template 4.8"). No "we" for the model's actions.
- Numbers: `\num{2220273}` prints 2,220,273 with `group-separator={,}`; ranges with
  `\SIrange`/`\numrange`; percentages with `\SI{12.3}{\percent}`.

## Translation rules (Italian → English)

- Translate the Italian report sentence by sentence in content, not word by word in form. Every
  fact, number, population, condition and citation of the Italian text stays; nothing is added.
- Italian constructions that do not work in English are rebuilt: long subordinate chains are
  split, "il quale/la quale" become relative clauses or new sentences, impersonal "si" becomes
  passive or a concrete subject.
- Labels (`\label`), citation keys, `\campo{}` contents, table structure and equation content are
  unchanged. Only prose, captions and table text are translated.
- Italian ordinal dates ("il 1º luglio 2024") become "1 July 2024"; times "alle 12 UTC" become
  "at 12 UTC".
