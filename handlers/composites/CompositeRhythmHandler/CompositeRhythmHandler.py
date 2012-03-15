from handlers.Handler import Handler


class CompositeRhythmHandler(Handler):

    ### INITIALIZER ###

    def __init__(self, division_handler, rhythm_handler):
        self.division_handler = division_handler
        self.rhythm_handler = rhythm_handler

    ### SPECIAL METHODS ###

    def __call__(self, time_signatures):
        divisions = self.division_handler(time_signatures)
        tuplets = self.rhythm_handler(divisions)
        return tuplets

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _tools_package(self):
        return 'handlers.composites'
