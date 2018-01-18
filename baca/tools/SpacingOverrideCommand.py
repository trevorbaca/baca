import abjad
import baca
from .Command import Command


class SpacingOverrideCommand(Command):
    r'''Spacing override command.

    ..  container:: example

        >>> baca.SpacingOverrideCommand()
        SpacingOverrideCommand(selector=baca.leaf(0))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_document',
        '_duration',
        )

    _magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

    ### INITIALIZER ###

    def __init__(self, duration=None, selector='baca.leaf(0)'):
        Command.__init__(self, selector=selector)
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._document = None
        self._duration = duration

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Applies command to result of selector called on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaf = baca.select(argument).leaf(0)
        assert isinstance(leaf, abjad.Skip), repr(leaf)
        self._attach_spacing_override(
            leaf,
            self.duration,
            document=self.document,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _attach_spacing_override(leaf, duration, document=None, eol=None):
        assert isinstance(leaf, abjad.Skip), repr(leaf)
        # overriding spacing for just one document:
        if document:
            include_document_tag = baca.tags.only(document)
            for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
                assert isinstance(wrapper.tag, str)
                if include_document_tag in wrapper.tag.split(':'):
                    if eol:
                        # automatic eol defers to explicit user override
                        return
                    message = 'already have {} spacing override.'
                    message = message.format(include_document_tag)
                    raise Exception(message)
            for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
                if not wrapper.tag:
                    continue
                words = wrapper.tag.split(':')
                if baca.tags.SPACING_OVERRIDE_MARKUP not in words:
                    continue
                if include_document_tag in words:
                    if eol:
                        # automatic eol defers to explicit user override
                        return
                    message = 'already have {} spacing override markup.'
                    message = message.format(include_document_tag)
                    raise Exception(message)
        # overriding fallback spacing for all documents:
        else:
            for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
                assert isinstance(wrapper.tag, str)
                if baca.tags.SPACING in wrapper.tag.split(':'):
                    abjad.detach(wrapper, leaf)
            for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
                if not wrapper.tag:
                    continue
                if baca.tags.SPACING_MARKUP in wrapper.tag.split(':'):
                    abjad.detach(wrapper, leaf)
        if eol:
            duration *= SpacingOverrideCommand._magic_lilypond_eol_adjustment
        spacing_section = baca.SpacingSection(duration=duration)
        if document is None:
            tag = baca.tags.SPACING
            deactivate = None
        else:
            tag = baca.tags.SPACING_OVERRIDE
            tag = baca.tags.only(document, tag)
            deactivate = True
        abjad.attach(
            spacing_section,
            leaf,
            deactivate=deactivate,
            site='SOC1',
            tag=tag,
            )
        if eol:
            markup = abjad.Markup(f'[[{duration!s}]]')
        else:
            markup = abjad.Markup(f'[{duration!s}]')
        markup = markup.fontsize(3)
        if document is None:
            color = 'BlueViolet'
        elif eol:
            color = 'DarkOrange'
        else:
            color = 'DeepPink1'
        markup = markup.with_color(abjad.SchemeColor(color))
        markup = abjad.new(markup, direction=abjad.Up)
        tag, deactivate = baca.tags.SPACING_OVERRIDE_MARKUP, None
        if document:
            tag = baca.tags.only(document, tag)
            deactivate = True
        abjad.attach(
            markup,
            leaf,
            deactivate=deactivate,
            site='SOC2',
            tag=tag,
            )
        # if overriding spacing for just one document:
        if document:
            class_ = SpacingOverrideCommand
            class_._exclude_other_spacing_sections_from_document(
                document, leaf)
            class_._exclude_other_spacing_markup_from_document(document, leaf)

    @staticmethod
    def _exclude_other_spacing_markup_from_document(document, leaf):
        tags = (baca.tags.SPACING_MARKUP, baca.tags.SPACING_OVERRIDE_MARKUP)
        my_document = baca.tags.only(document)
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if not wrapper.tag:
                continue
            words = wrapper.tag.split(':')
            if not any(tag in words for tag in tags):
                continue
            if my_document in words:
                continue
            wrapper._tag = baca.tags.forbid(document, wrapper.tag)

    @staticmethod
    def _exclude_other_spacing_sections_from_document(document, leaf):
        my_document = baca.tags.only(document)
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            assert isinstance(wrapper.tag, str)
            if my_document in wrapper.tag.split(':'):
                continue
            wrapper._tag = baca.tags.forbid(document, wrapper.tag)

    ### PUBLIC PROPERTIES ###

    @property
    def document(self):
        r'''Gets document.

        Set to tag, string or none.

        Returns string or none.
        '''
        if self._document is not None:
            assert isinstance(self._document, str)
        return self._document

    @property
    def duration(self):
        r'''Gets duration.

        Defaults to none.

        Set to nonreduced fraction or none.

        Returns nonreduced fraction.
        '''
        return self._duration
