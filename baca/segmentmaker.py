import abjad
import copy
import os
import pathlib
import sys
import traceback
import typing
from abjadext import rmakers
from . import classes
from . import commands as baca_commands
from . import indicators
from . import markups
from . import overrides as baca_overrides
from . import pitchclasses
from . import rhythmcommands
from . import scoping
from . import segmentclasses
from . import templates
from . import typings


class SegmentMaker(abjad.SegmentMaker):
    r"""
    Segment-maker.

    >>> from abjadext import rmakers

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'8
                            [
            <BLANKLINE>
                            c'8
            <BLANKLINE>
                            c'8
            <BLANKLINE>
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'8
                            [
            <BLANKLINE>
                            c'8
            <BLANKLINE>
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'8
                            [
            <BLANKLINE>
                            c'8
            <BLANKLINE>
                            c'8
            <BLANKLINE>
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'8
                            [
            <BLANKLINE>
                            c'8
            <BLANKLINE>
                            c'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    
    __documentation_section__ = 'Classes'

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_allow_empty_selections',
        '_breaks',
        '_cache',
        '_cached_time_signatures',
        '_clock_time_override',
        '_color_octaves',
        '_color_out_of_range_pitches',
        '_color_repeat_pitch_classes',
        '_do_not_check_persistence',
        '_do_not_include_layout_ly',
        '_duration',
        '_environment',
        '_fermata_measure_numbers',
        '_fermata_measure_staff_line_count',
        '_fermata_start_offsets',
        '_fermata_stop_offsets',
        '_final_bar_line',
        '_final_markup',
        '_final_markup_extra_offset',
        '_first_measure_number',
        '_first_segment',
        '_ignore_out_of_range_pitches',
        '_ignore_repeat_pitch_classes',
        '_ignore_unpitched_notes',
        '_ignore_unregistered_pitches',
        '_instruments',
        '_last_measure_is_fermata',
        '_last_segment',
        '_magnify_staves',
        '_margin_markups',
        '_metronome_marks',
        '_midi',
        '_nonfirst_segment_lilypond_include',
        '_offset_to_measure_number',
        '_previously_alive_contexts',
        '_score',
        '_score_template',
        '_segment_bol_measure_numbers',
        '_segment_directory',
        '_segment_duration',
        '_skip_wellformedness_checks',
        '_skips_instead_of_rests',
        '_sounds_during_segment',
        '_spacing',
        '_start_clock_time',
        '_stop_clock_time',
        '_test_container_identifiers',
        '_time_signatures',
        '_transpose_score',
        '_validate_measure_count',
        '_voice_metadata',
        '_voice_names',
        '_commands',
        )

    _absolute_string_trio_stylesheet_path = pathlib.Path(
        '/',
        'Users',
        'trevorbaca',
        'Scores',
        '_docs',
        'source',
        '_stylesheets',
        'string-trio.ily',
        )

    _absolute_two_voice_staff_stylesheet_path = pathlib.Path(
        '/',
        'Users',
        'trevorbaca',
        'Scores',
        '_docs',
        'source',
        '_stylesheets',
        'two-voice-staff.ily',
        )

    _prototype_to_manifest_name = {
        'abjad.Instrument': 'instruments',
        'abjad.MetronomeMark': 'metronome_marks',
        'abjad.MarginMarkup': 'margin_markups',
        }

    _publish_storage_format = True

    _status_to_color = {
        'default': 'DarkViolet',
        'explicit': 'blue',
        'reapplied': 'green4',
        'redundant': 'DeepPink1',
        }

    _status_to_redraw_color = {
        'default': 'violet',
        'explicit': 'DeepSkyBlue2',
        'reapplied': 'OliveDrab',
        'redundant': 'DeepPink4',
        }

    _score_package_stylesheet_path = pathlib.Path(
        '..', '..', 'stylesheets', 'stylesheet.ily',
        )

    _score_package_nonfirst_segment_path = pathlib.Path(
        '..', '..', 'stylesheets', 'nonfirst-segment.ily',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allow_empty_selections: bool = None,
        breaks: segmentclasses.BreakMeasureMap = None,
        clock_time_override: abjad.MetronomeMark = None,
        color_octaves: bool = None,
        color_out_of_range_pitches: bool = True,
        color_repeat_pitch_classes: bool = True,
        do_not_check_persistence: bool = None,
        do_not_include_layout_ly: bool = None,
        fermata_measure_staff_line_count: int = None,
        final_bar_line: typing.Union[bool, str] = None,
        final_markup: tuple = None,
        final_markup_extra_offset: typings.NumberPair = None,
        first_measure_number: int = None,
        first_segment: bool = None,
        ignore_out_of_range_pitches: bool = None,
        ignore_repeat_pitch_classes: bool = None,
        ignore_unpitched_notes: bool = None,
        ignore_unregistered_pitches: bool = None,
        nonfirst_segment_lilypond_include: bool = None,
        instruments: abjad.OrderedDict = None,
        last_segment: bool = None,
        magnify_staves: typing.Union[
            abjad.Multiplier,
            typing.Tuple[abjad.Multiplier, abjad.Tag],
            ] = None,
        margin_markups: abjad.OrderedDict = None,
        metronome_marks: abjad.OrderedDict = None,
        score_template: templates.ScoreTemplate = None,
        segment_directory: abjad.Path = None,
        spacing: segmentclasses.HorizontalSpacingSpecifier = None,
        skip_wellformedness_checks: bool = None,
        skips_instead_of_rests: bool = None,
        test_container_identifiers: bool = None,
        time_signatures: typing.List[tuple] = None,
        transpose_score: bool = None,
        validate_measure_count: int = None,
        ) -> None:
        super().__init__()
        self._allow_empty_selections = allow_empty_selections
        self._breaks = breaks
        if clock_time_override is not None:
            assert isinstance(clock_time_override, abjad.MetronomeMark)
        self._clock_time_override = clock_time_override
        self._color_octaves = color_octaves
        self._color_out_of_range_pitches = color_out_of_range_pitches
        self._color_repeat_pitch_classes = color_repeat_pitch_classes
        self._cache = None
        self._cached_time_signatures: typing.List[abjad.TimeSignature] = []
        self._do_not_check_persistence = do_not_check_persistence
        self._do_not_include_layout_ly = do_not_include_layout_ly
        self._duration: typing.Optional[abjad.Duration] = None
        self._fermata_measure_numbers: typing.List = []
        self._fermata_measure_staff_line_count = \
            fermata_measure_staff_line_count
        self._fermata_start_offsets: typing.List[abjad.Offset] = []
        self._fermata_stop_offsets: typing.List[abjad.Offset] = []
        if final_bar_line is not None:
            assert isinstance(final_bar_line, (bool, str))
        self._final_bar_line = final_bar_line
        self._final_markup = final_markup
        self._final_markup_extra_offset = final_markup_extra_offset
        self._first_measure_number = first_measure_number
        if first_segment is not None:
            first_segment = bool(first_segment)
        self._first_segment = first_segment
        if ignore_out_of_range_pitches is not None:
            ignore_out_of_range_pitches = bool(ignore_out_of_range_pitches)
        self._ignore_out_of_range_pitches = ignore_out_of_range_pitches
        self._ignore_repeat_pitch_classes = ignore_repeat_pitch_classes
        self._ignore_unpitched_notes = ignore_unpitched_notes
        self._ignore_unregistered_pitches = ignore_unregistered_pitches
        self._nonfirst_segment_lilypond_include = \
            nonfirst_segment_lilypond_include
        self._instruments = instruments
        self._last_measure_is_fermata = False
        self._last_segment = last_segment
        self._magnify_staves = magnify_staves
        self._margin_markups = margin_markups
        self._metronome_marks = metronome_marks
        self._midi: typing.Optional[bool] = None
        self._offset_to_measure_number: typing.Dict[abjad.Offset, int] = {}
        self._previously_alive_contexts: typing.List[str] = []
        self._score_template = score_template
        self._segment_bol_measure_numbers: typing.List[int] = []
        if segment_directory is not None:
            segment_directory = abjad.Path(
                segment_directory,
                scores=segment_directory.parent.parent.parent.parent,
                )
        self._segment_directory: typing.Optional[abjad.Path] = segment_directory
        self._segment_duration: typing.Optional[abjad.Duration] = None
        self._skip_wellformedness_checks = skip_wellformedness_checks
        self._skips_instead_of_rests = skips_instead_of_rests
        self._spacing = spacing
        self._sounds_during_segment: abjad.OrderedDict = abjad.OrderedDict()
        self._start_clock_time: typing.Optional[str] = None
        self._stop_clock_time: typing.Optional[str] = None
        if test_container_identifiers is not None:
            test_container_identifiers = bool(test_container_identifiers)
        self._test_container_identifiers = test_container_identifiers
        self._transpose_score = transpose_score
        self._validate_measure_count = validate_measure_count
        self._voice_metadata: abjad.OrderedDict = abjad.OrderedDict()
        self._voice_names: typing.Optional[typing.Tuple[str, ...]] = None
        self._commands: typing.List[scoping.Command] = []
        self._import_manifests()
        self._initialize_time_signatures(time_signatures)
        self._validate_measure_count_()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        scopes: typing.Union[scoping.Scope, scoping.TimelineScope],
        *commands: typing.Union[scoping.Command, scoping.Suite],
        ) -> None:
        r"""
        Wraps each command in ``commands`` with each scope in ``scopes``.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     baca.label(abjad.label().with_indices()),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 0 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 1 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 2 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 3 }
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 4 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 5 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 6 }
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 7 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 8 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 9 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 10 }
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 11 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 12 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 13 }
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Commands may be grouped into lists:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> commands = []
            >>> commands.append(baca.make_even_divisions())
            >>> commands.append(baca.label(abjad.label().with_indices()))

            >>> maker(
            ...     'MusicVoice',
            ...     commands,
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 0 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 1 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 2 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 3 }
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 4 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 5 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 6 }
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 7 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 8 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 9 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 10 }
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 11 }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 12 }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ^ \markup { 13 }
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on noncommand input:

            >>> maker(
            ...     'MusicVoice',
            ...     'text',
            ...     )
            Traceback (most recent call last):
                ...
            Exception: 
            <BLANKLINE>
            Must be command:
            <BLANKLINE>
            text

        ..  container:: example

            Raises exception on unknown voice name:

            >>> maker(
            ...     'PercussionVoice',
            ...     baca.make_repeated_duration_notes([(1, 4)]),
            ...     )
            Traceback (most recent call last):
                ...
            Exception: unknown voice name 'PercussionVoice'.

        """
        commands_ = classes.Sequence(commands).flatten(
            classes=(list, scoping.Suite),
            depth=-1,
            )
        commands = tuple(commands_)
        if self.score_template is not None:
            self._cache_voice_names()
            abbreviations = self.score_template.voice_abbreviations
        else:
            abbreviations = abjad.OrderedDict()
        abbreviations = abbreviations or abjad.OrderedDict()
        scopes_ = self._unpack_scopes(scopes, abbreviations)
        scope_type = (scoping.Scope, scoping.TimelineScope)
        assert all(isinstance(_, scope_type) for _ in scopes_), repr(scopes_)
        for command in commands:
            if isinstance(command, list):
                raise Exception('use baca.suite().')
            if not isinstance(command, scoping.Command):
                message = '\n\nMust be command:'
                message += f'\n\n{format(command)}'
                raise Exception(message)
        scope_count = len(scopes_)
        for i, current_scope in enumerate(scopes_):
            if (self._voice_names and
                current_scope.voice_name not in self._voice_names):
                message = f'unknown voice name {current_scope.voice_name!r}.'
                raise Exception(message)
            if isinstance(current_scope, scoping.TimelineScope):
                for scope_ in current_scope.scopes:
                    if scope_.voice_name in abbreviations:
                        voice_name = abbreviations[scope_.voice_name]
                        scope_._voice_name = voice_name
            for command in commands:
                assert isinstance(command, scoping.Command), repr(command)
                if not command._matches_scope_index(scope_count, i):
                    continue
                if isinstance(command, scoping.Command):
                    commands_ = [command]
                else:
                    commands_ = command
                for command_ in commands_:
                    assert isinstance(command_, scoping.Command), repr(command_)
                    scope_ = command_._override_scope(current_scope)
                    scope_ = copy.copy(scope_)
                    command_ = copy.copy(command_)
                    command_.scope = scope_
                    self.commands.append(command_)

    ### PRIVATE METHODS ###

    def _add_final_bar_line(self):
        if self.final_bar_line is False:
            return
        strings = []
        abbreviation = '|'
        if self.last_segment:
            abbreviation = '|.'
        if isinstance(self.final_bar_line, str):
            abbreviation = self.final_bar_line
        strings.append(r'\baca_bar_line_visible')
        strings.append(rf'\bar "{abbreviation}"')
        literal = abjad.LilyPondLiteral(strings, 'after')
        last_skip = classes.Selection(self.score['GlobalSkips']).skip(-1)
        abjad.attach(literal, last_skip, tag='SM5')

    def _add_final_markup(self):
        if self.final_markup is None:
            return
        command = baca_commands.markup(
            markups.final_markup(*self.final_markup),
            selector='baca.leaf(-1)',
            direction=abjad.Down,
            )
        self.score.add_final_markup(
            command.indicators[0],
            extra_offset=self.final_markup_extra_offset,
            )

    def _alive_during_any_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        assert self.previous_metadata is not None
        names: typing.List = self.previous_metadata.get(
            'alive_during_segment',
            [],
            )
        return context.name in names

    def _alive_during_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        assert self.previous_metadata is not None
        names: typing.List = self.previous_metadata.get(
            'alive_during_segment',
            [],
            )
        return context.name in names

    def _analyze_momento(self, context, momento):
        previous_indicator = self._momento_to_indicator(momento)
        if previous_indicator is None:
            return
        if isinstance(previous_indicator, indicators.SpacingSection):
            return
        if momento.context in self.score:
            momento_context = self.score[momento.context]
        else:
            # context alive in previous segment doesn't exist in this segment
            return
        leaf = abjad.inspect(momento_context).get_leaf(0)
        if isinstance(previous_indicator, abjad.Instrument):
            prototype = abjad.Instrument
        else:
            prototype = type(previous_indicator)
        indicator = abjad.inspect(leaf).get_indicator(prototype)
        status = None
        if indicator is None:
            status = 'reapplied'
        elif previous_indicator == indicator:
            if isinstance(previous_indicator, abjad.TimeSignature):
                status = 'reapplied'
            elif isinstance(previous_indicator, abjad.Dynamic):
                if previous_indicator.sforzando:
                    status = 'explicit'
                else:
                    status = 'redundant'
            else:
                status = 'redundant'
        edition = momento.edition or abjad.Tag()
        return leaf, previous_indicator, status, edition

    def _annotate_sounds_during(self):
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            pleaves = classes.Selection(voice).pleaves()
            value = bool(pleaves)
            abjad.annotate(voice, abjad.tags.SOUNDS_DURING_SEGMENT, value)
            self._sounds_during_segment[voice.name] = value

    def _apply_breaks(self):
        if self.breaks is None:
            return
        self.breaks(self.score['GlobalSkips'])
        if self.breaks.local_measure_numbers:
            abjad.setting(self.score).current_bar_number = 1

    def _apply_first_and_last_ties(self, voice):
        dummy_tie = abjad.Tie()
        for current_leaf in abjad.iterate(voice).leaves():
            inspection = abjad.inspect(current_leaf)
            if inspection.has_indicator(abjad.tags.LEFT_BROKEN_REPEAT_TIE_TO):
                rhythmcommands.TieCorrectionCommand._add_tie(
                    current_leaf,
                    direction=abjad.Left,
                    repeat=True,
                    )
                continue
            elif inspection.has_indicator(abjad.tags.RIGHT_BROKEN_TIE_FROM):
                rhythmcommands.TieCorrectionCommand._add_tie(
                    current_leaf,
                    direction=abjad.Right,
                    repeat=False,
                    )
                continue
            if not dummy_tie._attachment_test(current_leaf):
                continue
            if abjad.inspect(current_leaf).has_indicator(abjad.tags.TIE_TO):
                previous_leaf = abjad.inspect(current_leaf).get_leaf(-1)
                if dummy_tie._attachment_test(previous_leaf):
                    previous_logical_tie = abjad.inspect(
                        previous_leaf).get_logical_tie()
                    if current_leaf not in previous_logical_tie:
                        current_logical_tie = abjad.inspect(
                            current_leaf).get_logical_tie()
                        leaves = previous_logical_tie + current_logical_tie
                        abjad.detach(abjad.Tie, previous_leaf)
                        abjad.detach(abjad.Tie, current_leaf)
                        inspector = abjad.inspect(current_leaf)
                        string = abjad.tags.REPEAT_TIE 
                        repeat_ties = inspector.has_indicator(string)
                        tie = abjad.Tie(repeat=repeat_ties)
                        abjad.attach(tie, leaves, tag='SM16')
                abjad.detach(abjad.tags.TIE_TO, current_leaf)
            if abjad.inspect(current_leaf).has_indicator(abjad.tags.TIE_FROM):
                next_leaf = abjad.inspect(current_leaf).get_leaf(1)
                if dummy_tie._attachment_test(next_leaf):
                    current_logical_tie = abjad.inspect(
                        current_leaf).get_logical_tie()
                    if next_leaf not in current_logical_tie:
                        next_logical_tie = abjad.inspect(
                            next_leaf).get_logical_tie()
                        leaves = current_logical_tie + next_logical_tie
                        abjad.detach(abjad.Tie, current_leaf)
                        abjad.detach(abjad.Tie, next_leaf)
                        inspector = abjad.inspect(current_leaf)
                        string = abjad.tags.REPEAT_TIE
                        repeat_ties = inspector.has_indicator(string)
                        tie = abjad.Tie(repeat=repeat_ties)
                        abjad.attach(tie, leaves, tag='SM17')
                abjad.detach(abjad.tags.TIE_FROM, current_leaf)

    def _apply_spacing(self):
        if self.spacing is None:
            return
        with abjad.Timer() as timer:
            self.spacing(self)
        if os.getenv('TRAVIS'):
            return
        if 3 < timer.elapsed_time:
            count = int(timer.elapsed_time)
            raise Exception(f'spacing application {count} {seconds}!')

    def _assert_nonoverlapping_rhythms(self, rhythms, voice):
        previous_stop_offset = 0
        for rhythm in rhythms:
            start_offset = rhythm.start_offset
            if start_offset < previous_stop_offset:
                raise Exception(f'{voice} has overlapping rhythms.')
            duration = abjad.inspect(rhythm.annotation).get_duration()
            stop_offset = start_offset + duration
            previous_stop_offset = stop_offset

    @staticmethod
    def _attach_color_cancelation_literal(
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        ):
        if getattr(wrapper.indicator, 'latent', False):
            return
        if getattr(wrapper.indicator, 'hide', False):
            return
        if not getattr(wrapper.indicator, 'redraw', False):
            return
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            cancelation=True,
            )

    @staticmethod
    def _attach_color_literal(
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        redraw=False,
        cancelation=False,
        ):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        if getattr(wrapper.indicator, 'hide', False) is True:
            return
        if isinstance(wrapper.indicator, abjad.Instrument):
            return
        if not getattr(wrapper.indicator, 'persistent', False):
            return
        if wrapper.indicator.persistent == 'abjad.MetronomeMark':
            return
        if isinstance(wrapper.indicator, abjad.PersistentOverride):
            return
        if existing_tag is not None:
            assert isinstance(existing_tag, abjad.Tag), repr(existing_tag)
        stem = abjad.String.to_indicator_stem(wrapper.indicator)
        grob = SegmentMaker._indicator_to_grob(wrapper.indicator)
        context = wrapper._find_correct_effective_context()
        assert isinstance(context, abjad.Context), repr(context)
        string = rf'\override {context.lilypond_type}.{grob}.color ='
        if cancelation is True:
            string += ' ##f'
        elif redraw is True:
            color = SegmentMaker._status_to_redraw_color[status]
            string += f" #(x11-color '{color})"
        else:
            string = rf'\once {string}'
            color = SegmentMaker._status_to_color[status]
            string += f" #(x11-color '{color})"
        if redraw:
            literal = abjad.LilyPondLiteral(string, 'after')
        else:
            literal = abjad.LilyPondLiteral(string)
        if getattr(wrapper.indicator, 'latent', False):
            if redraw:
                prefix = 'redrawn'
            else:
                prefix = None
            if cancelation:
                suffix = 'color_cancellation'
            else:
                suffix = 'color'
        else:
            prefix = None
            if redraw:
                suffix = 'redraw_color'
            elif cancelation:
                suffix = 'color_cancellation'
            else:
                suffix = 'color'
        tag = SegmentMaker._get_tag(status, stem, prefix=prefix, suffix=suffix)
        if existing_tag:
            tag = existing_tag.prepend(tag)
        if isinstance(wrapper.indicator, abjad.TimeSignature):
            string = rf'\baca_time_signature_color "{color}"'
            literal = abjad.LilyPondLiteral(string)
        if cancelation is True:
            abjad.attach(
                literal,
                wrapper.component,
                deactivate=True,
                tag=tag.prepend('SM7'),
                )
        else:
            abjad.attach(
                literal,
                wrapper.component,
                deactivate=existing_deactivate,
                tag=tag.prepend('SM6'),
                )

    @staticmethod
    def _attach_color_redraw_literal(
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        ):
        if not getattr(wrapper.indicator, 'redraw', False):
            return
        if getattr(wrapper.indicator, 'hide', False):
            return
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            redraw=True,
            )

    def _attach_fermatas(self):
        always_make_global_rests = self.score_template.always_make_global_rests
        if not always_make_global_rests:
            del(self.score['GlobalRests'])
            return
        has_fermata = False
        if not has_fermata and not always_make_global_rests:
            del(self.score['GlobalRests'])
            return
        context = self.score['GlobalRests']
        rests = self._make_multimeasure_rests()
        context.extend(rests)

    def _attach_first_appearance_score_template_defaults(self):
        if self.first_segment:
            return
        staff__group = (abjad.Staff, abjad.StaffGroup)
        dictionary = self.previous_metadata['persistent_indicators']
        for staff__group in abjad.iterate(self.score).components(staff__group):
            if staff__group.name in dictionary:
                continue
            for wrapper in self.score_template.attach_defaults(staff__group):
                self._treat_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    'default',
                    )

    def _attach_first_segment_score_template_defaults(self):
        if not self.first_segment:
            return
        for wrapper in self.score_template.attach_defaults(self.score):
            self._treat_persistent_wrapper(
                self.manifests,
                wrapper,
                'default',
                )

    @staticmethod
    def _attach_latent_indicator_alert(
        manifests,
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        ):
        if not getattr(wrapper.indicator, 'latent', False):
            return
        if existing_tag is not None:
            assert isinstance(existing_tag, abjad.Tag), repr(existing_tag)
        leaf = wrapper.component
        indicator = wrapper.indicator
        assert indicator.latent, repr(indicator)
        if isinstance(indicator, abjad.Clef):
            return
        key = SegmentMaker._indicator_to_key(indicator, manifests)
        if key is not None:
            key = f'“{key}”'
        else:
            key = type(indicator).__name__
        if isinstance(indicator, abjad.Instrument):
            if status == 'default':
                tag = abjad.tags.DEFAULT_INSTRUMENT_ALERT
            elif status == 'explicit':
                tag = abjad.tags.EXPLICIT_INSTRUMENT_ALERT
            elif status == 'reapplied':
                tag = abjad.tags.REAPPLIED_INSTRUMENT_ALERT
            else:
                assert status == 'redundant', repr(status)
                tag = abjad.tags.REDUNDANT_INSTRUMENT_ALERT
            left, right = '(', ')'
        else:
            assert isinstance(indicator, abjad.MarginMarkup)
            if status == 'default':
                tag = abjad.tags.DEFAULT_MARGIN_MARKUP_ALERT
            elif status == 'explicit':
                tag = abjad.tags.EXPLICIT_MARGIN_MARKUP_ALERT
            elif status == 'reapplied':
                tag = abjad.tags.REAPPLIED_MARGIN_MARKUP_ALERT
            else:
                assert status == 'redundant', repr(status)
                tag = abjad.tags.REDUNDANT_MARGIN_MARKUP_ALERT
            left, right = '[', ']'
        tag = abjad.Tag(tag)
        markup = abjad.Markup.from_literal(f'{left}{key}{right}')
        markup = abjad.new(markup, direction=abjad.Up)
        color = SegmentMaker._status_to_color[status]
        color = abjad.SchemeColor(color)
        markup = markup.with_color(color)
        if existing_tag:
            tag = existing_tag.prepend(tag)
        abjad.attach(
            markup,
            leaf,
            deactivate=existing_deactivate,
            tag=tag.prepend('SM11'),
            )

    def _attach_metronome_mark_text_span_indicators(self):
        indicator_count = 0
        skips = classes.Selection(self.score['GlobalSkips']).skips()
        last_leaf_metronome_mark = abjad.inspect(skips[-1]).get_indicator(
            abjad.MetronomeMark,
            default=None,
            )
        add_right_text_to_me = None
        if last_leaf_metronome_mark:
            tempo_prototype = (
                abjad.MetronomeMark,
                indicators.Accelerando,
                indicators.Ritardando,
                )
            for skip in reversed(skips[:-1]):
                if abjad.inspect(skip).has_indicator(tempo_prototype):
                    add_right_text_to_me = skip
                    break
        for skip in skips:
            inspector = abjad.inspect(skip)
            metronome_mark = inspector.get_indicator(
                abjad.MetronomeMark,
                default=None,
                )
            metric_modulation = inspector.get_indicator(
                abjad.MetricModulation,
                default=None,
                )
            accelerando = inspector.get_indicator(
                indicators.Accelerando,
                default=None,
                )
            ritardando = inspector.get_indicator(
                indicators.Ritardando,
                default=None,
                )
            if metronome_mark is not None:
                metronome_mark._hide = True
                wrapper = inspector.wrapper(abjad.MetronomeMark)
            if metric_modulation is not None:
                metric_modulation._hide = True
            if accelerando is not None:
                accelerando._hide = True
            if ritardando is not None:
                ritardando._hide = True
            if skip is skips[-1]:
                break
            if metronome_mark is None and metric_modulation is not None:
                wrapper = inspector.wrapper(abjad.MetricModulation)
            if metronome_mark is None and accelerando is not None:
                wrapper = inspector.wrapper(indicators.Accelerando)
            if metronome_mark is None and ritardando is not None:
                wrapper = inspector.wrapper(indicators.Ritardando)
            has_trend = accelerando is not None or ritardando is not None
            if (metronome_mark is None and
                metric_modulation is None and
                not has_trend):
                continue
            indicator_count += 1
            tag = wrapper.tag
            if metronome_mark is not None:
                left_text = metronome_mark._get_markup()
                if metric_modulation is not None:
                    markups = []
                    markups.append(left_text)
                    markups.append(abjad.Markup.hspace(2))
                    markups.append(abjad.Markup('[').upright())
                    modulation = metric_modulation._get_markup()
                    modulation = abjad.Markup.line([modulation])
                    markups.append(modulation)
                    markups.append(abjad.Markup.hspace(0.5))
                    markups.append(abjad.Markup(']').upright())
                    left_text = abjad.Markup.concat(markups)
            elif accelerando is not None:
                left_text = accelerando._get_markup()
            elif ritardando is not None:
                left_text = ritardando._get_markup()
            if has_trend:
                style = 'dashed_line_with_arrow'
            else:
                style = 'invisible_line'
            stop_text_span = abjad.StopTextSpan()
            abjad.attach(
                stop_text_span,
                skip,
                tag='MMI1',
                )
            if add_right_text_to_me is skip:
                right_text = last_leaf_metronome_mark._get_markup()
            else:
                right_text = None
            start_text_span = abjad.StartTextSpan(
                left_text=left_text,
                right_text=right_text,
                style=style,
                )
            abjad.attach(
                start_text_span,
                skip,
                deactivate=True,
                tag='MMI2',
                )
            string = str(tag)
            if 'DEFAULT' in string:
                status = 'default'
            elif 'EXPLICIT' in string:
                status = 'explicit'
            elif 'REAPPLIED' in str(tag):
                status = 'reapplied'
            elif 'REDUNDANT' in str(tag):
                status = 'redundant'
            else:
                status = None
            assert status is not None
            color = self._status_to_color[status]
            tag = f'{status.upper()}_METRONOME_MARK_WITH_COLOR'
            tag = abjad.Tag(tag)
            color = abjad.SchemeColor(color)
            left_text_with_color = left_text.with_color(color)

            if right_text:
                wrapper = abjad.inspect(skips[-1]).wrapper(abjad.MetronomeMark)
                tag = wrapper.tag
                string = str(tag)
                if 'DEFAULT' in string:
                    status = 'default'
                elif 'EXPLICIT' in string:
                    status = 'explicit'
                elif 'REAPPLIED' in str(tag):
                    status = 'reapplied'
                elif 'REDUNDANT' in str(tag):
                    status = 'redundant'
                else:
                    status = None
                assert status is not None
                color = self._status_to_color[status]
                color = abjad.SchemeColor(color)
                right_text_with_color = right_text.with_color(color)
            else:
                right_text_with_color = None
            start_text_span = abjad.StartTextSpan(
                left_text=left_text_with_color,
                right_text=right_text_with_color,
                style=style,
                )
            abjad.attach(
                start_text_span,
                skip,
                deactivate=False,
                tag='MMI3',
                )
        if indicator_count:
            last_skip = skip
            stop_text_span = abjad.StopTextSpan()
            abjad.attach(
                stop_text_span,
                last_skip,
                tag='MMI4',
                )

    def _born_this_segment(self, component):
        prototype = (abjad.Staff, abjad.StaffGroup)
        assert isinstance(component, prototype), repr(component)
        return not self._alive_during_previous_segment(component)

    def _bundle_manifests(self, voice_name=None):
        manifests = abjad.OrderedDict()
        previous_segment_voice_metadata = \
            self._get_previous_segment_voice_metadata(voice_name)
        manifests['manifests'] = self.manifests
        manifests['offset_to_measure_number'] = self._offset_to_measure_number
        manifests['previous_segment_voice_metadata'
            ] = previous_segment_voice_metadata
        manifests['score_template'] = self.score_template
        return manifests

    def _cache_fermata_measure_numbers(self):
        if 'GlobalRests' not in self.score:
            return
        context = self.score['GlobalRests']
        mm_rests = abjad.select(context).leaves(abjad.MultimeasureRest)
        last_measure_index = len(mm_rests) - 1
        first_measure_number = self._get_first_measure_number()
        tag = abjad.tags.FERMATA_MEASURE
        for measure_index, mm_rest in enumerate(mm_rests):
            if not abjad.inspect(mm_rest).has_indicator(tag):
                continue
            if measure_index == last_measure_index:
                self._last_measure_is_fermata = True
            measure_number = first_measure_number + measure_index
            timespan = abjad.inspect(mm_rest).get_timespan()
            self._fermata_start_offsets.append(timespan.start_offset)
            self._fermata_stop_offsets.append(timespan.stop_offset)
            self._fermata_measure_numbers.append(measure_number)

    def _cache_leaves(self):
        measure_timespans = []
        for measure_index in range(self.measure_count):
            measure_number = measure_index + 1
            measure_timespan = self._get_measure_timespan(measure_number)
            measure_timespans.append(measure_timespan)
        self._cache = abjad.OrderedDict()
        contexts = [self.score['GlobalSkips']]
        if 'GlobalRests' in self.score:
            contexts.append(self.score['GlobalRests'])
        contexts.extend(abjad.select(self.score).components(abjad.Voice))
        for context in contexts:
            leaves_by_measure_number = abjad.OrderedDict()
            self._cache[context.name] = leaves_by_measure_number
            for measure_index in range(self.measure_count):
                measure_number = measure_index + 1
                leaves_by_measure_number[measure_number] = []
            for leaf in abjad.iterate(context).leaves():
                leaf_timespan = abjad.inspect(leaf).get_timespan()
                for i, measure_timespan in enumerate(measure_timespans):
                    measure_number = i + 1
                    if leaf_timespan.starts_during_timespan(measure_timespan):
                        leaves_by_measure_number[measure_number].append(leaf)

    def _cache_previously_alive_contexts(self) -> None:
        if self.segment_directory is None:
            return
        contexts: typing.Set[str] = set()
        string = 'alive_during_segment'
        for segment in self.segment_directory.parent.list_paths():
            if segment == self.segment_directory:
                break
            contexts_ = segment.get_metadatum(string)
            contexts.update(contexts_)
        self._previously_alive_contexts.extend(sorted(contexts))

    def _cache_voice_names(self):
        if self._voice_names is not None:
            return
        if self.score_template is None:
            return
        voice_names = ['GlobalSkips', 'GlobalRests', 'TimelineScope']
        score = self.score_template()
        for voice in abjad.iterate(score).components(abjad.Voice):
            if voice.name is not None:
                voice_names.append(voice.name)
        voice_names_ = tuple(voice_names)
        self._voice_names = voice_names_

    def _call_commands(self):
        command_count = 0
        for command in self.commands:
            assert isinstance(command, scoping.Command)
            if isinstance(command, rhythmcommands.RhythmCommand):
                continue
            command_count += 1
            selection = self._scope_to_leaf_selection(command)
            voice_name = command.scope.voice_name
            command.runtime = self._bundle_manifests(voice_name)
            try:
                command(selection)
            except:
                print(f'Interpreting ...\n\n{format(command)}\n')
                raise
            self._handle_mutator(command)
            if getattr(command, 'persist', None):
                parameter = command.parameter
                state = command.state
                assert 'name' not in state
                state['name'] = command.persist
                if voice_name not in self.voice_metadata:
                    self.voice_metadata[voice_name] = abjad.OrderedDict()
                self.voice_metadata[voice_name][parameter] = state
        return command_count

    def _call_rhythm_commands(self):
        self._attach_fermatas()
        command_count = 0
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            assert not len(voice), repr(voice)
            voice_metadata = self._voice_metadata.get(
                voice.name,
                abjad.OrderedDict(),
                )
            commands = self._voice_to_rhythm_commands(voice)
            if not commands:
                if self.skips_instead_of_rests:
                    maker = rhythmcommands.SkipRhythmMaker()
                else:
                    mask = rmakers.silence(
                        [0],
                        1,
                        use_multimeasure_rests=True,
                        )
                    maker = rmakers.NoteRhythmMaker(division_masks=[mask])
                selections = maker(self.time_signatures)
                voice.extend(selections)
                continue
            rhythms = []
            for command in commands:
                if command.scope.measures is None:
                    raise Exception(format(command))
                measures = command.scope.measures
                result = self._get_measure_time_signatures(*measures)
                start_offset, time_signatures = result
                command.runtime = self._bundle_manifests(voice.name)
                try:
                    command(start_offset, time_signatures)
                except:
                    print(f'Interpreting ...\n\n{format(command)}\n')
                    raise
                rhythm = command.payload
                rhythms.append(rhythm)
                if command.persist and command.state:
                    state = command.state
                    assert 'name' not in state
                    state['name'] = command.persist
                    voice_metadata[command.parameter] = command.state
                command_count += 1
            if bool(voice_metadata):
                self._voice_metadata[voice.name] = voice_metadata
            rhythms.sort()
            self._assert_nonoverlapping_rhythms(rhythms, voice.name)
            rhythms = self._intercalate_silences(rhythms)
            voice.extend(rhythms)
            self._apply_first_and_last_ties(voice)
        return command_count

    def _check_all_music_in_part_containers(self):
        name = 'all_music_in_part_containers'
        if getattr(self.score_template, name, None) is not True:
            return
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for component in voice:
                if isinstance(component, (abjad.MultimeasureRest, abjad.Skip)):
                    continue
                if (type(component) is abjad.Container and
                    component.identifier and
                    component.identifier.startswith('%*% ')):
                    continue
                message = f'{voice.name} contains {component!r}'
                message += ' outside part container.'
                raise Exception(message)

    def _check_persistent_indicators(self):
        if self.do_not_check_persistence:
            return
        if self.environment == 'docs':
            return
        tag = abjad.tags.SOUNDS_DURING_SEGMENT
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            if not abjad.inspect(voice).get_annotation(tag):
                continue
            for i, leaf in enumerate(abjad.iterate(voice).leaves()):
                self._check_persistent_indicators_for_leaf(voice.name, leaf, i)

    def _check_persistent_indicators_for_leaf(self, voice, leaf, i):
        prototype = (
            indicators.Accelerando,
            abjad.MetronomeMark,
            indicators.Ritardando,
            )
        mark = abjad.inspect(leaf).get_effective(prototype)
        if mark is None:
            message = f'{voice} leaf {i} ({leaf!s}) missing metronome mark.'
            raise Exception(message)
        instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
        if instrument is None:
            message = f'{voice} leaf {i} ({leaf!s}) missing instrument.'
            raise Exception(message)
        if not self.score_template.do_not_require_margin_markup:
            markup = abjad.inspect(leaf).get_effective(abjad.MarginMarkup)
            if markup is None:
                message = f'{voice} leaf {i} ({leaf!s}) missing margin markup.'
                raise Exception(message)
        clef = abjad.inspect(leaf).get_effective(abjad.Clef)
        if clef is None:
            message = f'{voice} leaf {i} ({leaf!s}) missing clef.'
            raise Exception(message)

    def _check_range(self):
        markup = abjad.Markup('*', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for pleaf in abjad.iterate(voice).leaves(pitched=True):
                instrument = abjad.inspect(pleaf).get_effective(
                    abjad.Instrument
                    )
                if instrument is None:
                    continue
                if pleaf not in instrument.pitch_range:
                    if not self.ignore_out_of_range_pitches:
                        raise Exception(
                            f'{voice.name} out of range {pleaf!r}.',
                            )
                    if self.color_out_of_range_pitches:
                        abjad.attach(markup, pleaf, tag='SM13')
                        string = r'\baca_out_of_range_warning'
                        literal = abjad.LilyPondLiteral(string)
                        abjad.attach(literal, pleaf, tag='SM13')

    def _check_wellformedness(self):
        if self.skip_wellformedness_checks:
            return
        if (self.color_octaves or
            self.color_repeat_pitch_classes or
            self.ignore_repeat_pitch_classes):
            return
        manager = WellformednessManager(allow_percussion_clef=True)
        if not manager.is_well_formed(self.score):
            message = manager.tabulate_wellformedness(self.score)
            raise Exception('\n' + message)

    def _collect_alive_during_segment(self):
        result = []
        for context in abjad.iterate(self.score).components(abjad.Context):
            result.append(context.name)
        return result

    def _collect_first_appearance_margin_markup(self):
        if self.first_segment:
            return
        if not self.margin_markups:
            return
        self._cache_previously_alive_contexts()
        dictionary = abjad.OrderedDict()
        prototype = abjad.MarginMarkup
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            if staff.name in self._previously_alive_contexts:
                continue
            for leaf in abjad.iterate(staff).leaves():
                margin_markup = abjad.inspect(leaf).get_effective(prototype)
                if margin_markup is not None:
                    key = self._indicator_to_key(
                        margin_markup,
                        self.manifests,
                        )
                    dictionary[staff.name] = key
                    break
        return dictionary

    def _collect_metadata(self):
        metadata = abjad.OrderedDict()
        metadata['alive_during_segment'] = self._collect_alive_during_segment()
        if self._container_to_part_assignment:
            metadata['container_to_part_assignment'] = \
                self._container_to_part_assignment
        if self._duration is not None:
            metadata['duration'] = self._duration
        if self._fermata_measure_numbers:
            metadata['fermata_measure_numbers'] = self._fermata_measure_numbers
        dictionary = self._collect_first_appearance_margin_markup()
        if dictionary:
            metadata['first_appearance_margin_markup'] = dictionary
        metadata['first_measure_number'] = self._get_first_measure_number()
        metadata['last_measure_number'] = self._get_last_measure_number()
        if self._last_measure_is_fermata:
            metadata['last_measure_is_fermata'] = True
        metadata['persistent_indicators'] = \
            self._collect_persistent_indicators()
        if self.segment_name is not None:
            metadata['segment_name'] = self.segment_name
        metadata['segment_number'] = self._get_segment_number()
        metadata['sounds_during_segment'] = self._sounds_during_segment
        if self._start_clock_time is not None:
            metadata['start_clock_time'] = self._start_clock_time
        if self._stop_clock_time is not None:
            metadata['stop_clock_time'] = self._stop_clock_time
        metadata['time_signatures'] = self._cached_time_signatures
        if self.voice_metadata:
            metadata['voice_metadata'] = self.voice_metadata
        self.metadata.update(metadata)
        self.metadata.sort(recurse=True)
        for key, value in self.metadata.items():
            if not bool(value):
                message = f'{key} metadata should be nonempty'
                message += f' (not {value!r}).'
                raise Exception(message)

    def _collect_persistent_indicators(self):
        result = abjad.OrderedDict()
        contexts = abjad.iterate(self.score).components(abjad.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda _: _.name)
        for context in contexts:
            momentos = []
            dictionary = context._get_persistent_wrappers()
            for wrapper in dictionary.values():
                leaf = wrapper.component
                parentage = abjad.inspect(leaf).get_parentage()
                first_context = parentage.get_first(abjad.Context)
                indicator = wrapper.indicator
                value = self._indicator_to_key(indicator, self.manifests)
                if value is None and self.environment != 'docs':
                    raise Exception(
                        'can not find persistent indicator in manifest:\n\n'
                        f'  {indicator}'
                        )
                if isinstance(indicator.persistent, str):
                    prototype = indicator.persistent
                else:
                    prototype = type(indicator)
                    prototype = self._prototype_string(prototype)
                editions = wrapper.tag.editions()
                if editions:
                    words = [str(_) for _ in editions]
                    editions = abjad.Tag.from_words(words)
                else:
                    editions = None
                momento = abjad.Momento(
                    context=first_context.name,
                    edition=editions,
                    prototype=prototype,
                    value=value,
                    )
                momentos.append(momento)
            if momentos:
                momentos.sort(key=lambda _: _.prototype)
                result[context.name] = momentos
        dictionary = self.previous_metadata.get('persistent_indicators')
        if dictionary:
            for context_name, momentos in dictionary.items():
                if context_name not in result:
                    result[context_name] = momentos
        return result

    def _color_octaves_(self):
        if not self.color_octaves:
            return
        score = self.score
        vertical_moments = abjad.iterate(score).vertical_moments()
        markup = abjad.Markup('OCTAVE', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for vertical_moment in vertical_moments:
            pleaves, pitches = [], []
            for leaf in vertical_moment.leaves:
                if abjad.inspect(leaf).has_indicator(
                    abjad.tags.STAFF_POSITION,
                    ):
                    continue
                if isinstance(leaf, abjad.Note):
                    pleaves.append(leaf)
                    pitches.append(leaf.written_pitch)
                elif isinstance(leaf, abjad.Chord):
                    pleaves.append(leaf)
                    pitches.extend(leaf.written_pitches)
            if not pitches:
                continue
            pitch_classes = [_.pitch_class for _ in pitches]
            if pitchclasses.PitchClassSegment(pitch_classes).has_duplicates():
                color = True
                for pleaf in pleaves:
                    inspection = abjad.inspect(pleaf)
                    if inspection.has_indicator(abjad.tags.ALLOW_OCTAVE):
                        color = False
                if not color:
                    continue
                for pleaf in pleaves:
                    abjad.attach(markup, pleaf, tag='SM12')
                    string = r'\baca_octave_warning'
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, pleaf, tag='SM12')

    def _color_repeat_pitch_classes_(self):
        if not self.color_repeat_pitch_classes:
            return
        manager = WellformednessManager
        lts = manager._find_repeat_pitch_classes(self.score)
        markup = abjad.Markup('@', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for lt in lts:
            for leaf in lt:
                abjad.attach(markup, leaf, tag='SM14')
                string = r'\baca_repeat_pitch_class_warning'
                literal = abjad.LilyPondLiteral(string)
                abjad.attach(literal, leaf, tag='SM14')

    def _color_unpitched_notes(self):
        if self.ignore_unpitched_notes:
            return
        tag = abjad.tags.NOT_YET_PITCHED
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.inspect(pleaf).has_indicator(tag):
                continue
            string = r'\baca_unpitched_music_warning'
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, pleaf, tag='SM24')

    def _color_unregistered_pitches(self):
        if self.ignore_unregistered_pitches:
            return
        tag = abjad.tags.NOT_YET_REGISTERED
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.inspect(pleaf).has_indicator(tag):
                continue
            string = r'\baca_unregistered_pitch_warning'
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, pleaf, tag='SM25')

    def _comment_measure_numbers(self):
        contexts = []
        contexts.extend(self.score['GlobalContext'])
        contexts.extend(abjad.iterate(self.score).components(abjad.Voice))
        first_measure_number = self._get_first_measure_number()
        for context in contexts:
            for leaf in abjad.iterate(context).leaves():
                offset = abjad.inspect(leaf).get_timespan().start_offset
                measure_number = self._offset_to_measure_number.get(
                    offset,
                    None,
                    )
                if measure_number is None:
                    continue
                local_measure_number = measure_number - first_measure_number
                local_measure_number += 1
                if self.segment_name :
                    name = self.segment_name + ' '
                else:
                    name = ''
                if self.first_segment or self.environment == 'docs':
                    string = f'% [{name}{context.name}'
                    string += f' measure {measure_number}]'
                else:
                    string = f'% [{name}{context.name}'
                    string += f' measure {measure_number} /'
                    string += f' measure {local_measure_number}]'
                literal = abjad.LilyPondLiteral(string, 'absolute_before')
                abjad.attach(literal, leaf, tag='SM4')

    def _deactivate_tags(self, tags):
        if not tags:
            return
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if wrapper.tag is None:
                    continue
                for tag in tags:
                    if tag in wrapper.tag:
                        wrapper.deactivate = True
                        break

    @staticmethod
    def _extend_beam(leaf):
        beam = abjad.inspect(leaf).get_spanner(abjad.Beam)
        if beam is None:
            return
        all_leaves = []
        all_leaves.extend(beam.leaves)
        durations = []
        if beam.durations:
            durations.extend(beam.durations)
        else:
            duration = abjad.inspect(beam.leaves).get_duration()
            durations.append(duration)
        intervening_skips = []
        index = 1
        while True:
            next_leaf = abjad.inspect(leaf).get_leaf(index)
            if next_leaf is None:
                return
            index += 1
            if isinstance(next_leaf, abjad.Skip):
                beam = abjad.inspect(next_leaf).get_spanner(abjad.Beam)
                if beam is None:
                    intervening_skips.append(next_leaf)
                    continue
            break
        abjad.detach(abjad.Beam, leaf)
        all_leaves.extend(intervening_skips)
        if intervening_skips:
            intervening_skips = abjad.select(intervening_skips)
            duration = abjad.inspect(intervening_skips).get_duration()
            durations.append(duration)
        beam = abjad.inspect(next_leaf).get_spanner(abjad.Beam)
        if beam is None:
            all_leaves.append(next_leaf)
            duration = abjad.inspect(next_leaf).get_duration()
            durations.append(duration)
        else:
            all_leaves.extend(beam.leaves)
            if beam.durations:
                durations.extend(beam.durations)
            else:
                duration = abjad.inspect(beam.leaves).get_duration()
                durations.append(duration)
        abjad.detach(abjad.Beam, next_leaf)
        all_leaves = abjad.select(all_leaves)
        assert abjad.inspect(all_leaves).get_duration() == sum(durations)
        beam = abjad.Beam(beam_rests=True, durations=durations)
        abjad.attach(beam, all_leaves, tag='SM35')

    def _extend_beams(self):
        for leaf in abjad.iterate(self.score).leaves():
            if abjad.inspect(leaf).get_indicator(abjad.tags.RIGHT_BROKEN_BEAM):
                self._extend_beam(leaf)

    def _force_nonnatural_accidentals(self):
        natural = abjad.Accidental('natural')
        for pleaf in classes.Selection(self.score).pleaves():
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                note_heads = pleaf.note_heads
            for note_head in note_heads:
                if note_head.written_pitch.accidental != natural:
                    note_head.is_forced = True

    def _get_first_measure_number(self):
        if self.first_measure_number is not None:
            return self.first_measure_number
        if not self.previous_metadata:
            return 1
        string = 'first_measure_number'
        first_measure_number = self.previous_metadata.get(string)
        time_signatures = self.previous_metadata.get('time_signatures')
        if first_measure_number is None or time_signatures is None:
            return 1
        first_measure_number += len(time_signatures)
        return first_measure_number

    @staticmethod
    def _get_key(dictionary, value):
        if dictionary is not None:
            for key, value_ in dictionary.items():
                if value_ == value:
                    return key

    def _get_last_measure_number(self):
        return self._get_first_measure_number() + self.measure_count - 1

    def _get_lilypond_includes(self):
        if self.environment == 'docs':
            if abjad.inspect(self.score).get_indicator(abjad.tags.TWO_VOICE):
                return ['two-voice-staff.ily']
            else:
                return ['string-trio.ily']
        elif self.environment == 'external':
            if abjad.inspect(self.score).get_indicator(abjad.tags.TWO_VOICE):
                return [self._absolute_two_voice_staff_stylesheet_path]
            else:
                return [self._absolute_string_trio_stylesheet_path]
        includes = []
        includes.append(self._score_package_stylesheet_path)
        if (not self.first_segment or
            self.nonfirst_segment_lilypond_include):
            includes.append(self._score_package_nonfirst_segment_path)
        return includes

    def _get_measure_number_tag(self, leaf):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        measure_number = self._offset_to_measure_number.get(start_offset)
        if measure_number is not None:
            return f'MEASURE_{measure_number}'

    def _get_measure_offsets(self, start_measure, stop_measure):
        skips = classes.Selection(self.score['GlobalSkips']).skips()
        start_skip = skips[start_measure - 1]
        assert isinstance(start_skip, abjad.Skip), start_skip
        start_offset = abjad.inspect(start_skip).get_timespan().start_offset
        stop_skip = skips[stop_measure - 1]
        assert isinstance(stop_skip, abjad.Skip), stop_skip
        stop_offset = abjad.inspect(stop_skip).get_timespan().stop_offset
        return start_offset, stop_offset

    def _get_measure_time_signatures(
        self,
        start_measure=None,
        stop_measure=None,
        ):
        assert stop_measure is not None
        start_index = start_measure - 1
        if stop_measure is None:
            time_signatures = [self.time_signatures[start_index]]
        else:
            if stop_measure == -1:
                stop_measure = self.measure_count
            stop_index = stop_measure
            time_signatures = self.time_signatures[start_index:stop_index]
        measure_timespan = self._get_measure_timespan(start_measure)
        return measure_timespan.start_offset, time_signatures

    def _get_measure_timespan(self, measure_number):
        start_offset, stop_offset = self._get_measure_offsets(
            measure_number,
            measure_number,
            )
        return abjad.Timespan(start_offset, stop_offset)

    def _get_measure_timespans(self, measure_numbers):
        timespans = []
        first_measure_number = self._get_first_measure_number()
        measure_indices = [
            _ - first_measure_number - 1 for _ in measure_numbers
            ]
        skips = classes.Selection(self.score['GlobalSkips']).skips()
        for i, skip in enumerate(skips):
            if i in measure_indices:
                timespan = abjad.inspect(skip).get_timespan()
                timespans.append(timespan)
        return timespans

    def _get_persistent_indicator(self, context, prototype):
        assert isinstance(context, abjad.Context), repr(context)
        if not self.previous_metadata:
            return
        dictionary = self.previous_metadata.get('persistent_indicators')
        if not dictionary:
            return
        momentos = dictionary.get(context.name)
        if not momentos:
            return
        prototype_string = self._prototype_string(prototype)
        for momento in momentos:
            if momento.prototype == prototype_string:
                indicator = self._key_to_indicator(momento.value, prototype)
                return (indicator, momento.context)

    def _get_previous_segment_voice_metadata(self, voice_name):
        if not self.previous_metadata:
            return
        voice_metadata = self.previous_metadata.get('voice_metadata')
        if not voice_metadata:
            return
        return voice_metadata.get(voice_name, abjad.OrderedDict())

    def _get_previous_state(self, voice_name, command_persist):
        if not self.previous_metadata:
            return
        if not command_persist:
            return
        dictionary = self.previous_metadata.get('voice_metadata')
        if not bool(dictionary):
            return
        dictionary = dictionary.get(voice_name)
        if not bool(dictionary):
            return
        previous_state = dictionary.get(command_persist)
        return previous_state

    def _get_previous_stop_clock_time(self):
        if self.previous_metadata:
            return self.previous_metadata.get('stop_clock_time')

    def _get_segment_measure_numbers(self):
        first_measure_number = self._get_first_measure_number()
        last_measure_number = self._get_last_measure_number()
        return list(range(first_measure_number, last_measure_number + 1))

    def _get_segment_number(self):
        if not self.previous_metadata:
            segment_number = 0
        else:
            segment_number = self.previous_metadata.get('segment_number')
            if segment_number is None:
                message = 'previous metadata missing segment number.'
                raise Exception(message)
        return segment_number + 1

    @staticmethod
    def _get_tag(status, stem, prefix=None, suffix=None):
        stem = abjad.String(stem).delimit_words()
        stem = '_'.join([_.upper() for _ in stem])
        if suffix is not None:
            name = f'{status.upper()}_{stem}_{suffix.upper()}'
        else:
            name = f'{status.upper()}_{stem}'
        if prefix is not None:
            name = f'{prefix.upper()}_{name}'
        tag = getattr(abjad.tags, name)
        return abjad.Tag(tag)

    def _handle_mutator(self, command):
        if (hasattr(command, '_mutates_score') and command._mutates_score()):
            self._cache = None
            self._update_score_one_time()

    def _import_manifests(self):
        if not self.segment_directory:
            return
        score_package = self.segment_directory._import_score_package()
        if not self.instruments:
            instruments = getattr(score_package, 'instruments', None)
            self._instruments = instruments
        if not self.margin_markups:
            margin_markups = getattr(score_package, 'margin_markups', None)
            self._margin_markups = margin_markups
        if not self.metronome_marks:
            metronome_marks = getattr(score_package, 'metronome_marks', None)
            self._metronome_marks = metronome_marks
        if not self.score_template:
            score_template = getattr(score_package, 'ScoreTemplate', None)
            if score_template is not None:
                score_template = score_template()
            self._score_template = score_template

    @staticmethod
    def _indicator_to_grob(indicator):
        if isinstance(indicator, abjad.Dynamic):
            return 'DynamicText'
        elif isinstance(indicator, abjad.Instrument):
            return 'InstrumentName'
        elif isinstance(indicator, abjad.MetronomeMark):
            return 'TextScript'
        elif isinstance(indicator, abjad.MarginMarkup):
            return 'InstrumentName'
        elif isinstance(indicator, indicators.StaffLines):
            return 'StaffSymbol'
        return type(indicator).__name__

    @staticmethod
    def _indicator_to_key(indicator, manifests):
        if isinstance(indicator, abjad.Clef):
            key = indicator.name
        elif isinstance(indicator, abjad.Dynamic):
            if indicator.name == 'niente':
                key = 'niente'
            else:
                key = indicator.command or indicator.name
        elif isinstance(indicator, abjad.Instrument):
            key = SegmentMaker._get_key(
                manifests['abjad.Instrument'],
                indicator,
                )
        elif isinstance(indicator, abjad.MetronomeMark):
            key = SegmentMaker._get_key(
                manifests['abjad.MetronomeMark'],
                indicator,
                )
        elif isinstance(indicator, abjad.MarginMarkup):
           key = SegmentMaker._get_key(
                manifests['abjad.MarginMarkup'],
                indicator,
                )
        elif isinstance(indicator, abjad.PersistentOverride):
            key = indicator
        elif isinstance(indicator, indicators.StaffLines):
            key = indicator.line_count
        elif isinstance(indicator, (indicators.Accelerando, indicators.Ritardando)):
            key = f'abjad.{repr(indicator)}'
        else:
            key = str(indicator)
        return key

    def _initialize_time_signatures(self, time_signatures):
        time_signatures = time_signatures or ()
        time_signatures_ = list(time_signatures)
        time_signatures_ = []
        for time_signature in time_signatures:
            time_signature = abjad.TimeSignature(time_signature)
            time_signatures_.append(time_signature)
        time_signatures_ = tuple(time_signatures_)
        if not time_signatures_:
            time_signatures_ = None
        self._time_signatures = time_signatures_

    def _intercalate_silences(self, rhythms):
        result = []
        durations = [_.duration for _ in self.time_signatures]
        measure_start_offsets = abjad.mathtools.cumulative_sums(durations)
        segment_duration = measure_start_offsets[-1]
        self._segment_duration = segment_duration
        previous_stop_offset = abjad.Offset(0)
        for rhythm in rhythms:
            start_offset = rhythm.start_offset
            if start_offset < previous_stop_offset:
                raise Exception('overlapping offsets: {rhythm!r}.')
            if previous_stop_offset < start_offset:
                silences = self._make_measure_silences(
                    previous_stop_offset,
                    start_offset,
                    measure_start_offsets,
                    )
                result.extend(silences)
            result.extend(rhythm.annotation)
            duration = abjad.inspect(rhythm.annotation).get_duration()
            previous_stop_offset = start_offset + duration
        if previous_stop_offset < segment_duration:
            silences = self._make_measure_silences(
                previous_stop_offset,
                segment_duration,
                measure_start_offsets,
                )
            result.extend(silences)
        return result

    def _key_to_indicator(self, key, prototype):
        assert isinstance(key, (int, str)), repr(key)
        if key is None:
            return 
        if prototype in (abjad.Clef, abjad.Dynamic):
            indicator = prototype(key)
        elif prototype is abjad.Instrument:
            indicator = self.instruments.get(key)
        elif prototype is abjad.MarginMarkup:
            indicator = self.margin_markups.get(key)
        elif prototype is abjad.MetronomeMark:
            indicator = self.metronome_marks.get(key)
        elif prototype is abjad.TimeSignature:
            indicator = abjad.TimeSignature.from_string(key)
        elif prototype is indicators.StaffLines:
            indicator = indicators.StaffLines(line_count=key)
        else:
            raise Exception(prototype)
        return indicator

    def _label_clock_time(self):
        if self.environment == 'docs':
            return
        skips = classes.Selection(self.score['GlobalSkips']).skips()
        if self.clock_time_override:
            metronome_mark = self.clock_time_override
            abjad.attach(metronome_mark, skips[0])
        if abjad.inspect(skips[0]).get_effective(abjad.MetronomeMark) is None:
            return
        start_clock_time = self._get_previous_stop_clock_time()
        start_clock_time = start_clock_time or "0'00''"
        self._start_clock_time = start_clock_time 
        minutes = 0
        if "'" in self._start_clock_time:
            tick_index = self._start_clock_time.find("'")
            minutes = self._start_clock_time[:tick_index]
            minutes = int(minutes)
        seconds = self._start_clock_time[-4:-2]
        seconds = int(seconds)
        seconds = 60 * minutes + seconds
        segment_start_offset = abjad.Duration(seconds)
        tag = abjad.Tag(abjad.tags.CLOCK_TIME_MARKUP)
        label = abjad.label(
            skips,
            deactivate=True,
            tag=tag.prepend('SM28'),
            )
        segment_stop_duration = label.with_start_offsets(
            brackets=True,
            clock_time=True,
            global_offset=segment_start_offset,
            markup_command=r'\baca-dark-cyan-markup',
            )
        segment_stop_offset = abjad.Offset(segment_stop_duration)
        self._stop_clock_time = segment_stop_offset.to_clock_string()
        segment_duration = segment_stop_offset - segment_start_offset
        segment_duration = segment_duration.to_clock_string()
        self._duration = segment_duration
        if self.clock_time_override:
            metronome_mark = self.clock_time_override
            abjad.detach(metronome_mark, skips[0])

    def _label_measure_indices(self):
        skips = classes.Selection(self.score['GlobalSkips']).skips()
        first_measure_number = self._get_first_measure_number()
        for measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + measure_index
            string = rf'\baca-dark-cyan-markup ({measure_number})'
            markup = abjad.Markup.from_literal(
                string,
                direction=abjad.Up,
                literal=True
                )
            tag = abjad.Tag(abjad.tags.MEASURE_NUMBER_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM31'),
                )
            string = rf'\baca-dark-cyan-markup <{measure_index}>'
            markup = abjad.Markup.from_literal(
                string,
                direction=abjad.Up,
                literal=True
                )
            tag = abjad.Tag(abjad.tags.MEASURE_INDEX_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM32'),
                )
            local_measure_number = measure_index + 1
            string = rf'\baca-dark-cyan-markup (({local_measure_number}))'
            markup = abjad.Markup.from_literal(
                string,
                direction=abjad.Up,
                literal=True,
                )
            tag = abjad.Tag(abjad.tags.LOCAL_MEASURE_NUMBER_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM42'),
                )

    def _label_stage_numbers(self):
        skips = classes.Selection(self.score['GlobalSkips']).skips()
        for measure_index in range(self.measure_count):
            measure_number = measure_index + 1
            name = self.segment_name
            if bool(name):
                string = f'[{name}.{measure_number}]'
            else:
                string = f'[{measure_number}]'
            string = rf'\baca-dark-cyan-markup {string}'
            markup = abjad.Markup.from_literal(
                string,
                direction=abjad.Up,
                literal=True,
                )
            skip = skips[measure_index]
            tag = abjad.Tag(abjad.tags.STAGE_NUMBER_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM3'),
                )

    def _magnify_staves_(self):
        if self.magnify_staves is None:
            return
        if isinstance(self.magnify_staves, tuple):
            multiplier, tag = self.magnify_staves
        else:
            multiplier, tag = self.magnify_staves, None
        multiplier = abjad.Multiplier(multiplier)
        numerator, denominator = multiplier.pair
        string = rf'\magnifyStaff #{numerator}/{denominator}'
        tag = abjad.Tag(tag).prepend('SM41')
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            first_leaf = abjad.inspect(staff).get_leaf(0)
            assert first_leaf is not None
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(
                literal,
                first_leaf,
                tag=tag,
                )

    def _make_global_skips(self):
        context = self.score['GlobalSkips']
        for time_signature in self.time_signatures:
            skip = abjad.Skip(1)
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, skip, tag=None)
            abjad.attach(time_signature, skip, context='Score', tag='SM1')
            context.append(skip)
        if self.first_segment:
            return
        # empty start bar allows LilyPond to print bar numbers
        # at start of nonfirst segments
        first_skip = classes.Selection(context).skip(0)
        literal = abjad.LilyPondLiteral(r'\bar ""')
        tag = abjad.Tag(abjad.tags.EMPTY_START_BAR)
        tag = tag.prepend('+SEGMENT')
        abjad.attach(
            literal,
            first_skip,
            tag=tag.prepend('SM2'),
            )

    def _make_lilypond_file(self):
        includes = self._get_lilypond_includes()
        lilypond_file = abjad.LilyPondFile.new(
            music=self.score,
            date_time_token=False,
            includes=includes,
            use_relative_includes=False,
            )
        block_names = ('layout', 'paper')
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) in block_names:
                lilypond_file.items.remove(item)
        if self._midi:
            block = abjad.Block(name='midi')
            lilypond_file.items.append(block)
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) == 'header':
                lilypond_file.items.remove(item)
        if self.environment != 'docs' and not self.do_not_include_layout_ly:
            assert len(lilypond_file.score_block.items) == 1
            score = lilypond_file.score_block.items[0]
            assert isinstance(score, abjad.Score)
            include = abjad.Container()
            string = r'\include "layout.ly"'
            literal = abjad.LilyPondLiteral(string, 'opening')
            abjad.attach(literal, include, tag=None)
            container = abjad.Container(
                [include, score],
                is_simultaneous=True,
                )
            lilypond_file.score_block.items[:] = [container]
        self._lilypond_file = lilypond_file

    def _make_measure_silences(self, start, stop, measure_start_offsets):
        offsets = [start]
        for measure_start_offset in measure_start_offsets:
            if start < measure_start_offset < stop:
                offsets.append(measure_start_offset)
        offsets.append(stop)
        silences = []
        durations = abjad.mathtools.difference_series(offsets)
        for duration in durations:
            multiplier = abjad.Multiplier(duration)
            if self.skips_instead_of_rests:
                silence = abjad.Skip(1)
            else:
                silence = abjad.MultimeasureRest(1)
            abjad.attach(multiplier, silence, tag=None)
            silences.append(silence)
        return silences

    def _make_multimeasure_rests(self):
        rests = []
        for time_signature in self.time_signatures:
            rest = abjad.MultimeasureRest(abjad.Duration(1))
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, rest, tag=None)
            rests.append(rest)
        return rests

    def _make_score(self):
        score = self.score_template()
        self._score = score
        if self.do_not_include_layout_ly:
            first_measure_number = self._get_first_measure_number()
            if first_measure_number != 1:
                abjad.setting(score).current_bar_number = first_measure_number

    def _momento_to_indicator(self, momento):
        # for selector evaluation:
        import baca
        if momento.value is None:
            return
        if momento.value in ('baca.Accelerando()', 'baca.Ritardando()'):
            indicator = eval(momento.value)
            return indicator
        if momento.prototype in self._prototype_to_manifest_name:
            name = self._prototype_to_manifest_name.get(momento.prototype)
            dictionary = getattr(self, name)
            if dictionary is None:
                raise Exception(f'can not find {name!r} manifest.')
            return dictionary.get(momento.value)
        class_ = eval(momento.prototype)
        if hasattr(class_, 'from_string'):
            indicator =  class_.from_string(momento.value)
        elif class_ is abjad.Dynamic and momento.value.startswith('\\'):
            indicator = class_(name='', command=momento.value)
        elif isinstance(momento.value, class_):
            indicator = momento.value
        elif class_ is indicators.StaffLines:
            indicator = class_(line_count=momento.value)
        else:
            indicator = class_(momento.value)
        return indicator

    def _parallelize_multimeasure_rests(self):
        prototype = abjad.MultimeasureRest
        context = self.score['MusicContext']
        for mmrest in abjad.iterate(context).components(prototype):
            previous = abjad.inspect(mmrest).get_leaf(-1)
            if previous is None:
                continue
            if isinstance(previous, prototype):
                continue
            should_parallelize = False
            spanners = abjad.inspect(previous).get_spanners(abjad.TextSpanner)
            for spanner in spanners:
                if getattr(spanner, 'leak', False) is True:
                    should_parallelize = True
            for indicator in abjad.inspect(previous).get_indicators(
                abjad.StopTextSpan):
                if indicator.leak is True:
                    should_parallelize = True
            if not should_parallelize:
                continue
            parentage = abjad.inspect(previous).get_parentage()
            voice = parentage.get_first(abjad.Voice)
            multiplier = abjad.inspect(mmrest).get_indicator(
                abjad.Multiplier,
                )
            before = abjad.LilyPondLiteral(
                [
                    rf'\voices "{voice.name}", "MultimeasureRestVoice"',
                    '<<',
                    r'    \tweak NoteHead.no-ledgers ##t',
                    r'    \tweak NoteHead.transparent ##t',
                    r'    \tweak Dots.transparent ##t',
                    rf"    c'1 * {multiplier!s}",
                    r'\\',
                    ],
                    'before',
                    )
            abjad.attach(before, mmrest)
            after = abjad.LilyPondLiteral('>>', 'after')
            abjad.attach(after, mmrest)

    def _populate_offset_to_measure_number(self):
        measure_number = self._get_first_measure_number()
        for skip in classes.Selection(self.score['GlobalSkips']).skips():
            offset = abjad.inspect(skip).get_timespan().start_offset
            self._offset_to_measure_number[offset] = measure_number
            measure_number += 1

    def _print_cache(self):
        for context in self._cache:
            print(f'CONTEXT {context} ...')
            leaves_by_measure_number = self._cache[context]
            for measure_number in leaves_by_measure_number:
                print(f'MEASURE {measure_number} ...')
                for leaf in leaves_by_measure_number[measure_number]:
                    print(leaf)

    @staticmethod
    def _prototype_string(class_):
        parts = class_.__module__.split('.')
        if parts[-1] != class_.__name__:
            parts.append(class_.__name__)
        return f'{parts[0]}.{parts[-1]}'

    def _reapply_persistent_indicators(self):
        if self.first_segment:
            return
        string = 'persistent_indicators'
        dictionary = self.previous_metadata.get('persistent_indicators')
        if not dictionary:
            return
        for context in abjad.iterate(self.score).components(abjad.Context):
            momentos = dictionary.get(context.name)
            if not momentos:
                continue
            for momento in momentos:
                result = self._analyze_momento(context, momento)
                if result is None:
                    continue
                leaf, previous_indicator, status, edition = result
                if isinstance(previous_indicator, abjad.TimeSignature):
                    if status is None:
                        continue
                    assert status == 'reapplied', repr(status)
                    wrapper = abjad.inspect(leaf).wrapper(abjad.TimeSignature)
                    edition = edition.prepend('SM38')
                    wrapper.tag = wrapper.tag.prepend(edition)
                    self._treat_persistent_wrapper(
                        self.manifests,
                        wrapper,
                        status,
                        )
                    continue
                prototype = (
                    indicators.Accelerando,
                    abjad.MetronomeMark,
                    indicators.Ritardando,
                    )
                if isinstance(previous_indicator, prototype):
                    if status == 'reapplied':
                        wrapper = abjad.attach(
                            previous_indicator,
                            leaf,
                            tag=edition.append('SM36'),
                            wrapper=True,
                            )
                        self._treat_persistent_wrapper(
                            self.manifests,
                            wrapper,
                            status,
                            )
                    else:
                        assert status in ('redundant', None), repr(status)
                        if status is None:
                            status = 'explicit'
                        wrappers = abjad.inspect(leaf).wrappers(prototype)
                        # lone metronome mark or lone tempo trend:
                        if len(wrappers) == 1:
                            wrapper = wrappers[0]
                        # metronome mark + tempo trend:
                        else:
                            assert 1 < len(wrappers), repr(wrappers)
                            prototype = abjad.MetronomeMark
                            wrapper = abjad.inspect(leaf).wrapper(prototype)
                        wrapper.tag = wrapper.tag.prepend(edition)
                        self._treat_persistent_wrapper(
                            self.manifests,
                            wrapper,
                            status,
                            )
                    continue
                attached = False
                tag = edition.append('SM37')
                if isinstance(previous_indicator, abjad.MarginMarkup):
                    tag = tag.append('-PARTS')
                try:
                    wrapper = abjad.attach(
                        previous_indicator,
                        leaf,
                        tag=tag,
                        wrapper=True,
                        )
                    attached = True
                except abjad.PersistentIndicatorError:
                    pass
                if attached:
                    self._treat_persistent_wrapper(
                        self.manifests,
                        wrapper,
                        status,
                        )

    def _remove_redundant_time_signatures(self):
        previous_time_signature = None
        self._cached_time_signatures = []
        for skip in classes.Selection(self.score['GlobalSkips']).skips():
            time_signature = abjad.inspect(skip).get_indicator(
                abjad.TimeSignature
                )
            self._cached_time_signatures.append(str(time_signature))
            if time_signature == previous_time_signature:
                abjad.detach(time_signature, skip)
            else:
                previous_time_signature = time_signature

    def _remove_tags(self, tags):
        tags = tags or []
        tags = list(tags)
        if self.environment == 'docs':
            tags += abjad.tags.documentation_removal_tags()
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if wrapper.tag is None:
                    continue
                for word in wrapper.tag:
                    if word in tags:
                        abjad.detach(wrapper, leaf)
                        break

    def _scope_to_leaf_selection(self, command):
        leaves = []
        selections = self._scope_to_leaf_selections(command.scope)
        for selection in selections:
            leaves.extend(selection)
        selection = abjad.select(leaves)
        if not selection:
            message = f'EMPTY SELECTION:\n\n{format(command)}'
            if self.allow_empty_selections:
                print(message)
            else:
                raise Exception(message)
        assert selection.are_leaves(), repr(selection)
        if isinstance(command.scope, scoping.TimelineScope):
            selection = command.scope._sort_by_timeline(selection)
        return selection

    def _scope_to_leaf_selections(self, scope):
        if self._cache is None:
            self._cache_leaves()
        if isinstance(scope, scoping.Scope):
            scopes = [scope]
        else:
            assert isinstance(scope, scoping.TimelineScope)
            scopes = list(scope.scopes)
        leaf_selections = []
        for scope in scopes:
            leaves = []
            try:
                leaves_by_measure_number = self._cache[scope.voice_name]
            except KeyError:
                print(f'Unknown voice {scope.voice_name} ...\n')
                raise
            start = scope.measures[0]
            if scope.measures[1] == -1:
                stop = self.measure_count + 1
            else:
                stop = scope.measures[1] + 1
            if start < 0:
                start = self.measure_count - abs(start) + 1
            if stop < 0:
                stop = self.measure_count - abs(stop) + 1
            for measure_number in range(start, stop):
                leaves.extend(leaves_by_measure_number[measure_number])
            leaf_selections.append(abjad.select(leaves))
        return leaf_selections

    def _set_status_tag(wrapper, status, redraw=None, stem=None):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        existing_tag = wrapper.tag
        stem = stem or abjad.String.to_indicator_stem(wrapper.indicator)
        prefix = None
        if redraw is True:
            prefix = 'redrawn'
        tag = SegmentMaker._get_tag(status, stem, prefix=prefix)
        if wrapper.tag:
            tag = wrapper.tag.prepend(tag)
        tag = tag.prepend('SM8')
        wrapper.tag = tag

    def _shift_clefs_into_fermata_measures(self):
        fermata_stop_offsets = self._fermata_stop_offsets[:]
        if self.previous_metadata.get('last_measure_is_fermata') is True:
            fermata_stop_offsets.insert(0, abjad.Offset(0))
        if not fermata_stop_offsets:
            return
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.inspect(leaf).get_timespan().start_offset
                if start_offset not in fermata_stop_offsets:
                    continue
                wrapper = abjad.inspect(leaf).wrapper(abjad.Clef)
                if wrapper is None or not wrapper.tag:
                    continue
                if abjad.tags.EXPLICIT_CLEF not in wrapper.tag:
                    continue
                measure_number = self._offset_to_measure_number.get(
                    start_offset,
                    )
                if measure_number is None:
                    continue
                clef = wrapper.indicator
                command = baca_overrides.clef_shift(
                    clef,
                    selector='baca.leaf(0)',
                    )
                command.runtime = self._bundle_manifests()
                command(leaf)

    def _shorten_long_repeat_ties(self):
        leaves = abjad.iterate(self.score).leaves()
        for leaf in leaves:
            ties = abjad.inspect(leaf).get_spanners(abjad.Tie)
            if not ties:
                continue
            tie = ties.pop()
            if not tie.repeat:
                continue
            previous_leaf = abjad.inspect(leaf).get_leaf(-1)
            if previous_leaf is None:
                continue
            minimum_duration = abjad.Duration(1, 8)
            if abjad.inspect(previous_leaf).get_duration() < minimum_duration:
                string = r"\shape #'((2 . 0) (1 . 0) (0.5 . 0) (0 . 0))"
                string += " RepeatTie"
                literal = abjad.LilyPondLiteral(string)
                abjad.attach(literal, leaf, tag='SM26')

    def _style_fermata_measures(self):
        if self.fermata_measure_staff_line_count is None:
            return
        if not self._fermata_start_offsets:
            return
        prototype = indicators.StaffLines
        staff_lines = indicators.StaffLines(
            line_count=self.fermata_measure_staff_line_count,
            )
        bar_lines_already_styled = []
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.inspect(leaf).get_timespan().start_offset
                if start_offset not in self._fermata_start_offsets:
                    continue
                before = abjad.inspect(leaf).get_effective(prototype)
                next_leaf = abjad.inspect(leaf).get_leaf(1)
                if next_leaf is not None:
                    after = abjad.inspect(next_leaf).get_effective(prototype)
                if before != staff_lines:
                    strings = staff_lines._get_lilypond_format(context=staff)
                    if getattr(before, 'line_count', 5) == 5:
                        context = staff.lilypond_type
                        string = f"{context}.BarLine.bar-extent = #'(-2 . 2)"
                        string = r'\once \override ' + string
                        strings.append(string)
                    if strings:
                        literal = abjad.LilyPondLiteral(strings)
                        abjad.attach(literal, leaf, tag='SM20')
                if next_leaf is not None and staff_lines != after:
                    strings = after._get_lilypond_format(context=staff)
                    literal = abjad.LilyPondLiteral(strings)
                    abjad.attach(literal, next_leaf, tag='SM21')
                if next_leaf is None and before != staff_lines:
                    before_line_count = getattr(before, 'line_count', 5)
                    before_staff_lines = indicators.StaffLines(
                        line_count=before_line_count,
                        hide=True,
                        )
                    abjad.attach(
                        before_staff_lines,
                        leaf,
                        tag='SM23',
                        synthetic_offset=1_000_000,
                        )
                if start_offset in bar_lines_already_styled:
                    continue
                strings = []
                if (staff_lines.line_count == 0 and
                    not (next_leaf is None and self.last_segment)):
                    string = r'Score.BarLine.transparent = ##t'
                    string = r'\once \override ' + string
                    strings.append(string)
                    string = r'Score.SpanBar.transparent = ##t'
                    string = r'\once \override ' + string
                    strings.append(string)
                elif staff_lines.line_count == 1:
                    string = "Score.BarLine.bar-extent = #'(-2 . 2)"
                    string = r'\once \override ' + string
                    strings.append(string)
                if strings:
                    literal = abjad.LilyPondLiteral(strings, 'after')
                    tag = abjad.Tag(abjad.tags.EOL_FERMATA)
                    measure_number_tag = self._get_measure_number_tag(leaf)
                    if measure_number_tag is not None:
                        tag = tag.append(measure_number_tag)
                    abjad.attach(
                        literal,
                        leaf,
                        tag=tag.prepend('SM22'),
                        )
                bar_lines_already_styled.append(start_offset)

    def _transpose_score_(self):
        if not self.transpose_score:
            return
        for pleaf in classes.Selection(self.score).pleaves():
            if abjad.inspect(pleaf).has_indicator(abjad.tags.DO_NOT_TRANSPOSE):
                continue
            abjad.Instrument.transpose_from_sounding_pitch(pleaf)

    @staticmethod
    def _treat_persistent_wrapper(manifests, wrapper, status):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        assert bool(wrapper.indicator.persistent), repr(wrapper)
        assert isinstance(status, str), repr(status)
        context = wrapper._find_correct_effective_context()
        assert isinstance(context, abjad.Context), repr(wrapper)
        leaf = wrapper.component
        assert isinstance(leaf, abjad.Leaf), repr(wrapper)
        indicator = wrapper.indicator
        existing_tag = wrapper.tag
        tempo_trend = (indicators.Accelerando, indicators.Ritardando)
        if (isinstance(indicator, abjad.MetronomeMark) and
            abjad.inspect(leaf).has_indicator(tempo_trend)):
            status = 'explicit'
        if (isinstance(wrapper.indicator, abjad.Dynamic) and
            abjad.inspect(leaf).get_indicators(abjad.DynamicTrend)):
            status = 'explicit'
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        SegmentMaker._attach_latent_indicator_alert(
            manifests,
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        SegmentMaker._attach_color_cancelation_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        if isinstance(wrapper.indicator, abjad.Clef):
            string = rf'\set {context.lilypond_type}.forceClef = ##t'
            literal = abjad.LilyPondLiteral(string)
            wrapper_ = abjad.attach(
                literal,
                wrapper.component,
                tag=wrapper.tag.prepend('SM33'),
                wrapper=True,
                )
            SegmentMaker._set_status_tag(wrapper_, status, stem='CLEF')
        SegmentMaker._set_status_tag(wrapper, status)
        SegmentMaker._attach_color_redraw_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        if (isinstance(indicator, (abjad.Instrument, abjad.MarginMarkup)) and
            not getattr(indicator, 'hide', False)):
            strings = indicator._get_lilypond_format(context=context)
            literal = abjad.LilyPondLiteral(strings, 'after')
            stem = abjad.String.to_indicator_stem(indicator)
            wrapper_ = abjad.attach(
                literal,
                leaf,
                tag=existing_tag.prepend('SM34'),
                wrapper=True,
                )
            SegmentMaker._set_status_tag(
                wrapper_,
                status,
                redraw=True,
                stem=stem,
                )

    def _treat_untreated_persistent_wrappers(self):
        tempo_prototype = (
            indicators.Accelerando,
            abjad.MetronomeMark,
            indicators.Ritardando,
            )
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if not getattr(wrapper.indicator, 'persistent', False):
                    continue
                if wrapper.tag and wrapper.tag.has_persistence_tag():
                    continue
                if isinstance(wrapper.indicator, abjad.Instrument):
                    prototype = abjad.Instrument
                elif isinstance(wrapper.indicator, tempo_prototype):
                    prototype = tempo_prototype
                else:
                    prototype = type(wrapper.indicator)

                previous_indicator = abjad.inspect(leaf).get_effective(
                    prototype,
                    n=-1,
                    )
                if previous_indicator != wrapper.indicator:
                    status = 'explicit'
                elif (isinstance(previous_indicator, abjad.Dynamic) and
                    previous_indicator.sforzando):
                    status = 'explicit'
                else:
                    status = 'redundant'
                self._treat_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    status,
                    )

    @staticmethod
    def _unpack_measure_token_list(measure_token_list):
        assert isinstance(measure_token_list, list), repr(measure_token_list)
        measure_tokens = []
        for measure_token in measure_token_list:
            if isinstance(measure_token, int):
                measure_tokens.append(measure_token)
            elif isinstance(measure_token, tuple):
                assert len(measure_token) == 2, repr(scopes)
                start, stop = measure_token
                measure_tokens.append((start, stop))
            else:
                raise TypeError(measure_token_list)
        return measure_tokens

    def _unpack_scope_pair(self, scopes, abbreviations):
        assert isinstance(scopes, tuple), repr(scopes)
        assert len(scopes) == 2, repr(scopes)
        assert isinstance(scopes[0], (list, str)), repr(scopes)
        assert isinstance(scopes[1], (int, list, tuple)), repr(scopes)
        if isinstance(scopes[0], str):
            voice_names = [scopes[0]]
        else:
            voice_names = scopes[0]
        assert isinstance(voice_names, list), repr(voice_names)
        assert all(isinstance(_, str) for _ in voice_names)
        token_type = typing.Union[int, typing.Tuple[int, int]]
        measure_tokens: typing.List[token_type] = []
        if isinstance(scopes[1], int):
            measure_tokens.append(scopes[1])
        elif isinstance(scopes[1], tuple):
            assert len(scopes[1]) == 2, repr(scopes)
            start, stop = scopes[1]
            measure_tokens.append((start, stop))
        elif isinstance(scopes[1], list):
            measure_tokens = self._unpack_measure_token_list(scopes[1])
        else:
            raise TypeError(scopes)
        scopes_ = []
        voice_names_ = []
        for voice_name in voice_names:
            result = abbreviations.get(voice_name, voice_name)
            if isinstance(result, list):
                voice_names_.extend(result)
            else:
                assert isinstance(result, str)
                voice_names_.append(result)
        voice_names = voice_names_
        for voice_name in voice_names:
            for measure_token in measure_tokens:
                scope = scoping.Scope(
                    measures=measure_token,
                    voice_name=voice_name,
                    )
                scopes_.append(scope)
        prototype = (scoping.Scope, scoping.TimelineScope)
        assert all(isinstance(_, prototype) for _ in scopes_)
        return scopes_

    def _unpack_scopes(self, scopes, abbreviations):
        scope_type = (scoping.Scope, scoping.TimelineScope)
        scopes__: typing.List[scoping.scope_typing]
        if isinstance(scopes, str):
            voice_name = abbreviations.get(scopes, scopes)
            scope = scoping.Scope(voice_name=voice_name)
            scopes__ = [scope]
        elif isinstance(scopes, tuple):
            scopes__ = self._unpack_scope_pair(scopes, abbreviations)
        elif isinstance(scopes, scope_type):
            scopes__ = [scopes]
        else:
            assert isinstance(scopes, list), repr(scopes)
            scopes_ = []
            for scope in scopes:
                if isinstance(scope, tuple):
                    scopes__ = self._unpack_scope_pair(scope, abbreviations)
                    scopes_.extend(scopes__)
                else:
                    scopes_.append(scope)
            scopes__ = scopes_
        assert isinstance(scopes__, list), repr(scopes__)
        scopes_ = []
        for scope in scopes__:
            if isinstance(scope, str):
                voice_name = abbreviations.get(scope, scope)
                scope_ = scoping.Scope(voice_name=voice_name)
                scopes_.append(scope_)
            elif isinstance(scope, tuple):
                voice_name, measures = scope
                voice_name = abbreviations.get(voice_name, voice_name)
                if isinstance(measures, list):
                    measures = self._unpack_measure_token_list(measures)
                    for measure_token in measures:
                        scope_ = scoping.Scope(
                            measures=measure_token,
                            voice_name=voice_name,
                            )
                        scopes_.append(scope_)
                else:
                    scope_ = scoping.Scope(
                        measures=measures,
                        voice_name=voice_name,
                        )
                    scopes_.append(scope_)
            else:
                scope_ = scope
                scopes_.append(scope_)
        return scopes_

    def _update_score_one_time(self):
        is_forbidden_to_update = self.score._is_forbidden_to_update
        self.score._is_forbidden_to_update = False
        self.score._update_now(offsets=True)
        self.score._is_forbidden_to_update = is_forbidden_to_update

    def _validate_measure_count_(self):
        if not self.validate_measure_count:
            return
        found = len(self.time_signatures)
        if found != self.validate_measure_count:
            message =  f'found {found} measures'
            message += f' (not {self.validate_measure_count}).'
            raise Exception(message)

    def _voice_to_rhythm_commands(self, voice):
        commands = []
        for command in self.commands:
            if not isinstance(command, rhythmcommands.RhythmCommand):
                continue
            if command.scope.voice_name == voice.name:
                commands.append(command)
        return commands

    def _whitespace_leaves(self):
        for leaf in abjad.iterate(self.score).leaves():
            literal = abjad.LilyPondLiteral('', 'absolute_before')
            abjad.attach(literal, leaf, tag=None)
            if abjad.inspect(leaf).get_leaf(1) is None:
                literal = abjad.LilyPondLiteral('', 'absolute_after')
                abjad.attach(literal, leaf, tag=None)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_empty_selections(self) -> typing.Optional[bool]:
        """
        Is true when segment allows empty selectors.

        Otherwise segment raises exception on empty selectors.
        """
        return self._allow_empty_selections

    @property
    def breaks(self) -> typing.Optional[segmentclasses.BreakMeasureMap]:
        """
        Gets breaks.
        """
        return self._breaks

    @property
    def clock_time_override(self) -> typing.Optional[abjad.MetronomeMark]:
        """
        Gets clock time override.
        """
        return self._clock_time_override

    @property
    def color_octaves(self) -> typing.Optional[bool]:
        r"""
        Is true when segment-maker colors octaves.

        ..  container:: example

            Colors octaves:

            >>> maker = baca.SegmentMaker(
            ...     color_octaves=True,
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 31)),
            ...     time_signatures=[(6, 16), (6, 16)],
            ...     )

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'ViolinMusicVoice',
            ...     [[2, 4, 5, 7, 9, 11]],
            ...     baca.flags(),
            ...     )
            >>> maker(
            ...     ('ViolinMusicVoice', 1),
            ...     baca.rhythm(contribution['ViolinMusicVoice']),
            ...     )

            >>> contribution = music_maker(
            ...     'CelloMusicVoice',
            ...     [[-3, -5, -7, -8, -10, -12]],
            ...     baca.flags(),
            ...     )
            >>> maker(
            ...     ('CelloMusicVoice', 1),
            ...     baca.rhythm(contribution['CelloMusicVoice']),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    autoBeaming = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #31                                             %! HSS1:SPACING
                            \time 6/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #31                                             %! HSS1:SPACING
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context StringSectionStaffGroup = "String Section Staff Group"
                        <<
                            \tag Violin                                                                  %! ST4
                            \context ViolinMusicStaff = "ViolinMusicStaff"
                            {
                                \context ViolinMusicVoice = "ViolinMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolinMusicVoice measure 1]                               %! SM4
                                            \clef "treble"                                               %! SM8:DEFAULT_CLEF:ST3
                                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override ViolinMusicStaff.Clef.color = ##f                  %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set ViolinMusicStaff.forceClef = ##t                        %! SM8:DEFAULT_CLEF:SM33:ST3
                                            d'16
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Violin)                                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            e'16
                <BLANKLINE>
                                            \baca_octave_warning                                         %! SM12
                                            f'16
                                            - \tweak color #red                                          %! SM12
                                            ^ \markup { OCTAVE }                                         %! SM12
                <BLANKLINE>
                                            g'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            b'16
                                        }
                                    }
                <BLANKLINE>
                                    % [ViolinMusicVoice measure 2]                                       %! SM4
                                    R1 * 3/8
                <BLANKLINE>
                                }
                            }
                            \tag Viola                                                                   %! ST4
                            \context ViolaMusicStaff = "ViolaMusicStaff"
                            {
                                \context ViolaMusicVoice = "ViolaMusicVoice"
                                {
                <BLANKLINE>
                                    % [ViolaMusicVoice measure 1]                                        %! SM4
                                    \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                                    \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                    \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                    R1 * 3/8
                                    ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                    % [ViolaMusicVoice measure 2]                                        %! SM4
                                    R1 * 3/8
                <BLANKLINE>
                                }
                            }
                            \tag Cello                                                                   %! ST4
                            \context CelloMusicStaff = "CelloMusicStaff"
                            {
                                \context CelloMusicVoice = "CelloMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [CelloMusicVoice measure 1]                                %! SM4
                                            \clef "bass"                                                 %! SM8:DEFAULT_CLEF:ST3
                                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override CelloMusicStaff.Clef.color = ##f                   %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set CelloMusicStaff.forceClef = ##t                         %! SM8:DEFAULT_CLEF:SM33:ST3
                                            a16
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Cello)                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)  %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            g16
                <BLANKLINE>
                                            \baca_octave_warning                                         %! SM12
                                            f16
                                            - \tweak color #red                                          %! SM12
                                            ^ \markup { OCTAVE }                                         %! SM12
                <BLANKLINE>
                                            e16
                <BLANKLINE>
                                            d16
                <BLANKLINE>
                                            c16
                                        }
                                    }
                <BLANKLINE>
                                    % [CelloMusicVoice measure 2]                                        %! SM4
                                    R1 * 3/8
                <BLANKLINE>
                                }
                            }
                        >>
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._color_octaves

    @property
    def color_out_of_range_pitches(self) -> typing.Optional[bool]:
        r"""
        Is true when segment-maker colors out-of-range pitches.

        ..  container:: example

            Colors out-of-range pitches:

            >>> music_maker = baca.MusicMaker()

            >>> collection_lists = [
            ...     [[4]],
            ...     [[-12, 2, 3, 5, 8, 9, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 10, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for i, collections in enumerate(collection_lists):
            ...     contribution = music_maker(
            ...         'Voice 1',
            ...         collections,
            ...         baca.flags(),
            ...         )
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     color_out_of_range_pitches=True,
            ...     ignore_out_of_range_pitches=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     ('MusicVoice', 1),
            ...     baca.instrument(abjad.Violin()),
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    autoBeaming = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 7/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 7/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        e'16
                                        ^ \markup {                                                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                            \with-color                                                  %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                                #(x11-color 'blue)                                       %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                                (Violin)                                                 %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                            }                                                            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        \baca_out_of_range_warning                                       %! SM13
                                        c16
                                        - \tweak color #red                                              %! SM13
                                        ^ \markup { * }                                                  %! SM13
                <BLANKLINE>
                                        d'16
                <BLANKLINE>
                                        ef'!16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                        af'!16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        c'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        b'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        bf'!16
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        bf'!16
                <BLANKLINE>
                                        c'16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._color_out_of_range_pitches

    @property
    def color_repeat_pitch_classes(self) -> typing.Optional[bool]:
        r"""
        Is true when segment-maker colors repeat pitch-classes.

        ..  container:: example

            Colors repeat pitch-classes:

            >>> music_maker = baca.MusicMaker()

            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 9, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 12, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for i, collections in enumerate(collection_lists):
            ...     contribution = music_maker(
            ...         'Voice 1',
            ...         collections,
            ...         baca.flags(),
            ...         )
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     color_repeat_pitch_classes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.HorizontalSpacingSpecifier(
            ...         minimum_duration=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     ('MusicVoice', 1),
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    autoBeaming = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 7/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 7/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        e'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        fs'!16
                <BLANKLINE>
                                        d'16
                <BLANKLINE>
                                        ef'!16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                        \baca_repeat_pitch_class_warning                                 %! SM14
                                        a'16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        \baca_repeat_pitch_class_warning                                 %! SM14
                                        a'16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        c'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        b'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        bf'!16
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        \baca_repeat_pitch_class_warning                                 %! SM14
                                        c''16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        \baca_repeat_pitch_class_warning                                 %! SM14
                                        c'16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._color_repeat_pitch_classes

    @property
    def commands(self) -> typing.List[scoping.Command]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def do_not_check_persistence(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker does not check persistent indicators.
        """
        return self._do_not_check_persistence

    @property
    def do_not_include_layout_ly(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker does not include layout.ly.
        """
        return self._do_not_include_layout_ly

    @property
    def fermata_measure_staff_line_count(self) -> typing.Optional[int]:
        """
        Gets fermata measure staff lines.
        """
        return self._fermata_measure_staff_line_count

    @property
    def final_bar_line(self) -> typing.Union[bool, str, None]:
        r"""
        Gets final bar line.

        ..  container:: example

            Nonlast segment sets final bar line to ``'|'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Override nonlast segment final bar line like this:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='||',
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "||"                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Last segment in score sets final bar line to ``'|.'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     last_segment=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|."                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Override last segment final bar line like this:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='||',
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> metadata = {'segment_count': 1}
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     metadata=metadata,
            ...     )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "||"                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._final_bar_line

    @property
    def final_markup(self) -> typing.Optional[tuple]:
        r"""
        Gets final markup.

        ..  container:: example

            Sets final markup:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='|.',
            ...     final_markup=(['Madison, WI'], ['October 2016']),
            ...     final_markup_extra_offset=(-9, -2),
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|."                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                \once \override TextScript.extra-offset = #'(-9 . -2)
                                c'8
                                _ \markup {                                                              %! SCORE2
                                    \override                                                            %! SCORE2
                                        #'(font-name . "Palatino")                                       %! SCORE2
                                        \with-color                                                      %! SCORE2
                                            #black                                                       %! SCORE2
                                            \right-column                                                %! SCORE2
                                                {                                                        %! SCORE2
                                                    \line                                                %! SCORE2
                                                        {                                                %! SCORE2
                                                            "Madison, WI"                                %! SCORE2
                                                        }                                                %! SCORE2
                                                    \line                                                %! SCORE2
                                                        {                                                %! SCORE2
                                                            "October 2016"                               %! SCORE2
                                                        }                                                %! SCORE2
                                                }                                                        %! SCORE2
                                    }                                                                    %! SCORE2
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._final_markup

    @property
    def final_markup_extra_offset(self) -> typing.Optional[typings.NumberPair]:
        """
        Gets final markup extra offset.
        """
        return self._final_markup_extra_offset

    @property
    def first_measure_number(self) -> typing.Optional[int]:
        """
        Gets user-defined first measure number.
        """
        return self._first_measure_number

    @property
    def first_segment(self) -> typing.Optional[bool]:
        """
        Is true when segment is first in score.
        """
        if self._first_segment is not None:
            return self._first_segment
        return self._get_segment_number() == 1
        
    @property
    def ignore_out_of_range_pitches(self) -> typing.Optional[bool]:
        """
        Is true when segment ignores out-of-range pitches.
        """
        return self._ignore_out_of_range_pitches

    @property
    def ignore_repeat_pitch_classes(self) -> typing.Optional[bool]:
        """
        Is true when segment ignores repeat pitch-classes.
        """
        return self._ignore_repeat_pitch_classes

    @property
    def ignore_unpitched_notes(self) -> typing.Optional[bool]:
        r"""
        Is true when segment ignores unpitched notes.

        ..  container:: example

            Ignores unpitched notes:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                                [
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Colors unpitched notes:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._ignore_unpitched_notes

    @property
    def ignore_unregistered_pitches(self) -> typing.Optional[bool]:
        r"""
        Is true when segment ignores unregistered pitches.

        ..  container:: example

            Ignores unregistered pitches:

                >>> music_maker = baca.MusicMaker(
                ...     baca.PitchFirstRhythmCommand(
                ...         rhythm_maker=baca.PitchFirstRhythmMaker(
                ...             acciaccatura_specifiers=[
                ...                 baca.AcciaccaturaSpecifier(),
                ...                 ],
                ...             talea=rmakers.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     color_unregistered_pitches=True,
                ...     denominator=8,
                ...     )

            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 8, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 8, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for collections in collection_lists:
            ...     contribution = music_maker('Voice 1', collections)
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     ignore_unregistered_pitches=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 3/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            s1 * 3/16
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        e'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            fs'16
                                            [                                                            %! ACC1
                <BLANKLINE>
                                            d'16
                <BLANKLINE>
                                            ef'16
                <BLANKLINE>
                                            f'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            af'16
                                            ]                                                            %! ACC1
                <BLANKLINE>
                                        }
                                        c'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        b'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            bf'16
                                            [                                                            %! ACC1
                <BLANKLINE>
                                            g'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            af'16
                <BLANKLINE>
                                            c'16
                                            ]                                                            %! ACC1
                <BLANKLINE>
                                        }
                                        f'8.
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Colors unregistered pitches:

                >>> music_maker = baca.MusicMaker(
                ...     baca.PitchFirstRhythmCommand(
                ...         rhythm_maker=baca.PitchFirstRhythmMaker(
                ...             acciaccatura_specifiers=[
                ...                 baca.AcciaccaturaSpecifier(),
                ...                 ],
                ...             talea=rmakers.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     color_unregistered_pitches=True,
                ...     denominator=8,
                ...     )

            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 8, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 8, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for collections in collection_lists:
            ...     contribution = music_maker('Voice 1', collections)
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 3/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            s1 * 3/16
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        \baca_unregistered_pitch_warning                                 %! SM25
                                        e'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            fs'16
                                            [                                                            %! ACC1
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            d'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            ef'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            f'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            a'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            af'16
                                            ]                                                            %! ACC1
                <BLANKLINE>
                                        }
                                        \baca_unregistered_pitch_warning                                 %! SM25
                                        c'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        \baca_unregistered_pitch_warning                                 %! SM25
                                        b'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            bf'16
                                            [                                                            %! ACC1
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            g'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            a'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            af'16
                <BLANKLINE>
                                            \baca_unregistered_pitch_warning                             %! SM25
                                            c'16
                                            ]                                                            %! ACC1
                <BLANKLINE>
                                        }
                                        \baca_unregistered_pitch_warning                                 %! SM25
                                        f'8.
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        """
        return self._ignore_unregistered_pitches

    @property
    def instruments(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets instruments.
        """
        return self._instruments

    @property
    def last_segment(self) -> typing.Optional[bool]:
        """
        Is true when composer declares segment to be last in score.
        """
        return self._last_segment

    @property
    def lilypond_file(self) -> typing.Optional[abjad.LilyPondFile]:
        """
        Gets LilyPond file.
        """
        return self._lilypond_file

    @property
    def magnify_staves(self) -> typing.Union[
        abjad.Multiplier,
        typing.Tuple[abjad.Multiplier, abjad.Tag],
        None,
        ]:
        """
        Gets staff magnification.
        """
        return self._magnify_staves

    @property
    def manifests(self) -> abjad.OrderedDict:
        """
        Gets manifests.
        """
        manifests = abjad.OrderedDict()
        manifests['abjad.Instrument'] = self.instruments
        manifests['abjad.MarginMarkup'] = self.margin_markups
        manifests['abjad.MetronomeMark'] = self.metronome_marks
        return manifests

    @property
    def margin_markups(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets margin markups.
        """
        return self._margin_markups

    @property
    def measure_count(self) -> int:
        """
        Gets measure count.
        """
        if self.time_signatures:
            return len(self.time_signatures)
        return 0

    @property
    def metadata(self) -> abjad.OrderedDict:
        r"""
        Gets segment metadata.

        ..  container:: example

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Clef',
            ...         value='alto',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )

            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "alto"                                                             %! SM8:REAPPLIED_CLEF:SM37
                                \once \override Staff.Clef.color = #(x11-color 'green4)                  %! SM6:REAPPLIED_CLEF_COLOR:SM37
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:REAPPLIED_CLEF_COLOR_CANCELLATION:SM37
                                \set Staff.forceClef = ##t                                               %! SM8:REAPPLIED_CLEF:SM33:SM37
                                R1 * 1/2
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)                     %! SM6:REAPPLIED_CLEF_REDRAW_COLOR:SM37
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> abjad.f(maker.metadata, strict=89)
            abjad.OrderedDict(
                [
                    (
                        'alive_during_segment',
                        [
                            'Score',
                            'GlobalContext',
                            'GlobalSkips',
                            'MusicContext',
                            'MusicStaff',
                            'MusicVoice',
                            ],
                        ),
                    ('first_measure_number', 1),
                    ('last_measure_number', 4),
                    (
                        'persistent_indicators',
                        abjad.OrderedDict(
                            [
                                (
                                    'MusicStaff',
                                    [
                                        abjad.Momento(
                                            context='MusicVoice',
                                            prototype='abjad.Clef',
                                            value='alto',
                                            ),
                                        ],
                                    ),
                                (
                                    'Score',
                                    [
                                        abjad.Momento(
                                            context='GlobalSkips',
                                            prototype='abjad.TimeSignature',
                                            value='3/8',
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ('segment_number', 2),
                    (
                        'sounds_during_segment',
                        abjad.OrderedDict(
                            [
                                ('MusicVoice', False),
                                ]
                            ),
                        ),
                    (
                        'time_signatures',
                        ['4/8', '3/8', '4/8', '3/8'],
                        ),
                    ]
                )

        """
        return self._metadata

    @property
    def metronome_marks(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets metronome marks.
        """
        return self._metronome_marks

    @property
    def midi(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker outputs MIDI.
        """
        return self._midi

    @property
    def nonfirst_segment_lilypond_include(self) -> typing.Optional[bool]:
        """
        Is true when nonfirst segment lilypond include appears in output file.
        """
        return self._nonfirst_segment_lilypond_include

    @property
    def previous_metadata(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets previous segment metadata.
        """
        return self._previous_metadata

    @property
    def score_template(self) -> typing.Optional[abjad.ScoreTemplate]:
        """
        Gets score template.

        ..  container:: example

            Gets score template:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     )

            >>> maker.score_template
            SingleStaffScoreTemplate()

        """
        return self._score_template

    @property
    def skip_wellformedness_checks(self) -> typing.Optional[bool]:
        """
        Is true when segment skips wellformedness checks.
        """
        return self._skip_wellformedness_checks

    @property
    def skips_instead_of_rests(self) -> typing.Optional[bool]:
        r"""
        Is true when segment fills empty measures with skips.

        ..  container:: example

            Fills empty measures with multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Fills empty measures with skips:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     skips_instead_of_rests=True,
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                s1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                s1 * 3/8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                s1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                s1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._skips_instead_of_rests

    @property
    def spacing(self) -> typing.Optional[segmentclasses.HorizontalSpacingSpecifier]:
        """
        Gets spacing.
        """
        return self._spacing

    @property
    def test_container_identifiers(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker adds container identifiers in docs
        environment.
        """
        return self._test_container_identifiers

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    @property
    def transpose_score(self) -> typing.Optional[bool]:
        r"""
        Is true when segment transposes score.

        ..  container:: example

            Transposes score:

            >>> instruments = abjad.OrderedDict()
            >>> instruments['clarinet'] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=True,
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.instrument(instruments['clarinet']),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                fs'!8
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“clarinet”)                                                     %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                fs'!8
                <BLANKLINE>
                                g'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                fs'!8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                fs'!8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                g'8
                                [
                <BLANKLINE>
                                fs'!8
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                fs'!8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                g'8
                                [
                <BLANKLINE>
                                fs'!8
                <BLANKLINE>
                                g'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Does not transpose score:

            >>> instruments = abjad.OrderedDict()
            >>> instruments['clarinet'] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=False,
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.instrument(instruments['clarinet']),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color "blue"                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                e'8
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“clarinet”)                                                     %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                [
                <BLANKLINE>
                                f'8
                <BLANKLINE>
                                e'8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                e'8
                                [
                <BLANKLINE>
                                f'8
                <BLANKLINE>
                                e'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                f'8
                                [
                <BLANKLINE>
                                e'8
                <BLANKLINE>
                                f'8
                <BLANKLINE>
                                e'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                f'8
                                [
                <BLANKLINE>
                                e'8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._transpose_score

    @property
    def validate_measure_count(self) -> typing.Optional[int]:
        """
        Gets validate measure count.

        ..  container:: example

            Raises exception when measures found do not equal validate count:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     validate_measure_count=6,
            ...     )
            Traceback (most recent call last):
                ...
            Exception: found 4 measures (not 6).

        """
        return self._validate_measure_count
    
    @property
    def voice_metadata(self) -> abjad.OrderedDict:
        """
        Gets voice metadata.
        """
        return self._voice_metadata

    ### PUBLIC METHODS ###

    def run(
        self,
        deactivate: typing.List[str] = None,
        environment: str = None,
        metadata: abjad.OrderedDict = None,
        midi: bool = None,
        previous_metadata: abjad.OrderedDict = None,
        remove: typing.List[str] = None,
        segment_directory: abjad.Path = None,
        ) -> abjad.LilyPondFile:
        """
        Runs segment-maker.

        :param deactivate: tags to deactivate in LilyPond file output.

        :param environment: stylesheet path control parameter. Leave set to
            none to render segments in real score.
            Set to ``'docs'`` for API examples.
            Set to ``'external'`` to debug API examples in a separate file.

        :param metadata: metadata found in current segment directory.

        :param midi: set to true to generate MIDI output.

        :param previous_metadata: metadata found in previous segment directory.

        :param remove: tags to remove in LilyPond file output.

        :param segment_directory: path providing access to current segment
            directory.

        """
        self._environment = environment
        self._metadata: abjad.OrderedDict = abjad.OrderedDict(metadata)
        self._midi = midi
        self._previous_metadata = abjad.OrderedDict(previous_metadata)
        self._segment_directory = segment_directory
        self._import_manifests()
        with abjad.Timer() as timer:
            self._make_score()
            self._make_lilypond_file()
            self._make_global_skips()
            self._label_measure_indices()
            self._label_stage_numbers()
        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            print(f'  Score initialization {count} {seconds} ...')

        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                command_count = self._call_rhythm_commands()
        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            message = f'  Rhythm commands {count} {seconds}'
            message += f' [for {command_count} commands] ...'
            print(message)

        with abjad.Timer() as timer:
            self._populate_offset_to_measure_number()
            self._extend_beams()
            self._annotate_sounds_during()
            self._attach_first_segment_score_template_defaults()
            self._reapply_persistent_indicators()
            self._attach_first_appearance_score_template_defaults()
            self._apply_spacing()
        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            print(f'  After-rhythm commands {count} {seconds} ...')

        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                command_count = self._call_commands()
        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            message = f'  Nonrhythm commands {count} {seconds}'
            message += f' [for {command_count} commands] ...'
            print(message)

        # TODO: optimize by consolidating score iteration:
        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                self._remove_redundant_time_signatures()
                self._cache_fermata_measure_numbers()
                self._shorten_long_repeat_ties()
                self._treat_untreated_persistent_wrappers()
                self._attach_metronome_mark_text_span_indicators()
                self._transpose_score_()
                self._add_final_bar_line()
                self._add_final_markup()
                self._color_unregistered_pitches()
                self._color_unpitched_notes()
                self._check_wellformedness()
                self._check_range()
                self._check_persistent_indicators()
                self._color_repeat_pitch_classes_()
                self._color_octaves_()
                self._force_nonnatural_accidentals()
                self._magnify_staves_()
                self._whitespace_leaves()
                self._comment_measure_numbers()
                self._apply_breaks()
                self._parallelize_multimeasure_rests()
                self._style_fermata_measures()
                self._shift_clefs_into_fermata_measures()
                self._deactivate_tags(deactivate or [])
                self._remove_tags(remove)
                self._add_container_identifiers()
                self._check_all_music_in_part_containers()
                self._check_duplicate_part_assignments()
                self._collect_metadata()

        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            print(f'  Postprocessing {count} {seconds} ...')

        with abjad.Timer() as timer:
            method = getattr(self.score, '_update_now')
            method(offsets_in_seconds=True)
        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            print(f'  Offsets-in-seconds update {count} {seconds} ...')

        with abjad.Timer() as timer:
            self._label_clock_time()
        count = int(timer.elapsed_time)
        seconds = abjad.String('second').pluralize(count)
        if self.environment != 'docs':
            print(f'  Clocktime markup {count} {seconds} ...')

        assert isinstance(self.lilypond_file, abjad.LilyPondFile)
        return self.lilypond_file

class WellformednessManager(abjad.WellformednessManager):
    """
    Wellformedness manager.

    ..  container:: example

        >>> baca.WellformednessManager()
        WellformednessManager()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allow_percussion_clef=None,
        ):
        abjad.WellformednessManager.__init__(
            self,
            allow_percussion_clef=allow_percussion_clef,
            )

    ### SPECIAL METHODS ###

    def __call__(
        self,
        argument: typing.Union[abjad.Score, None] = None,
        ) -> typing.List[typing.Tuple[list, int, str]]:
        r"""
        Calls wellformedness checks on ``argument``.

        :param argument: input score.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> manager = baca.WellformednessManager()
            >>> result = manager(voice)
            >>> for violators, total, check in result:
            ...     print(check)
            ...     print(total)
            ...     print(violators)
            ...     print()
            check_discontiguous_spanners
            0
            []
            <BLANKLINE>
            check_duplicate_ids
            5
            []
            <BLANKLINE>
            check_empty_containers
            1
            []
            <BLANKLINE>
            check_misdurated_measures
            0
            []
            <BLANKLINE>
            check_misfilled_measures
            0
            []
            <BLANKLINE>
            check_mismatched_enchained_hairpins
            0
            []
            <BLANKLINE>
            check_mispitched_ties
            0
            []
            <BLANKLINE>
            check_misrepresented_flags
            4
            []
            <BLANKLINE>
            check_missing_parents
            5
            []
            <BLANKLINE>
            check_nested_measures
            0
            []
            <BLANKLINE>
            check_notes_on_wrong_clef
            4
            []
            <BLANKLINE>
            check_out_of_range_notes
            4
            []
            <BLANKLINE>
            check_overlapping_beams
            0
            []
            <BLANKLINE>
            check_overlapping_glissandi
            0
            set()
            <BLANKLINE>
            check_overlapping_hairpins
            0
            set()
            <BLANKLINE>
            check_overlapping_octavation_spanners
            0
            []
            <BLANKLINE>
            check_overlapping_ties
            0
            []
            <BLANKLINE>
            check_overlapping_trill_spanners
            0
            set()
            <BLANKLINE>
            check_repeat_pitch_classes
            4
            [LogicalTie([Note("c'4")]), LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")]), LogicalTie([Note("d'4")])]
            <BLANKLINE>
            check_tied_rests
            0
            []
            <BLANKLINE>

        Returns (violators, total, check) triples.
        """
        triples: list = []
        if argument is None:
            return triples
        names = [_ for _ in dir(self) if _.startswith('check_')]
        for name in sorted(names):
            check = getattr(self, name)
            violators, total = check(argument=argument)
            triples.append((violators, total, name))
        return triples

    ### PRIVATE METHODS ###

    @staticmethod
    def _find_repeat_pitch_classes(argument):
        violators = []
        for voice in abjad.iterate(argument).components(abjad.Voice):
            previous_lt, previous_pcs = None, []
            for lt in abjad.iterate(voice).logical_ties():
                if isinstance(lt.head, abjad.Note):
                    written_pitches = [lt.head.written_pitch]
                elif isinstance(lt.head, abjad.Chord):
                    written_pitches = lt.head.written_pitches
                else:
                    written_pitches = []
                pcs = [_.pitch_class for _ in written_pitches]
                inspection = abjad.inspect(lt.head)
                if (inspection.has_indicator(abjad.tags.NOT_YET_PITCHED) or
                    inspection.has_indicator(abjad.tags.ALLOW_REPEAT_PITCH)):
                    pass
                elif set(pcs) & set(previous_pcs):
                    if previous_lt not in violators:
                        violators.append(previous_lt)
                    if lt not in violators:
                        violators.append(lt)
                previous_lt = lt
                previous_pcs = pcs
        return violators

    ### PUBLIC METHODS ###

    @staticmethod
    def check_repeat_pitch_classes(argument=None):
        r"""
        Checks repeat pitch-classes by voice.

        ..  container:: example

            Finds no repeats:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> abjad.show(voice, strict=89) # doctest: +SKIP

            >>> manager = baca.WellformednessManager
            >>> manager.check_repeat_pitch_classes(voice)
            ([], 4)

        ..  container:: example

            Finds repeat pitches:

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> abjad.show(voice, strict=89) # doctest: +SKIP

            >>> manager = baca.WellformednessManager
            >>> manager.check_repeat_pitch_classes(voice)
            ([LogicalTie([Note("c'4")]), LogicalTie([Note("c'4")]), LogicalTie([Note("d'4")]), LogicalTie([Note("d'4")])], 4)

        ..  container:: example

            Finds repeat pitch-classes:

            >>> voice = abjad.Voice("c'4 d' e' e''")
            >>> abjad.show(voice, strict=89) # doctest: +SKIP

            >>> manager = baca.WellformednessManager
            >>> manager.check_repeat_pitch_classes(voice)
            ([LogicalTie([Note("e'4")]), LogicalTie([Note("e''4")])], 4)

        Returns violators and total.
        """
        total = len(classes.Selection(argument).plts())
        violators = WellformednessManager._find_repeat_pitch_classes(argument)
        return violators, total

    def is_well_formed(self, argument=None):
        r"""
        Is true when ``argument`` is well-formed.

        ..  container:: example

            Is well-formed:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> manager = baca.WellformednessManager()
            >>> manager.is_well_formed(voice)
            True

        ..  container:: example

            Repeat pitches are not well-formed:

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> manager = baca.WellformednessManager()
            >>> manager.is_well_formed(voice)
            False

        Returns true or false.
        """
        triples = self(argument)
        for violators, total, check_name in triples:
            if violators:
                return False
        return True

    def tabulate_wellformedness(self, argument=None):
        """
        Tabulates wellformedness violations.

        ..  container:: example

            Is well-formed:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> manager = baca.WellformednessManager()
            >>> string = manager.tabulate_wellformedness(voice)
            >>> print(string)
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 /	0 overlapping trill spanners
            0 /	4 repeat pitch classes
            0 /	0 tied rests

        ..  container:: example

            Repeat pitches are not well-formed:

            >>> voice = abjad.Voice("c'4 c' d' d'")
            >>> manager = baca.WellformednessManager()
            >>> string = manager.tabulate_wellformedness(voice)
            >>> print(string)
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 /	0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 /	0 overlapping trill spanners
            4 /	4 repeat pitch classes
            0 /	0 tied rests

        Returns string.
        """
        triples = self(argument)
        strings = []
        for violators, total, check_name in triples:
            count = len(violators)
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = f'{count} /\t{total} {check_name}'
            strings.append(string)
        return '\n'.join(strings)
