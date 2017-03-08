# -*- coding: utf-8 -*-
import abjad


class TrillSpecifier(abjad.abctools.AbjadObject):
    r'''Trill specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With figure-maker:

        ::

            >>> figure_maker = baca.FigureMaker(
            ...     baca.tools.TrillSpecifier(
            ...         minimum_written_duration=abjad.Duration(1, 4),
            ...         maximum_written_duration=None,
            ...         ),
            ...     )

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     talea_denominator=4,
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

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

            >>> collection_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = collection_maker.append_specifiers(
            ...     ('vn', baca.select_stages(1)),
            ...     baca.pitches('E4 F4'),
            ...     baca.messiaen_note_rhythm_specifier(),
            ...     baca.tools.TrillSpecifier(
            ...         minimum_written_duration=abjad.Duration(1, 4),
            ...         maximum_written_duration=None,
            ...         ),
            ...     )

        ::

            >>> result = collection_maker(is_doc_example=True)
            >>> lilypond_file, collection_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
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
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
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

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_deposit_annotations',
        '_forbidden_annotations',
        '_is_harmonic',
        '_interval',
        '_maximum_written_duration',
        '_minimum_written_duration',
        '_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deposit_annotations=None,
        forbidden_annotations=None,
        interval=None,
        is_harmonic=None,
        minimum_written_duration=None,
        maximum_written_duration=None,
        pitch=None,
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
        assert isinstance(is_harmonic, (bool, type(None)))
        self._is_harmonic = is_harmonic
        if minimum_written_duration is not None:
            minimum_written_duration = abjad.Duration(minimum_written_duration)
        self._minimum_written_duration = minimum_written_duration
        if maximum_written_duration is not None:
            maximum_written_duration = abjad.Duration(maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if pitch is not None:
            pitch = abjad.NamedPitch(pitch)
        self._pitch = pitch

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
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
                is_harmonic=self.is_harmonic,
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
            next_leaf = abjad.inspect_(leaves[-1]).get_leaf(1)
            if next_leaf is not None:
                leaves.append(next_leaf)
            if 1 < len(leaves):
                abjad.attach(spanner, leaves)

    def _has_forbidden_annotation(self, leaf):
        if self.forbidden_annotations is None:
            return False
        for forbidden_annotation in self.forbidden_annotations:
            if abjad.inspect_(leaf).get_annotation(forbidden_annotation):
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
    def interval(self):
        r'''Gets interval of trill specifier.

        Defaults to none.

        Set to interval or none.

        Returns interval or none.
        '''
        return self._interval

    @property
    def is_harmonic(self):
        r'''Is true when specifier formats trill pitch note head as a white
        diamond.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._is_harmonic

    @property
    def maximum_written_duration(self):
        r'''Gets maximum written duration of trill specifier.

        Set to duration or none.
        '''
        return self._maximum_written_duration

    @property
    def minimum_written_duration(self):
        r'''Gets minimum written duration of trill specifier.

        Set to duration or none.
        '''
        return self._minimum_written_duration

    @property
    def pitch(self):
        r'''Gets pitch of trill specifier.

        Set to pitch or none.
        '''
        return self._pitch
