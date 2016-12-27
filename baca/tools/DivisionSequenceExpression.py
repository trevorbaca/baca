# -*- coding: utf-8 -*-
import abjad
import baca


class DivisionSequenceExpression(abjad.expressiontools.Expression):
    r'''Division expression.

    ..  note:: Reimplement as frozen expression on DivisionSequence.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Inherits from sequence expression:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression[-3:]

        ::

            >>> expression([1, 2, 3, 4, 5])
            DivisionSequence([3, 4, 5])

    ..  container:: example

        Splits into quarter notes:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     durations=[Duration(1, 4)],
            ...     )

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> expression(divisions)
            DivisionSequence([DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]), DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])])

    ..  container:: example

        Splits into quarter notes and flattens result:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     durations=[Duration(1, 4)],
            ...     )
            >>> expression = expression.flatten()

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> expression(divisions)
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])

    ..  container:: example

        Splits into quarter notes with compound meter multiplier:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     compound_meter_multiplier=Multiplier((3, 2)),
            ...     durations=[Duration(1, 4)],
            ...     )

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> division_sequence = expression(divisions)
            >>> for part in division_sequence:
            ...     part
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])
            DivisionSequence([Division((3, 8)), Division((3, 8)), Division((3, 8)), Division((3, 8))])

    ..  container:: example

        Splits into quarter notes with compound meter multiplier and gets
        first division of part:

        ::

            >>> expression = baca.tools.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     compound_meter_multiplier=Multiplier((3, 2)),
            ...     durations=[Duration(1, 4)],
            ...     )
            >>> expression_2 = baca.tools.DivisionSequenceExpression()
            >>> expression_2 = expression_2.division_sequence()[0]
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
    
    _publish_storage_format = True

    ### SPECIAL METHODS ###

    def __add__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__add__')
        return proxy_method(i)

    def __getitem__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__getitem__')
        return proxy_method(i)

    def __radd__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__radd__')
        return proxy_method(i)

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

        Returns expression.
        '''
        template = '{{}}.split_by_durations('
        template += 'compound_meter_multiplier={compound_meter_multiplier}'
        template += ', cyclic={cyclic}'
        template += ', durations={durations}'
        template += ', pattern_rotation_index={pattern_rotation_index}'
        template += ', remainder={remainder}'
        template += ', remainder_fuse_threshold={remainder_fuse_threshold}'
        template += ')'
        template = template.format(
            compound_meter_multiplier=compound_meter_multiplier,
            cyclic=cyclic,
            durations=durations,
            pattern_rotation_index=pattern_rotation_index,
            remainder=remainder,
            remainder_fuse_threshold=remainder_fuse_threshold,
            )
        return self.append_callback(
            evaluation_template=template,
            module_names=['baca'],
            )

    def division_sequence(self):
        r'''Makes divison sequence initializer callback.

        Returns expression.
        '''
        formula_string_template = 'division_sequence({})'
        template = 'baca.tools.DivisionSequence'
        callback = type(self)(
            evaluation_template=template,
            formula_string_template=formula_string_template,
            is_initializer=True,
            module_names=['baca'],
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = type(self)(callbacks=callbacks)
        result._proxy_class = baca.tools.DivisionSequence
        return result
