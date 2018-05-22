import abjad
import baca
import collections
import typing
from abjad import rhythmos as rhythmos
from .Command import Command
from .DivisionMaker import DivisionMaker
from .FlattenDivisionCallback import FlattenDivisionCallback
from .FuseByCountsDivisionCallback import FuseByCountsDivisionCallback
from .PartitionDivisionCallback import PartitionDivisionCallback
from .SplitByDurationsDivisionCallback import SplitByDurationsDivisionCallback
from .SplitByRoundedRatiosDivisionCallback import \
    SplitByRoundedRatiosDivisionCallback
division_maker_type = (
    DivisionMaker,
    FlattenDivisionCallback,
    FuseByCountsDivisionCallback,
    PartitionDivisionCallback,
    SplitByDurationsDivisionCallback,
    SplitByRoundedRatiosDivisionCallback,
    )
division_maker_typing = typing.Union[
    DivisionMaker,
    FlattenDivisionCallback,
    FuseByCountsDivisionCallback,
    PartitionDivisionCallback,
    SplitByDurationsDivisionCallback,
    SplitByRoundedRatiosDivisionCallback,
    ]
rhythm_maker_type = (
    rhythmos.RhythmMaker,
    abjad.Selection,
    )
rhythm_maker_typing = typing.Union[
    rhythmos.RhythmMaker,
    abjad.Selection,
    typing.Iterable[
        typing.Tuple[
            typing.Union[
                rhythmos.RhythmMaker,
                abjad.Selection,
                ],
            abjad.Pattern,
            ],
        ],
    ]


