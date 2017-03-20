# -*- coding: utf-8 -*-
import abjad
import baca
import inspect


class PitchClassSet(abjad.PitchClassSet):
    r'''Pitch-class set.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes set:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> set_ = baca.pitch_class_set(items=items)
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    <fs' g' bf' bqf'>1
                }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when segment equals `argument`. Otherwise false.

        ..  container:: example

            Works with Abjad pitch-class sets:

            ::

                >>> set_1 = abjad.PitchClassSet([0, 1, 2, 3])
                >>> set_2 = baca.PitchClassSet([0, 1, 2, 3])

            ::

                >>> set_1 == set_2
                True

            ::

                >>> set_2 == set_1
                True

        '''
        if (not issubclass(type(argument), type(self)) and
            not issubclass(type(self), type(argument))):
            return False
        return self._collection == argument._collection

    ### PUBLIC METHODS ###

    def to_pitch_classes(self):
        r'''Makes new pitch-class set.

        ..  container:: example

            ::

                >>> set_ = baca.pitch_class_set([-2, -1.5, 6, 7, -1.5, 7])
                >>> set_
                PitchClassSet([6, 7, 10, 10.5])

            ::

                >>> set_.to_pitch_classes()
                PitchClassSet([6, 7, 10, 10.5])

        Returns new pitch-class set.
        '''
        return abjad.new(self)

    def to_pitches(self):
        r'''Makes pitch set.

        ..  container:: example

            ::

                >>> set_ = baca.pitch_class_set([-2, -1.5, 6, 7, -1.5, 7])
                >>> set_
                PitchClassSet([6, 7, 10, 10.5])

            ::

                >>> set_.to_pitches()
                PitchSet([6, 7, 10, 10.5])

        Returns pitch set.
        '''
        if self.item_class is abjad.NamedPitchClass:
            item_class = abjad.NamedPitch
        elif self.item_class is abjad.NumberedPitchClass:
            item_class = abjad.NumberedPitch
        else:
            raise TypeError(self.item_class)
        return baca.PitchSet(
            items=self,
            item_class=item_class,
            )


def _pitch_class_set(items=None, **keywords):
    if items:
        return PitchClassSet(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = baca.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchClassSet,
        markup_expression=abjad.Expression().markup(),
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchClassSet)
