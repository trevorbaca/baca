import abc
import abjad
import baca


class Command(abjad.AbjadObject):
    r'''Command.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'

    __slots__ = (
        '_deactivate',
        '_manifests',
        '_selector',
        '_tag',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate=None,
        selector=None,
        tag=None,
        ):
        self._deactivate = deactivate
        self._manifests = None
        if isinstance(selector, str):
            selector = eval(selector)
        if selector is not None:
            prototype = (abjad.Expression, baca.MapCommand)
            assert isinstance(selector, prototype), repr(selector)
        self._selector = selector
        if tag is not None:
            assert isinstance(tag, str)
        self._tag = tag

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        pass

    ### PRIVATE METHODS ###

    @staticmethod
    def _are_valid_tags(tags):
        assert isinstance(tags, list), repr(tags)
        assert '' not in tags, repr(tags)
        assert not any(':' in _ for _ in tags), repr(tags)
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def deactivate(self):
        r'''Is true when tag should write deactivated.

        Returns true, false or none.
        '''
        return self._deactivate

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def tag(self):
        r'''Gets colon-delimited tag.

        Returns string or none.
        '''
        if self.tags:
            return ':'.join(self.tags)

    @property
    def tags(self):
        r'''Gets tags.

        Returns list of strings.
        '''
        assert self._are_valid_tags(self._tags)
        return self._tags[:]
