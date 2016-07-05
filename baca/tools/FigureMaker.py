# -*- coding: utf-8 -*-
import abjad
import baca
import copy


class FigureMaker(abjad.abctools.AbjadObject):
    r'''Figure-maker.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Default figure-maker:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> result = figure_maker(figure_token)
            >>> selection, time_signature, state_manifest = result
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     [selection],
            ...     [time_signature],
            ...     pitched_staff=True,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> class_ = rhythmmakertools.RhythmMaker
            >>> staff = class_._get_staff(lilypond_file)
            >>> f(staff)
            \new Staff {
                {
                    \time 9/16
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
            }

    ..  container:: example

        **Example 2.** Unknown keyword raises exception:

        ::

            >>> baca.tools.FigureMaker(color='red')
            Traceback (most recent call last):
            ...
            Exception: unknown keyword: 'color'.

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Figures'

    __slots__ = (
        '_allow_repeated_pitches',
        '_annotate_unregistered_pitches',
        '_next_figure',
        '_preferred_denominator',
        '_specifiers',
        )

    _foreshadow_tag = 'foreshadow'

    _incomplete_tag = 'incomplete'

    _initializer_keywords = (
        'allow_repeated_pitches',
        'annotate_unregistered_pitches',
        'preferred_denominator',
        )

    _calltime_keywords = _initializer_keywords + (
        'extend_beam',
        'figure_name',
        'is_foreshadow',
        'is_incomplete',
        'is_recollection',
        'state_manifest',
        )

    _recollection_tag = 'recollection'

    _repeated_pitch_allowed_string = 'repeated pitch allowed'

    _state_variables = (
        '_next_figure',
        )

    ### INITIALIZER ###

    def __init__(self, *specifiers, **keywords):
        allow_repeated_pitches = keywords.get('allow_repeated_pitches')
        annotate_unregistered_pitches = keywords.get(
            'annotate_unregistered_pitches')
        preferred_denominator = keywords.get('preferred_denominator')
        for name in keywords:
            if name not in self._initializer_keywords:
                message = 'unknown keyword: {!r}.'
                message = message.format(name)
                raise Exception(message)
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

    ### SPECIAL METHODS ###

    def __call__(
        self,
        figure_token,
        *specifiers,
        **keywords
        ):
        r'''Calls figure-maker on `figure_token`.

        ..  container:: example

            **Example.** Unknown keyword raises exception:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token, color='red')
                Traceback (most recent call last):
                ...
                Exception: unknown keyword: 'color'.

        Returns selection, time signature, state manifest.
        '''
        annotate_unregistered_pitches = keywords.get(
            'annotate_unregistered_pitches')
        exhaustive = keywords.get('exhaustive')
        extend_beam = keywords.get('extend_beam')
        figure_name = keywords.get('figure_name')
        is_foreshadow = keywords.get('is_foreshadow')
        is_incomplete = keywords.get('is_incomplete')
        is_recollection = keywords.get('is_recollection')
        preferred_denominator = keywords.get('preferred_denominator')
        state_manifest = keywords.get('state_manifest')
        for keyword in keywords:
            if keyword not in self._calltime_keywords:
                message = 'unknown keyword: {!r}.'
                message = message.format(keyword)
                raise Exception(message)
        self._apply_state_manifest(state_manifest)
        container = self._make_selections(figure_token)
        self._annotate_unregistered_pitches_(
            container,
            annotate_unregistered_pitches=annotate_unregistered_pitches,
            )
        assert isinstance(container, abjad.Container), repr(container)
        self._apply_calltime_specifiers(container, specifiers)
        self._label_figure_name_(container, figure_name)
        self._annotate_figure_token(container, figure_token)
        self._annotate_deployment(
            container,
            is_foreshadow=is_foreshadow,
            is_recollection=is_recollection,
            )
        self._annotate_repeated_pitches(container)
        self._extend_beam_(container, extend_beam)
        self._check_well_formedness(container)
        time_signature = self._make_time_signature(
            container,
            preferred_denominator=preferred_denominator,
            )
        state_manifest = self._make_state_manifest()
        selection = abjad.select(container)
        assert len(selection) == 1
        return selection, time_signature, state_manifest

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        keyword_argument_names = (
            'annotate_unregistered_pitches',
            'preferred_denominator',
            )
        positional_argument_values = self.specifiers
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    def _annotate_repeated_pitches(self, container):
        if not self.allow_repeated_pitches:
            return
        for leaf in abjad.iterate(container).by_leaf(pitched=True):
            abjad.attach(self._repeated_pitch_allowed_string, leaf)

    def _annotate_deployment(
        self,
        object_,
        is_foreshadow=False,
        is_incomplete=False,
        is_recollection=False,
        ):
        if not is_foreshadow and not is_recollection and not is_incomplete:
            return
        for leaf in abjad.iterate(object_).by_leaf():
            if is_foreshadow:
                abjad.attach(self._foreshadow_tag, leaf)
            if is_incomplete:
                abjad.attach(self._incomplete_tag, leaf)
            if is_recollection:
                abjad.attach(self._recollection_tag, leaf)

    @staticmethod
    def _annotate_figure_token(container, figure_token):
        for leaf in abjad.iterate(container).by_leaf():
            figure_token_ = copy.deepcopy(figure_token)
            abjad.attach(figure_token_, leaf)

    def _annotate_unregistered_pitches_(
        self,
        expr,
        annotate_unregistered_pitches=None,
        ):
        if annotate_unregistered_pitches is None:
            annotate_unregistered_pitches = self.annotate_unregistered_pitches
        if not annotate_unregistered_pitches:
            return
        prototype = (abjad.Note, abjad.Chord)
        agent = abjad.iterate(expr)
        for note in agent.by_leaf(prototype, with_grace_notes=True):
            abjad.attach('not yet registered', note)

    def _apply_calltime_specifiers(self, container, specifiers):
        assert isinstance(container, abjad.Container), repr(container)
        selections = [abjad.select(_) for _ in container]
        nested_selections = None
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RhythmSpecifier):
                continue
            if isinstance(specifier, abjad.rhythmmakertools.BeamSpecifier):
                specifier._detach_all_beams(selections)
            if isinstance(specifier, baca.tools.NestingSpecifier):
                nested_selections = specifier(selections)
            else:
                specifier(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    def _apply_specifiers(self, selections):
        nested_selections = None
        specifiers = self.specifiers or []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RhythmSpecifier):
                continue
            if isinstance(specifier, abjad.rhythmmakertools.BeamSpecifier):
                specifier._detach_all_beams(selections)
            if isinstance(specifier, baca.tools.NestingSpecifier):
                nested_selections = specifier(selections)
            else:
                specifier(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    def _apply_state_manifest(self, state_manifest=None):
        state_manifest = state_manifest or {}
        assert isinstance(state_manifest, dict), repr(state_manifest)
        for key in state_manifest:
            value = state_manifest[key]
            setattr(self, key, value)

    def _assemble_tagged_rhythms(tagged_rhythms):
        selection = abjad.selectiontools.Selection()
        return selection

    @staticmethod
    def _check_well_formedness(selections):
        for component in abjad.iterate(selections).by_class():
            inspector = abjad.inspect_(component)
            if not inspector.is_well_formed():
                report = inspector.tabulate_well_formedness_violations()
                report = repr(component) + '\n' + report
                raise Exception(report)

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

    @staticmethod
    def _extend_beam_(selections, extend_beam):
        if not extend_beam:
            return
        leaves = list(abjad.iterate(selections).by_leaf())
        last_leaf = leaves[-1]
        abjad.attach('extend beam', last_leaf)

    def _get_rhythm_specifiers(self):
        result = []
        specifiers = self.specifiers or []
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RhythmSpecifier):
                result.append(specifier)
        if not result:
            specifier = baca.tools.RhythmSpecifier(
                patterns=abjad.patterntools.select_all(),
                rhythm_maker=baca.tools.FigureRhythmMaker(),
                )
            result.append(specifier)
        return result

    @staticmethod
    def _label_figure_name_(container, figure_name):
        if figure_name is None:
            return
        figure_name = str(figure_name)
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
        figure_name._annotation = 'figure name'
        leaves = list(abjad.iterate(container).by_leaf())
        abjad.attach(figure_name, leaves[0])

    def _make_selections(self, figure_token):
        tagged_rhythms = []
        rhythm_specifiers = self._get_rhythm_specifiers()
        figure_list = len(figure_token) * [None]
        for rhythm_specifier in rhythm_specifiers:
            figure_selection = rhythm_specifier._apply_figure_rhythm_maker(
                figure_list=figure_list,
                figure_token=figure_token,
                )
        assert isinstance(figure_list, list), repr(figure_list)
        container = abjad.Container(figure_list)
        selections = self._apply_specifiers(figure_list)
        return container

    def _make_state_manifest(self):
        state_manifest = {}
        for name in self._state_variables:
            value = getattr(self, name)
            state_manifest[name] = value
        return state_manifest

    def _make_time_signature(self, container, preferred_denominator=None):
        if preferred_denominator is None:
            preferred_denominator = self.preferred_denominator
        time_signatures = []
        duration = abjad.inspect_(container).get_duration()
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

            **Example 1.** No preferred denominator:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 3/4
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
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Preferred denominator supplied at configuration
            time:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     preferred_denominator=16,
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 12/16
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
                }

        ..  container:: example

            **Example 3.** Preferred denominator supplied at call time:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(
                ...     figure_token,
                ...     preferred_denominator=8,
                ...     )
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 6/8
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
                }

        ..  container:: example

            **Example 4.** Preferred denominator supplied at call time
            overrides preferred denominator supplied at configuration time:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     preferred_denominator=16,
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23, 17],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(
                ...     figure_token,
                ...     preferred_denominator=8,
                ...     )
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 6/8
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
                }

        Defaults to none.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._preferred_denominator 

    @property
    def specifiers(self):
        r'''Gets specifiers.

        ..  container:: example

            **Example 1.** Articulation specifier:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...         selector=selectortools.Selector().
                ...             by_class(Note, flatten=True),
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 9/16
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
                }

        ..  container:: example

            **Example 2.** Articulation specifier selects notes of nonfirst and
            nonlast tuplets:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 9/16
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
                }

        ..  container:: example

            **Example 3.** Register specifier transposes to octave rooted on
            F#3:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RegisterSpecifier(
                ...         registration=pitchtools.Registration(
                ...             [('[A0, C8]', -6)],
                ...             ),
                ...         ),
                ...     )

            ::

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 9/16
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
                }

        ..  container:: example

            **Example 4.** Register transition specifier transposes from octave
            of C4 to octave of C5:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 9/16
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
                }

        ..  container:: example

            **Example 5.** Hairpin specifier selects all leaves:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.DynamicSpecifier(
                ...         dynamic=spannertools.Hairpin('p < f'),
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).dynamic_line_spanner.staff_padding = 4.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #4.5
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 6.** Hairpin specifier selects runs of notes:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [None, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).dynamic_line_spanner.staff_padding = 4.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #4.5
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 7.** Hairpin specifiers select notes of first and last
            tuplet:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).dynamic_line_spanner.staff_padding = 4.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #4.5
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 8.** Hairpin specifiers treat first two tuplets and then
            the rest:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).dynamic_line_spanner.staff_padding = 6
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #6
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 9.** Slur specifier selects all leaves:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.SpannerSpecifier(
                ...         spanner=spannertools.Slur(),
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/16
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
                }

            This is default behavior.

        ..  container:: example

            **Example 10.** Slur specifier selects all components in each
            tuplet:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 11.** Slur specifier selects first two components of each
            tuplet:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 12.** Slur specifier selects last two components of each
            tuplet:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 13.** Slur and articulation specifiers:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 14.** Slur specifier selects leaves of first tuplet plus
            following leaf:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).stem.direction = Down
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Stem.direction = #down
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 15.** Beam specifier beams divisions together:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).beam.positions = (-6, -6)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Beam.positions = #'(-6 . -6)
                } {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 16.** Beam specifier beams nothing:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=False,
                ...         ),
                ...     )

            ::

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 11/16
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
                }

        ..  container:: example

            **Example 17.** Nesting specifier augments one sixteenth:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).beam.positions = (-5.5, -5.5)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Beam.positions = #'(-5.5 . -5.5)
                } {
                    {
                        \time 3/4
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
                }

        ..  container:: example

            **Example 18.** Nesting specifier augments first two stages
            one sixteenth:

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

                >>> figure_token = [
                ...     [0, 2, 10, 18],
                ...     [16, 15, 23],
                ...     [19, 13, 9, 8],
                ...     ]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> override(staff).beam.positions = (-5.5, -5.5)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff \with {
                    \override Beam.positions = #'(-5.5 . -5.5)
                } {
                    {
                        \time 3/4
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
                }

        ..  container:: example

            **Example 19.** Sixteenths followed by eighths:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 15/16
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
                }

        ..  container:: example

            **Example 20.** Sixteenths surrounding dotted eighths:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 19/16
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
                }

        ..  container:: example

            **Example 21.** Sixteenths surrounding argumented dotted eighths:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 5/4
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
                }

        ..  container:: example

            **Example 22.** Augmented sixteenths surrounding dotted eighths:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 5/4
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
                }

        ..  container:: example

            **Example 23.** Diminished sixteenths surrounding dotted eighths:

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

                >>> figure_token = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> result = figure_maker(figure_token)
                >>> selection, time_signature, state_manifest = result
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     [selection],
                ...     [time_signature],
                ...     pitched_staff=True,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> class_ = rhythmmakertools.RhythmMaker
                >>> staff = class_._get_staff(lilypond_file)
                >>> f(staff)
                \new Staff {
                    {
                        \time 9/8
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
                }

        Defaults to none.

        Set to specifiers or none.

        Returns specifiers or none.
        '''
        return self._specifiers