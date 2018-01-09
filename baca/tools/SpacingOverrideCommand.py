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
        '_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=None,
        selector='baca.leaf(0)',
        ):
        Command.__init__(self, selector=selector)
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
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
        abjad.detach(baca.SpacingSection, leaf)
        tag = abjad.Tags.build(abjad.Tags.SPACING_MARKUP)
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        spacing_section = baca.SpacingSection(duration=self.duration)
        tag = abjad.Tags.build(abjad.Tags.SPACING_OVERRIDE)
        abjad.attach(spacing_section, leaf, site='SOC1', tag=tag)
        markup = abjad.Markup(f'({self.duration!s})').fontsize(3).bold()
        markup = markup.with_color(abjad.SchemeColor('DeepPink1'))
        markup = abjad.new(markup, direction=abjad.Up)
        tag = abjad.Tags.build(abjad.Tags.SPACING_OVERRIDE_MARKUP)
        abjad.attach(markup, leaf, site='SOC2', tag=tag)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration.

        Defaults to none.

        Set to nonreduced fraction or none.

        Returns nonreduced fraction.
        '''
        return self._duration
