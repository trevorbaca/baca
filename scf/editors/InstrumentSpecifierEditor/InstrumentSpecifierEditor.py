from scf.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.InstrumentSpecifier import InstrumentSpecifier
from scf import selectors


class InstrumentSpecifierEditor(ParameterSpecifierEditor):

    def __init__(self, instruments=None, session=None, target=None):
        ParameterSpecifierEditor.__init__(self, session=session, target=target)
        self.instruments = instruments or []

    ### CLASS ATTRIBUTES ###

    target_class = InstrumentSpecifier
    target_manifest = TargetManifest(InstrumentSpecifier,
        ('instrument', 'st', selectors.InstrumentSelector),
        )

    ### READ-ONLY ATTRIBUTES ###

    @property
    def target_name(self):
        try:
            return self.target.instrument.name
        except AttributeError:
            pass

    ### PUBLIC METHODS ###

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        kwargs = {}
        if menu_key == 'st':
            kwargs['instruments'] = self.instruments
        return kwargs
