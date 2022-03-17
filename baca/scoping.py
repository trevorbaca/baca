"""
Scoping.
"""
import dataclasses
import os
import typing
from inspect import currentframe as _frame

import abjad

from . import indicators as _indicators
from . import memento as _memento
from . import tags as _tags
from . import typings


def _attach_color_redraw_literal(
    wrapper, status, existing_deactivate=None, existing_tag=None
):
    if not getattr(wrapper.indicator, "redraw", False):
        return
    if getattr(wrapper.indicator, "hide", False):
        return
    attach_color_literal(
        wrapper,
        status,
        existing_deactivate=wrapper.deactivate,
        redraw=True,
    )


def _attach_color_cancelation_literal(
    wrapper, status, existing_deactivate=None, existing_tag=None
):
    if getattr(wrapper.indicator, "latent", False):
        return
    if getattr(wrapper.indicator, "hide", False):
        return
    if not getattr(wrapper.indicator, "redraw", False):
        return
    attach_color_literal(
        wrapper,
        status,
        existing_deactivate=wrapper.deactivate,
        cancelation=True,
    )


def _attach_latent_indicator_alert(
    manifests, wrapper, status, existing_deactivate=None
):
    if not getattr(wrapper.indicator, "latent", False):
        return
    leaf = wrapper.component
    indicator = wrapper.indicator
    assert indicator.latent, repr(indicator)
    if isinstance(indicator, abjad.Clef):
        return
    key = _indicator_to_key(indicator, manifests)
    if key is not None:
        key = f"“{key}”"
    else:
        key = type(indicator).__name__
    if isinstance(indicator, abjad.Instrument):
        if status == "default":
            tag = _tags.DEFAULT_INSTRUMENT_ALERT
        elif status == "explicit":
            tag = _tags.EXPLICIT_INSTRUMENT_ALERT
        elif status == "reapplied":
            tag = _tags.REAPPLIED_INSTRUMENT_ALERT
        else:
            assert status == "redundant", repr(status)
            tag = _tags.REDUNDANT_INSTRUMENT_ALERT
        left, right = "(", ")"
    else:
        assert isinstance(indicator, abjad.MarginMarkup)
        if status == "default":
            tag = _tags.DEFAULT_MARGIN_MARKUP_ALERT
        elif status == "explicit":
            tag = _tags.EXPLICIT_MARGIN_MARKUP_ALERT
        elif status == "reapplied":
            tag = _tags.REAPPLIED_MARGIN_MARKUP_ALERT
        else:
            assert status == "redundant", repr(status)
            tag = _tags.REDUNDANT_MARGIN_MARKUP_ALERT
        left, right = "[", "]"
    assert isinstance(tag, abjad.Tag), repr(tag)
    string = f"{left}{key}{right}"
    markup_function = _status_to_markup_function[status]
    string = rf'\{markup_function} "{string}"'
    markup = abjad.Markup(string)
    tag = tag.append(site(_frame()))
    abjad.attach(
        markup, leaf, deactivate=existing_deactivate, direction=abjad.Up, tag=tag
    )


def _get_key(dictionary, value):
    if dictionary is not None:
        for key, value_ in dictionary.items():
            if value_ == value:
                return key


def _get_tag(status, stem, prefix=None, suffix=None):
    stem = abjad.string.delimit_words(stem)
    stem = "_".join([_.upper() for _ in stem])
    if suffix is not None:
        name = f"{status.upper()}_{stem}_{suffix.upper()}"
    else:
        name = f"{status.upper()}_{stem}"
    if prefix is not None:
        name = f"{prefix.upper()}_{name}"
    tag = getattr(_tags, name)
    return tag


def _indicator_to_grob(indicator):
    if isinstance(indicator, abjad.Dynamic):
        return "DynamicText"
    elif isinstance(indicator, abjad.Instrument):
        return "InstrumentName"
    elif isinstance(indicator, abjad.MetronomeMark):
        return "TextScript"
    elif isinstance(indicator, abjad.MarginMarkup):
        return "InstrumentName"
    elif isinstance(indicator, _indicators.StaffLines):
        return "StaffSymbol"
    return type(indicator).__name__


