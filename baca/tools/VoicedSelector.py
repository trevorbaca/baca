# -*- coding: utf-8 -*-
import abjad


class VoicedSelector(abjad.abctools.AbjadValueObject):
    r'''Voiced selector.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.VoicedSelector()
            VoicedSelector()

    ..  container:: example

        ::

            >>> selector = baca.tools.VoicedSelector(
            ...     voice_name='Piano Music Voice 1',
            ...     selector=baca.select.logical_tie(0),
            ...     )

        ::

            >>> f(selector)
            baca.tools.VoicedSelector(
                voice_name='Piano Music Voice 1',
                selector=selectortools.Selector(
                    callbacks=(
                        selectortools.LogicalTieSelectorCallback(
                            flatten=True,
                            pitched=False,
                            trivial=True,
                            ),
                        selectortools.ItemSelectorCallback(
                            item=0,
                            apply_to_each=False,
                            ),
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_selector',
        '_voice_name',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, voice_name=None, selector=None):
        if selector is not None:
            if not isinstance(selector, abjad.selectortools.Selector):
                message = 'must be selector: {!r}.'
                message = message.format(selector)
                raise TypeError(message)
        self._selector = selector
        if voice_name is not None:
            if not isinstance(voice_name, str):
                message = 'must be voice name: {!r}.'
                message = message.format(voice_name)
                raise TypeError(message)
        self._voice_name = voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        Returns selector or none.
        '''
        return self._selector

    @property
    def voice_name(self):
        r'''Gets voice name.

        Returns string or none.
        '''
        return self._voice_name
