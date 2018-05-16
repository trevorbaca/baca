import abjad
import baca


class AnchorSpecifier(abjad.AbjadValueObject):
    """
    Anchor specifier.

    ..  container:: example

        >>> baca.AnchorSpecifier()
        AnchorSpecifier()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(3) Specifiers'

    __slots__ = (
        '_figure_name',
        '_local_selector',
        '_remote_selector',
        '_remote_voice_name',
        '_use_remote_stop_offset',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        figure_name=None,
        local_selector=None,
        remote_selector=None,
        remote_voice_name=None,
        use_remote_stop_offset=None,
        ):
        if figure_name is not None:
            assert isinstance(figure_name, str), repr(figure_name)
        self._figure_name = figure_name
        if isinstance(local_selector, str):
            local_selector = eval(local_selector)
        if (local_selector is not None and
            not isinstance(local_selector, abjad.Expression)):
            raise TypeError(f'must be selector: {local_selector!r}.')
        self._local_selector = local_selector
        if isinstance(remote_selector, str):
            remote_selector = eval(remote_selector)
        if (remote_selector is not None and
            not isinstance(remote_selector, abjad.Expression)):
            raise TypeError(f'must be selector: {remote_selector!r}.')
        self._remote_selector = remote_selector
        if (remote_voice_name is not None and
            not isinstance(remote_voice_name, str)):
            raise TypeError(f'must be string: {remote_voice_name!r}.')
        self._remote_voice_name = remote_voice_name
        if use_remote_stop_offset is not None:
            use_remote_stop_offset = bool(use_remote_stop_offset)
        self._use_remote_stop_offset = use_remote_stop_offset

    ### PUBLIC PROPERTIES ###

    @property
    def figure_name(self):
        """
        Gets figure name.

        Returns strings or none.
        """
        return self._figure_name

    @property
    def local_selector(self):
        """
        Gets local selector.

        Returns selector or none.
        """
        return self._local_selector

    @property
    def remote_selector(self):
        """
        Gets remote selector.

        Returns selector or none.
        """
        return self._remote_selector

    @property
    def remote_voice_name(self):
        """
        Gets remote voice name.

        Set to string or none.

        Returns strings or none.
        """
        return self._remote_voice_name

    @property
    def use_remote_stop_offset(self):
        """
        Is true when contribution anchors to remote selection stop offset.

        Otherwise anchors to remote selection start offset.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._use_remote_stop_offset
