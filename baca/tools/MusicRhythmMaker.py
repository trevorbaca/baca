import abjad
import baca
import collections
import math


class MusicRhythmMaker(abjad.rhythmmakertools.RhythmMaker):
    r'''Music rhythm-maker.

    ::

        >>> import baca

    ..  container:: example

        Sixteenths and eighths:

        ::

            >>> rhythm_maker = baca.MusicRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10, 8]]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff {
                {
                    \time 5/16
                    {
                        c'16 [
                        d'16
                        bf'8
                        af'16 ]
                    }
                }
            }

        ::

            >>> collections = [[18, 16, 15, 20, 19]]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff {
                {
                    \time 3/8
                    {
                        fs''16 [
                        e''16
                        ef''8
                        af''16
                        g''16 ]
                    }
                }
            }

        ::

            >>> collections = [[9]]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff {
                {
                    \time 1/16
                    {
                        a'16
                    }
                }
            }

        ::

            >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff {
                {
                    \time 13/16
                    {
                        c'16 [
                        d'16
                        bf'8
                        af'16 ]
                    }
                    {
                        fs''16 [
                        e''8
                        ef''16
                        af''16
                        g''8 ]
                    }
                    {
                        a'16
                    }
                }
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Music'

    __slots__ = (
        '_acciaccatura_specifiers',
        '_next_attack',
        '_next_segment',
        '_state_manifest',
        '_talea',
        '_time_treatments',
        )

    _state_variables = (
        '_next_attack',
        '_next_segment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        acciaccatura_specifiers=None,
        beam_specifier=None,
        division_masks=None,
        duration_specifier=None,
        logical_tie_masks=None,
        talea=None,
        tie_specifier=None,
        time_treatments=None,
        tuplet_specifier=None,
        ):
        abjad.rhythmmakertools.RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_specifier=duration_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        if acciaccatura_specifiers is not None:
            prototype = baca.AcciaccaturaSpecifier
            for acciaccatura_specifier in acciaccatura_specifiers:
                assert isinstance(acciaccatura_specifier, prototype)
        self._acciaccatura_specifiers = acciaccatura_specifiers
        self._next_attack = 0
        self._next_segment = 0
        self._state_manifest = collections.OrderedDict()
        talea = talea or abjad.rhythmmakertools.Talea()
        if not isinstance(talea, abjad.rhythmmakertools.Talea):
            message = 'must be talea: {!r}.'
            message = message.format(talea)
            raise TypeError(message)
        self._talea = talea
        if time_treatments is not None:
            for time_treatment in time_treatments:
                if not self._is_time_treatment(time_treatment):
                    message = 'invalid time treatment: {!r}.'
                    message = message.format(time_treatment)
                    raise Exception(message)
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections,
        rest_affix_specifier=None,
        collection_index=None,
        state_manifest=None,
        total_collections=None,
        ):
        r'''Calls rhythm-maker on `collections`.

        ..  container:: example

            Without state manifest:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        {
                            a'8
                        }
                    }
                }

            ::

                >>> rhythm_maker._print_state_manifest()
                _next_attack: 9
                _next_segment: 3

        ..  container:: example

            With state manifest:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> state_manifest = {'_next_attack': 2}
                >>> selections, state_manifest = rhythm_maker(
                ...     collections,
                ...     state_manifest=state_manifest,
                ...     )
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'8 [
                            d'16
                            bf'16 ]
                        }
                        {
                            fs''8 [
                            e''16
                            ef''16
                            af''8
                            g''16 ]
                        }
                        {
                            a'16
                        }
                    }
                }

            ::

                >>> rhythm_maker._print_state_manifest()
                _next_attack: 11
                _next_segment: 3


        Returns selections together with state manifest.
        '''
        self._apply_state_manifest(state_manifest)
        selections = self._make_music(
            collections,
            rest_affix_specifier=rest_affix_specifier,
            collection_index=collection_index,
            total_collections=total_collections,
            )
        selections = self._apply_specifiers(selections)
        self._check_well_formedness(selections)
        state_manifest = self._make_state_manifest()
        return selections, state_manifest

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_rest_affixes(
        leaves,
        talea,
        rest_prefix,
        rest_suffix,
        affix_skips_instead_of_rests,
        decrease_durations,
        ):
        if rest_prefix:
            durations = [(_, talea.denominator) for _ in rest_prefix]
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            leaves_ = maker([None], durations)
            leaves[0:0] = leaves_
        if rest_suffix:
            durations = [(_, talea.denominator) for _ in rest_suffix]
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            leaves_ = maker([None], durations)
            leaves.extend(leaves_)
        return leaves

    def _apply_state_manifest(self, state_manifest=None):
        for name in self._state_variables:
            value = setattr(self, name, 0)
        state_manifest = state_manifest or {}
        assert isinstance(state_manifest, dict), repr(state_manifest)
        for key in state_manifest:
            value = state_manifest[key]
            setattr(self, key, value)

    @staticmethod
    def _fix_rounding_error(durations, total_duration):
        current_duration = sum(durations)
        if current_duration < total_duration:
            missing_duration = total_duration - current_duration
            if durations[0] < durations[-1]:
                durations[-1] += missing_duration
            else:
                durations[0] += missing_duration
        elif sum(durations) == total_duration:
            return durations
        elif total_duration < current_duration:
            extra_duration = current_duration - total_duration
            if durations[0] < durations[-1]:
                durations[-1] -= extra_duration
            else:
                durations[0] -= extra_duration
        assert sum(durations) == total_duration
        return durations

    def _get_acciaccatura_specifier(self, collection_index, total_collections):
        if not self.acciaccatura_specifiers:
            return
        for acciaccatura_specifier in self.acciaccatura_specifiers:
            pattern = acciaccatura_specifier._get_pattern()
            if pattern.matches_index(collection_index, total_collections):
                return acciaccatura_specifier

    def _get_talea(self):
        if self.talea is not None:
            return self.talea
        return abjad.rhythmmakertools.Talea()

    def _get_time_treatments(self):
        if not self.time_treatments:
            return abjad.CyclicTuple([0])
        return abjad.CyclicTuple(self.time_treatments)

    @staticmethod
    def _is_time_treatment(argument):
        if argument is None:
            return True
        elif isinstance(argument, int):
            return True
        elif isinstance(argument, str):
            return True
        elif isinstance(argument, abjad.Ratio):
            return True
        elif isinstance(argument, abjad.Multiplier):
            return True
        elif argument.__class__ is abjad.Duration:
            return True
        elif argument in ('accel', 'rit'):
            return True
        return False

    @classmethod
    def _make_accelerando(class_, leaf_selection, accelerando_indicator):
        assert accelerando_indicator in ('accel', 'rit')
        tuplet = abjad.Tuplet((1, 1), leaf_selection)
        if len(tuplet) == 1:
            return tuplet
        durations = [abjad.inspect(_).get_duration() for _ in leaf_selection]
        if accelerando_indicator == 'accel':
            exponent = 0.625
        elif accelerando_indicator == 'rit':
            exponent = 1.625
        multipliers = class_._make_accelerando_multipliers(durations, exponent)
        assert len(leaf_selection) == len(multipliers)
        for multiplier, leaf in zip(multipliers, leaf_selection):
            abjad.attach(multiplier, leaf)
        rhythm_maker_class = abjad.rhythmmakertools.AccelerandoRhythmMaker
        if rhythm_maker_class._is_accelerando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Right
        elif rhythm_maker_class._is_ritardando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Left
        tuplet.force_times_command = True
        duration = abjad.inspect(tuplet).get_duration()
        duration = abjad.Duration(duration)
        markup = duration.to_score_markup()
        markup = markup.scale((0.75, 0.75))
        abjad.override(tuplet).tuplet_number.text = markup
        return tuplet

    @classmethod
    def _make_accelerando_multipliers(class_, durations, exponent):
        r'''Makes accelerando multipliers.

        ..  container:: example

            Set exponent less than 1 for decreasing durations:

            ::

                >>> class_ = baca.MusicRhythmMaker
                >>> durations = 4 * [abjad.Duration(1)]
                >>> result = class_._make_accelerando_multipliers(
                ...     durations,
                ...     0.5,
                ...     )
                >>> for multiplier in result: multiplier
                ...
                NonreducedFraction(2048, 1024)
                NonreducedFraction(848, 1024)
                NonreducedFraction(651, 1024)
                NonreducedFraction(549, 1024)

        ..  container:: example

            Set exponent to 1 for trivial multipliers:

            ::

                >>> class_ = baca.MusicRhythmMaker
                >>> durations = 4 * [abjad.Duration(1)]
                >>> result = class_._make_accelerando_multipliers(durations, 1)
                >>> for multiplier in result: multiplier
                ...
                NonreducedFraction(1024, 1024)
                NonreducedFraction(1024, 1024)
                NonreducedFraction(1024, 1024)
                NonreducedFraction(1024, 1024)

        ..  container:: example

            Set exponent greater than 1 for increasing durations:

            ::

                >>> class_ = baca.MusicRhythmMaker
                >>> durations = 4 * [abjad.Duration(1)]
                >>> result = class_._make_accelerando_multipliers(
                ...     durations,
                ...     0.5,
                ...     )
                >>> for multiplier in result: multiplier
                ...
                NonreducedFraction(2048, 1024)
                NonreducedFraction(848, 1024)
                NonreducedFraction(651, 1024)
                NonreducedFraction(549, 1024)

        Set exponent greater than 1 for ritardando.

        Set exponent less than 1 for accelerando.
        '''
        pairs = abjad.mathtools.cumulative_sums_pairwise(durations)
        total_duration = pairs[-1][-1]
        start_offsets = [_[0] for _ in pairs]
        #print(total_duration, start_offsets)
        start_offsets = [_ / total_duration for _ in start_offsets]
        #print(total_duration, start_offsets)
        start_offsets_ = []
        rhythm_maker_class = abjad.rhythmmakertools.AccelerandoRhythmMaker
        for start_offset in start_offsets:
            start_offset_ = rhythm_maker_class._interpolate_exponential(
                0,
                total_duration,
                start_offset,
                exponent,
                )
            start_offsets_.append(start_offset_)
        #print(start_offsets_)
        #start_offsets_ = [float(total_duration * _) for _ in start_offsets_]
        start_offsets_.append(float(total_duration))
        durations_ = abjad.mathtools.difference_series(start_offsets_)
        durations_ = rhythm_maker_class._round_durations(durations_, 2**10)
        durations_ = class_._fix_rounding_error(durations_, total_duration)
        multipliers = []
        assert len(durations) == len(durations_)
        for duration_, duration in zip(durations_, durations):
            multiplier = duration_ / duration
            multiplier = abjad.Multiplier(multiplier)
            multiplier = multiplier.with_denominator(2**10)
            multipliers.append(multiplier)
        return multipliers

    def _make_music(
        self,
        collections,
        rest_affix_specifier=None,
        collection_index=None,
        total_collections=None,
        ):
        segment_count = len(collections)
        selections = []
        if collection_index is None:
            for i, segment in enumerate(collections):
                if rest_affix_specifier is not None:
                    result = rest_affix_specifier(i, segment_count)
                    rest_prefix, rest_suffix = result
                    affix_skips_instead_of_rests = \
                        rest_affix_specifier.skips_instead_of_rests
                else:
                    rest_prefix, rest_suffix = None, None
                    affix_skips_instead_of_rests = None
                selection = self._make_selection(
                    segment,
                    segment_count,
                    rest_prefix=rest_prefix,
                    rest_suffix=rest_suffix,
                    affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                    )
                selections.append(selection)
        else:
            assert len(collections) == 1, repr(collections)
            segment = collections[0]
            if rest_affix_specifier is not None:
                result = rest_affix_specifier(collection_index, total_collections)
                rest_prefix, rest_suffix = result
                affix_skips_instead_of_rests = \
                    rest_affix_specifier.skips_instead_of_rests
            else:
                rest_prefix, rest_suffix = None, None
                affix_skips_instead_of_rests = None
            selection = self._make_selection(
                segment,
                segment_count,
                rest_prefix=rest_prefix,
                rest_suffix=rest_suffix,
                affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        selections = self._apply_division_masks(selections)
        specifier = self._get_duration_specifier()
        if specifier.rewrite_meter:
            #selections = specifier._rewrite_meter_(
            #    selections,
            #    input_divisions,
            #    )
            raise NotImplementedError()
        return selections

    def _make_selection(
        self,
        segment,
        segment_count,
        rest_prefix=None,
        rest_suffix=None,
        affix_skips_instead_of_rests=None,
        ):
        collection_index = self._next_segment
        acciaccatura_specifier = self._get_acciaccatura_specifier(
            collection_index,
            segment_count,
            )
        self._next_segment += 1
        if not segment:
            return abjad.Selection()
        talea = self._get_talea()
        leaves = []
        specifier = self._get_duration_specifier()
        decrease_durations = specifier.decrease_monotonic
        current_selection = self._next_segment - 1
        time_treatment = self._get_time_treatments()[current_selection]
        if time_treatment is None:
            time_treatment = 0
        grace_containers = None
        if acciaccatura_specifier is not None:
            grace_containers, segment = acciaccatura_specifier(segment)
            assert len(grace_containers) == len(segment)
        for pitch_expression in segment:
            prototype = abjad.NumberedPitchClass
            if isinstance(pitch_expression, prototype):
                pitch_expression = pitch_expression.number
            count = self._next_attack
            while talea[count] < 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    decrease_monotonic=decrease_durations,
                    )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
            self._next_attack += 1
            duration = talea[count]
            assert 0 < duration, repr(duration)
            skips_instead_of_rests = False
            if (isinstance(pitch_expression, tuple) and
                len(pitch_expression) == 2 and
                pitch_expression[-1] in (None, 'skip')):
                multiplier = pitch_expression[0]
                duration = abjad.Duration(1, talea.denominator)
                duration *= multiplier
                if pitch_expression[-1] == 'skip':
                    skips_instead_of_rests = True
                pitch_expression = None
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=skips_instead_of_rests,
                )
            leaves_ = maker([pitch_expression], [duration])
            leaves.extend(leaves_)
            count = self._next_attack
            while talea[count] < 0 and not count % len(talea) == 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    decrease_monotonic=decrease_durations,
                    )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
        leaves = self._add_rest_affixes(
            leaves,
            talea,
            rest_prefix,
            rest_suffix,
            affix_skips_instead_of_rests,
            decrease_durations,
            )
        leaf_selection = abjad.Selection(leaves)
        if isinstance(time_treatment, int):
            tuplet = self._make_tuplet_with_extra_count(
                leaf_selection,
                time_treatment,
                talea.denominator,
                )
        elif time_treatment in ('accel', 'rit'):
            tuplet = self._make_accelerando(leaf_selection, time_treatment)
        elif isinstance(time_treatment, abjad.Ratio):
            numerator, denominator = time_treatment.numbers
            multiplier = abjad.NonreducedFraction((denominator, numerator))
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
        elif isinstance(time_treatment, abjad.Multiplier):
            tuplet = abjad.Tuplet(time_treatment, leaf_selection)
        elif time_treatment.__class__ is abjad.Duration:
            tuplet_duration = time_treatment
            contents_duration = leaf_selection.get_duration()
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not tuplet.multiplier.is_proper_tuplet_multiplier:
                tuplet._fix()
        else:
            message = 'invalid time treatment: {!r}.'
            message = message.format(time_treatment)
            raise Exception(message)
        assert isinstance(tuplet, abjad.Tuplet)
        if grace_containers is not None:
            logical_ties = abjad.iterate(tuplet).by_logical_tie()
            pairs = zip(grace_containers, logical_ties)
            for grace_container, logical_tie in pairs:
                if grace_container is None:
                    continue
                abjad.attach(grace_container, logical_tie.head)
        selection = abjad.Selection([tuplet])
        return selection

    def _make_state_manifest(self):
        state_manifest = {}
        for name in self._state_variables:
            value = getattr(self, name)
            state_manifest[name] = value
        return state_manifest

    @staticmethod
    def _make_tuplet_with_extra_count(
        leaf_selection,
        extra_count,
        denominator,
        ):
        contents_duration = leaf_selection.get_duration()
        contents_duration = contents_duration.with_denominator(denominator)
        contents_count = contents_duration.numerator
        if 0 < extra_count:
            extra_count %= contents_count
        elif extra_count < 0:
            extra_count = abs(extra_count)
            extra_count %= math.ceil(contents_count / 2.0)
            extra_count *= -1
        new_contents_count = contents_count + extra_count
        tuplet_multiplier = abjad.Multiplier(
            new_contents_count,
            contents_count,
            )
        if not tuplet_multiplier.is_proper_tuplet_multiplier:
            message = '{!r} gives {} with {} and {}.'
            message = message.format(
                leaf_selection,
                tuplet_multiplier,
                contents_count,
                new_contents_count,
                )
            raise Exception(message)
        tuplet = abjad.Tuplet(tuplet_multiplier, leaf_selection)
        return tuplet

    @staticmethod
    def _normalize_multiplier(multiplier):
        assert 0 < multiplier, repr(multiplier)
        while multiplier <= abjad.Multiplier(1, 2):
            multiplier *= 2
        while abjad.Multiplier(2) <= multiplier:
            multiplier /= 2
        return multiplier

    def _print_state_manifest(self):
        state_manifest = self._make_state_manifest()
        for key in sorted(state_manifest):
            value = state_manifest[key]
            message = '{}: {}'
            message = message.format(key, value)
            print(message)

    ### PUBLIC PROPERTIES ###

    @property
    def acciaccatura_specifiers(self):
        r'''Gets acciaccatura specifiers.

        ..  container:: example

            Graced quarters:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier()
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=4,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0],
                ...     [2, 10],
                ...     [18, 16, 15],
                ...     [20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> score = lilypond_file[abjad.Score]
                >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
                >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/2
                        {
                            c'4
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'4
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''4
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16 ]
                            }
                            c'4
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16
                                fs''16
                                e''16 ]
                            }
                            ef''4
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'4
                        }
                    }
                }

        ..  container:: example

            Graced rests:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             lmr_specifier=baca.LMRSpecifier()
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=4,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [None],
                ...     [0, None],
                ...     [2, 10, None],
                ...     [18, 16, 15, None],
                ...     [20, 19, 9, 0, None],
                ...     [2, 10, 18, 16, 15, None],
                ...     [20, 19, 9, 0, 2, 10, None],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> score = lilypond_file[abjad.Score]
                >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
                >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 7/4
                        {
                            r4
                        }
                        {
                            \acciaccatura {
                                c'16
                            }
                            r4
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16 ]
                            }
                            r4
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16
                                ef''16 ]
                            }
                            r4
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16 ]
                            }
                            r4
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16
                                fs''16
                                e''16
                                ef''16 ]
                            }
                            r4
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16
                                bf'16 ]
                            }
                            r4
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.acciaccatura_specifiers is None
                True

        Set to acciaccatura specifiers or none.

        Returns acciaccatura specifiers or none.
        '''
        return self._acciaccatura_specifiers

    @property
    def beam_specifier(self):
        r'''Gets beam specifier.

        ..  container:: example

            Beams each division by default:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[1],
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override TupletBracket.staff-padding = #1.5
                } {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Beams divisions together:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[1],
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5.5 . -5.5)
                } {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #2
                            c'16 [
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            d'16
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            bf'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            fs''16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            e''16
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            ef''8
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            af''16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #0
                            a'8 ]
                        }
                    }
                }

        ..  container:: example

            Beams nothing:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=False,
                ...         ),
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[1],
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            d'16
                            bf'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            e''16
                            ef''8
                            af''16
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Does not beam rests:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[1],
                ...     )

            ::

                >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override TupletBracket.staff-padding = #1.5
                } {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16
                            d'16 [
                            bf'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16 [
                            e''16
                            ef''8
                            af''16 ]
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Does beam rests:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_rests=True,
                ...     ),
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[1],
                ...     )

            ::

                >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override TupletBracket.staff-padding = #1.5
                } {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16 [
                            d'16
                            bf'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            r16 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Beams rests with stemlets:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_rests=True,
                ...         stemlet_length=0.75,
                ...     ),
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[1],
                ...     )

            ::

                >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override TupletBracket.staff-padding = #1.5
                } {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            \override Staff.Stem.stemlet-length = #0.75
                            r16 [
                            d'16
                            \revert Staff.Stem.stemlet-length
                            bf'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            \override Staff.Stem.stemlet-length = #0.75
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            \revert Staff.Stem.stemlet-length
                            r16 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            \revert Staff.Stem.stemlet-length
                            \override Staff.Stem.stemlet-length = #0.75
                            a'8
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.beam_specifier is None
                True

        Set to beam specifier or none.

        Returns beam specifier or none.
        '''
        return abjad.rhythmmakertools.RhythmMaker.beam_specifier.fget(self)

    @property
    def division_masks(self):
        r'''Gets division masks.

        ..  container:: example

            No division masks:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Silences every other division:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_every([1], period=2),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        r4.
                        {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Sustains every other division:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     division_masks=[
                ...         abjad.sustain_every([1], period=2),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        c'4.
                        {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.division_masks is None
                True

        Set to division masks or none.

        Returns tuple of division masks or none.
        '''
        return abjad.rhythmmakertools.RhythmMaker.division_masks.fget(self)

    @property
    def duration_specifier(self):
        r'''Gets duration specifier.

        ..  container:: example

            Spells nonassignable durations with monontonically decreasing
            durations by default:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[4, 4, 5],
                ...         denominator=32,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 39/32
                        {
                            c'8 [
                            d'8
                            bf'8 ~
                            bf'32 ]
                        }
                        {
                            fs''8 [
                            e''8
                            ef''8 ~
                            ef''32
                            af''8
                            g''8 ]
                        }
                        {
                            a'8 ~ [
                            a'32 ]
                        }
                    }
                }

        ..  container:: example

            Spells nonassignable durations with monontonically increasing
            durations:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
                ...         decrease_monotonic=False,
                ...         ),
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[4, 4, 5],
                ...         denominator=32,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 39/32
                        {
                            c'8 [
                            d'8
                            bf'32 ~
                            bf'8 ]
                        }
                        {
                            fs''8 [
                            e''8
                            ef''32 ~
                            ef''8
                            af''8
                            g''8 ]
                        }
                        {
                            a'32 ~ [
                            a'8 ]
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.duration_specifier is None
                True

        Set to duration specifier or none.

        Returns duration specifier or none.
        '''
        return abjad.rhythmmakertools.RhythmMaker.duration_specifier.fget(self)

    @property
    def logical_tie_masks(self):
        r'''Gets logical tie masks.

        ..  container:: example

            Silences every third logical tie:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     logical_tie_masks=[
                ...         abjad.silence_every([2], period=3),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16 ]
                            r8
                        }
                        {
                            fs''16 [
                            e''16 ]
                            r8
                            af''16 [
                            g''16 ]
                        }
                        {
                            r8
                        }
                    }
                }

        ..  container:: example

            Silences first and last logical ties:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     logical_tie_masks=[
                ...         abjad.silence_first(),
                ...         abjad.silence_last(),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            r16
                            d'16 [
                            bf'8 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        {
                            r8
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.logical_tie_masks is None
                True

        Set to patterns or none.

        Returns tuple patterns or none.
        '''
        return abjad.rhythmmakertools.RhythmMaker.logical_tie_masks.fget(self)

    @property
    def talea(self):
        r'''Gets talea.

        ..  container:: example

            With rests:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_rests=True,
                ...         stemlet_length=1.5,
                ...         ),
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[3, -1, 2, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/2
                        {
                            \override Staff.Stem.stemlet-length = #1.5
                            c'8. [
                            r16
                            d'8
                            \revert Staff.Stem.stemlet-length
                            bf'8 ]
                        }
                        {
                            \override Staff.Stem.stemlet-length = #1.5
                            fs''8. [
                            r16
                            e''8
                            ef''8
                            af''8.
                            r16
                            \revert Staff.Stem.stemlet-length
                            g''8 ]
                        }
                        {
                            \revert Staff.Stem.stemlet-length
                            \override Staff.Stem.stemlet-length = #1.5
                            a'8
                        }
                    }
                }

        ..  container:: example

            With very large nonassignable counts:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[29],
                ...         denominator=64,
                ...         ),
                ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 29/32
                        {
                            c'4..
                            c'64 \repeatTie
                            d'4..
                            d'64 \repeatTie
                        }
                    }
                }

        ..  container:: example

            Defaults to even sixteenths:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.talea
                Talea(counts=[1], denominator=16)

        Set to talea or none.

        Returns talea.
        '''
        return self._talea

    @property
    def tie_specifier(self):
        r'''Gets tie specifier.

        ..  container:: example

            Ties across divisions with matching pitches:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [10, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16
                            bf'8 ~ ]
                        }
                        {
                            bf'16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Ties consecutive notes with matching pitches:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                ...         tie_consecutive_notes=True,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [10, 16, 16, 19, 19], [19]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'16 [
                            d'16
                            bf'8 ~ ]
                        }
                        {
                            bf'16 [
                            e''16 ~
                            e''8
                            g''16 ~
                            g''16 ~ ]
                        }
                        {
                            g''8
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.tie_specifier is None
                True

        Set to tie specifier or none.

        Returns tie specifier or none.
        '''
        return abjad.rhythmmakertools.RhythmMaker.tie_specifier.fget(self)

    @property
    def time_treatments(self):
        r'''Gets time treatments.

        ..  container:: example

            One extra count per division:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=[1],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }
                }

        ..  container:: example

            One missing count per division:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=[-1],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16 [
                            d'16
                            bf'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16 [
                            e''16
                            ef''8
                            af''16
                            g''16 ]
                        }
                        {
                            a'8
                        }
                    }
                }

        ..  container:: example

            Accelerandi:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=['accel'],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0],
                ...     [2, 10],
                ...     [18, 16, 15],
                ...     [20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-5, -5)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5 . -5)
                    \override Stem.direction = #down
                } {
                    {
                        \time 21/16
                        {
                            c'16
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            d'16 * 1328/1024 [
                            bf'16 * 720/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'8.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            fs''16 * 1552/1024 [
                            e''16 * 832/1024
                            ef''16 * 688/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            af''16 * 1728/1024 [
                            g''16 * 928/1024
                            a'16 * 768/1024
                            c'16 * 672/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            d'16 * 1872/1024 [
                            bf'16 * 1008/1024
                            fs''16 * 832/1024
                            e''16 * 736/1024
                            ef''16 * 672/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            af''16 * 2000/1024 [
                            g''16 * 1088/1024
                            a'16 * 896/1024
                            c'16 * 784/1024
                            d'16 * 720/1024
                            bf'16 * 656/1024 ]
                        }
                        \revert TupletNumber.text
                    }
                }

        ..  container:: example

            Ritardandi:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=['rit'],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0],
                ...     [2, 10],
                ...     [18, 16, 15],
                ...     [20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-5, -5)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5 . -5)
                    \override Stem.direction = #down
                } {
                    {
                        \time 21/16
                        {
                            c'16
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            d'16 * 656/1024 [
                            bf'16 * 1392/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'8.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            fs''16 * 512/1024 [
                            e''16 * 1072/1024
                            ef''16 * 1488/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            af''16 * 432/1024 [
                            g''16 * 896/1024
                            a'16 * 1232/1024
                            c'16 * 1536/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            d'16 * 368/1024 [
                            bf'16 * 784/1024
                            fs''16 * 1072/1024
                            e''16 * 1328/1024
                            ef''16 * 1568/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            af''16 * 336/1024 [
                            g''16 * 704/1024
                            a'16 * 960/1024
                            c'16 * 1184/1024
                            d'16 * 1392/1024
                            bf'16 * 1568/1024 ]
                        }
                        \revert TupletNumber.text
                    }
                }

        ..  container:: example

            Accelerandi followed by ritardandi:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=['accel', 'rit'],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0, 2],
                ...     [10, 18, 16, 15, 20],
                ...     [19, 9, 0, 2, 10, 18],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-5, -5)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5 . -5)
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/8
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            c'16 * 1872/1024 [
                            d'16 * 1008/1024
                            bf'16 * 832/1024
                            fs''16 * 736/1024
                            e''16 * 672/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            ef''16 * 336/1024 [
                            af''16 * 704/1024
                            g''16 * 960/1024
                            a'16 * 1184/1024
                            c'16 * 1392/1024
                            d'16 * 1568/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            bf'16 * 1872/1024 [
                            fs''16 * 1008/1024
                            e''16 * 832/1024
                            ef''16 * 736/1024
                            af''16 * 672/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            g''16 * 336/1024 [
                            a'16 * 704/1024
                            c'16 * 960/1024
                            d'16 * 1184/1024
                            bf'16 * 1392/1024
                            fs''16 * 1568/1024 ]
                        }
                        \revert TupletNumber.text
                    }
                }

        ..  container:: example

            Mixed accelerandi, ritardandi and prolation:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=['accel', -2, 'rit'],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2],
                ...     [10, 18, 16, 15, 20],
                ...     [19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-5, -5)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5 . -5)
                    \override Stem.direction = #down
                } {
                    {
                        \time 13/8
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            c'16 * 1872/1024 [
                            d'16 * 1008/1024
                            bf'16 * 832/1024
                            fs''16 * 736/1024
                            e''16 * 672/1024 ]
                        }
                        \revert TupletNumber.text
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            ef''16 [
                            af''16
                            g''16
                            a'16
                            c'16 ]
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            d'16 * 368/1024 [
                            bf'16 * 784/1024
                            fs''16 * 1072/1024
                            e''16 * 1328/1024
                            ef''16 * 1568/1024 ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #right
                            af''16 * 1872/1024 [
                            g''16 * 1008/1024
                            a'16 * 832/1024
                            c'16 * 736/1024
                            d'16 * 672/1024 ]
                        }
                        \revert TupletNumber.text
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            bf'16 [
                            fs''16
                            e''16
                            ef''16
                            af''16 ]
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c'4 ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \times 1/1 {
                            \once \override Beam.grow-direction = #left
                            g''16 * 368/1024 [
                            a'16 * 784/1024
                            c'16 * 1072/1024
                            d'16 * 1328/1024
                            bf'16 * 1568/1024 ]
                        }
                        \revert TupletNumber.text
                    }
                }

        ..  container:: example

            Specified by tuplet multiplier:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=[abjad.Ratio((3, 2))],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0],
                ...     [2, 10],
                ...     [18, 16, 15],
                ...     [20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-6, -6)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                } {
                    {
                        \time 7/4
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8 [
                            bf'8 ]
                        }
                        \times 2/3 {
                            fs''8 [
                            e''8
                            ef''8 ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            af''8 [
                            g''8
                            a'8
                            c'8 ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8 [
                            bf'8
                            fs''8
                            e''8
                            ef''8 ]
                        }
                        \times 2/3 {
                            af''8 [
                            g''8
                            a'8
                            c'8
                            d'8
                            bf'8 ]
                        }
                    }
                }

        ..  container:: example

            Segment durations equal to a quarter:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=[abjad.Duration(1, 4)],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
                ...         preferred_denominator=abjad.Duration(1, 16),
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0],
                ...     [2, 10],
                ...     [18, 16, 15],
                ...     [20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-6, -6)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                } {
                    {
                        \time 3/2
                        {
                            c'4
                        }
                        {
                            d'8 [
                            bf'8 ]
                        }
                        \times 4/6 {
                            fs''8 [
                            e''8
                            ef''8 ]
                        }
                        {
                            af''16 [
                            g''16
                            a'16
                            c'16 ]
                        }
                        \times 4/5 {
                            d'16 [
                            bf'16
                            fs''16
                            e''16
                            ef''16 ]
                        }
                        \times 4/6 {
                            af''16 [
                            g''16
                            a'16
                            c'16
                            d'16
                            bf'16 ]
                        }
                    }
                }

        ..  container:: example

            Segment durations alternating between a quarter and a dotted
            quarter:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     time_treatments=[abjad.Duration(1, 4), abjad.Duration(3, 8)],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 2],
                ...         denominator=8,
                ...         ),
                ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
                ...         preferred_denominator=abjad.Duration(1, 16),
                ...         ),
                ...     )

            ::

                >>> collections = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     [20, 19, 9, 0, 2],
                ...     [10, 18, 16, 15, 20],
                ...     [19, 9, 0, 2, 10],
                ...     ]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).beam.positions = (-6, -6)
                >>> abjad.override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                } {
                    {
                        \time 15/8
                        \times 4/6 {
                            c'16 [
                            d'16
                            bf'8
                            fs''16
                            e''16 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            ef''8 [
                            af''16
                            g''16
                            a'8
                            c'16 ]
                        }
                        \times 4/7 {
                            d'16 [
                            bf'8
                            fs''16
                            e''16
                            ef''8 ]
                        }
                        {
                            af''16 [
                            g''16
                            a'8
                            c'16
                            d'16 ]
                        }
                        \times 4/7 {
                            bf'8 [
                            fs''16
                            e''16
                            ef''8
                            af''16 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            g''16 [
                            a'8
                            c'16
                            d'16
                            bf'8 ]
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.time_treatments is None
                True

        Set to time treatments or none.

        Time treatments defined equal to integers; positive multipliers;
        positive durations; and the strings ``'accel'`` and ``'rit'``.

        Returns tuple of time treatments or none.
        '''
        return self._time_treatments

    @property
    def tuplet_specifier(self):
        r'''Gets tuplet specifier.

        ..  container:: example

            Does not simplify redudant tuplets by default:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[3],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[-2],
                ...     )

            ::

                >>> collections = [[0, 2], [10, 18, 16], [15, 20], [19, 9, None]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override TupletBracket.staff-padding = #1.5
                } {
                    {
                        \time 11/8
                        \times 2/3 {
                            c'8. [
                            d'8. ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            bf'8. [
                            fs''8.
                            e''8. ]
                        }
                        \times 2/3 {
                            ef''8. [
                            af''8. ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            g''8. [
                            a'8. ]
                            r8.
                        }
                    }
                }

        ..  container:: example

            Simplifies redundant tuplets:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[3],
                ...         denominator=16,
                ...         ),
                ...     time_treatments=[-2],
                ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
                ...         simplify_redundant_tuplets=True,
                ...         ),
                ...     )

            ::

                >>> collections = [[0, 2], [10, 18, 16], [15, 20], [19, 9, None]]
                >>> selections, state_manifest = rhythm_maker(collections)
                >>> lilypond_file = rhythm_maker.show(selections)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff \with {
                    \override TupletBracket.staff-padding = #1.5
                } {
                    {
                        \time 11/8
                        {
                            c'8 [
                            d'8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            bf'8. [
                            fs''8.
                            e''8. ]
                        }
                        {
                            ef''8 [
                            af''8 ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            g''8. [
                            a'8. ]
                            r8.
                        }
                    }
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker()
                >>> rhythm_maker.tuplet_specifier is None
                True

        Set to tuplet specifier or none.

        Returns tuplet specifier or none.
        '''
        return abjad.rhythmmakertools.RhythmMaker.tuplet_specifier.fget(self)

    ### PUBLIC METHODS ###

    @staticmethod
    def show(selections, time_signatures=None):
        r'''Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        '''
        return abjad.LilyPondFile.rhythm(
            selections,
            time_signatures=time_signatures,
            )
