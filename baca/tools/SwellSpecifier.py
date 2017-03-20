# -*- coding: utf-8 -*-
import abjad
import baca
import copy


class SwellSpecifier(abjad.abctools.AbjadObject):
    r'''Swell specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Attaches niente swell to all pitched logical ties:

        ::

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.niente_swell('p'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5
                            r8
                            \once \override Hairpin.circled-tip = ##t
                            c'16 \< [
                            d'16 \p ]
                            bf'4 ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16 [
                            e''16 ]
                            ef''4 ~
                            ef''16
                            r16
                            af''16 [
                            \once \override Hairpin.circled-tip = ##t
                            g''16 ] \> \p
                        }
                        \times 4/5 {
                            a'16 \!
                            r4
                            \revert TupletBracket.staff-padding
                        }
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_selector',
        '_start_count',
        '_start_token',
        '_stop_count',
        '_stop_token',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector=None,
        start_count=None,
        start_token=None,
        stop_count=None,
        stop_token=None,
        ):
        if selector is not None:
            assert isinstance(selector, abjad.Selector)
        self._selector = selector
        assert 0 < start_count, repr(start_count)
        assert isinstance(start_token, str), repr(start_token)
        assert 0 < stop_count, repr(stop_count)
        assert isinstance(stop_token, str), repr(stop_token)
        self._start_count = start_count
        self._start_token = start_token
        self._stop_count = stop_count
        self._stop_token = stop_token

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        selector = self.selector or baca.select_pls()
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            leaves = abjad.select(selection).by_leaf()
            start_hairpin = abjad.Hairpin(
                self.start_token,
                include_rests=True,
                )
            if len(leaves) < self.minimum_leaf_count:
                #message = 'specifier requires at least {} leaves: {!r}.'
                #message = message.format(self.minimum_leaf_count, leaves)
                #raise Exception(message)
                if len(leaves) == 0:
                    return
                prototype = (abjad.Note, abjad.Chord)
                for leaf in leaves:
                    if isinstance(leaf, prototype):
                        lone_dynamic = start_hairpin.stop_dynamic
                        lone_dynamic = copy.copy(lone_dynamic)
                        abjad.attach(lone_dynamic, leaf)
                        break
                return
            start_leaves = leaves[:self.start_count]
            abjad.attach(start_hairpin, start_leaves)
            stop_hairpin = abjad.Hairpin(
                self.stop_token,
                include_rests=True,
                )
            stop_leaves = leaves[-self.stop_count:]
            abjad.attach(stop_hairpin, stop_leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_leaf_count(self):
        r'''Gets minimum leaf count.

        Defined equal to start count + stop count - 1.

        Returns positive integer.
        '''
        return self.start_count + self.stop_count - 1

    @property
    def selector(self):
        r'''Gets selector

        Returns selector or none.
        '''
        return self._selector

    @property
    def start_count(self):
        r'''Gets start count.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._start_count

    @property
    def start_token(self):
        r'''Gets start token.

        Set to string or none.

        Returns string or none.
        '''
        return self._start_token

    @property
    def stop_count(self):
        r'''Gets stop count.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._stop_count

    @property
    def stop_token(self):
        r'''Gets stop token.

        Set to string or none.

        Returns string or none.
        '''
        return self._stop_token