def _indicator_to_key(indicator, manifests):
    if isinstance(indicator, abjad.Clef):
        key = indicator.name
    elif isinstance(indicator, abjad.Dynamic):
        if indicator.name == "niente":
            key = "niente"
        else:
            key = indicator.command or indicator.name
    elif isinstance(indicator, abjad.StartHairpin):
        key = indicator.shape
    elif isinstance(indicator, abjad.Instrument):
        key = _get_key(manifests["abjad.Instrument"], indicator)
    elif isinstance(indicator, abjad.MetronomeMark):
        key = _get_key(manifests["abjad.MetronomeMark"], indicator)
    elif isinstance(indicator, abjad.MarginMarkup):
        key = _get_key(manifests["abjad.MarginMarkup"], indicator)
    elif isinstance(indicator, _memento.PersistentOverride):
        key = indicator
    elif isinstance(indicator, _indicators.BarExtent):
        key = indicator.line_count
    elif isinstance(indicator, _indicators.StaffLines):
        key = indicator.line_count
    elif isinstance(indicator, _indicators.Accelerando | _indicators.Ritardando):
        key = {"hide": indicator.hide}
    else:
        key = str(indicator)
    return key


def _set_status_tag(wrapper, status, redraw=None, stem=None):
    assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
    stem = stem or to_indicator_stem(wrapper.indicator)
    prefix = None
    if redraw is True:
        prefix = "redrawn"
    tag = wrapper.tag.append(site(_frame()))
    status_tag = _get_tag(status, stem, prefix=prefix)
    tag = tag.append(status_tag)
    wrapper.tag = tag


_status_to_color = {
    "default": "DarkViolet",
    "explicit": "blue",
    "reapplied": "green4",
    "redundant": "DeepPink1",
}


_status_to_markup_function = {
    "default": "baca-default-indicator-markup",
    "explicit": "baca-explicit-indicator-markup",
    "reapplied": "baca-reapplied-indicator-markup",
    "redundant": "baca-redundant-indicator-markup",
}

_status_to_redraw_color = {
    "default": "violet",
    "explicit": "DeepSkyBlue2",
    "reapplied": "OliveDrab",
    "redundant": "DeepPink4",
}


def attach_color_literal(
    wrapper,
    status,
    existing_deactivate=None,
    redraw=False,
    cancelation=False,
):
    assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
    if getattr(wrapper.indicator, "hide", False) is True:
        return
    if isinstance(wrapper.indicator, abjad.Instrument):
        return
    if not getattr(wrapper.indicator, "persistent", False):
        return
    if getattr(wrapper.indicator, "parameter", None) == "METRONOME_MARK":
        return
    if isinstance(wrapper.indicator, _memento.PersistentOverride):
        return
    if isinstance(wrapper.indicator, _indicators.BarExtent):
        return
    stem = to_indicator_stem(wrapper.indicator)
    grob = _indicator_to_grob(wrapper.indicator)
    context = wrapper._find_correct_effective_context()
    assert isinstance(context, abjad.Context), repr(context)
    string = rf"\override {context.lilypond_type}.{grob}.color ="
    if cancelation is True:
        string += " ##f"
    elif redraw is True:
        color = _status_to_redraw_color[status]
        string += f" #(x11-color '{color})"
    else:
        string = rf"\once {string}"
        color = _status_to_color[status]
        string += f" #(x11-color '{color})"
    if redraw:
        literal = abjad.LilyPondLiteral(string, format_slot="after")
    else:
        literal = abjad.LilyPondLiteral(string)
    if getattr(wrapper.indicator, "latent", False):
        if redraw:
            prefix = "redrawn"
        else:
            prefix = None
        if cancelation:
            suffix = "color_cancellation"
        else:
            suffix = "color"
    else:
        prefix = None
        if redraw:
            suffix = "redraw_color"
        elif cancelation:
            suffix = "color_cancellation"
        else:
            suffix = "color"
    status_tag = _get_tag(status, stem, prefix=prefix, suffix=suffix)
    if isinstance(wrapper.indicator, abjad.TimeSignature):
        string = rf"\baca-time-signature-color #'{color}"
        literal = abjad.LilyPondLiteral(string)
    if cancelation is True:
        tag = site(_frame(), n=1)
        tag = tag.append(status_tag)
        abjad.attach(literal, wrapper.component, deactivate=True, tag=tag)
    else:
        tag = site(_frame(), n=2)
        tag = tag.append(status_tag)
        abjad.attach(
            literal,
            wrapper.component,
            deactivate=existing_deactivate,
            tag=tag,
        )


