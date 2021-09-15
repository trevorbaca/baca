"""
Scoping.
"""
import functools
import inspect
import typing

import abjad

from . import indicators
from . import tags as _tags
from . import typings

### CLASSES ###


class Scope:
    """
    Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     measures=(1, 9),
        ...     voice_name='ViolinMusicVoice',
        ...     )

        >>> string = abjad.storage(scope)
        >>> print(string)
        baca.Scope(
            measures=(1, 9),
            voice_name='ViolinMusicVoice',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_measures", "_voice_name")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        measures: typings.SliceTyping = (1, -1),
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
    def measures(self) -> abjad.IntegerPair:
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


class TimelineScope:
    """
    Timeline scope.

    ..  container:: example

        >>> scope = baca.timeline([
        ...     ('PianoMusicVoice', (5, 9)),
        ...     ('ClarinetMusicVoice', (7, 12)),
        ...     ('ViolinMusicVoice', (8, 12)),
        ...     ('OboeMusicVoice', (9, 12)),
        ...     ])

        >>> string = abjad.storage(scope)
        >>> print(string)
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

    __slots__ = ("_scopes",)

    ### INITIALIZER ###

    def __init__(self, *, scopes=None):
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
            start_offset_1 = abjad.get.timespan(leaf_1).start_offset
            start_offset_2 = abjad.get.timespan(leaf_2).start_offset
            if start_offset_1 < start_offset_2:
                return -1
            if start_offset_2 < start_offset_1:
                return 1
            index_1 = abjad.get.parentage(leaf_1).score_index()
            index_2 = abjad.get.parentage(leaf_2).score_index()
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
        String constant set to  ``'Timeline_Scope'``.
        """
        return "Timeline_Scope"


ScopeTyping = typing.Union[Scope, TimelineScope]


class Command:
    """
    Command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_deactivate",
        "_map",
        "_match",
        "_measures",
        "_offset_to_measure_number",
        "_previous_segment_voice_metadata",
        "_runtime",
        "_scope",
        "_score_template",
        "_selector",
        "_tag_measure_number",
        "_tags",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: ScopeTyping = None,
        selector: abjad.Expression = None,
        tag_measure_number: bool = None,
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
    ) -> None:
        self._deactivate = deactivate
        self._map = map
        self._match = match
        self._measures: typing.Optional[typings.SliceTyping] = measures
        self._runtime = abjad.OrderedDict()
        self._scope = scope
        selector_ = selector
        if selector_ is not None and not callable(selector_):
            message = "selector must be callable:\n"
            message += f"   {repr(selector_)}"
            raise Exception(message)
        self._selector = selector_
        self._tag_measure_number = tag_measure_number
        self._initialize_tags(tags)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None, runtime: abjad.OrderedDict = None) -> None:
        """
        Calls command on ``argument``.
        """
        if runtime is not None:
            assert isinstance(runtime, abjad.OrderedDict)
        self._runtime = runtime or abjad.OrderedDict()
        if self.map is not None:
            assert callable(self.map)
            argument = self.map(argument)
            if (
                hasattr(self.map, "_is_singular_get_item")
                and self.map._is_singular_get_item()
            ):
                raise Exception("ASDF")
                argument = [argument]
            for subargument in argument:
                self._call(argument=subargument)
        else:
            return self._call(argument=argument)

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
        literals = []
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
            assert isinstance(manager_, abjad.TweakInterface)
            literals.append(bool(manager_._literal))
            if manager_._literal is True:
                manager._literal = True
            tuples = manager_._get_attribute_tuples()
            for attribute, value in tuples:
                setattr(manager, attribute, value)
        if True in literals and False in literals:
            message = "all tweaks must be literal"
            message += ", or else all tweaks must be nonliteral:\n"
            strings = [f"    {repr(_)}" for _ in tweaks]
            string = "\n".join(strings)
            message += string
            raise Exception(message)

    def _call(self, argument=None):
        pass

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    def _initialize_tags(self, tags):
        tags_ = []
        for tag in tags or []:
            if tag in (None, ""):
                continue
            elif isinstance(tag, str):
                for word in tag.split(":"):
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
            assert len(self.match) == 2
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
            tags = tags.split(":")
        assert isinstance(tags, list), repr(tags)
        tags_: typing.List[typing.Union[str, abjad.Tag]] = []
        for item in tags:
            if isinstance(item, abjad.Tag):
                tags_.append(item)
            else:
                assert isinstance(item, str), repr(item)
                tags_.extend(item.split(":"))
        return tags_

    @staticmethod
    def _remove_reapplied_wrappers(leaf, indicator):
        if not getattr(indicator, "persistent", False):
            return
        if getattr(indicator, "parameter", None) == "TEXT_SPANNER":
            return
        if abjad.get.timespan(leaf).start_offset != 0:
            return
        dynamic_prototype = (abjad.Dynamic, abjad.StartHairpin)
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
        stem = Command._to_indicator_stem(indicator)
        assert stem in (
            "BAR_EXTENT",
            "BEAM",
            "CLEF",
            "DYNAMIC",
            "INSTRUMENT",
            "MARGIN_MARKUP",
            "METRONOME_MARK",
            "OTTAVA",
            "PEDAL",
            "PERSISTENT_OVERRIDE",
            "PHRASING_SLUR",
            "REPEAT_TIE",
            "SLUR",
            "STAFF_LINES",
            "TIE",
            "TRILL",
        ), repr(stem)
        reapplied_wrappers = []
        reapplied_indicators = []
        wrappers = list(abjad.get.wrappers(leaf))
        effective_wrapper = abjad.get.effective_wrapper(leaf, prototype)
        if effective_wrapper and effective_wrapper not in wrappers:
            component = effective_wrapper.component
            start_1 = abjad.get.timespan(leaf).start_offset
            start_2 = abjad.get.timespan(component).start_offset
            if start_1 == start_2:
                wrappers_ = abjad.get.wrappers(component)
                wrappers.extend(wrappers_)
        for wrapper in wrappers:
            if not wrapper.tag:
                continue
            is_reapplied_wrapper = False
            for word in abjad.Tag(wrapper.tag):
                if f"REAPPLIED_{stem}" in word or f"DEFAULT_{stem}" in word:
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
                counter = abjad.String("indicator").pluralize(count)
                message = f"found {count} reapplied {counter};"
                message += " expecting 1.\n\n"
                raise Exception(message)
            return reapplied_indicators[0]

    @staticmethod
    def _to_indicator_stem(indicator) -> abjad.String:
        """
        Changes ``indicator`` to stem.

        ..  container:: example

            >>> baca.Command._to_indicator_stem(abjad.Clef("alto"))
            'CLEF'

            >>> baca.Command._to_indicator_stem(abjad.Clef("treble"))
            'CLEF'

            >>> baca.Command._to_indicator_stem(abjad.Dynamic("f"))
            'DYNAMIC'

            >>> baca.Command._to_indicator_stem(abjad.StartHairpin("<"))
            'DYNAMIC'

            >>> baca.Command._to_indicator_stem(abjad.Cello())
            'INSTRUMENT'

            >>> baca.Command._to_indicator_stem(abjad.Violin())
            'INSTRUMENT'

            >>> metronome_mark = abjad.MetronomeMark((1, 4), 58)
            >>> baca.Command._to_indicator_stem(metronome_mark)
            'METRONOME_MARK'

            >>> start_text_span = abjad.StartTextSpan()
            >>> baca.Command._to_indicator_stem(start_text_span)
            'TEXT_SPANNER'

            >>> stop_text_span = abjad.StopTextSpan()
            >>> baca.Command._to_indicator_stem(stop_text_span)
            'TEXT_SPANNER'

        """
        assert getattr(indicator, "persistent", False), repr(indicator)
        if isinstance(indicator, abjad.Instrument):
            stem = "INSTRUMENT"
        elif getattr(indicator, "parameter", None) == "TEMPO":
            stem = "METRONOME_MARK"
        elif hasattr(indicator, "parameter"):
            stem = indicator.parameter
        else:
            stem = type(indicator).__name__
        return abjad.String(stem).to_shout_case()

    @staticmethod
    def _validate_indexed_tweaks(tweaks):
        if tweaks is None:
            return
        assert isinstance(tweaks, tuple), repr(tweaks)
        for tweak in tweaks:
            if isinstance(tweak, abjad.TweakInterface):
                continue
            if (
                isinstance(tweak, tuple)
                and len(tweak) == 2
                and isinstance(tweak[0], abjad.TweakInterface)
            ):
                continue
            raise Exception(tweak)

    @staticmethod
    def _validate_tags(tags):
        assert isinstance(tags, list), repr(tags)
        assert "" not in tags, repr(tags)
        assert not any(":" in _ for _ in tags), repr(tags)
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
    def measures(self) -> typing.Optional[typings.SliceTyping]:
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
    # TODO: always return tag (never none) for in-place append
    @property
    def tag(self) -> abjad.Tag:
        """
        Gets tag.
        """
        # TODO: replace self.get_tag() functionality
        words = [str(_) for _ in self.tags]
        string = ":".join(words)
        tag = abjad.Tag(string)
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
            start_offset = abjad.get.timespan(leaf).start_offset
            measure_number = self.runtime["offset_to_measure_number"].get(start_offset)
            if getattr(self, "after", None) is True:
                measure_number += 1
            if measure_number is not None:
                tag = abjad.Tag(f"MEASURE_{measure_number}")
                tags.append(tag)
        if tags:
            words = [str(_) for _ in tags]
            string = ":".join(words)
            tag = abjad.Tag(string)
            return tag
        # TODO: return empty tag (instead of none)
        return None


