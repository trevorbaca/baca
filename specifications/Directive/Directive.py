from baca.specifications.Selection import Selection


class Directive(object):

    ### INITIALIZER ###

    def __init__(self, chunk_name=None):
        self.chunk_name = chunk_name
        self.divion_handler = None
        self.selection = None
        self.rhythm_handler = None

    ### PUBLIC METHODS ###

    def select_chunk(self):
        selection = Selection()
        selection.append_constituent(self.chunk_name)
        self.selection = selection

    def select_voice(self, voice_name):
        selection = Selection()
        selection.append_constituent(voice_name)
        self.selection = selection

    def set_clusters(self, cluster_handler):
        self.cluster_handler

    def set_dynamics(self, dynamic_handler):
        self.dynamic_handler = dynamic_handler

    def set_pitch_classes(server, pitch_class_handler):
        self.pitch_class_server = server
        self.pitch_class_handler = pitch_class_handler
    
    def set_rhythm(self, division_handler, rhythm_handler):
        self.division_handler = division_handler
        self.rhythm_handler = rhythm_handler
