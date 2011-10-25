import baca
import datetime


def test_helpers_signature_01():

    composer = baca.scf.helpers.signature()

    assert isinstance(composer, baca.scf.Composer)
    assert composer.last_name == 'Bača'
    assert composer.first_name == 'Trevor'
    assert composer.birthdate == datetime.datetime(1975, 10, 14)
