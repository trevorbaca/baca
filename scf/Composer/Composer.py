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

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.last_name == other.last_name:
                if self.first_name == other.first_name:
                    if self.birthdate == other.birthdate:
                        return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(type(self).__name__, self.last_name, self.first_name, self.birthdate)

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
