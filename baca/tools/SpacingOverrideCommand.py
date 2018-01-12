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
        '_eol',
        )

    _magic_lilypond_eol_adjustment = abjad.Multiplier(17, 12)

    ### INITIALIZER ###

    def __init__(self, duration=None, eol=None, selector='baca.leaf(0)'):
        Command.__init__(self, selector=selector)
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._build = None
        self._duration = duration
        if eol is not None:
            eol = bool(eol)
        self._eol = eol

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
        tag = baca.tags.SPACING
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        tag = baca.tags.SPACING_MARKUP
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            if wrapper.tag == tag:
                abjad.detach(wrapper, leaf)
        if self.build:
            tag = baca.tags.only(self.build, baca.tags.SPACING_OVERRIDE)
            for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
                if wrapper.tag == tag:
                    raise Exception(f'already have {tag} spacing override.')
            tag = baca.tags.only(
                self.build,
                baca.tags.SPACING_OVERRIDE_MARKUP,
                )
            for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
                if wrapper.tag == tag:
                    message = f'already have {tag} spacing override markup.'
                    raise Exception(message)
        duration = self.duration
        if self.eol:
            duration *= self._magic_lilypond_eol_adjustment
        spacing_section = baca.SpacingSection(duration=duration)
        tag, deactivate = baca.tags.SPACING_OVERRIDE, None
        if self.build:
            tag = baca.tags.only(self.build, tag)
            deactivate = True
        abjad.attach(
            spacing_section,
            leaf,
            deactivate=deactivate,
            site='SOC1',
            tag=tag,
            )
        markup = abjad.Markup(f'({duration!s})').fontsize(3).bold()
        if self.build is None:
            color = 'BlueViolet'
        else:
            color = 'DarkOrange'
        markup = markup.with_color(abjad.SchemeColor(color))
        markup = abjad.new(markup, direction=abjad.Up)
        tag, deactivate = baca.tags.SPACING_OVERRIDE_MARKUP, None
        if self.build:
            tag = baca.tags.only(self.build, tag)
            deactivate = True
        abjad.attach(
            markup,
            leaf,
            deactivate=deactivate,
            site='SOC2',
            tag=tag,
            )
        self._add_negation_to_other_wrappers(self.build, leaf)

    ### PRIVATE METHODS ###

    def _add_negation_to_other_wrappers(self, build, leaf):
        if build is None:
            return
        tag = baca.tags.SPACING_OVERRIDE
        for wrapper in abjad.inspect(leaf).wrappers(baca.SpacingSection):
            words = wrapper.tag.split(':')
            if (not wrapper.tag or
                tag not in words or
                any(_.startswith('+') for _ in words)):
                continue
            wrapper._tag = baca.tags.forbid(build, wrapper.tag)
        tag = baca.tags.SPACING_OVERRIDE_MARKUP
        for wrapper in abjad.inspect(leaf).wrappers(abjad.Markup):
            words = wrapper.tag.split(':')
            if (not wrapper.tag or
                tag not in words or
                any(_.startswith('+') for _ in words)):
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

    @property
    def eol(self):
        r'''Is true when EOL multiplier should apply to duration.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._eol
