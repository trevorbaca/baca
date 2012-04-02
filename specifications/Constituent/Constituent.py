class Constituent(object):

    ### INITIALIZER ###

    def __init__(self, component_name, criterion=None, start=None, stop=None):
        self.component_name = component_name
        self.criterion = criterion
        self.start = start
        self.stop = stop
