from abjad.tools.abctools.AbjadObject import AbjadObject


class DivisionsRetrievalRequest(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, voice_name, start_segment_name, callback=None, count=None, n=1, offset=None):
        self.voice_name = voice_name
        self.start_segment_name = start_segment_name
        self.callback = callback
        self.count = count
        self.n = n
        self.offset = offset
