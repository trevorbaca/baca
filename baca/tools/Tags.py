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

    DEFAULT_CLEF = enum.auto()
    DEFAULT_CLEF_COLOR = enum.auto()
    DEFAULT_CLEF_COLOR_CANCELLATION = enum.auto()
    DEFAULT_CLEF_REDRAW_COLOR = enum.auto()

    EXPLICIT_CLEF = enum.auto()
    EXPLICIT_CLEF_COLOR = enum.auto()
    EXPLICIT_CLEF_COLOR_CANCELLATION = enum.auto()
    EXPLICIT_CLEF_REDRAW_COLOR = enum.auto()

    REAPPLIED_CLEF = enum.auto()
    REAPPLIED_CLEF_COLOR = enum.auto() 
    REAPPLIED_CLEF_COLOR_CANCELLATION = enum.auto()
    REAPPLIED_CLEF_REDRAW_COLOR = enum.auto()

    REDUNDANT_CLEF = enum.auto()
    REDUNDANT_CLEF_COLOR = enum.auto()
    REDUNDANT_CLEF_COLOR_CANCELLATION = enum.auto()
    REDUNDANT_CLEF_REDRAW_COLOR = enum.auto()

    ### DYNAMICS ###

    EXPLICIT_DYNAMIC = enum.auto()
    EXPLICIT_DYNAMIC_COLOR = enum.auto()
    EXPLICIT_DYNAMIC_COLOR_CANCELLATION = enum.auto()
    EXPLICIT_DYNAMIC_REDRAW_COLOR = enum.auto()

    REAPPLIED_DYNAMIC = enum.auto()
    REAPPLIED_DYNAMIC_COLOR = enum.auto() 
    REAPPLIED_DYNAMIC_COLOR_CANCELLATION = enum.auto()
    REAPPLIED_DYNAMIC_REDRAW_COLOR = enum.auto()

    REDUNDANT_DYNAMIC = enum.auto()
    REDUNDANT_DYNAMIC_COLOR = enum.auto()
    REDUNDANT_DYNAMIC_COLOR_CANCELLATION = enum.auto()
    REDUNDANT_DYNAMIC_REDRAW_COLOR = enum.auto()

    ### INSTRUMENTS ###

    DEFAULT_INSTRUMENT = enum.auto()
    DEFAULT_INSTRUMENT_ALERT = enum.auto()
    DEFAULT_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    DEFAULT_INSTRUMENT_COLOR = enum.auto()
    REDRAWN_DEFAULT_INSTRUMENT = enum.auto()
    REDRAWN_DEFAULT_INSTRUMENT_COLOR = enum.auto()

    EXPLICIT_INSTRUMENT = enum.auto()
    EXPLICIT_INSTRUMENT_ALERT = enum.auto()
    EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    EXPLICIT_INSTRUMENT_COLOR = enum.auto()
    REDRAWN_EXPLICIT_INSTRUMENT = enum.auto()
    REDRAWN_EXPLICIT_INSTRUMENT_COLOR = enum.auto()

    REAPPLIED_INSTRUMENT = enum.auto()
    REAPPLIED_INSTRUMENT_ALERT = enum.auto()
    REAPPLIED_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    REAPPLIED_INSTRUMENT_COLOR = enum.auto() 
    REDRAWN_REAPPLIED_INSTRUMENT = enum.auto()
    REDRAWN_REAPPLIED_INSTRUMENT_COLOR = enum.auto()

    REDUNDANT_INSTRUMENT = enum.auto()
    REDUNDANT_INSTRUMENT_ALERT = enum.auto()
    REDUNDANT_INSTRUMENT_ALERT_WITH_COLOR = enum.auto()
    REDUNDANT_INSTRUMENT_COLOR = enum.auto()
    REDRAWN_REDUNDANT_INSTRUMENT = enum.auto()
    REDRAWN_REDUNDANT_INSTRUMENT_COLOR = enum.auto()

    ### MARGIN MARKUP ###

    DEFAULT_MARGIN_MARKUP = enum.auto()
    DEFAULT_MARGIN_MARKUP_ALERT = enum.auto()
    DEFAULT_MARGIN_MARKUP_ALERT_WITH_COLOR = enum.auto()
    DEFAULT_MARGIN_MARKUP_COLOR = enum.auto()
    REDRAWN_DEFAULT_MARGIN_MARKUP = enum.auto()
    REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR = enum.auto()

    EXPLICIT_MARGIN_MARKUP = enum.auto()
    EXPLICIT_MARGIN_MARKUP_ALERT = enum.auto()
    EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR = enum.auto()
    EXPLICIT_MARGIN_MARKUP_COLOR = enum.auto()
    REDRAWN_EXPLICIT_MARGIN_MARKUP = enum.auto()
    REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR = enum.auto()

    REAPPLIED_MARGIN_MARKUP = enum.auto()
    REAPPLIED_MARGIN_MARKUP_ALERT = enum.auto()
    REAPPLIED_MARGIN_MARKUP_ALERT_WITH_COLOR = enum.auto()
    REAPPLIED_MARGIN_MARKUP_COLOR = enum.auto() 
    REDRAWN_REAPPLIED_MARGIN_MARKUP = enum.auto()
    REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR = enum.auto()

    REDUNDANT_MARGIN_MARKUP = enum.auto()
    REDUNDANT_MARGIN_MARKUP_ALERT = enum.auto()
    REDUNDANT_MARGIN_MARKUP_ALERT_WITH_COLOR = enum.auto()
    REDUNDANT_MARGIN_MARKUP_COLOR = enum.auto()
    REDRAWN_REDUNDANT_MARGIN_MARKUP = enum.auto()
    REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR = enum.auto()

    ### METRONOME MARKS ###

    EXPLICIT_METRONOME_MARK = enum.auto()
    EXPLICIT_METRONOME_MARK_WITH_COLOR = enum.auto()

    REAPPLIED_METRONOME_MARK = enum.auto()
    REAPPLIED_METRONOME_MARK_WITH_COLOR = enum.auto() 

    REDUNDANT_METRONOME_MARK = enum.auto()
    REDUNDANT_METRONOME_MARK_WITH_COLOR = enum.auto()

    ### SPACING SECTION ###

    EXPLICIT_SPACING_SECTION = enum.auto()
    EXPLICIT_SPACING_SECTION_COLOR = enum.auto()

    REAPPLIED_SPACING_SECTION = enum.auto()
    REAPPLIED_SPACING_SECTION_COLOR = enum.auto() 

    REDUNDANT_SPACING_SECTION = enum.auto()
    REDUNDANT_SPACING_SECTION_COLOR = enum.auto()

    ### STAFF LINES ###

    EXPLICIT_STAFF_LINES = enum.auto()
    EXPLICIT_STAFF_LINES_COLOR = enum.auto()

    REAPPLIED_STAFF_LINES = enum.auto()
    REAPPLIED_STAFF_LINES_COLOR = enum.auto() 

    REDUNDANT_STAFF_LINES = enum.auto()
    REDUNDANT_STAFF_LINES_COLOR = enum.auto()

    ### TIME SIGNATURES ###

    EXPLICIT_TIME_SIGNATURE = enum.auto()
    EXPLICIT_TIME_SIGNATURE_COLOR = enum.auto()

    REAPPLIED_TIME_SIGNATURE = enum.auto()
    REAPPLIED_TIME_SIGNATURE_COLOR = enum.auto()

    REDUNDANT_TIME_SIGNATURE = enum.auto()
    REDUNDANT_TIME_SIGNATURE_COLOR = enum.auto()

    ### PUBLIC METHODS ###

    @staticmethod
    def build(tag, build=None):
        r'''Tags `tag` with `build` name or ``'SEGMENT'``..

        Returns string.
        '''
        if build is not None:
            words = abjad.String(build).delimit_words()
            build = '_'.join(words)
            build = build.upper()
            return f'{build}_{tag.name}'
        else:
            return f'SEGMENT_{tag.name}'
