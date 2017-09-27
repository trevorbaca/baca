import abjad
import baca
import inspect


class DivisionSequenceExpression(abjad.Expression):
    r'''Division expression.

    ..  note:: Reimplement as signatured-decorated DivisionSequence method.

    ::

        >>> import baca

    ..  container:: example

        Inherits from sequence expression and coerces input:

        ::

            >>> expression = baca.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression[-3:]

        ::

            >>> expression([1, 2, 3, 4, 5])
            DivisionSequence([Division((3, 1)), Division((4, 1)), Division((5, 1))])

    ..  container:: example

        Splits into quarter notes:

        ::

            >>> expression = baca.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> for item in expression(divisions):
            ...     item
            ...
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])

    ..  container:: example

        Splits into quarter notes and flattens result:

        ::

            >>> expression = baca.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )
            >>> expression = expression.flatten()

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> for item in expression(divisions):
            ...     item
            ...
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))

    ..  container:: example

        Splits into quarter notes with compound meter multiplier:

        ::

            >>> expression = baca.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     compound_meter_multiplier=(3, 2),
            ...     durations=[(1, 4)],
            ...     )

        ::

            >>> divisions = [(4, 4), (6, 4)]
            >>> for item in expression(divisions):
            ...     item
            ...
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))])
            DivisionSequence([Division((3, 8)), Division((3, 8)), Division((3, 8)), Division((3, 8))])

    ..  container:: example

        Splits into quarter notes with compound meter multiplier and gets
        first division of part:

        ::

            >>> expression = baca.DivisionSequenceExpression()
            >>> expression = expression.division_sequence()
            >>> expression = expression.split_by_durations(
            ...     compound_meter_multiplier=(3, 2),
            ...     durations=[(1, 4)],
            ...     )
            >>> expression_2 = baca.DivisionSequenceExpression()
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

    __documentation_section__ = 'Divisions'

    __slots__ = (
        )

    _publish_storage_format = True

    ### SPECIAL METHODS ###

    def __add__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__add__')
        return proxy_method(i)

    def __getitem__(self, argument):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__getitem__')
        return proxy_method(argument)

    def __radd__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__radd__')
        return proxy_method(i)

    ### PUBLIC METHODS ###

    def division_sequence(self):
        r'''Makes divison sequence expression.

        Returns expression.
        '''
        class_ = baca.DivisionSequence
        callback = self._make_initializer_callback(
            class_,
            module_names=['baca'],
            string_template='{}',
            )
        expression = self.append_callback(callback)
        return abjad.new(expression, proxy_class=class_)

    def split_by_durations(
        self,
        compound_meter_multiplier=None,
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=abjad.Right,
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
        evaluation_template = template.format(
            compound_meter_multiplier=compound_meter_multiplier,
            cyclic=cyclic,
            durations=durations,
            pattern_rotation_index=pattern_rotation_index,
            remainder=remainder,
            remainder_fuse_threshold=remainder_fuse_threshold,
            )
        callback = abjad.Expression._frame_to_callback(
            inspect.currentframe(),
            evaluation_template=evaluation_template,
            module_names=['baca'],
            )
        return self.append_callback(callback)
