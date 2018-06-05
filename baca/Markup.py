import abjad


class Markup(abjad.Markup):
    """
    Markup subclass.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### PUBLIC METHODS ###

    def boxed(self):
        r"""
        Makes boxed markup.
        
        ..  container:: example

            >>> markup = baca.Markup('Allegro assai')
            >>> markup = markup.boxed()
            >>> abjad.f(markup)
            \markup {
                \override
                    #'(box-padding . 0.5)
                    \box
                        "Allegro assai"
                }

            >>> abjad.show(markup) # doctest: +SKIP

        Sets box-padding to 0.5.
        """
        return self.box().override(('box-padding', 0.5))
