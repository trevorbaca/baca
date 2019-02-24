"""
Rhythm library.
"""
import abjad
import collections
import inspect
import math
import typing
from abjadext import rmakers
from . import classes
from . import divisions as baca_divisions
from . import const
from . import overrides
from . import scoping
from . import typings
mask_typing = typing.Union[rmakers.SilenceMask, rmakers.SustainMask]


### CLASSES ###

class RhythmCommand(scoping.Command):
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
        ...     'Music_Voice',
        ...     command,
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
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_annotate_unpitched_music',
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
        '_state',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        annotate_unpitched_music: bool = None,
        division_maker: baca_divisions.DivisionMaker = None,
        division_expression: abjad.Expression = None,
        left_broken: bool = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        multimeasure_rests: bool = None,
        persist: str = None,
        reference_meters: typing.Iterable[abjad.Meter] = None,
        rewrite_meter: bool = None,
        rewrite_rest_filled: bool = None,
        rhythm_maker: typings.RhythmMakerTyping = None,
        right_broken: bool = None,
        scope: scoping.ScopeTyping = None,
        split_at_measure_boundaries: bool = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            match=match,
            measures=measures,
            scope=scope,
            )
        if annotate_unpitched_music is not None:
            annotate_unpitched_music = bool(annotate_unpitched_music)
        self._annotate_unpitched_music = annotate_unpitched_music
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += f':\n{division_expression} {division_maker}.'
            raise Exception(message)
        if division_maker is not None:
            assert isinstance(division_maker, baca_divisions.division_maker_type), repr(division_maker)
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
        self._state: typing.Optional[abjad.OrderedDict] = None

    ### SPECIAL METHODS ###

    def _call(
        self,
        runtime: abjad.OrderedDict = None,
        start_offset: abjad.Offset = None,
        time_signatures: typing.Iterable[abjad.TimeSignature] = None,
        ) -> None:
        """
        Calls command on ``start_offset`` and ``time_signatures``.
        """
        self._runtime = runtime or abjad.OrderedDict()
        music, start_offset = self._make_rhythm(start_offset, time_signatures)
        assert isinstance(music, (tuple, list, abjad.Voice))
        first_leaf = abjad.inspect(music).leaf(0)
        final_leaf = abjad.inspect(music).leaf(-1)
        pitched_prototype = (abjad.Note, abjad.Chord)
        payload = abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=None,
            annotation=music,
            )
        self._payload = payload

    ### PRIVATE METHODS ###

    @staticmethod
    def _annotate_unpitched_music_(argument):
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
        divisions = [baca_divisions.Division(_) for _ in durations]
        durations = [_.duration for _ in divisions]
        start_offset = abjad.Offset(start_offset)
        durations.insert(0, start_offset)
        start_offsets = abjad.mathtools.cumulative_sums(durations)[1:-1]
        assert len(divisions) == len(start_offsets)
        divisions_ = []
        for division, start_offset in zip(divisions, start_offsets):
            division_ = baca_divisions.Division(
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
                division_maker = baca_divisions.DivisionMaker()
            divisions = self._durations_to_divisions(
                time_signatures,
                start_offset,
                )
            divisions = division_maker(divisions)
            divisions = classes.Sequence(divisions).flatten(depth=-1)
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
            labelled_divisions = classes.Sequence(labelled_divisions)
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
        if self.annotate_unpitched_music or not literal_selections:
            self._annotate_unpitched_music_(selections)
        return selections, start_offset

    def _previous_segment_stop_state(self):
        previous_segment_stop_state = None
        dictionary = self.runtime.get('previous_segment_voice_metadata')
        if dictionary:
            previous_segment_stop_state = dictionary.get(const.RHYTHM)
            if (previous_segment_stop_state is not None and
                previous_segment_stop_state.get('name') != self.persist):
                previous_segment_stop_state = None
        return previous_segment_stop_state

    def _tag_broken_ties(self, selections):
        if not isinstance(self.rhythm_maker, rmakers.RhythmMaker):
            return
        if (self.left_broken and
            self.rhythm_maker.previous_state.get('incomplete_final_note')):
            if not self.repeat_ties:
                raise Exception('left-broken ties must be repeat ties.')
            first_leaf = abjad.select(selections).leaf(0)
            if isinstance(first_leaf, abjad.Note):
                abjad.attach(const.LEFT_BROKEN_REPEAT_TIE_TO, first_leaf)
        if (self.right_broken and
            self.rhythm_maker.state.get('incomplete_final_note')):
            if self.repeat_ties:
                raise Exception('right-broken ties must be conventional.')
            final_leaf = abjad.select(selections).leaf(-1)
            if isinstance(final_leaf, abjad.Note):
                abjad.attach(abjad.tags.RIGHT_BROKEN_TIE_FROM, final_leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def annotate_unpitched_music(self) -> typing.Optional[bool]:
        """
        Is true when command annotates unpitched music.
        """
        return self._annotate_unpitched_music

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
            ...     'Music_Voice',
            ...     command,
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
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
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
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                                [
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                                ]
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

        """
        return self._division_expression

    @property
    def division_maker(self) -> typing.Optional[baca_divisions.DivisionMakerTyping]:
        """
        Gets division-maker.
        """
        return self._division_maker

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when rhythm is left-broken.

        Talea rhythm-maker knows how to tag incomplete last notes.
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
        return const.RHYTHM

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
        """
        Is true when rhythm command uses repeat ties.
        """
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
            ...     'Music_Voice',
            ...     baca.make_repeat_tied_notes(),
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
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 10/8                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 5/4                                                                     %! _make_global_skips(1)
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
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4.
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                \repeatTie
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4.
                                \repeatTie
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4                                                                      %! baca_make_repeat_tied_notes
                                \repeatTie
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

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
            ...     'Music_Voice',
            ...     baca.label(label),
            ...     baca.text_script_font_size(-2),
            ...     baca.text_script_staff_padding(5),
            ...     command,
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
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
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
                                \override TextScript.font-size = #-2                                     %! baca_text_script_font_size:OverrideCommand(1)
                                \override TextScript.staff-padding = #5                                  %! baca_script_staff_padding:OverrideCommand(1)
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'16
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                ~
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                                _ \markup {
                                    \fraction
                                        2
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                r2
                                _ \markup {
                                    \fraction
                                        8
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                [
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                                ]
                                \revert TextScript.font-size                                             %! baca_text_script_font_size:OverrideCommand(2)
                                \revert TextScript.staff-padding                                         %! baca_script_staff_padding:OverrideCommand(2)
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

        ..  container:: example exception

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

        Talea rhythm-maker knows how to tag incomplete last notes.
        """
        return self._right_broken

    @property
    def split_at_measure_boundaries(self) -> typing.Optional[bool]:
        """
        Is true when command splits at measure boundaries.
        """
        return self._split_at_measure_boundaries

    @property
    def state(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state

class SkipRhythmMaker(rmakers.RhythmMaker):
    r"""
    Skip rhythm-maker.

    >>> import abjadext

    ..  container:: example

        Makes skips equal to the duration of input divisions.

        >>> rhythm_maker = baca.SkipRhythmMaker()

        >>> divisions = [(1, 4), (3, 16), (5, 8)]
        >>> selections = rhythm_maker(divisions)

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            <BLANKLINE>
            \context Staff = "Music_Staff" %! baca.SingleStaffScoreTemplate.__call__
            {                              %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context Voice = "Music_Voice" %! baca.SingleStaffScoreTemplate.__call__
                {                              %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    % [Music_Voice measure 1] %! _comment_measure_numbers
                    \override TextScript.font-size = #-2 %! baca_text_script_font_size:OverrideCommand(1)
                    \override TextScript.staff-padding = #5 %! baca_script_staff_padding:OverrideCommand(1)
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'8.
                    _ \markup {
                        \fraction
                            3
                            16
                        }
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'4
                    _ \markup {
                        \fraction
                            4
                            16
                        }
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'16
                    _ \markup {
                        \fraction
                            3
                            16
                        }
                    ~
            <BLANKLINE>
                    % [Music_Voice measure 2] %! _comment_measure_numbers
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'8
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'4
                    _ \markup {
                        \fraction
                            4
                            16
                        }
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'8
                    _ \markup {
                        \fraction
                            2
                            16
                        }
            <BLANKLINE>
                    % [Music_Voice measure 3] %! _comment_measure_numbers
                    r2
                    _ \markup {
                        \fraction
                            8
                            16
                        }
            <BLANKLINE>
                    % [Music_Voice measure 4] %! _comment_measure_numbers
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'16
                    _ \markup {
                        \fraction
                            1
                            16
                        }
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'4
                    _ \markup {
                        \fraction
                            4
                            16
                        }
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'8.
                    _ \markup {
                        \fraction
                            3
                            16
                        }
            <BLANKLINE>
                    % [Music_Voice measure 5] %! _comment_measure_numbers
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'4
                    _ \markup {
                        \fraction
                            4
                            16
                        }
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'8.
                    _ \markup {
                        \fraction
                            3
                            16
                        }
                    [
            <BLANKLINE>
                    \baca-unpitched-music-warning %! _color_unpitched_notes
                    c'16
                    _ \markup {
                        \fraction
                            1
                            16
                        }
                    ]
                    \revert TextScript.font-size %! baca_text_script_font_size:OverrideCommand(2)
                    \revert TextScript.staff-padding %! baca_script_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                } %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            } %! baca.SingleStaffScoreTemplate.__call__

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        divisions: typing.List[typings.IntegerPair],
        previous_state: abjad.OrderedDict = None,
        ) -> typing.List[abjad.Selection]:
        """
        Calls skip rhythm-maker on ``divisions``.
        """
        return rmakers.RhythmMaker.__call__(
            self,
            divisions,
            previous_state=previous_state,
            )

    def __format__(self, format_specification='') -> str:
        """
        Formats skip rhythm-maker.

        Set ``format_specification`` to ``''`` or ``'storage'``.

        ..  container:: example

            >>> rhythm_maker = baca.SkipRhythmMaker()
            >>> abjad.f(rhythm_maker)
            baca.SkipRhythmMaker()

        """
        return super().__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_music(self, divisions):
        result = []
        for division in divisions:
            prototype = abjad.NonreducedFraction
            assert isinstance(division, prototype), repr(division)
            written_duration = abjad.Duration(1)
            multiplied_duration = division
            skip = self._make_skips(
                written_duration,
                [multiplied_duration],
                tag=self.tag,
                )
            result.append(skip)
        return result

    @staticmethod
    def _make_skips(written_duration, multiplied_durations, tag=None):
        skips = []
        written_duration = abjad.Duration(written_duration)
        for multiplied_duration in multiplied_durations:
            multiplied_duration = abjad.Duration(multiplied_duration)
            multiplier = multiplied_duration / written_duration
            skip = abjad.Skip(written_duration, multiplier=multiplier, tag=tag)
            skips.append(skip)
        return abjad.select(skips)

    ### PUBLIC PROPERTIES ###

    @property
    def tuplet_specifier(self) -> typing.Optional[rmakers.TupletSpecifier]:
        r"""
        Gets tuplet specifier.

        ..  container:: example

            No effect because ``SkipRhythmMaker`` makes skips instead of
            tuplets:

            >>> rhythm_maker = baca.SkipRhythmMaker(
            ...     tuplet_specifier=abjadext.rmakers.TupletSpecifier(
            ...         force_fraction=True,
            ...         ),
            ...     )

            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> selections = rhythm_maker(divisions)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                <BLANKLINE>
                \context Staff = "Music_Staff" %! baca.SingleStaffScoreTemplate.__call__
                {                              %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context Voice = "Music_Voice" %! baca.SingleStaffScoreTemplate.__call__
                    {                              %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        % [Music_Voice measure 1] %! _comment_measure_numbers
                        \override TextScript.font-size = #-2 %! baca_text_script_font_size:OverrideCommand(1)
                        \override TextScript.staff-padding = #5 %! baca_script_staff_padding:OverrideCommand(1)
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'8.
                        _ \markup {
                            \fraction
                                3
                                16
                            }
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'4
                        _ \markup {
                            \fraction
                                4
                                16
                            }
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'16
                        _ \markup {
                            \fraction
                                3
                                16
                            }
                        ~
                <BLANKLINE>
                        % [Music_Voice measure 2] %! _comment_measure_numbers
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'8
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'4
                        _ \markup {
                            \fraction
                                4
                                16
                            }
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'8
                        _ \markup {
                            \fraction
                                2
                                16
                            }
                <BLANKLINE>
                        % [Music_Voice measure 3] %! _comment_measure_numbers
                        r2
                        _ \markup {
                            \fraction
                                8
                                16
                            }
                <BLANKLINE>
                        % [Music_Voice measure 4] %! _comment_measure_numbers
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'16
                        _ \markup {
                            \fraction
                                1
                                16
                            }
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'4
                        _ \markup {
                            \fraction
                                4
                                16
                            }
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'8.
                        _ \markup {
                            \fraction
                                3
                                16
                            }
                <BLANKLINE>
                        % [Music_Voice measure 5] %! _comment_measure_numbers
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'4
                        _ \markup {
                            \fraction
                                4
                                16
                            }
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'8.
                        _ \markup {
                            \fraction
                                3
                                16
                            }
                        [
                <BLANKLINE>
                        \baca-unpitched-music-warning %! _color_unpitched_notes
                        c'16
                        _ \markup {
                            \fraction
                                1
                                16
                            }
                        ]
                        \revert TextScript.font-size %! baca_text_script_font_size:OverrideCommand(2)
                        \revert TextScript.staff-padding %! baca_script_staff_padding:OverrideCommand(2)
                <BLANKLINE>
                    } %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                } %! baca.SingleStaffScoreTemplate.__call__

        Returns tuplet specifier or none.
        """
        return super().tuplet_specifier

class TieCorrectionCommand(scoping.Command):
    """
    Tie correction command.

    ..  container:: example

        >>> baca.TieCorrectionCommand()
        TieCorrectionCommand(selector=baca.pleaf(-1))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_repeat',
        '_untie',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: abjad.HorizontalAlignment = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        repeat: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.pleaf(-1)',
        untie: bool = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope, selector=selector,
            )
        if direction is not None:
            assert direction in (abjad.Right, abjad.Left, None)
        self._direction = direction
        self._map = map
        if repeat is not None:
            repeat = bool(repeat)
        self._repeat = repeat
        if untie is not None:
            untie = bool(untie)
        self._untie = untie

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = classes.Selection(argument).leaves()
        for leaf in leaves:
            if self.untie is True:
                #self._sever_tie(leaf, self.direction, self.repeat)
                self._sever_tie(leaf, self.direction)
            else:
                self._add_tie(leaf, self.direction, self.repeat)

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_tie(current_leaf, direction, repeat):
        assert direction in (abjad.Left, abjad.Right, None), repr(direction)
        left_broken, right_broken = None, None
        if direction is None:
            direction = abjad.Right
        #current_tie = abjad.inspect(current_leaf).spanner(abjad.Tie)
        if direction == abjad.Right:
            next_leaf = abjad.inspect(current_leaf).leaf(1)
            if next_leaf is None:
                right_broken = True
#                if current_tie is not None:
#                    new_leaves = list(current_tie.leaves)
#                    new_tie = abjad.new(current_tie)
#                else:
#                    new_leaves = [current_leaf]
#                    new_tie = abjad.Tie(repeat=repeat)
            else:
                pass
#                next_tie = abjad.inspect(next_leaf).spanner(abjad.Tie)
#                if current_tie is not None and next_tie is not None:
#                    if current_tie is next_tie:
#                        return
#                    else:
#                        new_leaves = list(current_tie) + list(next_tie)
#                        new_tie = abjad.new(current_tie)
#                elif current_tie is not None and next_tie is None:
#                    new_leaves = list(current_tie) + [next_leaf]
#                    new_tie = abjad.new(current_tie)
#                elif current_tie is None and next_tie is not None:
#                    new_leaves = [current_leaf] + list(next_tie)
#                    new_tie = abjad.Tie(repeat=repeat)
#                else:
#                    assert current_tie is None and next_tie is None
#                    new_leaves = [current_leaf, next_leaf]
#                    new_tie = abjad.Tie(repeat=repeat)
        else:
            assert direction == abjad.Left
            previous_leaf = abjad.inspect(current_leaf).leaf(-1)
            if previous_leaf is None:
                left_broken = True
#                if current_tie is not None:
#                    new_leaves = list(current_tie.leaves)
#                    new_tie = abjad.new(current_tie, repeat=repeat)
#                else:
#                    new_leaves = [current_leaf]
#                    new_tie = abjad.Tie(repeat=repeat)
            else:
                pass
#                previous_tie = abjad.inspect(previous_leaf).spanner(
#                    abjad.Tie)
#                if previous_tie is not None and current_tie is not None:
#                    if previous_tie is current_tie:
#                        return
#                    else:
#                        new_leaves = list(previous_tie) + list(current_tie)
#                        new_tie = abjad.new(previous_tie)
#                elif previous_tie is not None and current_tie is None:
#                    new_leaves = list(previous_tie) + [current_leaf]
#                    new_tie = abjad.new(previous_tie)
#                elif previous_tie is None and current_tie is not None:
#                    new_leaves = [previous_leaf] + list(current_tie)
#                    new_tie = abjad.Tie(repeat=repeat)
#                else:
#                    assert previous_tie is None and current_tie is None
#                    new_leaves = [previous_leaf, current_leaf]
#                    new_tie = abjad.Tie(repeat=repeat)

#        new_leaves = abjad.select(new_leaves)
#        for leaf in new_leaves:
#            abjad.detach(abjad.Tie, leaf)
#        new_tie = abjad.new(
#            new_tie,
#            left_broken=left_broken,
#            right_broken=right_broken,
#            )
#        abjad.attach(new_tie, new_leaves, tag='TieCorrectionCommand')

        if direction == abjad.Left:
            if repeat:
                repeat_tie = abjad.RepeatTie(left_broken=left_broken)
                abjad.attach(repeat_tie, current_leaf, tag='TieCorrectionCommand')
            else:
                tie = abjad.TieIndicator(right_broken=right_broken)
                abjad.attach(tie, previous_leaf, tag='TieCorrectionCommand') 
        else:
            assert direction == abjad.Right
            if not repeat:
                tie = abjad.TieIndicator(right_broken=right_broken)
                abjad.attach(tie, current_leaf, tag='TieCorrectionCommand')
            else:
                repeat_tie = abjad.RepeatTie(left_broken=left_broken)
                abjad.attach(repeat_tie, next_leaf, tag='TieCorrectionCommand')

    @staticmethod
    #def _sever_tie(current_leaf, direction, repeat):
    def _sever_tie(current_leaf, direction):
#        current_tie = abjad.inspect(current_leaf).spanner(abjad.Tie)
#        if current_tie is None:
#            return
#        if direction is None:
#            direction = abjad.Right
#        leaf_index = current_tie.leaves.index(current_leaf)
#        current_tie._fracture(leaf_index, direction=direction)
        if direction in (abjad.Right, None):
            abjad.detach(abjad.TieIndicator, current_leaf)
            next_leaf = abjad.inspect(current_leaf).leaf(1)
            if next_leaf is not None:
                abjad.detach(abjad.RepeatTie, next_leaf)
        else:
            assert direction == abjad.Left
            abjad.detach(abjad.RepeatTie, current_leaf)
            previous_leaf = abjad.inspect(current_leaf).leaf(-1)
            if previous_leaf is not None:
                abjad.detach(abjad.TieIndicator, previous_leaf)
            
    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[abjad.HorizontalAlignment]:
        """
        Gets direction.

        Interprets none equal to right.
        """
        return self._direction

    @property
    def repeat(self) -> typing.Optional[bool]:
        """
        Is true when newly created ties should be repeat ties.
        """
        return self._repeat

    @property
    def untie(self) -> typing.Optional[bool]:
        """
        Is true when command severs tie instead of creating tie.
        """
        return self._untie

### FACTORY FUNCTIONS ###

def beam_divisions(
    *,
    stemlets: typings.Number = None,
    ) -> rmakers.BeamSpecifier:
    r"""
    Beams divisions.

    ..  container:: example

        Beams divisions:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_divisions(),
        ...     baca.rests_around([2], [2]),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            r8
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            r8
                        }
                    }
                }
            >>

    ..  container:: example

        Beams divisions with stemlets:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_divisions(stemlets=2),
        ...     baca.rests_around([2], [2]),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 2
                            r8
                            [
                            c'16
                            d'16
                            \revert Staff.Stem.stemlet-length
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 2
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            \revert Staff.Stem.stemlet-length
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 2
                            a'16
                            [
                            \revert Staff.Stem.stemlet-length
                            r8
                            ]
                        }
                    }
                }
            >>

    """
    return rmakers.BeamSpecifier(
        beam_each_division=True,
        beam_rests=bool(stemlets),
        stemlet_length=stemlets,
        )

def beam_everything(
    *,
    stemlets: typings.Number = None,
    ) -> rmakers.BeamSpecifier:
    r"""
    Beams everything.

    ..  container:: example

        Beams everything:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_everything(),
        ...     baca.rests_around([2], [2]),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            r8
                            [
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            c'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            bf'16
                        }
                        \scaleDurations #'(1 . 1) {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            g''16
                        }
                        \scaleDurations #'(1 . 1) {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            a'16
                            r8
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        Beams everything with stemlets:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_everything(stemlets=2),
        ...     baca.rests_around([2], [2]),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 2
                            r8
                            [
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            c'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            bf'16
                        }
                        \scaleDurations #'(1 . 1) {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            g''16
                        }
                        \scaleDurations #'(1 . 1) {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            a'16
                            \revert Staff.Stem.stemlet-length
                            r8
                            ]
                        }
                    }
                }
            >>

    """
    return rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_each_division=True,
        beam_rests=True,
        stemlet_length=stemlets,
        )

def beam_runs() -> rmakers.BeamSpecifier:
    r"""
    Beams PLT runs.

    ..  container:: example

        Beams PLT runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_runs(),
        ...     baca.rests_around([2], [2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            d'16
                            ]
                            bf'4
                            ~
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            fs''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            e''16
                            ]
                            ef''4
                            ~
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            ef''16
                            r16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            af''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            g''16
                        }
                        \times 2/3 {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            a'16
                            ]
                            r8
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_each_division=True,
        beam_rests=False,
        )

def flags() -> rmakers.BeamSpecifier:
    r"""
    Flags music.

    ..  container:: example

        Flags music:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.flags(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            d'16
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            e''16
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            g''16
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return rmakers.BeamSpecifier(
        beam_divisions_together=False,
        beam_each_division=False,
        )

def make_even_divisions(
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_even_divisions',
    ) -> RhythmCommand:
    """
    Makes even divisions.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.EvenDivisionRhythmMaker(
            tag=tag,
            tuplet_specifier=rmakers.TupletSpecifier(
                extract_trivial=True,
                ),
            ),
        )

def make_fused_tuplet_monads(
    *,
    measures: typings.Slice = None,
    tag: str  = 'baca_make_fused_tuplet_monads',
    tuplet_ratio: typing.Tuple[int] = None,
    ) -> RhythmCommand:
    """
    Makes fused tuplet monads.
    """
    tuplet_ratios = []
    if tuplet_ratio is None:
        tuplet_ratios.append((1,))
    else:
        tuplet_ratios.append(tuplet_ratio)
    return RhythmCommand(
        division_expression=abjad.sequence()
            .sum()
            .sequence(),
        measures=measures,
        rhythm_maker=rmakers.TupletRhythmMaker(
            tag=tag,
            tie_specifier=rmakers.TieSpecifier(
                repeat_ties=True,
                ),
            tuplet_ratios=tuplet_ratios,
            tuplet_specifier=rmakers.TupletSpecifier(
                extract_trivial=True,
                rewrite_rest_filled=True,
                trivialize=True,
                ),
            ),
        )

def make_monads(
    fractions: str,
    ) -> RhythmCommand:
    r"""
    Makes monads.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 4)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_monads('2/5 2/5 1/5'),
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
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1                                                                       %! _make_global_skips(1)
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
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                        %! _color_unpitched_notes
                                c'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-unpitched-music-warning                                        %! _color_unpitched_notes
                                c'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-unpitched-music-warning                                        %! _color_unpitched_notes
                                c'4
            <BLANKLINE>
                            }
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    components: typing.List[abjad.Component] = []
    maker = abjad.LeafMaker()
    pitch = 0
    for fraction in fractions.split():
        leaves = maker([pitch], [fraction])
        components.extend(leaves)
    rhythm_maker = abjad.select(components)
    return RhythmCommand(
        annotate_unpitched_music=True,
        rhythm_maker=rhythm_maker,
        )

