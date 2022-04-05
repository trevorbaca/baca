"""
Indicators.
"""
import dataclasses
import typing

import abjad

from . import const as _const


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Accelerando:
    r"""
    Accelerando.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> accelerando = baca.Accelerando()
        >>> abjad.attach(accelerando, staff[0], direction=abjad.UP)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    ^ \markup \large \upright accel.
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> accelerando = baca.Accelerando()
        >>> bundle = abjad.bundle(
        ...     accelerando,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak extra-offset #'(0 . 2)",
        ... )
        >>> abjad.attach(bundle, note, direction=abjad.UP)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            - \tweak extra-offset #'(0 . 2)
            ^ \markup \large \upright accel.

    Tweak extra-offset to align accelerando markup with other metronome mark spanner
    segments.

    Accelerandi format as LilyPond markup.

    Accelerandi are not followed by any type of dashed line.
    """

    hide: bool = False
    markup: abjad.Markup | None = None

    context: typing.ClassVar[str] = "Score"
    directed: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "METRONOME_MARK"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    trend: typing.ClassVar[bool] = True

    def __post_init__(self):
        self.hide = bool(self.hide)
        if self.markup is not None:
            assert isinstance(self.markup, abjad.Markup), repr(self.markup)

    def __str__(self) -> str:
        r"""
        Gets string representation of accelerando.

        ..  container:: example

            String representation of accelerando with default markup:

            >>> print(str(baca.Accelerando()))
            \markup \large \upright accel.

        ..  container:: example

            String representation of accelerando with custom markup:

            >>> markup = abjad.Markup(r"\markup \bold \italic accelerando")
            >>> accelerando = baca.Accelerando(markup=markup)
            >>> print(str(accelerando))
            \markup \bold \italic accelerando

        """
        return self._get_markup().string

    @property
    def _contents_repr_string(self):
        return str(self)

    def _default_markup(self):
        contents = r"\large \upright accel."
        return abjad.Markup(rf"\markup {contents}")

    def _get_lilypond_format(self):
        return str(self)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = abjad.ContributionsBySite()
        if not self.hide:
            markup = self._get_markup()
            contributions_ = markup._get_contributions(
                component=component, wrapper=wrapper
            )
            contributions.update(contributions_)
        return contributions

    def _get_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup()


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class BarExtent:
    """
    Bar extent.

    ..  container:: example

        >>> bar_extent_1 = baca.BarExtent(1)
        >>> bar_extent_2 = baca.BarExtent(1)
        >>> bar_extent_3 = baca.BarExtent(5)

        >>> bar_extent_1 == bar_extent_1
        True
        >>> bar_extent_1 == bar_extent_2
        True
        >>> bar_extent_1 == bar_extent_3
        False

        >>> bar_extent_2 == bar_extent_1
        True
        >>> bar_extent_2 == bar_extent_2
        True
        >>> bar_extent_2 == bar_extent_3
        False

        >>> bar_extent_3 == bar_extent_1
        False
        >>> bar_extent_3 == bar_extent_2
        False
        >>> bar_extent_3 == bar_extent_3
        True

    """

    line_count: int
    hide: bool = False

    context = "Staff"
    persistent = True

    def __post_init__(self):
        if not isinstance(self.line_count, int):
            raise Exception(f"line count must be integer (not {self.line_count!r}).")
        assert 0 <= self.line_count, repr(self.line_count)
        self.hide = bool(self.hide)

    def _get_bar_extent(self, component):
        if not isinstance(component, abjad.Leaf):
            return None
        staff = abjad.get.parentage(component).get(abjad.Staff)
        staff_parent = abjad.get.parentage(staff).parent
        if staff_parent[0] is not staff and staff_parent[-1] is not staff:
            return None
        bottom, top = -2, 2
        # 7, 14 used in Huitzil
        line_count_to_bar_extent = {
            0: 0,
            1: 0,
            2: 0.5,
            3: 1,
            4: 1.5,
            5: 2,
            6: 2.5,
            7: 4,
            14: 4,
        }
        if self._staff_is_effectively_topmost(staff):
            top = line_count_to_bar_extent[self.line_count]
        if self._staff_is_effectively_bottommost(staff):
            bottom = -line_count_to_bar_extent[self.line_count]
        return (bottom, top)

    def _get_contributions(self, component=None):
        contributions = abjad.ContributionsBySite()
        if self.hide:
            return contributions
        bar_extent = self._get_bar_extent(component)
        if bar_extent is None:
            return contributions
        bottom, top = bar_extent
        string = r"\override Staff.BarLine.bar-extent = "
        string += f"#'({bottom} . {top})"
        previous = abjad.get.effective(component, BarExtent, n=-1)
        if previous is None or previous.line_count <= self.line_count:
            contributions.before.commands.append(string)
        else:
            contributions.after.commands.append(string)
        return contributions

    @staticmethod
    def _staff_is_effectively_bottommost(staff):
        assert isinstance(staff, abjad.Staff)
        staff_parent = abjad.get.parentage(staff).parent
        if staff_parent[-1] is not staff:
            return False
        if len(staff_parent) == 1:
            return True
        empty_prototype = (abjad.MultimeasureRest, abjad.Skip)
        siblings = staff_parent[:-1]
        tag = _const.REMOVE_ALL_EMPTY_STAVES
        for sibling in siblings:
            if not abjad.get.annotation(sibling, tag):
                return True
            for leaf in abjad.iterate.leaves(sibling):
                if not isinstance(leaf, empty_prototype):
                    return True
        staff_grandparent = abjad.get.parentage(staff_parent).parent
        if staff_grandparent is None:
            return True
        if staff_grandparent[-1] is staff_parent:
            return True
        if len(staff_grandparent) == 1:
            return True
        return False

    @staticmethod
    def _staff_is_effectively_topmost(staff):
        assert isinstance(staff, abjad.Staff)
        staff_parent = abjad.get.parentage(staff).parent
        if staff_parent[0] is not staff:
            return False
        if len(staff_parent) == 1:
            return True
        empty_prototype = (abjad.MultimeasureRest, abjad.Skip)
        siblings = staff_parent[1:]
        tag = _const.REMOVE_ALL_EMPTY_STAVES
        for sibling in siblings:
            if not abjad.get.annotation(sibling, tag):
                return True
            for leaf in abjad.iterate.leaves(sibling):
                if not isinstance(leaf, empty_prototype):
                    return True
        staff_grandparent = abjad.get.parentage(staff_parent).parent
        if staff_grandparent is None:
            return True
        if staff_grandparent[0] is staff_parent:
            return True
        if len(staff_grandparent) == 1:
            return True
        return False


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Ritardando:
    r"""
    Ritardando.

    ..  container:: example

        Default ritardando:

        >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> ritardando = baca.Ritardando()
        >>> abjad.attach(ritardando, staff[0], direction=abjad.UP)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    ^ \markup \large \upright rit.
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        Custom ritardando:

        >>> markup = abjad.Markup(r"\markup \bold \italic ritardando")
        >>> ritardando = baca.Ritardando(markup=markup)
        >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(ritardando, staff[0], direction=abjad.UP)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    ^ \markup \bold \italic ritardando
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> ritardando = baca.Ritardando()
        >>> bundle = abjad.bundle(
        ...     ritardando,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak extra-offset #'(0 . 2)",
        ... )
        >>> abjad.attach(bundle, note, direction=abjad.UP)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            - \tweak extra-offset #'(0 . 2)
            ^ \markup \large \upright rit.

    Tweak extra-offset to align ritardando markup with other metronome mark spanner
    segments.

    Ritardandi format as LilyPond markup.

    Ritardandi are not followed by any type of dashed line or other spanner.
    """

    hide: bool = False
    markup: abjad.Markup | None = None

    context: typing.ClassVar[str] = "Score"
    parameter: typing.ClassVar[str] = "METRONOME_MARK"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    trend: typing.ClassVar[bool] = True

    def __post_init__(self):
        self.hide = bool(self.hide)
        if self.markup is not None:
            assert isinstance(self.markup, abjad.Markup), repr(self.markup)

    def __str__(self) -> str:
        r"""
        Gets string representation of ritardando.

        ..  container:: example

            Default ritardando:

            >>> print(str(baca.Ritardando()))
            \markup \large \upright rit.

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r"\markup \bold \italic ritardando")
            >>> ritardando = baca.Ritardando(markup=markup)
            >>> print(str(ritardando))
            \markup \bold \italic ritardando

        """
        return self._get_markup().string

    @property
    def _contents_repr_string(self):
        return str(self)

    def _default_markup(self):
        contents = r"\large \upright rit."
        return abjad.Markup(rf"\markup {contents}")

    def _get_lilypond_format(self):
        return str(self)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = abjad.ContributionsBySite()
        if not self.hide:
            markup = self._get_markup()
            contributions_ = markup._get_contributions(
                component=component, wrapper=wrapper
            )
            contributions.update(contributions_)
        return contributions

    def _get_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup()


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class StaffLines:
    """
    Staff lines.

    ..  container:: example

        >>> staff_lines_1 = baca.StaffLines(1)
        >>> staff_lines_2 = baca.StaffLines(1)
        >>> staff_lines_3 = baca.StaffLines(5)

        >>> staff_lines_1 == staff_lines_1
        True
        >>> staff_lines_1 == staff_lines_2
        True
        >>> staff_lines_1 == staff_lines_3
        False

        >>> staff_lines_2 == staff_lines_1
        True
        >>> staff_lines_2 == staff_lines_2
        True
        >>> staff_lines_2 == staff_lines_3
        False

        >>> staff_lines_3 == staff_lines_1
        False
        >>> staff_lines_3 == staff_lines_2
        False
        >>> staff_lines_3 == staff_lines_3
        True

    """

    line_count: int
    hide: bool = False

    context = "Staff"
    persistent = True

    def __post_init__(self):
        if not isinstance(self.line_count, int):
            raise Exception(f"line count must be integer (not {self.line_count!r}).")
        assert 0 <= self.line_count, repr(self.line_count)
        if self.hide is not None:
            self.hide = bool(self.hide)

    def _get_lilypond_format(self, context=None):
        if isinstance(context, abjad.Context):
            assert isinstance(context.lilypond_type, str), repr(context)
            lilypond_type = context.lilypond_type
        else:
            lilypond_type = self.context
        strings = []
        strings.append(r"\stopStaff")
        string = rf"\once \override {lilypond_type}.StaffSymbol.line-count ="
        string += f" {self.line_count}"
        strings.append(string)
        strings.append(r"\startStaff")
        return strings

    def _get_contributions(self, component=None):
        contributions = abjad.ContributionsBySite()
        if self.hide:
            return contributions
        staff = abjad.get.parentage(component).get(abjad.Staff)
        strings = self._get_lilypond_format(context=staff)
        contributions.before.commands.extend(strings)
        return contributions


