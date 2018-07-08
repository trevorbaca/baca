import abjad
import baca
import typing
from . import indicatorlib
from . import typings
from .Command import Command


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
        key: typing.Union[
            str,
            indicatorlib.Accelerando,
            indicatorlib.Ritardando] = None,
        redundant: bool = None,
        selector: typings.Selector = 'baca.leaf(0)',
        tags: typing.List[abjad.Tag] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        prototype = (str, indicatorlib.Accelerando, indicatorlib.Ritardando)
        if key is not None:
            assert isinstance(key, prototype), repr(key)
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
        if isinstance(self.key, str) and self.runtime['manifests'] is not None:
            metronome_marks = self.runtime['manifests']['abjad.MetronomeMark']
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
        reapplied = self._remove_reapplied_wrappers(leaf, indicator)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            wrapper=True,
            )
        if indicator == reapplied:
            SegmentMaker._treat_persistent_wrapper(
                self.runtime['manifests'],
                wrapper,
                'redundant',
                )

    ### PUBLIC PROPERTIES ###

    @property
    def key(self) -> typing.Optional[typing.Union[str,
    indicatorlib.Accelerando, indicatorlib.Ritardando]]:
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
