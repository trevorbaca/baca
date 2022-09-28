"""
Accumulator.
"""
import dataclasses

import abjad


def _initialize_time_signatures(time_signatures):
    time_signatures = time_signatures or ()
    time_signatures_ = list(time_signatures)
    time_signatures_ = []
    for time_signature in time_signatures:
        if isinstance(time_signature, str):
            time_signature = abjad.TimeSignature.from_string(time_signature)
        else:
            time_signature = abjad.TimeSignature(time_signature)
        time_signatures_.append(time_signature)
    time_signatures_ = tuple(time_signatures_)
    if not time_signatures_:
        time_signatures_ = None
    return time_signatures_


def get_voice_names(score):
    voice_names = ["Skips", "Rests"]
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice.name is not None:
            voice_names.append(voice.name)
            words = voice.name.split(".")
            if "Music" in words:
                rest_voice_name = voice.name.replace("Music", "Rests")
                voice_names.append(rest_voice_name)
            elif "Voice" in words:
                rest_voice_name = f"{voice.name}.Rests"
                voice_names.append(rest_voice_name)
    return tuple(voice_names)


def measures(items):
    time_signatures = [abjad.TimeSignature(_) for _ in items]
    return MeasureServer(time_signatures)


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class CommandAccumulator:

    _voice_abbreviations: dict | None = dataclasses.field(default_factory=dict)
    _voice_names: tuple[str, ...] = dataclasses.field(default_factory=tuple)
    commands: list = dataclasses.field(default_factory=list, init=False)
    time_signatures: list[abjad.TimeSignature] = dataclasses.field(default_factory=list)
    voice_name_to_voice: dict = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        self.time_signatures = _initialize_time_signatures(self.time_signatures)

    def _populate_voice_name_to_voice(self, score):
        for voice in abjad.iterate.components(score, abjad.Voice):
            self.voice_name_to_voice[voice.name] = voice
            for abbreviation, voice_name in self._voice_abbreviations.items():
                if voice_name == voice.name:
                    self.voice_name_to_voice[abbreviation] = voice

    def get(self, start=None, stop=None):
        if start is None and stop is None:
            return self.time_signatures
        assert 0 < start, start
        if stop is None:
            stop = start
        assert 0 < stop, stop
        return self.time_signatures[start - 1 : stop]

    def get_time_signatures(self):
        return _initialize_time_signatures(self.time_signatures)

    def measures(self):
        return MeasureServer(self.time_signatures)

    def voice(self, abbreviation: str) -> abjad.Voice | None:
        assert isinstance(abbreviation, str), repr(abbreviation)
        if abbreviation in self.voice_name_to_voice:
            return self.voice_name_to_voice[abbreviation]
        return None

    def voices(self, abbreviations=None) -> list[abjad.Voice]:
        voices = []
        for abbreviation in abbreviations or self._voice_names:
            if abbreviation in self.voice_name_to_voice:
                voice = self.voice_name_to_voice[abbreviation]
                voices.append(voice)
        return voices


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class MeasureServer:

    time_signatures: list[abjad.TimeSignature]

    def __call__(self, start=None, stop=None):
        if start is None and stop is None:
            return self.time_signatures
        assert 0 < start, start
        if stop is None:
            stop = start
        assert 0 < stop, stop
        return self.time_signatures[start - 1 : stop]
