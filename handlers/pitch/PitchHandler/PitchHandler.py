from handlers.Handler import Handler


class PitchHandler(Handler):

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _tools_package(self):
        return 'handlers.pitch'
