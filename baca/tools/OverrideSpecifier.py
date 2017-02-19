# -*- coding: utf-8 -*-
import abjad


class OverrideSpecifier(abjad.abctools.AbjadObject):
    r'''Override specifier.
    
    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With figure-maker:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.OverrideSpecifier(
            ...         grob_name='beam',
            ...         attribute_name='positions',
            ...         attribute_value='(-6, -6)',
            ...         ),
            ...     baca.tools.OverrideSpecifier(
            ...         grob_name='stem',
            ...         attribute_name='direction',
            ...         attribute_value=Down,
            ...         ),
            ...     )

        ::

            >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker('Voice 1', segments)
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            c'16 [
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            d'16
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            bf'16 ]
                        }
                        {
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            fs''16 [
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            e''16
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            ef''16
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            af''16
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            g''16 ]
                        }
                        {
                            \once \override Beam.positions = #'(-6 . -6)
                            \once \override Stem.direction = #down
                            a'16
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     baca.make_even_run_rhythm_specifier(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.tools.OverrideSpecifier(
            ...         grob_name='beam',
            ...         attribute_name='positions',
            ...         attribute_value='(-6, -6)',
            ...         ),
            ...     baca.tools.OverrideSpecifier(
            ...         grob_name='stem',
            ...         attribute_name='direction',
            ...         attribute_value=Down,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                e'8 [
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                d''8
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                f'8
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                e''8 ]
                            }
                            {
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                g'8 [
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                f''8
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                e'8 ]
                            }
                            {
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                d''8 [
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                f'8
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                e''8
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                g'8 ]
                            }
                            {
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                f''8 [
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                e'8
                                \once \override Beam.positions = #'(-6 . -6)
                                \once \override Stem.direction = #down
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        ::

            >>> baca.tools.OverrideSpecifier()
            OverrideSpecifier()

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_attribute_name',
        '_attribute_value',
        '_context_name',
        '_grob_name',
        '_maximum_settings',
        '_maximum_written_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        context_name=None,
        grob_name=None, 
        attribute_name=None,
        attribute_value=None,
        maximum_written_duration=None,
        maximum_settings=None,
        ):
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
        if grob_name is not None:
            assert isinstance(grob_name, str), repr(grob_name)
        self._grob_name = grob_name
        if attribute_name is not None:
            assert isinstance(attribute_name, str), repr(attribute_name)
        self._attribute_name = attribute_name
        self._attribute_value = attribute_value
        if maximum_written_duration is not None:
            maximum_written_duration = abjad.durationtools.Duration(
                maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if maximum_settings is not None:
            assert isinstance(maximum_settings, dict), maximum_settings
        self._maximum_settings = maximum_settings

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls specifier.

        Returns none.
        '''
        statement = 'abjad.override(leaf)'
        if self.context_name is not None:
            statement += '.{context_name}'
        statement += '.{grob_name}.{attribute_name} = {attribute_value}'
        if self.maximum_written_duration is not None:
            context_name = self.maximum_settings['context_name']
            grob_name = self.maximum_settings['grob_name']
            attribute_name = self.maximum_settings['attribute_name']
            attribute_value = self.maximum_settings['attribute_value']
        else:
            context_name = self.context_name
            grob_name = self.grob_name
            attribute_name = self.attribute_name
            attribute_value = self.attribute_value
        statement = statement.format(
            context_name=context_name,
            grob_name=grob_name,
            attribute_name=attribute_name,
            attribute_value=attribute_value,
            )
        for leaf in abjad.iterate(argument).by_leaf():
            if  (self.maximum_written_duration is None or
                (self.maximum_written_duration is not None and
                self.maximum_written_duration <= leaf.written_duration)):
                exec(statement, globals(), locals())

    ### PUBLIC PROPERTIES ###

    @property
    def attribute_name(self):
        r'''Gets attribute name.

        Set to string or none.
        '''
        return self._attribute_name

    @property
    def attribute_value(self):
        r'''Gets attribute value.

        Set to string or none.
        '''
        return self._attribute_value

    @property
    def context_name(self):
        r'''Gets context name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._context_name

    @property
    def grob_name(self):
        r'''Gets grob name.

        Set to string or none.
        '''
        return self._grob_name

    # TODO: replace with explicit inequality
    @property
    def maximum_settings(self):
        r'''Gets maximum settings for leaves with written duration
        greater than or equal to maximum written duration of specifier.

        ..  note:: Write examples and tests.

        Set to dictionary or none.
        '''
        return self._maximum_settings

    # TODO: replace with explicit inequality
    @property
    def maximum_written_duration(self):
        r'''Gets maximum written duration.

        Written durations equal to or greater than this will
        not be handled.

        Set to duration or none.
        '''
        return self._maximum_written_duration
