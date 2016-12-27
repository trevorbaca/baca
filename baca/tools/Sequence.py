# -*- coding: utf-8 -*-
import abjad
import inspect


class Sequence(abjad.Sequence):
    r'''Sequence.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes from numbers:

        ..  container:: example

            ::

                >>> baca.Sequence([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            ::

                >>> expression = baca.sequence()
                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes from segment:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = abjad.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
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

                >>> baca.sequence(items=segment)
                Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

        ..  container:: example expression

            ::

                >>> expression = baca.sequence()
                >>> expression(items=segment)
                Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

    ..  container:: example

        Maps transposition to multiple segments:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = abjad.PitchClassSegment(items=items)
                >>> segments = [
                ...     abjad.PitchClassSegment(items=[-2, -1.5, 6]),
                ...     abjad.PitchClassSegment(items=[7, -1.5, 7]),
                ...     ]
                >>> sequence = baca.Sequence(items=segments)
                >>> expression = Expression()
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.transpose(n=1)
                >>> sequence = sequence.map(expression)
                >>> 'TODO: make sequence.sum() work'
                'TODO: make sequence.sum() work'
                >>> segment = sequence[0] + sequence[1]
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
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

                >>> expression = Expression()
                >>> transposition = expression.pitch_class_segment()
                >>> transposition = transposition.transpose(n=1)
                >>> expression = baca.sequence()
                >>> expression = expression.map(transposition)
                >>> segments = [
                ...     abjad.PitchClassSegment(items=[-2, -1.5, 6]),
                ...     abjad.PitchClassSegment(items=[7, -1.5, 7]),
                ...     ]
                >>> segments = expression(segments)
                >>> segment = segments[0] + segments[1]
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _partition_by_rgf(self, rgf):
        '''Partitions `sequence` by restricted growth function `rgf`.

        ::

            >>> sequence = baca.Sequence(range(10))
            >>> rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]

        ::

            >>> sequence._partition_by_rgf(rgf)
            Sequence([Sequence([0, 1, 4]), Sequence([2, 3, 5, 8]), Sequence([6, 7]), Sequence([9])])

        Returns list of lists.
        '''
        rgf = type(self)(rgf)
        if not rgf.is_restricted_growth_function():
            message = 'must be restricted growth function: {!r}.'
            message = message.format(rgf)
            raise ValueError(message)
        if not len(self) == len(rgf):
            message = 'lengths must be equal.'
            raise ValueError(message)
        partition = []
        for part_index in range(max(rgf)):
            part = []
            partition.append(part)
        for n, part_number in zip(self, rgf):
            part_index = part_number - 1
            part = partition[part_index]
            part.append(n)
        partition = [type(self)(_) for _ in partition]
        partition = type(self)(partition)
        return partition

    ### PUBLIC METHODS ###

    def accumulate(self, operand, n=1):
        r'''Accumulates `operand` calls against sequence `n` times.

        ..  container:: example

            Accumulates transposition:

            ..  container:: example

                ::

                    >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                    >>> J = abjad.PitchClassSegment(items=items)
                    >>> show(J) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = J.__illustrate__()
                    >>> f(lilypond_file[Voice])
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
                    
                    >>> initializer = Expression()
                    >>> initializer = initializer.pitch_class_segment()
                    >>> sequence = baca.sequence(items=J)
                    >>> operand = abjad.Transposition(n=3)
                    >>> sequence = sequence.accumulate(operand, n=3)
                    >>> sequence = sequence.map(initializer)
                    >>> for segment in sequence:
                    ...     segment
                    ...
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
                    PitchClassSegment([1, 1.5, 9, 10, 1.5, 10])
                    PitchClassSegment([4, 4.5, 0, 1, 4.5, 1])
                    PitchClassSegment([7, 7.5, 3, 4, 7.5, 4])

            ..  container:: example expression

                ::
                    
                    >>> initializer = Expression()
                    >>> initializer = initializer.pitch_class_segment()
                    >>> operand = abjad.Transposition(n=3)
                    >>> expression = baca.sequence()
                    >>> expression = expression.accumulate(operand, n=3)
                    >>> expression = expression.map(initializer)
                    >>> sequence = expression(J)
                    >>> for segment in sequence:
                    ...     segment
                    ...
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
                    PitchClassSegment([1, 1.5, 9, 10, 1.5, 10])
                    PitchClassSegment([4, 4.5, 0, 1, 4.5, 1])
                    PitchClassSegment([7, 7.5, 3, 4, 7.5, 4])

        ..  container:: example

            Accumulates transposition to identity:

            ..  container:: example

                ::

                    >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                    >>> J = abjad.PitchClassSegment(items=items)
                    >>> show(J) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = J.__illustrate__()
                    >>> f(lilypond_file[Voice])
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
                    
                    >>> initializer = Expression()
                    >>> initializer = initializer.pitch_class_segment()
                    >>> sequence = baca.sequence(items=J)
                    >>> operand = abjad.Transposition(n=5)
                    >>> sequence = sequence.accumulate(operand, n=Identity)
                    >>> sequence = sequence.map(initializer)
                    >>> for segment in sequence:
                    ...     segment
                    ...
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
                    PitchClassSegment([3, 3.5, 11, 0, 3.5, 0])
                    PitchClassSegment([8, 8.5, 4, 5, 8.5, 5])
                    PitchClassSegment([1, 1.5, 9, 10, 1.5, 10])
                    PitchClassSegment([6, 6.5, 2, 3, 6.5, 3])
                    PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])
                    PitchClassSegment([4, 4.5, 0, 1, 4.5, 1])
                    PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])
                    PitchClassSegment([2, 2.5, 10, 11, 2.5, 11])
                    PitchClassSegment([7, 7.5, 3, 4, 7.5, 4])
                    PitchClassSegment([0, 0.5, 8, 9, 0.5, 9])
                    PitchClassSegment([5, 5.5, 1, 2, 5.5, 2])

            ..  container:: example expression

                ::
                    
                    >>> initializer = Expression()
                    >>> initializer = initializer.pitch_class_segment()
                    >>> operand = abjad.Transposition(n=5)
                    >>> expression = baca.sequence()
                    >>> expression = expression.accumulate(operand, n=Identity)
                    >>> expression = expression.map(initializer)
                    >>> sequence = expression(J)
                    >>> for segment in sequence:
                    ...     segment
                    ...
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
                    PitchClassSegment([3, 3.5, 11, 0, 3.5, 0])
                    PitchClassSegment([8, 8.5, 4, 5, 8.5, 5])
                    PitchClassSegment([1, 1.5, 9, 10, 1.5, 10])
                    PitchClassSegment([6, 6.5, 2, 3, 6.5, 3])
                    PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])
                    PitchClassSegment([4, 4.5, 0, 1, 4.5, 1])
                    PitchClassSegment([9, 9.5, 5, 6, 9.5, 6])
                    PitchClassSegment([2, 2.5, 10, 11, 2.5, 11])
                    PitchClassSegment([7, 7.5, 3, 4, 7.5, 4])
                    PitchClassSegment([0, 0.5, 8, 9, 0.5, 9])
                    PitchClassSegment([5, 5.5, 1, 2, 5.5, 2])

        Returns new sequence of length `n` + 1 when `n` is an integer.

        Returns new sequence with length equal to identity when `n` is set to
        identity.
        '''
        if self._frozen_expression:
            return self._make_callback(inspect.currentframe())
        result = [self]
        if n is Identity:
            for i in range(1000):
                result_ = result[-1]
                result_ = operand(result_)
                if result_ == result[0]:
                    break
                result.append(result_)
            else:
                message = 'can not achieve identity in 1000 iterations.'
                raise Exception(message)
        else:
            for i in range(n):
                result_ = result[-1]
                result_ = operand(result_)
                result.append(result_)
        result = type(self)(items=result)
        return result

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

            Helianthates list of segments:

            ..  container:: example

                ::

                    >>> J = abjad.PitchClassSegment(items=[0, 2, 4], name='J')
                    >>> K = abjad.PitchClassSegment(items=[5, 6], name='K')
                    >>> L = abjad.PitchClassSegment(items=[7, 9, 11], name='L')
                    >>> sequence = baca.sequence([J, K, L])
                    >>> sequence = sequence.helianthate(n=-1, m=1)
                    >>> for segment in sequence:
                    ...     segment
                    ...
                    PitchClassSegment([0, 2, 4], name='J')
                    PitchClassSegment([5, 6], name='K')
                    PitchClassSegment([7, 9, 11], name='L')
                    PitchClassSegment([6, 5], name='r1(K)')
                    PitchClassSegment([11, 7, 9], name='r1(L)')
                    PitchClassSegment([4, 0, 2], name='r1(J)')
                    PitchClassSegment([9, 11, 7], name='r2(L)')
                    PitchClassSegment([2, 4, 0], name='r2(J)')
                    PitchClassSegment([5, 6], name='r2(K)')
                    PitchClassSegment([0, 2, 4], name='r3(J)')
                    PitchClassSegment([6, 5], name='r3(K)')
                    PitchClassSegment([7, 9, 11], name='r3(L)')
                    PitchClassSegment([5, 6], name='r4(K)')
                    PitchClassSegment([11, 7, 9], name='r4(L)')
                    PitchClassSegment([4, 0, 2], name='r4(J)')
                    PitchClassSegment([9, 11, 7], name='r5(L)')
                    PitchClassSegment([2, 4, 0], name='r5(J)')
                    PitchClassSegment([6, 5], name='r5(K)')

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence()
                    >>> expression = expression.helianthate(n=-1, m=1)
                    >>> J = abjad.PitchClassSegment(items=[0, 2, 4], name='J')
                    >>> K = abjad.PitchClassSegment(items=[5, 6], name='K')
                    >>> L = abjad.PitchClassSegment(items=[7, 9, 11], name='L')
                    >>> sequence = expression([J, K, L])
                    >>> for segment in sequence:
                    ...     segment
                    ...
                    PitchClassSegment([0, 2, 4], name='J')
                    PitchClassSegment([5, 6], name='K')
                    PitchClassSegment([7, 9, 11], name='L')
                    PitchClassSegment([6, 5], name='r1(K)')
                    PitchClassSegment([11, 7, 9], name='r1(L)')
                    PitchClassSegment([4, 0, 2], name='r1(J)')
                    PitchClassSegment([9, 11, 7], name='r2(L)')
                    PitchClassSegment([2, 4, 0], name='r2(J)')
                    PitchClassSegment([5, 6], name='r2(K)')
                    PitchClassSegment([0, 2, 4], name='r3(J)')
                    PitchClassSegment([6, 5], name='r3(K)')
                    PitchClassSegment([7, 9, 11], name='r3(L)')
                    PitchClassSegment([5, 6], name='r4(K)')
                    PitchClassSegment([11, 7, 9], name='r4(L)')
                    PitchClassSegment([4, 0, 2], name='r4(J)')
                    PitchClassSegment([9, 11, 7], name='r5(L)')
                    PitchClassSegment([2, 4, 0], name='r5(J)')
                    PitchClassSegment([6, 5], name='r5(K)')

        ..  container:: example

            Trivial helianthation:

            ..  container:: example

                ::

                    >>> sequence = baca.sequence([[1, 2, 3], [4, 5], [6, 7, 8]])
                    >>> sequence.helianthate()
                    Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

            ..  container:: example expression

                ::

                    >>> expression = baca.sequence()
                    >>> expression = expression.helianthate()
                    >>> expression([[1, 2, 3], [4, 5], [6, 7, 8]])
                    Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

        '''
        template = 'H({{}}, {n}, {m}'.format(n=n, m=m)
        if self._frozen_expression:
            return self._make_callback(
                inspect.currentframe(),
                formula_string_template=template,
                )
        start = list(self[:])
        result = list(self[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m
        def _generalized_rotate(argument, n=0):
            if hasattr(argument, 'rotate'):
                return argument.rotate(n=n)
            return abjad.sequencetools.rotate_sequence(argument, n=n)
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
        result = type(self)(result)
        return result

    def is_restricted_growth_function(self):
        '''Is true when sequence is a restricted growth function.

        ..  container:: example

            Is true when sequence is a restricted growth function:

            ::

                >>> baca.Sequence([1, 1, 1, 1]).is_restricted_growth_function()
                True

            ::

                >>> baca.Sequence([1, 1, 1, 2]).is_restricted_growth_function()
                True

            ::

                >>> baca.Sequence([1, 1, 2, 1]).is_restricted_growth_function()
                True

            ::

                >>> baca.Sequence([1, 1, 2, 2]).is_restricted_growth_function()
                True

        ..  container:: example

            Is false when sequence is not a restricted growth function:

            ::

                >>> baca.Sequence([1, 1, 1, 3]).is_restricted_growth_function()
                False

            ::

                >>> baca.Sequence([17,]).is_restricted_growth_function()
                False

        A restricted growth function is a sequence ``l`` such that
        ``l[0] == 1`` and such that ``l[i] <= max(l[:i]) + 1`` for
        ``1 <= i <= len(l)``.

        Returns true or false.
        '''
        try:
            for i, n in enumerate(self):
                if i == 0:
                    if not n == 1:
                        return False
                else:
                    if not n <= max(self[:i]) + 1:
                        return False
            return True
        except TypeError:
            return False

    @staticmethod
    def yield_restricted_growth_functions(length):
        '''Yields restricted growth functions of `length`.

        ::

            >>> rgfs = baca.Sequence.yield_restricted_growth_functions(4)
            >>> for rgf in rgfs:
            ...     rgf
            ...
            (1, 1, 1, 1)
            (1, 1, 1, 2)
            (1, 1, 2, 1)
            (1, 1, 2, 2)
            (1, 1, 2, 3)
            (1, 2, 1, 1)
            (1, 2, 1, 2)
            (1, 2, 1, 3)
            (1, 2, 2, 1)
            (1, 2, 2, 2)
            (1, 2, 2, 3)
            (1, 2, 3, 1)
            (1, 2, 3, 2)
            (1, 2, 3, 3)
            (1, 2, 3, 4)

        Returns restricted growth functions in lex order.

        Returns generator of tuples.
        '''
        if not abjad.mathtools.is_positive_integer(length):
            raise TypeError
        last_rgf = list(range(1, length + 1))
        rgf = length * [1]
        yield tuple(rgf)
        while not rgf == last_rgf:
            for i, x in enumerate(reversed(rgf)):
                if x < max(rgf[:-(i+1)]) + 1:
                    first_part = rgf[:-(i+1)]
                    increased_part = [rgf[-(i+1)] + 1]
                    trailing_ones = i * [1]
                    rgf = first_part + increased_part + trailing_ones
                    yield tuple(rgf)
                    break

    def yield_set_partitions(self):
        '''Yields all set partitions of sequence.

        ..  container:: example

            ::

                >>> sequence = baca.Sequence([21, 22, 23, 24])
                >>> for set_partition in sequence.yield_set_partitions(): 
                ...     set_partition
                ...
                Sequence([Sequence([21, 22, 23, 24])])
                Sequence([Sequence([21, 22, 23]), Sequence([24])])
                Sequence([Sequence([21, 22, 24]), Sequence([23])])
                Sequence([Sequence([21, 22]), Sequence([23, 24])])
                Sequence([Sequence([21, 22]), Sequence([23]), Sequence([24])])
                Sequence([Sequence([21, 23, 24]), Sequence([22])])
                Sequence([Sequence([21, 23]), Sequence([22, 24])])
                Sequence([Sequence([21, 23]), Sequence([22]), Sequence([24])])
                Sequence([Sequence([21, 24]), Sequence([22, 23])])
                Sequence([Sequence([21]), Sequence([22, 23, 24])])
                Sequence([Sequence([21]), Sequence([22, 23]), Sequence([24])])
                Sequence([Sequence([21, 24]), Sequence([22]), Sequence([23])])
                Sequence([Sequence([21]), Sequence([22, 24]), Sequence([23])])
                Sequence([Sequence([21]), Sequence([22]), Sequence([23, 24])])
                Sequence([Sequence([21]), Sequence([22]), Sequence([23]), Sequence([24])])

        Returns set partitions in order of restricted growth function.

        Returns generator of list of lists.
        '''
        for rgf in Sequence.yield_restricted_growth_functions(len(self)):
            partition = self._partition_by_rgf(rgf)
            yield partition


def _sequence(items=None, **keywords):
    if items is not None:
        return Sequence(items=items, **keywords)
    expression = abjad.Expression()
    expression = expression._initialize(
        Sequence,
        formula_string_template='{}',
        module_names=['baca'],
        **keywords
        )
    return expression
