from baca.specification.Constituent import Constituent


class Selection(object):

    ### INITIALIZER ###

    def __init__(self, 
        score_segment_name=None, constituents=None, context_name=None, 
        criterion=None, start=None, stop=None):
        self.constituents = constituents or []
        if any([score_segment_name, context_name, criterion, start, stop]):
            self.append_constituent(
                score_segment_name=score_segment_name, context_name=context_name,
                criterion=criterion, start=start, stop=stop)

    ### PUBLIC METHODS ###

    def append_constituent(self, 
        score_segment_name=None, context_name=None, criterion=None, start=None, stop=None):
        constituent = Constituent(
            score_segment_name=None, context_name=None, criterion=criterion, start=None, stop=None)
        self.constituents.append(constituent)

    def append_note_and_chord_constituent(self, 
        score_segment_name=None, context_name=None, start=None, stop=None):
        constituent = Constituent(score_segment_name=score_segment_name, context_name=context_name, 
            criterion='note and chord', start=start, stop=stop)
        self.constituents.append(constituent)
