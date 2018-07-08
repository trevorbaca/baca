import abjad
import functools
import typing
from . import indicatorlib
from . import typings


### CLASSES ###

class Command(abjad.AbjadObject):
    """
    Command.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'

    __slots__ = (
        '_deactivate',
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_runtime',
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
        selector: typings.Selector = None,
        tag_measure_number: bool = None,
        ) -> None:
        # for selector evaluation
        import baca
        self._deactivate = deactivate
        self._runtime = abjad.OrderedDict()
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
        pass

    ### PRIVATE METHODS ###

    def _apply_tweaks(self, argument):
        if not self.tweaks:
            return
        manager = abjad.tweak(argument)
        for manager_ in self.tweaks:
            tuples = manager_._get_attribute_tuples()
            for attribute, value in tuples:
                setattr(manager, attribute, value)

    @staticmethod
    def _remove_reapplied_wrappers(leaf, indicator):
        if not getattr(indicator, 'persistent', False):
            return
        if abjad.inspect(leaf).get_timespan().start_offset != 0:
            return
        tempo_prototype = (
            abjad.MetronomeMark,
            indicatorlib.Accelerando,
            indicatorlib.Ritardando,
            )
        if isinstance(indicator, abjad.Instrument):
            prototype = abjad.Instrument
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
            start_1 = abjad.inspect(leaf).get_timespan().start_offset
            start_2 = abjad.inspect(component).get_timespan().start_offset
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
                message = f'found {count} reapplied indicator(s);'
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
            start_offset = abjad.inspect(leaf).get_timespan().start_offset
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

class Map(abjad.AbjadObject):
    r"""
    Map.

    ..  container:: example

        >>> baca.Map()
        Map()

    ..  container:: example

        Attaches accents to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.apply(
        ...             baca.pheads(),
        ...             baca.marcato(),
        ...             baca.staccato(),
        ...             ),
        ...         baca.slur(
        ...             abjad.tweak(abjad.Down).direction,
        ...             ),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            [
                            - \tweak direction #down                                                 %! SC
                            (                                                                        %! SC
                            e''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            ]
                            ef''4
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            [
                            g''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            ]
                            )                                                                        %! SC
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_runtime',
        '_score_template',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector: typings.Selector = None,
        *commands: typing.Union[Command, 'Map', 'Suite'],
        ) -> None:
        if isinstance(selector, str):
            selector_ = eval(selector)
        else:
            selector_ = selector
        if selector_ is not None:
            assert isinstance(selector_, abjad.Expression), repr(selector_)
        self._selector = selector_
        command_list: typing.List[
            typing.Union[Command, Map, Suite]
            ] = []
        for command in commands:
            if not isinstance(command, (Command, Map, Suite)):
                message = '\n  Must contain only commands and suites.'
                message += f'\n  Not {type(command).__name__}: {command!r}.'
                raise Exception(message)
            command_list.append(command)
        self._commands = tuple(command_list)
        self._runtime = abjad.OrderedDict()

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> typing.Optional[typing.List]:
        """
        Maps each command in ``commands`` to each item in output of selector
        called on ``argument``.
        """
        if argument is None:
            return None
        if not self.commands:
            return None
        if self.selector is not None:
            argument = self.selector(argument)
            if self.selector._is_singular_get_item():
                argument = [argument]
        items_ = []
        for command in self.commands:
            for item in argument:
                item_ = command(item)
                items_.append(item_)
        return items_

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple[
        typing.Union[Command, 'Map', 'Suite'], ...,
        ]:
        """
        Gets commands.
        """
        return self._commands

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

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets selector.
        """
        return self._selector

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
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_score_template',
        '_runtime',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *commands: typing.Union[Command, Map, 'Suite'],
        ) -> None:
        command_list: typing.List[typing.Union[Command, Map, Suite]] = []
        for command in commands:
            if not isinstance(command, (Command, Map, Suite)):
                message = '\n  Must contain only commands, maps, suites.'
                message += f'\n  Not {type(command).__name__}: {command!r}.'
                raise Exception(message)
            command_list.append(command)
        self._commands = tuple(command_list)
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

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple[
        typing.Union[Command, Map, 'Suite'], ...
        ]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def runtime(self) -> abjad.OrderedDict:
        """
        Gets segment-maker runtime.
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

