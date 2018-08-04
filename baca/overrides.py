"""
Override library.
"""
import abjad
import typing
from . import scoping
from . import typings


### CLASSES ###

class OverrideCommand(scoping.Command):
    r"""
    Override command.

    >>> from abjadext import rmakers

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
                            \override Beam.positions = #'(6 . 6)                                     %! OverrideCommand(1)
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
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
                            \revert Beam.positions                                                   %! OverrideCommand(2)
                            \revert Stem.direction                                                   %! OverrideCommand(2)
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
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override Beam.positions = #'(6 . 6)                                     %! OverrideCommand(1)
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            \override Rest.direction = #up                                           %! OverrideCommand(1)
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            r8
                            \revert Rest.direction                                                   %! OverrideCommand(2)
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
                            \revert Beam.positions                                                   %! OverrideCommand(2)
                            \revert Stem.direction                                                   %! OverrideCommand(2)
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
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaves()',
        tag_measure_number: bool = None,
        tags: typing.List = None,
        value: typing.Any = None,
        whitelist: typing.Tuple[type] = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            deactivate=deactivate,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
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
        assert self._validate_tags(tags), repr(tags)
        self._tags = tags
        self._value = value
        if whitelist is not None:
            assert isinstance(whitelist, tuple), repr(whitelist)
            assert all(issubclass(_, abjad.Leaf) for _ in whitelist)
        self._whitelist = whitelist

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
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
            parentage = abjad.inspect(leaves[0]).parentage()
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
            tag = tag.prepend('OverrideCommand(1)')
        else:
            tag = abjad.Tag('OverrideCommand(1)')
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
            tag = tag.prepend('OverrideCommand(2)')
        else:
            tag = abjad.Tag('OverrideCommand(2)')
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

### FACTORY FUNCTIONS ###

def accidental_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides accidental stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='accidental',
        selector=selector,
        value=False,
        )

def accidental_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ):
    """
    Overrides accidental transparency on.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='accidental',
        selector=selector,
        )

def accidental_x_extent_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides accidental x-extent.
    """
    return OverrideCommand(
        attribute='X_extent',
        grob='accidental',
        selector=selector,
        value=False,
        )

def bar_extent(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    after: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides bar line bar extent.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.bar_extent((-4, 4), selector=baca.group_by_measure()[1]),
        ...     baca.bar_extent((-4, 4), selector=baca.leaf(-1), after=True),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            \override Staff.BarLine.bar-extent = #'(-4 . 4)                          %! OverrideCommand(1)
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
                            \revert Staff.BarLine.bar-extent                                         %! OverrideCommand(2)
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \once \override Staff.BarLine.bar-extent = #'(-4 . 4)                    %! OverrideCommand(1)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return OverrideCommand(
        after=after,
        attribute='bar_extent',
        context='Staff',
        grob='bar_line',
        selector=selector,
        value=pair,
        )

def bar_extent_zero() -> scoping.Suite:
    """
    Makes bar-extent zero suite.
    """
    return scoping.suite(
        bar_extent(
            (0, 0),
            after=True,
            selector='baca.leaves()',
            ),
        bar_extent(
            (0, 0),
            after=True,
            selector='baca.leaf(-1)',
            ),
        )

def bar_line_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides bar line transparency.

    ..  container:: example

        Makes all bar lines transparent:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     baca.bar_line_transparent(),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override Score.BarLine.transparent = ##t                                %! OverrideCommand(1)
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
                            \revert Score.BarLine.transparent                                        %! OverrideCommand(2)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Makes bar line before measure 1 transparent:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     baca.bar_line_transparent(selector=baca.group_by_measure()[1]),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            \override Score.BarLine.transparent = ##t                                %! OverrideCommand(1)
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
                            \revert Score.BarLine.transparent                                        %! OverrideCommand(2)
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        context='Score',
        grob='bar_line',
        selector=selector,
        )

def beam_positions(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides beam positions.

    ..  container:: example

        Overrides beam positions on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_positions(6),
        ...     baca.rests_around([2], [4]),
        ...     time_treatments=[-1],
        ...     )
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
                        \times 4/5 {
                            \override Beam.positions = #'(6 . 6)                                     %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \times 4/5 {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Beam.positions                                                   %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides beam positions on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.beam_positions(6, selector=baca.tuplet(1)),
        ...     baca.rests_around([2], [4]),
        ...     time_treatments=[-1],
        ...     )
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
                        \times 4/5 {
                            r8
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \times 4/5 {
                            \override Beam.positions = #'(6 . 6)                                     %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                            \revert Beam.positions                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='positions',
        value=(n, n),
        grob='beam',
        selector=selector,
        )

def beam_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides beam stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='beam',
        selector=selector,
        value=False,
        )

def beam_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides beam transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='beam',
        selector=selector,
        )

def clef_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides clef extra offset.
    """
    return OverrideCommand(
        attribute='extra_offset',
        context='Staff',
        grob='clef',
        selector=selector,
        value=pair,
        )

