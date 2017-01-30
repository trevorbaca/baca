# -*- coding: utf-8 -*-
import abjad
import baca


class FigurePitchSpecifier(abjad.abctools.AbjadObject):
    r'''Figure pitch specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Accumulates transposed pitch-classes to identity:

        ::

            >>> transposition = baca.pitch_class_segment().transpose(n=3)
            >>> expression = baca.sequence().map(transposition)
            >>> expression = baca.sequence().accumulate([transposition])
            >>> expression = expression.join()[0]
            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.FigurePitchSpecifier(
            ...         expressions=[expression],
            ...         to_pitch_classes=True,
            ...         ),
            ...     )

        ::

            >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker(segment_list, 'Voice 1')
            >>> lilypond_file = figure_maker.make(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    {
                        {
                            c'16 [
                            d'16
                            bf'16 ]
                        }
                        {
                            fs'16 [
                            e'16
                            ef'16
                            af'16
                            g'16 ]
                        }
                        {
                            a'16
                        }
                        {
                            ef'16 [
                            f'16
                            cs'16 ]
                        }
                        {
                            a'16 [
                            g'16
                            fs'16
                            b'16
                            bf'16 ]
                        }
                        {
                            c'16
                        }
                        {
                            fs'16 [
                            af'16
                            e'16 ]
                        }
                        {
                            c'16 [
                            bf'16
                            a'16
                            d'16
                            cs'16 ]
                        }
                        {
                            ef'16
                        }
                        {
                            a'16 [
                            b'16
                            g'16 ]
                        }
                        {
                            ef'16 [
                            cs'16
                            c'16
                            f'16
                            e'16 ]
                        }
                        {
                            fs'16
                        }
                    }
                }
            >>

    Figure pitch specifiers tell figure-makers what to do with figure tokens.

    Figure-makers interpret figure pitch specifiers prior to other specifiers.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Figures'

    __slots__ = (
        '_expressions',
        '_remove_duplicate_pitch_classes',
        '_remove_duplicate_pitches',
        '_to_pitch_classes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        expressions=None,
        remove_duplicate_pitches=None,
        remove_duplicate_pitch_classes=None,
        to_pitch_classes=None,
        ):
        self._expressions = expressions
        if to_pitch_classes is not None:
            to_pitch_classes = bool(to_pitch_classes)
        self._to_pitch_classes = to_pitch_classes
        self._remove_duplicate_pitch_classes = remove_duplicate_pitch_classes
        self._remove_duplicate_pitches = remove_duplicate_pitches

    ### SPECIAL METHODS ###

    def __call__(self, segment_list=None):
        r'''Calls specifier on `segment_list`.

        ..  container:: example

            Returns none whens `segment_list` is none:

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier()
                >>> specifier() is None
                True

        ..  container:: example
        
            Returns sequence of pitch segments be default:

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier()
                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> for segment in specifier(segment_list):
                ...     segment
                ...
                PitchSegment([0, 2, 10])
                PitchSegment([18, 16, 15, 20, 19])
                PitchSegment([9])

        Returns new segment list.
        '''
        if segment_list is None:
            return
        segment_list = self._coerce(segment_list)
        assert isinstance(segment_list, baca.Sequence), repr(segment_list)
        #segment_list = self._remove_duplicates(segment_list)
        segment_list = self._apply_expressions(segment_list)
        return segment_list

    def __repr__(self, segment_list=None):
        r'''Gets interpreter representation.

        ..  container:: example

            ::

                >>> baca.tools.FigurePitchSpecifier()
                FigurePitchSpecifier()

        Returns string.
        '''
        superclass = super(FigurePitchSpecifier, self)
        return superclass.__repr__()

    ### PRIVATE METHODS ###

    def _apply_expressions(self, segment_list):
        for expression in self.expressions or []:
            assert isinstance(expression, abjad.Expression), repr(expression)
            segment_list = expression(segment_list)
        return segment_list

    def _coerce(self, segment_list):
        if self.to_pitch_classes:
            return self._to_pitch_class_segments(segment_list)
        return self._to_pitch_segments(segment_list)

    def _remove_duplicates(self, segment_list):
        if self.remove_duplicate_pitches:
            segment_list = self._remove_duplicate_pitches_(segment_list)
        if self.remove_duplicate_pitch_classes:
            segment_list = self._remove_duplicate_pitch_classes_(segment_list)
        return segment_list

    @staticmethod
    def _to_pitch_class_segments(segment_list):
        segments = []
        for item in segment_list:
            segment = baca.PitchClassSegment(items=item)
            segments.append(segment)
        return baca.Sequence(items=segments)

    @staticmethod
    def _to_pitch_segments(segment_list):
        segments = []
        for item in segment_list:
            segment = abjad.PitchSegment(items=item)
            segments.append(segment)
        return baca.Sequence(items=segments)

    def _to_pitch_tree(self, segment_list):
        item_class = None
        if self.to_pitch_classes:
            item_class = abjad.NumberedPitchClass
        return baca.tools.PitchTree(
            item_class=item_class,
            items=segment_list,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def expressions(self):
        r'''Gets expressions.

        ..  container:: example

            Transposes pitch-classes:

            ::

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> transposition = baca.sequence().map(transposition)
                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.FigurePitchSpecifier(
                ...         expressions=[transposition],
                ...         to_pitch_classes=True,
                ...         ),
                ...     )

            ::

                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(segment_list, 'Voice 1')
                >>> lilypond_file = figure_maker.make(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        {
                            {
                                ef'16 [
                                f'16
                                cs'16 ]
                            }
                            {
                                a'16 [
                                g'16
                                fs'16
                                b'16
                                bf'16 ]
                            }
                            {
                                c'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier()
                >>> specifier.expressions is None
                True

        Set to expressions or none.

        Returns list of expressions or none.
        '''
        if self._expressions is not None:
            return list(self._expressions)

    @property
    def to_pitch_classes(self):
        r'''Is true when specifier changes pitches to pitch-classes.
        Otherwise false.

        ..  note:: Applies prior to expressions.

        ..  container:: example

            Example figure:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(segment_list, 'Voice 1')
                >>> lilypond_file = figure_maker.make(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
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
                            }
                        }
                    }
                >>

        ..  container:: example

            Changes pitches to pitch-classes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.FigurePitchSpecifier(
                ...         to_pitch_classes=True,
                ...         ),
                ...     )

            ::

                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(segment_list, 'Voice 1')
                >>> lilypond_file = figure_maker.make(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs'16 [
                                e'16
                                ef'16
                                af'16
                                g'16 ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example
        
            ::

                >>> specifier = baca.tools.FigurePitchSpecifier(
                ...     to_pitch_classes=True,
                ...     )
                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> for segment in specifier(segment_list):
                ...     segment
                ...
                PitchClassSegment([0, 2, 10])
                PitchClassSegment([6, 4, 3, 8, 7])
                PitchClassSegment([9])

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier()
                >>> specifier.to_pitch_classes is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._to_pitch_classes

    @property
    def remove_duplicate_pitch_classes(self):
        r'''Is true when specifier removes duplicate pitch-classes.

        ..  container:: example

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier(
                ...     remove_duplicate_pitch_classes=True
                ...     )
                >>> segment_list = [[0, 2, 10], [18, 16, 15, 22, 19], [9]]
                >>> for segment in specifier(segment_list):
                ...     segment
                ...
                PitchSegment([0, 2, 10])
                PitchSegment([18, 16, 15, 22, 19])
                PitchSegment([9])

            ..  note:: Make this remove the 22.

        Returns true, false or none.
        '''
        return self._remove_duplicate_pitch_classes

    @property
    def remove_duplicate_pitches(self):
        r'''Is true when specifier removes duplicate pitches.

        ..  container:: example

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier(
                ...     remove_duplicate_pitch_classes=True
                ...     )
                >>> segment_list = [[0, 2, 10], [18, 16, 15, 10, 19], [9]]
                >>> for segment in specifier(segment_list):
                ...     segment
                ...
                PitchSegment([0, 2, 10])
                PitchSegment([18, 16, 15, 10, 19])
                PitchSegment([9])

            ..  note:: Make this remove the second 10.

        Returns true, false or none.
        '''
        return self._remove_duplicate_pitches
