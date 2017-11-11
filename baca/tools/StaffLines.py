import abjad


class StaffLines(abjad.AbjadObject):
    r'''Staff lines.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Utilities'

    __slots__ = (
        '_context',
        '_line_count',
        )

    ### INITIALIZER ###

    def __init__(self, line_count=None):
        self._context = abjad.Staff
        self._line_count = line_count

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        bundle.before.commands.append(r'\stopStaff')
        string = r'\once \override Staff.StaffSymbol.line-count ='
        string += f' {self.line_count}'
        bundle.before.commands.append(string)
        bundle.before.commands.append(r'\startStaff')
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Is staff.

        ..  container:: example

            >>> baca.StaffLines(1).context
            <class 'abjad.tools.scoretools.Staff.Staff'>

        Returns staff.
        '''
        return self._context

    @property
    def line_count(self):
        r'''Gets line count.
        '''
        return self._line_count
