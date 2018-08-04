import abjad
import copy
import functools
import typing
from . import classes
from . import indicators
from . import typings


### CLASSES ###

class Scope(abjad.AbjadObject):
    """
    Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     measures=(1, 9),
        ...     voice_name='ViolinMusicVoice',
        ...     )

        >>> abjad.f(scope, strict=89)
        baca.Scope(
            measures=(1, 9),
            voice_name='ViolinMusicVoice',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_measures',
        '_voice_name',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        measures: typing.Union[int, typing.Tuple[int, int]] = (1, -1),
        voice_name: str = None,
        ) -> None:
        if isinstance(measures, int):
            measures = (measures, measures)
        assert isinstance(measures, tuple), repr(measures)
        assert len(measures) == 2, repr(measures)
        start, stop = measures
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        self._measures = measures
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def measures(self) -> typing.Tuple[int, int]:
        """
        Gets measures.
        """
        return self._measures

    @property
    def voice_name(self) -> typing.Optional[str]:
        """
        Gets voice name.
        """
        return self._voice_name

class TimelineScope(abjad.AbjadObject):
    """
    Timeline scope.

    ..  container:: example

        >>> scope = baca.timeline([
        ...     ('PianoMusicVoice', (5, 9)),
        ...     ('ClarinetMusicVoice', (7, 12)),
        ...     ('ViolinMusicVoice', (8, 12)),
        ...     ('OboeMusicVoice', (9, 12)),
        ...     ])

        >>> abjad.f(scope, strict=89)
        baca.TimelineScope(
            scopes=(
                baca.Scope(
                    measures=(5, 9),
                    voice_name='PianoMusicVoice',
                    ),
                baca.Scope(
                    measures=(7, 12),
                    voice_name='ClarinetMusicVoice',
                    ),
                baca.Scope(
                    measures=(8, 12),
                    voice_name='ViolinMusicVoice',
                    ),
                baca.Scope(
                    measures=(9, 12),
                    voice_name='OboeMusicVoice',
                    ),
                ),
            )

        ..  container:: example

            >>> baca.TimelineScope()
            TimelineScope()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_scopes',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        scopes=None,
        ):
        if scopes is not None:
            assert isinstance(scopes, (tuple, list))
            scopes_ = []
            for scope in scopes:
                if not isinstance(scope, Scope):
                    scope = Scope(*scope)
                scopes_.append(scope)
            scopes = scopes_
            scopes = tuple(scopes)
        self._scopes = scopes

    ### PRIVATE METHODS ###

    @staticmethod
    def _sort_by_timeline(leaves):
        assert leaves.are_leaves(), repr(leaves)
        def compare(leaf_1, leaf_2):
            start_offset_1 = abjad.inspect(leaf_1).timespan().start_offset
            start_offset_2 = abjad.inspect(leaf_2).timespan().start_offset
            if start_offset_1 < start_offset_2:
                return -1
            if start_offset_2 < start_offset_1:
                return 1
            index_1 = abjad.inspect(leaf_1).parentage().score_index
            index_2 = abjad.inspect(leaf_2).parentage().score_index
            if index_1 < index_2:
                return -1
            if index_2 < index_1:
                return 1
            return 0
        leaves = list(leaves)
        leaves.sort(key=functools.cmp_to_key(compare))
        return abjad.select(leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def scopes(self) -> typing.Tuple[Scope]:
        """
        Gets scopes.
        """
        return self._scopes

    @property
    def voice_name(self) -> str:
        """
        Returns ``'TimelineScope'``.
        """
        return 'TimelineScope'

scope_typing = typing.Union[
    Scope,
    TimelineScope,
    ]

class Command(abjad.AbjadObject):
    """
    Command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_deactivate',
        '_map',
        '_match',
        '_measures',
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_runtime',
        '_scope',
        '_score_template',
        '_selector',
        '_tag_measure_number',
        '_tags',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scope_typing = None,
        selector: typings.Selector = None,
        tag_measure_number: bool = None,
        ) -> None:
        # for selector evaluation
        import baca
        self._deactivate = deactivate
        self._map = map
        self._match = match
        self._measures: typings.Slice = None
        self._runtime = abjad.OrderedDict()
        self.scope = scope
        if isinstance(selector, str):
            selector_ = eval(selector)
        else:
            selector_ = selector
        if selector_ is not None:
            assert isinstance(selector_, abjad.Expression), repr(selector_)
        self._selector = selector_
        self._tags: typing.Optional[typing.List[abjad.Tag]] = None
        self.tag_measure_number = tag_measure_number

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if self.map is not None:
            assert isinstance(self.map, abjad.Expression)
            argument = self.map(argument)
            if self.map._is_singular_get_item():
                argument = [argument]
            for subargument in argument:
                self._call(argument=subargument)
        else:
            return self._call(argument=argument)

    ### PRIVATE METHODS ###

    @staticmethod
    def _apply_tweaks(argument, tweaks):
        if not tweaks:
            return
        manager = abjad.tweak(argument)
        for manager_ in tweaks:
            tuples = manager_._get_attribute_tuples()
            for attribute, value in tuples:
                setattr(manager, attribute, value)

    def _call(self, argument=None):
        pass

    def _matches_scope_index(self, scope_count, i):
        if isinstance(self.match, int):
            if 0 <= self.match and self.match != i:
                return False
            if self.match < 0 and -(scope_count - i) != self.match:
                return False
        elif isinstance(self.match, tuple):
            assert len(self.match) == 2, repr(command)
            triple = slice(*self.match).indices(scope_count)
            if i not in range(*triple):
                return False
        elif isinstance(self.match, list):
            assert all(isinstance(_, int) for _ in self.match)
            if i not in self.match:
                return False
        return True

    def _override_scope(self, scope):
        assert isinstance(scope, (Scope, TimelineScope)), repr(scope)
        if not self.measures:
            return scope
        if isinstance(self.measures, int):
            measures = (self.measures, self.measures)
        else:
            assert isinstance(self.measures, tuple), repr(self.measures)
            measures = self.measures
        scope_ = abjad.new(
            scope,
            measures=measures,
            )
        return scope_

    @staticmethod
    def _remove_reapplied_wrappers(leaf, indicator):
        if not getattr(indicator, 'persistent', False):
            return
        # TODO: getattr(indicator, 'parameter', NONE) == # 'TEXT_SPAN'
        prototype = (abjad.StartTextSpan, abjad.StopTextSpan)
        if isinstance(indicator, prototype):
            return
        if abjad.inspect(leaf).timespan().start_offset != 0:
            return
        dynamic_prototype = (
            abjad.Dynamic,
            abjad.DynamicTrend,
            )
        tempo_prototype = (
            abjad.MetronomeMark,
            indicators.Accelerando,
            indicators.Ritardando,
            )
        if isinstance(indicator, abjad.Instrument):
            prototype = abjad.Instrument
        elif isinstance(indicator, dynamic_prototype):
            prototype = dynamic_prototype
        elif isinstance(indicator, tempo_prototype):
            prototype = tempo_prototype
        else:
            prototype = type(indicator)
        stem = abjad.String.to_indicator_stem(indicator)
        assert stem in (
            'CLEF',
            'DYNAMIC',
            'INSTRUMENT',
            'MARGIN_MARKUP',
            'METRONOME_MARK',
            'PERSISTENT_OVERRIDE',
            'STAFF_LINES',
            ), repr(stem)
        reapplied_wrappers = []
        reapplied_indicators = []
        wrappers = list(abjad.inspect(leaf).wrappers())
        effective_wrapper = abjad.inspect(leaf).effective_wrapper(prototype)
        if effective_wrapper and effective_wrapper not in wrappers:
            component = effective_wrapper.component
            start_1 = abjad.inspect(leaf).timespan().start_offset
            start_2 = abjad.inspect(component).timespan().start_offset
            if start_1 == start_2:
                wrappers_ = abjad.inspect(component).wrappers()
                wrappers.extend(wrappers_)
        for wrapper in wrappers:
            if not wrapper.tag:
                continue
            is_reapplied_wrapper = False
            for word in abjad.Tag(wrapper.tag):
                if f'REAPPLIED_{stem}' in word or f'DEFAULT_{stem}' in word:
                    is_reapplied_wrapper = True
            if not is_reapplied_wrapper:
                continue
            reapplied_wrappers.append(wrapper)
            if isinstance(wrapper.indicator, prototype):
                reapplied_indicators.append(wrapper.indicator)
            abjad.detach(wrapper, wrapper.component)
        if reapplied_wrappers:
            count = len(reapplied_indicators)
            if count != 1:
                for reapplied_wrapper in reapplied_wrappers:
                    print(reapplied_wrapper)
                counter = abjad.String('indicator').pluralize(count)
                message = f'found {count} reapplied {counter};'
                message += ' expecting 1.\n\n'
                raise Exception(message)
            return reapplied_indicators[0]

    @staticmethod
    def _validate_tags(tags):
        assert isinstance(tags, list), repr(tags)
        assert '' not in tags, repr(tags)
        assert not any(':' in _ for _ in tags), repr(tags)
        return True

    @staticmethod
    def _validate_tweaks(tweaks):
        if tweaks is None:
            return
        assert isinstance(tweaks, tuple), repr(tweaks)
        for tweak in tweaks:
            if not isinstance(tweak, abjad.LilyPondTweakManager):
                raise Exception(tweaks)

    ### PUBLIC PROPERTIES ###

    @property
    def deactivate(self) -> typing.Optional[bool]:
        """
        Is true when command deactivates tag.
        """
        return self._deactivate

    @property
    def map(self) -> typing.Union[str, abjad.Expression, None]:
        """
        Gets precondition map.
        """
        return self._map

    @map.setter
    def map(self, argument):
        """
        Gets precondition map.
        """
        assert isinstance(argument, (str, abjad.Expression)), repr(argument)
        self._map = argument

    @property
    def match(self) -> typing.Optional[typings.Indices]:
        """
        Gets match.
        """
        return self._match

    @property
    def measures(self) -> typing.Optional[typings.Slice]:
        """
        Gets measures.
        """
        return self._measures

    @measures.setter
    def measures(self, argument):
        """
        Gets measures.
        """
        if argument is not None:
            assert isinstance(argument, (int, tuple, list)), repr(argument)
        self._measures = argument

    @property
    def runtime(self) -> abjad.OrderedDict:
        """
        Gets segment-maker runtime dictionary.
        """
        return self._runtime

    @runtime.setter
    def runtime(self, argument):
        """
        Gets segment-maker runtime dictionary.
        """
        assert isinstance(argument, abjad.OrderedDict), repr(argument)
        self._runtime = argument

    @property
    def scope(self) -> scope_typing:
        """
        Gets scope.
        """
        return self._scope

    @scope.setter
    def scope(self, argument):
        """
        Gets scope.
        """
        if argument is not None:
            assert isinstance(argument, (Scope, TimelineScope))
        self._scope = argument

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets selector.
        """
        return self._selector

    # TODO: reimplement as method with leaf argument
    # TODO: supply with all self.get_tag(leaf) functionality
    # TODO: always return tag (never none) for in-place prepend
    @property
    def tag(self) -> abjad.Tag:
        """
        Gets tag.
        """
        # TODO: replace self.get_tag() functionality
        words = [str(_) for _ in self.tags]
        tag = abjad.Tag.from_words(words)
        assert isinstance(tag, abjad.Tag)
        return tag

    @property
    def tag_measure_number(self) -> typing.Optional[bool]:
        """
        Is true when command tags measure number.
        """
        return self._tag_measure_number

    @tag_measure_number.setter
    def tag_measure_number(self, argument):
        assert argument in (True, False, None), repr(argument)
        self._tag_measure_number = argument
        for command in getattr(self, 'commands', []):
            command._tag_measure_number = argument

    @property
    def tags(self) -> typing.List[abjad.Tag]:
        """
        Gets tags.
        """
        assert self._validate_tags(self._tags)
        result: typing.List[abjad.Tag] = []
        if self._tags:
            result = self._tags[:]
        return result

    ### PUBLIC METHODS ###

    # TODO: replace in favor of self.tag(leaf)
    def get_tag(self, leaf: abjad.Leaf = None) -> typing.Optional[abjad.Tag]:
        """
        Gets tag for ``leaf``.
        """
        tags = self.tags[:]
        if self.tag_measure_number:
            start_offset = abjad.inspect(leaf).timespan().start_offset
            measure_number = self.runtime[
                'offset_to_measure_number'].get(start_offset)
            if measure_number is not None:
                tag = abjad.Tag(f'MEASURE_{measure_number}')
                tags.append(tag)
        if tags:
            words = [str(_) for _ in tags]
            words.sort()
            tag = abjad.Tag.from_words(words)
            return tag
        # TODO: return empty tag (instead of none)
        return None

class Suite(abjad.AbjadObject):
    """
    Suite.

    ..  container:: example

        >>> baca.Suite()
        Suite()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_measures',
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_score_template',
        '_runtime',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *commands: typing.Union[Command, 'Suite'],
        ) -> None:
        command_list: typing.List[typing.Union[Command, Suite]] = []
        for command in commands:
            if isinstance(command, (Command, Suite)):
                command_list.append(command)
                continue
            message = '\n  Must contain only commands, maps, suites.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
        self._commands = tuple(command_list)
        self._measures: typings.Slice = None
        self._runtime = abjad.OrderedDict()

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies commands to ``argument``.
        """
        if argument is None:
            return
        if not self.commands:
            return
        for command in self.commands:
            command(argument)

    def __iter__(self):
        """
        Iterates commands.
        """
        return iter(self.commands)

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple[typing.Union[Command, 'Suite'], ...]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def map(self) -> None:
        """
        Gets precondition map.
        """
        pass

    @map.setter
    def map(self, argument):
        """
        Gets precondition map.
        """
        assert isinstance(argument, (str, abjad.Expression)), repr(argument)
        for command in self.commands:
            command.map = argument

    @property
    def measures(self) -> typing.Optional[typings.Slice]:
        """
        Gets measures.
        """
        return self._measures

    @measures.setter
    def measures(self, argument):
        """
        Gets measures.
        """
        if argument is not None:
            assert isinstance(argument, (int, tuple, list)), repr(argument)
        for command in self.commands:
            command.measures = argument

    @property
    def runtime(self) -> abjad.OrderedDict:
        """
        Gets segment-maker runtime dictionary.
        """
        return self._runtime

    @runtime.setter
    def runtime(self, argument):
        """
        Gets segment-maker runtime dictionary.
        """
        assert isinstance(argument, abjad.OrderedDict), repr(argument)
        for command in self.commands:
            command.runtime = argument

### FACTORY FUNCTIONS ###

def apply(
    selector: typings.Selector,
    *commands: typing.Iterable[Command],
    ) -> typing.List[Command]:
    r"""
    Applies ``selector`` to each command in ``commands``.

    ..  container:: example

        Applies leaf selector to commands:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.apply(
        ...         baca.leaves()[4:-3],
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            [
                            (                                                                        %! SC
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            ]
                            )                                                                        %! SC
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Applies measure selector to commands:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.apply(
        ...         baca.mgroups()[1:-1],
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            [
                            (                                                                        %! SC
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            -\marcato                                                                %! IndicatorCommand
                            -\staccato                                                               %! IndicatorCommand
                            ]
                            )                                                                        %! SC
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM_24
                            c'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Raises exception on nonselector input:

        >>> baca.apply(99, baca.staccato())
        Traceback (most recent call last):
            ...
        Exception:
            Selector must be str or expression.
            Not 99.

    """
    if not isinstance(selector, (str, abjad.Expression)):
        message = '\n  Selector must be str or expression.'
        message += f'\n  Not {selector!r}.'
        raise Exception(message)
    commands_: typing.List[Command] = []
    for command in commands:
        assert isinstance(command, Command), repr(command)
        command_ = abjad.new(command, selector=selector)
        commands_.append(command_)
    return commands_

def map(
    selector: typing.Union[abjad.Expression, str],
    *commands: typing.Union[Command, Suite],
    ) -> typing.List[typing.Union[Command, Suite]]:
    """
    Maps ``selector`` to each command in ``commands``.
    """
    if not isinstance(selector, (abjad.Expression, str)):
        message = '\n  Map selector must be expression or string.'
        message += f'\n  Not {format(selector)}.'
        raise Exception(message)
    if not commands:
        raise Exception('map commands must not be empty.')
    commands_ = []
    for item in commands:
        if isinstance(item, (list, tuple)):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if not isinstance(command, (Command, Suite)):
            message = '\n  Must be command or suite.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
    result = []
    for command in commands_:
        command.map = selector
        result.append(command)
    return result

# TODO: change to baca.scope()
def match(
    pattern,
    *commands: typing.Union[Command, Suite],
    ) -> typing.List[typing.Union[Command, Suite]]:
    """
    Applies each scope that matches ``pattern`` to each command in
    ``commands``.
    """
    if pattern is not None:
        assert isinstance(pattern, (int, tuple, list)), repr(pattern)
    result: typing.List[typing.Union[Command, Suite]] = []
    for command in commands:
        if isinstance(command, Command):
            command_ = abjad.new(command, match=pattern)
        else:
            assert isinstance(command, Suite), repr(command)
            commands_ = []
            for command_ in command:
                command_ = abjad.new(command_, match=pattern)
                commands_.append(command_)
            command_ = Suite(*commands_)
        result.append(command_)
    return result

def measures(
    measures: typing.Optional[typings.Slice],
    *commands: typing.Union[Command, Suite],
    ) -> typing.List[typing.Union[Command, Suite]]:
    r"""
    Wraps each command in ``commands`` with ``measures``.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 16)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.measures(
        ...         (1, 2),
        ...         baca.make_even_divisions(),
        ...         ),
        ...     baca.measures(
        ...         (3, 4),
        ...         baca.make_repeat_tied_notes(),
        ...         ),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca_bar_line_visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            f'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f'4.
                            \repeatTie
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    commands_ = []
    for command in classes.Sequence(commands).flatten(depth=-1):
        assert isinstance(command, (Command, Suite)), repr(command)
        command.measures = copy.copy(measures)
        commands_.append(command)
    return commands_

_command_typing = typing.Union[Command, Suite]

def not_parts(command: Command) -> _command_typing:
    """
    Tags ``command`` with ``-PARTS``.

    Returns ``command``.
    """
    return tag('-PARTS', command)

def not_score(command: Command) -> _command_typing:
    """
    Tags ``command`` with ``-SCORE``.

    Returns ``command``.
    """
    return tag('-SCORE', command)

def not_segment(command: Command) -> _command_typing:
    """
    Tags ``command`` with ``-SEGMENT``.

    Returns ``command``.
    """
    return tag('-SEGMENT', command)

def only_parts(command: Command) -> _command_typing:
    """
    Tags ``command`` with ``+PARTS``.

    Returns ``command``.
    """
    return tag('+PARTS', command)

def only_score(command: Command) -> _command_typing:
    """
    Tags ``command`` with ``+SCORE``.

    Returns ``command``.
    """
    return tag('+SCORE', command)

def only_segment(command: Command) -> _command_typing:
    """
    Tags ``command`` with ``+SEGMENT``.

    Returns ``command``.
    """
    return tag('+SEGMENT', command)

def suite(
    *commands: typing.Union[Command, Suite],
    ) -> Suite:
    """
    Makes suite.

    ..  container:: example

        Raises exception on noncommand:

        >>> baca.suite('Allegro')
        Traceback (most recent call last):
            ...
        Exception:
            Must contain only commands, maps, suites.
            Not str:
            Allegro

    """
    commands_ = []
    for item in commands:
        if isinstance(item, (list, tuple)):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if isinstance(command, (Command, Suite)):
            continue
        message = '\n  Must contain only commands, maps, suites.'
        message += f'\n  Not {type(command).__name__}:'
        message += f'\n  {format(command)}'
        raise Exception(message)
    return Suite(*commands_)

def tag(
    tags: typing.Union[str, typing.List[str]],
    command: typing.Union[Command, Suite],
    *,
    deactivate: bool = None,
    tag_measure_number: bool = None,
    ) -> typing.Union[Command, Suite]:
    """
    Appends each tag in ``tags`` to ``command``.

    Sorts ``command`` tags.

    Returns ``command`` for in-place definition file application.
    """
    if isinstance(tags, str):
        tags = [tags]
    if not isinstance(tags, list):
        message = f'tags must be string or list of strings'
        message += f' (not {tags!r}).'
        raise Exception(message)
    assert Command._validate_tags(tags), repr(tags)
    if not isinstance(command, (Command, Suite)):
        raise Exception('can only tag command or suite.')
    if isinstance(command, Suite):
        for command_ in command.commands:
            tag(
                tags,
                command_,
                deactivate=deactivate,
                tag_measure_number=tag_measure_number,
                )
    else:
        assert isinstance(command, Command), repr(command)
        assert command._tags is not None
        tags.sort()
        tags_ = [abjad.Tag(_) for _ in tags]
        command._tags.extend(tags_)
        command._deactivate = deactivate
        command.tag_measure_number = tag_measure_number
    return command

def timeline(scopes) -> TimelineScope:
    """
    Makes timeline scope.
    """
    scopes_ = []
    for scope in scopes:
        voice_name, measures = scope
        scope_ = Scope(measures=measures, voice_name=voice_name)
        scopes_.append(scope_)
    return TimelineScope(scopes=scopes_)
