# -*- encoding: utf-8 -*-
from baca.scf.Composer import Composer
import datetime


def signature():
    
    return Composer(
        last_name = 'Bača',
        first_name = 'Trevor',
        birthdate = datetime.datetime(1975, 10, 14))
