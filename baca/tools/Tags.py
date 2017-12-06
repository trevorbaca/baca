import abjad
import enum


class Tags(abjad.Enumeration):
    r'''Tags.

    ..  container::

        >>> baca.Tags.EXPLICIT_CLEF_COMMAND
        Tags.EXPLICIT_CLEF_COMMAND

        >>> baca.Tags.REDUNDANT_CLEF_COMMAND
        Tags.REDUNDANT_CLEF_COMMAND

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        )

    ### CLEFS ###

    EXPLICIT_CLEF_COLOR = enum.auto()
    EXPLICIT_CLEF_COMMAND = enum.auto()
    EXPLICIT_CLEF_SHADOW_COLOR = enum.auto()
    EXPLICIT_CLEF_UNCOLOR = enum.auto()

    REAPPLIED_CLEF_COLOR = enum.auto() 
    REAPPLIED_CLEF_COMMAND = enum.auto()
    REAPPLIED_CLEF_SHADOW_COLOR = enum.auto()
    REAPPLIED_CLEF_UNCOLOR = enum.auto()

    REDUNDANT_CLEF_COLOR = enum.auto()
    REDUNDANT_CLEF_COMMAND = enum.auto()
    REDUNDANT_CLEF_SHADOW_COLOR = enum.auto()
    REDUNDANT_CLEF_UNCOLOR = enum.auto()

    ### DYNAMICS ###

    EXPLICIT_DYNAMIC_COLOR = enum.auto()
    EXPLICIT_DYNAMIC_COMMAND = enum.auto()
    EXPLICIT_DYNAMIC_SHADOW_COLOR = enum.auto()
    EXPLICIT_DYNAMIC_UNCOLOR = enum.auto()

    REDUNDANT_DYNAMIC_COLOR = enum.auto()
    REDUNDANT_DYNAMIC_COMMAND = enum.auto()
    REDUNDANT_DYNAMIC_SHADOW_COLOR = enum.auto()
    REDUNDANT_DYNAMIC_UNCOLOR = enum.auto()

    REMINDER_DYNAMIC_COLOR = enum.auto() 
    REMINDER_DYNAMIC_COMMAND = enum.auto()
    REMINDER_DYNAMIC_SHADOW_COLOR = enum.auto()
    REMINDER_DYNAMIC_UNCOLOR = enum.auto()

    ### INSTRUMENTS ###

    EXPLICIT_INSTRUMENT_CHANGE_COLORED_MARKUP = enum.auto()
    EXPLICIT_INSTRUMENT_CHANGE_MARKUP = enum.auto()
    EXPLICIT_INSTRUMENT_COLOR = enum.auto()
    EXPLICIT_INSTRUMENT_COMMAND = enum.auto()
    EXPLICIT_INSTRUMENT_SHADOW_COLOR = enum.auto()
    EXPLICIT_INSTRUMENT_SHADOW_COMMAND = enum.auto()
    EXPLICIT_INSTRUMENT_UNCOLOR = enum.auto()

    REAPPLIED_INSTRUMENT_CHANGE_COLORED_MARKUP = enum.auto()
    REAPPLIED_INSTRUMENT_CHANGE_MARKUP = enum.auto()
    REAPPLIED_INSTRUMENT_COLOR = enum.auto() 
    REAPPLIED_INSTRUMENT_COMMAND = enum.auto()
    REAPPLIED_INSTRUMENT_SHADOW_COLOR = enum.auto()
    REAPPLIED_INSTRUMENT_SHADOW_COMMAND = enum.auto()
    REAPPLIED_INSTRUMENT_UNCOLOR = enum.auto()

    REDUNDANT_INSTRUMENT_CHANGE_COLORED_MARKUP = enum.auto()
    REDUNDANT_INSTRUMENT_CHANGE_MARKUP = enum.auto()
    REDUNDANT_INSTRUMENT_COLOR = enum.auto()
    REDUNDANT_INSTRUMENT_COMMAND = enum.auto()
    REDUNDANT_INSTRUMENT_SHADOW_COLOR = enum.auto()
    REDUNDANT_INSTRUMENT_SHADOW_COMMAND = enum.auto()
    REDUNDANT_INSTRUMENT_UNCOLOR = enum.auto()

    ### METRONOME MARKS ###

    EXPLICIT_METRONOME_MARK_COLOR = enum.auto()
    EXPLICIT_METRONOME_MARK_COMMAND = enum.auto()
    EXPLICIT_METRONOME_MARK_SHADOW_COLOR = enum.auto()
    EXPLICIT_METRONOME_MARK_UNCOLOR = enum.auto()

    REDUNDANT_METRONOME_MARK_COLOR = enum.auto()
    REDUNDANT_METRONOME_MARK_COMMAND = enum.auto()
    REDUNDANT_METRONOME_MARK_SHADOW_COLOR = enum.auto()
    REDUNDANT_METRONOME_MARK_UNCOLOR = enum.auto()

    REMINDER_METRONOME_MARK_COLOR = enum.auto() 
    REMINDER_METRONOME_MARK_COMMAND = enum.auto()
    REMINDER_METRONOME_MARK_SHADOW_COLOR = enum.auto()
    REMINDER_METRONOME_MARK_UNCOLOR = enum.auto()

    ### STAFF LINES ###

    EXPLICIT_STAFF_LINES_COLOR = enum.auto()
    EXPLICIT_STAFF_LINES_COMMAND = enum.auto()
    EXPLICIT_STAFF_LINES_SHADOW_COLOR = enum.auto()
    EXPLICIT_STAFF_LINES_UNCOLOR = enum.auto()

    REAPPLIED_STAFF_LINES_COLOR = enum.auto() 
    REAPPLIED_STAFF_LINES_COMMAND = enum.auto()
    REAPPLIED_STAFF_LINES_SHADOW_COLOR = enum.auto()
    REAPPLIED_STAFF_LINES_UNCOLOR = enum.auto()

    REDUNDANT_STAFF_LINES_COLOR = enum.auto()
    REDUNDANT_STAFF_LINES_COMMAND = enum.auto()
    REDUNDANT_STAFF_LINES_SHADOW_COLOR = enum.auto()
    REDUNDANT_STAFF_LINES_UNCOLOR = enum.auto()

    ### TIME SIGNATURES ###

    EXPLICIT_TIME_SIGNATURE_COLOR = enum.auto()
    EXPLICIT_TIME_SIGNATURE_COMMAND = enum.auto()
    EXPLICIT_TIME_SIGNATURE_SHADOW_COLOR = enum.auto()
    EXPLICIT_TIME_SIGNATURE_UNCOLOR = enum.auto()

    REDUNDANT_TIME_SIGNATURE_COLOR = enum.auto()
    REDUNDANT_TIME_SIGNATURE_COMMAND = enum.auto()
    REDUNDANT_TIME_SIGNATURE_SHADOW_COLOR = enum.auto()
    REDUNDANT_TIME_SIGNATURE_UNCOLOR = enum.auto()

    ### OTHER ###

    CLOCK_TIME_MARKUP = enum.auto()
    EMPTY_START_BAR = enum.auto()
    FERMATA_BAR_LINE = enum.auto()
    FIGURE_NAME_MARKUP = enum.auto()
    SPACING = enum.auto()
    STAGE_NUMBER_MARKUP = enum.auto()

    ### PUBLIC METHODS ###

    @staticmethod
    def tag(tag, build=None):
        r'''Tags `tag` with `build` name or with SEGMENT.

        Returns string.
        '''
        if build is not None:
            return f'BUILD:{build.upper()}:{tag.name}'
        return f'SEGMENT:{tag.name}'
