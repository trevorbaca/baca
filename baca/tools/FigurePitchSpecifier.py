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
            >>> music_maker = baca.MusicMaker(
            ...     baca.tools.FigurePitchSpecifier(
            ...         expressions=[expression],
            ...         to_pitch_classes=True,
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
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
        '_remove_duplicates',
        '_to_pitch_classes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        expressions=None,
        remove_duplicate_pitch_classes=None,
        remove_duplicates=None,
        to_pitch_classes=None,
        ):
        self._expressions = expressions
        if to_pitch_classes is not None:
            to_pitch_classes = bool(to_pitch_classes)
        self._remove_duplicate_pitch_classes = remove_duplicate_pitch_classes
        self._remove_duplicates = remove_duplicates
        self._to_pitch_classes = to_pitch_classes

    ### SPECIAL METHODS ###

    def __call__(self, collections=None):
        r'''Calls specifier on `collections`.

        ..  container:: example

            Returns none when `collections` is none:

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier()
                >>> specifier() is None
                True

        ..  container:: example
        
            Returns sequence of numbered pitch collections by default:

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier()
                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> for collection in specifier(collections):
                ...     collection
                ...
                PitchSegment([0, 2, 10])
                PitchSegment([18, 16, 15, 20, 19])
                PitchSegment([9])

        Returns new collection list.
        '''
        if collections is None:
            return
        collections = baca.CollectionList(collections=collections)
        if self.to_pitch_classes:
            collections = collections.to_pitch_classes()
        collections = self._remove_duplicates_(collections)
        collections = self._apply_expressions(collections)
        return collections

    def __repr__(self):
        r'''Gets interpreter representation of specifier.

        ..  container:: example

            ::

                >>> baca.tools.FigurePitchSpecifier()
                FigurePitchSpecifier()

        Returns string.
        '''
        superclass = super(FigurePitchSpecifier, self)
        return superclass.__repr__()

    ### PRIVATE METHODS ###

    def _apply_expressions(self, collections):
        sequence = baca.Sequence(items=collections)
        for expression in self.expressions or []:
            assert isinstance(expression, abjad.Expression), repr(expression)
            sequence = expression(sequence)
        return abjad.new(collections, collections=sequence)

    def _remove_duplicates_(self, collections):
        if self.remove_duplicates:
            collections = collections.remove_duplicates()
        if self.remove_duplicate_pitch_classes:
            collections = collections.remove_duplicate_pitch_classes()
        return collections

    def _to_pitch_tree(self, collections):
        item_class = None
        if self.to_pitch_classes:
            item_class = abjad.NumberedPitchClass
        return baca.tools.PitchTree(
            item_class=item_class,
            items=collections,
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
                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.FigurePitchSpecifier(
                ...         expressions=[transposition],
                ...         to_pitch_classes=True,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
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
    def remove_duplicate_pitch_classes(self):
        r'''Is true when specifier removes duplicate pitch-classes.

        ..  container:: example

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier(
                ...     remove_duplicate_pitch_classes=True
                ...     )
                >>> collections = [[0, 2, 10], [18, 16, 15, 22, 19], [9]]
                >>> for collection in specifier(collections):
                ...     collection
                ...
                PitchSegment([0, 2, 10])
                PitchSegment([18, 16, 15, 19])
                PitchSegment([9])

        Returns true, false or none.
        '''
        return self._remove_duplicate_pitch_classes

    @property
    def remove_duplicates(self):
        r'''Is true when specifier removes duplicates.

        ..  container:: example

            ::

                >>> specifier = baca.tools.FigurePitchSpecifier(
                ...     remove_duplicates=True
                ...     )
                >>> collections = [[0, 2, 10], [18, 16, 15, 10, 19], [9]]
                >>> for collection in specifier(collections):
                ...     collection
                ...
                PitchSegment([0, 2, 10])
                PitchSegment([18, 16, 15, 19])
                PitchSegment([9])

        Returns true, false or none.
        '''
        return self._remove_duplicates

    @property
    def to_pitch_classes(self):
        r'''Is true when specifier changes pitches to pitch-classes.
        Otherwise false.

        ..  note:: Applies prior to expressions.

        ..  container:: example

            Example figure:

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
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
                            }
                        }
                    }
                >>

        ..  container:: example

            Changes pitches to pitch-classes:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.FigurePitchSpecifier(
                ...         to_pitch_classes=True,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker('Voice 1', collections)
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
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
                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> for collection in specifier(collections):
                ...     collection
                ...
                PitchClassSegment([0, 2, 10])
                PitchClassSegment([6, 4, 3, 8, 7])
                PitchClassSegment([9])

        ..  container:: example
        
            ::

                >>> specifier = baca.tools.FigurePitchSpecifier(
                ...     to_pitch_classes=True,
                ...     )
                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> collections = baca.CollectionList(collections)
                >>> for collection in specifier(collections):
                ...     collection
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
