import abjad
from .Command import Command


class TrillCommand(Command):
    r'''Trill command.

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.TrillCommand(
            ...         minimum_written_duration=abjad.Duration(1, 4),
            ...         maximum_written_duration=None,
            ...         ),
            ...     )

        ::

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     talea_denominator=4,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'4 \startTrillSpan
                            d'4 \stopTrillSpan \startTrillSpan
                            bf'4 \stopTrillSpan \startTrillSpan
                        }
                        {
                            fs''4 \stopTrillSpan \startTrillSpan
                            e''4 \stopTrillSpan \startTrillSpan
                            ef''4 \stopTrillSpan \startTrillSpan
                            af''4 \stopTrillSpan \startTrillSpan
                            g''4 \stopTrillSpan \startTrillSpan
                        }
                        {
                            a'4 \stopTrillSpan
                        }
                    }
                }
            >>

    ..  container:: example

        With collection-maker:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.scope(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('E4 F4'),
            ...     baca.messiaen_notes(),
            ...     baca.TrillCommand(
            ...         minimum_written_duration=abjad.Duration(1, 4),
            ...         maximum_written_duration=None,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, collection_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            e'2 \startTrillSpan
                            f'4. \stopTrillSpan \startTrillSpan
                            e'2 \stopTrillSpan \startTrillSpan
                            f'4. \stopTrillSpan
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_deposit_annotations',
        '_forbidden_annotations',
        '_harmonic',
        '_interval',
        '_maximum_written_duration',
        '_minimum_written_duration',
        '_selector',
        '_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deposit_annotations=None,
        forbidden_annotations=None,
        interval=None,
        harmonic=None,
        minimum_written_duration=None,
        maximum_written_duration=None,
        pitch=None,
        selector=None,
        ):
        if deposit_annotations is not None:
            assert isinstance(deposit_annotations, (tuple, list))
            deposit_annotations = tuple(deposit_annotations)
        self._deposit_annotations = deposit_annotations
        if forbidden_annotations is not None:
            assert isinstance(forbidden_annotations, (tuple, list))
            assert all(isinstance(_, str) for _ in forbidden_annotations)
            forbidden_annotations = tuple(forbidden_annotations)
        self._forbidden_annotations = forbidden_annotations
        self._interval = interval
        assert isinstance(harmonic, (bool, type(None)))
        self._harmonic = harmonic
        if minimum_written_duration is not None:
            minimum_written_duration = abjad.Duration(minimum_written_duration)
        self._minimum_written_duration = minimum_written_duration
        if maximum_written_duration is not None:
            maximum_written_duration = abjad.Duration(maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if pitch is not None:
            pitch = abjad.NamedPitch(pitch)
        self._pitch = pitch
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        logical_ties = abjad.select(argument).by_logical_tie(pitched=True)
        for logical_tie in logical_ties:
            written_duration = abjad.Duration(0)
            for note in logical_tie:
                written_duration += note.written_duration
            if self.minimum_written_duration is not None:
                if written_duration < self.minimum_written_duration:
                    continue
            if self.maximum_written_duration is not None:
                if self.maximum_written_duration <= written_duration:
                    continue
            spanner = abjad.TrillSpanner(
                interval=self.interval,
                is_harmonic=self.harmonic,
                pitch=self.pitch,
                )
            leaves = []
            for note in logical_tie:
                leaves.append(note)
            skip_spanner = False
            for leaf in leaves:
                if self._has_forbidden_annotation(leaf):
                    skip_spanner = True
                    break
            if skip_spanner:
                continue
            next_leaf = abjad.inspect(leaves[-1]).get_leaf(1)
            if next_leaf is not None:
                leaves.append(next_leaf)
            if 1 < len(leaves):
                leaves = abjad.select(leaves)
                abjad.attach(spanner, leaves)

    def _has_forbidden_annotation(self, leaf):
        if self.forbidden_annotations is None:
            return False
        for forbidden_annotation in self.forbidden_annotations:
            if abjad.inspect(leaf).has_indicator(forbidden_annotation):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def deposit_annotations(self):
        r'''Gets annotations to deposit on affected components.

        Set to annotations or none.
        '''
        return self._deposit_annotations

    @property
    def forbidden_annotations(self):
        r'''Gets annotations that indiate a component is forbidden
        from being affected.

        Set to annotations or none.
        '''
        return self._forbidden_annotations

    @property
    def harmonic(self):
        r'''Is true when command formats trill pitch note head as a white
        diamond.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._harmonic

    @property
    def interval(self):
        r'''Gets interval of trill command.

        Defaults to none.

        Set to interval or none.

        Returns interval or none.
        '''
        return self._interval

    @property
    def maximum_written_duration(self):
        r'''Gets maximum written duration of trill command.

        Set to duration or none.
        '''
        return self._maximum_written_duration

    @property
    def minimum_written_duration(self):
        r'''Gets minimum written duration of trill command.

        Set to duration or none.
        '''
        return self._minimum_written_duration

    @property
    def pitch(self):
        r'''Gets pitch of trill command.

        Set to pitch or none.
        '''
        return self._pitch

    @property
    def selector(self):
        r'''Gets selector.

        Set to selector or none.
        '''
        return self._selector
