# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.lilypondfiletools.HeaderBlock import HeaderBlock


class AdobeCaslonProHeader(HeaderBlock):

    ### INITIALIZER ###

    def __init__(self, composer=None, title=None):
        HeaderBlock.__init__(self)
        if composer is not None:
            self.composer = markuptools.make_vertically_adjusted_composer_markup(composer,
                font_name='Times', font_size=3, space_above=20, space_right=0)
        self.tagline = markuptools.Markup('""')
        if title is not None:
            self.title = markuptools.make_centered_title_markup(title,
                font_name='Adobe Caslon Pro Bold', font_size=18)
