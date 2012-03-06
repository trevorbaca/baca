from scf.wizards.Wizard import Wizard
from scf import selectors


class PitchClassTransformCreationWizard(Wizard):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'pitch class transform creation wizard'

    ### PUBLIC METHODS ###

    def get_explicit_breadcrumb(self, transform_indicator_pairs):
        if transform_indicator_pairs:
            return 'append pitch-class transform:'

    def get_pitch_class_transform_argument(self, pitch_class_transform_name):
        if pitch_class_transform_name in ('transpose', 'multiply'):
            getter = self.make_getter(where=self.where())
            getter.append_integer_in_range('index', start=0, stop=11)
            result = getter.run()
            if self.backtrack():
                return
            return result
        elif pitch_class_transform_name in ('invert'):
            return 'None'
        else:
            raise ValueError(pitch_class_transform_name)

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        transform_indicator_pairs = []
        while True:
            breadcrumb = self.transform_indicator_pairs_to_breadcrumb(transform_indicator_pairs)
            self.push_breadcrumb(breadcrumb=breadcrumb)
            selector = selectors.PitchClassTransformSelector(session=self.session)
            selector.explicit_breadcrumb = self.get_explicit_breadcrumb(transform_indicator_pairs)
            self.push_backtrack()
            pitch_class_transform_name = selector.run(clear=clear)
            self.pop_backtrack()
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
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return transform_indicator_pairs

    def transform_indicator_pairs_to_breadcrumb(self, transform_indicator_pairs):
        if transform_indicator_pairs:
            result = []
            for transform_name, transform_argument in transform_indicator_pairs:
                string = transform_name[0].upper()
                if string in ('T', 'M'):
                    string = string + str(transform_argument)
                result.append(string)
            result = ''.join(result)
            return '{} - {}'.format(self.breadcrumb, result)
        else:
            return self.breadcrumb
