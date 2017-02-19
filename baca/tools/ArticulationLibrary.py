# -*- coding: utf-8 -*-
import abjad


class ArticulationLibrary(object):
    '''Articulation interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

    @staticmethod
    def accents():
        import baca
        return baca.tools.ArticulationSpecifier(articulations=['>'])

    @staticmethod
    def alternate_accented_bow_strokes():
        import baca
        return baca.tools.ArticulationSpecifier(
            articulations=(['upbow', 'accent'], ['downbow', 'accent']),
            )

    @staticmethod
    def alternate_bow_strokes(downbow_first=True):
        import baca
        if downbow_first:
            return baca.tools.ArticulationSpecifier(
                articulations=(['downbow'], ['upbow']),
                )
        else:
            return baca.tools.ArticulationSpecifier(
                articulations=(['upbow'], ['downbow']),
                )

    @staticmethod
    def double_tonguing():
        import baca
        return baca.tools.ArticulationSpecifier(articulations=['tongue #2'])

    @staticmethod
    def down_bows():
        import baca
        return baca.tools.ArticulationSpecifier(articulations=['downbow'])

    @staticmethod
    def flageolet():
        return abjad.indicatortools.LilyPondCommand(
            'flageolet',
            format_slot='right',
            )

    @staticmethod
    def laissez_vibrer():
        import baca
        return baca.tools.ArticulationSpecifier(articulations=['laissezVibrer'])

    @staticmethod
    def marcati():
        import baca
        # TODO: avoid nontrivial logical ties
        return baca.tools.ArticulationSpecifier(articulations=['marcato'])

    @staticmethod
    def staccati():
        import baca
        # TODO: avoid nontrivial logical ties
        return baca.tools.ArticulationSpecifier(articulations=['staccato'])

    @staticmethod
    def staccatissimi():
        import baca
        # TODO: avoid nontrivial logical ties
        return baca.tools.ArticulationSpecifier(articulations=['staccatissimo'])

    @staticmethod
    def stem_tremolo():
        import baca
        return baca.tools.StemTremoloSpecifier(tremolo_flags=32)

    @staticmethod
    def tenuti():
        import baca
        return baca.tools.ArticulationSpecifier(articulations=['tenuto'])

    @staticmethod
    def tremolo_down(n, maximum_adjustment=-1.5):
        import baca
        pair = (0, -n)
        return experimental.tools.baca.tools.OverrideSpecifier(
            grob_name='stem_tremolo',
            attribute_name='extra_offset',
            attribute_value=str(pair),
            maximum_written_duration=abjad.Duration(1),
            maximum_settings={
                'grob_name': 'stem_tremolo',
                'attribute_name': 'extra_offset',
                'attribute_value': str((0, maximum_adjustment)),
                },
            )

    @staticmethod
    def up_bows():
        import baca
        return baca.tools.ArticulationSpecifier(articulations=['upbow'])
