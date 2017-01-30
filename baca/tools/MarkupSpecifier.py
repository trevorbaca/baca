# -*- coding: utf-8 -*-
import abjad


class MarkupSpecifier(abjad.abctools.AbjadObject):
    r'''Markup specifier.
    
    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Markup specifier selects head of first pitched logical tie by default:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.MarkupSpecifier(
            ...         markup=Markup('*'),
            ...         ),
            ...     baca.tools.RhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=rhythmmakertools.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker(segment_list, 'Voice 1')
            >>> lilypond_file = figure_maker.make(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
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
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        if self.markup is None:
            return
        selector = self._get_selector()
        #print(selector)
        selections = selector(argument)
        #raise Exception(selections)
        for item in selections:
            markup = abjad.new(self.markup)
            abjad.attach(markup, item)

    ### PRIVATE METHODS ###

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.selectortools.Selector()
            selector = selector.by_logical_tie(pitched=True, flatten=True)
            selector = selector.get_slice(stop=1, apply_to_each=False)
            selector = selector.get_item(0, apply_to_each=True)
            return selector
        return self.selector

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

            Markup specifier selects head of first pitched logical tie by
            default:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.MarkupSpecifier(
                ...         markup=Markup('*'),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[5, 4, 4, 5, 4, 4, 4],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(segment_list, 'Voice 1')
                >>> lilypond_file = figure_maker.make(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
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

            Markup specifier selects heads of pitched logical ties:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.MarkupSpecifier(
                ...         markup=Markup('*'),
                ...         selector=select().by_logical_tie(pitched=True).
                ...         get_item(0, apply_to_each=True),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[5, 4, 4, 5, 4, 4, 4],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segment_list = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(segment_list, 'Voice 1')
                >>> lilypond_file = figure_maker.make(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
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