def make_multimeasure_rests(
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_multimeasure_rests',
    ) -> RhythmCommand:
    """
    Makes multimeasure rests.
    """
    mask = rmakers.SilenceMask(
        pattern=abjad.index_all(),
        use_multimeasure_rests=True,
        )
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=[mask],
            tag=tag,
            ),
        )

def make_notes(
    *,
    dmask: rmakers.MaskKeyword = None,
    measures: typings.Slice = None,
    repeat_ties: bool = False,
    tag: str = 'baca_make_notes',
    ) -> RhythmCommand:
    """
    Makes notes; rewrites meter.
    """
    tie_specifier = None
    if repeat_ties:
        tie_specifier = rmakers.TieSpecifier(repeat_ties=True)
    return RhythmCommand(
        measures=measures,
        rewrite_meter=True,
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=dmask,
            tag=tag,
            tie_specifier=tie_specifier,
            )
        )

def make_repeat_tied_notes(
    *,
    dmask: rmakers.MaskKeyword = None,
    do_not_rewrite_meter: bool = None,
    measures: typings.Slice = None,
    tag: str = 'baca_make_repeat_tied_notes',
    ) -> RhythmCommand:
    """
    Makes repeat-tied notes; rewrites meter.
    """
    return RhythmCommand(
        measures=measures,
        rewrite_meter=not(do_not_rewrite_meter),
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=dmask,
            tag=tag,
            tie_specifier=rmakers.TieSpecifier(
                tie_across_divisions=True,
                repeat_ties=True,
                ),
            ),
        )

