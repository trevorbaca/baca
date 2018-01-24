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
        '_offset_to_measure_number',
        '_selector',
        '_tag_measure_number',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate=None,
        selector=None,
        tag_measure_number=None,
        ):
        self._deactivate = deactivate
        if isinstance(selector, str):
            selector = eval(selector)
        if selector is not None:
            prototype = (abjad.Expression, baca.MapCommand)
            assert isinstance(selector, prototype), repr(selector)
        self._selector = selector
        self.manifests = None
        self.offset_to_measure_number = None
        self.tag_measure_number = tag_measure_number

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
    def manifests(self):
        r'''Gets segment-maker manifests.

        Returns dictionary.
        '''
        return self._manifests

    @manifests.setter
    def manifests(self, dictionary):
        prototype = (abjad.OrderedDict, type(None))
        assert isinstance(dictionary, prototype), repr(dictionary)
        self._manifests = dictionary
        for command in getattr(self, 'commands', []):
            command._manifests = dictionary

    @property
    def offset_to_measure_number(self):
        r'''Gets segment-maker offset_to_measure_number dictionary.

        Returns dictionary.
        '''
        return self._offset_to_measure_number

    @offset_to_measure_number.setter
    def offset_to_measure_number(self, dictionary):
        prototype = (dict, type(None))
        assert isinstance(dictionary, prototype), repr(dictionary)
        self._offset_to_measure_number = dictionary
        for command in getattr(self, 'commands', []):
            command._offset_to_measure_number = dictionary

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
    def tag_measure_number(self):
        r'''Is true when command should tag measure number at format-time.

        Returns true, false or none.
        '''
        return self._tag_measure_number

    @manifests.setter
    def tag_measure_number(self, argument):
        assert argument in (True, False, None), repr(argument)
        self._tag_measure_number = argument
        for command in getattr(self, 'commands', []):
            command._tag_measure_number = argument

    @property
    def tags(self):
        r'''Gets tags.

        Returns list of strings.
        '''
        assert self._are_valid_tags(self._tags)
        return self._tags[:]

    ### PUBLIC METHODS ###

    def get_tag(self, leaf=None):
        r'''Gets tag for `leaf`.

        Returns colon-delimited string.
        '''
        tags = self.tags[:]
        if self._tag_measure_number:
            start_offset = abjad.inspect(leaf).get_timespan().start_offset
            measure_number = self._offset_to_measure_number.get(start_offset)
            if measure_number is not None:
                tag = f'MEASURE_{measure_number}'
                tags.append(tag)
        if tags:
            tags.sort()
            return ':'.join(tags)
