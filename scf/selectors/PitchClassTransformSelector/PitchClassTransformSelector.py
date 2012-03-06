from scf.selectors.Selector import Selector


class PitchClassTransformSelector(Selector):

    ### CLASS ATTRIBUTES ###

    tags_to_match = ('is_pitch_class_transform', )
    target_human_readable_name = 'pitch-class transform'

    ### PUBLIC METHODS ###

    def list_target_items(self):
        result = []
        result.append('transpose')
        result.append('invert')
        result.append('multiply')
        return result
