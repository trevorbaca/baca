# -*- coding: utf-8 -*-
import abjad


class SpannerSpecifier(abjad.abctools.AbjadObject):
    r'''Spanner specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.SpannerSpecifier()
            SpannerSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_selector',
        '_spanner',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector=None,
        spanner=None,
        ):
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector
        if spanner is not None:
            assert isinstance(spanner, abjad.spannertools.Spanner)
        self._spanner = spanner

    ### SPECIAL METHODS ###

    def __call__(self, selection):
        r'''Calls spanner figure specifier on `selection`.

        Returns none.
        '''
        if self.spanner is None:
            return
        selector = self._get_selector()
        #print(selector)
        #print(selection)
        selections = selector(selection)
        #print(selections)
        for index, selection in enumerate(selections):
            self._apply_payload(index, selection)
            
    ### PRIVATE METHODS ###

    def _apply_payload(self, index, selection):
        spanner = abjad.new(self.spanner)
        leaves = list(abjad.iterate(selection).by_leaf())
        if 1 < len(leaves):
            abjad.attach(spanner, leaves)

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.select()
            selector = selector.by_leaf()
            return selector
        return self.selector

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects leaves by default:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         spanner=Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [ (
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16 )
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects leaves:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         spanner=Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [[1]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                cs'16
                            }
                        }
                    }
                >>

            Spanner refuses to span a single leaf.

        Defaults to leaves.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def spanner(self):
        r'''Gets spanner.

        Defaults to none.

        Set to spanner or none.

        Returns spanner or none.
        '''
        return self._spanner
