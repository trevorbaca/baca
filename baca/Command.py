import abc
import abjad
import baca
import typing
from .Typing import Selector


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
        selector: Selector = None,
        tag_measure_number: bool = None,
        ) -> None:
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

    @abc.abstractmethod
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
            baca.Accelerando,
            abjad.MetronomeMark,
            baca.Ritardando,
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
        selector: Selector = None,
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