def treat_persistent_wrapper(manifests, wrapper, status):
    assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
    assert bool(wrapper.indicator.persistent), repr(wrapper)
    assert isinstance(status, str), repr(status)
    indicator = wrapper.indicator
    prototype = (
        abjad.Glissando,
        abjad.Ottava,
        abjad.RepeatTie,
        abjad.StartBeam,
        abjad.StartPhrasingSlur,
        abjad.StartPianoPedal,
        abjad.StartSlur,
        abjad.StartTextSpan,
        abjad.StartTrillSpan,
        abjad.StopBeam,
        abjad.StopPhrasingSlur,
        abjad.StopPianoPedal,
        abjad.StopSlur,
        abjad.StopTextSpan,
        abjad.StopTrillSpan,
        abjad.Tie,
    )
    if isinstance(indicator, prototype):
        return
    context = wrapper._find_correct_effective_context()
    assert isinstance(context, abjad.Context), repr(wrapper)
    leaf = wrapper.component
    assert isinstance(leaf, abjad.Leaf), repr(wrapper)
    existing_tag = wrapper.tag
    tempo_trend = (_indicators.Accelerando, _indicators.Ritardando)
    if isinstance(indicator, abjad.MetronomeMark) and abjad.get.has_indicator(
        leaf, tempo_trend
    ):
        status = "explicit"
    if isinstance(wrapper.indicator, abjad.Dynamic) and abjad.get.indicators(
        leaf, abjad.StartHairpin
    ):
        status = "explicit"
    if isinstance(wrapper.indicator, abjad.Dynamic | abjad.StartHairpin):
        color = _status_to_color[status]
        words = [
            f"{status.upper()}_DYNAMIC_COLOR",
            "_treat_persistent_wrapper(1)",
        ]
        words.extend(existing_tag.editions())
        words = [str(_) for _ in words]
        string = ":".join(words)
        tag_ = abjad.Tag(string)
        string = f"#(x11-color '{color})"
        abjad.tweak(wrapper.indicator, tag=tag_).color = string
        _set_status_tag(wrapper, status)
        return
    attach_color_literal(wrapper, status, existing_deactivate=wrapper.deactivate)
    _attach_latent_indicator_alert(
        manifests, wrapper, status, existing_deactivate=wrapper.deactivate
    )
    _attach_color_cancelation_literal(
        wrapper,
        status,
        existing_deactivate=wrapper.deactivate,
        existing_tag=existing_tag,
    )
    if isinstance(wrapper.indicator, abjad.Clef):
        string = rf"\set {context.lilypond_type}.forceClef = ##t"
        literal = abjad.LilyPondLiteral(string)
        wrapper_ = abjad.attach(
            literal,
            wrapper.component,
            tag=wrapper.tag.append(site(_frame(), n=2)),
            wrapper=True,
        )
        _set_status_tag(wrapper_, status, stem="CLEF")
    _set_status_tag(wrapper, status)
    _attach_color_redraw_literal(
        wrapper,
        status,
        existing_deactivate=wrapper.deactivate,
        existing_tag=existing_tag,
    )
    if isinstance(indicator, abjad.Instrument | abjad.MarginMarkup) and not getattr(
        indicator, "hide", False
    ):
        strings = indicator._get_lilypond_format(context=context)
        literal = abjad.LilyPondLiteral(strings, format_slot="after")
        stem = to_indicator_stem(indicator)
        wrapper_ = abjad.attach(
            literal,
            leaf,
            tag=existing_tag.append(site(_frame(), n=3)),
            wrapper=True,
        )
        _set_status_tag(wrapper_, status, redraw=True, stem=stem)


@dataclasses.dataclass(slots=True)
class Scope:
    """
    Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     measures=(1, 9),
        ...     voice_name="ViolinMusicVoice",
        ... )
        >>> scope
        Scope(measures=(1, 9), voice_name='ViolinMusicVoice')

    """

    # TODO: reverse order of parameters; make voice_name mandatory

    measures: typings.SliceTyping = (1, -1)
    voice_name: str | None = None

    def __post_init__(self):
        if isinstance(self.measures, int):
            self.measures = (self.measures, self.measures)
        assert isinstance(self.measures, list | tuple), repr(self.measures)
        assert len(self.measures) == 2, repr(self.measures)
        start, stop = self.measures
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        assert isinstance(self.voice_name, str), repr(self.voice_name)