class CommandWrapper(abjad.AbjadObject):
    r"""
    Command wrapper.

    ..  container:: example

        Pitch command wrapped with simple scope:

        >>> command = baca.CommandWrapper(
        ...     command=baca.pitches([7, 1, 3, 4, 5, 11]),
        ...     scope=baca.scope('ViolinMusicVoice', (1, 4)),
        ...     )

        >>> abjad.f(command, strict=89)
        baca.CommandWrapper(
            command=baca.PitchCommand(
                cyclic=True,
                pitches=abjad.CyclicTuple(
                    [
                        abjad.NamedPitch("g'"),
                        abjad.NamedPitch("cs'"),
                        abjad.NamedPitch("ef'"),
                        abjad.NamedPitch("e'"),
                        abjad.NamedPitch("f'"),
                        abjad.NamedPitch("b'"),
                        ]
                    ),
                selector=baca.pleaves(),
                ),
            scope=baca.Scope(
                stages=(1, 4),
                voice_name='ViolinMusicVoice',
                ),
            )

    ..  container:: example

        Pitch command wrapped with timeline scope:

        >>> command = baca.CommandWrapper(
        ...     command=baca.pitches([7, 1, 3, 4, 5, 11]),
        ...     scope=baca.timeline([
        ...         ('ViolinMusicVoice', (1, 4)),
        ...         ('ViolaMusicVoice', (1, 4)),
        ...         ]),
        ...     )

        >>> abjad.f(command, strict=89)
        baca.CommandWrapper(
            command=baca.PitchCommand(
                cyclic=True,
                pitches=abjad.CyclicTuple(
                    [
                        abjad.NamedPitch("g'"),
                        abjad.NamedPitch("cs'"),
                        abjad.NamedPitch("ef'"),
                        abjad.NamedPitch("e'"),
                        abjad.NamedPitch("f'"),
                        abjad.NamedPitch("b'"),
                        ]
                    ),
                selector=baca.pleaves(),
                ),
            scope=baca.TimelineScope(
                scopes=(
                    baca.Scope(
                        stages=(1, 4),
                        voice_name='ViolinMusicVoice',
                        ),
                    baca.Scope(
                        stages=(1, 4),
                        voice_name='ViolaMusicVoice',
                        ),
                    ),
                ),
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'

    __slots__ = (
        '_command',
        '_scope',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        command=None,
        scope=None,
        ):
        if scope is not None:
            prototype = (Scope, TimelineScope)
            assert isinstance(scope, prototype), format(scope)
        self._scope = scope
        if command is not None:
            threeway = (Command, Map, Suite)
            assert isinstance(command, threeway), format(command)
        self._command = command

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        """
        Gets command.

        ..  container:: example

            >>> command = baca.CommandWrapper(
            ...     command=baca.pitches([7, 1, 3, 4, 5, 11]),
            ...     scope=baca.scope('ViolinMusicVoice', (1, 4)),
            ...     )

            >>> abjad.f(command.command, strict=89)
            baca.PitchCommand(
                cyclic=True,
                pitches=abjad.CyclicTuple(
                    [
                        abjad.NamedPitch("g'"),
                        abjad.NamedPitch("cs'"),
                        abjad.NamedPitch("ef'"),
                        abjad.NamedPitch("e'"),
                        abjad.NamedPitch("f'"),
                        abjad.NamedPitch("b'"),
                        ]
                    ),
                selector=baca.pleaves(),
                )

        Defaults to none.

        Set to command or none.

        Returns command or none.
        """
        return self._command

    @property
    def scope(self):
        """
        Gets scope.

        ..  container:: example

            Gets scope:

            >>> command = baca.CommandWrapper(
            ...     command=baca.pitches([7, 1, 3, 4, 5, 11]),
            ...     scope=baca.scope('ViolinMusicVoice', (1, 4)),
            ...     )

            >>> abjad.f(command.scope, strict=89)
            baca.Scope(
                stages=(1, 4),
                voice_name='ViolinMusicVoice',
                )

        Defaults to none.

        Set to scope or none.

        Returns scope or none.
        """
        return self._scope

class MeasureWrapper(abjad.AbjadObject):
    """
    Measure wrapper.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_command',
        '_measures',
        )

    ### INITIALIZER ###

    def __init__(self, *, command=None, measures=None):
        self._command = command
        self._measures = measures

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        """
        Gets command.
        """
        return self._command

    @property
    def measures(self):
        """
        Gets measures.
        """
        return self._measures

