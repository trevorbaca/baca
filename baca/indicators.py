"""
Indciators.
"""
import typing

import abjad

from . import const

### CLASSES ###


class Accelerando:
    r"""
    Accelerando.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> accelerando = baca.Accelerando()
        >>> abjad.attach(accelerando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    ^ \markup {
                        \large
                            \upright
                                accel.
                        }
                    d'4
                    e'4
                    f'4
                }
            >>

    Accelerandi format as LilyPond markup.

    Accelerandi are not followed by any type of dashed line.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_hide", "_markup", "_tweaks")

    _context = "Score"

    _parameter = "METRONOME_MARK"

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        hide: bool = None,
        markup: abjad.Markup = None,
        tweaks: abjad.TweakInterface = None,
    ) -> None:
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        if markup is not None:
            assert isinstance(markup, abjad.Markup), repr(markup)
        self._markup = markup
        if tweaks is not None:
            assert isinstance(tweaks, abjad.TweakInterface), repr(tweaks)
        self._tweaks = abjad.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes accelerando.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        r"""
        Gets string representation of accelerando.

        ..  container:: example

            String representation of accelerando with default markup:

            >>> print(str(baca.Accelerando()))
            \markup {
                \large
                    \upright
                        accel.
                }

        ..  container:: example

            String representation of accelerando with custom markup:

            >>> markup = abjad.Markup(r'\bold { \italic { accelerando } }')
            >>> accelerando = baca.Accelerando(markup=markup)
            >>> print(str(accelerando))
            \markup {
                \bold
                    {
                        \italic
                            {
                                accelerando
                            }
                    }
                }

        """
        return str(self._get_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _default_markup(self):
        contents = r"\large \upright accel."
        return abjad.Markup(contents=contents)

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if not self.hide:
            if self.tweaks:
                tweaks = self.tweaks._list_format_contributions()
                bundle.after.markup.extend(tweaks)
            markup = self._get_markup()
            markup = abjad.new(markup, direction=abjad.Up)
            markup_format_pieces = markup._get_format_pieces()
            bundle.after.markup.extend(markup_format_pieces)
        return bundle

    def _get_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup()

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            >>> baca.Accelerando().context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def hide(self) -> typing.Optional[bool]:
        """
        Is true when accelerando generates no LilyPond input.
        """
        return self._hide

    @property
    def markup(self) -> typing.Optional[abjad.Markup]:
        r"""
        Gets markup of accelerando.

        ..  container:: example

            >>> markup = abjad.Markup(r'\bold { \italic { accel. } }')
            >>> accelerando = baca.Accelerando(markup=markup)
            >>> print(str(accelerando.markup))
            \markup {
                \bold
                    {
                        \italic
                            {
                                accel.
                            }
                    }
                }

        """
        return self._markup

    @property
    def parameter(self) -> str:
        """
        Is ``'METRONOME_MARK'``.

        ..  container:: example

            >>> baca.Accelerando().parameter
            'METRONOME_MARK'

        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> baca.Accelerando().persistent
            True

        """
        return self._persistent

    @property
    def tweaks(self) -> typing.Optional[abjad.TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> accelerando = baca.Accelerando()
            >>> abjad.tweak(accelerando).color = "#blue"
            >>> abjad.tweak(accelerando).extra_offset = "#'(0 . 2)"
            >>> abjad.attach(accelerando, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \tweak color #blue
                - \tweak extra-offset #'(0 . 2)
                ^ \markup {
                    \large
                        \upright
                            accel.
                    }

        ..  container:: example

            Tweaks can set at initialization:

            >>> baca.Accelerando(tweaks=abjad.tweak("#blue").color)
            Accelerando(tweaks=TweakInterface(('_literal', None), ('color', '#blue')))

        ..  container:: example

            Tweaks survive copy:

            >>> accelerando = baca.Accelerando()
            >>> abjad.tweak(accelerando).color = "#blue"
            >>> accelerando
            Accelerando(tweaks=TweakInterface(('_literal', None), ('color', '#blue')))

            >>> import copy
            >>> copy.copy(accelerando)
            Accelerando(tweaks=TweakInterface(('_literal', None), ('color', '#blue')))

        Tweak extra-offset to align accelerando markup with other metronome
        mark spanner segments.
        """
        return self._tweaks


