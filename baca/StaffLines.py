import abjad


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
        Is true when staff lines line count equals `argument` line count.

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
