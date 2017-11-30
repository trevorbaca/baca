import abjad
import baca
from .Command import Command


class OverrideCommand(Command):
    r'''Override command.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.beam_positions(6),
        ...     baca.stems_up(),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            \override Beam.positions = #'(6 . 6)
                            \override Stem.direction = #up
                            c'16 [
                            d'16
                            bf'16 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''16
                            af''16
                            g''16 ]
                        }
                        {
                            a'16
                            \revert Beam.positions
                            \revert Stem.direction
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.beam_positions(6),
        ...     baca.rests_up(),
        ...     baca.stems_up(),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.TaleaRhythmMaker(
        ...             talea=rhythmos.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" % SEGMENT:EMPTY_BAR:1
                        s1 * 1/2
                            - \markup { % STAGE_NUMBER:2
                                \fontsize % STAGE_NUMBER:2
                                    #-3 % STAGE_NUMBER:2
                                    \with-color % STAGE_NUMBER:2
                                        #(x11-color 'DarkCyan) % STAGE_NUMBER:2
                                        [1] % STAGE_NUMBER:2
                                } % STAGE_NUMBER:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
            <BLANKLINE>
                            %%% MusicVoice [measure 1] %%%
                            \override Beam.positions = #'(6 . 6)
                            \override Stem.direction = #up
                            \clef "treble" % SEGMENT:EXPLICIT-CLEF:2
                            \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CLEF:COLOR:1
                            e'8 [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8 ]
            <BLANKLINE>
                            \override Rest.direction = #up
                            r8
            <BLANKLINE>
                            %%% MusicVoice [measure 2] %%%
                            e''8 [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8 ]
            <BLANKLINE>
                            %%% MusicVoice [measure 3] %%%
                            r8
            <BLANKLINE>
                            e'8 [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8 ]
            <BLANKLINE>
                            %%% MusicVoice [measure 4] %%%
                            r8
                            \revert Rest.direction
            <BLANKLINE>
                            e''8 [
            <BLANKLINE>
                            g'8 ]
                            \bar "|"
                            \revert Beam.positions
                            \revert Stem.direction
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> baca.OverrideCommand()
        OverrideCommand(selector=baca.leaves())

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_after',
        '_attribute',
        '_context',
        '_grob',
        '_tag',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        after=None,
        attribute=None,
        context=None,
        grob=None,
        selector='baca.leaves()',
        tag=None,
        value=None,
        ):
        Command.__init__(self, selector=selector)
        if after is not None:
            after = bool(after)
        self._after = after
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag
        self._value = value

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves(grace_notes=False)
        context = self.context
        grob = self.grob
        attribute = self.attribute
        value = self.value
        once = bool(len(leaves) == 1)
        string = abjad.LilyPondFormatManager.make_lilypond_override_string(
            grob,
            attribute,
            value,
            context=context,
            once=once,
            )
        string = string[1:]
        format_slot = 'before'
        if self.after is True:
            format_slot = 'after'
        override = abjad.LilyPondCommand(string, format_slot=format_slot)
        abjad.attach(override, leaves[0], tag=self.tag)
        if once:
            return
        string = abjad.LilyPondFormatManager.make_lilypond_revert_string(
            grob,
            attribute,
            context=context,
            )
        string = string[1:]
        revert = abjad.LilyPondCommand(string, format_slot='after')
        abjad.attach(revert, leaves[-1], tag=self.tag)

    ### PUBLIC PROPERTIES ###

    @property
    def after(self):
        r'''Is true if command positions LilyPond command after selection.
        '''
        return self._after 

    @property
    def attribute(self):
        r'''Gets attribute name.

        Set to string or none.
        '''
        return self._attribute

    @property
    def context(self):
        r'''Gets context name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._context

    @property
    def grob(self):
        r'''Gets grob name.

        Set to string or none.
        '''
        return self._grob

    @property
    def tag(self):
        r'''Gets tag.

        Set to string or none.
        '''
        return self._tag

    @property
    def value(self):
        r'''Gets attribute value.

        Set to string or none.
        '''
        return self._value