def make_repeated_duration_notes(
    durations: typing.Iterable,
    *,
    beam_specifier: rmakers.BeamSpecifier = None,
    dmask: rmakers.MaskKeyword = None,
    do_not_rewrite_meter: bool = None,
    measures: typings.Slice = None,
    tag: str = 'baca_make_repeated_duration_notes',
    ) -> RhythmCommand:
    """
    Makes repeated-duration notes; rewrites meter.
    """
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    tie_specifier = rmakers.TieSpecifier(
        repeat_ties=True,
        )
    division_expression = baca_divisions.split_by_durations(
        durations=durations
        )
    return RhythmCommand(
        division_expression=division_expression,
        measures=measures,
        rewrite_meter=not(do_not_rewrite_meter),
        rhythm_maker=rmakers.NoteRhythmMaker(
            beam_specifier=beam_specifier,
            division_masks=dmask,
            tag=tag,
            tie_specifier=tie_specifier,
            ),
        )

def make_rests(
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_rests',
    ) -> RhythmCommand:
    """
    Makes rests.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=[rmakers.silence([0], 1)],
            tag=tag,
            ),
        )

def make_rhythm(
    selection: typing.Union[str, abjad.Selection],
    *,
    measures: typings.Slice = None,
    repeat_tie_threshold: typing.Union[
        bool,
        typings.IntegerPair,
        abjad.DurationInequality,
        ] = None,
    ) -> RhythmCommand:
    r"""
    Sets rhythm to ``selection``.

    ..  container:: example

        With ``repeat_tie_threshold``:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (4, 8), (3,8), (4, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_rhythm(
        ...         "d'4. ~ d'2 ~ d'4. ~ d'2",
        ...         repeat_tie_threshold=(4, 8),
        ...         ),
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
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            d'4.
                            ~
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            d'2
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d'4.
                            \repeatTie
                            ~
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d'2
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    if isinstance(selection, str):
        container = abjad.Container(selection)
        argument = abjad.mutate(container).eject_contents()
    else:
        assert isinstance(selection, abjad.Selection), repr(selection)
        argument = selection
    if repeat_tie_threshold is not None:
        temporary_container = abjad.Container([argument])
        for logical_tie in abjad.select(temporary_container).logical_ties():
            if logical_tie.is_trivial:
                continue
            for leaf in logical_tie.leaves:
                abjad.detach(abjad.TieIndicator, leaf)
                abjad.detach(abjad.RepeatTie, leaf)
            abjad.tie(
                logical_tie,
                repeat=repeat_tie_threshold,
                # TODO: add tag
                #tag='baca_make_rhythm',
                )
        temporary_container[:] = []
    return RhythmCommand(
        measures=measures,
        rhythm_maker=argument,
        )

def make_single_attack(
    duration,
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_single_attack',
    ) -> RhythmCommand:
    """
    Makes single attacks with ``duration``.
    """
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    rhythm_maker = rmakers.IncisedRhythmMaker(
        incise_specifier=rmakers.InciseSpecifier(
            fill_with_notes=False,
            outer_divisions_only=True,
            prefix_talea=[numerator],
            prefix_counts=[1],
            talea_denominator=denominator,
            ),
        tag=tag,
        )
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rhythm_maker,
        )

