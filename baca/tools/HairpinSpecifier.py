# -*- coding: utf-8 -*-
import abjad
import baca


class HairpinSpecifier(abjad.abctools.AbjadObject):
    r'''Hairpin specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Attaches hairpins to nontrivial ties:

        ::

            >>> specifier = baca.tools.HairpinSpecifier(
            ...     hairpin_tokens=['f > niente', 'niente < f'],
            ...     span='nontrivial ties',
            ...     )
            >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
            >>> staff = abjad.Staff(string)
            >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
            >>> logical_ties = list(logical_ties)
            >>> specifier(logical_ties)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \once \override Hairpin.circled-tip = ##t
                c'4 ~ \> \f
                c'4 ~
                c'4 \!
                r4
                \once \override Hairpin.circled-tip = ##t
                d'4 ~ \<
                d'4 ~
                d'4 \f
                r4
            }

    ..  container:: example

        Gets storage format of specifier:

        ::

            >>> f(specifier)
            baca.tools.HairpinSpecifier(
                hairpin_tokens=datastructuretools.CyclicTuple(
                    [
                        ('f', '>', 'niente'),
                        ('niente', '<', 'f'),
                        ]
                    ),
                span='nontrivial ties',
                )

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_enchain_hairpins',
        '_flare',
        '_hairpin_tokens',
        '_include_following_rests',
        '_minimum_duration',
        '_omit_lone_note_dynamic',
        '_pattern',
        '_span',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        enchain_hairpins=None,
        flare=None,
        hairpin_tokens=None,
        include_following_rests=None,
        minimum_duration=None,
        omit_lone_note_dynamic=None,
        pattern=None,
        span='contiguous notes and chords',
        ):
        if enchain_hairpins is not None:
            enchain_hairpins = bool(enchain_hairpins)
        self._enchain_hairpins = enchain_hairpins
        self._flare = flare
        hairpin_tokens = hairpin_tokens or []
        prototype = (list, tuple, abjad.CyclicTuple, abjad.Sequence,)
        assert isinstance(hairpin_tokens, prototype), repr(hairpin_tokens)
        tokens = []
        for element in hairpin_tokens:
            if isinstance(element, str):
                element = tuple(element.split())
                if not abjad.spannertools.Hairpin._is_hairpin_token(element):
                    message = 'must be valid hairpin token: {!r}.'
                    message = message.format(element)
                    raise Exception(message)
            tokens.append(element)
        hairpin_tokens = tokens
        hairpin_tokens = abjad.datastructuretools.CyclicTuple(hairpin_tokens)
        self._hairpin_tokens = hairpin_tokens
        if include_following_rests is not None:
            include_following_rests = bool(include_following_rests)
        self._include_following_rests = include_following_rests
        if minimum_duration is not None:
            minimum_duration = abjad.durationtools.Duration(minimum_duration)
        self._minimum_duration = minimum_duration
        if omit_lone_note_dynamic is not None:
            omit_lone_note_dynamic = bool(omit_lone_note_dynamic)
        self._omit_lone_note_dynamic = omit_lone_note_dynamic
        if pattern is not None:
            prototype = (abjad.Pattern, abjad.patterntools.CompoundPattern)
            assert isinstance(pattern, prototype), repr(prototype)
        self._pattern = pattern
        strings = (
            'contiguous notes and chords',
            'nontrivial ties',
            )
        if span not in strings:
            assert isinstance(span, (tuple, list)), repr(span)
        self._span = span

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls hairpin specifier on `logical_ties`.

        Passes silently when `logical_ties` is empty.

        Returns none.
        '''
        if not logical_ties:
            return
        if not isinstance(logical_ties[0], abjad.selectiontools.LogicalTie):
            assert isinstance(logical_ties[0], abjad.scoretools.Leaf)
            logical_ties = [
                abjad.selectiontools.LogicalTie(_) for _ in logical_ties]
        if (self.span == 'contiguous notes and chords'
            or isinstance(self.span, (tuple, list))):
            groups = self._group_contiguous_logical_ties(logical_ties)
        elif self.span == 'nontrivial ties':
            groups = [[_] for _ in logical_ties]
        else:
            raise ValueError(self.span)
        if isinstance(self.span, (tuple, list)):
            if not self.enchain_hairpins:
                groups = self._partition_groups(groups)
            else:
                groups = self._partition_enchained_groups(groups)
        hairpin_tokens = self.hairpin_tokens
        for group_index, group in enumerate(groups):
            notes = []
            for logical_tie in group:
                for note in logical_tie:
                    notes.append(note)
            if len(notes) == 0:
                continue
            total_notes = len(notes)
            notes_to_span = []
            pattern = self.pattern or abjad.select_all()
            notes_to_span = pattern.get_matching_items(notes)
            notes_to_span = list(notes_to_span)
            if not notes_to_span:
                continue
            if self.include_following_rests:
                last_note = notes_to_span[-1]
                next_leaf = abjad.inspect_(last_note).get_leaf(1)
                prototype = (
                    abjad.scoretools.Rest,
                    abjad.scoretools.MultimeasureRest,
                    )
                if isinstance(next_leaf, prototype):
                    notes_to_span.append(next_leaf)
            if len(notes_to_span) == 1 and self.omit_lone_note_dynamic:
                continue
            if len(notes_to_span) == 1 and not self.omit_lone_note_dynamic:
                hairpin_token = hairpin_tokens[group_index]
                start_dynamic = hairpin_token[0]
                if start_dynamic == 'niente':
                    message = 'can not attach niente dynamics to components.'
                    raise Exception(message)
                dynamic = abjad.indicatortools.Dynamic(start_dynamic)
                abjad.attach(dynamic, notes[0])
                continue
            hairpin_token = hairpin_tokens[group_index]
            if hairpin_token is None:
                continue
            if isinstance(hairpin_token, tuple):
                descriptor = ' '.join([_ for _ in hairpin_token if _])
                include_rests = bool(self.include_following_rests)
                hairpin = abjad.spannertools.Hairpin(
                    descriptor=descriptor,
                    include_rests=include_rests,
                    )
                abjad.attach(hairpin, notes_to_span)
            # hook to allow callable custom classes like SwellSpecifier
            else:
                hairpin_token(notes_to_span)
            if self.flare:
                first_note = notes_to_span[0]
                prototype = abjad.scoretools.Note
                assert isinstance(first_note, prototype), repr(first_note)
                stencil = abjad.schemetools.Scheme('flared-hairpin')
                abjad.override(first_note).hairpin.stencil = stencil

    ### PRIVATE METHODS ###

    def _group_contiguous_logical_ties(self, logical_ties):
        result = []
        current_group = [logical_ties[0]]
        for logical_tie in logical_ties[1:]:
            last_timespan = current_group[-1].get_timespan()
            current_timespan = logical_tie.get_timespan()
            if last_timespan.stops_when_timespan_starts(current_timespan):
                current_group.append(logical_tie)
            else:
                result.append(current_group)
                current_group = [logical_tie]
        if current_group:
            result.append(current_group)
        return result

    def _partition_by_enchained_counts(self, leaves, counts):
        assert isinstance(leaves, list), repr(leaves)
        counts = abjad.datastructuretools.CyclicTuple(counts)
        shards = []
        shard_index = 0
        leaf_start_index = 0
        total_leaves = len(leaves)
        while True:
            current_count = counts[shard_index]
            leaf_stop_index = leaf_start_index + current_count
            shard = leaves[leaf_start_index:leaf_stop_index]
            shards.append(shard)
            shard_index += 1
            leaf_start_index = leaf_stop_index - 1
            if total_leaves <= leaf_stop_index:
                break
        return shards

    def _partition_enchained_groups(self, groups):
        new_groups = []
        for group in groups:
            leaves = abjad.iterate(group).by_leaf()
            leaves = list(leaves)
            shards = self._partition_by_enchained_counts(
                leaves,
                counts=self.span,
                )
            new_groups.extend(shards)
        new_groups = [[_] for _ in new_groups]
        return new_groups

    def _partition_groups(self, groups):
        new_groups = []
        for group in groups:
            leaves = abjad.iterate(group).by_leaf()
            leaves = list(leaves)
            shards = baca.Sequence(leaves).partition_by_counts(
                counts=self.span,
                cyclic=True,
                )
            new_groups.extend(shards)
        groups = new_groups
        groups = [[_] for _ in groups]
        return groups

    ### PUBLIC PROPERTIES ###

    @property
    def enchain_hairpins(self):
        r'''Is true when hairpins enchain. Otherwise false.

        ..  container:: example

            Spans groups of notes and chords:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['p < f', 'f > p'],
                ...     span=[3, 2],
                ...     )
                >>> string = "c'8 ~ c' ~ c' ~ c' ~ c' ~ c' ~ c' ~ c'"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ~ \< \p
                    c'8 ~
                    c'8 ~ \f
                    c'8 ~ \> \f
                    c'8 ~ \p
                    c'8 ~ \< \p
                    c'8 ~
                    c'8 \f
                }

        ..  container:: example

            Spans enchained groups of notes and chords:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > p'],
                ...     span=[3, 2],
                ...     )
                >>> string = "c'8 ~ c' ~ c' ~ c' ~ c' ~ c' ~ c' ~ c'"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ~ \< \p
                    c'8 ~
                    c'8 ~ \f \> \f
                    c'8 ~ \p \< \p
                    c'8 ~
                    c'8 ~ \f \> \f
                    c'8 ~ \p \< \p
                    c'8 \f
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._enchain_hairpins

    @property
    def flare(self):
        r'''Is true when hairpins are flared. Otherwise false.

        ..  container:: example

            Does not flare hairpins:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['f > p', 'p < f'],
                ...     span='nontrivial ties',
                ...     )
                >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \> \f
                    c'4 ~
                    c'4 \p
                    r4
                    d'4 ~ \< \p
                    d'4 ~
                    d'4 \f
                    r4
                }
                
        ..  container:: example

            Does flare hairpins:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     flare=True,
                ...     hairpin_tokens=['f > p', 'p < f'],
                ...     span='nontrivial ties',
                ...     )
                >>> string = "c'4 ~ c' ~ c' r4 d'4 ~ d' ~ d' r4"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \once \override Hairpin.stencil = #flared-hairpin
                    c'4 ~ \> \f
                    c'4 ~
                    c'4 \p
                    r4
                    \once \override Hairpin.stencil = #flared-hairpin
                    d'4 ~ \< \p
                    d'4 ~
                    d'4 \f
                    r4
                }

            Note that a LilyPond bug currently prevents flared hairpins from
            working correctly with circled-tip hairpins.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._flare

    @property
    def hairpin_tokens(self):
        r'''Gets hairpin tokens of specifier.

        ..  container:: example

            Spans notes and chords in repeating groups of 4:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['p < f'],
                ...     span=[4],
                ...     )
                >>> string = "c'16 d' e' f' ~ f' e' d' c' ~ c' d' e' f' ~ f' e' d' c'"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'16 \< \p
                    d'16
                    e'16
                    f'16 ~ \f
                    f'16 \< \p
                    e'16
                    d'16
                    c'16 ~ \f
                    c'16 \< \p
                    d'16
                    e'16
                    f'16 ~ \f
                    f'16 \< \p
                    e'16
                    d'16
                    c'16 \f
                }

        ..  container:: example

            Omits every other group:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=[None, 'p < f'],
                ...     span=[4],
                ...     )
                >>> string = "c'16 d' e' f' ~ f' e' d' c' ~ c' d' e' f' ~ f' e' d' c'"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'16
                    d'16
                    e'16
                    f'16 ~
                    f'16 \< \p
                    e'16
                    d'16
                    c'16 ~ \f
                    c'16
                    d'16
                    e'16
                    f'16 ~
                    f'16 \< \p
                    e'16
                    d'16
                    c'16 \f
                }

        Hairpin token defined equal to triple like ``('f', '>', 'p')``,
        string like ``'f > p'`` or none.

        Set to haipin token, list of hairpin tokens or none.

        Returns cyclic tuple.
        '''
        return self._hairpin_tokens

    @property
    def include_following_rests(self):
        r'''Is true if every hairpin extends to include rests
        following the last note or chord in each hairpin. Otherwise false.

        ..  container:: example

            Does not include following rests:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > niente'],
                ...     span=[2, 3],
                ...     )
                >>> string = "c'8 ~ c' ~ c' r c' ~ c' ~ c' r"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ~ \< \p
                    \once \override Hairpin.circled-tip = ##t
                    c'8 ~ \f \> \f
                    c'8 \!
                    r8
                    c'8 ~ \< \p
                    \once \override Hairpin.circled-tip = ##t
                    c'8 ~ \f \> \f
                    c'8 \!
                    r8
                }

        ..  container:: example

            Includes following rests:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > niente'],
                ...     include_following_rests=True,
                ...     span=[2, 3],
                ...     )
                >>> string = "c'8 ~ c' ~ c' r c' ~ c' ~ c' r"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ~ \< \p
                    \once \override Hairpin.circled-tip = ##t
                    c'8 ~ \f \> \f
                    c'8
                    r8 \!
                    c'8 ~ \< \p
                    \once \override Hairpin.circled-tip = ##t
                    c'8 ~ \f \> \f
                    c'8
                    r8 \!
                }

        ..  container:: example

            Includes following multimeasure rests:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     enchain_hairpins=True,
                ...     hairpin_tokens=['p < f', 'f > niente'],
                ...     include_following_rests=True,
                ...     span=[2, 3],
                ...     )
                >>> string = "c'8 ~ c' ~ c' r c' ~ c' ~ c' ~ c' R1"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ~ \< \p
                    \once \override Hairpin.circled-tip = ##t
                    c'8 ~ \f \> \f
                    c'8
                    r8 \!
                    c'8 ~ \< \p
                    \once \override Hairpin.circled-tip = ##t
                    c'8 ~ \f \> \f
                    c'8 ~
                    c'8
                    R1 \!
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._include_following_rests

    @property
    def minimum_duration(self):
        r'''Gets minimum duration of specifier.

        Returns duration or none.
        '''
        return self._minimum_duration

    @property
    def omit_lone_note_dynamic(self):
        r'''Is true when start dynamic of hairpin does not attach to lone
        notes. Otherwise false.

        ..  container:: example

            Does not omit lone note dynamic:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['ppp < p'],
                ...     span='nontrivial ties',
                ...     )
                >>> staff = abjad.Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4 \ppp
                    g'4 \ppp
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        ..  container:: example

            Omits lone note dynamic:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['ppp < p'],
                ...     omit_lone_note_dynamic=True,
                ...     span='nontrivial ties',
                ...     )
                >>> staff = abjad.Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4
                    g'4
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._omit_lone_note_dynamic

    @property
    def pattern(self):
        r'''Gets pattern.

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def span(self):
        r'''Gets span of specifier.
        
        ..  container:: example

            Spans contiguous notes and chords:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['ppp < p'],
                ...     span='contiguous notes and chords',
                ...     )
                >>> staff = abjad.Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8
                    d'8 ~
                    d'4 \p
                    r4
                    e'4 \< \ppp
                    g'4
                    fs'4 ~
                    fs'4 \p
                }

        ..  container:: example

            Spans nontrivial ties:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['ppp < p'],
                ...     omit_lone_note_dynamic=True,
                ...     span='nontrivial ties',
                ...     )
                >>> staff = abjad.Staff("c'4 ~ c'8 d'8 ~ d'4 r4 e'4 g'4 fs'4 ~ fs'4")
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~ \< \ppp
                    c'8 \p
                    d'8 ~ \< \ppp
                    d'4 \p
                    r4
                    e'4
                    g'4
                    fs'4 ~ \< \ppp
                    fs'4 \p
                }

        ..  container:: example

            Spans notes and chords grouped in repeating groups of 3 and 4:

            ::

                >>> specifier = baca.tools.HairpinSpecifier(
                ...     hairpin_tokens=['p < f'],
                ...     span=[3, 4],
                ...     )
                >>> string = "c'16 d' ~ d' e' c' d' ~ d' e' c' d' ~ d' e' c'8 e'8"
                >>> staff = abjad.Staff(string)
                >>> logical_ties = abjad.iterate(staff).by_logical_tie(pitched=True)
                >>> logical_ties = list(logical_ties)
                >>> specifier(logical_ties)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'16 \< \p
                    d'16 ~
                    d'16 \f
                    e'16 \< \p
                    c'16
                    d'16 ~
                    d'16 \f
                    e'16 \< \p
                    c'16
                    d'16 ~ \f
                    d'16 \< \p
                    e'16
                    c'8
                    e'8 \f
                }

        Defaults to ``'contiguous notes and chords'``.

        Set to ``'contiguous notes and chords'``, ``'nontrivial ties'`` or
        an iterable of positive integers.

        Returns ``'contiguous notes and chords'``, ``'nontrivial ties'`` or
        an iterable of positive integers.
        '''
        return self._span
