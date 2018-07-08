import abjad
import collections
import typing


### CLASSES ###

class Accelerando(abjad.AbjadValueObject):
    r"""
    Accelerando.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> accelerando = baca.Accelerando()
        >>> abjad.attach(accelerando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
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

    __slots__ = (
        '_hide',
        '_markup',
        )

    _context = 'Score'

    _persistent = 'abjad.MetronomeMark'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        hide: bool = None,
        markup: abjad.Markup = None,
        ) -> None:
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        if markup is not None:
            assert isinstance(markup, abjad.Markup), repr(markup)
        self._markup = markup

    ### SPECIAL METHODS ###

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
        contents = r'\large \upright accel.'
        return abjad.Markup(contents=contents)

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if not self.hide:
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
    def persistent(self) -> str:
        """
        Is ``'abjad.MetronomeMark'``.

        ..  container:: example

            >>> baca.Accelerando().persistent
            'abjad.MetronomeMark'

        """
        return self._persistent

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on accelerando.
        """
        pass

class LBSD(abjad.AbjadObject):
    """
    Line-break system details.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_alignment_distances',
        '_y_offset',
        )

    _override = r'\overrideProperty'
    _override += ' Score.NonMusicalPaperColumn.line-break-system-details'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        y_offset=None,
        alignment_distances=None,
        ):
        self._y_offset = y_offset
        if alignment_distances is not None:
            assert isinstance(alignment_distances, collections.Iterable)
            alignment_distances = tuple(alignment_distances)
        self._alignment_distances = alignment_distances

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        alignment_distances = ' '.join(
            str(_) for _ in self.alignment_distances
            )
        string = rf"\baca_lbsd #{self.y_offset} #'({alignment_distances})"
        bundle.before.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def alignment_distances(self):
        """
        Gets alignment distances.
        """
        return self._alignment_distances

    @property
    def y_offset(self):
        """
        Gets Y offset.
        """
        return self._y_offset

class Ritardando(abjad.AbjadValueObject):
    r"""
    Ritardando.

    ..  container:: example

        Default ritardando:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> ritardando = baca.Ritardando()
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
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
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(ritardando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
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

    __slots__ = (
        '_hide',
        '_markup',
        )

    _context = 'Score'

    _persistent = 'abjad.MetronomeMark'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        hide: bool = None,
        markup: abjad.Markup = None,
        ) -> None:
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        if markup is not None:
            assert isinstance(markup, abjad.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

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
        contents = r'\large \upright rit.'
        return abjad.Markup(contents=contents)

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if not self.hide:
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
    def persistent(self) -> str:
        """
        Is ``'abjad.MetronomeMark'``.

        ..  container:: example

            >>> baca.Ritardando().persistent
            'abjad.MetronomeMark'

        """
        return self._persistent

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on ritardando.
        """
        pass

class StaffLines(abjad.AbjadObject):
    """
    Staff lines.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_hide',
        '_line_count',
        )

    _context = 'Staff'

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        line_count=None,
        hide=None,
        ):
        if line_count is not None:
            assert isinstance(line_count, int), repr(line_count)
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

            >>> staff_lines_1 = baca.StaffLines(line_count=1)
            >>> staff_lines_2 = baca.StaffLines(line_count=1)
            >>> staff_lines_3 = baca.StaffLines(line_count=5)

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

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self, context=None):
        if isinstance(context, abjad.Context):
            assert isinstance(context.lilypond_type, str), repr(context)
            lilypond_type = context.lilypond_type
        else:
            lilypond_type = self.context
        strings = []
        strings.append(r'\stopStaff')
        string = rf'\once \override {lilypond_type}.StaffSymbol.line-count ='
        string += f' {self.line_count}'
        strings.append(string)
        strings.append(r'\startStaff')
        return strings

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.hide:
            return bundle
        staff = abjad.inspect(component).get_parentage().get_first(abjad.Staff)
        strings = self._get_lilypond_format(context=staff)
        bundle.before.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Returns class constant ``'Staff'``.

        ..  container:: example

            >>> baca.StaffLines(line_count=1).context
            'Staff'

        Returns ``'Staff'``.
        """
        return self._context

    @property
    def hide(self):
        """
        Is true when staff lines should not appear in output.

        ..  container:: example

            >>> baca.StaffLines(line_count=1, hide=True).hide
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

            >>> baca.StaffLines(line_count=1).line_count
            1

        Returns nonnegative integer.
        """
        return self._line_count

    @property
    def persistent(self):
        """
        Is class constant true.

        ..  container:: example

            >>> baca.StaffLines(line_count=1).persistent
            True

        Returns true.
        """
        return self._persistent
