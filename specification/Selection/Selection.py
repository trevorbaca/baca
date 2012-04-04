from baca.specification.Constituent import Constituent


class Selection(object):

    ### INITIALIZER ###

    def __init__(self, 
        constituents=None, context_name=None, criterion=None, 
        score_segment_name=None, start=None, stop=None):
        self.constituents = constituents or []
        if any([score_segment_name, context_name, criterion, start, stop]):
            self.append_constituent(
                score_segment_name=score_segment_name, context_name=context_name,
                criterion=criterion, start=start, stop=stop)

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        return self.constituents.__getitem__(arg)

    def __getslice__(self, start, stop):
        return self.constituents.__getslice__(start, stop)

    def __repr__(self):
        return '{}({!r}'.format(type(self).__name__, self.constituents)

    ### PUBLIC METHODS ###

    def append_constituent(self, 
        context_name=None, criterion=None, score_segment_name=None, start=None, stop=None):
        constituent = Constituent(context_name=context_name, criterion=criterion, 
            score_segment_name=score_segment_name, start=start, stop=stop)
        self.constituents.append(constituent)

    def append_note_and_chord_constituent(self, 
        score_segment_name=None, context_name=None, start=None, stop=None):
        constituent = Constituent(score_segment_name=score_segment_name, context_name=context_name, 
            criterion='note and chord', start=start, stop=stop)
        self.constituents.append(constituent)
