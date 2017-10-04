import abjad
import baca
import collections
import copy
import inspect
import itertools


class Sequence(abjad.Sequence):
    r'''Sequence.

    ..  container:: example

        Initializes from numbers:

        ..  container:: example

            ::

                >>> baca.Sequence([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            ::

                >>> expression = baca.sequence()

            ::

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes from collection:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> collection = abjad.PitchClassSegment(items=items)
                >>> show(collection) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = collection.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            ::

                >>> baca.sequence(items=collection)
                Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

        ..  container:: example expression

            ::

                >>> expression = baca.sequence()

            ::

                >>> expression(items=collection)
                Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

    ..  container:: example

        Maps transposition to multiple collections:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> collection = abjad.PitchClassSegment(items=items)
                >>> collections = [
                ...     abjad.PitchClassSegment(items=[-2, -1.5, 6]),
                ...     abjad.PitchClassSegment(items=[7, -1.5, 7]),
                ...     ]

            ::

                >>> expression = baca.Expression()
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.transpose(n=1)

            ::

                >>> sequence = baca.Sequence(collections)
                >>> sequence = sequence.map(expression)
                >>> sequence.join()
                Sequence([PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])])

            ::

                >>> collection = sequence.join()[0]
                >>> show(collection) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = collection.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            ::

                >>> collections = [
                ...     baca.PitchClassSegment(items=[-2, -1.5, 6]),
                ...     baca.PitchClassSegment(items=[7, -1.5, 7]),
                ...     ]

            ::

                >>> transposition = baca.Expression()
                >>> transposition = transposition.pitch_class_segment()
                >>> transposition = transposition.transpose(n=1)
                >>> expression = baca.sequence(name='J')
                >>> expression = expression.map(transposition)
                >>> expression = expression.join()

            ::

                >>> expression(collections)
                Sequence([PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])])

            ::

                >>> expression.get_string()
                'join(T1(X) /@ J)'

            ::

                >>> collection = expression(collections)[0]
                >>> markup = expression.get_markup()
                >>> show(collection, figure_name=markup) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = collection.__illustrate__(
                ...     figure_name=markup,
                ...     )
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    b'8
                        ^ \markup {
                            \concat
                                {
                                    join(
                                    \line
                                        {
                                            \concat
                                                {
                                                    T
                                                    \sub
                                                        1
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
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_accumulate_markup(markup, operands=None, count=None):
        import abjad
        if count is None:
            count = abjad.Identity
        markup_list = abjad.MarkupList()
        operands = operands or [abjad.Identity]
        operand_markups = []
        for operand in operands:
            if hasattr(operand, 'get_markup'):
                operand_markup = operand.get_markup(name='X')
            else:
                operand_markup = str(operand)
            operand_markups.append(operand_markup)
        operand_markup = abjad.MarkupList(operand_markups).concat()
        markup_list.append(operand_markup)
        infix = 'Φ'
        if count != abjad.Identity:
            infix += '/' + str(count)
        markup_list.append(infix)
        markup_list.append(markup)
        markup = markup_list.line()
        return markup

    @staticmethod
    def _make_accumulate_string_template(operands=None, count=None):
        if count is None:
            count = abjad.Identity
        operands = operands or [abjad.Identity]
        operand_strings = []
        for operand in operands:
            if hasattr(operand, 'get_string'):
                operand_string = operand.get_string(name='X')
            else:
                operand_string = str(operand)
            operand_strings.append(operand_string)
        if len(operand_strings) == 1:
            operands = operand_strings[0]
        else:
            operands = ', '.join(operand_strings)
            operands = '[' + operands + ']'
        if count == abjad.Identity:
            string_template = '{} Φ {{}}'.format(operands)
        else:
            string_template = '{} Φ/{} {{}}'
            string_template = string_template.format(operands, count)
        return string_template

    def _update_expression(
        self,
        frame,
        evaluation_template=None,
        map_operand=None,
        subclass_hook=None,
        ):
        import baca
        callback = baca.Expression._frame_to_callback(
            frame,
            evaluation_template=evaluation_template,
            map_operand=map_operand,
            subclass_hook=subclass_hook,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC METHODS ###

    @abjad.Signature(
        markup_maker_callback='_make_accumulate_markup',
        string_template_callback='_make_accumulate_string_template',
        )
    def accumulate(self, operands=None, count=None):
        r'''Accumulates `operands` calls against sequence to identity.

        ..  container:: example

            Accumulates identity operator:

            ..  container:: example

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])
                    >>> baca.Sequence(items=[collection_1, collection_2])
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> sequence = baca.Sequence(items=[collection_1, collection_2])
                    >>> for item in sequence.accumulate():
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

            ..  container:: example expression

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])

                ::

                    >>> expression = baca.sequence(name='J').accumulate()

                ::

                    >>> for item in expression([collection_1, collection_2]):
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> expression.get_string()
                    'Identity Φ J'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        Identity
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates alpha:

            ..  container:: example

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])
                    >>> baca.Sequence(items=[collection_1, collection_2])
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> alpha = baca.pitch_class_segment().alpha()

                ::

                    >>> sequence = baca.Sequence(items=[collection_1, collection_2])
                    >>> for item in sequence.accumulate([alpha]):
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])

            ..  container:: example expression

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])

                ::

                    >>> alpha = baca.pitch_class_segment().alpha()
                    >>> expression = baca.sequence(name='J').accumulate([alpha])

                ::

                    >>> for sequence in expression([collection_1, collection_2]):
                    ...     sequence
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])

                ::

                    >>> expression.get_string()
                    'A(X) Φ J'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                A
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates transposition:

            ..  container:: example

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])
                    >>> baca.Sequence(items=[collection_1, collection_2])
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> transposition = baca.Expression()
                    >>> transposition = transposition.pitch_class_segment()
                    >>> transposition = transposition.transpose(n=3)

                ::

                    >>> sequence = baca.Sequence(items=[collection_1, collection_2])
                    >>> for item in sequence.accumulate([transposition]):
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([3, 4, 5, 6]), PitchClassSegment([7, 8])])
                    Sequence([PitchClassSegment([6, 7, 8, 9]), PitchClassSegment([10, 11])])
                    Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

            ..  container:: example expression

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])

                ::

                    >>> transposition = baca.pitch_class_segment().transpose(n=3)
                    >>> expression = baca.sequence(name='J').accumulate(
                    ...     [transposition],
                    ...     )

                ::

                    >>> for sequence in expression([collection_1, collection_2]):
                    ...     sequence
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([3, 4, 5, 6]), PitchClassSegment([7, 8])])
                    Sequence([PitchClassSegment([6, 7, 8, 9]), PitchClassSegment([10, 11])])
                    Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

                ::

                    >>> expression.get_string()
                    'T3(X) Φ J'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                T
                                                \sub
                                                    3
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates alpha followed by transposition:

            ..  container:: example

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])
                    >>> baca.Sequence(items=[collection_1, collection_2])
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> transposition = baca.Expression()
                    >>> transposition = transposition.pitch_class_segment()
                    >>> transposition = transposition.transpose(n=3)
                    >>> alpha = baca.Expression()
                    >>> alpha = alpha.pitch_class_segment()
                    >>> alpha = alpha.alpha()

                ::

                    >>> sequence = baca.Sequence(items=[collection_1, collection_2])
                    >>> for item in sequence.accumulate([alpha, transposition]):
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])
                    Sequence([PitchClassSegment([4, 3, 6, 5]), PitchClassSegment([8, 7])])
                    Sequence([PitchClassSegment([5, 2, 7, 4]), PitchClassSegment([9, 6])])
                    Sequence([PitchClassSegment([8, 5, 10, 7]), PitchClassSegment([0, 9])])
                    Sequence([PitchClassSegment([9, 4, 11, 6]), PitchClassSegment([1, 8])])
                    Sequence([PitchClassSegment([0, 7, 2, 9]), PitchClassSegment([4, 11])])
                    Sequence([PitchClassSegment([1, 6, 3, 8]), PitchClassSegment([5, 10])])
                    Sequence([PitchClassSegment([4, 9, 6, 11]), PitchClassSegment([8, 1])])
                    Sequence([PitchClassSegment([5, 8, 7, 10]), PitchClassSegment([9, 0])])
                    Sequence([PitchClassSegment([8, 11, 10, 1]), PitchClassSegment([0, 3])])
                    Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

            ..  container:: example expression

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])

                ::

                    >>> alpha = baca.pitch_class_segment().alpha()
                    >>> transposition = baca.pitch_class_segment().transpose(n=3)
                    >>> expression = baca.sequence(name='J').accumulate(
                    ...     [alpha, transposition],
                    ...     )

                ::

                    >>> for sequence in expression([collection_1, collection_2]):
                    ...     sequence
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])
                    Sequence([PitchClassSegment([4, 3, 6, 5]), PitchClassSegment([8, 7])])
                    Sequence([PitchClassSegment([5, 2, 7, 4]), PitchClassSegment([9, 6])])
                    Sequence([PitchClassSegment([8, 5, 10, 7]), PitchClassSegment([0, 9])])
                    Sequence([PitchClassSegment([9, 4, 11, 6]), PitchClassSegment([1, 8])])
                    Sequence([PitchClassSegment([0, 7, 2, 9]), PitchClassSegment([4, 11])])
                    Sequence([PitchClassSegment([1, 6, 3, 8]), PitchClassSegment([5, 10])])
                    Sequence([PitchClassSegment([4, 9, 6, 11]), PitchClassSegment([8, 1])])
                    Sequence([PitchClassSegment([5, 8, 7, 10]), PitchClassSegment([9, 0])])
                    Sequence([PitchClassSegment([8, 11, 10, 1]), PitchClassSegment([0, 3])])
                    Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

                ::

                    >>> expression.get_string()
                    '[A(X), T3(X)] Φ J'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                A
                                                \bold
                                                    X
                                            }
                                        \concat
                                            {
                                                T
                                                \sub
                                                    3
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates permutation:

            ..  container:: example

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])
                    >>> baca.Sequence(items=[collection_1, collection_2])
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> permutation = baca.Expression()
                    >>> permutation = permutation.pitch_class_segment()
                    >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                    >>> permutation = permutation.permute(row)

                ::

                    >>> sequence = baca.Sequence(items=[collection_1, collection_2])
                    >>> for item in sequence.accumulate([permutation]):
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                    Sequence([PitchClassSegment([4, 10, 2, 5]), PitchClassSegment([1, 3])])
                    Sequence([PitchClassSegment([8, 4, 2, 7]), PitchClassSegment([0, 6])])
                    Sequence([PitchClassSegment([1, 8, 2, 3]), PitchClassSegment([10, 5])])
                    Sequence([PitchClassSegment([0, 1, 2, 6]), PitchClassSegment([4, 7])])
                    Sequence([PitchClassSegment([10, 0, 2, 5]), PitchClassSegment([8, 3])])
                    Sequence([PitchClassSegment([4, 10, 2, 7]), PitchClassSegment([1, 6])])
                    Sequence([PitchClassSegment([8, 4, 2, 3]), PitchClassSegment([0, 5])])
                    Sequence([PitchClassSegment([1, 8, 2, 6]), PitchClassSegment([10, 7])])
                    Sequence([PitchClassSegment([0, 1, 2, 5]), PitchClassSegment([4, 3])])
                    Sequence([PitchClassSegment([10, 0, 2, 7]), PitchClassSegment([8, 6])])
                    Sequence([PitchClassSegment([4, 10, 2, 3]), PitchClassSegment([1, 5])])
                    Sequence([PitchClassSegment([8, 4, 2, 6]), PitchClassSegment([0, 7])])
                    Sequence([PitchClassSegment([1, 8, 2, 5]), PitchClassSegment([10, 3])])
                    Sequence([PitchClassSegment([0, 1, 2, 7]), PitchClassSegment([4, 6])])
                    Sequence([PitchClassSegment([10, 0, 2, 3]), PitchClassSegment([8, 5])])
                    Sequence([PitchClassSegment([4, 10, 2, 6]), PitchClassSegment([1, 7])])
                    Sequence([PitchClassSegment([8, 4, 2, 5]), PitchClassSegment([0, 3])])
                    Sequence([PitchClassSegment([1, 8, 2, 7]), PitchClassSegment([10, 6])])

            ..  container:: example expression

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])

                ::

                    >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                    >>> permutation = baca.pitch_class_segment().permute(row)
                    >>> expression = baca.sequence(name='J').accumulate(
                    ...     [permutation],
                    ...     )

                ::

                    >>> for sequence in expression([collection_1, collection_2]):
                    ...     sequence
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                    Sequence([PitchClassSegment([4, 10, 2, 5]), PitchClassSegment([1, 3])])
                    Sequence([PitchClassSegment([8, 4, 2, 7]), PitchClassSegment([0, 6])])
                    Sequence([PitchClassSegment([1, 8, 2, 3]), PitchClassSegment([10, 5])])
                    Sequence([PitchClassSegment([0, 1, 2, 6]), PitchClassSegment([4, 7])])
                    Sequence([PitchClassSegment([10, 0, 2, 5]), PitchClassSegment([8, 3])])
                    Sequence([PitchClassSegment([4, 10, 2, 7]), PitchClassSegment([1, 6])])
                    Sequence([PitchClassSegment([8, 4, 2, 3]), PitchClassSegment([0, 5])])
                    Sequence([PitchClassSegment([1, 8, 2, 6]), PitchClassSegment([10, 7])])
                    Sequence([PitchClassSegment([0, 1, 2, 5]), PitchClassSegment([4, 3])])
                    Sequence([PitchClassSegment([10, 0, 2, 7]), PitchClassSegment([8, 6])])
                    Sequence([PitchClassSegment([4, 10, 2, 3]), PitchClassSegment([1, 5])])
                    Sequence([PitchClassSegment([8, 4, 2, 6]), PitchClassSegment([0, 7])])
                    Sequence([PitchClassSegment([1, 8, 2, 5]), PitchClassSegment([10, 3])])
                    Sequence([PitchClassSegment([0, 1, 2, 7]), PitchClassSegment([4, 6])])
                    Sequence([PitchClassSegment([10, 0, 2, 3]), PitchClassSegment([8, 5])])
                    Sequence([PitchClassSegment([4, 10, 2, 6]), PitchClassSegment([1, 7])])
                    Sequence([PitchClassSegment([8, 4, 2, 5]), PitchClassSegment([0, 3])])
                    Sequence([PitchClassSegment([1, 8, 2, 7]), PitchClassSegment([10, 6])])

                ::

                    >>> expression.get_string()
                    'permute(X, row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]) Φ J'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                permute(
                                                \bold
                                                    X
                                                ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates permutation followed by transposition:

            ..  container:: example

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])
                    >>> baca.Sequence(items=[collection_1, collection_2])
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                ::

                    >>> permutation = baca.Expression()
                    >>> permutation = permutation.pitch_class_segment()
                    >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                    >>> permutation = permutation.permute(row)
                    >>> transposition = baca.Expression()
                    >>> transposition = transposition.pitch_class_segment()
                    >>> transposition = transposition.transpose(n=3)

                ::

                    >>> sequence = baca.Sequence(items=[collection_1, collection_2])
                    >>> for item in sequence.accumulate(
                    ...     [permutation, transposition],
                    ...     ):
                    ...     item
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                    Sequence([PitchClassSegment([1, 3, 5, 9]), PitchClassSegment([11, 10])])
                    Sequence([PitchClassSegment([0, 6, 7, 9]), PitchClassSegment([11, 4])])
                    Sequence([PitchClassSegment([3, 9, 10, 0]), PitchClassSegment([2, 7])])
                    Sequence([PitchClassSegment([6, 9, 4, 10]), PitchClassSegment([2, 3])])
                    Sequence([PitchClassSegment([9, 0, 7, 1]), PitchClassSegment([5, 6])])
                    Sequence([PitchClassSegment([9, 10, 3, 0]), PitchClassSegment([7, 5])])
                    Sequence([PitchClassSegment([0, 1, 6, 3]), PitchClassSegment([10, 8])])
                    Sequence([PitchClassSegment([10, 0, 5, 6]), PitchClassSegment([4, 1])])
                    Sequence([PitchClassSegment([1, 3, 8, 9]), PitchClassSegment([7, 4])])
                    Sequence([PitchClassSegment([0, 6, 1, 9]), PitchClassSegment([3, 8])])
                    Sequence([PitchClassSegment([3, 9, 4, 0]), PitchClassSegment([6, 11])])
                    Sequence([PitchClassSegment([6, 9, 8, 10]), PitchClassSegment([5, 11])])
                    Sequence([PitchClassSegment([9, 0, 11, 1]), PitchClassSegment([8, 2])])
                    Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

            ..  container:: example expression

                ::

                    >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                    >>> collection_2 = baca.PitchClassSegment([4, 5])

                ::

                    >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                    >>> permutation = baca.pitch_class_segment().permute(row)
                    >>> transposition = baca.pitch_class_segment().transpose(n=3)
                    >>> expression = baca.sequence(name='J').accumulate(
                    ...     [permutation, transposition],
                    ...     )

                ::

                    >>> for sequence in expression([collection_1, collection_2]):
                    ...     sequence
                    ...
                    Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                    Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                    Sequence([PitchClassSegment([1, 3, 5, 9]), PitchClassSegment([11, 10])])
                    Sequence([PitchClassSegment([0, 6, 7, 9]), PitchClassSegment([11, 4])])
                    Sequence([PitchClassSegment([3, 9, 10, 0]), PitchClassSegment([2, 7])])
                    Sequence([PitchClassSegment([6, 9, 4, 10]), PitchClassSegment([2, 3])])
                    Sequence([PitchClassSegment([9, 0, 7, 1]), PitchClassSegment([5, 6])])
                    Sequence([PitchClassSegment([9, 10, 3, 0]), PitchClassSegment([7, 5])])
                    Sequence([PitchClassSegment([0, 1, 6, 3]), PitchClassSegment([10, 8])])
                    Sequence([PitchClassSegment([10, 0, 5, 6]), PitchClassSegment([4, 1])])
                    Sequence([PitchClassSegment([1, 3, 8, 9]), PitchClassSegment([7, 4])])
                    Sequence([PitchClassSegment([0, 6, 1, 9]), PitchClassSegment([3, 8])])
                    Sequence([PitchClassSegment([3, 9, 4, 0]), PitchClassSegment([6, 11])])
                    Sequence([PitchClassSegment([6, 9, 8, 10]), PitchClassSegment([5, 11])])
                    Sequence([PitchClassSegment([9, 0, 11, 1]), PitchClassSegment([8, 2])])
                    Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

                ::

                    >>> expression.get_string()
                    '[permute(X, row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]), T3(X)] Φ J'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                permute(
                                                \bold
                                                    X
                                                ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                                            }
                                        \concat
                                            {
                                                T
                                                \sub
                                                    3
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        Returns sequence of accumulated sequences.

        Returns sequence of length `count` + 1 with integer `count`.

        Returns sequence of orbit length with `count` set to identity.
        '''
        if count is None:
            count = abjad.Identity
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='accumulate',
                subclass_hook='_evaluate_accumulate',
                map_operand=operands,
                )
        operands = operands or [baca.Expression()]
        if not isinstance(operands, list):
            operands = [operands]
        items = [self]
        if count == abjad.Identity:
            for i in range(1000):
                sequence = items[-1]
                for operand in operands:
                    sequence = sequence.map(operand)
                    items.append(sequence)
                if sequence == items[0]:
                    items.pop(-1)
                    break
            else:
                message = '1000 iterations without identity: {!r} to {!r}.'
                message = message.format(items[0], items[-1])
                raise Exception(message)
        else:
            for i in range(count - 1):
                sequence = items[-1]
                for operand in operands:
                    sequence = sequence.map(operand)
                    items.append(sequence)
        return type(self)(items=items)

    @abjad.Signature(
        method_name='β',
        is_operator=True,
        superscript='count',
        )
    def boustrophedon(self, count=2):
        r'''Iterates sequence boustrophedon.

        ..  container:: example

            Iterates atoms boustrophedon:

            ::

                >>> sequence = baca.Sequence([1, 2, 3, 4, 5])

            ::

                >>> sequence.boustrophedon(count=0)
                Sequence([])

            ::

                >>> sequence.boustrophedon(count=1)
                Sequence([1, 2, 3, 4, 5])

            ::

                >>> sequence.boustrophedon(count=2)
                Sequence([1, 2, 3, 4, 5, 4, 3, 2, 1])

            ::

                >>> sequence.boustrophedon(count=3)
                Sequence([1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5])

        ..  container:: example

            Iterates collections boustrophedon:

            ::

                >>> collections = [
                ...     baca.PitchClassSegment([1, 2, 3]),
                ...     baca.PitchClassSegment([4, 5, 6]),
                ...     ]
                >>> sequence = baca.Sequence(collections)

            ::

                >>> sequence.boustrophedon(count=0)
                Sequence([])

            ::

                >>> for collection in sequence.boustrophedon(count=1):
                ...     collection
                ...
                PitchClassSegment([1, 2, 3])
                PitchClassSegment([4, 5, 6])

            ::

                >>> for collection in sequence.boustrophedon(count=2):
                ...     collection
                ...
                PitchClassSegment([1, 2, 3])
                PitchClassSegment([4, 5, 6])
                PitchClassSegment([5, 4])
                PitchClassSegment([3, 2, 1])

            ::

                >>> for collection in sequence.boustrophedon(count=3):
                ...     collection
                ...
                PitchClassSegment([1, 2, 3])
                PitchClassSegment([4, 5, 6])
                PitchClassSegment([5, 4])
                PitchClassSegment([3, 2, 1])
                PitchClassSegment([2, 3])
                PitchClassSegment([4, 5, 6])

        ..  container:: example

            Iterates mixed items boustrophedon:

            ::

                >>> collection = baca.PitchClassSegment([1, 2, 3])
                >>> sequence = baca.Sequence([collection, 4, 5])
                >>> for item in sequence.boustrophedon(count=3):
                ...     item
                ...
                PitchClassSegment([1, 2, 3])
                4
                5
                4
                PitchClassSegment([3, 2, 1])
                PitchClassSegment([2, 3])
                4
                5

        ..  container:: example expression

            ::

                >>> collections = [
                ...     baca.PitchClassSegment([1, 2, 3]),
                ...     baca.PitchClassSegment([4, 5, 6]),
                ...     ]

            ::

                >>> expression = baca.sequence(name='J')
                >>> expression = expression.boustrophedon(count=3)

            ::

                >>> for collection in expression(collections):
                ...     collection
                ...
                PitchClassSegment([1, 2, 3])
                PitchClassSegment([4, 5, 6])
                PitchClassSegment([5, 4])
                PitchClassSegment([3, 2, 1])
                PitchClassSegment([2, 3])
                PitchClassSegment([4, 5, 6])

            ::

                >>> expression.get_string()
                'β3(J)'

            ::

                >>> markup = expression.get_markup()
                >>> show(markup) # doctest: +SKIP

            ..  docs::

                >>> f(markup)
                \markup {
                    \concat
                        {
                            β
                            \super
                                3
                            \bold
                                J
                        }
                    }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        for i in range(count):
            if i == 0:
                for item in self:
                    result.append(copy.copy(item))
            elif i % 2 == 0:
                if isinstance(self[0], collections.Iterable):
                    result.append(self[0][1:])
                else:
                    pass
                for item in self[1:]:
                    result.append(copy.copy(item))
            else:
                if isinstance(self[-1], collections.Iterable):
                    item = type(self[-1])(list(reversed(self[-1]))[1:])
                    result.append(item)
                else:
                    pass
                for item in reversed(self[:-1]):
                    if isinstance(item, collections.Iterable):
                        item = type(item)(list(reversed(item)))
                        result.append(item)
                    else:
                        result.append(item)
        return type(self)(items=result)

    def get_degree_of_rotational_symmetry(self):
        '''Gets degree of rotational symmetry.

        ..  container:: example

            ::

                >>> baca.Sequence([1, 1, 1, 1, 1, 1]).get_degree_of_rotational_symmetry()
                6

            ::

                >>> baca.Sequence([1, 2, 1, 2, 1, 2]).get_degree_of_rotational_symmetry()
                3

            ::

                >>> baca.Sequence([1, 2, 3, 1, 2, 3]).get_degree_of_rotational_symmetry()
                2

            ::

                >>> baca.Sequence([1, 2, 3, 4, 5, 6]).get_degree_of_rotational_symmetry()
                1

            ::

                >>> baca.Sequence().get_degree_of_rotational_symmetry()
                1

        Returns positive integer.
        '''
        degree_of_rotational_symmetry = 0
        for index in range(len(self)):
            rotation = self[index:] + self[:index]
            if rotation == self:
                degree_of_rotational_symmetry += 1
        degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
        return degree_of_rotational_symmetry

    def get_period_of_rotation(self):
        '''Gets period of rotation.

        ..  container:: example

            ::

                >>> baca.Sequence([1, 2, 3, 4, 5, 6]).get_period_of_rotation()
                6

            ::

                >>> baca.Sequence([1, 2, 3, 1, 2, 3]).get_period_of_rotation()
                3

            ::

                >>> baca.Sequence([1, 2, 1, 2, 1, 2]).get_period_of_rotation()
                2

            ::

                >>> baca.Sequence([1, 1, 1, 1, 1, 1]).get_period_of_rotation()
                1

            ::

                >>> baca.Sequence().get_period_of_rotation()
                0

        Defined equal to length of sequence divided by degree of rotational
        symmetry of sequence.

        Returns positive integer.
        '''
        return len(self) // self.get_degree_of_rotational_symmetry()

    def group_by_sign(self, sign=(-1, 0, 1)):
        r'''Groups sequence by sign of items.

        ::

            >>> sequence = baca.Sequence(
            ...     [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6],
            ...     )

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign():
                ...     item
                ...
                Sequence([0, 0])
                Sequence([-1, -1])
                Sequence([2, 3])
                Sequence([-5])
                Sequence([1, 2, 5])
                Sequence([-5, -6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([-1]):
                ...     item
                ...
                Sequence([0])
                Sequence([0])
                Sequence([-1, -1])
                Sequence([2])
                Sequence([3])
                Sequence([-5])
                Sequence([1])
                Sequence([2])
                Sequence([5])
                Sequence([-5, -6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([0]):
                ...     item
                ...
                Sequence([0, 0])
                Sequence([-1])
                Sequence([-1])
                Sequence([2])
                Sequence([3])
                Sequence([-5])
                Sequence([1])
                Sequence([2])
                Sequence([5])
                Sequence([-5])
                Sequence([-6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([1]):
                ...     item
                ...
                Sequence([0])
                Sequence([0])
                Sequence([-1])
                Sequence([-1])
                Sequence([2, 3])
                Sequence([-5])
                Sequence([1, 2, 5])
                Sequence([-5])
                Sequence([-6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([-1, 0]):
                ...     item
                ...
                Sequence([0, 0])
                Sequence([-1, -1])
                Sequence([2])
                Sequence([3])
                Sequence([-5])
                Sequence([1])
                Sequence([2])
                Sequence([5])
                Sequence([-5, -6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([-1, 1]):
                ...     item
                ...
                Sequence([0])
                Sequence([0])
                Sequence([-1, -1])
                Sequence([2, 3])
                Sequence([-5])
                Sequence([1, 2, 5])
                Sequence([-5, -6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([0, 1]):
                ...     item
                ...
                Sequence([0, 0])
                Sequence([-1])
                Sequence([-1])
                Sequence([2, 3])
                Sequence([-5])
                Sequence([1, 2, 5])
                Sequence([-5])
                Sequence([-6])

        ..  container:: example

            ::

                >>> for item in sequence.group_by_sign([-1, 0, 1]):
                ...     item
                ...
                Sequence([0, 0])
                Sequence([-1, -1])
                Sequence([2, 3])
                Sequence([-5])
                Sequence([1, 2, 5])
                Sequence([-5, -6])

        Groups negative elements when ``-1`` in `sign`.

        Groups zero-valued elements When ``0`` in `sign`.

        Groups positive elements when ``1`` in `sign`.

        Returns nested sequence.
        '''
        items = []
        pairs = itertools.groupby(self, abjad.mathtools.sign)
        for current_sign, group in pairs:
            if current_sign in sign:
                items.append(type(self)(group))
            else:
                for item in group:
                    items.append(type(self)([item]))
        return type(self)(items=items)

    @abjad.Signature(method_name='H')
    def helianthate(self, n=0, m=0):
        r'''Helianthates sequence.

        ..  container:: example

            Helianthates list of lists:

            ..  container:: example

                ::

                    >>> sequence = baca.Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])
                    >>> sequence = sequence.helianthate(n=-1, m=1)
                    >>> for item in sequence:
                    ...     item
                    ...
                    [1, 2, 3]
                    [4, 5]
                    [6, 7, 8]
                    [5, 4]
                    [8, 6, 7]
                    [3, 1, 2]
                    [7, 8, 6]
                    [2, 3, 1]
                    [4, 5]
                    [1, 2, 3]
                    [5, 4]
                    [6, 7, 8]
                    [4, 5]
                    [8, 6, 7]
                    [3, 1, 2]
                    [7, 8, 6]
                    [2, 3, 1]
                    [5, 4]

            ..  container:: example expression


                ::

                    >>> expression = baca.sequence()
                    >>> expression = expression.helianthate(n=-1, m=1)

                ::

                    >>> sequence = expression([[1, 2, 3], [4, 5], [6, 7, 8]])
                    >>> for item in sequence:
                    ...     item
                    [1, 2, 3]
                    [4, 5]
                    [6, 7, 8]
                    [5, 4]
                    [8, 6, 7]
                    [3, 1, 2]
                    [7, 8, 6]
                    [2, 3, 1]
                    [4, 5]
                    [1, 2, 3]
                    [5, 4]
                    [6, 7, 8]
                    [4, 5]
                    [8, 6, 7]
                    [3, 1, 2]
                    [7, 8, 6]
                    [2, 3, 1]
                    [5, 4]

        ..  container:: example

            Helianthates list of collections:

            ..  container:: example

                ::

                    >>> J = baca.PitchClassSegment(items=[0, 2, 4])
                    >>> K = baca.PitchClassSegment(items=[5, 6])
                    >>> L = baca.PitchClassSegment(items=[7, 9, 11])
                    >>> sequence = baca.sequence([J, K, L])
                    >>> sequence = sequence.helianthate(n=-1, m=1)
                    >>> for collection in sequence:
                    ...     collection
                    ...
                    PitchClassSegment([0, 2, 4])
                    PitchClassSegment([5, 6])
                    PitchClassSegment([7, 9, 11])
                    PitchClassSegment([6, 5])
                    PitchClassSegment([11, 7, 9])
                    PitchClassSegment([4, 0, 2])
                    PitchClassSegment([9, 11, 7])
                    PitchClassSegment([2, 4, 0])
                    PitchClassSegment([5, 6])
                    PitchClassSegment([0, 2, 4])
                    PitchClassSegment([6, 5])
                    PitchClassSegment([7, 9, 11])
                    PitchClassSegment([5, 6])
                    PitchClassSegment([11, 7, 9])
                    PitchClassSegment([4, 0, 2])
                    PitchClassSegment([9, 11, 7])
                    PitchClassSegment([2, 4, 0])
                    PitchClassSegment([6, 5])

            ..  container:: example expression

                ::

                    >>> J = baca.PitchClassSegment(items=[0, 2, 4])
                    >>> K = baca.PitchClassSegment(items=[5, 6])
                    >>> L = baca.PitchClassSegment(items=[7, 9, 11])

                ::

                    >>> expression = baca.sequence()
                    >>> expression = expression.helianthate(n=-1, m=1)

                ::

                    >>> for collection in expression([J, K, L]):
                    ...     collection
                    ...
                    PitchClassSegment([0, 2, 4])
                    PitchClassSegment([5, 6])
                    PitchClassSegment([7, 9, 11])
                    PitchClassSegment([6, 5])
                    PitchClassSegment([11, 7, 9])
                    PitchClassSegment([4, 0, 2])
                    PitchClassSegment([9, 11, 7])
                    PitchClassSegment([2, 4, 0])
                    PitchClassSegment([5, 6])
                    PitchClassSegment([0, 2, 4])
                    PitchClassSegment([6, 5])
                    PitchClassSegment([7, 9, 11])
                    PitchClassSegment([5, 6])
                    PitchClassSegment([11, 7, 9])
                    PitchClassSegment([4, 0, 2])
                    PitchClassSegment([9, 11, 7])
                    PitchClassSegment([2, 4, 0])
                    PitchClassSegment([6, 5])

        ..  container:: example

            Trivial helianthation:

            ..  container:: example

                ::

                    >>> items = [[1, 2, 3], [4, 5], [6, 7, 8]]
                    >>> sequence = baca.sequence(items)
                    >>> sequence.helianthate()
                    Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence()
                    >>> expression = expression.helianthate()

                ::

                    >>> expression([[1, 2, 3], [4, 5], [6, 7, 8]])
                    Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        start = list(self[:])
        result = list(self[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m

        def _generalized_rotate(argument, n=0):
            if hasattr(argument, 'rotate'):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = type(self)(argument).rotate(n=n)
            argument = argument_type(argument)
            return argument
        i = 0
        while True:
            inner = [_generalized_rotate(_, m) for _ in self]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
            i += 1
            if i == 1000:
                message = '1000 iterations without identity.'
                raise Exception(message)
        return type(self)(items=result)

    @abjad.Signature(
        is_operator=True,
        method_name='P',
        subscript='counts',
        )
    def partition(self, counts=None):
        r'''Partitions sequence cyclically by `counts` with overhang.

        ..  container:: example

            ..  container:: example

                ::

                    >>> sequence = baca.Sequence(range(16))
                    >>> parts = sequence.partition([3])

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])
                    Sequence([15])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence(name='J').partition([3])

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])
                    Sequence([15])

                ::

                    >>> expression.get_string()
                    'P[3](J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                P
                                \sub
                                    [3]
                                \bold
                                    J
                            }
                        }


        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.partition_by_counts(
            counts=counts,
            cyclic=True,
            overhang=True,
            )

    @abjad.Signature()
    def reveal(self, count=None):
        r'''Reveals contents of sequence.

        ..  container:: example

            With no count:

            ..  container:: example

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal()
                    Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence(name='J').reveal()

                ::

                    >>> expression([[1, 2, 3], 4, [5, 6]])
                    Sequence([[1, 2, 3], 4, [5, 6]])

                ::

                    >>> expression.get_string()
                    'reveal(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            With zero count:

            ..  container:: example expression

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=0)
                    Sequence([])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence(name='J').reveal(count=0)

                ::

                    >>> expression([[1, 2, 3], 4, [5, 6]])
                    Sequence([])

                ::

                    >>> expression.get_string()
                    'reveal(J, count=0)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                ", count=0)"
                            }
                        }

        ..  container:: example

            With positive count:

            ..  container:: example

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=1)
                    Sequence([[1]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=2)
                    Sequence([[1, 2]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=3)
                    Sequence([[1, 2, 3]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=4)
                    Sequence([[1, 2, 3], 4])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=5)
                    Sequence([[1, 2, 3], 4, [5]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=6)
                    Sequence([[1, 2, 3], 4, [5, 6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=99)
                    Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence(name='J').reveal(count=2)

                ::

                    >>> expression([[1, 2, 3], 4, [5, 6]])
                    Sequence([[1, 2]])

                ::

                    >>> expression.get_string()
                    'reveal(J, count=2)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                ", count=2)"
                            }
                        }

        ..  container:: example

            With negative count:

            ..  container:: example

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-1)
                    Sequence([[6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-2)
                    Sequence([[5, 6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-3)
                    Sequence([4, [5, 6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-4)
                    Sequence([[3], 4, [5, 6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-5)
                    Sequence([[2, 3], 4, [5, 6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-6)
                    Sequence([[1, 2, 3], 4, [5, 6]])

                ::

                    >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-99)
                    Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence(name='J').reveal(count=-2)

                ::

                    >>> expression([[1, 2, 3], 4, [5, 6]])
                    Sequence([[5, 6]])

                ::

                    >>> expression.get_string()
                    'reveal(J, count=-2)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  docs::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                ", count=-2)"
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if count is None:
            return type(self)(items=self)
        if count == 0:
            return type(self)()
        if count < 0:
            result = self.reverse(recurse=True)
            result = result.reveal(count=abs(count))
            result = result.reverse(recurse=True)
            return result
        current = 0
        items_ = []
        for item in self:
            if isinstance(item, collections.Iterable):
                subitems_ = []
                for subitem in item:
                    subitems_.append(subitem)
                    current += 1
                    if current == count:
                        item_ = type(item)(subitems_)
                        items_.append(item_)
                        return type(self)(items=items_)
                item_ = type(item)(subitems_)
                items_.append(item_)
            else:
                items_.append(item)
                current += 1
                if current == count:
                    return type(self)(items=items_)
        return type(self)(items=items_)


def _sequence(items=None, **keywords):
    if items is not None:
        return Sequence(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = baca.Expression(name=name)
    callback = expression._make_initializer_callback(
        Sequence,
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=Sequence)
