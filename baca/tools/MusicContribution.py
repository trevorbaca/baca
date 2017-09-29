import abjad
import baca


class MusicContribution(abjad.AbjadValueObject):
    r'''Music contribution.

    ..  container:: example

        ::

            >>> baca.MusicContribution()
            MusicContribution()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Music'

    __slots__ = (
        '_anchor',
        '_color_selector_result',
        '_figure_name',
        '_hide_time_signature',
        '_selections',
        '_state_manifest',
        '_time_signature',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        anchor=None,
        color_selector_result=None,
        figure_name=None,
        hide_time_signature=None,
        selections=None,
        state_manifest=None,
        time_signature=None,
        ):
        if (anchor is not None and
            not isinstance(anchor, baca.AnchorCommand)):
            message = 'must be anchor specifier: {!r}.'
            message = message.format(anchor)
            raise TypeError(message)
        self._anchor = anchor
        self._color_selector_result = color_selector_result
        self._figure_name = figure_name
        if hide_time_signature is not None:
            hide_time_signature = bool(hide_time_signature)
        self._hide_time_signature = hide_time_signature
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
    def anchor(self):
        r'''Gets anchor.

        Returns anchor specifier or none.
        '''
        return self._anchor

    @property
    def color_selector_result(self):
        r'''Gets color selector result.

        Returns selector result or none.
        '''
        return self._color_selector_result

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
