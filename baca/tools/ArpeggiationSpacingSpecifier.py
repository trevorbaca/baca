import abjad
import baca


class ArpeggiationSpacingSpecifier(abjad.AbjadValueObject):
    r'''Arpeggiation spacing specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> specifier = baca.ArpeggiationSpacingSpecifier()
            >>> specifier([[6, 0, 4, 5, 8]])
            CollectionList([<6, 12, 16, 17, 20>])

    ..  container:: example

        ::

            >>> specifier = baca.ArpeggiationSpacingSpecifier()
            >>> specifier([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
            CollectionList([<0, 2, 10>, <6, 16, 27, 32, 43>, <9>])

    ..  container:: example

        ::

            >>> baca.ArpeggiationSpacingSpecifier()
            ArpeggiationSpacingSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_direction',
        '_pattern',
        '_selector',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, direction=None, pattern=None, selector=None):
        if direction is not None:
            assert direction in (Up, Down), repr(direction)
        self._direction = direction
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, collections=None):
        r'''Calls specifier on `collections`.

        ..  container:: example

            ::

                >>> specifier = baca.ArpeggiationSpacingSpecifier()
                >>> specifier([])
                PitchSegment([])

        ..  container:: example

            ::

                >>> specifier = baca.ArpeggiationSpacingSpecifier()
                >>> specifier() is None
                True

        Returns collection list or none.
        '''
        if collections is None:
            return
        if collections == []:
            return baca.PitchSegment(item_class=abjad.NumberedPitch)
        if not isinstance(collections, baca.CollectionList):
            collections = baca.CollectionList(collections)
        pitch_class_collections = collections.to_pitch_classes()
        pattern = self.pattern or abjad.index_all()
        collections_ = []
        total_length = len(collections)
        class_ = baca.ChordalSpacingSpecifier
        direction = self.direction or Up
        for i in range(total_length):
            if pattern.matches_index(i, total_length):
                pitch_class_collection = pitch_class_collections[i]
                if isinstance(pitch_class_collection, abjad.Set):
                    pitch_classes = list(sorted(pitch_class_collection))
                else:
                    pitch_classes = list(pitch_class_collection)
                if direction is Up:
                    pitches = class_._to_tightly_spaced_pitches_ascending(
                        pitch_classes,
                        )
                else:
                    pitches = class_._to_tightly_spaced_pitches_descending(
                        pitch_classes,
                        )
                if isinstance(pitch_class_collection, abjad.Set):
                    collection_ = baca.PitchSet(items=pitches)
                else:
                    collection_ = baca.PitchSegment(items=pitches)
                collections_.append(collection_)
            else:
                collections_.append(collections[i])
        return baca.CollectionList(collections_)

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r"""Gets direction.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     collections,
                ...     baca.ArpeggiationSpacingSpecifier(
                ...         direction=Up,
                ...         ),
                ...     baca.RegisterToOctaveCommand(octave_number=2),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c,16 [
                                d,16
                                bf,16 ]
                            }
                            {
                                fs,16 [
                                e16
                                ef'16
                                af'16
                                g''16 ]
                            }
                            {
                                a,16
                            }
                        }
                    }
                >>

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     collections,
                ...     baca.ArpeggiationSpacingSpecifier(
                ...         direction=Down,
                ...         ),
                ...     baca.RegisterToOctaveCommand(octave_number=2),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d16
                                bf,16 ]
                            }
                            {
                                fs16 [
                                e16
                                ef16
                                af,16
                                g,16 ]
                            }
                            {
                                a,16
                            }
                        }
                    }
                >>

        Set to up, down or none.

        Returns up, down or none.
        """
        return self._direction

    @property
    def pattern(self):
        r'''Gets pattern.

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def selector(self):
        r'''Gets selector.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
