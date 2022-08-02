"""
Accumulator.
"""
import dataclasses

import abjad

from . import command as _command


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


def _unpack_measure_token_list(measure_token_list):
    assert isinstance(measure_token_list, list), repr(measure_token_list)
    measure_tokens = []
    for measure_token in measure_token_list:
        if isinstance(measure_token, int):
            measure_tokens.append(measure_token)
        elif isinstance(measure_token, tuple):
            assert len(measure_token) == 2
            start, stop = measure_token
            measure_tokens.append((start, stop))
        else:
            raise TypeError(measure_token_list)
    return measure_tokens


def _unpack_scope_pair(scopes, abbreviations):
    assert isinstance(scopes, tuple), repr(scopes)
    assert len(scopes) == 2, repr(scopes)
    assert isinstance(scopes[0], list | str), repr(scopes)
    assert isinstance(scopes[1], int | list | tuple), repr(scopes)
    if isinstance(scopes[0], str):
        voice_names = [scopes[0]]
    else:
        voice_names = scopes[0]
    assert isinstance(voice_names, list), repr(voice_names)
    assert all(isinstance(_, str) for _ in voice_names)
    measure_tokens = []
    if isinstance(scopes[1], int):
        measure_tokens.append(scopes[1])
    elif isinstance(scopes[1], tuple):
        assert len(scopes[1]) == 2, repr(scopes)
        start, stop = scopes[1]
        measure_tokens.append((start, stop))
    elif isinstance(scopes[1], list):
        measure_tokens = _unpack_measure_token_list(scopes[1])
    else:
        raise TypeError(scopes)
    scopes_ = []
    voice_names_ = []
    for voice_name in voice_names:
        result = abbreviations.get(voice_name, voice_name)
        if isinstance(result, list):
            voice_names_.extend(result)
        else:
            assert isinstance(result, str)
            voice_names_.append(result)
    voice_names = voice_names_
    for voice_name in voice_names:
        for measure_token in measure_tokens:
            scope = _command.Scope(measures=measure_token, voice_name=voice_name)
            scopes_.append(scope)
    assert all(isinstance(_, _command.Scope) for _ in scopes_)
    return scopes_


def _unpack_scopes(scopes, abbreviations):
    if isinstance(scopes, str):
        result = abbreviations.get(scopes, scopes)
        if isinstance(result, str):
            voice_names = [result]
        else:
            assert isinstance(result, list), repr(result)
            voice_names = result
        scopes__ = []
        for voice_name in voice_names:
            scope = _command.Scope(voice_name=voice_name)
            scopes__.append(scope)
    elif isinstance(scopes, tuple):
        scopes__ = _unpack_scope_pair(scopes, abbreviations)
    elif isinstance(scopes, _command.Scope):
        scopes__ = [scopes]
    else:
        assert isinstance(scopes, list), repr(scopes)
        scopes_ = []
        for scope in scopes:
            if isinstance(scope, tuple):
                scopes__ = _unpack_scope_pair(scope, abbreviations)
                scopes_.extend(scopes__)
            else:
                scopes_.append(scope)
        scopes__ = scopes_
    assert isinstance(scopes__, list), repr(scopes__)
    scopes_ = []
    for scope in scopes__:
        if isinstance(scope, str):
            voice_name = abbreviations.get(scope, scope)
            scope_ = _command.Scope(voice_name=voice_name)
            scopes_.append(scope_)
        elif isinstance(scope, tuple):
            voice_name, measures = scope
            voice_name = abbreviations.get(voice_name, voice_name)
            if isinstance(measures, list):
                measures = _unpack_measure_token_list(measures)
                for measure_token in measures:
                    scope_ = _command.Scope(
                        measures=measure_token, voice_name=voice_name
                    )
                    scopes_.append(scope_)
            else:
                scope_ = _command.Scope(measures=measures, voice_name=voice_name)
                scopes_.append(scope_)
        else:
            scope_ = scope
            scopes_.append(scope_)
    return scopes_


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


class CommandAccumulator:
    """
    Command accumulator.
    """

    __slots__ = (
        "_voice_name_to_voice",
        "commands",
        "first_measure_number",
        "functions",
        "instruments",
        "metronome_marks",
        "short_instrument_names",
        "time_signatures",
        "voice_abbreviations",
        "voice_names",
    )

    def __init__(
        self,
        *functions,
        instruments=None,
        metronome_marks=None,
        short_instrument_names=None,
        time_signatures=None,
        voice_abbreviations=None,
        voice_names=None,
    ):
        self._voice_name_to_voice = {}
        self.commands = []
        self.first_measure_number = None
        self.functions = functions or ()
        self.instruments = instruments
        self.metronome_marks = metronome_marks
        self.short_instrument_names = short_instrument_names
        self.time_signatures = _initialize_time_signatures(time_signatures)
        self.voice_abbreviations = voice_abbreviations or {}
        self.voice_names = voice_names

    def __call__(self, scopes, *commands):
        classes = (list, _command.Suite)
        commands_ = abjad.sequence.flatten(list(commands), classes=classes, depth=-1)
        commands = tuple(commands_)
        abbreviations = self.voice_abbreviations
        assert isinstance(abbreviations, dict), repr(abbreviations)
        scopes_ = _unpack_scopes(scopes, abbreviations)
        for scope_ in scopes_:
            assert scope_.voice_name != "Skips", repr(scope_)
        assert all(isinstance(_, _command.Scope) for _ in scopes_), repr(scopes_)
        for command in commands:
            if command is None:
                continue
            if isinstance(command, list):
                raise Exception("use baca.suite().")
            if not isinstance(command, _command.Command):
                message = "\n\nMust be command:"
                message += f"\n\n{repr(command)}"
                raise Exception(message)
        scope_count = len(scopes_)
        for i, current_scope in enumerate(scopes_):
            if self.voice_names and current_scope.voice_name not in self.voice_names:
                raise Exception(f"unknown voice name {current_scope.voice_name!r}.")
            for command in commands:
                if command is None:
                    continue
                assert isinstance(command, _command.Command), repr(command)
                if not command._matches_scope_index(scope_count, i):
                    continue
                if isinstance(command, _command.Command):
                    commands_ = [command]
                else:
                    commands_ = command
                for command_ in commands_:
                    assert isinstance(command_, _command.Command), repr(command_)
                    measures = command_.measures
                    if isinstance(measures, int):
                        measures = (measures, measures)
                    if measures is not None:
                        scope_ = dataclasses.replace(current_scope, measures=measures)
                    else:
                        scope_ = dataclasses.replace(current_scope)
                    # command_ = copy.copy(command_)
                    # command_.scope = scope_
                    command_ = dataclasses.replace(command_, scope=scope_)
                    self.commands.append(command_)

    def get(self, start=None, stop=None):
        if start is None and stop is None:
            return self.time_signatures
        assert 0 < start, start
        if stop is None:
            stop = start
        assert 0 < stop, stop
        return self.time_signatures[start - 1 : stop]

    def manifests(self):
        return {
            "abjad.Instrument": self.instruments,
            "abjad.MetronomeMark": self.metronome_marks,
            "abjad.ShortInstrumentName": self.short_instrument_names,
        }

    def voice(self, abbreviation):
        assert isinstance(abbreviation, str), repr(abbreviation)
        if abbreviation in self._voice_name_to_voice:
            return self._voice_name_to_voice[abbreviation]
