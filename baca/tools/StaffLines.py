import abjad


class StaffLines(abjad.AbjadObject):
    r'''Staff lines.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_line_count',
        '_suppress_format',
        )

    _context = 'Staff'

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, line_count=None, suppress_format=None):
        self._line_count = line_count
        if suppress_format is not None:
            suppress_format = bool(suppress_format)
        self._suppress_format = suppress_format

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when staff lines line count equals `argument` line count.

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

        '''
        if not isinstance(argument, type(self)):
            return False
        return self.line_count == argument.line_count

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.suppress_format:
            return bundle
        bundle.before.commands.append(r'\stopStaff')
        string = r'\once \override Staff.StaffSymbol.line-count ='
        string += f' {self.line_count}'
        bundle.before.commands.append(string)
        bundle.before.commands.append(r'\startStaff')
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Returns ``'Staff'``.

        ..  container:: example

            >>> baca.StaffLines(1).context
            'Staff'

        Returns ``'Staff'``.
        '''
        return self._context

    @property
    def line_count(self):
        r'''Gets line count.
        '''
        return self._line_count

    @property
    def persistent(self):
        r'''Is true.

        ..  container:: example

            >>> baca.StaffLines(1).persistent
            True

        Returns true.
        '''
        return self._persistent

    @property
    def suppress_format(self):
        r'''Is true when staff lines should not format.

        Returns true, false or none.
        '''
        return self._suppress_format
