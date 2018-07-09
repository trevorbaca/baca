import abjad
from . import scoping
from . import rhythmcommands
from .LMRSpecifier import LMRSpecifier


class NestingCommand(scoping.Command):
    r"""
    Nesting command.

    >>> from abjadext import rmakers

    ..  container:: example

        Augments one sixteenth:

        >>> music_maker = baca.MusicMaker(
        ...     baca.NestingCommand(
        ...         time_treatments=['+1/16'],
        ...         ),
        ...     rmakers.BeamSpecifier(
        ...         beam_divisions_together=True,
        ...         ),
        ...     )

        >>> collections = [
        ...     [0, 2, 10, 18],
        ...     [16, 15, 23],
        ...     [19, 13, 9, 8],
        ...     ]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/11 {
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                fs''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                b''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                cs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                af'16
                                ]
                            }
                        }
                    }
                }
            >>

    ..  container:: example

        Calltime nesting command preserves beam subdivisions and works with
        extend beam:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

        >>> containers, time_signatures = [], []
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10, 18], [16, 15, 23]],
        ...     baca.NestingCommand(
        ...         time_treatments=['+1/16'],
        ...         ),
        ...     extend_beam=True,
        ...     )
        >>> containers.extend(contribution['Voice 1'])
        >>> time_signatures.append(contribution.time_signature)
        >>> contribution = music_maker('Voice 1', [[19, 13, 9, 8]])
        >>> containers.extend(contribution['Voice 1'])
        >>> time_signatures.append(contribution.time_signature)
        >>> selection = abjad.select(containers)

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         minimum_duration=abjad.Duration(1, 24),
        ...         ),
        ...     time_signatures=time_signatures,
        ...     )
        >>> maker(
        ...     'MusicVoice',
        ...     baca.RhythmCommand(
        ...         rhythm_maker=selection,
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> staff = lilypond_file[abjad.Staff]
        >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
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
                        \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                        \time 1/2                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                        \time 1/4                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/4
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    \with
                    {
                        \override Beam.positions = #'(-5.5 . -5.5)
                    }
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 8/7 {
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [MusicVoice measure 1]                                     %! SM4
                                        \set stemLeftBeamCount = 0                                   %! SM35
                                        \set stemRightBeamCount = 2                                  %! SM35
                                        c'16
                                        [                                                            %! SM35
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM35
                                        \set stemRightBeamCount = 2                                  %! SM35
                                        d'16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM35
                                        \set stemRightBeamCount = 2                                  %! SM35
                                        bf'!16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM35
                                        \set stemRightBeamCount = 1                                  %! SM35
                                        fs''!16
                                    }
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        \set stemLeftBeamCount = 1                                   %! SM35
                                        \set stemRightBeamCount = 2                                  %! SM35
                                        e''16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM35
                                        \set stemRightBeamCount = 2                                  %! SM35
                                        ef''!16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM35
                                        \set stemRightBeamCount = 1                                  %! SM35
                                        b''16
                                    }
                                }
                            }
                            {
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [MusicVoice measure 2]                                         %! SM4
                                    \set stemLeftBeamCount = 1                                       %! SM35
                                    \set stemRightBeamCount = 2                                      %! SM35
                                    g''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2                                       %! SM35
                                    \set stemRightBeamCount = 2                                      %! SM35
                                    cs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2                                       %! SM35
                                    \set stemRightBeamCount = 2                                      %! SM35
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2                                       %! SM35
                                    \set stemRightBeamCount = 0                                      %! SM35
                                    af'!16
                                    ]                                                                %! SM35
            <BLANKLINE>
                                }
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lmr_specifier',
        '_time_treatments',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        lmr_specifier=None,
        time_treatments=None,
        ):
        if lmr_specifier is not None:
            prototype = LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier
        if time_treatments is not None:
            assert isinstance(time_treatments, (list, tuple))
            is_time_treatment = rhythmcommands.PitchFirstRhythmMaker._is_time_treatment
            for time_treatment in time_treatments:
                assert is_time_treatment(time_treatment), repr(time_treatment)
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(self, selections=None):
        r"""
        Calls command on ``selections``.

        ..  container:: example

            With rest affixes:

            >>> music_maker = baca.MusicMaker(
            ...     baca.NestingCommand(time_treatments=['+1/16']),
            ...     baca.RestAffixSpecifier(
            ...         prefix=[2],
            ...         suffix=[3],
            ...         ),
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 17/16 {
                                \scaleDurations #'(1 . 1) {
                                    r8
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    b''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af'16
                                    ]
                                    r8.
                                }
                            }
                        }
                    }
                >>

        Returns new selections.
        """
        if selections is None:
            return
        time_treatments = self._get_time_treatments()
        if time_treatments is None:
            return selections
        tuplets = []
        for selection in selections:
            if not isinstance(selection, abjad.Selection):
                raise Exception(f'should be selection: {selection!r}.')
            assert len(selection) == 1, repr(selection)
            assert isinstance(selection[0], abjad.Tuplet)
            tuplets.append(selection[0])
        if self.lmr_specifier is None:
            tuplet_selections = [abjad.select(tuplets)]
        else:
            tuplet_selections = self.lmr_specifier(tuplets)
            tuplet_selections = [
                abjad.select(list(_)) for _ in tuplet_selections]
        selections_ = []
        prototype = abjad.Selection
        for index, tuplet_selection in enumerate(tuplet_selections):
            assert isinstance(tuplet_selection, prototype), repr(
                tuplet_selection)
            time_treatment = time_treatments[index]
            if time_treatment is None:
                selections_.append(tuplet_selection)
            else:
                nested_tuplet = self._make_nested_tuplet(
                    tuplet_selection,
                    time_treatment,
                    )
                selection_ = abjad.Selection([nested_tuplet])
                selections_.append(selection_)
        return selections_

    ### PRIVATE METHODS ###

    def _get_time_treatments(self):
        if self.time_treatments:
            return abjad.CyclicTuple(self.time_treatments)

    @staticmethod
    def _make_nested_tuplet(tuplet_selection, time_treatment):
        assert isinstance(tuplet_selection, abjad.Selection)
        for tuplet in tuplet_selection:
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        if isinstance(time_treatment, str):
            addendum = abjad.Duration(time_treatment)
            contents_duration = abjad.inspect(tuplet_selection).get_duration()
            target_duration = contents_duration + addendum
            multiplier = target_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif time_treatment.__class__ is abjad.Multiplier:
            #tuplet = abjad.Tuplet(time_treatment, tuplet_selection)
            tuplet = abjad.Tuplet(time_treatment, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif time_treatment.__class__ is abjad.Duration:
            target_duration = time_treatment
            contents_duration = abjad.inspect(tuplet_selection).get_duration()
            multiplier = target_duration / contents_duration
            #tuplet = abjad.Tuplet(multiplier, tuplet_selection)
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        else:
            raise Exception(f'bad time treatment: {time_treatment!r}.')
        return tuplet

    ### PUBLIC PROPERTIES ###

    # TODO: write LMR specifier examples
    @property
    def lmr_specifier(self):
        """
        Gets LMR specifier.

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        """
        return self._lmr_specifier

    @property
    def time_treatments(self):
        """
        Gets time treatments.

        Defaults to none.

        Set to time treatments or none.

        Returns time treatments or none.
        """
        return self._time_treatments
