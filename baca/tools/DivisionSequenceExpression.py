# -*- coding: utf-8 -*-
import abjad
import baca


class DivisionSequenceExpression(abjad.expressiontools.SequenceExpression):
    r'''Division expression.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Inherits from sequence expression:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression[-3:]

        ::

            >>> expression([1, 2, 3, 4, 5])
            Sequence([3, 4, 5])

    ..  container:: example

        **Example 2.** Splits into quarter notes:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.split_by_durations(
            ...     durations=[Duration(1, 4)],
            ...     )

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> expression(divisions)
            DivisionSequence([DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]), DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])])

    ..  container:: example

        **Example 3.** Splits into quarter notes and flattens result:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.split_by_durations(
            ...     durations=[Duration(1, 4)],
            ...     )
            >>> expression = expression.flatten()

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> expression(divisions)
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])

    ..  container:: example

        **Example 4.** Splits into quarter notes with compound meter
        multiplier:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.split_by_durations(
            ...     compound_meter_multiplier=Multiplier((3, 2)),
            ...     durations=[Duration(1, 4)],
            ...     )

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> expression(divisions)
            DivisionSequence([DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]), DivisionSequence([Division((3, 8)), Division((3, 8)), Division((3, 8)), Division((3, 8))])])

    ..  container:: example

        **Example 5.** Splits into quarter notes with compound meter multiplier
        and gets division of each:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.split_by_durations(
            ...     compound_meter_multiplier=Multiplier((3, 2)),
            ...     durations=[Duration(1, 4)],
            ...     )
            >>> expression_2 = baca.tools.DivisionSequenceExpression()[0]
            >>> expression = expression.map(expression_2)

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> expression(divisions)
            DivisionSequence([Division((1, 4)), Division((3, 8))])

    Initializer returns division sequence expression.

    Call returns division sequence.
    '''

    ### CLASS VARIALBES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, callbacks=None):
        superclass = super(abjad.expressiontools.SequenceExpression, self)
        superclass.__init__(callbacks=callbacks)
        #self._client_class = baca.tools.DivisionSequence

    ### PUBLIC METHODS ###

    def split_by_durations(
        self, 
        compound_meter_multiplier=None,
        cyclic=True,
        durations=(), 
        pattern_rotation_index=0,
        remainder=Right,
        remainder_fuse_threshold=None,
        ):
        r'''Makes split-by-durations callback.

        Returns callback.
        '''
        arguments = {
            'compound_meter_multiplier': compound_meter_multiplier,
            'cyclic': cyclic,
            'durations': durations,
            'pattern_rotation_index': pattern_rotation_index,
            'remainder': remainder,
            'remainder_fuse_threshold': remainder_fuse_threshold,
            }
        name = 'baca.tools.DivisionSequence.split_by_durations'
        #return self.make_callback(name, arguments, module_names=['baca'])
        result = self.make_callback(
            'baca.tools.DivisionSequence({})',
            module_names=['baca'],
            )
        result = result.make_callback(name, arguments, module_names=['baca'])
        return result
