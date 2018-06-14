import abjad
import baca
import typing
from .Command import Command
from .Typing import Selector


class BowContactPointCommand(Command):
    """
    Bow contact point command.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'
    
    __slots__ = (
        '_bow_contact_points',
        '_helper',
        '_tweaks',
        )

    _default_bow_contact_points = [
        (0, 7), (4, 7), (5, 7), (6, 7), (7, 7), (6, 7),
        (7, 7), (0, 7), (7, 7), (0, 7), (7, 7),
        (0, 7), (4, 7), (5, 7), (6, 7), (7, 7), (6, 7), (7, 7),
        (0, 4), (1, 4), (2, 4), (1, 4),
        ]

    start_command = r'\startBCPTextSpan'
    stop_command = r'\stopBCPTextSpan'

    ### INITIALIZER ###

    def __init__(
        self,
        bcps: typing.Iterable[typing.Tuple[int, int]] = None,
        *tweaks: abjad.LilyPondTweakManager,
        helper: typing.Callable = None,
        selector: Selector = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        if bcps is None:
            bcps = BowContactPointCommand._default_bow_contact_points
        self._validate_bcps(bcps)
        self._bow_contact_points = bcps
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
        if self.selector:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        spanner = self._get_existing_bcp_spanner(leaves)
        if spanner is None:
            spanner = abjad.TextSpanner(
                commands=(self.start_command, self.stop_command),
                )
            self._apply_tweaks(spanner)
            abjad.attach(spanner, leaves)
        bcps = baca.sequence(self.bow_contact_points)
        if not bcps:
            return
        if self.helper:
            bcps = self.helper(bcps, argument)
        bcps = abjad.CyclicTuple(bcps)
        lts = baca.select(argument).lts()
        total = len(lts)
        previous_bcp = None
        i = 0
        for lt in lts:
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
            markup = abjad.Markup.fraction(numerator, denominator)
            spanner.attach(markup, lt.head)
            if lts is lts[-1]:
                continue
            if isinstance(lt.head, abjad.Note):
                arrow = abjad.ArrowLineSegment()
                spanner.attach(arrow, lt.head)
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

    def _get_existing_bcp_spanner(self, leaves):
        spanners = abjad.inspect(leaves).get_spanners(abjad.TextSpanner)
        for spanner in spanners:
            if spanner.commands[0] == self.start_command:
                for leaf in leaves:
                    if leaf not in spanner:
                        message = 'existing BCP spanner found but does not'
                        message += ' include all leaves.'
                        raise Exception(message)
                return spanner
                
    @staticmethod
    def _validate_bcps(bcps):
        if bcps is None:
            return
        for bcp in bcps:
            assert isinstance(bcp, tuple), repr(bcp)
            assert len(bcp) == 2, repr(bcp)

    ### PUBLIC PROPERTIES ###

    @property
    def bow_contact_points(self) -> typing.Iterable[typing.Tuple[int, int]]:
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
            ...     baca.bcps([], abjad.tweak(5).staff_padding),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> maker(
            ...     ('MusicVoice', (1, 2)),
            ...     baca.bcps([(1, 5), (2, 5)]),
            ...     )

            >>> maker(
            ...     ('MusicVoice', (3, 4)),
            ...     baca.bcps([(3, 5), (4, 5)]),
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
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
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
                                [
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                1
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                f'8
                                -\upbow
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                2
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                e'8
                                -\downbow
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                1
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                f'8
                                -\upbow
                                ]
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                2
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                e'8
                                -\downbow
                                \stopBCPTextSpan
                                [
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                1
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                f'8
                                -\upbow
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                2
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                e'8
                                -\downbow
                                ]
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                1
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                f'8
                                -\downbow
                                \stopBCPTextSpan
                                [
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                3
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                e'8
                                -\upbow
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                4
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                f'8
                                -\downbow
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                3
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                e'8
                                -\upbow
                                ]
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                4
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                f'8
                                -\downbow
                                \stopBCPTextSpan
                                [
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                3
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                e'8
                                -\upbow
                                \stopBCPTextSpan
                                - \tweak Y-extent ##f
                                - \tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \fraction
                                                4
                                                5
                                            \hspace
                                                #0.25
                                        }
                                    }
                                - \tweak arrow-width 0.25
                                - \tweak dash-fraction 1
                                - \tweak bound-details.left.stencil-align-dir-y #center
                                - \tweak bound-details.right.arrow ##t
                                - \tweak bound-details.right-broken.padding 0
                                - \tweak bound-details.right-broken.text ##f
                                - \tweak bound-details.right.padding 0.5
                                - \tweak bound-details.right.stencil-align-dir-y #center
                                - \tweak bound-details.right.text \markup {
                                    \concat
                                        {
                                            \hspace
                                                #0.0
                                            \fraction
                                                3
                                                5
                                        }
                                    }
                                - \tweak staff-padding #5
                                \startBCPTextSpan
                <BLANKLINE>
                                f'8
                                -\downbow
                                ]
                                \stopBCPTextSpan
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._bow_contact_points

    @property
    def helper(self) -> typing.Optional[typing.Callable]:
        """
        Gets BCP helper.
        """
        return self._helper

    @property
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
        """
        Gets tweaks.
        """
        return self._tweaks