class SpacingSection:
    r"""
    Spacing section.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(baca.SpacingSection((2, 24)), staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "baca.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \baca-new-spacing-section #2 #24
                c'4
                d'4
                e'4
                f'4
            }

    """

    __slots__ = ("duration",)

    _context = "Score"
    _persistent = True

    def __init__(self, duration=None):
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self.duration = duration

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a spacing section with same duration as this spacing
        section.

        ..  container:: example

            >>> spacing_section_1 = baca.SpacingSection((2, 24))
            >>> spacing_section_2 = baca.SpacingSection((2, 24))
            >>> spacing_section_3 = baca.SpacingSection((3, 24))

            >>> spacing_section_1 == spacing_section_1
            True
            >>> spacing_section_1 == spacing_section_2
            True
            >>> spacing_section_1 == spacing_section_3
            False

            >>> spacing_section_2 == spacing_section_1
            True
            >>> spacing_section_2 == spacing_section_2
            True
            >>> spacing_section_2 == spacing_section_3
            False

            >>> spacing_section_3 == spacing_section_1
            False
            >>> spacing_section_3 == spacing_section_2
            False
            >>> spacing_section_3 == spacing_section_3
            True

        Returns string.
        """
        if isinstance(argument, type(self)):
            return self.duration == argument.duration
        return False

    def __hash__(self):
        """
        Hashes spacing section.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(duration={self.duration!r})"

    def __str__(self):
        """
        Gets string representation of spacing section.

        ..  container:: example

            >>> str(baca.SpacingSection((2, 24)))
            '2/24'

        Returns string.
        """
        return str(self.duration)

    def _get_contributions(self, leaf=None):
        contributions = abjad.ContributionsBySite()
        numerator, denominator = self.duration.pair
        string = rf"\baca-new-spacing-section #{numerator} #{denominator}"
        contributions.before.commands.append(string)
        return contributions

    @staticmethod
    def from_string(string):
        """
        Makes spacing section from fraction ``string``.

        ..  container:: example

            >>> baca.SpacingSection.from_string("2/24")
            SpacingSection(duration=NonreducedFraction(2, 24))

        Returns new spacing section.
        """
        duration = abjad.NonreducedFraction(string)
        return SpacingSection(duration=duration)
