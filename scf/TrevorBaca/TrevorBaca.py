# -*- encoding: utf-8 -*-
from baca.scf.Composer import Composer
import datetime


class TrevorBaca(Composer):

    def __init__(self):
        Composer.__init__(self,
            last_name = 'Bača',
            first_name = 'Trevor',
            birthdate = datetime.datetime(1975, 10, 14))

    ### OVERLOADS ###
    
    def __repr__(self):
        return '%s()' % type(self).__name__
