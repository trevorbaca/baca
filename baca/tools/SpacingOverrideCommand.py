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
        '_build',
        '_duration',
        )

    _magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

    ### INITIALIZER ###

    def __init__(self, duration=None, selector='baca.leaf(0)'):
        Command.__init__(self, selector=selector)
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._build = None
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
        self._attach_spacing_override(leaf, self.duration, build=self.build)

    ### PRIVATE METHODS ###

    @staticmethod
    def _attach_spacing_override(leaf, duration, build=None, eol=None):
        assert isinstance(leaf, abjad.Skip), repr(leaf)
        # overriding spacing for just one build:
        if build:
            include_build_tag = baca.tags.only(build)
            for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
                assert isinstance(wrapper.tag, str)
                if include_build_tag in wrapper.tag.split(':'):
                    if eol:
                        # automatic eol defers to explicit user override
                        return
                    message = 'already have {} spacing override.'
                    message = message.format(include_build_tag)
                    raise Exception(message)
            for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
                if not wrapper.tag:
                    continue
                words = wrapper.tag.split(':')
                if baca.tags.SPACING_OVERRIDE_MARKUP not in words:
                    continue
                if include_build_tag in words:
                    if eol:
                        # automatic eol defers to explicit user override
                        return
                    message = 'already have {} spacing override markup.'
                    message = message.format(include_build_tag)
                    raise Exception(message)
        # overriding fallback spacing for all builds:
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
        if build is None:
            tag = baca.tags.SPACING
            deactivate = None
        else:
            tag = baca.tags.SPACING_OVERRIDE
            tag = baca.tags.only(build, tag)
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
        if build is None:
            color = 'BlueViolet'
        elif eol:
            color = 'DarkOrange'
        else:
            color = 'DeepPink1'
        markup = markup.with_color(abjad.SchemeColor(color))
        markup = abjad.new(markup, direction=abjad.Up)
        tag, deactivate = baca.tags.SPACING_OVERRIDE_MARKUP, None
        if build:
            tag = baca.tags.only(build, tag)
            deactivate = True
        abjad.attach(
            markup,
            leaf,
            deactivate=deactivate,
            site='SOC2',
            tag=tag,
            )
        # if overriding spacing for just one build:
        if build:
            class_ = SpacingOverrideCommand
            class_._exclude_other_spacing_sections_from_build(build, leaf)
            class_._exclude_other_spacing_markup_from_build(build, leaf)

    @staticmethod
    def _exclude_other_spacing_sections_from_build(build, leaf):
        my_build = baca.tags.only(build)
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            assert isinstance(wrapper.tag, str)
            if my_build in wrapper.tag.split(':'):
                continue
            wrapper._tag = baca.tags.forbid(build, wrapper.tag)

    @staticmethod
    def _exclude_other_spacing_markup_from_build(build, leaf):
        tags = (baca.tags.SPACING_MARKUP, baca.tags.SPACING_OVERRIDE_MARKUP)
        my_build = baca.tags.only(build)
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if not wrapper.tag:
                continue
            words = wrapper.tag.split(':')
            if not any(tag in words for tag in tags):
                continue
            if my_build in words:
                continue
            wrapper._tag = baca.tags.forbid(build, wrapper.tag)

    ### PUBLIC PROPERTIES ###

    @property
    def build(self):
        r'''Gets build prefix.

        Set to tag, string or none.

        Returns string or none.
        '''
        if self._build is not None:
            assert isinstance(self._build, str)
        return self._build

    @property
    def duration(self):
        r'''Gets duration.

        Defaults to none.

        Set to nonreduced fraction or none.

        Returns nonreduced fraction.
        '''
        return self._duration
