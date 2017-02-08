# -*- coding: utf-8 -*-
import abjad
import baca
import collections


class RestAffixSpecifier(abjad.abctools.AbjadValueObject):
    r'''Rest affix specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.RestAffixSpecifier()
            RestAffixSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_denominator',
        '_pattern',
        '_prefix',
        '_skips_instead_of_rests',
        '_suffix',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        denominator=None,
        pattern=None,
        prefix=None,
        skips_instead_of_rests=None,
        suffix=None,
        ):
        if denominator is not None:
            assert isinstance(denominator, int), repr(denominator)
        self._denominator = denominator
        self._pattern = pattern
        if prefix is not None:
            assert isinstance(prefix, collections.Iterable), repr(prefix)
        self._prefix = prefix
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if suffix is not None:
            assert isinstance(suffix, collections.Iterable), repr(suffix)
        self._suffix = suffix

    ### SPECIAL METHODS ###

    def __call__(self, selections):
        r'''Calls specifier on `selections`.

        Returns none.
        '''
        if not selections:
            return
        if not self.prefix and not self.suffix:
            return
        denominator = self.denominator or 16
        rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            division_masks=[abjad.rhythmmakertools.silence_all()],
            )
        targets = []
        if self.pattern is None:
            targets.append(selections)
        else:
            total_length = len(selections)
            for i, selection in enumerate(selections): 
                if self.pattern.matches_index(i, total_length):
                    targets.append(selection)
        for target in targets:
            leaves = list(abjad.iterate(target).by_leaf())
            if self.prefix:
                assert all(isinstance(_, int) for _ in self.prefix)
                divisions = [(_, denominator) for _ in self.prefix]
                rests = rhythm_maker(divisions)
                rests = baca.Sequence(rests).flatten()
                if self.skips_instead_of_rests:
                    rests = [abjad.Skip(_.written_duration) for _ in rests]
                first_leaf = leaves[0]
                abjad.mutate(first_leaf).splice(rests, direction=Left)
            if self.suffix:
                assert all(isinstance(_, int) for _ in self.suffix)
                divisions = [(_, denominator) for _ in self.suffix]
                rests = rhythm_maker(divisions)
                rests = baca.Sequence(rests).flatten()
                if self.skips_instead_of_rests:
                    rests = [abjad.Skip(_.written_duration) for _ in rests]
                last_leaf = leaves[-1]
                abjad.mutate(last_leaf).splice(rests, direction=Right)

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self):
        r'''Gets denominator.

        Returns nonnegative integer power of two or none.
        '''
        return self._denominator

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            Treats entire figure when pattern is none:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.RestAffixSpecifier(
                ...         denominator=32,
                ...         prefix=[1],
                ...         suffix=[2],
                ...         ),
                ...     time_treatments=[1],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/3 {
                                r32
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16
                                r16
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats first stage and last stage in figure:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.RestAffixSpecifier(
                ...         denominator=32,
                ...         pattern=abjad.Pattern(indices=[0, -1]),
                ...         prefix=[1],
                ...         suffix=[2],
                ...         ),
                ...     time_treatments=[1],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                r32
                                c'16 [
                                d'16
                                bf'16 ]
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                r32
                                a'16
                                r16
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats every stage in figure:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.RestAffixSpecifier(
                ...         denominator=32,
                ...         pattern=abjad.patterntools.select_all(),
                ...         prefix=[1],
                ...         suffix=[2],
                ...         ),
                ...     time_treatments=[1],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                r32
                                c'16 [
                                d'16
                                bf'16 ]
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \tweak edge-height #'(0.7 . 0)
                            \times 6/5 {
                                r32
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                                r16
                            }
                            {
                                r32
                                a'16
                                r16
                            }
                        }
                    }
                >>

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def prefix(self):
        r'''Gets prefix.

        ..  container:: example

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.RestAffixSpecifier(
                ...         denominator=16,
                ...         prefix=[3],
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8.
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        Returns list of integers or none.
        '''
        return self._prefix

    @property
    def skips_instead_of_rests(self):
        r'''Is true when specifier makes skips instead of rests.

        Returns true, false or none.
        '''
        return self._skips_instead_of_rests

    @property
    def suffix(self):
        r'''Gets suffix.

        ..  container:: example

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.RestAffixSpecifier(
                ...         denominator=16,
                ...         suffix=[3],
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16
                                r8.
                            }
                        }
                    }
                >>

        Returns list of integers or none.
        '''
        return self._suffix
