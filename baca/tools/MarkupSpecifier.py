# -*- coding: utf-8 -*-
import abjad
import baca


class MarkupSpecifier(abjad.abctools.AbjadObject):
    r'''Markup specifier.
    
    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Markup specifier selects first pitched leaf by default:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.tools.MusicRhythmSpecifier(
            ...         rhythm_maker=baca.tools.MusicRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.tools.MarkupSpecifier(
            ...         markup=abjad.Markup('*'),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'8 ~ [ - \markup { * }
                            c'32
                            d'8
                            bf'8 ]
                        }
                        {
                            fs''8 ~ [
                            fs''32
                            e''8
                            ef''8
                            af''8 ~
                            af''32
                            g''8 ]
                        }
                        {
                            a'8 ~ [
                            a'32 ]
                        }
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_markup',
        '_selector',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        markup=None,
        selector=None,
        ):
        if isinstance(markup, str):
            markup = abjad.Markup(markup)
        if markup is not None:
            assert isinstance(markup, abjad.Markup), repr(markup)
        self._markup = markup
        if selector is not None:
            assert isinstance(selector, abjad.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        if not argument or self.markup is None:
            return
        selector = self.selector or baca.select_plt_head(0)
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            for component in  selection:
                markup = abjad.new(self.markup)
                abjad.attach(markup, component)

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets markup.

        Defaults to none.

        Set to markup or none.

        Returns markup or none.
        '''
        return self._markup

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects first pitched head:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.MarkupSpecifier(
                ...         markup=abjad.Markup('*'),
                ...         ),
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[5, 4, 4, 5, 4, 4, 4],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'8 ~ [ - \markup { * }
                                c'32
                                d'8
                                bf'8 ]
                            }
                            {
                                fs''8 ~ [
                                fs''32
                                e''8
                                ef''8
                                af''8 ~
                                af''32
                                g''8 ]
                            }
                            {
                                a'8 ~ [
                                a'32 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects pitched heads:

            ::

                >>> music_maker = baca.MusicMaker(
                ...     baca.tools.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.tools.MusicRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[5, 4, 4, 5, 4, 4, 4],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.tools.MarkupSpecifier(
                ...         markup=abjad.Markup('*'),
                ...         selector=baca.select_plt_heads(),
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'8 ~ [ - \markup { * }
                                c'32
                                d'8 - \markup { * }
                                bf'8 ] - \markup { * }
                            }
                            {
                                fs''8 ~ [ - \markup { * }
                                fs''32
                                e''8 - \markup { * }
                                ef''8 - \markup { * }
                                af''8 ~ - \markup { * }
                                af''32
                                g''8 ] - \markup { * }
                            }
                            {
                                a'8 ~ [ - \markup { * }
                                a'32 ]
                            }
                        }
                    }
                >>

        Defaults to head of first pitched logical tie.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