class Scope(abjad.AbjadObject):
    """
    Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     stages=(1, 9),
        ...     voice_name='ViolinMusicVoice',
        ...     )

        >>> abjad.f(scope, strict=89)
        baca.Scope(
            stages=(1, 9),
            voice_name='ViolinMusicVoice',
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_stages',
        '_voice_name',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        stages: typing.Tuple[int, int] = None,
        voice_name: str = None,
        ) -> None:
        assert isinstance(stages, tuple), repr(stages)
        assert len(stages) == 2, repr(stages)
        start, stop = stages
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        self._stages = stages
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def stages(self) -> typing.Tuple[int, int]:
        """
        Gets stages.
        """
        return self._stages

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
                    stages=(5, 9),
                    voice_name='PianoMusicVoice',
                    ),
                baca.Scope(
                    stages=(7, 12),
                    voice_name='ClarinetMusicVoice',
                    ),
                baca.Scope(
                    stages=(8, 12),
                    voice_name='ViolinMusicVoice',
                    ),
                baca.Scope(
                    stages=(9, 12),
                    voice_name='OboeMusicVoice',
                    ),
                ),
            )

        ..  container:: example

            >>> baca.TimelineScope()
            TimelineScope()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

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
            start_offset_1 = abjad.inspect(leaf_1).get_timespan().start_offset
            start_offset_2 = abjad.inspect(leaf_2).get_timespan().start_offset
            if start_offset_1 < start_offset_2:
                return -1
            if start_offset_2 < start_offset_1:
                return 1
            index_1 = abjad.inspect(leaf_1).get_parentage().score_index
            index_2 = abjad.inspect(leaf_2).get_parentage().score_index
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

### FACTORY FUNCTIONS ###

def map(
    selector: typing.Union[abjad.Expression, str],
    *commands: typing.Union[Command, Map, Suite],
    ) -> Map:
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
        if not isinstance(command, (Command, Map, Suite)):
            message = '\n  Must be command, map, suite.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
    return Map(selector, *commands_)

def measures(
    measures: typing.Union[int, typing.List[int], typing.Tuple[int, int]],
    *commands: Command,
    ) -> typing.List[MeasureWrapper]:
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
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
                            % [MusicVoice measure 1]                                                 %! SM4
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
                            % [MusicVoice measure 2]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            f'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f'4.
                            \repeatTie
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    wrappers = []
    for command in commands:
        wrapper = MeasureWrapper(
            command=command,
            measures=measures,
            )
        wrappers.append(wrapper)
    return wrappers

def not_parts(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``-PARTS``.

    Returns ``command``.
    """
    return tag('-PARTS', command)