class BarExtent:
    """
    Bar extent.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_hide", "_line_count")

    _context = "Staff"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, line_count, *, hide=None):
        if not isinstance(line_count, int):
            message = f"line count must be integer (not {line_count!r})."
            raise Exception(message)
        assert 0 <= line_count, repr(line_count)
        self._line_count = line_count
        if hide is not None:
            hide = bool(hide)
        self._hide = hide

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when bar extent line count equals ``argument`` line count.

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
        if not isinstance(argument, type(self)):
            return False
        return self.line_count == argument.line_count

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

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

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.hide:
            return bundle
        bar_extent = self._get_bar_extent(component)
        if bar_extent is None:
            return bundle
        bottom, top = bar_extent
        string = r"\override Staff.BarLine.bar-extent = "
        string += f"#'({bottom} . {top})"
        previous = abjad.get.effective(component, BarExtent, n=-1)
        if previous is None or previous.line_count <= self.line_count:
            bundle.before.commands.append(string)
        else:
            bundle.after.commands.append(string)
        return bundle

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
        tag = const.REMOVE_ALL_EMPTY_STAVES
        for sibling in siblings:
            if not abjad.get.annotation(sibling, tag):
                return True
            for leaf in abjad.iterate(sibling).leaves():
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
        tag = const.REMOVE_ALL_EMPTY_STAVES
        for sibling in siblings:
            if not abjad.get.annotation(sibling, tag):
                return True
            for leaf in abjad.iterate(sibling).leaves():
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

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Returns class constant ``'Staff'``.

        ..  container:: example

            >>> baca.BarExtent(1).context
            'Staff'

        Returns ``'Staff'``.
        """
        return self._context

    @property
    def hide(self) -> typing.Optional[bool]:
        """
        Is true when bar extent generates no LilyPond input.
        """
        return self._hide

    @property
    def line_count(self):
        """
        Gets line count.

        ..  container:: example

            >>> baca.BarExtent(1).line_count
            1

        Returns nonnegative integer.
        """
        return self._line_count

    @property
    def persistent(self):
        """
        Is true.

        ..  container:: example

            >>> baca.BarExtent(1).persistent
            True

        Class constant.
        """
        return self._persistent


