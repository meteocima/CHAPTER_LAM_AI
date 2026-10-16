# Anti-patterns (English)

Each entry: the pattern, a wrong example (✗) and the fix (✓). Numbers in the examples are
illustrative and must not be copied into the report. Expressions searched by `check_style_en.sh`
are marked `[grep]`.

## 1. Filler

- "it is important to note", "it is worth noting", "it should be noted", "notably" `[grep]`
  ✗ It is worth noting that `tp` is referred to 00Z.
  ✓ `tp` is accumulated from 00 UTC of the same day.
- "in conclusion", "in summary", "to summarize", "overall", "in other words", "ultimately" `[grep]`
  ✗ In summary, the archive holds 90 variables.
  ✓ (sentence removed: the number was already given)
- "as mentioned", "as discussed above", "as we will see" `[grep]`
  ✗ As mentioned above, the 10 m wind is resolved.
  ✓ (use `\cref` if the reference is needed; otherwise remove)

## 2. Inflated adjectives and adverbs

- "crucial", "key" as adjective, "essential", "fundamental", "vital", "pivotal" `[grep]`
  ✗ The snow-cover threshold is a crucial parameter.
  ✓ The snow-cover threshold is the only free parameter of the reconstruction.
- "robust", "reliable", "solid" without a measure `[grep]`
  ✗ The method is robust.
  ✓ The method gives the same result for thresholds between 1226 and 8583 cells.
- "novel", "innovative", "cutting-edge", "state-of-the-art", "sophisticated", "advanced" `[grep]`
- "significant(ly)" without a statistical test `[grep]`
  ✗ The error drops significantly.
  ✓ The root-mean-square error drops from 0.12 K to 0.08 K.
- "extremely", "highly", "greatly", "deeply", "particularly", "remarkably", "substantially",
  "dramatically", "perfectly", "seamlessly" `[grep]`
  ✗ The result is extremely sensitive to the season.
  ✓ The fraction of points reproduced within 1e-4 is 99.98% in July and 93.05% in January.

## 3. Structures

- Triads of adjectives or nouns
  ✗ A complete, consistent and verified archive.
  ✓ An archive of 246 messages per file, checked by an inventory test.
- "not only … but also" `[grep]`
- "it is not X, it is Y" / "not X but Y" as a reveal `[grep: "not just", "rather than simply"]`
  ✗ This is not a limit of the physics but of the output stream.
  ✓ The limit is the output stream: the scheme computes the field and does not write it.
- Rhetorical questions `[grep: ?]`
- Punchline at the end of a paragraph, summary at the end of a section
- Signposting: "in this section", "in this chapter", "below we", "the following", "we now turn",
  "this chapter presents" `[grep]`
  ✗ In this section we describe how the accumulated fields are encoded.
  ✓ The accumulated fields use product definition template 4.8.
- Constructed parallelisms (three sentences with the same structure)

## 4. Jargon and padding

- "plays a (key) role" `[grep]`
  ✗ Emissivity plays a key role in the inversion.
  ✓ The inversion needs the emissivity of every land-use category.
- "makes a difference", "game changer" `[grep]`
- "in terms of" as a generic connective `[grep]`
  ✗ The file is larger in terms of size.
  ✓ The file is 39 MB larger.
- "leverage", "utilize", "facilitate", "delve", "underscore", "showcase", "harness",
  "a wide range of", "a variety of", "in order to", "due to the fact that", "with respect to"
  used as padding `[grep]`
  ✗ The converter utilizes the static file in order to compute `cvl`.
  ✓ The converter computes `cvl` from the static file.
- "landscape", "realm", "tapestry", "journey", "testament" `[grep]`

## 5. Punctuation and formatting

- Em dashes as asides (`—`, `---`, spaced `–`) `[grep]`
- Colon to build suspense `[grep: line ending with ":"]`
  ✗ The reason is simple: the field was not written.
  ✓ The field was not written to the output stream.
- Bold in the body `[grep: \textbf, \bfseries]`
- Bullet lists instead of prose `[grep: \begin{itemize}, flagged for manual check]`
- Scare quotes ("so-called", terms in quotes for irony) `[grep: so-called]`
  ✗ The "dead" field.
  ✓ The identically zero field.

## 6. Stacked hedges

- "might potentially", "could possibly", "may potentially" `[grep]`
- "seems to suggest", "appears to indicate", "arguably" `[grep]`
- Scattered hedging adverbs: "probably", "likely", "somewhat", "to some extent", "fairly",
  "relatively", "tends to", "quite" `[grep]`
  ✗ The field is somewhat underestimated.
  ✓ The field is 0.625 of the ERA5 one.
