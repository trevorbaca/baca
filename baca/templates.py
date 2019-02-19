"""
Score template library.
"""
import abjad
import roman # type: ignore
import typing
from . import markups


### CLASSES ###

class ScoreTemplate(abjad.ScoreTemplate):
    """
    Score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_defaults',
        )

    voice_colors: dict = {
        }

    ### INITIALIZER ###

    def __init__(self) -> None:
        super().__init__()
        self._defaults: list = []

    ### PRIVATE METHODS ###

    @staticmethod
    def _assert_lilypond_identifiers(score):
        for context in abjad.iterate(score).components(abjad.Context):
            if not abjad.String(context.name).is_lilypond_identifier():
                message = f'invalid LilyPond identifier: {context.name!r}'
                raise Exception(message)
        
    @staticmethod
    def _assert_matching_custom_context_names(score):
        for context in abjad.iterate(score).components(abjad.Context):
            if context.lilypond_type in abjad.Context.lilypond_types:
                continue
            if context.name == context.lilypond_type:
                continue
            if context.name.replace('_', '') == context.lilypond_type:
                continue
            message = f'context {context.lilypond_type}'
            message += f' has name {context.name!r}.'
            raise Exception(message)

    @staticmethod
    def _assert_unique_context_names(score):
        names = []
        for context in abjad.iterate(score).components(abjad.Context):
            if context.name in names:
                raise Exception(f'duplicate context name: {context.name!r}.')

    def _attach_calltime_defaults(self, score):
        assert isinstance(score, abjad.Score)
        for lilypond_type, annotation, indicator in self.defaults:
            context = score[lilypond_type]
            abjad.annotate(context, annotation, indicator)
        
    def _attach_lilypond_tag(self, tag, context):
        for tag_ in tag.split('.'):
            if not abjad.String(tag_).is_lilypond_identifier():
                raise Exception(f'invalid LilyPond identifier: {tag_!r}.')
            part_names = [_.name for _ in self.part_manifest.parts]
            if part_names and tag_ not in part_names:
                raise Exception(f'not listed in parts manifest: {tag_!r}.')
        literal = abjad.LilyPondLiteral(fr'\tag {tag}', 'before')
        tag = 'baca.ScoreTemplate._attach_liypond_tag'
        abjad.attach(literal, context, tag=tag)

    @staticmethod
    def _set_square_delimiter(staff_group):
        abjad.setting(staff_group).system_start_delimiter = 'SystemStartSquare'

    @staticmethod
    def _to_roman(n):
        return roman.toRoman(n)

    def _validate_voice_names(self, score):
        voice_names = []
        for voice in abjad.iterate(score).components(abjad.Voice):
            voice_names.append(voice.name)
        for voice_name in sorted(self.voice_colors):
            if voice_name not in voice_names:
                raise Exception(f'voice not in score: {voice_name!r}.')

    ### PUBLIC PROPERTIES ###

    @property
    def defaults(self) -> list:
        """
        Gets defaults.
        """
        return self._defaults

    ### PUBLIC METHODS ###

    def group_families(self, *families) -> typing.List[abjad.Context]:
        """
        Groups ``families`` only when more than one family is passed in.

        Returns list of zero or more contexts.
        """
        families_ = []
        for family in families:
            if family is not None:
                assert isinstance(family, tuple), repr(family)
                if any(_ for _ in family[1:] if _ is not None):
                    families_.append(family)
        families = tuple(families_)
        contexts = []
        if len(families) == 0:
            pass
        elif len(families) == 1:
            family = families[0]
            contexts.extend([_ for _ in family[1:] if _ is not None])
        else:
            for family in families:
                if not isinstance(family, tuple):
                    assert isinstance(family, abjad.Context)
                    contexts.append(family)
                    continue
                square_staff_group = self.make_square_staff_group(*family)
                assert square_staff_group is not None
                contexts.append(square_staff_group)
        return contexts

    def make_music_context(self, *contexts) -> abjad.Context:
        """
        Makes music context.
        """
        contexts = tuple(_ for _ in contexts if _ is not None)
        return abjad.Context(
            contexts,
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='Music_Context',
            tag='baca.ScoreTemplate.make_music_context',
            )

    def make_piano_staff(
        self,
        stem: str,
        *contexts,
        ) -> typing.Optional[abjad.StaffGroup]:
        """
        Makes piano staff.
        """
        if not isinstance(stem, str):
            raise Exception(f'stem must be string: {stem!r}.')
        contexts = tuple(_ for _ in contexts if _ is not None)
        if contexts:
            return abjad.StaffGroup(contexts, name=f'{stem}_Piano_Staff')
        else:
            return None

    def make_square_staff_group(
        self,
        stem: str,
        *contexts,
        ) -> typing.Optional[typing.Union[abjad.Staff, abjad.StaffGroup]]:
        """
        Makes square staff group.
        """
        if not isinstance(stem, str):
            raise Exception(f'stem must be string: {stem!r}.')
        contexts = tuple(_ for _ in contexts if _ is not None)
        result = None
        if len(contexts) == 1:
            prototype = (abjad.Staff, abjad.StaffGroup)
            assert isinstance(contexts[0], prototype), repr(contexts[0])
            result = contexts[0]
        elif 1 < len(contexts):
            name = f'{stem}_Square_Staff_Group'
            staff_group = abjad.StaffGroup(
                contexts,
                name=name,
                tag='baca.ScoreTemplate.make_square_staff_group',
                )
            self._set_square_delimiter(staff_group)
            result = staff_group
        return result

    def make_staff_group(
        self,
        stem: str,
        *contexts,
        ) -> typing.Optional[abjad.StaffGroup]:
        """
        Makes staff group.
        """
        if not isinstance(stem, str):
            raise Exception(f'stem must be string: {stem!r}.')
        contexts = tuple(_ for _ in contexts if _ is not None)
        if contexts:
            return abjad.StaffGroup(
                contexts,
                name=f'{stem}_Staff_Group',
                tag='baca.ScoreTemplate.make_staff_group',
                )
        else:
            return None

class SingleStaffScoreTemplate(ScoreTemplate):
    r"""
    Single-staff score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        """
        Calls score template.
        """
        tag = 'baca.SingleStaffScoreTemplate.__call__'
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # MUSIC VOICE, MUSIC STAFF
        music_voice = abjad.Voice(
            name='Music_Voice',
            tag=tag,
            )
        music_staff = abjad.Staff(
            [music_voice],
            name='Music_Staff',
            tag=tag,
            )

        # MUSIC CONTEXT
        music_context = abjad.Context(
            [music_staff],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='Music_Context',
            tag=tag,
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            tag=tag,
            )
        self._attach_calltime_defaults(score)
        return score

