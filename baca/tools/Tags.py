import abjad


class Tags(abjad.Tags):
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

    _my_known_tags:tuple = (

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
        'DEFAULT_INSTRUMENT_COLOR',
        'REDRAWN_DEFAULT_INSTRUMENT',
        'REDRAWN_DEFAULT_INSTRUMENT_COLOR',

        'EXPLICIT_INSTRUMENT',
        'EXPLICIT_INSTRUMENT_ALERT',
        'EXPLICIT_INSTRUMENT_COLOR',
        'REDRAWN_EXPLICIT_INSTRUMENT',
        'REDRAWN_EXPLICIT_INSTRUMENT_COLOR',

        'REAPPLIED_INSTRUMENT',
        'REAPPLIED_INSTRUMENT_ALERT',
        'REAPPLIED_INSTRUMENT_COLOR',
        'REDRAWN_REAPPLIED_INSTRUMENT',
        'REDRAWN_REAPPLIED_INSTRUMENT_COLOR',

        'REDUNDANT_INSTRUMENT',
        'REDUNDANT_INSTRUMENT_ALERT',
        'REDUNDANT_INSTRUMENT_COLOR',
        'REDRAWN_REDUNDANT_INSTRUMENT',
        'REDRAWN_REDUNDANT_INSTRUMENT_COLOR',

        ### MARGIN MARKUP ###

        'DEFAULT_MARGIN_MARKUP',
        'DEFAULT_MARGIN_MARKUP_ALERT',
        'DEFAULT_MARGIN_MARKUP_COLOR',
        'REDRAWN_DEFAULT_MARGIN_MARKUP',
        'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR',

        'EXPLICIT_MARGIN_MARKUP',
        'EXPLICIT_MARGIN_MARKUP_ALERT',
        'EXPLICIT_MARGIN_MARKUP_COLOR',
        'REDRAWN_EXPLICIT_MARGIN_MARKUP',
        'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR',

        'REAPPLIED_MARGIN_MARKUP',
        'REAPPLIED_MARGIN_MARKUP_ALERT',
        'REAPPLIED_MARGIN_MARKUP_COLOR',
        'REDRAWN_REAPPLIED_MARGIN_MARKUP',
        'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR',

        'REDUNDANT_MARGIN_MARKUP',
        'REDUNDANT_MARGIN_MARKUP_ALERT',
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
        if tag in abjad.Tags._known_tags:
            raise Exception(f'tag already exists in abjad.Tags: {tag!r}.')

    _known_tags:tuple = abjad.Tags._known_tags + _my_known_tags

    ### PUBLIC PROPERTIES ###

    @staticmethod
    def all_broken_spanner_tags():
        r'''Gets all broken spanner tags.

        ..  container:: example

            >>> dictionary = baca.tags.all_broken_spanner_tags()
            >>> for tag in dictionary['activate']:
            ...     tag
            ...
            'LEFT_BROKEN_REPEAT_TIE'
            'RIGHT_BROKEN_TIE'

            >>> for tag in dictionary['deactivate']:
            ...     tag
            ...
            'LEFT_BROKEN_TRILL'
            'RIGHT_BROKEN_TRILL'

        '''
        import baca
        return {
            'activate': [
                baca.tags.LEFT_BROKEN_REPEAT_TIE,
                baca.tags.RIGHT_BROKEN_TIE,
                ],
            'deactivate': [
                baca.tags.LEFT_BROKEN_TRILL,
                baca.tags.RIGHT_BROKEN_TRILL,
                ],
            }

    @staticmethod
    def all_persistence_labels():
        r'''Gets all persistence labels.

        ..  container:: example

            >>> for string in baca.tags.all_persistence_labels():
            ...     string
            ...
            'DEFAULT_CLEF'
            'EXPLICIT_CLEF'
            'REAPPLIED_CLEF'
            'REDUNDANT_CLEF'
            'EXPLICIT_DYNAMIC'
            'REAPPLIED_DYNAMIC'
            'REDUNDANT_DYNAMIC'
            'DEFAULT_INSTRUMENT'
            'EXPLICIT_INSTRUMENT'
            'REAPPLIED_INSTRUMENT'
            'REDUNDANT_INSTRUMENT'
            'DEFAULT_MARGIN_MARKUP'
            'EXPLICIT_MARGIN_MARKUP'
            'REAPPLIED_MARGIN_MARKUP'
            'REDUNDANT_MARGIN_MARKUP'
            'EXPLICIT_METRONOME_MARK'
            'REAPPLIED_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'
            'EXPLICIT_STAFF_LINES'
            'REAPPLIED_STAFF_LINES'
            'REDUNDANT_STAFF_LINES'
            'EXPLICIT_TIME_SIGNATURE'
            'REAPPLIED_TIME_SIGNATURE'
            'REDUNDANT_TIME_SIGNATURE'

        Returns list.
        '''
        import baca
        return [
            baca.tags.DEFAULT_CLEF,
            baca.tags.EXPLICIT_CLEF,
            baca.tags.REAPPLIED_CLEF,
            baca.tags.REDUNDANT_CLEF,
            #
            baca.tags.EXPLICIT_DYNAMIC,
            baca.tags.REAPPLIED_DYNAMIC,
            baca.tags.REDUNDANT_DYNAMIC,
            #
            baca.tags.DEFAULT_INSTRUMENT,
            baca.tags.EXPLICIT_INSTRUMENT,
            baca.tags.REAPPLIED_INSTRUMENT,
            baca.tags.REDUNDANT_INSTRUMENT,
            #
            baca.tags.DEFAULT_MARGIN_MARKUP,
            baca.tags.EXPLICIT_MARGIN_MARKUP,
            baca.tags.REAPPLIED_MARGIN_MARKUP,
            baca.tags.REDUNDANT_MARGIN_MARKUP,
            #
            baca.tags.EXPLICIT_METRONOME_MARK,
            baca.tags.REAPPLIED_METRONOME_MARK,
            baca.tags.REDUNDANT_METRONOME_MARK,
            #
            baca.tags.EXPLICIT_STAFF_LINES,
            baca.tags.REAPPLIED_STAFF_LINES,
            baca.tags.REDUNDANT_STAFF_LINES,
            #
            baca.tags.EXPLICIT_TIME_SIGNATURE,
            baca.tags.REAPPLIED_TIME_SIGNATURE,
            baca.tags.REDUNDANT_TIME_SIGNATURE,
            #
            ]

    @staticmethod
    def all_persistent_indicator_color_tags(path=None):
        r'''Gets all persistent indicator color tags.

        ..  container:: example

            >>> dictionary = baca.tags.all_persistent_indicator_color_tags()
            >>> for tag in dictionary['activate']:
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
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

            >>> for tag in dictionary['deactivate']:
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        ..  container:: example

            Additional REAPPLIED_CLEF tag when path is not none and is in a
            build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> dictionary = baca.tags.all_persistent_indicator_color_tags(path)
            >>> for tag in dictionary['activate']:
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
            'REAPPLIED_CLEF'
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE'

            >>> for tag in dictionary['deactivate']:
            ...     tag
            ...
            'REAPPLIED_INSTRUMENT'
            'EXPLICIT_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        Returns two-part dictionary.
        '''
        import baca
        activate = []
        activate.extend(baca.tags.clef_color_tags(path))
        activate.extend(baca.tags.dynamic_color_tags())
        activate.extend(baca.tags.instrument_color_tags())
        activate.extend(baca.tags.margin_markup_color_tags())
        activate.extend(baca.tags.metronome_mark_color_tags()['activate'])
        activate.extend(baca.tags.staff_lines_color_tags())
        activate.extend(baca.tags.time_signature_color_tags())
        # TODO: if path is not None and not path.is_segment()
        if path is not None and path.build is not None:
            activate.append(baca.tags.REAPPLIED_TIME_SIGNATURE)
        deactivate = []
        ## TODO: if path is not None and not path.is_segment()
        if path is not None and path.build is not None:
            deactivate.append(baca.tags.REAPPLIED_INSTRUMENT)
        deactivate.extend(baca.tags.metronome_mark_color_tags()['deactivate'])
        return {
            'activate': activate,
            'deactivate': deactivate,
            }

    @staticmethod
    def clef_color_match(tags):
        r'''Matches clef color tags.

        Returns true or false.
        '''
        return set(tags) & set(Tags.clef_color_tags())

    @staticmethod
    def clef_color_tags(path=None):
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

        ..  container:: example

            If `path` is not none and is in a build directory, output includes
            the extra REAPPLIED_CLEF tag:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in baca.tags.clef_color_tags(path=path):
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
            'REAPPLIED_CLEF'

        Returns list.
        '''
        import baca
        tags = [
            baca.tags.DEFAULT_CLEF_COLOR,
            baca.tags.DEFAULT_CLEF_REDRAW_COLOR,
            baca.tags.EXPLICIT_CLEF_COLOR,
            baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
            baca.tags.REAPPLIED_CLEF_COLOR,
            baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
            baca.tags.REDUNDANT_CLEF_COLOR,
            baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
            ]
        ## TODO: if path is not None and not path.is_segment()
        if path is not None and path.build is not None:
            tags.append(baca.tags.REAPPLIED_CLEF)
        return tags

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
        import baca
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
    def has_persistence_label(string):
        r'''Is true when ``string`` has persistence label.

        ..  container:: example

            >>> baca.tags.has_persistence_label('')
            False

            >>> baca.tags.has_persistence_label('FOO')
            False

            >>> baca.tags.has_persistence_label('FOO:DEFAULT_CLEF')
            True

            >>> baca.tags.has_persistence_label('DEFAULT_CLEF')
            True

        Returns true or false.
        '''
        if not isinstance(string, str):
            return False
        all_persistence_labels = Tags.all_persistence_labels()
        words = string.split(':')
        for word in words:
            if word in all_persistence_labels:
                return True
        return False

    @staticmethod
    def instrument_color_tags():
        r'''Gets instrument color tags.

        ..  container:: example

            >>> for tag in baca.tags.instrument_color_tags():
            ...     tag
            ...
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'

        Returns list of strings.
        '''
        import baca
        return [
            baca.tags.DEFAULT_INSTRUMENT_ALERT,
            baca.tags.DEFAULT_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_DEFAULT_INSTRUMENT_COLOR,
            baca.tags.EXPLICIT_INSTRUMENT_ALERT,
            baca.tags.EXPLICIT_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
            baca.tags.REAPPLIED_INSTRUMENT_ALERT,
            baca.tags.REAPPLIED_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
            baca.tags.REDUNDANT_INSTRUMENT_ALERT,
            baca.tags.REDUNDANT_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
            ]

    @staticmethod
    def margin_markup_color_expression_match(tags):
        r'''Matches margin markup color expression tags.

        Returns true or false.
        '''
        tags_ = Tags.margin_markup_color_tags()
        return bool(set(tags) & set(tags_))

    @staticmethod
    def margin_markup_color_suppression_match(tags):
        r'''Matches margin markup color suppression tags.

        Returns true or false.
        '''
        tags_ = Tags.margin_markup_color_tags()
        return bool(set(tags) & set(tags_))

    @staticmethod
    def margin_markup_color_tags():
        r'''Gets margin markup color tags.

        ..  container:: example

            >>> for tag in baca.tags.margin_markup_color_tags():
            ...     tag
            ...
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'

        Returns list.
        '''
        import baca
        return [
            baca.tags.DEFAULT_MARGIN_MARKUP_ALERT,
            baca.tags.DEFAULT_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR,
            baca.tags.EXPLICIT_MARGIN_MARKUP_ALERT,
            baca.tags.EXPLICIT_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR,
            baca.tags.REAPPLIED_MARGIN_MARKUP_ALERT,
            baca.tags.REAPPLIED_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR,
            baca.tags.REDUNDANT_MARGIN_MARKUP_ALERT,
            baca.tags.REDUNDANT_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR,
            ]

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
            'REDUNDANT_METRONOME_MARK'

        Note that baca.tags.REAPPLIED_METRONOME_MARK is completely ignored.

        Returns two-part dictionary.
        '''
        import baca
        return {
            'activate': [
                baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
                baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
                baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
                ],
            'deactivate': [
                baca.tags.EXPLICIT_METRONOME_MARK,
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
        import baca
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
        import baca
        return [
            baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
            baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
            baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
            ]
