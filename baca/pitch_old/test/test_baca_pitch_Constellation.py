import baca
from baca.pitch_old.Constellation import Constellation


## TEST OVERRIDES ##

def test_baca_pitch_Constellation_01():

    constellation = baca.pitch_old.CC[0]
    assert isinstance(constellation, Constellation)