@dataclasses.dataclass(slots=True)
class TimelineScope:
    """
    Timeline scope.

    ..  container:: example

        >>> scope = baca.timeline([
        ...     ("PianoMusicVoice", (5, 9)),
        ...     ("ClarinetMusicVoice", (7, 12)),
        ...     ("ViolinMusicVoice", (8, 12)),
        ...     ("OboeMusicVoice", (9, 12)),
        ... ])

        >>> scope
        TimelineScope(scopes=(Scope(measures=(5, 9), voice_name='PianoMusicVoice'), Scope(measures=(7, 12), voice_name='ClarinetMusicVoice'), Scope(measures=(8, 12), voice_name='ViolinMusicVoice'), Scope(measures=(9, 12), voice_name='OboeMusicVoice')))

        ..  container:: example

            >>> baca.TimelineScope()
            TimelineScope(scopes=None)

    """

    scopes: typing.Any = None

    voice_name = "Timeline_Scope"

    def __post_init__(self):
        if self.scopes is not None:
            assert isinstance(self.scopes, tuple | list)
            scopes_ = []
            for scope in self.scopes:
                if not isinstance(scope, Scope):
                    scope = Scope(*scope)
                scopes_.append(scope)
            scopes = scopes_
            scopes = tuple(scopes)
            self.scopes = scopes


ScopeTyping: typing.TypeAlias = Scope | TimelineScope


def apply_tweaks(argument, tweaks, i=None, total=None):
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


def remove_reapplied_wrappers(leaf, indicator):
    if not getattr(indicator, "persistent", False):
        return
    if getattr(indicator, "parameter", None) == "TEXT_SPANNER":
        return
    if abjad.get.timespan(leaf).start_offset != 0:
        return
    dynamic_prototype = (abjad.Dynamic, abjad.StartHairpin)
    tempo_prototype = (
        abjad.MetronomeMark,
        _indicators.Accelerando,
        _indicators.Ritardando,
    )
    if isinstance(indicator, abjad.Instrument):
        prototype = abjad.Instrument
    elif isinstance(indicator, dynamic_prototype):
        prototype = dynamic_prototype
    elif isinstance(indicator, tempo_prototype):
        prototype = tempo_prototype
    else:
        prototype = type(indicator)
    stem = to_indicator_stem(indicator)
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
            counter = abjad.string.pluralize("indicator", count)
            message = f"found {count} reapplied {counter};"
            message += " expecting 1.\n\n"
            raise Exception(message)
        return reapplied_indicators[0]


def to_indicator_stem(indicator) -> str:
    """
    Changes ``indicator`` to stem.

    ..  container:: example

        >>> baca.scoping.to_indicator_stem(abjad.Clef("alto"))
        'CLEF'

        >>> baca.scoping.to_indicator_stem(abjad.Clef("treble"))
        'CLEF'

        >>> baca.scoping.to_indicator_stem(abjad.Dynamic("f"))
        'DYNAMIC'

        >>> baca.scoping.to_indicator_stem(abjad.StartHairpin("<"))
        'DYNAMIC'

        >>> baca.scoping.to_indicator_stem(abjad.Cello())
        'INSTRUMENT'

        >>> baca.scoping.to_indicator_stem(abjad.Violin())
        'INSTRUMENT'

        >>> metronome_mark = abjad.MetronomeMark((1, 4), 58)
        >>> baca.scoping.to_indicator_stem(metronome_mark)
        'METRONOME_MARK'

        >>> start_text_span = abjad.StartTextSpan()
        >>> baca.scoping.to_indicator_stem(start_text_span)
        'TEXT_SPANNER'

        >>> stop_text_span = abjad.StopTextSpan()
        >>> baca.scoping.to_indicator_stem(stop_text_span)
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
    return abjad.string.to_shout_case(stem)


def validate_indexed_tweaks(tweaks):
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


def _validate_tags(tags):
    assert isinstance(tags, list), repr(tags)
    assert "" not in tags, repr(tags)
    assert not any(":" in _ for _ in tags), repr(tags)
    return True


@dataclasses.dataclass(slots=True)
class Command:
    """
    Command.
    """

    deactivate: bool = False
    map: typing.Any = None
    match: typings.Indices = None
    measures: typings.SliceTyping = None
    scope: ScopeTyping | None = None
    selector: typing.Callable | None = None
    tag_measure_number: bool = False
    tags: list[abjad.Tag | None] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self._runtime = {}
        if self.selector is not None:
            assert callable(self.selector)
        self.tags = list(self.tags or [])
        assert _validate_tags(self.tags)
        self._initialize_tags(self.tags)

    def __call__(self, argument=None, runtime: dict = None) -> None:
        """
        Calls command on ``argument``.
        """
        self._runtime = runtime or {}
        if self.map is not None:
            assert callable(self.map)
            argument = self.map(argument)
            for subargument in argument:
                self._call(argument=subargument)
        else:
            return self._call(argument=argument)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}()"

    def _call(self, argument=None):
        pass

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

    @property
    def runtime(self) -> dict:
        """
        Gets segment-commands runtime dictionary.
        """
        return self._runtime

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

    # TODO: replace in favor of self.tag(leaf)
    def get_tag(self, leaf: abjad.Leaf = None) -> abjad.Tag | None:
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


@dataclasses.dataclass
class Suite:
    """
    Suite.

    ..  container:: example

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ...     selector=baca.selectors.pleaves(),
        ... )

        >>> suite
        Suite(commands=(IndicatorCommand(), IndicatorCommand()))

    ..  container:: example

        REGRESSION. Templating works like this:

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ... )
        >>> suite.commands[0].measures
        (1, 2)

        >>> new_suite = baca.suite(suite.commands, measures=(3, 4))
        >>> new_suite.commands[0].measures
        (3, 4)

    """

    commands: typing.Sequence["CommandTyping"] = ()
    keywords: dict | None = None

    def __post_init__(self):
        self.commands = self.commands or []
        assert all(isinstance(_, Command | Suite) for _ in self.commands)
        keywords = self.keywords or {}
        commands_ = []
        for item in self.commands:
            if isinstance(item, Command):
                item_ = dataclasses.replace(item, **keywords)
            else:
                item_ = Suite([new(_, **keywords) for _ in item.commands])
            commands_.append(item_)
        self.commands = tuple(commands_)

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
        Gets repr.
        """
        return f"{type(self).__name__}(commands={self.commands})"


