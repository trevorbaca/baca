import baca
from abjad.tools.segmenttools.Tags import Tags


class Tags(Tags):
    r'''Tags.

    ..  container:: example

        >>> baca.tags
        Tags()

    ..  container::

        All attributes return strings:

        >>> baca.tags.EXPLICIT_CLEF
        'EXPLICIT_CLEF'

        >>> baca.tags.REDUNDANT_CLEF
        'REDUNDANT_CLEF'

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        )

    _my_known_tags = (

        ### CLEFS ###

        'DEFAULT_CLEF',
        'DEFAULT_CLEF_COLOR',
        'DEFAULT_CLEF_COLOR_CANCELLATION',
        'DEFAULT_CLEF_REDRAW_COLOR',

        'EXPLICIT_CLEF',
        'EXPLICIT_CLEF_COLOR',
        'EXPLICIT_CLEF_COLOR_CANCELLATION',
        'EXPLICIT_CLEF_REDRAW_COLOR',

        'REAPPLIED_CLEF',
        'REAPPLIED_CLEF_COLOR',
        'REAPPLIED_CLEF_COLOR_CANCELLATION',
        'REAPPLIED_CLEF_REDRAW_COLOR',

        'REDUNDANT_CLEF',
        'REDUNDANT_CLEF_COLOR',
        'REDUNDANT_CLEF_COLOR_CANCELLATION',
        'REDUNDANT_CLEF_REDRAW_COLOR',

        ### DYNAMICS ###

        'EXPLICIT_DYNAMIC',
        'EXPLICIT_DYNAMIC_COLOR',
        'EXPLICIT_DYNAMIC_COLOR_CANCELLATION',
        'EXPLICIT_DYNAMIC_REDRAW_COLOR',

        'REAPPLIED_DYNAMIC',
        'REAPPLIED_DYNAMIC_COLOR',
        'REAPPLIED_DYNAMIC_COLOR_CANCELLATION',
        'REAPPLIED_DYNAMIC_REDRAW_COLOR',

        'REDUNDANT_DYNAMIC',
        'REDUNDANT_DYNAMIC_COLOR',
        'REDUNDANT_DYNAMIC_COLOR_CANCELLATION',
        'REDUNDANT_DYNAMIC_REDRAW_COLOR',

        ### INSTRUMENTS ###

        'DEFAULT_INSTRUMENT',
        'DEFAULT_INSTRUMENT_ALERT',
        'DEFAULT_INSTRUMENT_ALERT_WITH_COLOR',
        'DEFAULT_INSTRUMENT_COLOR',
        'REDRAWN_DEFAULT_INSTRUMENT',
        'REDRAWN_DEFAULT_INSTRUMENT_COLOR',

        'EXPLICIT_INSTRUMENT',
        'EXPLICIT_INSTRUMENT_ALERT',
        'EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR',
        'EXPLICIT_INSTRUMENT_COLOR',
        'REDRAWN_EXPLICIT_INSTRUMENT',
        'REDRAWN_EXPLICIT_INSTRUMENT_COLOR',

        'REAPPLIED_INSTRUMENT',
        'REAPPLIED_INSTRUMENT_ALERT',
        'REAPPLIED_INSTRUMENT_ALERT_WITH_COLOR',
        'REAPPLIED_INSTRUMENT_COLOR',
        'REDRAWN_REAPPLIED_INSTRUMENT',
        'REDRAWN_REAPPLIED_INSTRUMENT_COLOR',

        'REDUNDANT_INSTRUMENT',
        'REDUNDANT_INSTRUMENT_ALERT',
        'REDUNDANT_INSTRUMENT_ALERT_WITH_COLOR',
        'REDUNDANT_INSTRUMENT_COLOR',
        'REDRAWN_REDUNDANT_INSTRUMENT',
        'REDRAWN_REDUNDANT_INSTRUMENT_COLOR',

        ### MARGIN MARKUP ###

        'DEFAULT_MARGIN_MARKUP',
        'DEFAULT_MARGIN_MARKUP_ALERT',
        'DEFAULT_MARGIN_MARKUP_ALERT_WITH_COLOR',
        'DEFAULT_MARGIN_MARKUP_COLOR',
        'REDRAWN_DEFAULT_MARGIN_MARKUP',
        'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR',

        'EXPLICIT_MARGIN_MARKUP',
        'EXPLICIT_MARGIN_MARKUP_ALERT',
        'EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR',
        'EXPLICIT_MARGIN_MARKUP_COLOR',
        'REDRAWN_EXPLICIT_MARGIN_MARKUP',
        'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR',

        'REAPPLIED_MARGIN_MARKUP',
        'REAPPLIED_MARGIN_MARKUP_ALERT',
        'REAPPLIED_MARGIN_MARKUP_ALERT_WITH_COLOR',
        'REAPPLIED_MARGIN_MARKUP_COLOR',
        'REDRAWN_REAPPLIED_MARGIN_MARKUP',
        'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR',

        'REDUNDANT_MARGIN_MARKUP',
        'REDUNDANT_MARGIN_MARKUP_ALERT',
        'REDUNDANT_MARGIN_MARKUP_ALERT_WITH_COLOR',
        'REDUNDANT_MARGIN_MARKUP_COLOR',
        'REDRAWN_REDUNDANT_MARGIN_MARKUP',
        'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR',

        ### METRONOME MARKS ###

        'EXPLICIT_METRONOME_MARK',
        'EXPLICIT_METRONOME_MARK_WITH_COLOR',

        'REAPPLIED_METRONOME_MARK',
        'REAPPLIED_METRONOME_MARK_WITH_COLOR',

        'REDUNDANT_METRONOME_MARK',
        'REDUNDANT_METRONOME_MARK_WITH_COLOR',

        ### SPACING SECTION ###

        'EXPLICIT_SPACING_SECTION',
        'EXPLICIT_SPACING_SECTION_COLOR',

        'REAPPLIED_SPACING_SECTION',
        'REAPPLIED_SPACING_SECTION_COLOR',

        'REDUNDANT_SPACING_SECTION',
        'REDUNDANT_SPACING_SECTION_COLOR',

        ### STAFF LINES ###

        'EXPLICIT_STAFF_LINES',
        'EXPLICIT_STAFF_LINES_COLOR',

        'REAPPLIED_STAFF_LINES',
        'REAPPLIED_STAFF_LINES_COLOR',

        'REDUNDANT_STAFF_LINES',
        'REDUNDANT_STAFF_LINES_COLOR',

        ### TIME SIGNATURES ###

        'EXPLICIT_TIME_SIGNATURE',
        'EXPLICIT_TIME_SIGNATURE_COLOR',

        'REAPPLIED_TIME_SIGNATURE',
        'REAPPLIED_TIME_SIGNATURE_COLOR',

        'REDUNDANT_TIME_SIGNATURE',
        'REDUNDANT_TIME_SIGNATURE_COLOR',

        )

    for tag in _my_known_tags:
        if tag in Tags._known_tags:
            raise Exception(f'tag already exists in abjad.Tags: {tag!r}.')

    _known_tags = Tags._known_tags + _my_known_tags

    ### PUBLIC PROPERTIES ###

    @staticmethod
    def clef_color_match(tags):
        r'''Matches clef color tags.

        Returns true or false.
        '''
        return set(tags) & set(Tags.clef_color_tags())

    @staticmethod
    def clef_color_tags():
        r'''Gets clef color tags.

        ..  container:: example

            >>> for tag in baca.tags.clef_color_tags():
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'

        Returns list.
        '''
        return [
            baca.tags.DEFAULT_CLEF_COLOR,
            baca.tags.DEFAULT_CLEF_REDRAW_COLOR,
            baca.tags.EXPLICIT_CLEF_COLOR,
            baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
            baca.tags.REAPPLIED_CLEF_COLOR,
            baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
            baca.tags.REDUNDANT_CLEF_COLOR,
            baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
            ]

    @staticmethod
    def dynamic_color_match(tags):
        r'''Matches dynamic color tags.

        Returns true or false.
        '''
        return set(tags) & set(Tags.dynamic_color_tags())

    @staticmethod
    def dynamic_color_tags():
        r'''Gets dynamic color tags.

        ..  container:: example

            >>> for tag in baca.tags.dynamic_color_tags():
            ...     tag
            ...
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'

        Returns list.
        '''
        return [
            baca.tags.EXPLICIT_DYNAMIC_COLOR,
            baca.tags.EXPLICIT_DYNAMIC_REDRAW_COLOR,
            baca.tags.REAPPLIED_DYNAMIC,
            baca.tags.REAPPLIED_DYNAMIC_COLOR,
            baca.tags.REAPPLIED_DYNAMIC_REDRAW_COLOR,
            baca.tags.REDUNDANT_DYNAMIC_COLOR,
            baca.tags.REDUNDANT_DYNAMIC_REDRAW_COLOR,
            ]

    @staticmethod
    def margin_markup_color_expression_match(tags):
        r'''Matches margin markup color expression tags.

        Returns true or false.
        '''
        tags_ = Tags.margin_markup_color_tags()['activate']
        return bool(set(tags) & set(tags_))

    @staticmethod
    def margin_markup_color_suppression_match(tags):
        r'''Matches margin markup color suppression tags.

        Returns true or false.
        '''
        tags_ = Tags.margin_markup_color_tags()['deactivate']
        return bool(set(tags) & set(tags_))

    @staticmethod
    def margin_markup_color_tags():
        r'''Gets margin markup color tags.

        ..  container:: example

            >>> dictionary = baca.tags.margin_markup_color_tags()
            >>> for tag in dictionary['activate']:
            ...     tag
            ...
            'DEFAULT_MARGIN_MARKUP_ALERT_WITH_COLOR'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT_WITH_COLOR'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT_WITH_COLOR'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'

            >>> for tag in dictionary['deactivate']:
            ...     tag
            ...

        Returns two-part dictionary.
        '''
        return {
            'activate': [
                baca.tags.DEFAULT_MARGIN_MARKUP_ALERT_WITH_COLOR,
                baca.tags.DEFAULT_MARGIN_MARKUP_COLOR,
                baca.tags.REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR,
                baca.tags.EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR,
                baca.tags.EXPLICIT_MARGIN_MARKUP_COLOR,
                baca.tags.REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR,
                baca.tags.REAPPLIED_MARGIN_MARKUP_ALERT_WITH_COLOR,
                baca.tags.REAPPLIED_MARGIN_MARKUP_COLOR,
                baca.tags.REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR,
                baca.tags.REDUNDANT_MARGIN_MARKUP_ALERT_WITH_COLOR,
                baca.tags.REDUNDANT_MARGIN_MARKUP_COLOR,
                baca.tags.REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR,
                ],
            'deactivate': [
                ],
            }

    @staticmethod
    def metronome_mark_color_expression_match(tags):
        r'''Matches tags that should activate for colored metronome marks.

        Returns true or false.
        '''
        tags_ = Tags.metronome_mark_color_tags()['activate']
        return bool(set(tags) & set(tags_))

    @staticmethod
    def metronome_mark_color_suppression_match(tags):
        r'''Matches tags that should deactivate for colored metronome marks.

        Returns true or false.
        '''
        tags_ = Tags.metronome_mark_color_tags()['deactivate']
        return bool(set(tags) & set(tags_))

    @staticmethod
    def metronome_mark_color_tags():
        r'''Gets metronome mark color tags.

        ..  container:: example

            >>> dictionary = baca.tags.metronome_mark_color_tags()
            >>> for tag in dictionary['activate']:
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'

            >>> for tag in dictionary['deactivate']:
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK'
            'REAPPLIED_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        Returns two-part dictionary.
        '''
        return {
            'activate': [
                baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
                baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
                baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
                ],
            'deactivate': [
                baca.tags.EXPLICIT_METRONOME_MARK,
                baca.tags.REAPPLIED_METRONOME_MARK,
                baca.tags.REDUNDANT_METRONOME_MARK,
                ],
            }

    @staticmethod
    def staff_lines_color_match(tags):
        r'''Matches staff lines color tags.

        Returns true or false.
        '''
        return set(tags) & set(Tags.staff_lines_color_tags())

    @staticmethod
    def staff_lines_color_tags():
        r'''Gets staff lines color tags.

        ..  container:: example

            >>> for tag in baca.tags.staff_lines_color_tags():
            ...     tag
            ...
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'

        Returns list of strings.
        '''
        return [
            baca.tags.EXPLICIT_STAFF_LINES_COLOR,
            baca.tags.REAPPLIED_STAFF_LINES_COLOR,
            baca.tags.REDUNDANT_STAFF_LINES_COLOR,
            ]

    @staticmethod
    def time_signature_color_match(tags):
        r'''Matches time signature color tags.

        Returns true or false.
        '''
        return set(tags) & set(Tags.time_signature_color_tags())

    @staticmethod
    def time_signature_color_tags():
        r'''Gets time signature color tags.

        ..  container:: example

            >>> for tag in baca.tags.time_signature_color_tags():
            ...     tag
            ...
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

        Returns list.
        '''
        return [
            baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
            baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
            baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
            ]
