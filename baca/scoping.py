import abjad
import copy
import functools
import typing
from . import classes
from . import indicators
from . import typings


### CLASSES ###

class Scope(object):
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
        measures: typings.Slice = (1, -1),
        voice_name: str = None,
        ) -> None:
        if isinstance(measures, int):
            measures = (measures, measures)
        assert isinstance(measures, (list, tuple)), repr(measures)
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

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    ### PUBLIC PROPERTIES ###

    @property
    def measures(self) -> typings.IntegerPair:
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

class TimelineScope(object):
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

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

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
            index_1 = abjad.inspect(leaf_1).parentage().score_index()
            index_2 = abjad.inspect(leaf_2).parentage().score_index()
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
        Returns ``'Timeline_Scope'``.
        """
        return 'Timeline_Scope'

ScopeTyping = typing.Union[
    Scope,
    TimelineScope,
    ]

class Command(object):
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
        scope: ScopeTyping = None,
        selector: typings.Selector = None,
        tag_measure_number: bool = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        ) -> None:
        # for selector evaluation
        import baca
        self._deactivate = deactivate
        self._map = map
        self._match = match
        self._measures: typing.Optional[typings.Slice] = measures
        self._runtime = abjad.OrderedDict()
        self._scope = scope
        if isinstance(selector, str):
            selector_ = eval(selector)
        else:
            selector_ = selector
        if selector_ is not None:
            assert isinstance(selector_, abjad.Expression), repr(selector_)
        self._selector = selector_
        self._tag_measure_number = tag_measure_number
        self._initialize_tags(tags)

    ### SPECIAL METHODS ###

    def __call__(
        self,
        argument=None,
        runtime: abjad.OrderedDict = None,
        ) -> None:
        """
        Calls command on ``argument``.
        """
        if runtime is not None:
            assert isinstance(runtime, abjad.OrderedDict)
        self._runtime = runtime or abjad.OrderedDict()
        if self.map is not None:
            assert isinstance(self.map, abjad.Expression)
            argument = self.map(argument)
            if self.map._is_singular_get_item():
                argument = [argument]
            for subargument in argument:
                self._call(argument=subargument)
        else:
            return self._call(argument=argument)

    def __format__(self, format_specification=''):
        """
        Formats object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _apply_tweaks(argument, tweaks, i=None, total=None):
        if not tweaks:
            return
        manager = abjad.tweak(argument)
        for item in tweaks:
            if isinstance(item, tuple):
                assert len(item) == 2
                manager_, i_ = item
                if 0 <= i_ and i_ != i:
                    continue
                if i_ < 0 and i_ != -(total - i):
                    continue
            else:
                manager_ = item
            assert isinstance(manager_, abjad.LilyPondTweakManager)
            tuples = manager_._get_attribute_tuples()
            for attribute, value in tuples:
                setattr(manager, attribute, value)

    def _call(self, argument=None):
        pass

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    def _initialize_tags(self, tags):
        tags_ = []
        for tag in tags or []:
            if tag in (None, ''):
                continue
            elif isinstance(tag, str):
                for word in tag.split(':'):
                    tag_ = abjad.Tag(word)
                    tags_.append(tag_)
            elif isinstance(tag, abjad.Tag):
                tags_.append(tag)
            else:
                raise TypeError(tag)
        assert all(isinstance(_, abjad.Tag) for _ in tags_)
        self._tags = tags_

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

    @staticmethod
    def _preprocess_tags(tags) -> typing.List:
        if tags is None:
            return []
        if isinstance(tags, str):
            tags = tags.split(':')
        assert isinstance(tags, list), repr(tags)
        tags_: typing.List[typing.Union[str, abjad.Tag]] = []
        for item in tags:
            if isinstance(item, abjad.Tag):
                tags_.append(item)
            else:
                assert isinstance(item, str), repr(item)
                tags_.extend(item.split(':'))
        return tags_

    @staticmethod
    def _remove_reapplied_wrappers(leaf, indicator):
        if not getattr(indicator, 'persistent', False):
            return
        if getattr(indicator, 'parameter', None) == 'TEXT_SPANNER':
            return
        if abjad.inspect(leaf).timespan().start_offset != 0:
            return
        dynamic_prototype = (
            abjad.Dynamic,
            abjad.StartHairpin,
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
            'BEAM',
            'CLEF',
            'DYNAMIC',
            'INSTRUMENT',
            'MARGIN_MARKUP',
            'METRONOME_MARK',
            'OTTAVA',
            'PEDAL',
            'PERSISTENT_OVERRIDE',
            'SLUR',
            'STAFF_LINES',
            'TRILL',
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
    def _validate_indexed_tweaks(tweaks):
        if tweaks is None:
            return
        assert isinstance(tweaks, tuple), repr(tweaks)
        for tweak in tweaks:
            if isinstance(tweak, abjad.LilyPondTweakManager):
                continue
            if (isinstance(tweak, tuple) and
                len(tweak) == 2 and
                isinstance(tweak[0], abjad.LilyPondTweakManager)):
                continue
            raise Exception(tweak)

    @staticmethod
    def _validate_tags(tags):
        assert isinstance(tags, list), repr(tags)
        assert '' not in tags, repr(tags)
        assert not any(':' in _ for _ in tags), repr(tags)
        return True

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

    @property
    def runtime(self) -> abjad.OrderedDict:
        """
        Gets segment-maker runtime dictionary.
        """
        return self._runtime

    @property
    def scope(self) -> typing.Optional[ScopeTyping]:
        """
        Gets scope.
        """
        return self._scope

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

class Suite(object):
    """
    Suite.

    ..  container:: example

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ...     selector=baca.pleaves(),
        ...     )

        >>> abjad.f(suite)
        baca.Suite(
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.Articulation('>'),
                        ]
                    ),
                measures=(1, 2),
                selector=baca.pleaves(),
                tags=[
                    abjad.Tag('baca_accent'),
                    ],
                ),
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.Articulation('tenuto'),
                        ]
                    ),
                measures=(1, 2),
                selector=baca.pleaves(),
                tags=[
                    abjad.Tag('baca_tenuto'),
                    ],
                )
            )

    ..  container:: example

        REGRESSION. Works with ``abjad.new()``:

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ...     )
        >>> abjad.f(suite)
        baca.Suite(
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.Articulation('>'),
                        ]
                    ),
                measures=(1, 2),
                selector=baca.phead(0, exclude='HIDDEN'),
                tags=[
                    abjad.Tag('baca_accent'),
                    ],
                ),
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.Articulation('tenuto'),
                        ]
                    ),
                measures=(1, 2),
                selector=baca.phead(0, exclude='HIDDEN'),
                tags=[
                    abjad.Tag('baca_tenuto'),
                    ],
                )
            )

        >>> new_suite = abjad.new(suite, measures=(3, 4))
        >>> abjad.f(new_suite)
        baca.Suite(
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.Articulation('>'),
                        ]
                    ),
                measures=(3, 4),
                selector=baca.phead(0, exclude='HIDDEN'),
                tags=[
                    abjad.Tag('baca_accent'),
                    ],
                ),
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.Articulation('tenuto'),
                        ]
                    ),
                measures=(3, 4),
                selector=baca.phead(0, exclude='HIDDEN'),
                tags=[
                    abjad.Tag('baca_tenuto'),
                    ],
                )
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_offset_to_measure_number',
        '_previous_segment_voice_metadata',
        '_score_template',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        commands: typing.Sequence[typing.Union[Command, 'Suite']] = None,
        **keywords,
        ) -> None:
        commands_: typing.List[typing.Union[Command, Suite]] = []
        for command in commands or []:
            if isinstance(command, (Command, Suite)):
                command_ = abjad.new(command, **keywords)
                commands_.append(command_)
                continue
            message = '\n  Must contain only commands, maps, suites.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
        self._commands = tuple(commands_)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None, runtime=None) -> None:
        """
        Applies each command in ``commands`` to ``argument``.
        """
        if argument is None:
            return
        if not self.commands:
            return
        for command in self.commands:
            command(argument, runtime=runtime)

    def __format__(self, format_specification=''):
        """
        Formats object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __iter__(self):
        """
        Iterates commands.
        """
        return iter(self.commands)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = abjad.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        return abjad.FormatSpecification(
            self,
            storage_format_args_values=self.commands,
            storage_format_kwargs_names=names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple[typing.Union[Command, 'Suite'], ...]:
        """
        Gets commands.
        """
        return self._commands

### FACTORY FUNCTIONS ###

def chunk(
    *commands: typing.Union[Command, Suite],
    **keywords,
    ) -> Suite:
    """
    Chunks commands.
    """
    return suite(*commands, **keywords)

def compare_persistent_indicators(indicator_1, indicator_2) -> bool:
    """
    Compares persistent indicators.
    """
    if type(indicator_1) is not type(indicator_2):
        return False
    if not isinstance(indicator_1, abjad.Dynamic):
        return indicator_1 == indicator_2
    if indicator_1.sforzando or indicator_2.sforzando:
        return False
    if indicator_1.name == indicator_2.name:
        return indicator_1.command == indicator_2.command
    return False

def new(
    *commands: Command,
    **keywords,
    ) -> typing.Union[Command, Suite]:
    r"""
    Makes new ``commands`` with ``keywords``.

    ..  container:: example

        Applies leaf selector to commands:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=baca.leaves()[4:-3],
        ...         ),
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
                            (                                                                        %! baca_slur:SpannerIndicatorCommand(1)
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            )                                                                        %! baca_slur:SpannerIndicatorCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    ..  container:: example

        Applies measure selector to commands:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=baca.cmgroups()[1:-1],
        ...         ),
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
                            (                                                                        %! baca_slur:SpannerIndicatorCommand(1)
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            - \marcato                                                               %! baca_marcato:IndicatorCommand
                            - \staccato                                                              %! baca_staccato:IndicatorCommand
                            )                                                                        %! baca_slur:SpannerIndicatorCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    commands_: typing.List[typing.Union[Command, Suite]] = []
    for command in commands:
        assert isinstance(command, (Command, Suite)), repr(command)
        command_ = abjad.new(command, **keywords)
        commands_.append(command_)
    if len(commands_) == 1:
        return commands_[0]
    else:
        return suite(*commands_)

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

    ..  container:: example

        REGRESSION. Dynamic status color tweaks copy dynamic edition tags:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.only_parts(
        ...         baca.hairpin('p < f'),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'2                                                                      %! baca_make_notes
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1):+PARTS
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:+PARTS:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1):+PARTS
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:+PARTS:PiecewiseCommand(1)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4.                                                                     %! baca_make_notes
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1):+PARTS
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:+PARTS:PiecewiseCommand(2)
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

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
    **keywords,
    ) -> Suite:
    """
    Makes suite.

    ..  container:: example exception

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
    return Suite(commands_, **keywords)

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
        # TODO: maybe use abjad.new() here?
        command._tags.extend(tags_)
        command._deactivate = deactivate
        command._tag_measure_number = tag_measure_number
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
