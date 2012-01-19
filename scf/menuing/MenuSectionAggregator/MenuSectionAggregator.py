from baca.scf.menuing.MenuObject import MenuObject


class MenuSectionAggregator(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._sections = []

    ### READ-ONLY ATTRIBUTES ###

    @property
    def sections(self):
        return self._sections
