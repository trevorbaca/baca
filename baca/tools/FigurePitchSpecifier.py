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

            >>> # expression = baca.sequence().accumulate([transposition])
            >>> transposition = baca.pitch_class_segment().transpose(n=3)
            >>> transposition = baca.sequence().map(transposition)
            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.FigurePitchSpecifier(
            ...         expressions=[transposition],
            ...         to_pitch_classes=True,
            ...         ),
            ...     )

        ::

            >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> result = figure_maker(figure_token)
            >>> selection, time_signature, state_manifest = result
            >>> lilypond_file = rhythmmakertools.make_lilypond_file([selection])
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new Staff {
                {
                    \time 9/16
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
            }

    Figure pitch specifiers tell figure-makers what to do with figure tokens.

    Figure-makers interpret figure pitch specifiers prior to other specifiers.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Figures'

    __slots__ = (
        '_expressions',
        '_to_pitch_classes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        expressions=None,
        to_pitch_classes=None,
        ):
        self._expressions = expressions
        if to_pitch_classes is not None:
            to_pitch_classes = bool(to_pitch_classes)
        self._to_pitch_classes = to_pitch_classes

    ### SPECIAL METHODS ###

    def __call__(self, figure_token=None):
        r'''Calls specifier on `figure_token`.

        Returns new figure token.
        '''
        if figure_token is None:
            return
        figure_token = self._to_pitch_class_segments(figure_token)
        assert isinstance(figure_token, baca.Sequence), repr(figure_token)
        for expression in self.expressions or []:
            assert isinstance(expression, abjad.Expression), repr(expression)
            figure_token = expression(figure_token)
        return figure_token

    def __repr__(self, figure_token=None):
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

    def _to_pitch_class_segments(self, figure_token):
        segments = []
        for list_ in figure_token:
            segment = baca.PitchClassSegment(items=list_)
            segments.append(segment)
        return baca.Sequence(items=segments)

    def _to_pitch_tree(self, figure_token):
        item_class = None
        if self.to_pitch_classes:
            item_class = abjad.NumberedPitchClass
        return baca.tools.PitchTree(
            item_class=item_class,
            items=figure_token,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def expressions(self):
        r'''Gets expressions.

        ..  container:: example

            Transposes pitches:

            ::

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> transposition = baca.sequence().map(transposition)
                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.FigurePitchSpecifier(
                ...         expressions=[transposition],
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file([selection])
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff {
                    {
                        \time 9/16
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
                }

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file([selection])
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff {
                    {
                        \time 9/16
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
                }

        ..  container:: example

            Changes pitches to pitch-classes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.FigurePitchSpecifier(
                ...         to_pitch_classes=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file([selection])
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff {
                    {
                        \time 9/16
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
                }

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