def clef_shift(
    clef: typing.Union[str, abjad.Clef],
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> scoping.Suite:
    """
    Shifts clef to left by width of clef.
    """
    if isinstance(clef, str):
        clef = abjad.Clef(clef)
    if isinstance(clef, (int, float)):
        extra_offset_x = clef
    else:
        assert isinstance(clef, abjad.Clef)
        width = clef._to_width[clef.name]
        extra_offset_x = -width
    command = scoping.suite(
        clef_x_extent_false(),
        clef_extra_offset((extra_offset_x, 0)),
        )
    scoping.tag(
        abjad.tags.SHIFTED_CLEF,
        command,
        tag_measure_number=True,
        )
    return command

def clef_x_extent_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides clef x-extent.
    """
    return OverrideCommand(
        attribute='X_extent',
        context='Staff',
        grob='clef',
        selector=selector,
        value=False,
        )

def dls_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides dynamic line spanner padding.
    """
    return OverrideCommand(
        attribute='padding',
        value=str(n),
        grob='dynamic_line_spanner',
        selector=selector,
        )

def dls_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides dynamic line spanner staff padding

    ..  container:: example

        Overrides dynamic line spanner staff padding on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dls_staff_padding(4),
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.hairpin(
        ...             'p < f',
        ...             remove_length_1_spanner_start=True,
        ...             selector=baca.tleaves(),
        ...             ),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override DynamicLineSpanner.staff-padding = #'4                         %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            r4
                            \revert DynamicLineSpanner.staff-padding                                 %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides dynamic line spanner staff padding on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dls_staff_padding(4, selector=baca.tuplet(1)),
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.hairpin(
        ...             'p < f',
        ...             remove_length_1_spanner_start=True,
        ...             selector=baca.tleaves(),
        ...             ),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override DynamicLineSpanner.staff-padding = #'4                         %! OverrideCommand(1)
                            fs''16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='staff_padding',
        value=str(n),
        grob='dynamic_line_spanner',
        selector=selector,
        )

def dls_up(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides dynamic line spanner direction.

    ..  container:: example

        Up-overrides dynamic line spanner direction on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dls_up(),
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.hairpin(
        ...             'p < f',
        ...             remove_length_1_spanner_start=True,
        ...             selector=baca.tleaves(),
        ...             ),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override DynamicLineSpanner.direction = #up                             %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            r4
                            \revert DynamicLineSpanner.direction                                     %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Up-overrides dynamic line spanner direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dls_up(selector=baca.tuplet(1)),
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.hairpin(
        ...             'p < f',
        ...             remove_length_1_spanner_start=True,
        ...             selector=baca.tleaves(),
        ...             ),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override DynamicLineSpanner.direction = #up                             %! OverrideCommand(1)
                            fs''16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            \<                                                                       %! PiecewiseIndicatorCommand(1)
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \f                                                                       %! PiecewiseIndicatorCommand(2)
                            ]
                            \revert DynamicLineSpanner.direction                                     %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            \p                                                                       %! PiecewiseIndicatorCommand(1)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='dynamic_line_spanner',
        selector=selector,
        )

def dots_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides dots stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='dots',
        selector=selector,
        value=False,
        )

def dots_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides dots transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='dots',
        selector=selector,
        )

def dynamic_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> scoping.Suite:
    """
    Shifts dynamic to left by calculated width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    return scoping.suite(
        dynamic_text_extra_offset(
            (extra_offset_x, 0),
            selector=selector,
            ),
        dynamic_text_x_extent_zero(
            selector=selector,
            ),
        )

# TODO: test and document?
# TODO: appears not to do anything?
def dynamic_text_center(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> scoping.Suite:
    """
    Overrides dynamic text self-alignment-X and dynamic text X-extent.
    """
    command_1 = OverrideCommand(
        attribute='self_alignment_X',
        value=abjad.Center,
        grob='dynamic_text',
        selector=selector,
        )
    command_2 = dynamic_text_x_extent_zero(
        selector=selector,
        )
    return scoping.suite(
        command_1,
        command_2,
        )

def dynamic_text_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides dynamic text extra offset.

    ..  container:: example

        Overrides dynamic text extra offset on pitched leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].pleaf(0)),
        ...     baca.dynamic_text_extra_offset((-3, 0)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \once \override DynamicText.extra-offset = #'(-3 . 0)                    %! OverrideCommand(1)
                            c'16
                            \p                                                                       %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            \f                                                                       %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides dynamic text extra offset on leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].leaf(0)),
        ...     baca.dynamic_text_extra_offset(
        ...         (-3, 0),
        ...         selector=baca.tuplets()[1:2].leaf(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override DynamicText.extra-offset = #'(-3 . 0)                    %! OverrideCommand(1)
                            fs''16
                            \f                                                                       %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raise exception on nonpair input:

        >>> baca.dynamic_text_extra_offset(2)
        Traceback (most recent call last):
            ...
        Exception: dynamic text extra offset must be pair (not 2).

    """
    if not isinstance(pair, tuple):
        raise Exception(
            f'dynamic text extra offset must be pair (not {pair}).'
            )
    if len(pair) != 2:
        raise Exception(
            f'dynamic text extra offset must be pair (not {pair}).'
            )
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='dynamic_text',
        selector=selector,
        )

