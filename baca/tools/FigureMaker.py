# -*- coding: utf-8 -*-
import abjad
import baca
import copy


class FigureMaker(abjad.abctools.AbjadObject):
    r'''Figure-maker.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Default figure-maker:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker('Voice 1', segments)
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'16 [
                            d'16
                            bf'16 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''16
                            af''16
                            g''16 ]
                        }
                        {
                            a'16
                        }
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Figures'

    __slots__ = (
        '_allow_repeated_pitches',
        '_annotate_unregistered_pitches',
        '_next_figure',
        '_preferred_denominator',
        '_specifiers',
        '_voice_names',
        )

    _extend_beam_tag = 'extend beam'

    _foreshadow_tag = 'foreshadow'

    _incomplete_tag = 'incomplete'

    _publish_storage_format = True

    _recollection_tag = 'recollection'

    _repeated_pitch_allowed_string = 'repeated pitch allowed'

    _state_variables = (
        '_next_figure',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *specifiers,
        allow_repeated_pitches=None,
        annotate_unregistered_pitches=None,
        preferred_denominator=None,
        voice_names=None
        ):
        if allow_repeated_pitches is not None:
            allow_repeated_pitches = bool(allow_repeated_pitches)
        self._allow_repeated_pitches = allow_repeated_pitches
        if annotate_unregistered_pitches is not None:
            annotate_unregistered_pitches = bool(annotate_unregistered_pitches)
        self._annotate_unregistered_pitches = annotate_unregistered_pitches
        self._next_figure = 0
        if preferred_denominator is not None:
            assert abjad.mathtools.is_positive_integer(preferred_denominator)
        self._preferred_denominator = preferred_denominator
        self._specifiers = specifiers
        if voice_names is not None:
            assert all([isinstance(_, str) for _ in voice_names])
        self._voice_names = voice_names

    ### SPECIAL METHODS ###

    def __call__(
        self,
        voice_name,
        segments,
        *specifiers,
        allow_repeated_pitches=None,
        annotate_unregistered_pitches=None,
        division_masks=None,
        exhaustive=None,
        extend_beam=None,
        figure_name=None,
        hide_time_signature=None,
        imbrication_map=None,
        is_foreshadow=None,
        is_incomplete=None,
        is_recollection=None,
        local_anchor=None,
        logical_tie_masks=None,
        polyphony_map=None,
        preferred_denominator=None,
        remote_anchor=None,
        state_manifest=None,
        talea__counts=None,
        talea__denominator=None,
        time_treatments=None
        ):
        r'''Calls figure-maker on `segments` with keywords.

        ..  container:: example

            Default figure-maker:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Calltime counts:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     talea__counts=[1, 2],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'8
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''8
                                ef''16
                                af''8
                                g''16 ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>
                
        ..  container:: example

            Calltime denominator:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     talea__denominator=32,
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'32 [
                                d'32
                                bf'32 ]
                            }
                            {
                                fs''32 [
                                e''32
                                ef''32
                                af''32
                                g''32 ]
                            }
                            {
                                a'32
                            }
                        }
                    }
                >>

        ..  container:: example

            Calltime time treatments:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     time_treatments=[1],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  note:: Write hide_time_signature calltime examples.

        Returns selection, time signature, state manifest.
        '''
        self._validate_voice_name(voice_name)
        segments = self._coerce_segments(segments)
        self._apply_state_manifest(state_manifest)
        specifiers = list(self.specifiers or []) + list(specifiers)
        selections, specifiers = self._make_selections(
            segments,
            specifiers,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            talea__counts=talea__counts,
            talea__denominator=talea__denominator,
            time_treatments=time_treatments,
            )
        container = abjad.Container(selections)
        self._annotate_unregistered_pitches_(
            container,
            annotate_unregistered_pitches=annotate_unregistered_pitches,
            )
        specifiers = self._apply_nesting_specifiers(selections, specifiers)
        specifiers = self._apply_register_specifiers(selections, specifiers)
        result = self._apply_imbrication_specifiers(container, specifiers)
        imbricated_selections, specifiers = result
        result = baca.tools.PolyphonySpecifier._make_polyphony_selections(
            container,
            polyphony_map,
            )
        polyphony_selections, hauptstimme_skip = result
        self._apply_remaining_specifiers(selections, specifiers)
        self._label_figure_name_(container, figure_name)
        self._annotate_segment_list(container, segments)
        self._annotate_deployment(
            container,
            is_foreshadow=is_foreshadow,
            is_recollection=is_recollection,
            )
        self._annotate_repeated_pitches(container)
        self._extend_beam_(container, extend_beam)
        self._check_well_formedness(container)
        state_manifest = self._make_state_manifest()
        if hauptstimme_skip is not None:
            selection = abjad.select([hauptstimme_skip, container])
        else:
            selection = abjad.select([container])
        time_signature = self._make_time_signature(
            selection,
            polyphony_selections,
            preferred_denominator=preferred_denominator,
            )
        selections = {voice_name: selection}
        selections.update(imbricated_selections)
        selections.update(polyphony_selections)
        for value in selections.values():
            assert isinstance(value, abjad.Selection), repr(value)
        return baca.tools.FigureContribution(
            figure_name=figure_name,
            hide_time_signature=hide_time_signature,
            local_anchor=local_anchor,
            remote_anchor=remote_anchor,
            selections=selections,
            state_manifest=state_manifest,
            time_signature=time_signature,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_selections(argument):
        prototype = abjad.selectiontools.Selection
        return all(isinstance(_, prototype) for _ in argument)

    def _annotate_repeated_pitches(self, container):
        if not self.allow_repeated_pitches:
            return
        for leaf in abjad.iterate(container).by_leaf(pitched=True):
            abjad.attach(self._repeated_pitch_allowed_string, leaf)

    def _annotate_deployment(
        self,
        argument,
        is_foreshadow=False,
        is_incomplete=False,
        is_recollection=False,
        ):
        if not is_foreshadow and not is_recollection and not is_incomplete:
            return
        for leaf in abjad.iterate(argument).by_leaf():
            if is_foreshadow:
                abjad.attach(self._foreshadow_tag, leaf)
            if is_incomplete:
                abjad.attach(self._incomplete_tag, leaf)
            if is_recollection:
                abjad.attach(self._recollection_tag, leaf)

    @staticmethod
    def _annotate_segment_list(container, segments):
        for leaf in abjad.iterate(container).by_leaf():
            segments_ = copy.deepcopy(segments)
            abjad.attach(segments_, leaf)

    def _annotate_unregistered_pitches_(
        self,
        argument,
        annotate_unregistered_pitches=None,
        ):
        if annotate_unregistered_pitches is None:
            annotate_unregistered_pitches = self.annotate_unregistered_pitches
        if not annotate_unregistered_pitches:
            return
        prototype = (abjad.Note, abjad.Chord)
        agent = abjad.iterate(argument)
        for note in agent.by_leaf(prototype, with_grace_notes=True):
            abjad.attach('not yet registered', note)

    def _apply_figure_pitch_specifiers(self, segments, specifiers):
        prototype = (baca.tools.SegmentList, list, abjad.Sequence)
        assert isinstance(segments, prototype), repr(segments)
        specifiers_, unused_specifiers = [], []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.FigurePitchSpecifier):
                segments = specifier(segments)
            else:
                unused_specifiers.append(specifier)
        return segments, unused_specifiers

    def _apply_imbrication_specifiers(self, container, specifiers):
        unused_specifiers = []
        imbricated_selections = {}
        for specifier in specifiers:
            if not isinstance(specifier, baca.tools.ImbricationSpecifier):
                unused_specifiers.append(specifier)
                continue
            imbricated_selection = specifier(container)
            imbricated_selections.update(imbricated_selection)
        return imbricated_selections, unused_specifiers
        
    def _apply_nesting_specifiers(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.NestingSpecifier):
                specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_

    def _apply_register_specifiers(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        prototype = (
            baca.tools.RegisterSpecifier,
            baca.tools.RegisterInterpolationSpecifier,
            baca.tools.RegisterToOctaveSpecifier,
            baca.tools.RegisterTransitionSpecifier,
            )
        for specifier in specifiers:
            if isinstance(specifier, prototype):
                specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_

    def _apply_remaining_specifiers(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        for specifier in specifiers:
            if isinstance(specifier, abjad.rhythmmakertools.BeamSpecifier):
                specifier._detach_all_beams(selections)
            specifier(selections)

    def _apply_rest_affix_specifiers(self, selections, specifiers):
        unused_specifiers = []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RestAffixSpecifier):
                specifier(selections)
            else:
                unused_specifiers.append(specifier)
        return unused_specifiers

    def _apply_simultaneity_specifiers(self, segments, specifiers):
        specifiers_, unused_specifiers = [], []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.SimultaneitySpecifier):
                specifiers_.append(specifier)
            else:
                unused_specifiers.append(specifier)
        prototype = (baca.tools.SegmentList, list, abjad.Sequence)
        for specifier in specifiers_:
            assert isinstance(segments, prototype), repr(segments)
            segments = specifier(segments)
        return segments, unused_specifiers

    def _apply_spacing_specifiers(self, segments, specifiers):
        prototype = (baca.tools.SegmentList, list, abjad.Sequence)
        assert isinstance(segments, prototype), repr(segments)
        specifiers_, unused_specifiers = [], []
        prototype = (
            baca.tools.ArpeggiationSpacingSpecifier,
            baca.tools.ChordalSpacingSpecifier,
            )
        for specifier in specifiers:
            if isinstance(specifier, prototype):
                segments = specifier(segments)
            else:
                unused_specifiers.append(specifier)
        return segments, unused_specifiers

    def _apply_state_manifest(self, state_manifest=None):
        state_manifest = state_manifest or {}
        assert isinstance(state_manifest, dict), repr(state_manifest)
        for key in state_manifest:
            value = state_manifest[key]
            setattr(self, key, value)

    @staticmethod
    def _check_well_formedness(selections):
        for component in abjad.iterate(selections).by_class():
            inspector = abjad.inspect_(component)
            if not inspector.is_well_formed():
                report = inspector.tabulate_well_formedness_violations()
                report = repr(component) + '\n' + report
                raise Exception(report)

    @staticmethod
    def _coerce_segments(segments):
        item_class = abjad.NumberedPitch
        for segment in segments:
            for item in segment:
                if isinstance(item, str):
                    item_class = abjad.NamedPitch
                    break
        return baca.tools.SegmentList(
            segments=segments,
            item_class=item_class,
            )

    @staticmethod
    def _exactly_double(selections):
        length = len(selections)
        if length % 2 == 1:
            return False
        half_length = int(length / 2)
        for index in range(half_length):
            first_selection = selections[index]
            second_selection = selections[index+half_length]
            first_format = format(first_selection, 'lilypond') 
            second_format = format(second_selection, 'lilypond') 
            if not first_format == second_format:
                return False
        return True

    def _extend_beam_(self, selections, extend_beam):
        if not extend_beam:
            return
        leaves = list(abjad.iterate(selections).by_leaf())
        last_leaf = leaves[-1]
        abjad.attach(self._extend_beam_tag, last_leaf)

    def _get_imbrication_specifiers(self):
        result = []
        specifiers = self.specifiers or []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.ImbricationSpecifier):
                result.append(specifier)
        if not result:
            specifier = baca.tools.ImbricationSpecifier()
            result.append(specifier)
        return result

    def _get_rhythm_specifiers(self, specifiers):
        unused_specifiers, result = [], []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RhythmSpecifier):
                result.append(specifier)
            else:
                unused_specifiers.append(specifier)
        if not result:
            specifier = baca.tools.RhythmSpecifier(
                patterns=abjad.patterntools.select_all(),
                rhythm_maker=baca.tools.FigureRhythmMaker(),
                )
            result.append(specifier)
        return unused_specifiers, result

    def _get_storage_format_specification(self):
        agent = abjad.systemtools.StorageFormatAgent(self)
        keyword_argument_names = agent.signature_keyword_names
        positional_argument_values = self.specifiers
        return abjad.systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    @staticmethod
    def _label_figure_name_(container, figure_name):
        if figure_name is None:
            return
        figure_name = str(figure_name)
        original_figure_name = figure_name
        parts = figure_name.split('_')
        if len(parts) == 1:
            body = parts[0]
            figure_name = abjad.Markup(body)
        elif len(parts) == 2:
            body, subscript = parts
            figure_name = abjad.Markup.concat([
                abjad.Markup(body),
                abjad.Markup(subscript).sub(),
                ])
        else:
            message = 'unrecognized figure name: {!r}.'
            message = message.format(figure_name)
            raise Exception(figure_name)
        figure_name = abjad.Markup.concat([
            '[',
            figure_name,
            ']',
            ])
        figure_name = figure_name.with_color('darkgreen')
        figure_name = figure_name.fontsize(3)
        figure_name = abjad.Markup(figure_name, direction=Up)
        annotation = 'figure name: {}'.format(original_figure_name)
        figure_name._annotation = annotation
        leaves = list(abjad.iterate(container).by_leaf())
        abjad.attach(figure_name, leaves[0])

    def _make_selections(
        self,
        segments,
        specifiers,
        division_masks=None,
        logical_tie_masks=None,
        talea__counts=None,
        talea__denominator=None,
        time_treatments=None,
        ):
        segments, specifiers = self._apply_figure_pitch_specifiers(
            segments,
            specifiers,
            )
        segments, specifiers = self._apply_spacing_specifiers(
            segments,
            specifiers,
            )
        segments, specifiers = self._apply_simultaneity_specifiers(
            segments,
            specifiers,
            )
        selections = len(segments) * [None]
        specifiers, rhythm_specifiers = self._get_rhythm_specifiers(specifiers)
        for rhythm_specifier in rhythm_specifiers:
            rhythm_specifier._apply_figure_rhythm_maker(
                segments=segments,
                selections=selections,
                division_masks=division_masks,
                logical_tie_masks=logical_tie_masks,
                talea__counts=talea__counts,
                talea__denominator=talea__denominator,
                time_treatments=time_treatments,
                )
        assert self._all_are_selections(selections), repr(selections)
        specifiers = self._apply_rest_affix_specifiers(selections, specifiers)
        assert self._all_are_selections(selections), repr(selections)
        return selections, specifiers

    def _make_state_manifest(self):
        state_manifest = {}
        for name in self._state_variables:
            value = getattr(self, name)
            state_manifest[name] = value
        return state_manifest

    def _make_time_signature(
        self,
        selection,
        polyphony_selections,
        preferred_denominator=None,
        ):
        if preferred_denominator is None:
            preferred_denominator = self.preferred_denominator
        time_signatures = []
        polyphony_selections = list(polyphony_selections.values())
        for selection in polyphony_selections:
            assert isinstance(selection, abjad.Selection), repr(selection)
        selections = [selection] + polyphony_selections
        durations = [_.get_duration() for _ in selections]
        duration = max(durations)
        if preferred_denominator is not None:
            duration = duration.with_denominator(preferred_denominator)
        time_signature = abjad.indicatortools.TimeSignature(duration)
        return time_signature

    def _print_state_manifest(self):
        state_manifest = self._make_state_manifest()
        for key in sorted(state_manifest):
            value = state_manifest[key]
            message = '{}: {}'
            message = message.format(key, value)
            print(message)

    @staticmethod
    def _to_pitch_item_class(item_class):
        if item_class in (abjad.NamedPitch, abjad.NumberedPitch):
            return item_class
        elif item_class is abjad.NamedPitchClass:
            return abjad.NamedPitch
        elif item_class is abjad.NumberedPitchClass:
            return abjad.NumberedPitch
        else:
            raise TypeError(item_class)

    def _validate_voice_name(self, voice_name): 
        if not isinstance(voice_name, str):
            message = 'voice name must be string: {!r}.'
            message = message.format(voice_name)
            raise TypeError(message)
        if self.voice_names and voice_name not in self.voice_names:
            message = 'unknown voice name: {!r}.'
            message = message.format(voice_name)
            raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeated_pitches(self):
        r'''Is true when figure-maker allows repeated pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._allow_repeated_pitches

    @property
    def annotate_unregistered_pitches(self):
        r'''Is true when figure-maker annotates unregistered pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._annotate_unregistered_pitches

    @property
    def preferred_denominator(self):
        r'''Gets preferred denominator.

        ..  container:: example

            No preferred denominator by default:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16
                                f''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Preferred denominator supplied at configuration time:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     preferred_denominator=16,
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(
                ...     contribution,
                ...     time_signatures=[contribution.time_signature],
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16
                                f''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Preferred denominator supplied at call time:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     preferred_denominator=8,
                ...     )
                >>> lilypond_file = figure_maker.show(
                ...     contribution,
                ...     time_signatures=[contribution.time_signature],
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16
                                f''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Preferred denominator supplied at call time overrides preferred
            denominator supplied at configuration time:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     preferred_denominator=16,
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     preferred_denominator=8,
                ...     )
                >>> lilypond_file = figure_maker.show(
                ...     contribution,
                ...     time_signatures=[contribution.time_signature],
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16
                                f''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 ]
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._preferred_denominator 

    @property
    def specifiers(self):
        r'''Gets specifiers.

        ..  container:: example

            Articulation specifier:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...         selector=selectortools.Selector().
                ...             by_class(Note, flatten=True),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 -\staccato [
                                d'16 -\staccato
                                bf'16 -\staccato ]
                            }
                            {
                                fs''16 -\staccato [
                                e''16 -\staccato
                                ef''16 -\staccato
                                af''16 -\staccato
                                g''16 -\staccato ]
                            }
                            {
                                a'16 -\staccato
                            }
                        }
                    }
                >>

        ..  container:: example

            Articulation specifier selects notes of nonfirst and nonlast
            tuplets:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=[('.', '-')],
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet).
                ...             get_slice(
                ...                 start=1, stop=-1, apply_to_each=True).
                ...             by_class(Note, flatten=True),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 -\staccato -\tenuto [
                                e''16 -\staccato -\tenuto
                                ef''16 -\staccato -\tenuto
                                af''16 -\staccato -\tenuto
                                g''16 -\staccato -\tenuto ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Register specifier transposes to octave rooted on F#3:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RegisterSpecifier(
                ...         registration=pitchtools.Registration(
                ...             [('[A0, C8]', -6)],
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf16 ]
                            }
                            {
                                fs16 [
                                e'16
                                ef'16
                                af16
                                g16 ]
                            }
                            {
                                a16
                            }
                        }
                    }
                >>

        ..  container:: example

            Register transition specifier transposes from octave of C4 to
            octave of C5:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RegisterTransitionSpecifier(
                ...         start_registration=pitchtools.Registration(
                ...             [('[A0, C8]', 0)],
                ...             ),
                ...         stop_registration=pitchtools.Registration(
                ...             [('[A0, C8]', 12)],
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs'16 [
                                e''16
                                ef''16
                                af'16
                                g''16 ]
                            }
                            {
                                a''16
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifier selects all leaves:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('p < f'),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).dynamic_line_spanner.staff_padding = 4.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #4.5
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 \< \p [
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 \f ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifier selects runs of notes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('p < f'),
                ...         selector=selectortools.Selector().
                ...             by_leaf().
                ...             by_run(scoretools.Note),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.RestAffixSpecifier(
                ...         denominator=16,
                ...         pattern=abjad.Pattern(
                ...             indices=[0, -1],
                ...             inverted=True,
                ...             ),
                ...         prefix=[1],
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).dynamic_line_spanner.staff_padding = 4.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #4.5
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 \< \p [
                                d'16
                                bf'16
                                fs''16 \f ]
                            }
                            {
                                r16
                                ef''16 \< \p [
                                b''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 \f ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifiers select notes of first and last tuplet:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('p < f'),
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet).
                ...             get_item(0, apply_to_each=True),
                ...         ),
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('f > p'),
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet).
                ...             get_item(-1, apply_to_each=True),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).dynamic_line_spanner.staff_padding = 4.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #4.5
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 \< \p [
                                d'16
                                bf'16
                                fs''16 \f ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16 ]
                            }
                            {
                                g''16 \> \f [
                                cs''16
                                a'16
                                af'16 \p ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifiers treat first two tuplets and then the rest:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('p < f'),
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet).
                ...             get_slice(stop=2, apply_to_each=True).
                ...             by_leaf(),
                ...         ),
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('f > p'),
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet).
                ...             get_slice(start=2, apply_to_each=True).
                ...             by_leaf(),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).dynamic_line_spanner.staff_padding = 6
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #6
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 \< \p [
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16 \f ]
                            }
                            {
                                g''16 \> \f [
                                cs''16
                                a'16
                                af'16 \p ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Spanner specifier selects all leaves by default:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Stem.direction = #down
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [ (
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [
                                ef''16
                                b''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 ] )
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects all components in each tuplet:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet, flatten=True).
                ...             get_slice(apply_to_each=True),
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Stem.direction = #down
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [ (
                                d'16
                                bf'16
                                fs''16 ] )
                            }
                            {
                                e''16 [ (
                                ef''16
                                b''16 ] )
                            }
                            {
                                g''16 [ (
                                cs''16
                                a'16
                                af'16 ] )
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects first two components of each tuplet:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet, flatten=True).
                ...             get_slice(stop=2, apply_to_each=True),
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Stem.direction = #down
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [ (
                                d'16 )
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 [ (
                                ef''16 )
                                b''16 ]
                            }
                            {
                                g''16 [ (
                                cs''16 )
                                a'16
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects last two components of each tuplet:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet, flatten=True).
                ...             get_slice(start=-2, apply_to_each=True),
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Stem.direction = #down
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 (
                                fs''16 ] )
                            }
                            {
                                e''16 [
                                ef''16 (
                                b''16 ] )
                            }
                            {
                                g''16 [
                                cs''16
                                a'16 (
                                af'16 ] )
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur and articulation specifiers:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet, flatten=True).
                ...             get_slice(start=1, apply_to_each=True).
                ...             by_class(Note, flatten=True),
                ...         ),
                ...     baca.tools.SpannerSpecifier(
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet, flatten=True).
                ...             get_slice(stop=2, apply_to_each=True),
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Stem.direction = #down
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 [ (
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16 -\staccato )
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                fs''16 -\staccato
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                e''16 (
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                ef''16 -\staccato )
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                b''16 -\staccato
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                g''16 (
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                cs''16 -\staccato )
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                af'16 -\staccato ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects leaves of first tuplet plus following leaf:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         selector=selectortools.Selector().
                ...             by_class(scoretools.Tuplet).
                ...             get_slice(stop=1).
                ...             by_leaf(flatten=False).
                ...             with_next_leaf(),
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Stem.direction = #down
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [ (
                                d'16
                                bf'16
                                fs''16 ]
                            }
                            {
                                e''16 ) [
                                ef''16
                                b''16 ]
                            }
                            {
                                g''16 [
                                cs''16
                                a'16
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beam specifier beams divisions together:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).beam.positions = (-6, -6)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-6 . -6)
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                fs''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                b''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                g''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                cs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beam specifier beams nothing:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=False,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16
                                d'16
                                bf'16
                                fs''16
                            }
                            {
                                e''16
                                ef''16
                                b''16
                            }
                            {
                                g''16
                                cs''16
                                a'16
                                af'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Nesting specifier augments one sixteenth:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.NestingSpecifier(
                ...         time_treatments=['+1/16'],
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).beam.positions = (-5.5, -5.5)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5.5 . -5.5)
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 12/11 {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    fs''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    b''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    cs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    af'16 ]
                                }
                            }
                        }
                    }
                >>

        ..  container:: example

            Nesting specifier augments first two stages one sixteenth:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.NestingSpecifier(
                ...         lmr_specifier=baca.tools.LMRSpecifier(
                ...             left_length=2,
                ...             ),
                ...         time_treatments=['+1/16', None],
                ...         ),
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> staff = lilypond_file[Staff]
                >>> override(staff).beam.positions = (-5.5, -5.5)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff \with {
                    \override Beam.positions = #'(-5.5 . -5.5)
                } <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 8/7 {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    fs''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    b''16
                                }
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                g''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                cs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                af'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Sixteenths followed by eighths:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=8,
                ...                 ),
                ...             ),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select_first(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''8 [
                                e''8
                                ef''8
                                af''8
                                g''8 ]
                            }
                            {
                                a'8
                            }
                        }
                    }
                >>

        ..  container:: example

            Sixteenths surrounding dotted eighths:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select(indices=[0, -1]),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''8. [
                                e''8.
                                ef''8.
                                af''8.
                                g''8. ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Sixteenths surrounding argumented dotted eighths:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             time_treatments=[1],
                ...             ),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select(indices=[0, -1]),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 16/15 {
                                fs''8. [
                                e''8.
                                ef''8.
                                af''8.
                                g''8. ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Augmented sixteenths surrounding dotted eighths:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select(indices=[0, -1]),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             time_treatments=[1],
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''8. [
                                e''8.
                                ef''8.
                                af''8.
                                g''8. ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Diminished sixteenths surrounding dotted eighths:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select_all(),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     baca.tools.RhythmSpecifier(
                ...         patterns=patterntools.select(indices=[0, -1]),
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             time_treatments=[-1],
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker('Voice 1', segments)
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 2/3 {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''8. [
                                e''8.
                                ef''8.
                                af''8.
                                g''8. ]
                            }
                            {
                                a'16
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to specifiers or none.

        Returns specifiers or none.
        '''
        return self._specifiers

    @property
    def voice_names(self):
        r'''Gets voice names.

        Used to check call-time voice names.

        Defaults to none.

        Set to list of strings or none.

        Returns list or strings or none.
        '''
        if self._voice_names:
            return list(self._voice_names)

    ### PUBLIC METHODS ###

    @staticmethod
    def show(figure_contribution, time_signatures=None):
        r'''Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        '''
        assert isinstance(figure_contribution, baca.tools.FigureContribution)
        return abjad.rhythmmakertools.make_lilypond_file(
            figure_contribution.selections,
            time_signatures=time_signatures,
            attach_lilypond_voice_commands=True,
            )
