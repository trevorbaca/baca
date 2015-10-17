# -*- coding: utf-8 -*-
from abjad.tools.markuptools import Markup


class MarkupAgent(object):
    r'''Markup agent.

    ..  container:: example

        ::

            >>> import baca

    '''

    ### CLASS VARIABLES ###

    _long_space = 16

    _short_space = 10

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_instrument_name_markup(string, space, column=True):
        parts = string.split()
        if len(parts) == 1:
            markup = Markup(parts[0]).hcenter_in(space)
        elif column:
            markups = [Markup(_) for _ in parts]
            markup = Markup.center_column(markups, direction=None)
            markup = markup.hcenter_in(space)
        else:
            markups = [Markup(_) for _ in parts]
            markup = Markup.line(*markups)
            markup = markup.hcenter_in(space)
        return markup

    ### PUBLIC METHODS ###

    @classmethod
    def make_instrument_name_markup(class_, string, column=True):
        r'''Makes instrument name markup.

        ..  container:: example

            **Example 1.** Makes instrument name markup in column:

            ::

                >>> agent = baca.tools.MarkupAgent
                >>> markup = agent.make_instrument_name_markup('Eng. horn')

            ::

                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> f(markup)
                \markup {
                    \hcenter-in
                        #16
                        \center-column
                            {
                                Eng.
                                horn
                            }
                    }

        ..  container:: example

            **Example 2.** Makes instrument name markup in line:

            ::

                >>> agent = baca.tools.MarkupAgent
                >>> markup = agent.make_instrument_name_markup(
                ...     'Violin 1',
                ...     column=False,
                ...     )

            ::

                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> f(markup)
                \markup {
                    \hcenter-in
                        #16
                        \line
                            {
                                Violin
                                1
                            }
                    }
        
        Centers markup horizontally in 16 spaces.

        Returns markup.
        '''
        return class_._make_instrument_name_markup(
            string, 
            class_._long_space,
            column=column,
            )

    @classmethod
    def make_short_instrument_name_markup(class_, string, column=True):
        r'''Makes short instrument name markup.

        ..  container:: example

            **Example 1.** Makes short instrument name markup in column:

            ::

                >>> agent = baca.tools.MarkupAgent
                >>> markup = agent.make_short_instrument_name_markup(
                ...     'Eng. hn.',
                ...     )

            ::

                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> f(markup)
                \markup {
                    \hcenter-in
                        #10
                        \center-column
                            {
                                Eng.
                                hn.
                            }
                    }

        ..  container:: example

            **Example 2.** Makes short instrument name markup in line:

            ::

                >>> agent = baca.tools.MarkupAgent
                >>> markup = agent.make_short_instrument_name_markup(
                ...     'Vn. 1',
                ...     column=False,
                ...     )

            ::

                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> f(markup)
                \markup {
                    \hcenter-in
                        #10
                        \line
                            {
                                Vn.
                                1
                            }
                    }
        
        Centers markup horizontally in 10 spaces.

        Returns markup.
        '''
        return class_._make_instrument_name_markup(
            string, 
            class_._short_space,
            column=column,
            )