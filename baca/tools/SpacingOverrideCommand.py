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
        tag = abjad.Tags.SPACING
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        tag = abjad.Tags.SPACING_MARKUP
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        tag = abjad.Tags.SPACING_OVERRIDE
        if self.build_prefix:
            tag = abjad.Tags.build(tag, build=self.build_prefix)
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                raise Exception(f'already have {tag} spacing section.')
        tag = abjad.Tags.SPACING_OVERRIDE_MARKUP
        if self.build_prefix:
            tag = abjad.Tags.build(tag, build=self.build_prefix)
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                raise Exception(f'already have {tag} spacing override markup.')
        spacing_section = baca.SpacingSection(duration=self.duration)
        tag, deactivate = abjad.Tags.SPACING_OVERRIDE, None
        if self.build_prefix:
            tag = abjad.Tags.build(tag, build=self.build_prefix)
            deactivate = True
        abjad.attach(
            spacing_section,
            leaf,
            deactivate=deactivate,
            site='SOC1',
            tag=tag,
            )
        markup = abjad.Markup(f'({self.duration!s})').fontsize(3).bold()
        markup = markup.with_color(abjad.SchemeColor('BlueViolet'))
        markup = abjad.new(markup, direction=abjad.Up)
        tag, deactivate = abjad.Tags.SPACING_OVERRIDE_MARKUP, None
        if self.build_prefix:
            tag = abjad.Tags.build(tag, build=self.build_prefix)
            deactivate = True
        abjad.attach(
            markup,
            leaf,
            deactivate=deactivate,
            site='SOC2',
            tag=tag,
            )
        if self.build_prefix is not None:
            self._mark_segment_wrappers_as_segment_only(leaf)

    ### PRIVATE METHODS ###

    def _mark_segment_wrappers_as_segment_only(self, leaf):
        tag = abjad.Tags.SPACING_OVERRIDE
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                tag = abjad.Tags.build(tag, build='SEGMENT')
                wrapper._tag = tag
        tag = abjad.Tags.SPACING_OVERRIDE_MARKUP
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                tag = abjad.Tags.build(tag, build='SEGMENT')
                wrapper._tag = tag

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
