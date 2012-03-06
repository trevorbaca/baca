from scf.wizards.Wizard import Wizard
from scf import selectors


class PitchClassTransformCreationWizard(Wizard):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'pitch class transform creation wizard'

    ### PUBLIC METHODS ###

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        transform_indicator_pairs = []
        while True:
            self.push_breadcrumb()
            selector = selectors.PitchClassTransformSelector(session=self.session)
            pitch_class_transform_name = selector.run(clear=clear)
            if self.backtrack():
                break
            elif not pitch_class_transform_name:
                self.pop_breadcrumb()
                continue
            pitch_class_transform_argument = self.get_pitch_class_transform_argument(
                pitch_class_transform_name)
            if self.backtrack():
                break
            elif not pitch_class_transform_argument:
                self.pop_breadcrumb()
                continue
            pair = (pitch_class_transform_name, pitch_class_transform_argument)
            transform_indicator_pairs.append(pair)
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return transform_indicator_pairs
