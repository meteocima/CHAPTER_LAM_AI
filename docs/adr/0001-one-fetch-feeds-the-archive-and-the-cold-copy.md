# From 2018 back, one fetch of each wrfout feeds both the archive and the Cold Copy

From 2018 back, each wrfout is fetched once. From that one fetch this repo writes its GRIB2
archive and also has CHAPTER_INHOUSE's Ingest write the Cold Copy's day files. A wrfout is
deleted only when both are done. Fetching twice would spend the relay, and possibly a second
tape recall, on 9.14 GB files that serve another project too (CHAPTER_INHOUSE ADR-0031). For
2019-2025 the wrfout were already converted and deleted, so CHAPTER_INHOUSE's Pass fetches
them again. Settled with the user in #73 on 2026-11-01.

## How

- **The Ingest is called per phase, not per timestep.** When a phase's convert chain is
  done, a SLURM array writes one day per task on `dcgp_usr_prod`. A monthly phase already
  fetches every wrfout its own days read. The convert chain keeps its wrfout, and the driver
  also keeps the two files it used to throw away after their snapshot: the spin-up 00Z,
  which the Cold Copy reads for the accumulators of 01Z, and the state before the window.
  The task then deletes each wrfout whose GRIB exists and whose reading days are all
  written. The readers of a wrfout come from the Ingest's own `wrfouts_of_day`. A month's
  last 23Z is read by the next month's first day too, so the next phase deletes it.
- **The Ingest is called as a subprocess**, from a CHAPTER_INHOUSE clone pinned to a tag
  with its own uv project. The two venvs stay apart, and the development checkout, which is
  live code, is never what a job runs.
- **A Hole is declared, never inferred.** A wrfout missing from staging stops its day. It
  becomes a Hole only once its loss is verified on LRZ and it is listed, in the same list
  that writes the archive's missing timesteps.
- **The Cold Copy leaves Leonardo through a manifest.** A day gets its sha256 manifest only
  after its files are read back whole. CHAPTER_INHOUSE #38 copies days that have a manifest
  to CIMA's NAS, checks size and sha256 there, and only then deletes them here. This repo
  knows nothing of the NAS.

## Considered options

- **Ingest called by each convert job, or by the driver as each day completes**: both put
  the waiting into the driver and `convert_step.sh`, the most fragile code here. Per phase,
  the guard is one step at the end of the phase, at the cost of a month of wrfout (~7 TB)
  on disk until its array ends.
- **Ingest as a dependency of this venv**: one venv read live by every compute node, two
  projects' pins inside it.
- **Keeping 2018-12-31T23 and 2019-01-01T00 for the 2019-2025 Pass**, which reads them for
  Cold Copy day 2019-01-01: the Pass fetches the whole of 2019 anyway, and two files kept
  for an open-ended time are not worth it.
