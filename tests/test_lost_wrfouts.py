"""One list of wrfout verified lost on LRZ, for the archive and the Cold Copy (#73, ADR-0001).

`pipeline.lost_wrfouts` names each lost wrfout by run and lead. The Cold Copy reads
every entry as a Hole; the archive reads the lead-30 ones as before it read
`pipeline.missing_00z_days`: lead 30 of a run is the whole 00Z of the day after the
day it was run for (#72), which is then written missing. The old list still counts,
so nothing declared before is undeclared.
"""
from omegaconf import OmegaConf

from hpc.submit_step_pipeline import missing_00z_days


def pipeline(**kw):
    return OmegaConf.create({"missing_00z_days": [], "lost_wrfouts": [], **kw})


def test_a_lost_lead_30_is_the_00z_of_two_days_after_its_run_is_initialised():
    # Run 2018031018 is the run for 2018-03-11; its lead 30 is 2018-03-12T00 (#72).
    cfg = pipeline(lost_wrfouts=[{"run": "2018031018", "lead": 30, "reason": "x"}])
    assert missing_00z_days(cfg) == ["2018-03-12"]


def test_a_lost_wrfout_of_any_other_lead_leaves_the_archive_waiting():
    # Lead 6 is the spin-up 00Z, leads 7-29 an hour the archive has no rule to write
    # missing: the convert waits, as it always has.
    cfg = pipeline(lost_wrfouts=[{"run": "2018031018", "lead": 6, "reason": "x"},
                                 {"run": "2018031018", "lead": 15, "reason": "x"}])
    assert missing_00z_days(cfg) == []


def test_days_declared_the_old_way_still_count_once():
    cfg = pipeline(missing_00z_days=["2019-07-04", "2018-03-12"],
                   lost_wrfouts=[{"run": "2018031018", "lead": 30, "reason": "x"}])
    assert missing_00z_days(cfg) == ["2018-03-12", "2019-07-04"]
