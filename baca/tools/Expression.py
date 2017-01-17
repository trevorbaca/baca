# -*- coding: utf-8 -*-
import abjad


class Expression(abjad.Expression):
    r'''Expression.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### PRIVATE METHODS ###

    def _evaluate_accumulate(self, *arguments):
        import baca
        assert len(arguments) == 1, repr(arguments)
        globals_ = self._make_globals()
        assert '__argument_0' not in globals_
        __argument_0 = arguments[0]
        assert isinstance(__argument_0, baca.Sequence), repr(__argument_0)
        class_ = type(__argument_0)
        operands = self.map_operand
        globals_['__argument_0'] = __argument_0
        globals_['class_'] = class_
        globals_['operands'] = operands
        statement = '__argument_0.accumulate(operands=operands)'
        try:
            result = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            message = '{!r} raises {!r}.'
            message = message.format(statement, e)
            raise Exception(message)
        return result

    ### PUBLIC METHODS ###

    def pitch_class_segment(self, **keywords):
        r'''Makes pitch-class segment subclass expression.

        ..  container:: example

            Makes expression to apply alpha transform to pitch-class segment:

            ::

                >>> PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            ::

                >>> segment = PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
                >>> show(segment) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = baca.Expression(name='J')
                    >>> expression = expression.pitch_class_segment()
                    >>> expression = expression.alpha()

                ::

                    >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                    PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                ::

                    >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                    >>> markup = expression.get_markup()
                    >>> show(segment, figure_name=markup) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )


        Returns expression.
        '''
        import baca
        class_ = baca.PitchClassSegment
        callback = self._make_initializer_callback(
            class_,
            markup_expression=type(self)().markup(),
            module_names=['baca'],
            string_template='{}',
            **keywords
            )
        expression = self.append_callback(callback)
        return abjad.new(expression, proxy_class=class_)

    def pitch_class_segments(self):
        r'''Maps pitch-class segment subclass initializer to expression.
        '''
        initializer = Expression().pitch_class_segment()
        return self.map(initializer)
