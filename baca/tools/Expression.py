import abjad


class Expression(abjad.Expression):
    r'''Expression.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

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
            raise Exception(f'{statement!r} raises {e!r}.')
        return result

    ### PUBLIC METHODS ###

    def pitch_class_segment(self, **keywords):
        r'''Makes pitch-class segment subclass expression.

        ..  container:: example

            Makes expression to apply alpha transform to pitch-class segment:

            >>> baca.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> segment = baca.PitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=79) # doctest: +SKIP

            ..  container:: example expression

                >>> expression = baca.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.alpha()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )


        Returns expression.
        '''
        import baca
        class_ = baca.PitchClassSegment
        callback = self._make_initializer_callback(
            class_,
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

    def select(self, **keywords):
        r'''Makes select expression.

        ..  container:: example

            Makes expression to select leaves:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                >>> abjad.show(staff, strict=79) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff, strict=79)
                    \new Staff {
                        { % measure
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        } % measure
                        { % measure
                            af'8
                            r8
                        } % measure
                        { % measure
                            r8
                            gf'8
                        } % measure
                    }

            ..  container:: example expression

                >>> expression = baca.Expression()
                >>> expression = expression.select()
                >>> expression = expression.leaves()

                >>> for leaf in expression(staff):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Rest('r8')
                Rest('r8')
                Note("gf'8")

        Returns expression.
        '''
        import baca
        class_ = baca.Selection
        callback = self._make_initializer_callback(
            class_,
            module_names=['baca'],
            **keywords
            )
        expression = self.append_callback(callback)
        return abjad.new(
            expression,
            proxy_class=class_,
            template='baca',
            )