def make_skips(
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_skips',
    ) -> RhythmCommand:
    """
    Makes skips.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=SkipRhythmMaker()
        )

def make_tied_notes(
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_tied_notes',
    ) -> RhythmCommand:
    """
    Makes tied notes; rewrites meter.
    """
    return RhythmCommand(
        measures=measures,
        rewrite_meter=True,
        rhythm_maker=rmakers.NoteRhythmMaker(
            tag=tag,
            tie_specifier=rmakers.TieSpecifier(
                tie_across_divisions=True,
                ),
            ),
        )

def make_tied_repeated_durations(
    durations: typing.Iterable,
    *,
    measures: typings.Slice = None,
    tag: str = 'baca_make_tied_reepated_durations',
    ) -> RhythmCommand:
    """
    Makes tied repeated durations; does not rewrite meter.
    """
    command = make_repeated_duration_notes(
        durations,
        measures=measures,
        tag=tag,
        )
    return abjad.new(
        command,
        rewrite_meter=False,
        rhythm_maker__tie_specifier__tie_across_divisions=True,
        )

def repeat_tie_from(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
    ) -> TieCorrectionCommand:
    r"""
    Repeat-ties from leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.repeat_tie_from(selector=baca.leaf(1)),
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
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'2                                                                      %! baca_make_notes
                            \repeatTie                                                               %! TieCorrectionCommand
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return TieCorrectionCommand(
        repeat=True,
        selector=selector,
        )

