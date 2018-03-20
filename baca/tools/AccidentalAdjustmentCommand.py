import abjad
import baca
from .Command import Command
from .Typing import Selector


class AccidentalAdjustmentCommand(Command):
    r'''Accidental adjustment command.

    ..  container:: example

        >>> baca.AccidentalAdjustmentCommand()
        AccidentalAdjustmentCommand(selector=baca.pleaf(0))

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', (1, -1)),
        ...     baca.force_accidentals(baca.pleaves()[:2]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'!2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            f'!4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            e'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cautionary',
        '_forced',
        '_parenthesized',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cautionary: bool = None,
        forced: bool = None,
        parenthesized: bool = None,
        selector: Selector = 'baca.pleaf(0)',
        ) -> None:
        Command.__init__(self, selector=selector)
        if cautionary is not None:
            cautionary = bool(cautionary)
        self._cautionary = cautionary
        if forced is not None:
            forced = bool(forced)
        self._forced = forced
        if parenthesized is not None:
            parenthesized = bool(parenthesized)
        self._parenthesized = parenthesized
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        r'''Inserts ``selector`` output in container.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.tag:
            if not self.tag.only_edition() and not self.tag.not_editions():
                raise Exception(f'tag must have edition: {self.tag!r}.')
            alternative_tag = self.tag.prepend('AJC')
            primary_tag = alternative_tag.invert_edition_tags()
        for pleaf in baca.select(argument).pleaves():
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                assert isinstance(pleaf, abjad.Chord)
                note_heads = pleaf.note_heads
            for note_head in note_heads:
                if not self.tag:
                    if self.cautionary:
                        note_head.is_cautionary = True
                    if self.forced:
                        note_head.is_forced = True
                    if self.parenthesized:
                        note_head.is_parenthesized = True
                else:
                    alternative = abjad.new(note_head)
                    if self.cautionary:
                        alternative.is_cautionary = True
                    if self.forced:
                        alternative.is_forced = True
                    if self.parenthesized:
                        alternative.is_parenthesized = True
                    note_head.alternative = (
                        alternative,
                        str(alternative_tag),
                        str(primary_tag),
                        )

    ### PUBLIC PROPERTIES ###

    @property
    def cautionary(self) -> bool:
        r'''Is true when command makes accidentals cautionary.
        '''
        return self._cautionary

    @property
    def forced(self) -> bool:
        r'''Is true when command forces accidentals.
        '''
        return self._forced

    @property
    def parenthesized(self) -> bool:
        r'''Is true when command parenthesizes accidentals.
        '''
        return self._parenthesized