def not_score(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``-SCORE``.

    Returns ``command``.
    """
    return tag('-SCORE', command)

def not_segment(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``-SEGMENT``.

    Returns ``command``.
    """
    return tag('-SEGMENT', command)

def only_parts(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``+PARTS``.

    Returns ``command``.
    """
    return tag('+PARTS', command)

def only_score(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``+SCORE``.

    Returns ``command``.
    """
    return tag('+SCORE', command)

def only_segment(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``+SEGMENT``.

    Returns ``command``.
    """
    return tag('+SEGMENT', command)

def pick(
    pattern,
    *commands: Command,
    ) -> typing.List[typings.Pair]:
    """
    Maps ``pattern`` to each command in ``commands``.
    """
    pairs = []
    for command in commands:
        pair = (command, pattern)
        pairs.append(pair)
    return pairs

def scope(
    voice_name: str,
    stages: typing.Union[int, typing.Tuple[int, int]] = (1, -1),
    ) -> Scope:
    r"""
    Scopes ``voice_name`` for ``stages``.

    ..  container:: example

        >>> baca.scope('HornVoiceI', 1)
        Scope(stages=(1, 1), voice_name='HornVoiceI')

        >>> baca.scope('HornVoiceI', (1, 8))
        Scope(stages=(1, 8), voice_name='HornVoiceI')

        >>> baca.scope('HornVoiceI', (4, -1))
        Scope(stages=(4, -1), voice_name='HornVoiceI')

        >>> baca.scope('HornVoiceI')
        Scope(stages=(1, -1), voice_name='HornVoiceI')

    ..  container:: example

        Negative stage numbers are allowed:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_repeated_duration_notes([(1, 8)]),
        ...     )
        >>> maker(
        ...     ('MusicVoice', (-4, -3)),
        ...     baca.pitch('D4'),
        ...     )
        >>> maker(
        ...     ('MusicVoice', (-2, -1)),
        ...     baca.pitch('E4'),
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
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
                            % [MusicVoice measure 1]                                                 %! SM4
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Raises exception when stages are other than nonzero integers:

        >>> baca.scope('MusicVoice', 0)
        Traceback (most recent call last):
            ...
        Exception: stages must be nonzero integer or pair of nonzero integers (not 0).

        >>> baca.scope('MusicVoice', 'text')
        Traceback (most recent call last):
            ...
        Exception: stages must be nonzero integer or pair of nonzero integers (not 'text').

    """
    message = 'stages must be nonzero integer or pair of nonzero integers'
    message += f' (not {stages!r}).'
    if isinstance(stages, int):
        start, stop = stages, stages
    elif isinstance(stages, tuple):
        assert len(stages) == 2, repr(stages)
        start, stop = stages
    else:
        raise Exception(message)
    if (not isinstance(start, int) or
        not isinstance(stop, int) or 
        start == 0  or
        stop == 0):
        raise Exception(message)
    stages = (start, stop)
    return Scope(
        stages=stages,
        voice_name=voice_name,
        )

def suite(
    *commands: Command,
    ) -> Suite:
    """
    Makes suite.

    ..  container:: example

        Raises exception on noncommand:

        >>> baca.suite(['Allegro'])
        Traceback (most recent call last):
            ...
        Exception:
            Must contain only commands, maps, suites.
            Not list: ['Allegro'].

    """
    for command in commands:
        if not isinstance(command, (Command, Map, Suite)):
            message = '\n  Must contain only commands, maps, suites.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
    return Suite(*commands)

def tag(
    tags: typing.Union[str, typing.List[str]],
    command: typing.Union[Command, Map, Suite, abjad.Markup],
    *,
    deactivate: bool = None,
    tag_measure_number: bool = None,
    ) -> typing.Union[Command, Map, Suite]:
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
    if isinstance(command, abjad.Markup):
        command = markup(command)
    assert Command._validate_tags(tags), repr(tags)
    if isinstance(command, (Map, Suite)):
        for command_ in command.commands:
            tag(
                tags,
                command_,
                deactivate=deactivate,
                tag_measure_number=tag_measure_number,
                )
    else:
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
    scopes = [scope(*_) for _ in scopes]
    return TimelineScope(scopes=scopes)
