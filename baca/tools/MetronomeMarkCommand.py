import abjad
import baca
from .Command import Command
from .Typing import List
from .Typing import Optional
from .Typing import Selector
from .Typing import Union


class MetronomeMarkCommand(Command):
    r'''Metronome mark command.

    ..  container:: example

        >>> baca.MetronomeMarkCommand()
        MetronomeMarkCommand(selector=baca.leaf(0), tags=[])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate: bool = None,
        key: Union[str, abjad.Accelerando, abjad.Ritardando] = None,
        selector: Selector = 'baca.leaf(0)',
        tags: List[abjad.Tag] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if key is not None:
            assert isinstance(key, (str, abjad.Accelerando, abjad.Ritardando))
        self._key = key
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        r'''Applies command to result of selector called on `argument`.
        '''
        from baca.tools.SegmentMaker import SegmentMaker
        if argument is None:
            return
        if self.key is None:
            return
        if isinstance(self.key, str):
            metronome_marks = self.manifests['abjad.MetronomeMark']
            indicator = metronome_marks.get(self.key)
            if indicator is None:
                raise Exception(f'can not find metronome mark {self.key!r}.')
        else:
            indicator = self.key
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = baca.select(argument).leaf(0)
        spanner = abjad.inspect(leaf).get_spanner(abjad.MetronomeMarkSpanner)
        if spanner is None:
            raise Exception('can not find metronome mark spanner.')
        reapplied = self._remove_reapplied_wrappers(leaf, indicator)
        wrapper = spanner.attach(
            indicator,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            wrapper=True,
            )
        if indicator == reapplied:
            SegmentMaker._categorize_persistent_wrapper(
                self.manifests,
                wrapper,
                'redundant',
                )

    ### PUBLIC PROPERTIES ###

    @property
    def key(self) -> Optional[Union[str, abjad.Accelerando, abjad.Ritardando]]:
        r'''Gets metronome mark key.
        '''
        return self._key