def repeat_tie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Repeat-ties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.repeat_tie_to(selector=baca.leaf(2)),
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
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'2                                                                      %! baca_make_notes
                            \repeatTie                                                               %! TieCorrectionCommand
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        repeat=True,
        selector=selector,
        )

def rhythm(
    rhythm_maker: typings.RhythmMakerTyping,
    *,
    annotate_unpitched_music: bool = None,
    division_maker: baca_divisions.DivisionMaker = None,
    division_expression: abjad.Expression = None,
    left_broken: bool = None,
    measures: typings.Slice = None,
    multimeasure_rests: bool = None,
    persist: str = None,
    reference_meters: typing.Iterable[abjad.Meter] = None,
    rewrite_meter: bool = None,
    rewrite_rest_filled: bool = None,
    right_broken: bool = None,
    split_at_measure_boundaries: bool = None,
    ) -> RhythmCommand:
    """
    Makes rhythm command.
    """
    if isinstance(rhythm_maker, str):
        components = abjad.parse(rhythm_maker)
        rhythm_maker = abjad.select(components)
    return RhythmCommand(
        annotate_unpitched_music=annotate_unpitched_music,
        division_maker=division_maker,
        division_expression=division_expression,
        left_broken=left_broken,
        measures=measures,
        multimeasure_rests=multimeasure_rests,
        persist=persist,
        reference_meters=reference_meters,
        rewrite_meter=rewrite_meter,
        rewrite_rest_filled=rewrite_rest_filled,
        rhythm_maker=rhythm_maker,
        right_broken=right_broken,
        split_at_measure_boundaries=split_at_measure_boundaries,
        )

