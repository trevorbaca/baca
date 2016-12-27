# -*- coding: utf-8 -*-
import abjad
import baca
import copy


class ImbricationSpecifier(abjad.abctools.AbjadObject):
    r'''Imbrication specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Defaults:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.RhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=rhythmmakertools.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

        ::

            >>> figure_token = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> imbrication_map = {'Voice 1': [2, 19, 9, 18, 16]}
            >>> result = figure_maker(
            ...     ('Voice 2', figure_token),
            ...     imbrication_map=imbrication_map,
            ...     )
            >>> selections, time_signature, state_manifest = result
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     attach_lilypond_voice_commands=True,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                s16
                                d'16
                                s16
                                s16
                                s16
                            }
                            {
                                s16
                                s16
                                g''16 [
                                a'16 ]
                                s16
                            }
                            {
                                s16
                                s16
                                fs''16 [
                                e''16 ]
                                s16
                            }
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                c'16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                ef''16 ]
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Multiple imbricated voices:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.RhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=rhythmmakertools.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )
            >>> specifier_1 = baca.tools.ImbricationSpecifier(
            ...     baca.tools.ArticulationSpecifier(
            ...         articulations=['.'],
            ...         ),
            ...     rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     )
            >>> specifier_2 = baca.tools.ImbricationSpecifier(
            ...     baca.tools.ArticulationSpecifier(
            ...         articulations=['>'],
            ...         ),
            ...     rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     )

        ::

            >>> figure_token = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> imbrication_map = {
            ...     'Voice 1': (specifier_1, [2, 19, 9]),
            ...     'Voice 3': (specifier_2, [16, 10, 18]),
            ...     }
            >>> result = figure_maker(
            ...     ('Voice 2', figure_token),
            ...     imbrication_map=imbrication_map,
            ...     )
            >>> selections, time_signature, state_manifest = result
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     attach_lilypond_voice_commands=True,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                s16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16 -\staccato
                                s16
                                s16
                                s16
                            }
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16 -\staccato
                                s16
                            }
                            {
                                s16
                                s16
                                s16
                                s16
                                s16 ]
                            }
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                c'16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                ef''16 ]
                            }
                        }
                    }
                    \context Voice = "Voice 3" {
                        \voiceThree
                        {
                            {
                                s16 [
                                s16
                                s16
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16 -\accent
                            }
                            {
                                s16
                                s16
                                s16
                                s16
                                s16
                            }
                            {
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16 -\accent
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16 -\accent
                                s16
                                s16 ]
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_allow_unused_pitches',
        '_hocket',
        '_selector',
        '_specifiers',
        '_truncate_ties',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *specifiers,
        allow_unused_pitches=None,
        hocket=None,
        selector=None,
        truncate_ties=None
        ):
        self._specifiers = specifiers
        if allow_unused_pitches is not None:
            allow_unused_pitches = bool(allow_unused_pitches)
        self._allow_unused_pitches = allow_unused_pitches
        if hocket is not None:
            hocket = bool(hocket)
        self._hocket = hocket
        if selector is not None:
            if not isinstance(selector, abjad.selectortools.Selector):
                message = 'must be selector or none: {!r}.'
                message = message.format(selector)
                raise TypeError(selector)
        self._selector = selector
        if truncate_ties is not None:
            truncate_ties = bool(truncate_ties)
        self._truncate_ties = truncate_ties

    ### SPECIAL METHODS ###

    def __call__(self, container, imbrication_token):
        r'''Calls specifier on `container` with `imbrication_token`.

        ..  container:: example

            Imbrication together with polyphony:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )
                >>> polyphony_specifier = baca.tools.PolyphonySpecifier(
                ...      figure_maker=baca.tools.FigureMaker(
                ...         baca.tools.ArticulationSpecifier(
                ...             articulations=['.'],
                ...             ),
                ...         baca.tools.RhythmSpecifier(
                ...             patterns=patterntools.select_all(),
                ...             rhythm_maker=baca.tools.FigureRhythmMaker(
                ...                 talea=rhythmmakertools.Talea(
                ...                     counts=[2],
                ...                     denominator=16,
                ...                     ),
                ...                 ),
                ...             ),
                ...         ),
                ...     )
                >>> imbrication_specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> pair = (imbrication_specifier, [2, 15, 20])
                >>> imbrication_map = {'Voice 3': pair}
                >>> polyphony_map = [
                ...     ('Voice 1', [[18, 16, 15, 20, 19], [9]], polyphony_specifier),
                ...     ]
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     polyphony_map=polyphony_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 27/16
                            s1 * 27/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    fs''8 -\staccato [
                                    e''8 -\staccato
                                    ef''8 -\staccato
                                    af''8 -\staccato
                                    g''8 -\staccato ]
                                }
                                {
                                    a'8 -\staccato
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8. [
                                    d'8.
                                    bf'8. ]
                                }
                                {
                                    fs''8. [
                                    e''8.
                                    ef''8.
                                    af''8.
                                    g''8. ]
                                }
                                {
                                    a'8.
                                }
                            }
                        }
                        \context Voice = "Voice 3" {
                            \voiceThree
                            {
                                {
                                    s8. [
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    d'8. -\accent
                                    s8.
                                }
                                {
                                    s8.
                                    s8.
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    ef''8. -\accent
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    af''8. -\accent
                                    s8.
                                }
                                {
                                    s8. ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Works with pitch-classes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> pitch_classes = [
                ...     abjad.NumberedPitchClass(10),
                ...     abjad.NumberedPitchClass(6),
                ...     abjad.NumberedPitchClass(4),
                ...     abjad.NumberedPitchClass(3),
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, pitch_classes),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 27/16
                            s1 * 27/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s8. [
                                    s8.
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    bf'8. -\accent
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    fs''8. -\accent
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    e''8. -\accent
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    ef''8. -\accent
                                    s8.
                                    s8.
                                }
                                {
                                    s8. ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8. [
                                    d'8.
                                    bf'8. ]
                                }
                                {
                                    fs''8. [
                                    e''8.
                                    ef''8.
                                    af''8.
                                    g''8. ]
                                }
                                {
                                    a'8.
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Skips wrapped pitches:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     ]
                >>> imbricated_pitches = [
                ...     0,
                ...     baca.pitch.protect(10),
                ...     baca.pitch.protect(18),
                ...     10, 18,
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, imbricated_pitches),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 9/8
                            s1 * 9/8
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\accent [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\accent
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    s16
                                    s16 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'16 [
                                    d'16
                                    bf'16
                                    fs''16
                                    e''16 ]
                                }
                                {
                                    ef''16 [
                                    af''16
                                    g''16
                                    a'16 ]
                                }
                                {
                                    c'16 [
                                    d'16
                                    bf'16
                                    fs''16
                                    e''16 ]
                                }
                                {
                                    ef''16 [
                                    af''16
                                    g''16
                                    a'16 ]
                                }
                            }
                        }
                    >>
                >>

        Returns new container.
        '''
        original_container = container
        container = copy.deepcopy(container)
        imbrication_token = abjad.sequence(imbrication_token)
        imbrication_token = imbrication_token.flatten()
        cursor = baca.tools.Cursor(
            imbrication_token,
            singletons=True,
            suppress_exception=True,
            )
        pitch_number = cursor.next()
        if self.selector is not None:
            selection = self.selector(original_container)
        selected_logical_ties = None
        if self.selector is not None:
            selection = self.selector(container)
            agent = abjad.iterate(selection)
            selected_logical_ties = agent.by_logical_tie(pitched=True)
            selected_logical_ties = list(selected_logical_ties)
        agent = abjad.iterate(original_container)
        original_logical_ties = agent.by_logical_tie(pitched=True)
        logical_ties = abjad.iterate(container).by_logical_tie(pitched=True)
        pairs = zip(logical_ties, original_logical_ties)
        for logical_tie, original_logical_tie in pairs:
            if (selected_logical_ties is not None and
                logical_tie not in selected_logical_ties):
                for note in logical_tie:
                    duration = note.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(note).replace([skip])
            elif self._matches_pitch(logical_tie.head, pitch_number):
                if isinstance(pitch_number, baca.tools.Shell):
                    for note in logical_tie:
                        duration = note.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(note).replace([skip])
                    pitch_number = cursor.next()
                    continue
                pitch_number = cursor.next()
                if self.truncate_ties:
                    for note in logical_tie[1:]:
                        duration = note.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(note).replace([skip])
                if self.hocket:
                    for note in original_logical_tie:
                        duration = note.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(note).replace([skip])
            else:
                for note in logical_tie:
                    duration = note.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(note).replace([skip])
        if not self.allow_unused_pitches and not cursor.is_exhausted:
            message = '{!r} used only {} of {} pitches.'
            message = message.format(cursor, cursor.position-1, len(cursor))
            raise Exception(message)
        self._apply_specifiers(container)
        return container

    ### PRIVATE METHODS ###

    def _apply_specifiers(self, container):
        assert isinstance(container, abjad.Container), repr(container)
        nested_selections = None
        specifiers = self.specifiers or []
        selections = container[:]
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RhythmSpecifier):
                continue
            if isinstance(specifier, baca.tools.ImbricationSpecifier):
                continue
            if isinstance(specifier, abjad.rhythmmakertools.BeamSpecifier):
                specifier._detach_all_beams(selections)
            if isinstance(specifier, baca.tools.NestingSpecifier):
                nested_selections = specifier(selections)
            else:
                specifier(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    @staticmethod
    def _matches_pitch(note, pitch_object):
        if isinstance(pitch_object, baca.tools.Shell):
            pitch_object = pitch_object.payload
        if pitch_object is None:
            return False
        elif isinstance(pitch_object, (int, float)):
            source = note.written_pitch.pitch_number
        elif isinstance(pitch_object, abjad.NamedPitch):
            source = note.written_pitch
        elif isinstance(pitch_object, abjad.NumberedPitch):
            source = note.written_pitch
            source = abjad.NumberedPitch(source)
        elif isinstance(pitch_object, abjad.NamedPitchClass):
            source = note.written_pitch
            source = abjad.NamedPitchClass(source)
        elif isinstance(pitch_object, abjad.NumberedPitchClass):
            source = note.written_pitch
            source = abjad.NumberedPitchClass(source)
        else:
            message = 'unknown pitch object: {!r}.'
            message = message.format(pitch_object)
            raise TypeError(message)
        if not type(source) is type(pitch_object):
            message = 'type of {!r} must match type of {!r}.'
            message = message.format(source, pitch_object)
            raise TypeError(message)
        return source == pitch_object

    ### PUBLIC PROPERTIES ###

    @property
    def allow_unused_pitches(self):
        r'''Is true when specifier allows unused pitches.

        ..  container:: example

            Allows unused pitches:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...     ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     allow_unused_pitches=True,
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 5/8
                            s1 * 5/8
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\accent
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 -\accent
                                    s16 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    c'16 -\staccato ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on unused pitches:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...     ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     allow_unused_pitches=False,
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                Traceback (most recent call last):
                    ...
                Exception: Cursor(source=Sequence(items=(2, 19, 9, 18, 16)),
                position=4, singletons=True, suppress_exception=True)
                used only 3 of 5 pitches.

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.allow_unused_pitches is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._allow_unused_pitches

    @property
    def hocket(self):
        r'''Is true when specifier hockets voices.

        ..  container:: example

            Hockets voices:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...     ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     hocket=True,
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\accent
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 -\accent
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16 -\accent
                                    s16 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato [
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 -\staccato ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.hocket is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hocket

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects last nine notes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['>'],
                ...     ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     selector=baca.select.pitched_logical_ties(-9)
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 18, 16, 15]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 9/8
                            s1 * 9/8
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16 [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\accent
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\accent
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\accent
                                    s16
                                    s16
                                    s16 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    a'16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    a'16 -\staccato ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.selector is None
                True

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def specifiers(self):
        r'''Gets specifiers.

        ..  container:: example

            Beams nothing:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=False,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    g''16
                                    a'16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    fs''16
                                    e''16
                                    s16
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together but excludes skips:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 [ ]
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 ]
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16 ]
                                    s16
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together and includes skips:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    s16 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams each division and includes skips:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 19, 9, 18, 16])
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s16 [
                                    d'16
                                    s16
                                    s16
                                    s16 ]
                                }
                                {
                                    s16 [
                                    s16
                                    g''16
                                    a'16
                                    s16 ]
                                }
                                {
                                    s16 [
                                    s16
                                    fs''16
                                    e''16
                                    s16 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        Returns specifiers or none.
        '''
        return list(self._specifiers)

    @property
    def truncate_ties(self):
        r'''Is true when specifier truncates ties.

        ..  container:: example

            Truncates ties:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[5],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )
                >>> specifier = baca.tools.ImbricationSpecifier(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     truncate_ties=True,
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> imbrication_map = {
                ...     'Voice 1': (specifier, [2, 10, 18, 19, 9]),
                ...     }
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     imbrication_map=imbrication_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     attach_lilypond_voice_commands=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 45/32
                            s1 * 45/32
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    s8 [
                                    s32
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    d'8
                                    s32
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    bf'8
                                    s32
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    fs''8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    g''8
                                    s32
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    a'8
                                    s32 ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8 ~ [
                                    c'32
                                    d'8 ~
                                    d'32
                                    bf'8 ~
                                    bf'32 ]
                                }
                                {
                                    fs''8 ~ [
                                    fs''32
                                    e''8 ~
                                    e''32
                                    ef''8 ~
                                    ef''32
                                    af''8 ~
                                    af''32
                                    g''8 ~
                                    g''32 ]
                                }
                                {
                                    a'8 ~ [
                                    a'32 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.truncate_ties is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._truncate_ties
