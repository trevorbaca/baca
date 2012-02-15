from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.MusicSpecifier import MusicSpecifier


class MusicSpecifierEditor(InteractiveEditor):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name of 'music specifier editor'
        
    target_attribute_tuples = (
        ('music_specifier_name', predicates.is_string, True, None, 'sn'),
        ('tempo', predicates.is_tempo_token, True, None, 'tp'),
        #('performer_contribution_specifiers', object, 
        )

    target_class = MusicSpecifier

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.music_specifier_name
