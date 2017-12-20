import abjad
import enum


class Tags(abjad.Enumeration):
    r'''Tags.

    ..  container::

        >>> baca.Tags.EXPLICIT_CLEF
        Tags.EXPLICIT_CLEF

        >>> baca.Tags.REDUNDANT_CLEF
        Tags.REDUNDANT_CLEF

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        )

    ### CLEFS ###

    EXPLICIT_CLEF = enum.auto()
    EXPLICIT_CLEF_COLOR = enum.auto()
    EXPLICIT_CLEF_COLOR_REDRAW = enum.auto()
    EXPLICIT_CLEF_UNCOLOR = enum.auto()

    REAPPLIED_CLEF = enum.auto()
    REAPPLIED_CLEF_COLOR = enum.auto() 
    REAPPLIED_CLEF_COLOR_REDRAW = enum.auto()
    REAPPLIED_CLEF_UNCOLOR = enum.auto()

    REDUNDANT_CLEF = enum.auto()
    REDUNDANT_CLEF_COLOR = enum.auto()
    REDUNDANT_CLEF_COLOR_REDRAW = enum.auto()
    REDUNDANT_CLEF_UNCOLOR = enum.auto()

    ### DYNAMICS ###

    EXPLICIT_DYNAMIC = enum.auto()
    EXPLICIT_DYNAMIC_COLOR = enum.auto()
    EXPLICIT_DYNAMIC_COLOR_REDRAW = enum.auto()
    EXPLICIT_DYNAMIC_UNCOLOR = enum.auto()

    REAPPLIED_DYNAMIC = enum.auto()
    REAPPLIED_DYNAMIC_COLOR = enum.auto() 
    REAPPLIED_DYNAMIC_COLOR_REDRAW = enum.auto()
    REAPPLIED_DYNAMIC_UNCOLOR = enum.auto()

    REDUNDANT_DYNAMIC = enum.auto()
    REDUNDANT_DYNAMIC_COLOR = enum.auto()
    REDUNDANT_DYNAMIC_COLOR_REDRAW = enum.auto()
    REDUNDANT_DYNAMIC_UNCOLOR = enum.auto()

    ### INSTRUMENTS ###

    EXPLICIT_INSTRUMENT = enum.auto()
    EXPLICIT_INSTRUMENT_ALERT = enum.auto()
    EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    EXPLICIT_INSTRUMENT_COLOR = enum.auto()
    #
    EXPLICIT_INSTRUMENT_COLOR_REDRAW = enum.auto()
    EXPLICIT_INSTRUMENT_REDRAW = enum.auto()

    REAPPLIED_INSTRUMENT = enum.auto()
    REAPPLIED_INSTRUMENT_ALERT = enum.auto()
    REAPPLIED_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    REAPPLIED_INSTRUMENT_COLOR = enum.auto() 
    #
    REAPPLIED_INSTRUMENT_COLOR_REDRAW = enum.auto()
    REAPPLIED_INSTRUMENT_REDRAW = enum.auto()

    REDUNDANT_INSTRUMENT = enum.auto()
    REDUNDANT_INSTRUMENT_ALERT = enum.auto()
    REDUNDANT_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    REDUNDANT_INSTRUMENT_COLOR = enum.auto()
    #
    REDUNDANT_INSTRUMENT_COLOR_REDRAW = enum.auto()
    REDUNDANT_INSTRUMENT_REDRAW = enum.auto()

    ### MARGIN MARKUP ###

    EXPLICIT_MARGIN_MARKUP = enum.auto()
    EXPLICIT_MARGIN_MARKUP_CHANGE_COLORED_MARKUP = enum.auto()
    EXPLICIT_MARGIN_MARKUP_CHANGE_MARKUP = enum.auto()
    EXPLICIT_MARGIN_MARKUP_COLOR = enum.auto()
    EXPLICIT_MARGIN_MARKUP_COLOR_REDRAW = enum.auto()
    EXPLICIT_MARGIN_MARKUP_REDRAW = enum.auto()
    EXPLICIT_MARGIN_MARKUP_UNCOLOR = enum.auto()

    REAPPLIED_MARGIN_MARKUP = enum.auto()
    REAPPLIED_MARGIN_MARKUP_CHANGE_COLORED_MARKUP = enum.auto()
    REAPPLIED_MARGIN_MARKUP_CHANGE_MARKUP = enum.auto()
    REAPPLIED_MARGIN_MARKUP_COLOR = enum.auto() 
    REAPPLIED_MARGIN_MARKUP_COLOR_REDRAW = enum.auto()
    REAPPLIED_MARGIN_MARKUP_REDRAW = enum.auto()
    REAPPLIED_MARGIN_MARKUP_UNCOLOR = enum.auto()

    REDUNDANT_MARGIN_MARKUP = enum.auto()
    REDUNDANT_MARGIN_MARKUP_CHANGE_COLORED_MARKUP = enum.auto()
    REDUNDANT_MARGIN_MARKUP_CHANGE_MARKUP = enum.auto()
    REDUNDANT_MARGIN_MARKUP_COLOR = enum.auto()
    REDUNDANT_MARGIN_MARKUP_COLOR_REDRAW = enum.auto()
    REDUNDANT_MARGIN_MARKUP_REDRAW = enum.auto()
    REDUNDANT_MARGIN_MARKUP_UNCOLOR = enum.auto()

    ### METRONOME MARKS ###

    EXPLICIT_METRONOME_MARK = enum.auto()
    EXPLICIT_METRONOME_MARK_COLOR = enum.auto()
    EXPLICIT_METRONOME_MARK_COLOR_REDRAW = enum.auto()
    EXPLICIT_METRONOME_MARK_UNCOLOR = enum.auto()

    REAPPLIED_METRONOME_MARK = enum.auto()
    REAPPLIED_METRONOME_MARK_COLOR = enum.auto() 
    REAPPLIED_METRONOME_MARK_COLOR_REDRAW = enum.auto()
    REAPPLIED_METRONOME_MARK_UNCOLOR = enum.auto()

    REDUNDANT_METRONOME_MARK = enum.auto()
    REDUNDANT_METRONOME_MARK_COLOR = enum.auto()
    REDUNDANT_METRONOME_MARK_COLOR_REDRAW = enum.auto()
    REDUNDANT_METRONOME_MARK_UNCOLOR = enum.auto()

    ### STAFF LINES ###

    EXPLICIT_STAFF_LINES = enum.auto()
    EXPLICIT_STAFF_LINES_COLOR = enum.auto()
    EXPLICIT_STAFF_LINES_COLOR_REDRAW = enum.auto()
    EXPLICIT_STAFF_LINES_UNCOLOR = enum.auto()

    REAPPLIED_STAFF_LINES = enum.auto()
    REAPPLIED_STAFF_LINES_COLOR = enum.auto() 
    REAPPLIED_STAFF_LINES_COLOR_REDRAW = enum.auto()
    REAPPLIED_STAFF_LINES_UNCOLOR = enum.auto()

    REDUNDANT_STAFF_LINES = enum.auto()
    REDUNDANT_STAFF_LINES_COLOR = enum.auto()
    REDUNDANT_STAFF_LINES_COLOR_REDRAW = enum.auto()
    REDUNDANT_STAFF_LINES_UNCOLOR = enum.auto()

    ### TIME SIGNATURES ###

    EXPLICIT_TIME_SIGNATURE = enum.auto()
    EXPLICIT_TIME_SIGNATURE_COLOR = enum.auto()
    EXPLICIT_TIME_SIGNATURE_COLOR_REDRAW = enum.auto()
    EXPLICIT_TIME_SIGNATURE_UNCOLOR = enum.auto()

    REAPPLIED_TIME_SIGNATURE = enum.auto()
    REAPPLIED_TIME_SIGNATURE_COLOR = enum.auto()
    REAPPLIED_TIME_SIGNATURE_COLOR_REDRAW = enum.auto()
    REAPPLIED_TIME_SIGNATURE_UNCOLOR = enum.auto()

    REDUNDANT_TIME_SIGNATURE = enum.auto()
    REDUNDANT_TIME_SIGNATURE_COLOR = enum.auto()
    REDUNDANT_TIME_SIGNATURE_COLOR_REDRAW = enum.auto()
    REDUNDANT_TIME_SIGNATURE_UNCOLOR = enum.auto()

    ### OTHER ###

    CLOCK_TIME_MARKUP = enum.auto()
    EMPTY_START_BAR = enum.auto()
    FERMATA_BAR_LINE = enum.auto()
    FIGURE_NAME_MARKUP = enum.auto()
    SPACING = enum.auto()
    SPACING_MARKUP = enum.auto()
    STAGE_NUMBER_MARKUP = enum.auto()

    ### PUBLIC METHODS ###

    @staticmethod
    def build(tag, build=None):
        r'''Tags `tag` with `build` name or with SEGMENT.

        Returns string.
        '''
        if build is not None:
            return f'BUILD:{build.upper()}:{tag.name}'
        return f'SEGMENT:{tag.name}'