class StringTrioScoreTemplate(ScoreTemplate):
    r"""
    String trio score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.StringTrioScoreTemplate.__call__
            <<                                                                                       %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.StringTrioScoreTemplate.__call__
                <<                                                                                   %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! baca.StringTrioScoreTemplate.__call__
                    <<                                                                               %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        \tag Violin                                                                  %! baca.ScoreTemplate._attach_liypond_tag
                        \context ViolinMusicStaff = "Violin_Music_Staff"                             %! baca.StringTrioScoreTemplate.__call__
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                            \context ViolinMusicVoice = "Violin_Music_Voice"                         %! baca.StringTrioScoreTemplate.__call__
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                                % [Violin_Music_Voice measure 1]                                     %! _comment_measure_numbers
                                \clef "treble"                                                       %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override ViolinMusicStaff.Clef.color = ##f                          %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set ViolinMusicStaff.forceClef = ##t                                %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                R1 * 1/2                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Violin)"                          %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)         %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [Violin_Music_Voice measure 2]                                     %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Violin_Music_Voice measure 3]                                     %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Violin_Music_Voice measure 4]                                     %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        \tag Viola                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                        \context ViolaMusicStaff = "Viola_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                            \context ViolaMusicVoice = "Viola_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                                % [Viola_Music_Voice measure 1]                                      %! _comment_measure_numbers
                                \clef "alto"                                                         %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set ViolaMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                R1 * 1/2                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Viola)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [Viola_Music_Voice measure 2]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Viola_Music_Voice measure 3]                                      %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Viola_Music_Voice measure 4]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        \tag Cello                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                        \context CelloMusicStaff = "Cello_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                            \context CelloMusicVoice = "Cello_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                                % [Cello_Music_Voice measure 1]                                      %! _comment_measure_numbers
                                \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                R1 * 1/2                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [Cello_Music_Voice measure 2]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Cello_Music_Voice measure 3]                                      %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Cello_Music_Voice measure 4]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.StringTrioScoreTemplate.__call__

    """

    ### CLASS VARIABLES ###

    _part_manifest = abjad.PartManifest(
        abjad.Part(section='Violin', section_abbreviation='VN'),
        abjad.Part(section='Viola', section_abbreviation='VA'),
        abjad.Part(section='Cello', section_abbreviation='VC'),
        )

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        """
        Calls string trio score template.
        """
        tag = 'baca.StringTrioScoreTemplate.__call__'
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # VIOLIN
        violin_music_voice = abjad.Voice(
            lilypond_type='ViolinMusicVoice',
            name='Violin_Music_Voice',
            tag=tag,
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            lilypond_type='ViolinMusicStaff',
            name='Violin_Music_Staff',
            tag=tag,
            )
        violin = abjad.Violin(
            markup=markups.instrument('Violin', hcenter_in=10),
            short_markup=markups.short_instrument(
                'Vn.',
                hcenter_in=10,
                ),
            )
        abjad.annotate(
            violin_music_staff,
            'default_instrument',
            violin,
            )
        abjad.annotate(
            violin_music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        self._attach_lilypond_tag('Violin', violin_music_staff)

        # VIOLA
        viola_music_voice = abjad.Voice(
            lilypond_type='ViolaMusicVoice',
            name='Viola_Music_Voice',
            tag=tag,
            )
        viola_music_staff = abjad.Staff(
            [viola_music_voice],
            lilypond_type='ViolaMusicStaff',
            name='Viola_Music_Staff',
            tag=tag,
            )
        abjad.annotate(
            viola_music_staff,
            'default_instrument',
            abjad.Viola(
                markup=markups.instrument('Viola', hcenter_in=10),
                short_markup=markups.short_instrument(
                    'Va.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            viola_music_staff,
            'default_clef',
            abjad.Clef('alto'),
            )
        self._attach_lilypond_tag('Viola', viola_music_staff)

        # CELLO
        cello_music_voice = abjad.Voice(
            lilypond_type='CelloMusicVoice',
            name='Cello_Music_Voice',
            tag=tag,
            )
        cello_music_staff = abjad.Staff(
            [cello_music_voice],
            lilypond_type='CelloMusicStaff',
            name='Cello_Music_Staff',
            tag=tag,
            )
        abjad.annotate(
            cello_music_staff,
            'default_instrument',
            abjad.Cello(
                markup=markups.instrument('Cello', hcenter_in=10),
                short_markup=markups.short_instrument(
                    'Vc.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            cello_music_staff,
            'default_clef',
            abjad.Clef('bass'),
            )
        self._attach_lilypond_tag('Cello', cello_music_staff)

        # SCORE
        string_section_staff_group = abjad.StaffGroup(
            [
                violin_music_staff,
                viola_music_staff,
                cello_music_staff,
                ],
            lilypond_type='StringSectionStaffGroup',
            name='String_Section_Staff_Group',
            tag=tag,
            )
        music_context = abjad.Context(
            [string_section_staff_group],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='Music_Context',
            tag=tag,
            )
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            tag=tag,
            )
        return score

class TwoVoiceStaffScoreTemplate(ScoreTemplate):
    r"""
    Two-voice staff score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice_One measure 1]                                            %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice_One measure 2]                                            %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice_One measure 3]                                            %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice_One measure 4]                                            %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice_Two measure 1]                                            %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice_Two measure 2]                                            %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice_Two measure 3]                                            %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice_Two measure 4]                                            %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    """

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        """
        Calls two-voice staff score template.
        """
        tag = 'baca.TwoVoiceStaffScoreTemplate.__call__'
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # MUSIC STAFF
        music_voice_1 = abjad.Voice(
            lilypond_type='MusicVoiceOne',
            name='Music_Voice_One',
            tag=tag,
            )
        music_voice_2 = abjad.Voice(
            lilypond_type='MusicVoiceTwo',
            name='Music_Voice_Two',
            tag=tag,
            )
        music_staff = abjad.Staff(
            [music_voice_1, music_voice_2],
            lilypond_type='MusicStaff',
            is_simultaneous=True,
            name='Music_Staff',
            tag=tag,
            )

        # MUSIC CONTEXT
        music_context = abjad.Context(
            [music_staff],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='Music_Context',
            tag=tag,
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            tag=tag,
            )
        abjad.attach(abjad.tags.TWO_VOICE, score, tag=None)
        return score

class ViolinSoloScoreTemplate(ScoreTemplate):
    r"""
    Violin solo score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.ViolinSoloScoreTemplate.__call__
            <<                                                                                       %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.ViolinSoloScoreTemplate.__call__
                <<                                                                                   %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
                    \tag Violin                                                                      %! baca.ScoreTemplate._attach_liypond_tag
                    \context ViolinMusicStaff = "Violin_Music_Staff"                                 %! baca.ViolinSoloScoreTemplate.__call__
                    {                                                                                %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
                        \context ViolinMusicVoice = "Violin_Music_Voice"                             %! baca.ViolinSoloScoreTemplate.__call__
                        {                                                                            %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
                            % [Violin_Music_Voice measure 1]                                         %! _comment_measure_numbers
                            \clef "treble"                                                           %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet)   %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override ViolinMusicStaff.Clef.color = ##f                              %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set ViolinMusicStaff.forceClef = ##t                                    %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                            R1 * 1/2                                                                 %! _call_rhythm_commands
                            ^ \baca-default-indicator-markup "(Violin)"                              %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)             %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                            % [Violin_Music_Voice measure 2]                                         %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Violin_Music_Voice measure 3]                                         %! _comment_measure_numbers
                            R1 * 1/2                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Violin_Music_Voice measure 4]                                         %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                        }                                                                            %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.ViolinSoloScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.ViolinSoloScoreTemplate.__call__

    """

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        """
        Calls violin solo score template.
        """
        tag = 'baca.ViolinSoloScoreTemplate.__call__'
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # VIOLIN
        violin_music_voice = abjad.Voice(
            lilypond_type='ViolinMusicVoice',
            name='Violin_Music_Voice',
            tag=tag,
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            lilypond_type='ViolinMusicStaff',
            name='Violin_Music_Staff',
            tag=tag,
            )
        violin = abjad.Violin(
            markup=markups.instrument('Violin'),
            short_markup=markups.short_instrument('Vn.'),
            )
        abjad.annotate(
            violin_music_staff,
            'default_instrument',
            violin,
            )
        abjad.annotate(
            violin_music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        self._attach_lilypond_tag('Violin', violin_music_staff)

        # MUSIC ONTEXT
        music_context = abjad.Context(
            [violin_music_staff],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='Music_Context',
            tag=tag,
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            tag=tag,
            )
        return score