CommandTyping: typing.TypeAlias = Command | Suite


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

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=baca.selectors.leaves((4, -3)),
        ...     ),
        ...     baca.make_even_divisions(),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
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
                    }
                >>
            }

    ..  container:: example

        Applies measure selector to commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=lambda _: baca.select.cmgroups(_)[1:-1],
        ...     ),
        ...     baca.make_even_divisions(),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
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
                    }
                >>
            }

    """
    result = []
    assert all(isinstance(_, Command | Suite) for _ in commands), repr(commands)
    for item in commands:
        item_: Command | Suite
        if isinstance(item, Command):
            item_ = dataclasses.replace(item, **keywords)
        else:
            item_ = Suite([new(_, **keywords) for _ in item.commands])
        result.append(item_)
    if len(result) == 1:
        return result[0]
    else:
        return suite(*result)


_command_typing = Command | Suite


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

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.only_parts(
        ...         baca.hairpin("p < f"),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'2
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        b'4.
                        b'2
                        b'4.
                        \f
                    }
                >>
            }

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


def site(frame, self=None, *, n=None):
    """
    Makes site from ``frame``.
    """
    parts = []
    path = frame.f_code.co_filename.removesuffix(".py")
    found_library = False
    for part in reversed(path.split(os.sep)):
        parts.append(part)
        if part == "baca":
            break
        if found_library:
            break
        if part == "library":
            found_library = True
    parts = [_ for _ in parts if _ != "library"]
    parts.reverse()
    if parts[0] == "baca":
        parts.pop()
    if isinstance(self, str):
        parts.append(self)
    elif self is not None:
        parts.append(type(self).__name__)
    parts.append(frame.f_code.co_name)
    string = ".".join(parts) + ("()" if n is None else f"({n})")
    return abjad.Tag(string)


def suite(*commands: CommandTyping, **keywords) -> Suite:
    """
    Makes suite.

    ..  container:: example exception

        Raises exception on noncommand:

        >>> baca.suite("Allegro")
        Traceback (most recent call last):
            ...
        Exception:
            Must contain only commands and suites.
            Not str:
            'Allegro'

    """
    commands_: list[Command | Suite] = []
    for item in commands:
        if isinstance(item, list | tuple):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if isinstance(command, Command | Suite):
            continue
        message = "\n  Must contain only commands and suites."
        message += f"\n  Not {type(command).__name__}:"
        message += f"\n  {repr(command)}"
        raise Exception(message)
    return Suite(commands_, keywords)


def tag(
    tags: abjad.Tag | list[abjad.Tag],
    command: CommandTyping,
    *,
    deactivate: bool = False,
    tag_measure_number: bool = False,
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
    assert _validate_tags(tags), repr(tags)
    if not isinstance(command, Command | Suite):
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
        command.tags.extend(tags_)
        command.deactivate = deactivate
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
