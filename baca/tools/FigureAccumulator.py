# -*- coding: utf-8 -*-
import abjad
import baca


class FigureAccumulator(abjad.abctools.AbjadObject):
    r'''Figure-accumulator.

    ::

        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Figures'

    __slots__ = (
        '_current_offset',
        '_figure_maker',
        '_figure_names',
        '_floating_selections',
        '_selections',
        '_time_signatures',
        )

    _all_voice_names = (
        'Voice 1',
        'Voice 2',
        'Voice 3',
        'Voice 4',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._current_offset = abjad.Offset(0)
        self._figure_maker = self._make_default_figure_maker()
        self._figure_names = []
        self._floating_selections = self._make_voice_dictionary()
        self._selections = self._make_voice_dictionary()
        self._time_signatures = []

    ### SPECIAL METHODS ###

    def __call__(self, figure_contribution):
        r'''Calls figure-accumulator on `figure_contribution`.

        Raises exception on duplicate figure name.

        ..  container:: example

            ::

                >>> accumulator = baca.tools.FigureAccumulator()
                >>> accumulator(
                ...     accumulator.figure_maker(
                ...         [[0, 1, 2, 3]],
                ...         figure_name='D',
                ...         voice_name='Voice 1',
                ...         ),
                ...     )

            ::

                >>> accumulator(
                ...     accumulator.figure_maker(
                ...         [[4, 5, 6, 7]],
                ...         figure_name='D',
                ...         voice_name='Voice 1',
                ...         ),
                ...     )
                Traceback (most recent call last):
                    ...
                Exception: duplicate figure name: D.

        Returns none.
        '''
        self._cache_figure_name(figure_contribution)
        self._cache_selections(figure_contribution)
        self._cache_floating_selections(figure_contribution)
        self._cache_time_signature(figure_contribution)

    ### PRIVATE METHODS ###

    def _assemble_floating_selections(self, segment_maker):
        for voice_name in sorted(self.selections):
            selection = self.assemble(voice_name)
            if selection:
                segment_maker.append_specifiers(
                    (voice_name, baca.select.stages(1, 1)),
                    baca.tools.RhythmSpecifier(
                        rhythm_maker=selection,
                        ),
                    )

    def _cache_figure_name(self, figure_contribution):
        if figure_contribution.figure_name is None:
            return
        if figure_contribution.figure_name in self._figure_names:
            message = 'duplicate figure name: {}.'
            message = message.format(figure_contribution.figure_name)
            raise Exception(message)
        self._figure_names.append(figure_contribution.figure_name)

    def _cache_floating_selections(self, figure_contribution):
        for voice_name in figure_contribution:
            selection = figure_contribution[voice_name]
            if not selection:
                continue
            start_offset = self._get_start_offset(
                selection,
                figure_contribution,
                )
            stop_offset = start_offset + selection.get_duration()
            timespan = abjad.Timespan(start_offset, stop_offset)
            floating_selection = baca.tools.FloatingSelection(
                selection=selection,
                timespan=timespan,
                )
            self._floating_selections[voice_name].append(floating_selection)
        self._current_offset = stop_offset

    def _cache_selections(self, figure_contribution):
        for voice_name in self.selections:
            if voice_name in figure_contribution:
                selections = figure_contribution[voice_name]
                self.selections[voice_name].extend(selections)
            else:
                figure_duration = figure_contribution._get_duration()
                multiplier = abjad.Multiplier(figure_duration)
                skip = abjad.Skip(1)
                abjad.attach(multiplier, skip)
                selection = abjad.selectiontools.Selection([skip])
                self.selections[voice_name].append(selection)

    def _cache_time_signature(self, figure_contribution):
        if figure_contribution.hide_time_signature:
            return
        if figure_contribution.remote_anchor is None:
            self.time_signatures.append(figure_contribution.time_signature)

    def _get_start_offset(self, selection, figure_contribution):
        if figure_contribution.remote_anchor is None:
            return self._current_offset
        voice_name = figure_contribution.remote_anchor.voice_name
        selector = figure_contribution.remote_anchor.selector
        selections = self.selections[voice_name]
        result = selector(selections)
        selected_leaves = list(abjad.iterate(result).by_leaf())
        first_selected_leaf = selected_leaves[0]
        dummy_container = abjad.Container(selections)
        timespan = abjad.inspect_(first_selected_leaf).get_timespan()
        del(dummy_container[:])
        remote_anchor_start_offset = timespan.start_offset
        local_anchor_start_offset = abjad.Offset(0)
        if figure_contribution.local_anchor is not None:
            selector = figure_contribution.local_anchor
            result = selector(selection)
            selected_leaves = list(abjad.iterate(result).by_leaf())
            first_selected_leaf = selected_leaves[0]
            dummy_container = abjad.Container(selection)
            timespan = abjad.inspect_(first_selected_leaf).get_timespan()
            del(dummy_container[:])
            local_anchor_start_offset = timespan.start_offset
        start_offset = remote_anchor_start_offset - local_anchor_start_offset
        return start_offset

    @staticmethod
    def _insert_skips(floating_selections, voice_name):
        for floating_selection in floating_selections:
            assert isinstance(floating_selection, baca.tools.FloatingSelection)
        floating_selections = list(floating_selections)
        floating_selections.sort(key=lambda _: _.timespan)
        try:
            first_start_offset = floating_selections[0].timespan.start_offset
        except:
            raise Exception(floating_selections, voice_name)
        timespans = [_.timespan for _ in floating_selections]
        timespans = abjad.timespantools.TimespanInventory(timespans)
        gaps = ~timespans
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        selections = floating_selections + list(gaps)
        def sort_function(argument):
            if isinstance(argument, baca.tools.FloatingSelection):
                return argument.timespan
            elif isinstance(argument, abjad.Timespan):
                return argument
            else:
                raise TypeError(argument)
        selections.sort(key=sort_function)
        fused_selection = []
        for selection in selections:
            if isinstance(selection, baca.tools.FloatingSelection):
                fused_selection.extend(selection.selection)
            else:
                assert isinstance(selection, abjad.Timespan)
                multiplier = abjad.Multiplier(selection.duration)
                skip = abjad.Skip(1)
                abjad.attach(multiplier, skip)
                fused_selection.append(skip)
        fused_selection = abjad.select(fused_selection)
        return fused_selection

    @staticmethod
    def _make_default_figure_maker():
        return baca.tools.FigureMaker(
            abjad.rhythmmakertools.BeamSpecifier(
                beam_divisions_together=True,
                ),
            baca.tools.RhythmSpecifier(
                patterns=abjad.patterntools.select_all(),
                rhythm_maker=baca.tools.FigureRhythmMaker(
                    talea=abjad.rhythmmakertools.Talea(
                        counts=[1],
                        denominator=16,
                        ),
                    ),
                ),
            annotate_unregistered_pitches=True,
            preferred_denominator=16,
            )

    def _make_voice_dictionary(self):
        return dict([(_, []) for _ in self._all_voice_names])

    def _populate_segment_maker(self, segment_maker):
        self._assemble_floating_selections(segment_maker)
#        for voice_name in self.selections:
#            selection = abjad.sequence(self.selections[voice_name])
#            selection = selection.flatten()
#            selection = abjad.selectiontools.Selection(selection)
#            segment_maker.append_specifiers(
#                (voice_name, baca.select.stages(1, 1)),
#                baca.tools.RhythmSpecifier(
#                    rhythm_maker=selection,
#                    ),
#                )

    ### PUBLIC PROPERTIES ###

    @property
    def figure_maker(self):
        r'''Gets default figure-maker.

        Returns figure-maker.
        '''
        return self._figure_maker

    @property
    def selections(self):
        r'''Gets selections by voice name.

        Returns dictionary.
        '''
        return self._selections

    @property
    def time_signatures(self):
        r'''Gets time signatures.

        Returns list.
        '''
        return self._time_signatures

    ### PUBLIC METHODS ###

    def assemble(self, voice_name):
        r'''Assembles complete selection for `voice_name`.

        Returns selection or none.
        '''
        floating_selections = self._floating_selections[voice_name]
        if not floating_selections:
            return
        selection = self._insert_skips(floating_selections, voice_name)
        assert isinstance(selection, abjad.Selection), repr(selection)
        return selection
