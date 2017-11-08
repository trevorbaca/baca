import abjad


class ExpressionGallery(abjad.AbjadObject):
    r'''Expression gallery.

    ..  container:: example expression

        Transposes collections:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.Expression()
        >>> transposition = transposition.pitch_class_segment()
        >>> transposition = transposition.transpose(n=3)
        >>> expression = baca.sequence(name='J')
        >>> expression = expression.map(transposition)

        >>> for collection in expression(collections):
        ...     collection
        ...
        PitchClassSegment([3, 4, 5, 6])
        PitchClassSegment([9, 10, 11, 0])

        >>> expression.get_string()
        'T3(X) /@ J'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup)
            \markup {
                \line
                    {
                        \concat
                            {
                                T
                                \sub
                                    3
                                \bold
                                    X
                            }
                        /@
                        \bold
                            J
                    }
                }

    ..  container:: example expression

        Transposes and joins:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.Expression()
        >>> transposition = transposition.pitch_class_segment()
        >>> transposition = transposition.transpose(n=3)
        >>> expression = baca.sequence(name='J')
        >>> expression = expression.map(transposition)
        >>> expression = expression.join()

        >>> expression(collections)
        Sequence([PitchClassSegment([3, 4, 5, 6, 9, 10, 11, 0])])

        >>> expression.get_string()
        'join(T3(X) /@ J)'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup)
            \markup {
                \concat
                    {
                        join(
                        \line
                            {
                                \concat
                                    {
                                        T
                                        \sub
                                            3
                                        \bold
                                            X
                                    }
                                /@
                                \bold
                                    J
                            }
                        )
                    }
                }

    ..  container:: example expression

        Transposes and flattens:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.Expression()
        >>> transposition = transposition.pitch_class_segment()
        >>> transposition = transposition.transpose(n=3)
        >>> expression = baca.sequence(name='J')
        >>> expression = expression.map(transposition)
        >>> expression = expression.flatten(depth=-1)

        >>> for collection in expression(collections):
        ...     collection
        ...
        NumberedPitchClass(3)
        NumberedPitchClass(4)
        NumberedPitchClass(5)
        NumberedPitchClass(6)
        NumberedPitchClass(9)
        NumberedPitchClass(10)
        NumberedPitchClass(11)
        NumberedPitchClass(0)

        >>> expression.get_string()
        'flatten(T3(X) /@ J, depth=-1)'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup)
            \markup {
                \concat
                    {
                        flatten(
                        \line
                            {
                                \concat
                                    {
                                        T
                                        \sub
                                            3
                                        \bold
                                            X
                                    }
                                /@
                                \bold
                                    J
                            }
                        ", depth=-1)"
                    }
                }

    ..  container:: example expression

        Transposes and repartitions:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment().transpose(n=3)
        >>> expression = baca.sequence(name='J').map(transposition)
        >>> expression = expression.flatten(depth=-1).partition([3])
        >>> expression = expression.pitch_class_segments()

        >>> for collection in expression(collections):
        ...     collection
        ...
        PitchClassSegment([3, 4, 5])
        PitchClassSegment([6, 9, 10])
        PitchClassSegment([11, 0])

        >>> expression.get_string()
        'X /@ P[3](flatten(T3(X) /@ J, depth=-1))'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup)
            \markup {
                \line
                    {
                        \bold
                            X
                        /@
                        \concat
                            {
                                P
                                \sub
                                    [3]
                                \concat
                                    {
                                        flatten(
                                        \line
                                            {
                                                \concat
                                                    {
                                                        T
                                                        \sub
                                                            3
                                                        \bold
                                                            X
                                                    }
                                                /@
                                                \bold
                                                    J
                                            }
                                        ", depth=-1)"
                                    }
                            }
                    }
                }

    ..  container:: example expression

        Transposes, repartitions and ox-plows:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment().transpose(n=3)
        >>> expression = baca.sequence(name='J').map(transposition)
        >>> expression = expression.flatten(depth=-1).partition([3])
        >>> expression = expression.pitch_class_segments()
        >>> expression = expression.boustrophedon()

        >>> for collection in expression(collections):
        ...     collection
        ...
        PitchClassSegment([3, 4, 5])
        PitchClassSegment([6, 9, 10])
        PitchClassSegment([11, 0])
        PitchClassSegment([11])
        PitchClassSegment([10, 9, 6])
        PitchClassSegment([5, 4, 3])

        >>> expression.get_string()
        'β2(X /@ P[3](flatten(T3(X) /@ J, depth=-1)))'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup)
            \markup {
                \concat
                    {
                        β
                        \super
                            2
                        \line
                            {
                                \bold
                                    X
                                /@
                                \concat
                                    {
                                        P
                                        \sub
                                            [3]
                                        \concat
                                            {
                                                flatten(
                                                \line
                                                    {
                                                        \concat
                                                            {
                                                                T
                                                                \sub
                                                                    3
                                                                \bold
                                                                    X
                                                            }
                                                        /@
                                                        \bold
                                                            J
                                                    }
                                                ", depth=-1)"
                                            }
                                    }
                            }
                    }
                }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'