class Suite:
    """
    Suite.

    ..  container:: example

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ...     selector=baca.selectors.pleaves(),
        ...     )

        >>> string = abjad.storage(suite)
        >>> print(string)
        baca.Suite(
            baca.IndicatorCommand(
                abjad.CyclicTuple(
                    [
                        abjad.Articulation('>'),
                        ]
                    ),
                measures=(1, 2),
                selector=...,
                tags=[
                    abjad.Tag('baca.accent()'),
                    ],
                ),
            baca.IndicatorCommand(
                abjad.CyclicTuple(
                    [
                        abjad.Articulation('tenuto'),
                        ]
                    ),
                measures=(1, 2),
                selector=...,
                tags=[
                    abjad.Tag('baca.tenuto()'),
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
        >>> string = abjad.storage(suite)
        >>> print(string)
        baca.Suite(
            baca.IndicatorCommand(
                abjad.CyclicTuple(
                    [
                        abjad.Articulation('>'),
                        ]
                    ),
                measures=(1, 2),
                selector=...,
                tags=[
                    abjad.Tag('baca.accent()'),
                    ],
                ),
            baca.IndicatorCommand(
                abjad.CyclicTuple(
                    [
                        abjad.Articulation('tenuto'),
                        ]
                    ),
                measures=(1, 2),
                selector=...,
                tags=[
                    abjad.Tag('baca.tenuto()'),
                    ],
                )
            )

        >>> new_suite = abjad.new(suite, measures=(3, 4))
        >>> string = abjad.storage(new_suite)
        >>> print(string)
        baca.Suite(
            baca.IndicatorCommand(
                abjad.CyclicTuple(
                    [
                        abjad.Articulation('>'),
                        ]
                    ),
                measures=(3, 4),
                selector=...,
                tags=[
                    abjad.Tag('baca.accent()'),
                    ],
                ),
            baca.IndicatorCommand(
                abjad.CyclicTuple(
                    [
                        abjad.Articulation('tenuto'),
                        ]
                    ),
                measures=(3, 4),
                selector=...,
                tags=[
                    abjad.Tag('baca.tenuto()'),
                    ],
                )
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_commands",
        "_offset_to_measure_number",
        "_previous_segment_voice_metadata",
        "_score_template",
    )

    ### INITIALIZER ###

    def __init__(
        self, commands: typing.Sequence["CommandTyping"] = None, **keywords
    ) -> None:
        commands_: typing.List[CommandTyping] = []
        for command in commands or []:
            if isinstance(command, (Command, Suite)):
                command_ = abjad.new(command, **keywords)
                commands_.append(command_)
                continue
            message = "\n  Must contain only commands, maps, suites."
            message += f"\n  Not {type(command).__name__}: {command!r}."
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
        manager = abjad.StorageFormatManager(self)
        names = list(manager.signature_keyword_names)
        return abjad.FormatSpecification(
            self,
            storage_format_args_values=self.commands,
            storage_format_keyword_names=names,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple["CommandTyping", ...]:
        """
        Gets commands.
        """
        return self._commands


CommandTyping = typing.Union[Command, Suite]


### FACTORY FUNCTIONS ###


def chunk(*commands: CommandTyping, **keywords) -> Suite:
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


def new(*commands: CommandTyping, **keywords) -> CommandTyping:
    r"""
    Makes new ``commands`` with ``keywords``.

    ..  container:: example

        Applies leaf selector to commands:

        >>> maker = baca.SegmentMaker(
        ...     includes=["baca.ily"],
        ...     preamble=[baca.global_context_string()],
        ...     score_template=baca.make_empty_score_maker(1),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=baca.selectors.leaves((4, -3)),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context GlobalContext = "Global_Context"
                <<
                    \context GlobalSkips = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                >>
                \context MusicContext = "Music_Context"
                {
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            b'8
                            [
                            b'8
                            b'8
                            b'8
                            ]
                            b'8
                            - \marcato
                            - \staccato
                            [
                            (
                            b'8
                            - \marcato
                            - \staccato
                            b'8
                            - \marcato
                            - \staccato
                            ]
                            b'8
                            - \marcato
                            - \staccato
                            [
                            b'8
                            - \marcato
                            - \staccato
                            b'8
                            - \marcato
                            - \staccato
                            b'8
                            - \marcato
                            - \staccato
                            )
                            ]
                            b'8
                            [
                            b'8
                            b'8
                            ]
                            <<
                                \context Voice = "Music_Voice"
                                {
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                                \context Voice = "Rest_Voice"
                                {
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                            >>
                        }
                    }
                }
            >>

    ..  container:: example

        Applies measure selector to commands:

        >>> maker = baca.SegmentMaker(
        ...     includes=["baca.ily"],
        ...     preamble=[baca.global_context_string()],
        ...     score_template=baca.make_empty_score_maker(1),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=lambda _: baca.Selection(_).cmgroups()[1:-1],
        ...         ),
        ...     baca.make_even_divisions(),
        ...     )

        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context GlobalContext = "Global_Context"
                <<
                    \context GlobalSkips = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                >>
                \context MusicContext = "Music_Context"
                {
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            b'8
                            [
                            b'8
                            b'8
                            b'8
                            ]
                            b'8
                            - \marcato
                            - \staccato
                            [
                            (
                            b'8
                            - \marcato
                            - \staccato
                            b'8
                            - \marcato
                            - \staccato
                            ]
                            b'8
                            - \marcato
                            - \staccato
                            [
                            b'8
                            - \marcato
                            - \staccato
                            b'8
                            - \marcato
                            - \staccato
                            b'8
                            - \marcato
                            - \staccato
                            )
                            ]
                            b'8
                            [
                            b'8
                            b'8
                            ]
                            <<
                                \context Voice = "Music_Voice"
                                {
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                                \context Voice = "Rest_Voice"
                                {
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                            >>
                        }
                    }
                }
            >>

    """
    commands_: typing.List[CommandTyping] = []
    for command in commands:
        assert isinstance(command, (Command, Suite)), repr(command)
        command_ = abjad.new(command, **keywords)
        commands_.append(command_)
    if len(commands_) == 1:
        return commands_[0]
    else:
        return suite(*commands_)


_command_typing = typing.Union[Command, Suite]


def not_mol(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``NOT_MOL`` (not middle-of-line).
    """
    return tag(_tags.NOT_MOL, command, tag_measure_number=True)


