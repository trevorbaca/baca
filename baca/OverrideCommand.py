import abjad
import baca
import typing
from .Command import Command
from .Typing import Selector


class OverrideCommand(Command):
    r"""
    Override command.

    >>> import abjadext.rmakers

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.beam_positions(6),
        ...     baca.stem_up(),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \override Beam.positions = #'(6 . 6)                                     %! OC1
                            \override Stem.direction = #up                                           %! OC1
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            \revert Beam.positions                                                   %! OC2
                            \revert Stem.direction                                                   %! OC2
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
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.beam_positions(6),
        ...     baca.rest_up(),
        ...     baca.stem_up(),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=abjadext.rmakers.TaleaRhythmMaker(
        ...             talea=abjadext.rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
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
                            \override Beam.positions = #'(6 . 6)                                     %! OC1
                            \override Stem.direction = #up                                           %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            \override Rest.direction = #up                                           %! OC1
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            r8
                            \revert Rest.direction                                                   %! OC2
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
                            \revert Beam.positions                                                   %! OC2
                            \revert Stem.direction                                                   %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> baca.OverrideCommand()
        OverrideCommand(selector=baca.leaves(), tags=[])

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_after',
        '_attribute',
        '_blacklist',
        '_context',
        '_grob',
        '_tags',
        '_value',
        '_whitelist',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        after: bool = None,
        attribute: str = None,
        blacklist: typing.Tuple[type] = None,
        context: str = None,
        deactivate: bool = None,
        grob: str = None,
        selector: Selector = 'baca.leaves()',
        tag_measure_number: bool = None,
        tags: typing.List = None,
        value: typing.Any = None,
        whitelist: typing.Tuple[type] = None,
        ) -> None:
        Command.__init__(
            self,
            deactivate=deactivate,
            selector=selector,
            tag_measure_number=tag_measure_number,
            )
        if after is not None:
            after = bool(after)
        self._after = after
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if blacklist is not None:
            assert isinstance(blacklist, tuple), repr(blacklist)
            assert all(issubclass(_, abjad.Leaf) for _ in blacklist)
        self._blacklist = blacklist
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags = tags
        self._value = value
        if whitelist is not None:
            assert isinstance(whitelist, tuple), repr(whitelist)
            assert all(issubclass(_, abjad.Leaf) for _ in whitelist)
        self._whitelist = whitelist

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves(grace_notes=False)
        if self.blacklist:
            for leaf in leaves:
                if isinstance(leaf, self.blacklist):
                    message = f'{type(leaf).__name__} is forbidden.'
                    raise Exception(message)
        if self.whitelist:
            for leaf in leaves:
                if not isinstance(leaf, self.whitelist):
                    names = ','.join(_.__name__ for _ in self.whitelist)
                    violator = type(leaf).__name__
                    message = f'only {names} (not {violator}) allowed.'
                    raise Exception(message)
        lilypond_type = self.context
        if lilypond_type is not None:
            assert isinstance(lilypond_type, (str)), repr(lilypond_type)
        if lilypond_type in dir(abjad):
            context = getattr(abjad, lilypond_type)
            assert issubclass(context, abjad.Context), repr(context)
            parentage = abjad.inspect(leaves[0]).get_parentage()
            context = parentage.get_first(context) or context()
            lilypond_type = context.lilypond_type
            assert isinstance(lilypond_type, str), repr(lilypond_type)
        grob = self.grob
        attribute = self.attribute
        value = self.value
        once = bool(len(leaves) == 1)
        string = abjad.LilyPondFormatManager.make_lilypond_override_string(
            grob,
            attribute,
            value,
            context=lilypond_type,
            once=once,
            )
        format_slot = 'before'
        if self.after is True:
            format_slot = 'after'
        literal = abjad.LilyPondLiteral(string, format_slot)
        tag = self.get_tag(leaves[0])
        if tag:
            tag = tag.prepend('OC1')
        else:
            tag = abjad.Tag('OC1')
        abjad.attach(
            literal,
            leaves[0],
            deactivate=self.deactivate,
            tag=tag,
            )
        if once:
            return
        string = abjad.LilyPondFormatManager.make_lilypond_revert_string(
            grob,
            attribute,
            context=lilypond_type,
            )
        literal = abjad.LilyPondLiteral(string, 'after')
        tag = self.get_tag(leaves[-1])
        if tag:
            tag = tag.prepend('OC2')
        else:
            tag = abjad.Tag('OC2')
        abjad.attach(
            literal,
            leaves[-1],
            deactivate=self.deactivate,
            tag=tag,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def after(self) -> typing.Optional[bool]:
        """
        Is true if command positions LilyPond command after selection.
        """
        return self._after 

    @property
    def attribute(self) -> typing.Optional[str]:
        """
        Gets attribute name.
        """
        return self._attribute

    @property
    def blacklist(self) -> typing.Optional[typing.Tuple[type]]:
        """
        Gets blacklist leaves.
        """
        return self._blacklist

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context name.
        """
        return self._context

    @property
    def grob(self) -> typing.Optional[str]:
        """
        Gets grob name.
        """
        return self._grob

    @property
    def value(self) -> typing.Any:
        """
        Gets attribute value.
        """
        return self._value

    @property
    def whitelist(self) -> typing.Optional[typing.Tuple[type]]:
        """
        Gets whitelist leaves.
        """
        return self._whitelist
