import abjad
import baca
from .Command import Command


class MetronomeMarkCommand(Command):
    r'''Metronome mark command.

    ..  container:: example

        >>> baca.MetronomeMarkCommand()
        MetronomeMarkCommand(selector=baca.leaf(0), tags=[])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key',
        '_manifest',
        '_site',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate=None,
        key=None,
        selector='baca.leaf(0)', 
        site=None,
        tags=None,
        ):
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if key is not None:
            assert isinstance(key, str)
        self._key = key
        # TODO: set to none instead?
        self._manifest = 'metronome_marks'
        if site is not None:
            assert isinstance(site, str), repr(site)
        self._site = site
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags = tags

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
        reapplied_mark = baca.IndicatorCommand._remove_reapplied_indicator(
            leaf,
            metronome_mark,
            )
        spanner.attach(
            metronome_mark,
            leaf,
            deactivate=self.deactivate,
            site=self.site,
            tag=self.tag,
            )
        if metronome_mark == reapplied_mark:
            score = abjad.inspect(leaf).get_parentage().get_first(abjad.Score)
            baca.SegmentMaker._categorize_persistent_indicator(
                self._manifests,
                score,
                leaf,
                metronome_mark,
                'redundant',
                spanner=spanner,
                )

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
    def site(self):
        r'''Gets site.

        Returns string or none.
        '''
        return self._site
