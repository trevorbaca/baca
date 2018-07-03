import abjad
import baca
import typing
from . import typings
from .Command import Command


class BowContactPointCommandNew(Command):
    """
    Bow contact point command.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'
    
    __slots__ = (
        '_bow_contact_points',
        '_final_spanner',
        '_helper',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *tweaks: abjad.LilyPondTweakManager,
        bcps: typing.Iterable[typing.Tuple[int, int]] = None,
        final_spanner: bool = None,
        helper: typing.Callable = None,
        selector: typings.Selector = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        if bcps is None:
            self._validate_bcps(bcps)
        self._bow_contact_points = bcps
        if final_spanner is not None:
            final_spanner = bool(final_spanner)
        self._final_spanner = final_spanner
        if helper is not None:
            assert callable(helper), repr(helper)
        self._helper = helper
        self._validate_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.bow_contact_points is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        bcps = baca.sequence(self.bow_contact_points)
        if self.helper:
            bcps = self.helper(bcps, argument)
        bcps = abjad.CyclicTuple(bcps)
        lts = baca.select(argument).lts()
        total = len(lts)

        if self.final_spanner:
            add_right_text_to_me = None
        else:
            rest_count, nonrest_count = 0, 0
            for lt in reversed(lts):
                if isinstance(lt.head, abjad.Rest):
                    rest_count += 1
                else:
                    if 0 < rest_count or 0 < nonrest_count:
                        add_right_text_to_me = lt.head
                        break
                    nonrest_count += 1

        if (self.final_spanner and
            not isinstance(lts[-1], abjad.Rest) and
            len(lts[-1]) == 1):
            next_leaf_after_argument = abjad.inspect(lts[-1][-1]).get_leaf(1)
            if next_leaf_after_argument is None:
                raise Exception(
                    'can not attach final spanner:'
                    ' argument includes end of score.'
                    )

        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(
                command=self.stop_command,
                )
            if (not self.final_spanner and
                lt is lts[-1] and
                not isinstance(lt.head, abjad.Rest)):
                abjad.attach(stop_text_span, lt.head)
                break
            previous_leaf = abjad.inspect(lt.head).get_leaf(-1)
            if (isinstance(lt.head, abjad.Rest) and
                isinstance(previous_leaf, (abjad.Rest, type(None)))):
                continue
            if (isinstance(lt.head, abjad.Note) and
                isinstance(previous_leaf, abjad.Rest) and
                previous_bcp is not None):
                numerator, denominator = previous_bcp
            else:
                bcp = bcps[i]
                numerator, denominator = bcp
                i += 1
                next_bcp = bcps[i]

            markup = abjad.Markup.fraction(numerator, denominator).upright()
            if lt is lts[-1]:
                if self.final_spanner:
                    style = 'solid_line_with_arrow'
                else:
                    style = 'invisible_line'
            elif isinstance(lt.head, (abjad.Note, abjad.Chord)):
                style = 'solid_line_with_arrow'
            else:
                style = 'invisible_line'
            if lt.head is add_right_text_to_me:
                numerator, denominator = next_bcp
                right_markup = abjad.Markup.fraction(numerator, denominator)
                right_markup = right_markup.upright()
            else:
                right_markup = None
                
            start_text_span = abjad.StartTextSpan(
                command=self.start_command,
                left_text=markup,
                right_text=right_markup,
                style=style,
                )
            abjad.attach(start_text_span, lt.head)

            if 0 < i:
                abjad.attach(stop_text_span, lt.head)
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(stop_text_span, next_leaf_after_argument)
            
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if isinstance(lt.head, abjad.Rest):
                pass
            elif isinstance(previous_leaf, abjad.Rest) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    abjad.attach(abjad.Articulation('upbow'), lt.head)
                elif bcp_fraction < next_bcp_fraction:
                    abjad.attach(abjad.Articulation('downbow'), lt.head)
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    abjad.attach(abjad.Articulation('upbow'), lt.head)
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    abjad.attach(abjad.Articulation('downbow'), lt.head)
            previous_bcp = bcp

    ### PRIVATE METHODS ###

    @staticmethod
    def _validate_bcps(bcps):
        if bcps is None:
            return
        for bcp in bcps:
            assert isinstance(bcp, tuple), repr(bcp)
            assert len(bcp) == 2, repr(bcp)

    ### PUBLIC PROPERTIES ###

    @property
    def bow_contact_points(self) -> typing.Optional[
        typing.Iterable[typing.Tuple[int, int]]
        ]:
        r"""
        Gets bow contact points.

        ..  container:: example

            PATTERN. Define chunkwise spanners like this:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.bcps_new(abjad.tweak(5).staff_padding),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
            ...     baca.measures(
            ...         (1, 2),
            ...         baca.bcps_new(bcps=[(1, 5), (2, 5)]),
            ...         ),
            ...     baca.measures(
            ...         (3, 4),
            ...         baca.bcps_new(bcps=[(3, 5), (4, 5)]),
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
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
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
                                e'8
                                -\downbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    1
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                                [
                <BLANKLINE>
                                f'8
                                -\upbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    2
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                -\downbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    1
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                -\upbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    2
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                e'8
                                -\downbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    1
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                                [
                <BLANKLINE>
                                f'8
                                -\upbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    2
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                - \tweak bound-details.right.text \markup {
                                    \upright
                                        \fraction
                                            1
                                            5
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                \bacaStopTextSpanBCP
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                f'8
                                -\downbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    3
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                                [
                <BLANKLINE>
                                e'8
                                -\upbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    4
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                -\downbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    3
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                -\upbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    4
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                f'8
                                -\downbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    3
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \bacaStartTextSpanBCP
                                [
                <BLANKLINE>
                                e'8
                                -\upbow
                                \bacaStopTextSpanBCP
                                - \abjad_solid_line_with_arrow
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \upright
                                                \fraction
                                                    4
                                                    5
                                            \hspace
                                                #0.5
                                        }
                                    }
                                - \tweak bound-details.right.text \markup {
                                    \upright
                                        \fraction
                                            3
                                            5
                                    }
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                \bacaStopTextSpanBCP
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._bow_contact_points

    @property
    def final_spanner(self) -> typing.Optional[bool]:
        """
        Is true when command outputs dangling final spanner.
        """
        return self._final_spanner

    @property
    def helper(self) -> typing.Optional[typing.Callable]:
        """
        Gets BCP helper.
        """
        return self._helper

    @property
    def start_command(self) -> str:
        r"""
        Gets ``'\bacaStartTextSpanBCP'``.
        """
        return r'\bacaStartTextSpanBCP'

    @property
    def stop_command(self) -> str:
        r"""
        Gets ``'\bacaStopTextSpanBCP'``.
        """
        return r'\bacaStopTextSpanBCP'

    @property
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
        """
        Gets tweaks.
        """
        return self._tweaks
