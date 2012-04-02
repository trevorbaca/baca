from handlers.pitch.PitchHandler import PitchHandler


class OctaveTranspositionHandler(PitchHandler):

    ### INITIALIZER ###

    def __init__(self, octave_transposition_mapping):
        self.octave_transposition_mapping = octave_transposition_mapping

    ### SPECIAL METHODS ###

    # TODO: implement based on L'archipel register_pitches.py
    def __call__(self, expr):
        pass   
