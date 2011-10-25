import baca
import datetime


def test_Composer_01():

    composer = baca.scf.Composer('Bača', 'Trevor', datetime.datetime(1975, 10, 14))

    assert composer.last_name == 'Bača'
    assert composer.first_name == 'Trevor'
    assert composer.birthdate == datetime.datetime(1975, 10, 14)
