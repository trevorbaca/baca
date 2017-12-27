import abjad
import baca
from .Command import Command


class TagCommand(Command):
    r'''Tag command.

    ..  container:: example

        >>> baca.TagCommand()
        TagCommand(selector=baca.leaves())

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     baca.tag('ViolinI', baca.leaves()[:2]),
        ...     baca.tag('ViolinI.ViolinII', baca.leaves()[2:]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs', remove=True)

        >>> abjad.f(lilypond_file[abjad.Score], strict=79)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tag',
        )

    ### INITIALIZER ###

    def __init__(self, selector='baca.leaves()', tag=None):
        Command.__init__(self, selector=selector)
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
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
        leaves = baca.select(argument).leaves()
        container = abjad.Container()
        abjad.mutate(leaves).wrap(container)
        string = rf'\tag {self.tag}'
        literal = abjad.LilyPondLiteral(string, 'before')
        abjad.attach(literal, container)

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self):
        r'''Gets tag.

        Returns string.
        '''
        return self._tag
