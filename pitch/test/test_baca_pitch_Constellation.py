import baca
from baca.pitch.Constellation import Constellation


## TEST OVERRIDES ##

def test_baca_pitch_Constellation_01():

    constellation = baca.pitch.CC[0]
    assert isinstance(constellation, Constellation)
