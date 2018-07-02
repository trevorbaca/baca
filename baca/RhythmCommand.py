import abjad
import baca
import collections
import typing
from abjadext import rmakers
from . import typings
from .Command import Command
from .DivisionMaker import DivisionMaker
rhythm_maker_type = (
    rmakers.RhythmMaker,
    abjad.Selection,
    )


class RhythmCommand(Command):
    r"""
    Rhythm command.

    >>> from abjadext import rmakers

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (4, 8), (3,8), (4, 8)],
        ...     )

        >>> command = baca.RhythmCommand(
        ...     rhythm_maker=rmakers.EvenDivisionRhythmMaker(
        ...         tuplet_specifier=rmakers.TupletSpecifier(
        ...             extract_trivial=True,
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     command,
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \override Score.BarLine.transparent = ##f                                    %! SM5
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

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_maker',
        '_division_expression',
        '_left_broken',
        '_multimeasure_rests',
        '_payload',
        '_persist',
        '_reference_meters',
        '_rewrite_meter',
        '_rewrite_rest_filled',
        '_rhythm_maker',
        '_right_broken',
        '_split_at_measure_boundaries',
        '_stages',
        '_state',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        division_maker: DivisionMaker = None,
        division_expression: abjad.Expression = None,
        left_broken: bool = None,
        multimeasure_rests: bool = None,
        persist: str = None,
        reference_meters: typing.Iterable[abjad.Meter] = None,
        rewrite_meter: bool = None,
        rewrite_rest_filled: bool = None,
        rhythm_maker: typings.RhythmMakerTyping = None,
        right_broken: bool = None,
        split_at_measure_boundaries: bool = None,
        stages: typing.Tuple[int, int] = None,
        ) -> None:
        Command.__init__(self)
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += f':\n{division_expression} {division_maker}.'
            raise Exception(message)
        if division_maker is not None:
            assert isinstance(division_maker, typings.division_maker_type), repr(division_maker)
        self._division_maker = division_maker
        if division_expression is not None:
            assert isinstance(division_expression, abjad.Expression)
        self._division_expression = division_expression
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if multimeasure_rests is not None:
            multimeasure_rests = bool(multimeasure_rests)
        self._multimeasure_rests = multimeasure_rests
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        if reference_meters is not None:
            assert isinstance(reference_meters, collections.Iterable)
            assert all(isinstance(_, abjad.Meter) for _ in reference_meters)
        self._reference_meters = reference_meters
        if rewrite_meter is not None:
            rewrite_meter = bool(rewrite_meter)
        self._rewrite_meter = rewrite_meter
        if rewrite_rest_filled is not None:
            rewrite_rest_filled = bool(rewrite_rest_filled)
        self._rewrite_rest_filled = rewrite_rest_filled
        self._check_rhythm_maker_input(rhythm_maker)
        self._rhythm_maker = rhythm_maker
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        if split_at_measure_boundaries is not None:
            split_at_measure_boundaries = bool(split_at_measure_boundaries)
        self._split_at_measure_boundaries = split_at_measure_boundaries
        if stages is not None:
            assert isinstance(stages, tuple), repr(stages)
            assert len(stages) == 2, repr(stages)
        self._stages = stages
        self._state: typing.Optional[abjad.OrderedDict] = None

    ### SPECIAL METHODS ###

    def __call__(
        self,
        start_offset: abjad.Offset = None,
        time_signatures: typing.Iterable[abjad.TimeSignature] = None,
        ) -> None:
        """
        Calls command on ``start_offset`` and ``time_signatures``.
        """
        music, start_offset = self._make_rhythm(start_offset, time_signatures)
        assert isinstance(music, (tuple, list, abjad.Voice))
        first_leaf = abjad.inspect(music).get_leaf(0)
        last_leaf = abjad.inspect(music).get_leaf(-1)
        pitched_prototype = (abjad.Note, abjad.Chord)
        payload = abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=None,
            annotation=music,
            )
        self._payload = payload

    ### PRIVATE METHODS ###

    @staticmethod
    def _annotate_unpitched_notes(argument):
        rest_prototype = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        for leaf in abjad.iterate(argument).leaves():
            if isinstance(leaf, abjad.Chord):
                message = f'rhythm-makers make only notes and rests: {leaf!r}.'
                raise Exception(message)
            elif isinstance(leaf, abjad.Note):
                abjad.attach(abjad.tags.NOT_YET_PITCHED, leaf, tag=None)
            elif isinstance(leaf, rest_prototype):
                pass
            else:
                raise TypeError(leaf)

    def _apply_division_expression(
        self,
        divisions,
        ) -> typing.Optional[abjad.Sequence]:
        if self.division_expression is not None:
            divisions_ = self.division_expression(divisions)
            if not isinstance(divisions_, abjad.Sequence):
                message = 'division expression must return sequence:\n'
                message += f'  Input divisions:\n'
                message += f'    {divisions}\n'
                message += f'  Division expression:\n'
                message += f'    {self.division_expression}\n'
                message += f'  Output divisions:\n'
                message += f'    {divisions_}'
                raise Exception(message)
            divisions = divisions_
        return divisions

    def _check_rhythm_maker_input(self, rhythm_maker):
        if rhythm_maker is None:
            return
        prototype = (abjad.Selection, rmakers.RhythmMaker)
        if isinstance(rhythm_maker, prototype):
            return
        if not self._check_rhythm_maker_pattern_pairs(rhythm_maker):
            message = "\n  Input parameter 'rhythm_maker' accepts:"
            message += '\n    rhythm-maker'
            message += '\n    selection'
            message += '\n    sequence of (rhythm-maker-or-selection, pattern) pairs'
            message += '\n    none'
            message += "\n  Input parameter 'rhythm_maker' received:"
            message += f'\n    {format(rhythm_maker)}'
            raise Exception(message)

    def _check_rhythm_maker_pattern_pairs(self, pairs):
        if not isinstance(pairs, collections.Sequence): 
            return False
        prototype = (abjad.Selection, rmakers.RhythmMaker, type(self))
        for pair in pairs:
            if not isinstance(pair, tuple) or len(pair) != 2:
                return False
            if not isinstance(pair[0], prototype):
                return False
            if pair[1] is True:
                return True
            if not isinstance(pair[1], (list, tuple, abjad.Pattern)):
                return False
        return True

    @staticmethod
    def _durations_to_divisions(durations, start_offset):
        divisions = [baca.Division(_) for _ in durations]
        durations = [_.duration for _ in divisions]
        start_offset = abjad.Offset(start_offset)
        durations.insert(0, start_offset)
        start_offsets = abjad.mathtools.cumulative_sums(durations)[1:-1]
        assert len(divisions) == len(start_offsets)
        divisions_ = []
        for division, start_offset in zip(divisions, start_offsets):
            division_ = baca.Division(
                division,
                start_offset=start_offset,
                )
            divisions_.append(division_)
        assert not any(_.start_offset is None for _ in divisions_)
        return divisions_

    def _make_rhythm(self, start_offset, time_signatures):
        rhythm_maker = self.rhythm_maker
        literal_selections = False
        if rhythm_maker is None:
            mask = rmakers.silence([0], 1, use_multimeasure_rests=True)
            rhythm_maker = rmakers.NoteRhythmMaker(division_masks=[mask])
        if isinstance(rhythm_maker, abjad.Selection):
            selections = [rhythm_maker]
            literal_selections = True
        else:
            if isinstance(rhythm_maker, rmakers.RhythmMaker):
                pairs = [(rhythm_maker, abjad.index([0], 1))]
            else:
                pairs = list(rhythm_maker)
            assert self._check_rhythm_maker_pattern_pairs(pairs)
            division_maker = self.division_maker
            if division_maker is None:
                division_maker = DivisionMaker()
            divisions = self._durations_to_divisions(
                time_signatures,
                start_offset,
                )
            divisions = division_maker(divisions)
            divisions = baca.sequence(divisions).flatten(depth=-1)
            divisions = self._apply_division_expression(divisions)
            division_count = len(divisions)
            start_offset = divisions[0].start_offset
            labelled_divisions = []
            for i, division in enumerate(divisions):
                for pair in pairs:
                    rhythm_maker, pattern = pair
                    if pattern is True:
                        pattern = abjad.index([0], 1)
                    if isinstance(pattern, list):
                        indices = pattern
                        pattern = abjad.index(indices)
                    elif isinstance(pattern, tuple):
                        triple = slice(*pattern).indices(division_count)
                        indices = list(range(*triple))
                        pattern = abjad.index(indices)
                    if pattern.matches_index(i, division_count):
                        labelled_divisions.append((division, rhythm_maker))
                        break
                else:
                    raise Exception(f'no rhythm-maker for division {i}.')
            assert len(labelled_divisions) == len(divisions)
            labelled_divisions = baca.sequence(labelled_divisions)
            labelled_divisions = labelled_divisions.group_by(
                lambda pair: pair[1],
                )
            selections = []
            previous_segment_stop_state = self._previous_segment_stop_state()
            maker_to_state = abjad.OrderedDict()
            for subsequence in labelled_divisions:
                divisions_ = [pair[0] for pair in subsequence]
                rhythm_maker = subsequence[0][1]
                if isinstance(rhythm_maker, type(self)):
                    rhythm_maker = rhythm_maker.rhythm_maker
                    assert isinstance(rhythm_maker, rmakers.RhythmMaker)
                # TODO: eventually allow previous segment stop state
                #       and local stop state to work together
                if previous_segment_stop_state is None:
                    previous_state = maker_to_state.get(rhythm_maker, None)
                else:
                    previous_state = previous_segment_stop_state
                selections_ = rhythm_maker(
                    divisions_,
                    previous_state=previous_state,
                    )
                maker_to_state[rhythm_maker] = rhythm_maker.state
                selections.extend(selections_)
            self._state = rhythm_maker.state
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        if self.split_at_measure_boundaries:
            specifier = rmakers.DurationSpecifier
            selections = specifier._split_at_measure_boundaries(
                selections,
                time_signatures,
                repeat_ties=self.repeat_ties,
                )
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        if self.rewrite_meter:
            selections = rmakers.DurationSpecifier._rewrite_meter_(
                selections,
                time_signatures,
                reference_meters=self.reference_meters,
                rewrite_tuplets=False,
                repeat_ties=self.repeat_ties,
                )
        if self.rewrite_rest_filled:
            selections = rmakers.DurationSpecifier._rewrite_rest_filled_(
                selections,
                multimeasure_rests=self.multimeasure_rests,
                )
        self._tag_broken_ties(selections)
        if not literal_selections:
            self._annotate_unpitched_notes(selections)
        return selections, start_offset

    def _previous_segment_stop_state(self):
        previous_segment_stop_state = None
        dictionary = self.runtime.get('previous_segment_voice_metadata')
        if dictionary:
            previous_segment_stop_state = dictionary.get(abjad.tags.RHYTHM)
            if previous_segment_stop_state.get('name') != self.persist:
                previous_segment_stop_state = None
        return previous_segment_stop_state

    def _tag_broken_ties(self, selections):
        if not isinstance(self.rhythm_maker, rmakers.RhythmMaker):
            return
        if (self.left_broken and
            self.rhythm_maker.previous_state.get('incomplete_last_note')):
            if not self.repeat_ties:
                raise Exception('left-broken ties must be repeat ties.')
            first_leaf = abjad.select(selections).leaf(0)
            if isinstance(first_leaf, abjad.Note):
                abjad.attach(abjad.tags.LEFT_BROKEN_REPEAT_TIE_TO, first_leaf)
        if (self.right_broken and
            self.rhythm_maker.state.get('incomplete_last_note')):
            if self.repeat_ties:
                raise Exception('right-broken ties must be conventional.')
            last_leaf = abjad.select(selections).leaf(-1)
            if isinstance(last_leaf, abjad.Note):
                abjad.attach(abjad.tags.RIGHT_BROKEN_TIE_FROM, last_leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def division_expression(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets division expression.

        ..  container:: example

            Sums divisions:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (4, 8), (3, 8), (4, 8)],
            ...     )

            >>> command = baca.RhythmCommand(
            ...     division_expression=abjad.sequence().sum().sequence(),
            ...     rhythm_maker=rmakers.EvenDivisionRhythmMaker(
            ...         tuplet_specifier=rmakers.TupletSpecifier(
            ...             extract_trivial=True,
            ...             ),
            ...         ),
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     command,
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
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
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
                            }
                        }
                    >>
                >>

        """
        return self._division_expression

    @property
    def division_maker(self) -> typing.Optional[typings.DivisionMakerTyping]:
        """
        Gets division-maker.
        """
        return self._division_maker

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when rhythm is left-broken.
        """
        return self._left_broken

    @property
    def multimeasure_rests(self) -> typing.Optional[bool]:
        """
        Is true when command spells each rest-filled division as a
        single multimeasure rest.
        """
        return self._multimeasure_rests

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.RhythmCommand().parameter
            'RHYTHM'

        """
        return abjad.tags.RHYTHM

    @property
    def payload(self) -> abjad.AnnotatedTimespan:
        """
        Gets payload.
        """
        return self._payload

    @property
    def persist(self) -> typing.Optional[str]:
        """
        Gets persist name.
        """
        return self._persist

    @property
    def reference_meters(self) -> typing.Optional[
        typing.Iterable[abjad.Meter]
        ]:
        """
        Gets reference meters.

        Only used to rewrite meters.
        """
        return self._reference_meters

    @property
    def repeat_ties(self) -> typing.Optional[bool]:
        tie_specifier = getattr(self.rhythm_maker, 'tie_specifier', None)
        if tie_specifier is None:
            return False
        return tie_specifier.repeat_ties

    @property
    def rewrite_meter(self) -> typing.Optional[bool]:
        r"""
        Is true when command rewrites meter.

        ..  container:: example

            REGRESSION. All notes below are tagged unpitched (and colored
            gold), even tied notes resulting from meter rewriting:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(10, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_repeat_tied_notes(),
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
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 10/8                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 5/4
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                c'4.
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                \repeatTie
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4.
                                \repeatTie
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                \repeatTie
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._rewrite_meter

    @property
    def rewrite_rest_filled(self) -> typing.Optional[bool]:
        """
        Is true when command rewrites rest-filled divisions.
        """
        return self._rewrite_rest_filled

    @property
    def rhythm_maker(self) -> typing.Optional[typings.RhythmMakerTyping]:
        r"""
        Gets rhythm-maker-or-selection or (rhythm-maker-or-selection, pattern)
        pairs.

        ..  container:: example

            Talea rhythm-maker remembers previous state across divisions:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=5 * [(4, 8)],
            ...     )

            >>> rhythm_maker_1 = rmakers.NoteRhythmMaker(
            ...     division_masks=[rmakers.silence([0], 1)],
            ...     )
            >>> rhythm_maker_2 = rmakers.TaleaRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[3, 4],
            ...         denominator=16,
            ...         ),
            ...     )
            >>> command = baca.RhythmCommand(
            ...     rhythm_maker=[
            ...         (rhythm_maker_1, [2]),
            ...         (rhythm_maker_2, True),
            ...         ],
            ...     )

            >>> label = abjad.label().with_durations(
            ...     direction=abjad.Down,
            ...     denominator=16,
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.label(label),
            ...     baca.text_script_font_size(-2),
            ...     baca.text_script_staff_padding(5),
            ...     command,
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
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                \override TextScript.font-size = #-2                                     %! OC1
                                \override TextScript.staff-padding = #5                                  %! OC1
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'16
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                ~
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                _ \markup {
                                    \fraction
                                        2
                                        16
                                    }
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                r2
                                _ \markup {
                                    \fraction
                                        8
                                        16
                                    }
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                                ]
                                \revert TextScript.font-size                                             %! OC2
                                \revert TextScript.staff-padding                                         %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on invalid input:

            >>> command = baca.RhythmCommand(
            ...     rhythm_maker='text',
            ...     )
            Traceback (most recent call last):
                ...
            Exception:
              Input parameter 'rhythm_maker' accepts:
                rhythm-maker
                selection
                sequence of (rhythm-maker-or-selection, pattern) pairs
                none
              Input parameter 'rhythm_maker' received:
                text

        """
        return self._rhythm_maker

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when rhythm is right-broken.
        """
        return self._right_broken

    @property
    def split_at_measure_boundaries(self) -> typing.Optional[bool]:
        """
        Is true when command splits at measure boundaries.
        """
        return self._split_at_measure_boundaries

    @property
    def stages(self) -> typing.Optional[typing.Tuple[int, int]]:
        """
        Gets stages.
        """
        return self._stages

    @property
    def state(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state
