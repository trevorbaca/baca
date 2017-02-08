# -*- coding: utf-8 -*-
import abjad
import baca


class FigureContribution(abjad.abctools.AbjadValueObject):
    r'''Figure contribution.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.FigureContribution()
            FigureContribution()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_figure_name',
        '_hide_time_signature',
        '_local_anchor',
        '_remote_anchor',
        '_selections',
        '_state_manifest',
        '_time_signature',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        figure_name=None,
        hide_time_signature=None,
        local_anchor=None,
        remote_anchor=None,
        selections=None,
        state_manifest=None,
        time_signature=None,
        ):
        self._figure_name = figure_name
        if hide_time_signature is not None:
            hide_time_signature = bool(hide_time_signature)
        self._hide_time_signature = hide_time_signature
        prototype = abjad.selectortools.Selector
        if local_anchor is not None:
            if not isinstance(local_anchor, prototype):
                message = 'must be selector: {!r}.'
                message = message.format(local_anchor)
                raise TypeError(message)
        self._local_anchor = local_anchor
        prototype = baca.tools.VoicedSelector
        if remote_anchor is not None:
            if not isinstance(remote_anchor, prototype):
                message = 'must be voiced selector: {!r}.'
                message = message.format(remote_anchor)
                raise TypeError(message)
        self._remote_anchor = remote_anchor
        self._selections = selections
        self._state_manifest = state_manifest
        self._time_signature = time_signature

    ### SPECIAL METHODS ###

    def __getitem__(self, voice_name):
        r'''Gets `voice_name` selection list.

        Returns list of selections.
        '''
        return self.selections.__getitem__(voice_name)

    def __iter__(self):
        r'''Iterates figure contribution.

        Yields voice names.
        '''
        for voice_name in self.selections:
            yield voice_name

    ### PUBLIC METHODS ###

    def _get_duration(self):
        durations = []
        for voice_name in sorted(self.selections):
            selection = self[voice_name]
            if selection:
                durations.append(selection.get_duration())
        assert len(set(durations)) == 1, repr(durations)
        return durations[0]

    ### PUBLIC PROPERTIES ###

    @property
    def figure_name(self):
        r'''Gets figure name.

        Returns string or none.
        '''
        return self._figure_name

    @property
    def hide_time_signature(self):
        r'''Is true when contribution hides time signature.

        Returns true, false or none.
        '''
        return self._hide_time_signature

    @property
    def local_anchor(self):
        r'''Gets local anchor selector.

        Returns selector or none.
        '''
        return self._local_anchor

    @property
    def remote_anchor(self):
        r'''Gets remote anchor selector.

        Returns selector or none.
        '''
        return self._remote_anchor

    @property
    def selections(self):
        r'''Gets selections.

        Returns list of selections or none.
        '''
        if self._selections is not None:
            assert isinstance(self._selections, dict), repr(self._selections)
            for value in self._selections.values():
                assert isinstance(value, abjad.Selection), repr(value)
        return self._selections

    @property
    def state_manifest(self):
        r'''Gets state manifest.

        Returns state manifest or none.
        '''
        return self._state_manifest

    @property
    def time_signature(self):
        r'''Gets time signature.

        Returns time signature or none.
        '''
        return self._time_signature
