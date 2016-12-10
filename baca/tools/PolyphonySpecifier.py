# -*- coding: utf-8 -*-
import abjad
import baca


class PolyphonySpecifier(abjad.abctools.AbjadObject):
    r'''Polyphony specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> specifier_1a = baca.tools.PolyphonySpecifier(
            ...     figure_maker=baca.tools.FigureMaker(
            ...         baca.tools.ArticulationSpecifier(
            ...             articulations=['>'],
            ...             ),
            ...         baca.tools.RhythmSpecifier(
            ...             patterns=abjad.patterntools.select_all(),
            ...             rhythm_maker=baca.tools.FigureRhythmMaker(
            ...                 talea=abjad.rhythmmakertools.Talea(
            ...                     counts=[2],
            ...                     denominator=16,
            ...                     ),
            ...                 time_treatments=[1],
            ...                 ),
            ...             ),
            ...         ),
            ...     local_anchor_selector=baca.selector.logical_tie(-3),
            ...     remote_anchor_selector=baca.selector.logical_tie(0),
            ...     )
            >>> specifier_1b = abjad.new(
            ...     specifier_1a,
            ...     local_anchor_selector=baca.selector.logical_tie(2),
            ...     remote_anchor_selector=baca.selector.logical_tie(4),
            ...     )
            >>> specifier_1c = abjad.new(
            ...     specifier_1a,
            ...     local_anchor_selector=baca.selector.logical_tie(1),
            ...     remote_anchor_selector=baca.selector.logical_tie(-2),
            ...     )
            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.ArticulationSpecifier(
            ...         articulations=['.'],
            ...         ),
            ...     baca.tools.RhythmSpecifier(
            ...         patterns=abjad.patterntools.select_all(),
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[3],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> polyphony_map = [
            ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier_1a),
            ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier_1b),
            ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier_1c),
            ...     ]
            >>> result = figure_maker(
            ...     ('Voice 2', figure_token),
            ...     polyphony_map=polyphony_map,
            ...     )
            >>> selections, time_signature, state_manifest = result
            >>> lilypond_file = abjad.rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     [time_signature],
            ...     attach_lilypond_voice_commands=True,
            ...     pitched_staff=True,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 171/80
                        s1 * 171/80
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/10 {
                                fs''8 -\accent [
                                e''8 -\accent
                                ef''8 -\accent
                                af''8 -\accent
                                g''8 -\accent ]
                            }
                        }
                        s1 * 1/16
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/10 {
                                fs''8 -\accent [
                                e''8 -\accent
                                ef''8 -\accent
                                af''8 -\accent
                                g''8 -\accent ]
                            }
                        }
                        s1 * 1/80
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/10 {
                                fs''8 -\accent [
                                e''8 -\accent
                                ef''8 -\accent
                                af''8 -\accent
                                g''8 -\accent ]
                            }
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        s1 * 11/40
                        {
                            {
                                c'8. -\staccato [
                                d'8. -\staccato
                                bf'8. -\staccato ]
                            }
                            {
                                fs''8. -\staccato [
                                e''8. -\staccato
                                ef''8. -\staccato
                                af''8. -\staccato
                                g''8. -\staccato ]
                            }
                            {
                                a'8. -\staccato
                            }
                        }
                    }
                >>
            >>

    '''
    
    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_figure_maker',
        '_local_anchor_selector',
        '_remote_anchor_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        figure_maker=None,
        local_anchor_selector=None,
        remote_anchor_selector=None,
        ):
        if figure_maker is not None:
            if not isinstance(figure_maker, baca.tools.FigureMaker):
                message = 'must be figure-maker or none: {!r}.'
                message = message.format(figure_maker)
                raise TypeError(message)
        self._figure_maker = figure_maker
        prototype = abjad.selectortools.Selector
        if local_anchor_selector is not None:
            if not isinstance(local_anchor_selector, prototype):
                message = 'must be selector or none: {!r}.'
                message = message.format(local_anchor_selector)
                raise TypeError(message)
        self._local_anchor_selector = local_anchor_selector
        if remote_anchor_selector is not None:
            if not isinstance(remote_anchor_selector, prototype):
                message = 'must be selector or none: {!r}.'
                message = message.format(remote_anchor_selector)
                raise TypeError(message)
        self._remote_anchor_selector = remote_anchor_selector

    ### SPECIAL METHODS ###

    def __call__(self, container, figure_token):
        r'''Calls polyphony specifier on `container` and `figure_token`.

        Returns selection.
        '''
        result = self.figure_maker(figure_token)
        selection, time_signature, state_manifest = result
        local_anchor = self._get_local_anchor(selection)
        remote_anchor = self._get_remote_anchor(container)
        timespan = abjad.inspect_(local_anchor).get_timespan()
        local_preanchor_duration = abjad.Duration(timespan.start_offset)
        timespan = abjad.inspect_(remote_anchor).get_timespan()
        remote_preanchor_duration = abjad.Duration(timespan.start_offset)
        start_offset = remote_preanchor_duration - local_preanchor_duration
        start_offset = abjad.Offset(start_offset)
        return start_offset, selection

    ### PRIVATE METHODS ###

    @staticmethod
    def _fuse_voices(selections_by_voice):
        for voice_name, selection_pairs in selections_by_voice.items():
            if not selection_pairs:
                continue
            if len(selection_pairs) == 1:
                selection_pair = selection_pairs[0]
                offset, selection = selection_pair
                if 0 < offset:
                    multiplier = abjad.Multiplier(offset)
                    skip = abjad.Skip(1)
                    abjad.attach(multiplier, skip)
                    selection = [skip] + selection[:]
                    selection = abjad.select(selection)
                    selection_pair = (abjad.Offset(0), selection)
                selection_pair = list(selection_pair)
                selections_by_voice[voice_name] = selection_pair
                continue
            selection_pairs.sort(key=lambda _: _[0])
            first_start_offset = selection_pairs[0][0]
            timespans = abjad.timespantools.TimespanInventory()
            for selection_pair in selection_pairs:
                start_offset, selection = selection_pair
                duration = selection.get_duration()
                stop_offset = start_offset + duration
                timespan = abjad.timespantools.Timespan(
                    start_offset,
                    stop_offset,
                    )
                timespans.append(timespan)
            gaps = ~timespans
            if 0 < first_start_offset:
                first_gap = abjad.timespantools.Timespan(0, first_start_offset)
                gaps.append(first_gap)
            selections = selection_pairs + list(gaps)
            def sort_function(object_):
                if isinstance(object_, tuple):
                    return object_[0]
                else:
                    return object_.start_offset
            selections.sort(key=sort_function)
            fused_selection = []
            for selection in selections:
                if isinstance(selection, tuple):
                    selection_ = selection[1]
                    fused_selection.extend(selection_)
                else:
                    assert isinstance(selection, abjad.timespantools.Timespan)
                    multiplier = abjad.Multiplier(selection.duration)
                    skip = abjad.Skip(1)
                    abjad.attach(multiplier, skip)
                    fused_selection.append(skip)
            fused_selection = abjad.select(fused_selection)
            start_offset = abjad.Offset(0)
            if first_start_offset < 0:
                start_offset = first_start_offset
            fused_selection_pair = [start_offset, fused_selection]
            selections_by_voice[voice_name] = fused_selection_pair

    def _get_local_anchor(self, selection):
        selector = self.local_anchor_selector or baca.selector.first_leaf()
        local_anchor = selector(selection)
        if isinstance(local_anchor, abjad.selectiontools.Selection):
            local_anchor = local_anchor[0]
        if not isinstance(local_anchor, abjad.scoretools.Component):
            message = 'must select selection or component: {!r}.'
            message = message.format(local_anchor_selector)
            raise Exception(message)
        return local_anchor

    def _get_remote_anchor(self, remote_container):
        selector = self.remote_anchor_selector or baca.selector.first_leaf()
        remote_anchor = selector(remote_container)
        if isinstance(remote_anchor, abjad.selectiontools.Selection):
            remote_anchor = remote_anchor[0]
        if not isinstance(remote_anchor, abjad.scoretools.Component):
            message = 'must select selection or component: {!r}.'
            message = message.format(remote_anchor_selector)
            raise Exception(message)
        return remote_anchor

    @classmethod
    def _make_polyphony_selections(class_, container, polyphony_map):
        if not polyphony_map:
            return {}, None
        polyphony_map = polyphony_map or []
        selections_by_voice = {}
        for entry in polyphony_map:
            assert isinstance(entry, tuple), repr(entry)
            assert len(entry) == 3, repr(entry)
            voice_name, figure_token, polyphony_specifier = entry
            result = polyphony_specifier(container, figure_token)
            start_offset, selection = result
            if voice_name not in selections_by_voice:
                selections_by_voice[voice_name] = []
            selections_by_voice[voice_name].append((start_offset, selection))
        class_._fuse_voices(selections_by_voice)
        offset_selections = selections_by_voice.values()
        hauptstimme_skips = []
        for voice_name, offset_selection in selections_by_voice.items():
            offset = offset_selection[0]
            selection = offset_selection[1]
            selections_by_voice[voice_name] = [selection]
            if offset < 0:
                multiplier = abjad.Multiplier(-offset)
                skip = abjad.Skip(1)
                abjad.attach(multiplier, skip)
                hauptstimme_skips.append(skip)
        hauptstimme_skip = None
        if hauptstimme_skips:
            hauptstimme_skip = max(hauptstimme_skips)
        return selections_by_voice, hauptstimme_skip

    ### PUBLIC PROPERTIES ###

    @property
    def figure_maker(self):
        r'''Gets figure-maker.

        See local anchor selector examples, below.

        Defaults to none.

        Set to figure-maker or none.

        Returns figure-maker or none.
        '''
        return self._figure_maker

    @property
    def local_anchor_selector(self):
        r'''Gets local alignment selector.

        ..  container:: example

            Left-overhang polyphony:

            ::

                >>> specifier = baca.tools.PolyphonySpecifier(
                ...     figure_maker=baca.tools.FigureMaker(
                ...         baca.tools.ArticulationSpecifier(
                ...             articulations=['>'],
                ...             ),
                ...         baca.tools.RhythmSpecifier(
                ...             patterns=abjad.patterntools.select_all(),
                ...             rhythm_maker=baca.tools.FigureRhythmMaker(
                ...                 talea=abjad.rhythmmakertools.Talea(
                ...                     counts=[2],
                ...                     denominator=16,
                ...                     ),
                ...                 time_treatments=[1],
                ...                 ),
                ...             ),
                ...         ),
                ...     local_anchor_selector=baca.selector.logical_tie(1),
                ...     )
                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=abjad.patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> polyphony_map = [
                ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier),
                ...     ]
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     polyphony_map=polyphony_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = abjad.rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     [time_signature],
                ...     attach_lilypond_voice_commands=True,
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 73/40
                            s1 * 73/40
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 11/10 {
                                    fs''8 -\accent [
                                    e''8 -\accent
                                    ef''8 -\accent
                                    af''8 -\accent
                                    g''8 -\accent ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            s1 * 11/80
                            {
                                {
                                    c'8. -\staccato [
                                    d'8. -\staccato
                                    bf'8. -\staccato ]
                                }
                                {
                                    fs''8. -\staccato [
                                    e''8. -\staccato
                                    ef''8. -\staccato
                                    af''8. -\staccato
                                    g''8. -\staccato ]
                                }
                                {
                                    a'8. -\staccato
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Right-overhang polyphony:

            ::

                >>> specifier = baca.tools.PolyphonySpecifier(
                ...     figure_maker=baca.tools.FigureMaker(
                ...         baca.tools.ArticulationSpecifier(
                ...             articulations=['>'],
                ...             ),
                ...         baca.tools.RhythmSpecifier(
                ...             patterns=abjad.patterntools.select_all(),
                ...             rhythm_maker=baca.tools.FigureRhythmMaker(
                ...                 talea=abjad.rhythmmakertools.Talea(
                ...                     counts=[2],
                ...                     denominator=16,
                ...                     ),
                ...                 time_treatments=[1],
                ...                 ),
                ...             ),
                ...         ),
                ...     local_anchor_selector=baca.selector.logical_tie(-2),
                ...     remote_anchor_selector=baca.selector.logical_tie(-1),
                ...     )
                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=abjad.patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> polyphony_map = [
                ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier),
                ...     ]
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     polyphony_map=polyphony_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = abjad.rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     [time_signature],
                ...     attach_lilypond_voice_commands=True,
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 71/40
                            s1 * 71/40
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            s1 * 87/80
                            {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 11/10 {
                                    fs''8 -\accent [
                                    e''8 -\accent
                                    ef''8 -\accent
                                    af''8 -\accent
                                    g''8 -\accent ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8. -\staccato [
                                    d'8. -\staccato
                                    bf'8. -\staccato ]
                                }
                                {
                                    fs''8. -\staccato [
                                    e''8. -\staccato
                                    ef''8. -\staccato
                                    af''8. -\staccato
                                    g''8. -\staccato ]
                                }
                                {
                                    a'8. -\staccato
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Inset polyphony:

            ::

                >>> specifier_1a = baca.tools.PolyphonySpecifier(
                ...     figure_maker=baca.tools.FigureMaker(
                ...         baca.tools.ArticulationSpecifier(
                ...             articulations=['>'],
                ...             ),
                ...         baca.tools.RhythmSpecifier(
                ...             patterns=abjad.patterntools.select_all(),
                ...             rhythm_maker=baca.tools.FigureRhythmMaker(
                ...                 talea=abjad.rhythmmakertools.Talea(
                ...                     counts=[2],
                ...                     denominator=16,
                ...                     ),
                ...                 time_treatments=[1],
                ...                 ),
                ...             ),
                ...         ),
                ...     local_anchor_selector=baca.selector.logical_tie(1),
                ...     remote_anchor_selector=baca.selector.logical_tie(1),
                ...     )
                >>> specifier_1b = abjad.new(
                ...     specifier_1a,
                ...     local_anchor_selector=baca.selector.logical_tie(-2),
                ...     remote_anchor_selector=baca.selector.logical_tie(-2),
                ...     )
                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=abjad.patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> polyphony_map = [
                ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier_1a),
                ...     ('Voice 1', [[18, 16, 15, 20, 19]], specifier_1b),
                ...     ]
                >>> result = figure_maker(
                ...     ('Voice 2', figure_token),
                ...     polyphony_map=polyphony_map,
                ...     )
                >>> selections, time_signature, state_manifest = result
                >>> lilypond_file = abjad.rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     [time_signature],
                ...     attach_lilypond_voice_commands=True,
                ...     pitched_staff=True,
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
                            s1 * 1/20
                            {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 11/10 {
                                    fs''8 -\accent [
                                    e''8 -\accent
                                    ef''8 -\accent
                                    af''8 -\accent
                                    g''8 -\accent ]
                                }
                            }
                            s1 * 13/80
                            {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 11/10 {
                                    fs''8 -\accent [
                                    e''8 -\accent
                                    ef''8 -\accent
                                    af''8 -\accent
                                    g''8 -\accent ]
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8. -\staccato [
                                    d'8. -\staccato
                                    bf'8. -\staccato ]
                                }
                                {
                                    fs''8. -\staccato [
                                    e''8. -\staccato
                                    ef''8. -\staccato
                                    af''8. -\staccato
                                    g''8. -\staccato ]
                                }
                                {
                                    a'8. -\staccato
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._local_anchor_selector

    @property
    def remote_anchor_selector(self):
        r'''Gets remote alignment selector.

        See local anchor selector examples, above.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._remote_anchor_selector
