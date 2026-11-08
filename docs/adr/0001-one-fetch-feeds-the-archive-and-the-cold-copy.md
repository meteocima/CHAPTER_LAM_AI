# From 2018 back, one fetch of each wrfout feeds both the archive and the Cold Copy

From 2018 back, each wrfout is fetched once. From that one fetch this repo writes its GRIB2
archive and also has CHAPTER_INHOUSE's Ingest write the Cold Copy's day files. A wrfout is
deleted only when both are done. Fetching twice would spend the relay, and possibly a second
tape recall, on 9.14 GB files that serve another project too (CHAPTER_INHOUSE ADR-0031). For
2019-2025 the wrfout were already converted and deleted, so they are fetched a second time,
by this repo's campaigns and not by CHAPTER_INHOUSE's Pass (amendment below). Settled with the
user in #73 on 2026-11-01.

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
- **The Cold Copy leaves Leonardo by itself, and the wrfout wait for it.** A day gets its
  `sha256sum` file only after its files are read back whole. The sequence runs
  CHAPTER_INHOUSE's copy (`tools.nas_push`, #38) in the background: it sends each such day to
  CIMA's NAS, checks it there and only then deletes its day files here. A wrfout goes only
  once its GRIB is written and every day reading it is in the copy's ledger, and the Static
  file goes at the campaign's end, so only the GRIB and the checksum files (the record that
  a day is done: without them a re-run would write it again) stay on Leonardo. Decided on
  2026-11-02, before launching 2018: until then the copy was a separate, manual step, and the
  wrfout went once their days were written on Leonardo.

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

## Outcome (2018)

Run once, over the whole of 2018, from 2026-11-02 to 2026-11-07 23:12Z (`DONE`): 8760 GRIB,
`check_grib_sanity` bad=0 in all 12 months; 365 Cold Copy days delivered, none lost whole, all
365 on CIMA's NAS (7.0 TB, `NAS_FINISHED`); `LEONARDO_CLEAN`, so only the GRIB and
`_checksums/*.sha256` stayed here. One fetch per wrfout held: no month was fetched twice for
the Cold Copy, bar day 2018-02-03's edge state, the defect of #74. The incidents on the way
(the `grep -q` under pipefail, the 0-byte relay, the double write of April, the login-node
outage, the NAS off for 8.6 h) are in CLAUDE.md's HPC gotchas; none came from the decision itself.

## Amendment (2026-11-08): 2019-2025, the Cold Copy alone, by this repo (#74)

The years whose GRIB were written before #73 get their Cold Copy from this repo's sequence too,
not from CHAPTER_INHOUSE's Pass: the same `run_year_rebuild.sh`, Ingest, NAS copy and sweep
that delivered 2018, one sequence per year (`COLD_COPY=true YEARS="2019"`). Their wrfout are
fetched a second time -- the one fetch of this ADR cannot be had back for years already
converted -- but once only, for the Cold Copy alone.

**No separate mode.** With `COLD_COPY=true` a wrfout is fetched while either reader still
needs it and it is not local: the archive (an hour reading its state has no GRIB and its
snapshot is missing) or the Cold Copy (a day of the campaign reading it is not delivered).
The driver asks the Ingest which, once per process (`cold_copy_day.py wanted`, over
`cold-copy-day released`), so the rule of which days read a wrfout stays there. 2018 (no
GRIB), 2019-2025 (no day) and the defect of #74 (a GRIB, an undelivered day: a trial's edge
the next phase skipped on its GRIB) are the same rule. A phase with no GRIB missing gets no
convert chain, no snapshot is written that no convert would release, and the sweep does not
wait for a reading hour past the campaign, which lets the record's last hour, 2025-07-02T23,
go.

Considered: a `COLD_COPY_ONLY` switch. Rejected because a switch can disagree with the data
-- a month with one GRIB missing, or the edge of #74 -- where the rule per reader cannot.
The 2019-01-01 edge that the option above would have kept is fetched by the 2019 campaign as
its state before the window.

