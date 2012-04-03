from baca.specifications.StatalServerRequest import StatalServerRequest


class DuratedStatalServerRequest(StatalServerRequest):

    ### INITIALIZER ###
    
    def __init__(self, server, n, complete=False, criterion='exactly', level=None, position=None):
        StatalServerRequest.__init__(self, server, n, complete=complete, level=level, position=position)
        self.criterion = criterion
