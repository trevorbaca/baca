import baca
import datetime


def test_TrevorBaca_01():

    trevor_baca = baca.scf.TrevorBaca()

    assert trevor_baca.last_name == 'Bača'
    assert trevor_baca.first_name == 'Trevor'
    assert trevor_baca.birthdate == datetime.datetime(1975, 10, 14)    
