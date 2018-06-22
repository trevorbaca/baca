import abjad
import baca
import typing
from .Accelerando import Accelerando
from .Ritardando import Ritardando
from .Command import Command
from .Typing import Selector


class MetronomeMarkCommand(Command):
    """
    Metronome mark command.

    ..  container:: example

        >>> baca.MetronomeMarkCommand()
        MetronomeMarkCommand(selector=baca.leaf(0), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key',
        '_redundant',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        key: typing.Union[str, Accelerando, Ritardando] = None,
        redundant: bool = None,
        selector: Selector = 'baca.leaf(0)',
        tags: typing.List[abjad.Tag] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if key is not None:
            assert isinstance(key, (str, Accelerando, Ritardando))
        self._key = key
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant
        tags = tags or []
        assert self._validate_tags(tags), repr(tags)
        self._tags = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        from .SegmentMaker import SegmentMaker
        if argument is None:
            return
        if self.key is None:
            return
        if self.redundant is True:
            return
        if isinstance(self.key, str) and self.manifests is not None:
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
        spanner = abjad.inspect(leaf).get_spanner(baca.MetronomeMarkSpanner)
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
            SegmentMaker._treat_persistent_wrapper(
                self.manifests,
                wrapper,
                'redundant',
                )

    ### PUBLIC PROPERTIES ###

    @property
    def key(self) -> typing.Optional[
            typing.Union[str, Accelerando, Ritardando]
            ]:
        """
        Gets metronome mark key.
        """
        return self._key

    @property
    def redundant(self) -> typing.Optional[bool]:
        """
        Is true when command is redundant.
        """
        return self._redundant
