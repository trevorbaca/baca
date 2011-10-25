import datetime


class Composer(object):
    
    def __init__(self, last_name=None, first_name=None, birthdate=None):
        assert isinstance(last_name, (str, type(None)))
        assert isinstance(first_name, (str, type(None)))
        assert isinstance(birthdate, (datetime.datetime, type(None)))
        self._last_name = last_name
        self._first_name = first_name
        self._birthdate = birthdate

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r, %r)' % (type(self).__name__, self.last_name, self.first_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def birthdate(self):
        return self._birthdate

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name
