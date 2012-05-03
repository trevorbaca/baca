# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.lilypondfiletools.HeaderBlock import HeaderBlock


class AdobeCaslonProHeader(HeaderBlock):

    ### INITIALIZER ###

    def __init__(self, composer=None, title=None):
        HeaderBlock.__init__(self)
        if composer is not None:
            self.composer = markuptools.Markup(r'''
                \override #'(font-name . "Times")
                \hspace #0 \raise #-40
                \fontsize #3 "%s"
                \hspace #15''' % composer)
        self.tagline = markuptools.Markup('""')
        if title is not None:
            self.title = markuptools.Markup(r'''\column {
                    \center-align {
                        \override #'(font-name . "Adobe Caslon Pro Bold")
                        \fontsize #18 {
                            " "   " "   " "   " "   " "
                            \line { %s } 
                            " "   " "   " "
                        }
                    }
                }''' % title)
