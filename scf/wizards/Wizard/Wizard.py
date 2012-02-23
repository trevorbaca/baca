from scf.core.SCFObject import SCFObject


class Wizard(SCFObject):

    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        self.target = target