class RhythmCommand(Command):
    r"""
    Rhythm command.

    >>> from abjad import rhythmos as rhythmos

    ..  container:: example

        >>> command = baca.RhythmCommand(
        ...     rhythm_maker=rhythmos.NoteRhythmMaker(),
        ...     )

    ..  container:: example

        >>> command = baca.RhythmCommand(
        ...     division_expression=abjad.sequence().sum().sequence(),
        ...     rhythm_maker=rhythmos.NoteRhythmMaker(),
        ...     )

    ..  container:: example

        >>> rhythm_maker_1 = rhythmos.NoteRhythmMaker()
        >>> rhythm_maker_2 = rhythmos.EvenRunRhythmMaker()
        >>> command = baca.RhythmCommand(
        ...     rhythm_maker=[
        ...         (rhythm_maker_1, abjad.index([0], 2)),
        ...         (rhythm_maker_2, abjad.index([1], 2)),
        ...         ],
        ...     )

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
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
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                \makeBlue                                                            %! SM24
                                c'8
                                [
            <BLANKLINE>
                                \makeBlue                                                            %! SM24
                                c'8
            <BLANKLINE>
                                \makeBlue                                                            %! SM24
                                c'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                \makeBlue                                                            %! SM24
                                c'8
                                [
            <BLANKLINE>
                                \makeBlue                                                            %! SM24
                                c'8
            <BLANKLINE>
                                \makeBlue                                                            %! SM24
                                c'8
                                ]
                            }
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \makeBlue                                                                %! SM24
                            c'4.
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                \makeBlue                                                            %! SM24
                                c'8
                                [
            <BLANKLINE>
                                \makeBlue                                                            %! SM24
                                c'8
            <BLANKLINE>
                                \makeBlue                                                            %! SM24
                                c'8
                                ]
                            }
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
                            \makeBlue                                                                %! SM24
                            c'4.
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
        '_persist',
        '_reference_meters',
        '_rewrite_meter',
        '_rewrite_rest_filled',
        '_rhythm_maker',
        '_rhythm_overwrites',
        '_right_broken',
        '_split_at_measure_boundaries',
        '_stages',
        '_state',
        '_tie_first',
        '_tie_last',
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
        rhythm_overwrites: typing.List[tuple] = None,
        rhythm_maker: rhythm_maker_typing = None,
        right_broken: bool = None,
        split_at_measure_boundaries: bool = None,
        stages: typing.Tuple[int, int] = None,
        tie_first: bool = None,
        tie_last: bool = None,
        ) -> None:
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += f':\n{division_expression} {division_maker}.'
            raise Exception(message)
        if division_maker is not None:
            assert isinstance(division_maker, division_maker_type), repr(division_maker)
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
        prototype = (rhythmos.RhythmMaker, abjad.Selection, type(None))
        if not isinstance(rhythm_maker, prototype):
            assert isinstance(rhythm_maker, collections.Iterable), repr(rhythm_maker)
            for pair in rhythm_maker:
                assert isinstance(pair, tuple), repr(pair)
                assert len(pair) == 2, repr(pair)
                rhythm_maker_, pattern = pair
                assert isinstance(rhythm_maker_, rhythm_maker_type)
                assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._rhythm_maker = rhythm_maker
        if rhythm_overwrites is not None:
            assert isinstance(rhythm_overwrites, list)
            assert all(isinstance(_, tuple) for _ in rhythm_overwrites)
        self._rhythm_overwrites = rhythm_overwrites
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
        if tie_first is not None:
            tie_first = bool(tie_first)
        self._tie_first = tie_first
        if tie_last is not None:
            tie_last = bool(tie_last)
        self._tie_last = tie_last

    ### SPECIAL METHODS ###

    def __call__(
        self,
        start_offset: abjad.Offset = None,
        time_signatures: typing.Iterable[abjad.TimeSignature] = None,
        ) -> abjad.AnnotatedTimespan:
        """
        Calls command on ``start_offset`` and ``time_signatures``.
        """
        music, start_offset = self._make_rhythm(start_offset, time_signatures)
        assert isinstance(music, (tuple, list, abjad.Voice))
        first_leaf = abjad.inspect(music).get_leaf(0)
        last_leaf = abjad.inspect(music).get_leaf(-1)
        pitched_prototype = (abjad.Note, abjad.Chord)
        if self.tie_first and isinstance(first_leaf, pitched_prototype):
            abjad.attach(abjad.tags.TIE_TO, first_leaf)
            if self.repeat_ties:
                abjad.attach(abjad.tags.REPEAT_TIE, first_leaf)
        if self.tie_last and isinstance(last_leaf, pitched_prototype):
            abjad.attach(abjad.tags.TIE_FROM, last_leaf)
            if self.repeat_ties:
                abjad.attach(abjad.tags.REPEAT_TIE, last_leaf)
        return abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=None,
            annotation=music,
            )

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

    def _get_storage_format_specification(self):
        agent = abjad.StorageFormatManager(self)
        keyword_argument_names = agent.signature_keyword_names
        if not self.rhythm_overwrites:
            keyword_argument_names = list(keyword_argument_names)
            keyword_argument_names.remove('rhythm_overwrites')
        return abjad.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    def _handle_rhythm_overwrites(self, time_signatures, selections):
        if not self.rhythm_overwrites:
            selections
        maker = abjad.MeasureMaker()
        dummy_measures = maker(time_signatures)
        dummy_time_signature_voice = abjad.Voice(dummy_measures)
        dummy_music_voice = abjad.Voice()
        dummy_music_voice.extend(selections)
        dummy_staff = abjad.Staff([
            dummy_time_signature_voice,
            dummy_music_voice,
            ])
        dummy_staff.is_simultaneous = True
        assert len(self.rhythm_overwrites) == 1, repr(self.rhythm_overwrites)
        selector, division_maker, rhythm_maker = self.rhythm_overwrites[0]
        old_selection = selector(dummy_music_voice)
        old_selection = abjad.select(old_selection)
        result = old_selection._get_parent_and_start_stop_indices()
        parent, start_index, stop_index = result
        old_duration = abjad.inspect(old_selection).get_duration()
        division_lists = division_maker([old_duration])
        assert len(division_lists) == 1
        division_list = division_lists[0]
        new_selection = rhythm_maker(division_list)
        stop_index += 1
        dummy_music_voice[start_index:stop_index] = new_selection
        music = dummy_music_voice[:]
        selections = [abjad.select(_) for _ in music]
        return selections

    # TODO: make self.state work with multimaker input
    def _make_rhythm(self, start_offset, time_signatures):
        rhythm_maker = self.rhythm_maker
        if rhythm_maker is None:
            mask = abjad.silence([0], 1, use_multimeasure_rests=True)
            rhythm_maker = rhythmos.NoteRhythmMaker(division_masks=[mask])
        if isinstance(rhythm_maker, abjad.Selection):
            selections = [rhythm_maker]
        else:
            prototype = (rhythmos.RhythmMaker, collections.Iterable)
            if not isinstance(rhythm_maker, prototype):
                message = 'must be rhythm-maker, selection or pairs:\n'
                message += f'  not {rhythm_maker!r}'
                raise TypeError(message)
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
            previous_state = None
            dictionary = self.previous_segment_voice_metadata
            if dictionary:
                previous_state = dictionary.get(abjad.tags.RHYTHM)
                if previous_state.get('name') != self.persist:
                    previous_state = None
            if isinstance(rhythm_maker, rhythmos.RhythmMaker):
                pairs = [(rhythm_maker, abjad.index([0], 1))]
            else:
                pairs = list(rhythm_maker)
            assert isinstance(pairs, list), repr(pairs)
            for pair in pairs:
                assert isinstance(pair, tuple), repr(pair)
                assert len(pair) == 2, repr(pair)
                rhythm_maker, pattern = pair
                assert isinstance(rhythm_maker, rhythmos.RhythmMaker)
                assert isinstance(pattern, abjad.Pattern), repr(pattern)
            selections = []
            previous_rhythm_maker, divisions_ = None, []
            for i, division in enumerate(divisions):
                divisions_.append(division)
                found_rhythm_maker = False
                for pair in pairs:
                    rhythm_maker, pattern = pair
                    if pattern.matches_index(i, division_count):
                        found_rhythm_maker = True
                        break
                if not found_rhythm_maker:
                    message = 'can not find rhythm-maker for division {i}.'
                    raise Exception(message)
                if (i == division_count - 1 or
                    (previous_rhythm_maker is not None and
                    rhythm_maker != previous_rhythm_maker)):
                    selections_ = rhythm_maker(
                        divisions_,
                        previous_state=previous_state,
                        )
                    selections.extend(selections_)
                    divisions_ = []
                if rhythm_maker != previous_rhythm_maker:
                    previous_rhythm_maker = rhythm_maker
            self._annotate_unpitched_notes(selections)
            self._state = rhythm_maker.state
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        if self.split_at_measure_boundaries:
            specifier = rhythmos.DurationSpecifier
            selections = specifier._split_at_measure_boundaries(
                selections,
                time_signatures,
                repeat_ties=self.repeat_ties,
                )
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        if self.rewrite_meter:
            selections = rhythmos.DurationSpecifier._rewrite_meter_(
                selections,
                time_signatures,
                reference_meters=self.reference_meters,
                rewrite_tuplets=False,
                repeat_ties=self.repeat_ties,
                )
        if self.rhythm_overwrites:
            selections = self._handle_rhythm_overwrites(
                time_signatures,
                selections,
                )
        if self.rewrite_rest_filled:
            selections = rhythmos.DurationSpecifier._rewrite_rest_filled_(
                selections,
                multimeasure_rests=self.multimeasure_rests,
                )
        self._tag_broken_ties(selections)
        return selections, start_offset

    def _tag_broken_ties(self, selections):
        if not isinstance(self.rhythm_maker, rhythmos.RhythmMaker):
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
        """
        Gets division expression.
        """
        return self._division_expression

    @property
    def division_maker(self) -> typing.Optional[division_maker_typing]:
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
        """
        Is true when command rewrites meter.
        """
        return self._rewrite_meter

    @property
    def rewrite_rest_filled(self) -> typing.Optional[bool]:
        """
        Is true when command rewrites rest-filled divisions.
        """
        return self._rewrite_rest_filled

    @property
    def rhythm_maker(self) -> typing.Optional[rhythm_maker_typing]:
        """
        Gets rhythm-maker or selection.
        """
        return self._rhythm_maker

    @property
    def rhythm_overwrites(self) -> typing.Optional[typing.List[tuple]]:
        """
        Gets rhythm overwrites.
        """
        return self._rhythm_overwrites

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

    @property
    def tie_first(self) -> typing.Optional[bool]:
        """
        Is true when command ties into first pleaf.
        """
        return self._tie_first

    @property
    def tie_last(self) -> typing.Optional[bool]:
        """
        Is true when command ties into last pleaf.
        """
        return self._tie_last
