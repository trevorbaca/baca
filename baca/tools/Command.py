import abc
import abjad
import baca
from .Typing import List
from .Typing import Optional
from .Typing import Selector
from .Typing import Union


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
        '_tags',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate: bool = None,
        selector: Selector = None,
        tag_measure_number: bool = None,
        ) -> None:
        from baca.tools.MapCommand import MapCommand
        self._deactivate: bool = deactivate
        if isinstance(selector, str):
            selector_ = eval(selector)
        else:
            selector_ = selector
        if selector_ is not None:
            prototype = (abjad.Expression, MapCommand)
            assert isinstance(selector_, prototype), repr(selector_)
        self._selector: Optional[abjad.Expression] = selector_
        self._tags: List[abjad.Tag] = None
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

    @staticmethod
    def _remove_reapplied_wrappers(leaf, indicator):
        if not getattr(indicator, 'persistent', False):
            return
        if abjad.inspect(leaf).get_timespan().start_offset != 0:
            return
        if isinstance(indicator, abjad.Instrument):
            prototype = abjad.Instrument
        elif isinstance(indicator, abjad.MetronomeMark):
            prototype = (
                abjad.Accelerando,
                abjad.MetronomeMark,
                abjad.Ritardando,
                )
        else:
            prototype = type(indicator)
        stem = abjad.String.to_indicator_stem(indicator)
        assert stem in (
            'CLEF',
            'DYNAMIC',
            'INSTRUMENT',
            'MARGIN_MARKUP',
            'METRONOME_MARK',
            'STAFF_LINES',
            ), repr(stem)
        reapplied_wrappers = []
        reapplied_indicators = []
        wrappers = list(abjad.inspect(leaf).wrappers())
        effective_wrapper = abjad.inspect(leaf).effective_wrapper(prototype)
        if effective_wrapper and effective_wrapper not in wrappers:
            component = effective_wrapper.component
            start_1 = abjad.inspect(leaf).get_timespan().start_offset
            start_2 = abjad.inspect(component).get_timespan().start_offset
            if start_1 == start_2:
                wrappers_ = abjad.inspect(component).wrappers()
                wrappers.extend(wrappers_)
        for wrapper in wrappers:
            if not wrapper.tag:
                continue
            is_reapplied_wrapper = False
            for word in abjad.Tag(wrapper.tag):
                if f'REAPPLIED_{stem}' in word or f'DEFAULT_{stem}' in word:
                    is_reapplied_wrapper = True
            if not is_reapplied_wrapper:
                continue
            reapplied_wrappers.append(wrapper)
            if isinstance(wrapper.indicator, prototype):
                reapplied_indicators.append(wrapper.indicator)
            abjad.detach(wrapper, wrapper.component)
        if reapplied_wrappers:
            count = len(reapplied_indicators)
            if count != 1:
                for reapplied_wrapper in reapplied_wrappers:
                    print(reapplied_wrapper)
                message = f'found {count} reapplied indicator(s);'
                message += ' expecting 1.\n\n'
                raise Exception(message)
            return reapplied_indicators[0]

    ### PUBLIC PROPERTIES ###

    @property
    def deactivate(self) -> Optional[bool]:
        r'''Is true when command deactivates tag.
        '''
        return self._deactivate

    @property
    def manifests(self) -> Optional[abjad.OrderedDict]:
        r'''Gets segment-maker manifests.
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
    def offset_to_measure_number(self) -> Optional[abjad.OrderedDict]:
        r'''Gets segment-maker offset-to-measure-number dictionary.
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
    def selector(self) -> Optional[abjad.Expression]:
        r'''Gets selector.
        '''
        return self._selector

    @property
    def tag(self) -> Optional[abjad.Tag]:
        r'''Gets tag.
        '''
        words = [str(_) for _ in self.tags]
        return abjad.Tag.from_words(words)

    @property
    def tag_measure_number(self) -> Optional[bool]:
        r'''Is true when command tags measure number.
        '''
        return self._tag_measure_number

    @tag_measure_number.setter
    def tag_measure_number(self, argument):
        assert argument in (True, False, None), repr(argument)
        self._tag_measure_number = argument
        for command in getattr(self, 'commands', []):
            command._tag_measure_number = argument

    @property
    def tags(self) -> List[abjad.Tag]:
        r'''Gets tags.
        '''
        assert self._are_valid_tags(self._tags)
        return self._tags[:]

    ### PUBLIC METHODS ###

    def get_tag(self, leaf: abjad.Leaf = None) -> Optional[abjad.Tag]:
        r'''Gets tag for `leaf`.
        '''
        tags = self.tags[:]
        if self._tag_measure_number:
            start_offset = abjad.inspect(leaf).get_timespan().start_offset
            measure_number = self._offset_to_measure_number.get(start_offset)
            if measure_number is not None:
                tag = abjad.Tag(f'MEASURE_{measure_number}')
                tags.append(tag)
        if tags:
            words = [str(_) for _ in tags]
            words.sort()
            return abjad.Tag.from_words(words)
        return None
