import abjad
import baca
from .Command import Command


class MetronomeMarkCommand(Command):
    r'''Metronome mark command.

    ..  container:: example

        >>> baca.MetronomeMarkCommand()
        MetronomeMarkCommand(selector=baca.leaf(0))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key',
        '_manifest',
        '_tag',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        key=None,
        selector='baca.leaf(0)', 
        tag=None,
        ):
        Command.__init__(self, selector=selector)
        if key is not None:
            assert isinstance(key, str)
        self._key = key
        self._manifest = 'metronome_marks'
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Applies command to result of selector called on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.key is None:
            return
        metronome_mark = self.manifest.get(self.key)
        if metronome_mark is None:
            raise Exception(f'can not find metronome mark {key!r}.')
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = baca.select(argument).leaf(0)
        spanner = abjad.inspect(leaf).get_spanner(abjad.MetronomeMarkSpanner)
        if spanner is None:
            raise Exception('can not find metronome mark spanner.')
        spanner.attach(metronome_mark, leaf, tag=self.tag)

    ### PUBLIC PROPERTIES ###

    @property
    def key(self):
        r'''Gets metronome mark key.

        Returns string or none.
        '''
        return self._key

    @property
    def manifest(self):
        r'''Gets metronome mark manifest.

        Populated by segment-maker at command wrap-time.

        Returns ordered dictionary.
        '''
        return self._manifest

    @property
    def tag(self):
        r'''Gets tag.

        Returns string or none.
        '''
        return self._tag