def silence_first() -> rmakers.SilenceMask:
    """
    Makes silence mask.
    
    ..  container::

        >>> abjad.f(baca.silence_first())
        abjadext.rmakers.silence([0])

    """
    return rmakers.silence([0])

def silence_last() -> rmakers.SilenceMask:
    """
    Makes silence mask.

    ..  container::

        >>> abjad.f(baca.silence_last())
        abjadext.rmakers.silence([-1])

    """
    return rmakers.silence([-1])

def sustain_first() -> rmakers.SustainMask:
    """
    Makes sustain mask.
    
    ..  container::

        >>> abjad.f(baca.sustain_first())
        abjadext.rmakers.sustain([0])

    """
    return rmakers.sustain([0])

def sustain_last() -> rmakers.SustainMask:
    """
    Makes sustain mask.

    ..  container::

        >>> abjad.f(baca.sustain_last())
        abjadext.rmakers.sustain([-1])

    """
    return rmakers.sustain([-1])

def tacet(
    color: str = 'green',
    *,
    measures: typings.Slice = None,
    selector: typings.Selector = 'baca.mmrests()',
    ) -> overrides.OverrideCommand:
    """
    Colors multimeasure rests.
    """
    command = overrides.mmrest_color(
        color,
        selector=selector,
        tag=f'{const.TACET}:baca_tacet',
        )
    command_ = scoping.new(command, measures=measures)
    assert isinstance(command_, overrides.OverrideCommand)
    return command_

def tie_from(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
    ) -> TieCorrectionCommand:
    r"""
    Ties from leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.tie_from(selector=baca.leaf(1)),
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
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
                            ~                                                                        %! TieCorrectionCommand
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return TieCorrectionCommand(
        repeat=False,
        selector=selector,
        )

def tie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Ties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.tie_to(selector=baca.leaf(1)),
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
                            c'2                                                                      %! baca_make_notes
                            ~                                                                        %! TieCorrectionCommand
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        repeat=False,
        selector=selector,
        )

def untie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Unties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_tied_notes(),
        ...     baca.untie_to(selector=baca.leaf(2)),
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
                            c'2                                                                      %! baca_make_tied_notes
                            ~
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_tied_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'2                                                                      %! baca_make_tied_notes
                            ~
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'4.                                                                     %! baca_make_tied_notes
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        selector=selector,
        untie=True,
        )
