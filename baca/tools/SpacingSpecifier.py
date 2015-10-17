# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import set_


class SpacingSpecifier(AbjadObject):
    r'''Spacing specifier.

    ..  container:: example

        **Example 1.** Default spacing specifier:

        ::
            >>> import baca

        ::

            >>> specifier = baca.tools.SpacingSpecifier()

        ::

            >>> print(format(specifier))
            baca.tools.SpacingSpecifier()

    ..  container:: example

        **Example 2.** Custom spacing specifier:

        ::

            >>> specifier = baca.tools.SpacingSpecifier(
            ...     fermata_measure_width=Duration(1, 4), 
            ...     minimum_width=Duration(1, 12),
            ...     multiplier=Multiplier(5, 2),
            ...     )

        ::

            >>> print(format(specifier))
            baca.tools.SpacingSpecifier(
                fermata_measure_width=durationtools.Duration(1, 4),
                minimum_width=durationtools.Duration(1, 12),
                multiplier=durationtools.Multiplier(5, 2),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_fermata_measure_width',
        '_minimum_width',
        '_multiplier',
        '_overrides',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fermata_measure_width=None,
        minimum_width=None,
        multiplier=None,
        overrides=None,
        ):
        if fermata_measure_width is not None:
            fermata_measure_width = durationtools.Duration(
                fermata_measure_width)
        self._fermata_measure_width = fermata_measure_width
        if minimum_width is not None:
            minimum_width = durationtools.Duration(minimum_width)
        self._minimum_width = minimum_width    
        if multiplier is not None:
            multiplier = durationtools.Multiplier(multiplier)
        self._multiplier = multiplier
        if overrides is not None:
            overrides = tuple(overrides)
        self._overrides = overrides

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker):
        r'''Calls spacing specifier on `segment_maker`.

        Operates in place.

        Returns none.
        '''
        score = segment_maker._score
        measure_timespans = {}
        skip_context = score['Time Signature Context Skips']
        for skip in skip_context:
            measure_timespan = inspect_(skip).get_timespan()
            measure_timespans[measure_timespan] = []
        # nested loop can be optimized with bisect()
        for leaf in iterate(score).by_leaf():
            leaf_timespan = inspect_(leaf).get_timespan()
            for measure_timespan in measure_timespans:
                if leaf_timespan.starts_during_timespan(measure_timespan):
                    leaf_duration = leaf_timespan.duration
                    measure_timespans[measure_timespan].append(leaf_duration)
                    break
            else:
                message = 'what measure does leaf {!r} start in?'
                message = message.format(leaf)
                raise Exception(message)
        fermata_start_offsets = segment_maker._fermata_start_offsets
        for skip in iterate(skip_context).by_leaf(scoretools.Skip):
            measure_timespan = inspect_(skip).get_timespan()
            if (self.fermata_measure_width is not None and
                measure_timespan.start_offset in fermata_start_offsets):
                duration = self.fermata_measure_width
            else:
                durations = measure_timespans[measure_timespan]
                duration = min(durations)
                if self.minimum_width is not None:
                    if self.minimum_width < duration:
                        duration = self.minimum_width
                if self.multiplier is not None:
                    duration = duration / self.multiplier
            command = indicatortools.LilyPondCommand('newSpacingSection')
            attach(command, skip)
            moment = schemetools.SchemeMoment(duration)
            set_(skip).score.proportional_notation_duration = moment

    ### PUBLIC PROPERTIES ###

    @property
    def fermata_measure_width(self):
        r'''Gets fermata measure width.

        Sets fermata measures to exactly this width when set; ignores minimum
        width and multiplier.

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._fermata_measure_width

    @property
    def minimum_width(self):
        r'''Gets minimum width.

        Defaults to none and interprets none equal to ``1/8``.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._minimum_width

    @property
    def multiplier(self):
        r'''Gets multiplier.

        Defaults to none.

        Set to multiplier or none.

        Returns multiplier or none.
        '''
        return self._multiplier

    @property
    def overrides(self):
        r'''Gets overrides.

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._overrides