def not_parts(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``-PARTS``.
    """
    return tag(_tags.NOT_PARTS, command)


def not_score(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``-SCORE``.
    """
    return tag(_tags.NOT_SCORE, command)


def not_segment(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``-SEGMENT``.
    """
    return tag(_tags.NOT_SEGMENT, command)


def only_mol(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``ONLY_MOL`` (only middle-of-line).
    """
    return tag(_tags.ONLY_MOL, command, tag_measure_number=True)


def only_parts(command: _command_typing) -> _command_typing:
    r"""
    Tags ``command`` with ``+PARTS``.

    ..  container:: example

        REGRESSION. Dynamic status color tweaks copy dynamic edition tags:

        >>> maker = baca.SegmentMaker(
        ...     includes=["baca.ily"],
        ...     preamble=[baca.global_context_string()],
        ...     score_template=baca.make_empty_score_maker(1),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.only_parts(
        ...         baca.hairpin('p < f'),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context GlobalContext = "Global_Context"
                <<
                    \context GlobalSkips = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                >>
                \context MusicContext = "Music_Context"
                {
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            b'2
                            - \tweak color #(x11-color 'blue)
                            \p
                            - \tweak color #(x11-color 'blue)
                            \<
                            b'4.
                            b'2
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \f
                            <<
                                \context Voice = "Music_Voice"
                                {
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                                \context Voice = "Rest_Voice"
                                {
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                            >>
                        }
                    }
                }
            >>

    """
    return tag(_tags.ONLY_PARTS, command)


def only_score(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``+SCORE``.
    """
    return tag(_tags.ONLY_SCORE, command)


def only_segment(command: _command_typing) -> _command_typing:
    """
    Tags ``command`` with ``+SEGMENT``.
    """
    return tag(_tags.ONLY_SEGMENT, command)


def site(frame, prefix, *, n=None) -> abjad.Tag:
    """
    Makes site from ``frame``.

    ..  todo:: Determine prefix dynamically.

    """
    frame_info = inspect.getframeinfo(frame)
    if n is None:
        string = f"{prefix}.{frame_info.function}()"
    else:
        string = f"{prefix}.{frame_info.function}({n})"
    return abjad.Tag(string)


def suite(*commands: CommandTyping, **keywords) -> Suite:
    """
    Makes suite.

    ..  container:: example exception

        Raises exception on noncommand:

        >>> baca.suite('Allegro')
        Traceback (most recent call last):
            ...
        Exception:
            Must contain only commands and suites.
            Not str:
            'Allegro'

    """
    commands_: typing.List[typing.Union[Command, Suite]] = []
    for item in commands:
        if isinstance(item, (list, tuple)):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if isinstance(command, (Command, Suite)):
            continue
        message = "\n  Must contain only commands and suites."
        message += f"\n  Not {type(command).__name__}:"
        message += f"\n  {repr(command)}"
        raise Exception(message)
    return Suite(commands_, **keywords)


def tag(
    tags: typing.Union[abjad.Tag, typing.List[abjad.Tag]],
    command: CommandTyping,
    *,
    deactivate: bool = None,
    tag_measure_number: bool = None,
) -> CommandTyping:
    """
    Appends each tag in ``tags`` to ``command``.

    Sorts ``command`` tags.

    Acts in place.
    """
    if isinstance(tags, abjad.Tag):
        tags = [tags]
    if not isinstance(tags, list):
        message = "tags must be tag or list of tags"
        message += f" (not {tags!r})."
        raise Exception(message)
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    assert Command._validate_tags(tags), repr(tags)
    if not isinstance(command, (Command, Suite)):
        raise Exception("can only tag command or suite.")
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
        try:
            tags.sort()
        except TypeError:
            pass
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
