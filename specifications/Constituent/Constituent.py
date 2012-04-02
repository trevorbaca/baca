class Constituent(object):

    ### INITIALIZER ###

    def __init__(self, component_name, start=None, stop=None):
        self.component_name = component_name
        self.start = start
        self.stop = stop
