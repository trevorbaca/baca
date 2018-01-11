import abjad
import baca
from .Command import Command


class SpacingOverrideCommand(Command):
    r'''Spacing override command.

    ..  container:: example

        >>> baca.SpacingOverrideCommand()
        SpacingOverrideCommand(selector=baca.leaf(0), tag='SPACING_OVERRIDE')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_build_prefix',
        '_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=None,
        selector='baca.leaf(0)',
        tag=abjad.Tags.SPACING_OVERRIDE.name,
        ):
        Command.__init__(self, selector=selector)
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._build_prefix = None
        self._duration = duration
        self._tag = tag

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
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == abjad.Tags.SPACING.name:
                abjad.detach(wrapper, leaf)
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == abjad.Tags.SPACING_MARKUP.name:
                abjad.detach(wrapper, leaf)
        if self._build_prefix is not None:
            tag = abjad.Tags.build(self.tag, build=self._build_prefix)
            deactivate = True
        else:
            tag = self.tag
            deactivate = None
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        spacing_section = baca.SpacingSection(duration=self.duration)
        abjad.attach(
            spacing_section,
            leaf,
            deactivate=deactivate,
            site='SOC1',
            tag=tag,
            )
        markup = abjad.Markup(f'({self.duration!s})').fontsize(3).bold()
        markup = markup.with_color(abjad.SchemeColor('DeepPink1'))
        markup = abjad.new(markup, direction=abjad.Up)

        tag = abjad.Tags.SPACING_OVERRIDE_MARKUP
        if self._build_prefix is not None:
            tag = abjad.Tags.build(tag, build=self._build_prefix)
        abjad.attach(
            markup,
            leaf,
            deactivate=True,
            site='SOC2',
            tag=tag,
            )
        if self._build_prefix is not None:
            self._mark_segment_wrappers_as_segment_only(leaf)

    ### PRIVATE METHODS ###

    def _mark_segment_wrappers_as_segment_only(self, leaf):
        tag = abjad.Tags.SPACING_OVERRIDE
        tag = getattr(tag, 'name', tag)
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                tag = abjad.Tags.build(tag)
                wrapper._tag = tag
        tag = abjad.Tags.SPACING_OVERRIDE_MARKUP
        tag = getattr(tag, 'name', tag)
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                tag = abjad.Tags.build(tag)
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
