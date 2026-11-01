# CHAPTER

CHAPTER is a dataset: a 3 km dynamical downscaling of ERA5 over Europe and the
Mediterranean basin, produced with WRF. This repository does not produce it — it converts
it, from the hourly wrfout it is delivered as into an ECMWF-compatible GRIB2 archive, and
from there into an Anemoi training dataset.

Two halves share this repo: the **conversion**, which decides what a GRIB file contains,
and the **orchestration**, which moves 9 GB files between two supercomputers. They share
almost no vocabulary, and the words that do cross over are the ones that collide.

This file is a glossary and nothing else. The reasoning behind the science — why `tp` is
the hour ending at its timestep and where 00Z takes it from, how the `skt` emissivity was measured, which hypotheses were refuted —
lives in `CLAUDE.md`, and what cannot be produced at all lives in `MISSING_VARIABLES.md`.

## Language

### Conversion

**CHAPTER**:
The dataset being converted: a 3 km dynamical downscaling of ERA5 over Europe and the
Mediterranean, produced with WRF and delivered as hourly wrfout.
_Avoid_: CHAPTER for the conversion pipeline, for this repository, or for the GRIB2 archive
it produces.

**Archive**:
The GRIB2 output of the conversion, one file per timestep. The archive is a rendering of
CHAPTER, not CHAPTER itself.

**Run**:
One WRF simulation, initialised at 18Z and lasting 30 h: its 6 h spinup, then the 24 h it
gives the archive, 01Z of its day to 00Z of the next.
_Avoid_: simulation. For an execution of the pipeline say execution or re-run, never run.

**Run folder**:
The directory on the remote archive holding one run's output, named for the run's
initialisation rather than for the dates it covers.
_Avoid_: init folder

**Spinup**:
The first 6 h of a run, discarded: output for a given date is taken from the run
initialised the previous evening, once that spinup has elapsed.
_Avoid_: spinoff

**Timestep**:
One hour of a run: one wrfout file in, one GRIB file out. The unit of work of the
step pipeline and the key of the ledger.
_Avoid_: step, hour

**Variable**:
One row of the registry: a produced quantity together with its ECMWF identity — shortName,
paramId, level type and the levels it is written on.
_Avoid_: entry, field, key, row

**GRIB message**:
One record inside a GRIB file: one variable, on one level, at one time. The archive's
90 variables produce 246 messages per timestep.
_Avoid_: record

**Schema**:
The message inventory a complete GRIB file must have — which shortNames, and how many of
each. A file is at the current schema or it is reconverted.

**GRIB step**:
The forecast step range encoded in a message, as opposed to the timestep it is valid at.
Accumulated variables carry a range; instantaneous ones do not.
_Avoid_: step

**Dataset variable**:
One column of the Anemoi dataset: one GRIB message's variable on one level (`t_850`, `2t`),
or a forcing anemoi computes at build time (`cos_latitude`). A pressure-level variable is
thirteen dataset variables; the archive's 246 messages plus the forcings make 255.
_Avoid_: variable, when the Anemoi column is meant

**Sidecar**:
A small file beside the archive holding something the converter needs but cannot read from
the timestep it is converting.

**Accumulation sidecar**:
The per-day sidecar holding a day's 00Z values, against which that day's accumulated
variables are referred. A timestep with no accumulation sidecar is not converted at all.

**Static sidecar**:
The single sidecar derived once from `geo_em`, holding the seven static fields. Unlike the
accumulation sidecar it is one file for the whole archive, not a per-day tree.

**Static**:
Invariant across every timestep of the archive. Exactly the seven fields read from the
static sidecar. `lsm` and `al` are **not** static: WRF reclassifies sea-ice points at
runtime, so both move.
_Avoid_: using static for a field that is merely expected to be non-zero.

**Dead field**:
A field that is identically zero on every sampled timestep. A dead field is not published,
whatever the physical reason for its being zero.

**Published**:
Written into the archive as a variable. The bar is that the WRF quantity **is** the ERA5
one, or that the difference states in one line; a field can be alive, useful and still
unpublished because nothing in ERA5 fits it.
_Avoid_: exported, included

