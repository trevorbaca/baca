from baca.specifications.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specifications.StatalServer import StatalServer


# TODO: implement & write tests
class DuratedStatalServer(StatalServer):

    ### SPECIAL METHODS ###
    
    def __call__(self, request):
        if isinstance(request, DuratedStatalServerRequest):
            raise NotImplementedError
        else:
            return StatalServer(request)
