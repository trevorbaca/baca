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
        '_build_prefix',
        '_duration',
        )

    ### INITIALIZER ###

    def __init__(self, duration=None, selector='baca.leaf(0)'):
        Command.__init__(self, selector=selector)
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._build_prefix = None
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
        tag = baca.Tags.SPACING
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        tag = baca.Tags.SPACING_MARKUP
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        tag = baca.Tags.build(self.build_prefix, baca.Tags.SPACING_OVERRIDE)
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                raise Exception(f'already have {tag} spacing section.')
        tag = baca.Tags.build(
            self.build_prefix,
            baca.Tags.SPACING_OVERRIDE_MARKUP,
            )
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                raise Exception(f'already have {tag} spacing override markup.')
        spacing_section = baca.SpacingSection(duration=self.duration)
        tag, deactivate = baca.Tags.SPACING_OVERRIDE, None
        if self.build_prefix:
            tag = baca.Tags.build(self.build_prefix, tag)
            deactivate = True
        abjad.attach(
            spacing_section,
            leaf,
            deactivate=deactivate,
            site='SOC1',
            tag=tag,
            )
        markup = abjad.Markup(f'({self.duration!s})').fontsize(3).bold()
        if self.build_prefix is None:
            color = 'BlueViolet'
        else:
            color = 'DarkOrange'
        markup = markup.with_color(abjad.SchemeColor(color))
        markup = abjad.new(markup, direction=abjad.Up)
        tag, deactivate = baca.Tags.SPACING_OVERRIDE_MARKUP, None
        if self.build_prefix:
            tag = baca.Tags.build(self.build_prefix, tag)
            deactivate = True
        abjad.attach(
            markup,
            leaf,
            deactivate=deactivate,
            site='SOC2',
            tag=tag,
            )
        self._negate_nonbuild_wrappers(self.build_prefix, leaf)

    ### PRIVATE METHODS ###

    def _negate_nonbuild_wrappers(self, build, leaf):
        if build is None:
            return
        tag = baca.Tags.SPACING_OVERRIDE
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            words = wrapper.tag.split('+')
            if (not wrapper.tag or
                tag not in words or
                wrapper.tag == baca.Tags.build(build, tag)):
                continue
            assert build not in words, repr(wrapper.tag)
            inverted_tag = f'-{baca.Tags.build(build)}+{wrapper.tag}'
            wrapper._tag = inverted_tag
        tag = baca.Tags.SPACING_OVERRIDE_MARKUP
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            words = wrapper.tag.split('+')
            if (not wrapper.tag or
                tag not in words or
                wrapper.tag == baca.Tags.build(build, tag)):
                continue
            assert build not in words, repr(wrapper.tag)
            inverted_tag = f'-{baca.Tags.build(build)}+{wrapper.tag}'
            wrapper._tag = inverted_tag

    ### PUBLIC PROPERTIES ###

    @property
    def build_prefix(self):
        r'''Gets build prefix.

        Set to tag, string or none.

        Returns string or none.
        '''
        if self._build_prefix is not None:
            assert isinstance(self._build_prefix, str)
        return self._build_prefix

    @property
    def duration(self):
        r'''Gets duration.

        Defaults to none.

        Set to nonreduced fraction or none.

        Returns nonreduced fraction.
        '''
        return self._duration
