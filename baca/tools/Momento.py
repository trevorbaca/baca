import abjad


class Momento(abjad.AbjadObject):
    r'''Momento.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_absent',
        '_class_string',
        '_key',
        '_local_context_name',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        absent=None,
        class_string=None,
        key=None,
        local_context_name=None,
        ):
        if absent is not None:
            absent = bool(absent)
        self._absent = absent
        if class_string is not None:
            assert isinstance(class_string, str), repr(class_string)
        self._class_string = class_string
        if key is not None:
            assert isinstance(key, str), repr(key)
        self._key = key
        if local_context_name is not None:
            assert isinstance(local_context_name, str), repr(local_context_name)
        self._local_context_name = local_context_name

    ### PUBLIC PROPERTIES ###

    @property
    def absent(self):
        r'''Is true when context is absent in this segment.

        Returns true, false or none.
        '''
        return self._absent

    @property
    def class_string(self):
        r'''Gets class string.

        Returns string.
        '''
        return self._class_string

    @property
    def key(self):
        r'''Gets key.

        Returns string.
        '''
        return self._key

    @property
    def local_context_name(self):
        r'''Gets local context name.

        Returns string.
        '''
        return self._local_context_name