# TODO: test and document?
# TODO: appears not to do anything?
def dynamic_text_left(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> scoping.Suite:
    """
    Overrides dynamic text self-alignment-X and dynamic text X-extent.
    """
    command_1 = OverrideCommand(
        attribute='self_alignment_X',
        value=abjad.Left,
        grob='dynamic_text',
        selector=selector,
        )
    command_2 = dynamic_text_x_extent_zero(
        selector=selector,
        )
    return scoping.suite(
        command_1,
        command_2,
        )

def dynamic_text_parent_alignment_x(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text parent alignment X to ``n``.
    """
    return OverrideCommand(
        attribute='parent_alignment_X',
        value=n,
        grob='dynamic_text',
        selector=selector,
        )

# TODO: test and document?
# TODO: appears not to do anything?
def dynamic_text_right(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> scoping.Suite:
    """
    Overrides dynamic text self-alignment-X and dynamic text X-extent.
    """
    command_1 = OverrideCommand(
        attribute='self_alignment_X',
        value=abjad.Right,
        grob='dynamic_text',
        selector=selector,
        )
    command_2 = dynamic_text_x_extent_zero(
        selector=selector,
        )
    return scoping.suite(
        command_1,
        command_2,
        )

def dynamic_text_stencil_false(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        value=False,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_transparent(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_x_extent_zero(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute='X_extent',
        value=(0, 0),
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_x_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute='X_offset',
        value=n,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_y_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text Y-extent.
    """
    return OverrideCommand(
        attribute='Y_offset',
        value=n,
        grob='dynamic_text',
        selector=selector,
        )

def flag_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides flag stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='flag',
        selector=selector,
        value=False,
        )

def flag_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides flag transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='flag',
        selector=selector,
        )

def glissando_thickness(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    """
    Overrides glissando thickness.
    """
    return OverrideCommand(
        attribute='thickness',
        value=str(n),
        grob='glissando',
        selector=selector,
        )



def hairpin_shorten_pair(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides hairpin shorten pair.
    """
    return OverrideCommand(
        attribute='shorten_pair',
        value=pair,
        grob='hairpin',
        selector=selector,
        )

def hairpin_start_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> scoping.Suite:
    """
    Shifts hairpin start dynamic to left by width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    return scoping.suite(
        dynamic_text_extra_offset((extra_offset_x, 0)),
        dynamic_text_x_extent_zero(),
        hairpin_shorten_pair((hairpin_shorten_left, 0)),
        )

def hairpin_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides hairpin stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        value=False,
        grob='hairpin',
        selector=selector,
        )

def hairpin_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides hairpin transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='hairpin',
        selector=selector,
        )

