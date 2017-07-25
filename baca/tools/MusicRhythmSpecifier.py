# -*- coding: utf-8 -*-
import abjad
import baca


class MusicRhythmSpecifier(abjad.abctools.AbjadObject):
    r'''Music rhythm specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.MusicRhythmSpecifier()
            MusicRhythmSpecifier()

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Music'

    __slots__ = (
        '_pattern',
        '_rhythm_maker',
        )

    _publish_storage_format = True

    ### INITIALIZER ###    

    def __init__(
        self,
        pattern=None,
        rhythm_maker=None,
        ):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        self._rhythm_maker = rhythm_maker

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections,
        selections,
        division_masks=None,
        logical_tie_masks=None,
        rest_affix_specifier=None,
        talea_counts=None,
        talea_denominator=None,
        thread=None,
        time_treatments=None,
        tuplet_denominator=None,
        ):
        assert len(selections) == len(collections)
        rhythm_maker = self._get_rhythm_maker(
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            talea_counts=talea_counts,
            talea_denominator=talea_denominator,
            time_treatments=time_treatments,
            tuplet_denominator=tuplet_denominator,
            )
        length = len(selections)
        pattern = self.pattern or abjad.index_all()
        prototype = (abjad.pitchtools.Segment, abjad.pitchtools.Set, list)
        collections_, indices = [], []
        for index, collection in enumerate(collections):
            assert isinstance(collection, prototype), repr(collection)
            if isinstance(collection, (abjad.pitchtools.Set, set)):
                collection_ = list(sorted(collection))[:1]
            else:
                collection_ = collection
            if not pattern.matches_index(index, length):
                continue
            collections_.append(collection_)
            indices.append(index)
        if thread:
            stage_selections, state_manifest = rhythm_maker(
                collections_,
                rest_affix_specifier=rest_affix_specifier,
                )
        else:
            stage_selections = []
            total_collections = len(collections_)
            for collection_index, collection_ in enumerate(collections_):
                stage_selections_, stage_manifest = rhythm_maker(
                    [collection_],
                    rest_affix_specifier=rest_affix_specifier,
                    collection_index=collection_index,
                    total_collections=total_collections,
                    )
                stage_selections.extend(stage_selections_)
        triples = zip(indices, stage_selections, collections)
        for index, stage_selection, collection in triples:
            assert len(stage_selection) == 1, repr(stage_selection)
            if not isinstance(collection, (abjad.pitchtools.Set, set)):
                selections[index] = stage_selection
                continue
            assert len(stage_selection) == 1, repr(stage_selection)
            tuplet = stage_selection[0]
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
            agent = abjad.iterate(stage_selection)
            logical_ties = agent.by_logical_tie(pitched=True)
            logical_ties = list(logical_ties)
            assert len(logical_ties) == 1, repr(stage_selection)
            logical_tie = logical_ties[0]
            for note in logical_tie.leaves:
                assert isinstance(note, abjad.Note), repr(note)
                duration = note.written_duration
                pitches = collection
                chord = abjad.Chord(pitches, duration)
                abjad.mutate(note).replace([chord])
            selections[index] = stage_selection
        return selections

    def _get_rhythm_maker(
        self,
        division_masks=None,
        logical_tie_masks=None,
        talea_counts=None,
        talea_denominator=None,
        time_treatments=None,
        tuplet_denominator=None,
        ):
        rhythm_maker = self.rhythm_maker or self._default_rhythm_maker
        keywords = {}
        if division_masks is not None:
            keywords['division_masks'] = division_masks
        if logical_tie_masks is not None:
            keywords['logical_tie_masks'] = logical_tie_masks
        if talea_counts is not None:
            keywords['talea__counts'] = talea_counts
        if talea_denominator is not None:
            keywords['talea__denominator'] = talea_denominator
        if time_treatments is not None:
            keywords['time_treatments'] = time_treatments
        if keywords:
            rhythm_maker = abjad.new(rhythm_maker, **keywords)
        if tuplet_denominator is not None:
            specifier = rhythm_maker.tuplet_spelling_specifier
            if specifier is None:
                specifier = abjad.rhythmmakertools.TupletSpellingSpecifier()
            specifier = abjad.new(
                specifier,
                preferred_denominator=tuplet_denominator,
                )
            rhythm_maker = abjad.new(
                rhythm_maker,
                tuplet_spelling_specifier=specifier,
                )
        return rhythm_maker

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def rhythm_maker(self):
        r'''Gets rhythm-maker.

        Set to rhythm-maker or none.

        Defaults to none.

        Returns rhythm-maker or music.
        '''
        return self._rhythm_maker
