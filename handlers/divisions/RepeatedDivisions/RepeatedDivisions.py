from abjad.tools import sequencetools
from baca.handlers.divisions.DivisionHandler import DivisionHandler


class RepeatedDivisions(DivisionHandler):

    ### INITIALIZER ##

    def __init__(self, divisions, remainder='right'):
        self.divisions = sequencetools.CyclicTuple(divisions)
        self.remainder = remainder

    ### PUBLIC METHODS ###

    def apply(self, time_signatures):
        result = []
        total_duration = sum([durationtools.Duration(x) for x in time_signatures])
        for division in self.divisions:
            if sum(result) < total_duration:
                # TODO: finish implementation
                pass
