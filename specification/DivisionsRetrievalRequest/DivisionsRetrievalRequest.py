from abjad.tools.abctools.AbjadObject import AbjadObject


class DivisionsRetrievalRequest(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, voice_name, start_segment_name, n=1):
        self.voice_name = voice_name
        self.start_segment_name = start_segment_name
        self.n = n