def mmrest_text_color(
    color: str = 'red',
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text color.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_color('red'),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override MultiMeasureRestText.color = #red                              %! OverrideCommand(1)
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            ^ \markup {                                                              %! IndicatorCommand
                                \override                                                            %! IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! IndicatorCommand
                                    \box                                                             %! IndicatorCommand
                                        still                                                        %! IndicatorCommand
                                }                                                                    %! IndicatorCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            \revert MultiMeasureRestText.color                                       %! OverrideCommand(2)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Raises exception when called on leaves other than multimeasure
        rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_color('red'),
        ...     baca.pitches([2, 4]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: only MultimeasureRest (not Note) allowed.

    """
    return OverrideCommand(
        attribute='color',
        value=color,
        grob='multi_measure_rest_text',
        selector=selector,
        whitelist=(abjad.MultimeasureRest,),
        )

def mmrest_text_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text extra offset.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_extra_offset((0, 2)),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override MultiMeasureRestText.extra-offset = #'(0 . 2)                  %! OverrideCommand(1)
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            ^ \markup {                                                              %! IndicatorCommand
                                \override                                                            %! IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! IndicatorCommand
                                    \box                                                             %! IndicatorCommand
                                        still                                                        %! IndicatorCommand
                                }                                                                    %! IndicatorCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            \revert MultiMeasureRestText.extra-offset                                %! OverrideCommand(2)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='multi_measure_rest_text',
        selector=selector,
        whitelist=(abjad.MultimeasureRest,),
        )

def mmrest_text_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text padding.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_padding(2),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override MultiMeasureRestText.padding = #2                              %! OverrideCommand(1)
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            ^ \markup {                                                              %! IndicatorCommand
                                \override                                                            %! IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! IndicatorCommand
                                    \box                                                             %! IndicatorCommand
                                        still                                                        %! IndicatorCommand
                                }                                                                    %! IndicatorCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            \revert MultiMeasureRestText.padding                                     %! OverrideCommand(2)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return OverrideCommand(
        attribute='padding',
        value=n,
        grob='multi_measure_rest_text',
        selector=selector,
        whitelist=(abjad.MultimeasureRest,),
        )

def mmrest_text_parent_center(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text parent alignment X to center.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_parent_center(),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override MultiMeasureRestText.parent-alignment-X = #0                   %! OverrideCommand(1)
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            ^ \markup {                                                              %! IndicatorCommand
                                \override                                                            %! IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! IndicatorCommand
                                    \box                                                             %! IndicatorCommand
                                        still                                                        %! IndicatorCommand
                                }                                                                    %! IndicatorCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            \revert MultiMeasureRestText.parent-alignment-X                          %! OverrideCommand(2)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return OverrideCommand(
        attribute='parent_alignment_X',
        value=0,
        grob='multi_measure_rest_text',
        selector=selector,
        whitelist=(abjad.MultimeasureRest,),
        )

def mmrest_text_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text staff padding.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_staff_padding(2),
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
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
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
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override MultiMeasureRestText.staff-padding = #2                        %! OverrideCommand(1)
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            ^ \markup {                                                              %! IndicatorCommand
                                \override                                                            %! IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! IndicatorCommand
                                    \box                                                             %! IndicatorCommand
                                        still                                                        %! IndicatorCommand
                                }                                                                    %! IndicatorCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            R1 * 3/8
                            \revert MultiMeasureRestText.staff-padding                               %! OverrideCommand(2)
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return OverrideCommand(
        attribute='staff_padding',
        value=n,
        grob='multi_measure_rest_text',
        selector=selector,
        whitelist=(abjad.MultimeasureRest,),
        )

def no_ledgers(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides note-head no-ledgers.
    """
    return OverrideCommand(
        attribute='no_ledgers',
        value=True,
        grob='note_head',
        selector=selector,
        )

def note_column_shift(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides note column force hshift.
    """
    return OverrideCommand(
        attribute='force_hshift',
        value=n,
        grob='note_column',
        selector=selector,
        )

def note_head_color(
    color: str,
    *,
    selector: typings.Selector = 'baca.pleaves()',
    ) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute='color',
        grob='note_head',
        selector=selector,
        value=color,
        )

def note_head_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides note-head stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='note_head',
        selector=selector,
        value=False,
        )

def note_head_style_cross(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides note-head style.

    ..  container:: example

        Overrides note-head style on all pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.note_head_style_cross(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override NoteHead.style = #'cross                                       %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \revert NoteHead.style                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides note-head style on pitched leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.note_head_style_cross(selector=baca.tuplet(1)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override NoteHead.style = #'cross                                       %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert NoteHead.style                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='style',
        value='cross',
        grob='note_head',
        selector=selector,
        )

def note_head_style_harmonic(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides note-head style for ``selector`` output.

    ..  container:: example

        Overrides note-head style on all PLTs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.note_head_style_harmonic(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override NoteHead.style = #'harmonic                                    %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \revert NoteHead.style                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides note-head style on PLTs in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.note_head_style_harmonic(selector=baca.tuplet(1)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override NoteHead.style = #'harmonic                                    %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert NoteHead.style                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='style',
        value='harmonic',
        grob='note_head',
        selector=selector,
        )

def note_head_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ):
    """
    Overrides note-head transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='note_head',
        selector=selector,
        )

def ottava_bracket_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides ottava bracket staff padding.
    """
    return OverrideCommand(
        attribute='staff_padding',
        context='Staff',
        value=n,
        grob='ottava_bracket',
        selector=selector,
        )

def rehearsal_mark_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides rehearsal mark extra offset.
    """
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        context='GlobalContext',
        grob='rehearsal_mark',
        selector=selector,
        )

def rehearsal_mark_y_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides rehearsal mark Y offset.
    """
    return OverrideCommand(
        attribute='Y_offset',
        value=n,
        context='GlobalContext',
        grob='rehearsal_mark',
        selector=selector,
        )

def repeat_tie_down(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides repeat tie direction.

    ..  container:: example

        Overrides repeat tie direction on pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.repeat_tie(),
        ...         ),
        ...     baca.repeat_tie_down(),
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override RepeatTie.direction = #down                                    %! OverrideCommand(1)
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            c''4
                            c''16
                            \repeatTie                                                               %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            b'4
                            \repeatTie                                                               %! SpannerCommand
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert RepeatTie.direction                                              %! OverrideCommand(2)
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides repeat tie direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.repeat_tie(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.repeat_tie_down(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            c''4
                            c''16
                            \repeatTie                                                               %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            \override RepeatTie.direction = #down                                    %! OverrideCommand(1)
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            b'4
                            \repeatTie                                                               %! SpannerCommand
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            \revert RepeatTie.direction                                              %! OverrideCommand(2)
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='repeat_tie',
        selector=selector,
        )

def repeat_tie_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides repeat tie stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='repeat_tie',
        selector=selector,
        value=False,
        )

def repeat_tie_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ):
    """
    Overrides repeat tie transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='repeat_tie',
        selector=selector,
        )

def repeat_tie_up(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides repeat tie direction.

    ..  container:: example

        Overrides repeat tie direction on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.repeat_tie(),
        ...         ),
        ...     baca.repeat_tie_up(),
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override RepeatTie.direction = #up                                      %! OverrideCommand(1)
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            c''4
                            c''16
                            \repeatTie                                                               %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            b'4
                            \repeatTie                                                               %! SpannerCommand
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert RepeatTie.direction                                              %! OverrideCommand(2)
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides repeat tie direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.repeat_tie(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.repeat_tie_up(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            c''4
                            c''16
                            \repeatTie                                                               %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            \override RepeatTie.direction = #up                                      %! OverrideCommand(1)
                            b'16
                            [
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            ]
                            b'4
                            \repeatTie                                                               %! SpannerCommand
                            b'16
                            \repeatTie                                                               %! SpannerCommand
                            \revert RepeatTie.direction                                              %! OverrideCommand(2)
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='repeat_tie',
        selector=selector,
        )

def rest_down(
    *,
    selector: typings.Selector = 'baca.rests()',
    ) -> OverrideCommand:
    r"""
    Overrides rest direction.

    ..  container:: example

        Down-overrides direction of rests:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rest_down(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Rest.direction = #down                                         %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Rest.direction                                                   %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Down-overrides direction of rests in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.rest_down(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            \once \override Rest.direction = #down                                   %! OverrideCommand(1)
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='rest',
        selector=selector,
        )

def rest_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.rest(0)',
    ) -> OverrideCommand:
    """
    Overrides rest extra offset.
    """
    if not isinstance(pair, tuple):
        raise Exception(
            f'rest extra offset must be pair (not {pair!r}).'
            )
    if len(pair) != 2:
        raise Exception(
            f'rest extra offset must be pair (not {pair!r}).'
            )
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='rest',
        selector=selector,
        )

def rest_position(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.rests()',
    ) -> OverrideCommand:
    r"""
    Overrides rest position.

    ..  container:: example

        Overrides rest position:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rest_position(-6),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Rest.staff-position = #-6                                      %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Rest.staff-position                                              %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides rest position in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.rest_position(-6),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            \once \override Rest.staff-position = #-6                                %! OverrideCommand(1)
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='staff_position',
        value=n,
        grob='rest',
        selector=selector,
        )