class Ritardando:
    r"""
    Ritardando.

    ..  container:: example

        Default ritardando:

        >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> ritardando = baca.Ritardando()
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    ^ \markup {
                        \large
                            \upright
                                rit.
                        }
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        Custom ritardando:

        >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
        >>> ritardando = baca.Ritardando(markup=markup)
        >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    ^ \markup {
                        \bold
                            {
                                \italic
                                    {
                                        ritardando
                                    }
                            }
                        }
                    d'4
                    e'4
                    f'4
                }
            >>

    Ritardandi format as LilyPond markup.

    Ritardandi are not followed by any type of dashed line or other spanner.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_hide", "_markup", "_tweaks")

    _context = "Score"

    _parameter = "METRONOME_MARK"

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        hide: bool = None,
        markup: abjad.Markup = None,
        tweaks: abjad.TweakInterface = None,
    ) -> None:
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        if markup is not None:
            assert isinstance(markup, abjad.Markup)
        self._markup = markup
        if tweaks is not None:
            assert isinstance(tweaks, abjad.TweakInterface), repr(tweaks)
        self._tweaks = abjad.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes ritardando.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        r"""
        Gets string representation of ritardando.

        ..  container:: example

            Default ritardando:

            >>> print(str(baca.Ritardando()))
            \markup {
                \large
                    \upright
                        rit.
                }

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = baca.Ritardando(markup=markup)
            >>> print(str(ritardando))
            \markup {
                \bold
                    {
                        \italic
                            {
                                ritardando
                            }
                    }
                }

        """
        return str(self._get_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _default_markup(self):
        contents = r"\large \upright rit."
        return abjad.Markup(contents=contents)

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if not self.hide:
            if self.tweaks:
                tweaks = self.tweaks._list_format_contributions()
                bundle.after.markup.extend(tweaks)
            markup = self._get_markup()
            markup = abjad.new(markup, direction=abjad.Up)
            markup_format_pieces = markup._get_format_pieces()
            bundle.after.markup.extend(markup_format_pieces)
        return bundle

    def _get_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup()

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r"""
        Gets (historically conventional) context.

        ..  container:: example

            Default ritardando:

            >>> ritardando = baca.Ritardando()
            >>> ritardando.context
            'Score'

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = baca.Ritardando(markup=markup)
            >>> ritardando.context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def hide(self) -> typing.Optional[bool]:
        """
        Is true when ritardando generates no LilyPond input.
        """
        return self._hide

    @property
    def markup(self) -> typing.Optional[abjad.Markup]:
        r"""
        Gets markup of ritardando.

        ..  container:: example

            Default ritardando:

            >>> ritardando = baca.Ritardando()
            >>> ritardando.markup is None
            True

        ..  container:: example

            Custom ritardando:

            >>> markup = abjad.Markup(r'\bold { \italic { ritardando } }')
            >>> ritardando = baca.Ritardando(markup=markup)
            >>> abjad.show(ritardando.markup) # doctest: +SKIP

            ..  docs::

                >>> print(ritardando.markup)
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    ritardando
                                }
                        }
                    }

        """
        return self._markup

    @property
    def parameter(self) -> str:
        """
        Is ``'METRONOME_MARK'``.

        ..  container:: example

            >>> baca.Ritardando().parameter
            'METRONOME_MARK'

        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> baca.Ritardando().persistent
            True

        """
        return self._persistent

    @property
    def tweaks(self) -> typing.Optional[abjad.TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> ritardando = baca.Ritardando()
            >>> abjad.tweak(ritardando).color = "#blue"
            >>> abjad.tweak(ritardando).extra_offset = "#'(0 . 2)"
            >>> abjad.attach(ritardando, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \tweak color #blue
                - \tweak extra-offset #'(0 . 2)
                ^ \markup {
                    \large
                        \upright
                            rit.
                    }

        ..  container:: example

            Tweaks can set at initialization:

            >>> baca.Ritardando(tweaks=abjad.tweak("#blue").color)
            Ritardando(tweaks=TweakInterface(('_literal', None), ('color', '#blue')))

        ..  container:: example

            Tweaks survive copy:

            >>> ritardando = baca.Ritardando()
            >>> abjad.tweak(ritardando).color = "#blue"
            >>> ritardando
            Ritardando(tweaks=TweakInterface(('_literal', None), ('color', '#blue')))

            >>> import copy
            >>> copy.copy(ritardando)
            Ritardando(tweaks=TweakInterface(('_literal', None), ('color', '#blue')))

        Tweak extra-offset to align ritardando markup with other metronome
        mark spanner segments.
        """
        return self._tweaks


class StaffLines:
    """
    Staff lines.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_hide", "_line_count")

    _context = "Staff"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, line_count, *, hide=None):
        if not isinstance(line_count, int):
            message = f"line count must be integer (not {line_count!r})."
            raise Exception(message)
        assert 0 <= line_count, repr(line_count)
        self._line_count = line_count
        if hide is not None:
            hide = bool(hide)
        self._hide = hide

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when staff lines line count equals ``argument`` line count.

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
        if not isinstance(argument, type(self)):
            return False
        return self.line_count == argument.line_count

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

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

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.hide:
            return bundle
        staff = abjad.get.parentage(component).get(abjad.Staff)
        strings = self._get_lilypond_format(context=staff)
        bundle.before.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Returns class constant ``'Staff'``.

        ..  container:: example

            >>> baca.StaffLines(1).context
            'Staff'

        Returns ``'Staff'``.
        """
        return self._context

    @property
    def hide(self):
        """
        Is true when staff lines should not appear in output.

        ..  container:: example

            >>> baca.StaffLines(1, hide=True).hide
            True

        Defaults to none.

        Returns true, false or none.
        """
        return self._hide

    @property
    def line_count(self):
        """
        Gets line count.

        ..  container:: example

            >>> baca.StaffLines(1).line_count
            1

        Returns nonnegative integer.
        """
        return self._line_count

    @property
    def persistent(self):
        """
        Is true.

        ..  container:: example

            >>> baca.StaffLines(1).persistent
            True

        Class constant.
        """
        return self._persistent


class SpacingSection:
    r"""
    Spacing section.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(baca.SpacingSection((2, 24)), staff[0])
        >>> lilypond_file = abjad.LilyPondFile(
        ...     [staff],
        ...     includes=["baca.ily"],
        ...  )
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

    ### CLASS VARIABLES ###

    __slots__ = ("_duration",)

    _context = "Score"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, duration=None):
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._duration = duration

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a spacing section with same duration as
        this spacing section.

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
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of spacing section.

        ..  container:: example

            >>> str(baca.SpacingSection((2, 24)))
            '2/24'

        Returns string.
        """
        return str(self.duration)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf=None):
        bundle = abjad.LilyPondFormatBundle()
        numerator, denominator = self.duration.pair
        string = rf"\baca-new-spacing-section #{numerator} #{denominator}"
        bundle.before.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        """
        Gets duration.

        ..  container:: example

            >>> baca.SpacingSection((2, 24)).duration
            NonreducedFraction(2, 24)

        Returns nonreduced fraction or none.
        """
        return self._duration

    ### PUBLIC METHODS ###

    @staticmethod
    def from_string(string):
        """
        Makes spacing section from fraction ``string``.

        ..  container:: example

            >>> baca.SpacingSection.from_string('2/24')
            SpacingSection(duration=NonreducedFraction(2, 24))

        Returns new spacing section.
        """
        duration = abjad.NonreducedFraction(string)
        return SpacingSection(duration=duration)
