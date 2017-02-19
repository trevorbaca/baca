# -*- coding: utf-8 -*-
import abjad


class AnchorSpecifier(abjad.abctools.AbjadValueObject):
    r'''Anchor specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.AnchorSpecifier()
            AnchorSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_just_after',
        '_local_selector',
        '_remote_selector',
        '_remote_voice_name',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        just_after=None,
        local_selector=None,
        remote_selector=None,
        remote_voice_name=None,
        ):
        if just_after is not None:
            just_after = bool(just_after)
        self._just_after = just_after
        if (local_selector is not None and
            not isinstance(local_selector, abjad.Selector)):
            message = 'must be selector: {!r}.'
            message = message.format(local_selector)
            raise TypeError(message)
        self._local_selector = local_selector
        if (remote_selector is not None and
            not isinstance(remote_selector, abjad.Selector)):
            message = 'must be selector: {!r}.'
            message = message.format(remote_selector)
            raise TypeError(message)
        self._remote_selector = remote_selector
        if (remote_voice_name is not None and
            not isinstance(remote_voice_name, str)):
            message = 'voice name must be string: {!r}.'
            message = message.format(remote_voice_name)
            raise TypeError(message)
        self._remote_voice_name = remote_voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def just_after(self):
        r'''Is true when contribution anchors just after remote selection.

        Returns true, false or none.
        '''
        return self._just_after

    @property
    def local_selector(self):
        r'''Gets local selector.

        Returns selector or none.
        '''
        return self._local_selector

    @property
    def remote_selector(self):
        r'''Gets remote selector.

        Returns selector or none.
        '''
        return self._remote_selector

    @property
    def remote_voice_name(self):
        r'''Gets remote voice name.

        Set to string or none.

        Returns strings or none.
        '''
        return self._remote_voice_name
