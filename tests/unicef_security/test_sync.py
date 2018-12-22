from pathlib import Path

import vcr

from unicef_security.sync import load_business_area, load_region


@vcr.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/load_business_area.yml'))
def test_load_business_area(db):
    ret = load_business_area()
    assert len(ret.created) > 0
    assert len(ret.updated) == 0


@vcr.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/load_region.yml'))
def test_load_region(db):
    ret = load_region()
    assert len(ret.created) == 8
    assert len(ret.updated) == 0