**Unpublished**:
Present in the wrfout and deliberately left out, as distinct from a field that cannot be
produced at all. The first is a decision and is recorded in `CHAPTER_VARIABLES.md`; the
second is a limit of the run and is recorded in `MISSING_VARIABLES.md`.
_Avoid_: missing, excluded — both blur the two.

### Audit

**Verdict**:
What the audit produces for one variable: a statement about whether the published
quantity is the one it claims to be, together with what that statement rests on.
A verdict is one of exactly three things — verified, wrong, or unverifiable — and
naming which is part of it.
_Avoid_: result, outcome, status.

**Verified**:
There is a measurement, and the verdict names which comparison produced it. Not
"it looks right": a verdict of verified without a named measurement is not a
verdict.

**Wrong**:
There is a measurement, and it disagrees. A verdict of wrong carries the issue
that records the defect, because this map measures and decides but does not
repair.

**Unverifiable**:
No comparison exists that could settle the variable, and the verdict says which
ones were tried and why each failed. **Never a default**: it is reached only
after the alternatives have been excluded in writing, and a variable nobody got
round to measuring is not unverifiable, it is unmeasured.
_Avoid_: unknown, untested — both blur the difference between "there is no way to
know" and "we did not look".

**Unmeasured**:
No verdict yet. A state of the audit, never a state of a variable.

### Orchestration

**Campaign**:
One bounded effort to fill a stretch of the archive, run as a detached login-node script
that survives being logged out. Spelled `sequence` in filenames and logs.
_Avoid_: sequence

**Phase**:
A campaign's sub-window, roughly a month, processed by its own pair of chains. Phases exist
so that no more than two of them occupy disk at once.

**Chain**:
One self-respawning driver lineage, identified by its own ledger, driver log and stop flag.
Two chains sharing any of those three would collide.

**Batch**:
The timesteps one driver process handles before it respawns — bounded by a count and by a
wall-time budget, whichever comes first.

**Window**:
A closed, inclusive range of dates and hours. An axis, not a level of containment: a
campaign, a phase and a chain each have one.
_Avoid_: using window for a campaign's phase table.

**Driver**:
The login-node process that walks a window one timestep at a time, fetching each and
submitting its conversion, then respawns itself for the next batch.

**Ledger**:
The append-only record of what happened to each timestep, one line per outcome, written
by a single chain. Spelled `status_log` in the configuration.
_Avoid_: status log

**Stage / staged**:
Placed on Leonardo disk and kept there. Staged files are deleted only deliberately.
_Avoid_: stage in the tape sense, even though LRZ's own tool calls it so (`dsacli stage`);
recalling from tape is recall.

**Recall**:
Bringing a file back from tape on the LRZ side, so that it can be fetched at all.

**Re-entrant**:
Safe to re-run over work already done: each timestep decides for itself whether it is
already finished and skips if so.

### Cold Copy

Terms owned by `meteocima/CHAPTER_INHOUSE` and defined in its `CONTEXT.md`; this repo uses
them as defined there, and adds none of its own. Two words collide: **Archive** there is the
platform's public store, here the GRIB2 archive; **Product** there is what a user's request
yields, so this repo does not call the GRIB2 archive and the Cold Copy "two products".

**Cold Copy**:
CIMA's own copy of the wrfout's informative fields, hourly, on model levels, one surface file
and one 3D file per calendar day. From 2018 back this repo writes it, beside the archive, from
the same fetched wrfout.
_Avoid_: backup, second archive

**Ingest**:
The code, in CHAPTER_INHOUSE, that writes the Cold Copy's files of one day from that day's
wrfout. This repo calls it; it does not reimplement it.
_Avoid_: conversion (that is what this repo does to make the archive)

**Day files**:
One calendar day of the Cold Copy, its surface file and its 3D file together. Day D reads 26
wrfout of two runs: leads 29 and 30 of the run for D-1, leads 6 to 29 of the run for D.

**Pass**:
CHAPTER_INHOUSE's own traversal of the wrfout to write the Cold Copy where this repo does not:
2019 to 2025.
_Avoid_: campaign, which is this repo's

**Hole**:
A wrfout lost at the source, declared so after verification on LRZ, that a day file holds
empty rather than waits for.
_Avoid_: gap, a wrfout merely not fetched yet

