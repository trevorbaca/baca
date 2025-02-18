"""
Treat.
"""

from inspect import currentframe as _frame

import abjad

from . import classes as _classes
from . import helpers as _helpers
from . import layout as _layout
from . import memento as _memento
from . import tags as _tags


def _attach_color_literal(
    wrapper,
    status,
    existing_deactivate=None,
    redraw=False,
    cancelation=False,
):
    assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
    unbundled_indicator = wrapper.unbundle_indicator()
    if getattr(unbundled_indicator, "hide", False) is True:
        return
    if isinstance(unbundled_indicator, abjad.Instrument):
        return
    if not getattr(unbundled_indicator, "persistent", False):
        return
    if getattr(unbundled_indicator, "parameter", None) == "METRONOME_MARK":
        return
    if isinstance(unbundled_indicator, _memento.PersistentOverride):
        return
    if isinstance(unbundled_indicator, _classes.BarExtent):
        return
    if isinstance(unbundled_indicator, _layout.SpacingSection):
        return
    stem = _to_indicator_stem(unbundled_indicator)
    grob = _indicator_to_grob(unbundled_indicator)
    context = wrapper._find_correct_effective_context(
        wrapper.component, wrapper.context
    )
    assert isinstance(context, abjad.Context), repr(context)
    string = rf"\override {context.lilypond_type}.{grob}.color ="
    if cancelation is True:
        string += " ##f"
    elif redraw is True:
        color = _status_to_redraw_color[status]
        string += f" #{color}"
    else:
        string = rf"\once {string}"
        color = _status_to_color[status]
        string += f" #{color}"
    if redraw:
        literal = abjad.LilyPondLiteral(string, site="absolute_after")
    else:
        literal = abjad.LilyPondLiteral(string, site="before")
    if getattr(unbundled_indicator, "latent", False):
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
    if isinstance(unbundled_indicator, abjad.TimeSignature):
        if color == "blue":
            string = "#blue"
        else:
            string = f" #{color}"
        string = rf"\baca-time-signature-color {string}"
        literal = abjad.LilyPondLiteral(string, site="before")
    if cancelation is True:
        tag = _helpers.function_name(_frame(), n=1)
        tag = tag.append(status_tag)
        abjad.attach(literal, wrapper.component, deactivate=True, tag=tag)
    else:
        tag = _helpers.function_name(_frame(), n=2)
        tag = tag.append(status_tag)
        abjad.attach(
            literal,
            wrapper.component,
            deactivate=existing_deactivate,
            tag=tag,
        )


def _attach_color_redraw_literal(
    wrapper, status, existing_deactivate=None, existing_tag=None
):
    unbundled_indicator = wrapper.unbundle_indicator()
    if not getattr(unbundled_indicator, "redraw", False):
        return
    if getattr(unbundled_indicator, "hide", False):
        return
    _attach_color_literal(
        wrapper,
        status,
        existing_deactivate=wrapper.deactivate,
        redraw=True,
    )


def _attach_color_cancelation_literal(
    wrapper, status, existing_deactivate=None, existing_tag=None
):
    unbundled_indicator = wrapper.unbundle_indicator()
    if getattr(unbundled_indicator, "latent", False):
        return
    if getattr(unbundled_indicator, "hide", False):
        return
    if not getattr(unbundled_indicator, "redraw", False):
        return
    _attach_color_literal(
        wrapper,
        status,
        existing_deactivate=wrapper.deactivate,
        cancelation=True,
    )


