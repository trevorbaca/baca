# -*- coding: utf-8 -*-
import abc
import abjad


class ScoreTemplate(abjad.abctools.AbjadValueObject):
    r'''Score template
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Templates'

    voice_abbreviations = {
        }

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''
        pass

    ### PRIVATE METHODS ###

    def _attach_tag(self, instrument_tag, context):
        assert isinstance(instrument_tag, str), repr(str)
        tag_string = 'tag {}'.format(instrument_tag)
        tag_command = abjad.indicatortools.LilyPondCommand(tag_string, 'before')
        abjad.attach(tag_command, context)

    def _make_time_signature_context(self):
        time_signature_context_multimeasure_rests = abjad.scoretools.Context(
            context_name='TimeSignatureContextMultimeasureRests',
            name='Time Signature Context Multimeasure Rests',
            )
        time_signature_context_skips = abjad.scoretools.Context(
            context_name='TimeSignatureContextSkips',
            name='Time Signature Context Skips',
            )
        time_signature_context = abjad.scoretools.Context(
            [
                time_signature_context_multimeasure_rests,
                time_signature_context_skips,
            ],
            context_name='TimeSignatureContext',
            is_simultaneous=True,
            name='Time Signature Context',
            )
        return time_signature_context