def rest_transparent(
    *,
    selector: typings.Selector = 'baca.rests()',
    ) -> OverrideCommand:
    r"""
    Overrides rest transparency.

    ..  container:: example

        Makes rests transparent:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.rest_transparent(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Rest.transparent = ##t                                         %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Rest.transparent                                                 %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Makes rests in tuplet 1 transparent:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.rest_transparent(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            \once \override Rest.transparent = ##t                                   %! OverrideCommand(1)
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='rest',
        selector=selector,
        )

def rest_up(
    *,
    selector: typings.Selector = 'baca.rests()',
    ) -> OverrideCommand:
    r"""
    Overrides rest direction.

    ..  container:: example

        Up-overrides rest direction:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rest_up(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Rest.direction = #up                                           %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Rest.direction                                                   %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Up-overrides direction of rests in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.rest_up(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            \once \override Rest.direction = #up                                     %! OverrideCommand(1)
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='rest',
        selector=selector,
        )

def script_color(
    color: str = 'red',
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides script color.

    ..  container:: example

        Overrides script color on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.script_color('red'),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Script.color = #red                                            %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert Script.color                                                     %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides script color on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.script_color('red'),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Script.color = #red                                            %! OverrideCommand(1)
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            \revert Script.color                                                     %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='color',
        value=color,
        grob='script',
        selector=selector,
        )

def script_down(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides script direction.

    ..  container:: example

        Down-overrides script direction on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.script_down(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Script.direction = #down                                       %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert Script.direction                                                 %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Down-overrides script direction all leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.script_down(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Script.direction = #down                                       %! OverrideCommand(1)
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            \revert Script.direction                                                 %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='script',
        selector=selector,
        )

def script_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides script extra offset.

    ..  container:: example

        Overrides script extra offset on leaf 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.script_extra_offset((-1.5, 0), selector=baca.leaf(1)),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \once \override Script.extra-offset = #'(-1.5 . 0)                       %! OverrideCommand(1)
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides script extra offset on leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.script_extra_offset((-1.5, 0), selector=baca.leaf(0)),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Script.extra-offset = #'(-1.5 . 0)                       %! OverrideCommand(1)
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='script',
        selector=selector,
        )