def _attach_latent_indicator_alert(
    manifests, leaf, indicator, status, existing_deactivate=None
):
    if not getattr(indicator, "latent", False):
        return
    assert indicator.latent, repr(indicator)
    if isinstance(indicator, abjad.Clef):
        return
    key = _indicator_to_key(indicator, manifests)
    if key is not None:
        key = f"“{key}”"
    else:
        key = type(indicator).__name__
    if isinstance(indicator, abjad.Instrument):
        if status == "explicit":
            tag = _tags.EXPLICIT_INSTRUMENT_ALERT
        elif status == "reapplied":
            tag = _tags.REAPPLIED_INSTRUMENT_ALERT
        else:
            assert status == "redundant", repr(status)
            tag = _tags.REDUNDANT_INSTRUMENT_ALERT
        left, right = "(", ")"
        markup = _status_to_instrument_markup[status]
        assert isinstance(tag, abjad.Tag), repr(tag)
        string = f"{left}{key}{right}"
        string = rf'\{markup} "{string}"'
        markup = abjad.Markup(string)
        tag = tag.append(_helpers.function_name(_frame()))
        abjad.attach(
            markup, leaf, deactivate=existing_deactivate, direction=abjad.UP, tag=tag
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
    elif isinstance(indicator, abjad.Ottava):
        return "OttavaBracket"
    elif isinstance(indicator, abjad.ShortInstrumentName):
        return "InstrumentName"
    elif isinstance(indicator, _classes.StaffLines):
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
    elif isinstance(indicator, abjad.ShortInstrumentName):
        key = _get_key(manifests["abjad.ShortInstrumentName"], indicator)
    elif isinstance(indicator, abjad.TimeSignature):
        key = f"{indicator.numerator}/{indicator.denominator}"
    elif isinstance(indicator, abjad.VoiceNumber):
        key = indicator.n
    elif isinstance(indicator, abjad.Ottava):
        key = indicator.n
    elif isinstance(indicator, _memento.PersistentOverride):
        key = indicator
    elif isinstance(indicator, _classes.BarExtent):
        key = indicator.line_count
    elif isinstance(indicator, _classes.StaffLines):
        key = indicator.line_count
    elif isinstance(indicator, _classes.Accelerando | _classes.Ritardando):
        key = {"hide": indicator.hide}
    else:
        key = str(indicator)
    return key


def _set_status_tag(wrapper, status, redraw=None, stem=None):
    assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
    unbundled_indicator = wrapper.unbundle_indicator()
    stem = stem or _to_indicator_stem(unbundled_indicator)
    prefix = None
    if redraw is True:
        prefix = "redrawn"
    tag = wrapper.tag
    tag_ = _helpers.function_name(_frame())
    if tag_.string not in tag.string:
        tag = tag.append(tag_)
    status_tag = _get_tag(status, stem, prefix=prefix)
    if status_tag.string not in tag.string:
        tag = tag.append(status_tag)
    wrapper.tag = tag


_status_to_color = {
    "explicit": "blue",
    "reapplied": "(x11-color 'green4)",
    "redundant": "(x11-color 'DeepPink1)",
}


_status_to_instrument_markup = {
    "explicit": "baca-explicit-instrument-markup",
    "reapplied": "baca-reapplied-instrument-markup",
    "redundant": "baca-redundant-instrument-markup",
}

_status_to_short_instrument_name_markup = {
    "explicit": "baca-explicit-short-instrument-name-markup",
    "reapplied": "baca-reapplied-short-instrument-name-markup",
    "redundant": "baca-redundant-short-instrument-name-markup",
}

_status_to_redraw_color = {
    "explicit": "(x11-color 'DeepSkyBlue2)",
    "reapplied": "(x11-color 'OliveDrab)",
    "redundant": "(x11-color 'DeepPink4)",
}


def compare_persistent_indicators(indicator_1, indicator_2) -> bool:
    if type(indicator_1) is not type(indicator_2):
        return False
    if not isinstance(indicator_1, abjad.Dynamic):
        return indicator_1 == indicator_2
    if indicator_1.sforzando or indicator_2.sforzando:
        return False
    if indicator_1.name == indicator_2.name:
        return indicator_1.command == indicator_2.command
    return False


def _to_indicator_stem(indicator) -> str:
    """
    Changes ``indicator`` to stem.

    ..  container:: example

        >>> baca.treat._to_indicator_stem(abjad.Clef("alto"))
        'CLEF'

        >>> baca.treat._to_indicator_stem(abjad.Clef("treble"))
        'CLEF'

        >>> baca.treat._to_indicator_stem(abjad.Dynamic("f"))
        'DYNAMIC'

        >>> baca.treat._to_indicator_stem(abjad.StartHairpin("<"))
        'DYNAMIC'

        >>> baca.treat._to_indicator_stem(abjad.Cello())
        'INSTRUMENT'

        >>> baca.treat._to_indicator_stem(abjad.Violin())
        'INSTRUMENT'

        >>> metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 58)
        >>> baca.treat._to_indicator_stem(metronome_mark)
        'METRONOME_MARK'

        >>> start_text_span = abjad.StartTextSpan()
        >>> baca.treat._to_indicator_stem(start_text_span)
        'TEXT_SPANNER'

        >>> stop_text_span = abjad.StopTextSpan()
        >>> baca.treat._to_indicator_stem(stop_text_span)
        'TEXT_SPANNER'

    """
    assert not isinstance(indicator, abjad.Bundle), repr(indicator)
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


def remove_reapplied_wrappers(leaf, item):
    if isinstance(item, abjad.Bundle):
        indicator = item.indicator
    else:
        indicator = item
    if not getattr(indicator, "persistent", False):
        return
    if getattr(indicator, "parameter", None) == "TEXT_SPANNER":
        return
    if abjad.get.timespan(leaf).start_offset != 0:
        return
    dynamic_prototype = (abjad.Dynamic, abjad.StartHairpin)
    tempo_prototype = (
        abjad.MetronomeMark,
        _classes.Accelerando,
        _classes.Ritardando,
    )
    if isinstance(indicator, abjad.Instrument):
        prototype = abjad.Instrument
    elif isinstance(indicator, dynamic_prototype):
        prototype = dynamic_prototype
    elif isinstance(indicator, tempo_prototype):
        prototype = tempo_prototype
    else:
        prototype = type(indicator)
    stem = _to_indicator_stem(indicator)
    assert stem in (
        "BAR_EXTENT",
        "BEAM",
        "CLEF",
        "DYNAMIC",
        "INSTRUMENT",
        "METRONOME_MARK",
        "OTTAVA",
        "PEDAL",
        "PERSISTENT_OVERRIDE",
        "PHRASING_SLUR",
        "REPEAT_TIE",
        "SHORT_INSTRUMENT_NAME",
        "SLUR",
        "STAFF_LINES",
        "TIE",
        "TRILL",
        "VOICE_NUMBER",
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
        assert isinstance(wrapper.tag, abjad.Tag)
        for word in wrapper.tag.words():
            if f"REAPPLIED_{stem}" in word:
                is_reapplied_wrapper = True
        if not is_reapplied_wrapper:
            continue
        reapplied_wrappers.append(wrapper)
        unbundled_indicator = wrapper.unbundle_indicator()
        if isinstance(unbundled_indicator, prototype):
            reapplied_indicators.append(unbundled_indicator)
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


def treat_persistent_wrapper(
    manifests: dict, wrapper: abjad.Wrapper, status: str
) -> abjad.Wrapper | None:
    assert isinstance(manifests, dict), repr(manifests)
    assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
    assert isinstance(status, str), repr(status)
    unbundled_indicator = wrapper.unbundle_indicator()
    unbundled_indicator.persistent is True, repr(wrapper)
    if getattr(unbundled_indicator, "spanner_stop", False) is True:
        return None
    prototype = (
        abjad.Glissando,
        abjad.RepeatTie,
        abjad.StartBeam,
        abjad.StartPhrasingSlur,
        abjad.StartPianoPedal,
        abjad.StartSlur,
        abjad.StartTextSpan,
        abjad.StartTrillSpan,
        abjad.Tie,
        abjad.VoiceNumber,
    )
    if isinstance(unbundled_indicator, prototype):
        return None
    context = wrapper._find_correct_effective_context(
        wrapper.component, wrapper.context
    )
    assert isinstance(context, abjad.Context), repr(wrapper)
    leaf = wrapper.component
    assert isinstance(leaf, abjad.Leaf), repr(wrapper)
    existing_tag = wrapper.tag
    tempo_trend = (_classes.Accelerando, _classes.Ritardando)
    if isinstance(unbundled_indicator, abjad.MetronomeMark) and abjad.get.has_indicator(
        leaf, tempo_trend
    ):
        status = "explicit"
    if isinstance(unbundled_indicator, abjad.Dynamic) and abjad.get.indicators(
        leaf, abjad.StartHairpin
    ):
        status = "explicit"
    if isinstance(unbundled_indicator, abjad.Dynamic | abjad.StartHairpin):
        color = _status_to_color[status]
        words = [
            f"{status.upper()}_DYNAMIC_COLOR",
            _helpers.function_name(_frame()).string,
        ]
        words.extend(existing_tag.editions())
        words = [_ if isinstance(_, str) else _.string for _ in words]
        string = ":".join(words)
        bundle = abjad.bundle(
            wrapper.indicator,
            rf"- \tweak color #{color}",
            overwrite=True,
            tag=abjad.Tag(string),
        )
        abjad.detach(wrapper, leaf)
        wrapper = abjad.attach(
            bundle,
            leaf,
            context=wrapper.context,
            deactivate=wrapper.deactivate,
            direction=wrapper.direction,
            synthetic_offset=wrapper.synthetic_offset,
            tag=wrapper.tag,
            wrapper=True,
        )
        _set_status_tag(wrapper, status)
        return wrapper
    else:
        _attach_color_literal(wrapper, status, existing_deactivate=wrapper.deactivate)
        _attach_latent_indicator_alert(
            manifests,
            wrapper.component,
            unbundled_indicator,
            status,
            existing_deactivate=wrapper.deactivate,
        )
        _attach_color_cancelation_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
        )
        if isinstance(unbundled_indicator, abjad.Clef):
            string = rf"\set {context.lilypond_type}.forceClef = ##t"
            literal = abjad.LilyPondLiteral(string, site="before")
            wrapper_ = abjad.attach(
                literal,
                wrapper.component,
                tag=wrapper.tag.append(_helpers.function_name(_frame(), n=2)),
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
        if isinstance(
            unbundled_indicator, abjad.Instrument | abjad.ShortInstrumentName
        ) and not getattr(unbundled_indicator, "hide", False):
            strings = unbundled_indicator._get_lilypond_format(context=context)
            literal = abjad.LilyPondLiteral(strings, site="absolute_after")
            stem = _to_indicator_stem(unbundled_indicator)
            wrapper_ = abjad.attach(
                literal,
                leaf,
                tag=existing_tag.append(_helpers.function_name(_frame(), n=3)),
                wrapper=True,
            )
            _set_status_tag(wrapper_, status, redraw=True, stem=stem)
        return None
