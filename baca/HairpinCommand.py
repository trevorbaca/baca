import abjad
import baca
import typing
from .Command import Command
from .Typing import Selector


class HairpinCommand(Command):
    r"""
    Hairpin command.

    ..  container:: example

        Hairpin with effort dynamics:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.hairpin('"p" < "f"'),
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
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
                            \effort_p                                                                %! HC1
                            \<                                                                       %! HC1
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
                            \effort_f                                                                %! HC1
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        >>> baca.HairpinCommand()
        HairpinCommand(selector=baca.tleaves(), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_broken',
        '_right_broken',
        '_start',
        '_stop',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *tweaks: abjad.LilyPondTweakManager,
        deactivate: bool = None,
        left_broken: str = None,
        selector: Selector = 'baca.tleaves()',
        right_broken: str = None,
        start: abjad.Dynamic = None,
        stop: abjad.Dynamic = None,
        tags: typing.List[abjad.Tag] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if left_broken is not None:
            assert left_broken in ('<', '>', 'niente'), repr(left_broken)
        self._left_broken = left_broken
        if right_broken is not None:
            assert right_broken in ('<', '>', 'niente'), repr(right_broken)
        self._right_broken = right_broken
        if start is not None:
            assert isinstance(start, abjad.Dynamic), repr(start)
        self._start = start
        if stop is not None:
            assert isinstance(stop, abjad.Dynamic), repr(stop)
        self._stop = stop
        tags = tags or []
        assert self._validate_tags(tags), repr(tags)
        self._tags = tags
        self._validate_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        from .SegmentMaker import SegmentMaker
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves()
        spanner = abjad.Hairpin(context='Voice')
        self._apply_tweaks(spanner)
        abjad.attach(
            spanner,
            leaves,
            left_broken=self.left_broken,
            right_broken=self.right_broken,
            tag=self.tag.prepend('HC1'),
            )
        dummy = abjad.Dynamic('f')
        if self.left_broken:
            assert self.start is None, repr(self.start)
            reapplied = self._remove_reapplied_wrappers(spanner[0], dummy)
        if self.right_broken:
            assert self.stop is None, repr(self.stop)
            reapplied = self._remove_reapplied_wrappers(spanner[-1], dummy)
        if self.start:
            reapplied = self._remove_reapplied_wrappers(spanner[0], self.start)
            leaf = spanner[0]
            assert isinstance(leaf, abjad.Leaf)
            wrapper = spanner.attach(
                self.start,
                leaf,
                deactivate=self.deactivate,
                tag=self.tag.prepend('HC2'),
                wrapper=True,
                )
            if self.start == reapplied:
                SegmentMaker._treat_persistent_wrapper(
                    self.runtime['manifests'],
                    wrapper,
                    'redundant',
                    )
        if self.stop and (1 < len(spanner) or self.left_broken):
            reapplied = self._remove_reapplied_wrappers(spanner[-1], self.stop)
            leaf = spanner[-1]
            assert isinstance(leaf, abjad.Leaf)
            wrapper = spanner.attach(
                self.stop,
                leaf,
                deactivate=self.deactivate,
                tag=self.tag.prepend('HC3'),
                wrapper=True,
                )
            if self.stop == reapplied:
                SegmentMaker._treat_persistent_wrapper(
                    self.runtime['manifests'],
                    wrapper,
                    'redundant',
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def left_broken(self) -> typing.Optional[str]:
        """
        Gets left-broken hairpin string.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[str]:
        """
        Gets right-broken hairpin string.
        """
        return self._right_broken

    @property
    def start(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets hairpin start.
        """
        return self._start

    @property
    def stop(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets hairpin stop.
        """
        return self._stop

    @property
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
        """
        Gets tweaks.
        """
        return self._tweaks