def script_padding(
    number: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides script padding.
    """
    return OverrideCommand(
        attribute='padding',
        value=number,
        grob='script',
        selector=selector,
        )

def script_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides script staff padding.
    """
    return OverrideCommand(
        attribute='staff_padding',
        value=n,
        grob='script',
        selector=selector,
        )

def script_up(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides script direction.

    ..  container:: example

        Up-overrides script direction on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.script_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Script.direction = #up                                         %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert Script.direction                                                 %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Up-overrides script direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.script_up(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            d'16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            bf'4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Script.direction = #up                                         %! OverrideCommand(1)
                            fs''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            e''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            ef''4
                            -\accent                                                                 %! IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IndicatorCommand
                            [
                            g''16
                            -\accent                                                                 %! IndicatorCommand
                            ]
                            \revert Script.direction                                                 %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            -\accent                                                                 %! IndicatorCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='script',
        selector=selector,
        )

def slur_down(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Overrides slur direction on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
        ...         baca.slur(),
        ...         ),
        ...     baca.slur_down(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Slur.direction = #down                                         %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            (                                                                        %! SpannerCommand
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            )                                                                        %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            (                                                                        %! SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            )                                                                        %! SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Slur.direction                                                   %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides slur direction leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
        ...         baca.slur(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.slur_down(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            (                                                                        %! SpannerCommand
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            )                                                                        %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Slur.direction = #down                                         %! OverrideCommand(1)
                            fs''16
                            [
                            (                                                                        %! SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            )                                                                        %! SpannerCommand
                            \revert Slur.direction                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='slur',
        selector=selector,
        )

def slur_up(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Up-overrides slur direction on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
        ...         baca.slur(),
        ...         ),
        ...     baca.slur_up(),
        ...     baca.stem_down(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.tuplet_bracket_down(),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Slur.direction = #up                                           %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \override TupletBracket.direction = #down                                %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            c'16
                            [
                            (                                                                        %! SpannerCommand
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            )                                                                        %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            (                                                                        %! SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            )                                                                        %! SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert Slur.direction                                                   %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                            \revert TupletBracket.direction                                          %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Up-overrides slur direction for leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
        ...         baca.slur(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.slur_up(),
        ...         ),
        ...     baca.stem_down(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.tuplet_bracket_down(),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \override TupletBracket.direction = #down                                %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            c'16
                            [
                            (                                                                        %! SpannerCommand
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            )                                                                        %! SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Slur.direction = #up                                           %! OverrideCommand(1)
                            fs''16
                            [
                            (                                                                        %! SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            )                                                                        %! SpannerCommand
                            \revert Slur.direction                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                            \revert TupletBracket.direction                                          %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='slur',
        selector=selector,
        )

def span_bar_color(
    color: str,
    *,
    after: bool = None,
    context: str = 'Score',
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides span bar color.
    """
    return OverrideCommand(
        after=after,
        attribute='color',
        value=color,
        context=context,
        grob='span_bar',
        selector=selector,
        )

def span_bar_extra_offset(
    pair: typings.NumberPair,
    *,
    after: bool = None,
    context: str = 'Score',
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides span bar extra offset.
    """
    return OverrideCommand(
        after=after,
        attribute='extra_offset',
        value=pair,
        context=context,
        grob='span_bar',
        selector=selector,
        )

def span_bar_transparent(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides span bar transparency.

    ..  container:: example

        Makes span bar before leaf 0 transparent:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.span_bar_transparent(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Score.SpanBar.transparent = ##t                          %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        context='Score',
        grob='span_bar',
        selector=selector,
        )

def stem_color(
    color: str = 'red',
    *,
    context: str = None,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides stem color.

    ..  container:: example

        Overrides stem color on pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.stem_color(color='red'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.color = #red                                              %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \revert Stem.color                                                       %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides stem color on pitched leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.stem_color('red'),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Stem.color = #red                                              %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert Stem.color                                                       %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='color',
        value=color,
        context=context,
        grob='stem',
        selector=selector,
        )

def stem_down(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides stem direction.

    ..  container:: example

        Down-overrides stem direction pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Down-overrides stem direction for leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.stem_down(),
        ...         ),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='stem',
        selector=selector,
        )

def stem_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides stem stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        grob='stem',
        selector=selector,
        value=False,
        )

def stem_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides stem transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='stem',
        selector=selector,
        )

def stem_up(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides stem direction.

    ..  container:: example

        Up-overrides stem direction on pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 2',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 2"
                {
                    \voiceTwo
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Up-overrides stem direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 2',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [10]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_down(),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.stem_up(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 2"
                {
                    \voiceTwo
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            bf'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='stem',
        selector=selector,
        )

def strict_note_spacing_off(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides spacing spanner strict note spacing.

    ..  container:: example

        Turns strict note spacing off on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.strict_note_spacing_off(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Score.SpacingSpanner.strict-note-spacing = ##f                 %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Score.SpacingSpanner.strict-note-spacing                         %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='strict_note_spacing',
        value=False,
        context='Score',
        grob='spacing_spanner',
        selector=selector,
        )

def sustain_pedal_staff_padding(
    n: typings.Number,
    *,
    context: str = 'Staff',
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides sustain pedal staff padding.

    ..  container:: example

        Overrides sustain pedal staff padding on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.sustain_pedal(selector=baca.rleaves()),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! SpannerCommand
                            r8
                            \sustainOn                                                               %! SpannerCommand
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! SpannerCommand
                            fs''16
                            \sustainOff                                                              %! SpannerCommand
                            [
                            \sustainOn                                                               %! SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! SpannerCommand
                            a'16
                            \sustainOff                                                              %! SpannerCommand
                            \sustainOn                                                               %! SpannerCommand
                            r4
                            \sustainOff                                                              %! SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides sustain pedal staff padding on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.sustain_pedal(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.sustain_pedal_staff_padding(4),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! SpannerCommand
                            r8
                            \sustainOn                                                               %! SpannerCommand
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                            \sustainOff                                                              %! SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \sustainOff                                                              %! SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! SpannerCommand
                            a'16
                            \sustainOn                                                               %! SpannerCommand
                            r4
                            \sustainOff                                                              %! SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='staff_padding',
        value=n,
        context=context,
        grob='sustain_pedal_line_spanner',
        selector=selector,
        )

def text_script_color(
    color: str = 'red',
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script color.

    ..  container:: example

        Overrides text script color on all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.text_script_color('red'),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.color = #red                                        %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TextScript.color                                                 %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides text script color on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.text_script_color('red'),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.color = #red                                        %! OverrideCommand(1)
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TextScript.color                                                 %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_color('red'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='color',
        blacklist=blacklist,
        value=color,
        grob='text_script',
        selector=selector,
        )

def text_script_down(
    selector: typings.Selector = 'baca.leaves()',
    *,
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script direction.

    ..  container:: example

        Down-overrides text script direction on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.text_script_down(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.direction = #down                                   %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TextScript.direction                                             %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Down-overrides text script direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.text_script_down(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.direction = #down                                   %! OverrideCommand(1)
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TextScript.direction                                             %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_down()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='direction',
        blacklist=blacklist,
        value=abjad.Down,
        grob='text_script',
        selector=selector,
        )

def text_script_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script extra offset.

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_extra_offset((0, 2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='extra_offset',
        blacklist=blacklist,
        value=pair,
        grob='text_script',
        selector=selector,
        )

def text_script_font_size(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    """
    Overrides text script font size.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='font_size',
        blacklist=blacklist,
        value=n,
        grob='text_script',
        selector=selector,
        )

def text_script_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script padding.

    ..  container:: example

        Overrides text script padding on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         selector=baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.text_script_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.padding = #4                                        %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TextScript.padding                                               %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides text script padding on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.text_script_padding(4),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.padding = #4                                        %! OverrideCommand(1)
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TextScript.padding                                               %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_padding(2),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='padding',
        blacklist=blacklist,
        value=n,
        grob='text_script',
        selector=selector,
        )

def text_script_parent_center(
    selector: typings.Selector = 'baca.leaves()',
    *,
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script parent alignment X to center.

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_parent_center()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='parent_alignment_X',
        blacklist=blacklist,
        value=0,
        grob='text_script',
        selector=selector,
        )

def text_script_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script staff padding.

    ..  container:: example

        Overrides text script staff padding on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.text_script_staff_padding(n=4),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.staff-padding = #4                                  %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TextScript.staff-padding                                         %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides text script staff padding on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.text_script_staff_padding(4),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.staff-padding = #4                                  %! OverrideCommand(1)
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TextScript.staff-padding                                         %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_staff_padding(2)
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='staff_padding',
        blacklist=blacklist,
        value=n,
        grob='text_script',
        selector=selector,
        )

def text_script_up(
    selector: typings.Selector = 'baca.leaves()',
    *,
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    r"""
    Overrides text script direction.

    ..  container:: example

        Up-overrides text script direction on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.text_script_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.direction = #up                                     %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TextScript.direction                                             %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Up-overrides text script direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.text_script_up(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IndicatorCommand
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.direction = #up                                     %! OverrideCommand(1)
                            fs''16
                            ^ \markup { "lo stesso tempo" }                                          %! IndicatorCommand
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TextScript.direction                                             %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.markup(
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_up()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='direction',
        blacklist=blacklist,
        value=abjad.Up,
        grob='text_script',
        selector=selector,
        )

def text_script_x_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    """
    Overrides text script X-offset.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='X_offset',
        blacklist=blacklist,
        value=n,
        grob='text_script',
        selector=selector,
        )

def text_script_y_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    allow_mmrests: bool = False,
    ) -> OverrideCommand:
    """
    Overrides text script Y-offset.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute='Y_offset',
        blacklist=blacklist,
        value=n,
        grob='text_script',
        selector=selector,
        )

def text_spanner_left_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides text spanner left padding.
    """
    return OverrideCommand(
        attribute='bound_details__left__padding',
        value=n,
        grob='text_spanner',
        selector=selector,
        )

def text_spanner_right_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides text spanner right padding.
    """
    return OverrideCommand(
        attribute='bound_details__right__padding',
        value=n,
        grob='text_spanner',
        selector=selector,
        )

def text_spanner_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides text spanner staff padding.

    ..  container:: example

        Overrides text spanner staff padding on all trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.text_spanner_staff_padding(6),
        ...     baca.text_script_staff_padding(6),
        ...     baca.text_spanner(
        ...         'pont. => ord.',
        ...         selector=baca.tleaves(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextSpanner.staff-padding = #6                                 %! OverrideCommand(1)
                            \override TextScript.staff-padding = #6                                  %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            - \abjad_dashed_line_with_arrow                                          %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PiecewiseIndicatorCommand(1)
                            \startTextSpan                                                           %! PiecewiseIndicatorCommand(1)
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \stopTextSpan                                                            %! PiecewiseIndicatorCommand(2)
                            r4
                            \revert TextSpanner.staff-padding                                        %! OverrideCommand(2)
                            \revert TextScript.staff-padding                                         %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides text spanner staff padding on trimmed leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.text_spanner_staff_padding(6),
        ...         ),
        ...     baca.text_script_staff_padding(6),
        ...     baca.text_spanner(
        ...        'pont. => ord.',
        ...         selector=baca.tuplets()[1:2].tleaves(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextScript.staff-padding = #6                                  %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TextSpanner.staff-padding = #6                                 %! OverrideCommand(1)
                            fs''16
                            - \abjad_dashed_line_with_arrow                                          %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! PiecewiseIndicatorCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PiecewiseIndicatorCommand(1)
                            \startTextSpan                                                           %! PiecewiseIndicatorCommand(1)
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \stopTextSpan                                                            %! PiecewiseIndicatorCommand(2)
                            ]
                            \revert TextSpanner.staff-padding                                        %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TextScript.staff-padding                                         %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='staff_padding',
        value=n,
        grob='text_spanner',
        selector=selector,
        )

def text_spanner_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides text spanner stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        value=False,
        grob='text_spanner',
        selector=selector,
        )

def text_spanner_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides text spanner transparent.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='text_spanner',
        selector=selector,
        )

def text_spanner_y_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides text spanner Y-offset.
    """
    return OverrideCommand(
        attribute='Y_offset',
        value=n,
        grob='text_spanner',
        selector=selector,
        )

def tie_down(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides tie direction.

    ..  container:: example

        Overrides tie direction on pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_up(),
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.tie(),
        ...         ),
        ...     baca.tie_down(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            \override Tie.direction = #down                                          %! OverrideCommand(1)
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ]
                            c''4
                            ~                                                                        %! SpannerCommand
                            c''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ~                                                                        %! SpannerCommand
                            ]
                            b'4
                            ~                                                                        %! SpannerCommand
                            b'16
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            \revert Tie.direction                                                    %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides tie direction on pitched leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_up(),
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.tie(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tie_down(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #up                                           %! OverrideCommand(1)
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ]
                            c''4
                            ~                                                                        %! SpannerCommand
                            c''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            \override Tie.direction = #down                                          %! OverrideCommand(1)
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ~                                                                        %! SpannerCommand
                            ]
                            b'4
                            ~                                                                        %! SpannerCommand
                            b'16
                            \revert Tie.direction                                                    %! OverrideCommand(2)
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='tie',
        selector=selector,
        )

def tie_up(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    r"""
    Overrides tie direction.

    ..  container:: example

        Overrides tie direction on pitched leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_down(),
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.tie(),
        ...         ),
        ...     baca.tie_up(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            \override Tie.direction = #up                                            %! OverrideCommand(1)
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ]
                            c''4
                            ~                                                                        %! SpannerCommand
                            c''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ~                                                                        %! SpannerCommand
                            ]
                            b'4
                            ~                                                                        %! SpannerCommand
                            b'16
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            \revert Tie.direction                                                    %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides tie direction on pitched leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[11, 11, 12], [11, 11, 11], [11]],
        ...     baca.rests_around([2], [4]),
        ...     baca.stem_down(),
        ...     baca.map(
        ...         baca.qruns(),
        ...         baca.tie(),
        ...         ),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tie_up(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            \override Stem.direction = #down                                         %! OverrideCommand(1)
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ]
                            c''4
                            ~                                                                        %! SpannerCommand
                            c''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            \override Tie.direction = #up                                            %! OverrideCommand(1)
                            b'16
                            ~                                                                        %! SpannerCommand
                            [
                            b'16
                            ~                                                                        %! SpannerCommand
                            ]
                            b'4
                            ~                                                                        %! SpannerCommand
                            b'16
                            \revert Tie.direction                                                    %! OverrideCommand(2)
                            r16
                        }
                        \times 4/5 {
                            b'16
                            \revert Stem.direction                                                   %! OverrideCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='tie',
        selector=selector,
        )

def time_signature_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides time signature extra offset.

    ..  container:: example

        Overrides time signature extra offset on leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.time_signature_extra_offset((-6, 0)),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)            %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    assert isinstance(pair, tuple), repr(pair)
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        context='Score',
        grob='time_signature',
        selector=selector,
        )

def time_signature_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides time signature transparency.

    ..  container:: example

        Makes all time signatures transparent:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.time_signature_transparent(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Score.TimeSignature.transparent = ##t                          %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Score.TimeSignature.transparent                                  %! OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        context='Score',
        grob='time_signature',
        selector=selector,
        )

def tremolo_down(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> OverrideCommand:
    """
    Overrides stem tremolo extra offset.
    """
    pair = (0, -n)
    return OverrideCommand(
        attribute='extra_offset',
        value=str(pair),
        grob='stem_tremolo',
        selector=selector,
        )

def trill_spanner_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.tleaves().with_next_leaf()',
    ) -> OverrideCommand:
    """
    Overrides trill spanner staff padding.
    """
    return OverrideCommand(
        attribute='staff_padding',
        value=n,
        grob='trill_spanner',
        selector=selector,
        )

def tuplet_bracket_down(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides tuplet bracket direction.

    ..  container:: example

        Overrides tuplet bracket direction on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.tuplet_bracket_down(),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \override TupletBracket.direction = #down                                %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                            \revert TupletBracket.direction                                          %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides tuplet bracket direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tuplet_bracket_down(),
        ...         ),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.direction = #down                                %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TupletBracket.direction                                          %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Down,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_bracket_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides tuplet bracket extra offset.

    ..  container:: example

        Overrides tuplet bracket extra offset on leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_extra_offset((-1, 0)),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override TupletBracket.extra-offset = #'(-1 . 0)                  %! OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides tuplet bracket extra offset on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tuplet_bracket_extra_offset((-1, 0)),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override TupletBracket.extra-offset = #'(-1 . 0)                  %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_bracket_outside_staff_priority(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides tuplet bracket outside-staff-priority.
    """
    return OverrideCommand(
        attribute='outside_staff_priority',
        value=n,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_bracket_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides tuplet bracket padding.
    """
    return OverrideCommand(
        attribute='padding',
        value=n,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_bracket_shorten_pair(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    """
    Overrides tuplet bracket shorten pair.
    """
    return OverrideCommand(
        attribute='shorten_pair',
        value=pair,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_bracket_staff_padding(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides tuplet bracket staff padding.

    ..  container:: example

        Overrides tuplet bracket staff padding on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides tuplet bracket staff padding on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tuplet_bracket_staff_padding(5),
        ...         ),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='staff_padding',
        value=n,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_bracket_up(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    r"""
    Overrides tuplet bracket direction.

    ..  container:: example

        Override tuplet bracket direction on leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.tuplet_bracket_up(),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \override TupletBracket.direction = #up                                  %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                            \revert TupletBracket.direction                                          %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Override tuplet bracket direction on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tuplet_bracket_up(),
        ...         ),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.direction = #up                                  %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \revert TupletBracket.direction                                          %! OverrideCommand(2)
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='direction',
        value=abjad.Up,
        grob='tuplet_bracket',
        selector=selector,
        )

def tuplet_number_denominator(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    return OverrideCommand(
        attribute='text',
        value='tuplet-number::calc-denominator-text',
        grob='tuplet_number',
        selector=selector,
        )

def tuplet_number_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides tuplet number extra offset.

    ..  container:: example

        Overrides tuplet number extra offset on leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.tuplet_number_extra_offset((-1, 0)),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            \once \override TupletNumber.extra-offset = #'(-1 . 0)                   %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Overrides tuplet number extra offset on leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.tuplet_number_extra_offset((-1, 0)),
        ...         ),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override TupletNumber.extra-offset = #'(-1 . 0)                   %! OverrideCommand(1)
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='tuplet_number',
        selector=selector,
        )

