import abjad
import baca


class OverrideCommand(abjad.AbjadObject):
    r'''Override command.
    ::

        >>> import baca

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.OverrideCommand(
            ...         grob_name='beam',
            ...         attribute_name='positions',
            ...         attribute_value='(-6, -6)',
            ...         ),
            ...     baca.OverrideCommand(
            ...         grob_name='stem',
            ...         attribute_name='direction',
            ...         attribute_value=abjad.Down,
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.OverrideCommand(
            ...         attribute_name='positions',
            ...         attribute_value=(-6, -6),
            ...         grob_name='beam',
            ...         revert=True,
            ...         ),
            ...     baca.OverrideCommand(
            ...         attribute_name='direction',
            ...         attribute_value=abjad.Up,
            ...         grob_name='rest',
            ...         revert=True,
            ...         selector=baca.select_rests(),
            ...         ),
            ...     baca.OverrideCommand(
            ...         attribute_name='direction',
            ...         attribute_value=abjad.Down,
            ...         grob_name='stem',
            ...         revert=True,
            ...         ),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.TaleaRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \set Staff.instrumentName = \markup { Violin }
                            \set Staff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            \override Beam.positions = #'(-6 . -6)
                            \override Stem.direction = #down
                            e'8 [
                            d''8
                            f'8 ]
                            \override Rest.direction = #up
                            r8
                            e''8 [
                            g'8
                            f''8 ]
                            r8
                            e'8 [
                            d''8
                            f'8 ]
                            r8
                            \revert Rest.direction
                            e''8 [
                            g'8 ]
                            \bar "|"
                            \revert Beam.positions
                            \revert Stem.direction
                        }
                    }
                >>
            >>

    ..  container:: example

        ::

            >>> baca.OverrideCommand()
            OverrideCommand()

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_attribute_name',
        '_attribute_value',
        '_context_name',
        '_grob_name',
        '_maximum_settings',
        '_maximum_written_duration',
        '_revert',
        '_selector',
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
        revert=None,
        selector=None,
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
            maximum_written_duration = abjad.Duration(maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if maximum_settings is not None:
            assert isinstance(maximum_settings, dict), maximum_settings
        self._maximum_settings = maximum_settings
        if revert is not None:
            revert = bool(revert)
        self._revert = revert
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

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
        manager = abjad.LilyPondFormatManager
        command = manager.make_lilypond_override_string(
            grob_name,
            attribute_name,
            attribute_value,
            context_name=context_name,
            is_once=False,
            )
        command = command.replace('\\', '')
        command = abjad.LilyPondCommand(command)
        revert = manager.make_lilypond_revert_string(
            grob_name,
            attribute_name,
            context_name=context_name,
            )
        revert = revert.replace('\\', '')
        revert = abjad.LilyPondCommand(revert, format_slot='after')
        selector = self.selector or baca.select_leaves()
        selections = selector(argument)
        if False:
            print(format(self))
            print()
            print(format(selector))
            print()
            print(argument)
            print()
            print(selections)
            print()
            print('---')
            print()
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            leaves = abjad.select(selection).by_leaf()
            if self.revert:
                abjad.attach(command, leaves[0])
                abjad.attach(revert, leaves[-1])
            else:
                for leaf in leaves:
                    if (self.maximum_written_duration is None or
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
        greater than or equal to maximum written duration of command.

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

    @property
    def revert(self):
        r'''Is true when command uses override / revert pair instead of
        multiple once commands.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._revert

    @property
    def selector(self):
        r'''Gets selector.

        Set to selector or none.

        Defaults to none.

        Returns selector or none.
        '''
        return self._selector
