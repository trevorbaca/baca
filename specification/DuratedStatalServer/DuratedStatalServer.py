from baca.specification.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specification.StatalServer import StatalServer


class DuratedStatalServer(StatalServer):

    ### SPECIAL METHODS ###
    
    def __call__(self, request):
        if isinstance(request, DuratedStatalServerRequest):
            raise NotImplementedError
        else:
            return StatalServer.__call__(self, request)
