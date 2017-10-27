import abjad


class ScoreTemplate(abjad.ScoreTemplate):
    r'''Score template
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    voice_colors = {
        }

    ### PRIVATE METHODS ###

    def _attach_tag(self, instrument_tag, context):
        assert isinstance(instrument_tag, str), repr(str)
        tag_string = f'tag {instrument_tag}'
        tag_command = abjad.LilyPondCommand(
            tag_string,
            'before',
            )
        abjad.attach(tag_command, context)

    def _make_time_signature_context(self):
        time_signature_context_multimeasure_rests = abjad.Context(
            context_name='GlobalRests',
            name='Global Rests',
            )
        time_signature_context_skips = abjad.Context(
            context_name='GlobalSkips',
            name='Global Skips',
            )
        time_signature_context = abjad.Context(
            [
                time_signature_context_multimeasure_rests,
                time_signature_context_skips,
            ],
            context_name='GlobalContext',
            is_simultaneous=True,
            name='Global Context',
            )
        return time_signature_context

    def _validate_voice_names(self, score):
        voice_names = []
        for voice in abjad.iterate(score).components(abjad.Voice):
            voice_names.append(voice.name)
        for voice_name in sorted(self.voice_colors):
            if voice_name not in voice_names:
                raise Exception(f'voice not in score: {voice_name!r}.')
