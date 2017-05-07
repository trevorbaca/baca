# -*- coding: utf-8 -*-
import abjad
import baca
import inspect


class PitchSet(abjad.PitchSet):
    r'''Pitch set.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes set:

        ..  container:: example

            ::

                >>> set_ = baca.pitch_set([-2, -1.5, 6, 7, -1.5, 7])
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new PianoStaff <<
                        \new Staff {
                            \new Voice {
                                <fs' g'>1
                            }
                        }
                        \new Staff {
                            \new Voice {
                                <bf bqf>1
                            }
                        }
                    >>
                >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when segment equals `argument`. Otherwise false.

        ..  container:: example

            Works with Abjad pitch sets:

            ::

                >>> set_1 = abjad.PitchSet([0, 1, 2, 3])
                >>> set_2 = baca.PitchSet([0, 1, 2, 3])

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

    def space_down(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r'''Spaces pitch set down.

        ..  container:: example

            ::

                >>> set_ = baca.pitch_set([12, 14, 21, 22])
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

            ::

                >>> set_.space_down(bass=0)
                PitchSet([0, 9, 10, 14])

            ::

                >>> set_ = set_.space_down(bass=0)
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <c' a' bf' d''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

        ..  container:: example

            With 2 in bass:

            ::

                >>> set_ = baca.pitch_set([12, 14, 21, 22])
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

            ::

                >>> set_.space_down(bass=2)
                PitchSet([2, 9, 10, 12])

            ::

                >>> set_ = set_.space_down(bass=2)
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <d' a' bf' c''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

        Returns new pitch set.
        '''
        specifier = baca.ChordalSpacingSpecifier(
            bass=bass,
            direction=Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, baca.CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def space_up(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r'''Spaces pitch set up.

        ..  container:: example

            ::

                >>> set_ = baca.pitch_set([12, 14, 21, 22])
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

            ::

                >>> set_.space_up(bass=0)
                PitchSet([0, 2, 9, 10])

            ::

                >>> set_ = set_.space_up(bass=0)
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <c' d' a' bf'>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

        ..  container:: example

            With 2 in bass:

            ::

                >>> set_ = baca.pitch_set([12, 14, 21, 22])
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

            ::

                >>> set_.space_up(bass=2)
                PitchSet([2, 9, 10, 12])

            ::

                >>> set_ = set_.space_up(bass=2)
                >>> show(set_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = set_.__illustrate__()
                >>> f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff <<
                    \new Staff {
                        \new Voice {
                            <d' a' bf' c''>1
                        }
                    }
                    \new Staff {
                        \new Voice {
                            s1
                        }
                    }
                >>

        Returns new pitch segment.
        '''
        specifier = baca.ChordalSpacingSpecifier(
            bass=bass,
            direction=Up,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, baca.CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def to_pitch_classes(self):
        r'''Makes pitch-class set.

        ..  container:: example

            ::

                >>> set_ = baca.pitch_set([-2, -1.5, 6, 19, -1.5, 21])
                >>> set_
                PitchSet([-2, -1.5, 6, 19, 21])

            ::

                >>> set_.to_pitch_classes()
                PitchClassSet([6, 7, 9, 10, 10.5])

        Returns new pitch-class set.
        '''
        if self.item_class is abjad.NumberedPitch:
            item_class = abjad.NumberedPitchClass
        elif self.item_class is abjad.NamedPitch:
            item_class = abjad.NamedPitchClass
        else:
            raise TypeError(self.item_class)
        return baca.PitchClassSet(
            items=self,
            item_class=item_class,
            )


def _pitch_set(items=None, **keywords):
    if items:
        return PitchSet(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = baca.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchSet,
        markup_expression=abjad.Expression().markup(),
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchSet)
