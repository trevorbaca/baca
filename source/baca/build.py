"""
Build.
"""

import dataclasses
import functools
import os
import pathlib
import shutil
import signal
import sys
import time
import types
import typing

import abjad

import baca


class TimeoutException(Exception):
    pass


def handler(signum, frame):
    raise TimeoutException("Function call timed out")


signal.signal(signal.SIGALRM, handler)


def _activate_tags(
    text: str,
    match: typing.Callable,
    name: str,
    messages: list,
    *,
    prepend_empty_chord: bool = False,
    undo: bool = False,
):
    assert isinstance(text, str), repr(text)
    assert callable(match), repr(match)
    assert isinstance(messages, list), repr(messages)
    assert isinstance(name, str), repr(name)
    if undo:
        text, count, skipped = abjad.deactivate(
            text,
            match,
            prepend_empty_chord=prepend_empty_chord,
        )
    else:
        text, count, skipped = abjad.activate(text, match)
    if undo:
        adjective = "inactive"
        gerund = "deactivating"
    else:
        adjective = "active"
        gerund = "activating"
    new_messages = []
    total = count + skipped
    if total == 0:
        new_messages.append(f"found no {name} tags")
    if 0 < total:
        tags = abjad.string.pluralize("tag", total)
        new_messages.append(f"found {total} {name} {tags}")
        if 0 < count:
            tags = abjad.string.pluralize("tag", count)
            message = f"{gerund} {count} {name} {tags}"
            new_messages.append(message)
        if 0 < skipped:
            tags = abjad.string.pluralize("tag", skipped)
            message = f"skipping {skipped} ({adjective}) {name} {tags}"
            new_messages.append(message)
    new_messages = [abjad.string.capitalize_start(_) + " ..." for _ in new_messages]
    if messages is not None:
        messages.extend(new_messages)
    return text


def _call_lilypond_on_music_ly_in_section(
    music_ly, music_pdf_mtime, lilypond_timeout=0
):
    music_pdf = music_ly.with_name("music.pdf")
    with abjad.contextmanagers.Timer() as timer:
        run_lilypond(
            music_ly, lilypond_timeout=lilypond_timeout, pdf_mtime=music_pdf_mtime
        )
        music_ly_pdf = music_ly.parent / "music.ly.pdf"
        if music_ly_pdf.is_file():
            shutil.move(str(music_ly_pdf), str(music_pdf))
    _music_ly_log = "." + music_ly.name + ".log"
    _music_ly_log = music_ly.parent / _music_ly_log
    _remove_lilypond_warnings(
        _music_ly_log,
        crescendo_too_small=True,
        decrescendo_too_small=True,
        overwriting_glissando=True,
    )
    return int(timer.elapsed_time())


def _color_persistent_indicators(
    text: str, messages: list[str], build: bool, *, undo: bool = False
) -> str:
    assert isinstance(text, str), repr(text)
    name = "persistent indicator"

    def _activate(tags):
        tags_ = _persistent_indicator_color_expression_tags(build=build)
        return bool(set(tags) & set(tags_))

    def _deactivate(tags):
        tags_ = _persistent_indicator_color_suppression_tags()
        return bool(set(tags) & set(tags_))

    if undo:
        messages.append(f"Uncoloring {name}s ...")
        text = _activate_tags(
            text, _deactivate, "persistent indicator color suppression", messages
        )
        text = _deactivate_tags(
            text, _activate, "persistent indicator color expression", messages
        )
    else:
        messages.append(f"Coloring {name}s ...")
        text = _activate_tags(
            text, _activate, "persistent indicator color expression", messages
        )
        text = _deactivate_tags(
            text, _deactivate, "persistent indicator color suppression", messages
        )
    messages.append("")
    return text


def _deactivate_tags(
    text: str,
    match: typing.Callable,
    name: str,
    messages: list,
    *,
    prepend_empty_chord: bool = False,
):
    return _activate_tags(
        text,
        match,
        name,
        messages=messages,
        prepend_empty_chord=prepend_empty_chord,
        undo=True,
    )


def _display_lilypond_log_errors(lilypond_log_file_path: pathlib.Path):
    assert isinstance(lilypond_log_file_path, pathlib.Path)
    with lilypond_log_file_path.open() as file_pointer:
        lines = file_pointer.readlines()
    error = False
    for line in lines:
        if (
            "fatal" in line
            or ("error" in line and "programming error" not in line)
            or "failed" in line
        ):
            print_always("ERROR IN LILYPOND LOG FILE ...")
            error = True
            break
    if error:
        print_always("".join(lines[:10]))


def _externalize(
    path: pathlib.Path,
    *,
    file_name: str | None = None,
    in_place: bool = False,
) -> pathlib.Path | None:
    assert isinstance(path, pathlib.Path), repr(path)
    if in_place is True:
        assert file_name is None, repr(file_name)
        path_ily = None
    elif file_name is None:
        path_ily = path.with_suffix(".ily")
    else:
        path_ily = path.with_name(file_name)
    if path_ily is not None:
        assert path_ily.suffix == ".ily", repr(path_ily)
    preamble_lines: list[str] = []
    score_lines: list[str] = []
    stack: dict[str, list[str]] = {}
    finished_variables = {}
    found_score = False
    with open(path) as pointer:
        readlines = pointer.readlines()
    for line in readlines:
        if (
            line.startswith(r"\score")
            or line.startswith(r"\context Score")
            or line.startswith("{")
        ):
            found_score = True
        if not found_score:
            preamble_lines.append(line)
        elif " %*% " in line:
            words = line.split()
            index = words.index("%*%")
            name = words[index + 1]
            # first line in expression:
            if name not in stack:
                stack[name] = []
                stack[name].append(line)
            # last line in expression
            else:
                stack[name].append(line)
                finished_variables[name] = stack[name]
                del stack[name]
                count = len(line) - len(line.lstrip())
                indent = count * " "
                first_line = finished_variables[name][0]
                dereference = []
                dereference.append(indent + "{")
                local_indent = 4 * " "
                dereference.append(indent + local_indent + "\\" + name)
                dereference.append(indent + "}")
                dereference = [_ + "\n" for _ in dereference]
                if bool(stack):
                    items = list(stack.items())
                    items[-1][-1].extend(dereference)
                else:
                    score_lines.extend(dereference)
        elif bool(stack):
            items = list(stack.items())
            items[-1][-1].append(line)
        else:
            score_lines.append(line)
    if in_place is False:
        assert path_ily is not None
        if path_ily.parent == path.parent:
            include_name = path_ily.name
        else:
            include_name = str(path_ily)
        include_line = f'\\include "{include_name}"'
        include_lines = [include_line]
        include_lines = [_ + "\n" for _ in include_lines]
        last_include = 0
        for i, line in enumerate(preamble_lines):
            if line.startswith(r"\include"):
                last_include = i
        preamble_lines[last_include + 1 : last_include + 1] = include_lines
    if preamble_lines[-2] == "\n":
        del preamble_lines[-2]
    lines = []
    lines.extend(preamble_lines)
    lines.extend(score_lines)
    lines_ = []
    for line in lines:
        lines_.append(line)
    text = "".join(lines_)
    path.write_text(text)
    lines = []
    if in_place is False:
        string = abjad.configuration.Configuration().lilypond_version_string()
        string = rf'\version "{string}"'
        lines.append(string + "\n")
        lines.append("\n")
    items = list(finished_variables.items())
    total = len(items)
    for i, item in enumerate(items):
        name, variable_lines = item
        first_line = variable_lines[0]
        count = len(first_line) - len(first_line.lstrip())
        first_line = first_line[count:]
        first_line = f"{name} = {first_line}"
        words = first_line.split()
        index = words.index("%*%")
        first_line = " ".join(words[:index])
        words = first_line.split(" = ")
        assert len(words) == 2, repr(words)
        first_lines = []
        first_lines.append(words[0] + " =")
        first_lines.extend(words[1:])
        first_lines = [_ + "\n" for _ in first_lines]
        lines.extend(first_lines)
        for variable_line in variable_lines[1:]:
            assert variable_line[:count].isspace(), repr(line)
            variable_line = variable_line[count:]
            if variable_line == "":
                variable_line = "\n"
            assert variable_line.endswith("\n"), repr(variable_line)
            lines.append(variable_line)
        not_topmost_index = None
        for j, line in enumerate(reversed(lines)):
            if line.strip() == f"%! {baca.tags.NOT_TOPMOST.string}":
                not_topmost_index = j
                break
            if line.isspace():
                break
        if not_topmost_index is not None:
            assert 0 < not_topmost_index
            index = -(not_topmost_index + 1)
            del lines[index]
        last_line = lines[-1]
        assert last_line.startswith("} ") or last_line.startswith(">> ")
        words = last_line.split()
        index = words.index("%*%")
        last_line = " ".join(words[:index])
        last_lines = [last_line]
        last_lines = [_ + "\n" for _ in last_lines]
        lines[-1:] = last_lines
        if i < total - 1:
            lines.append("\n")
            lines.append("\n")
    if in_place is False:
        assert path_ily is not None
        text = "".join(lines)
        path_ily.write_text(text)
        return path_ily
    else:
        assert "context Score" in score_lines[0]
        score_lines[0] = "page-layout-score = " + score_lines[0]
        lines_ = preamble_lines + lines + ["\n\n"] + score_lines
        text = "".join(lines_)
        path.write_text(text)
        return None


def _externalize_layout_ily_path(layout_ily_path):
    print_file_handling(f"Externalizing {baca.path.trim(layout_ily_path)} ...")
    _externalize(layout_ily_path, in_place=True)


def _externalize_music_ly_path(music_ly):
    print_file_handling(f"Externalizing {baca.path.trim(music_ly)} ...")
    assert "sections" in music_ly.parts, repr(music_ly)
    music_ily = _externalize(music_ly)
    for file in (music_ly, music_ily):
        text = file.read_text()
        messages = []
        text = _not_topmost(text, messages)
        file.write_text(text)
        if messages:
            message = "Appending not-topmost tags messages ..."
            print_file_handling(message, log_only=True)
            messages = "\n".join(messages) + "\n"
            _tags_file = file.with_name(f".{file.name}.tags")
            with _tags_file.open("a") as pointer:
                pointer.write(messages)


def _handle_edition_tags(
    text: str, messages: list[str], build_identifier: str, build_type: str
) -> str:
    """
    Handles edition tags.

    The logic here is important:

        * deactivations run first:

            -TAG (where TAG is either my directory or my buildtype)

            +TAG (where TAG is neither my directory nor my buildtype)

        * activations run afterwards:

            TAG_SET such that there exists at least one build-forbid -TAG (equal to
            neither my directory nor my buildtype) in TAG_SET and such that there exists
            no -TAG (equal to either my directory or my buildtype) in TAG_SET

            +TAG (where TAG is either my directory or my buildtype)

        Notionally: first we deactivate anything that is tagged EITHER specifically
        against me OR specifically for another build; then we activate anything that is
        deactivated for editions other than me; then we activate anything is tagged
        specifically for me.

    Also:

        For scores, build_identifier should be something like
            TABLOID_SCORE
            ARCH_A_SCORE
        For parts, build_identifier should be something like
            LETTER_PARTS_CELLO
            LETTER_PARTS_TRUMPET_3

    """
    assert isinstance(text, str), repr(text)
    assert abjad.string.is_shout_case(build_identifier), repr(build_identifier)
    assert not build_identifier.endswith("_PARTS"), repr(build_identifier)
    assert build_type in ("SECTION", "SCORE", "PARTS"), repr(build_type)
    messages.append("Handling edition tags ...")
    this_edition = abjad.Tag(f"+{build_type}")
    not_this_edition = abjad.Tag(f"-{build_type}")
    this_directory = abjad.Tag(f"+{build_identifier}")
    not_this_directory = abjad.Tag(f"-{build_identifier}")

    def _deactivate(tags):
        if not_this_edition in tags:
            return True
        if not_this_directory in tags:
            return True
        for tag in tags:
            if tag.string.startswith("+"):
                return True
        return False

    text = _deactivate_tags(text, _deactivate, "other-edition", messages)

    def _activate(tags):
        for tag in tags:
            if tag in [not_this_edition, not_this_directory]:
                return False
        for tag in tags:
            if tag.string.startswith("-"):
                return True
        return bool(set(tags) & set([this_edition, this_directory]))

    text = _activate_tags(text, _activate, "this-edition", messages)
    messages.append("")
    return text


def _handle_fermata_bar_lines(
    text: str,
    messages: list[str],
    bol_measure_numbers: list | None,
    final_measure_number: int | None,
) -> str:
    messages.append("Handling fermata bar lines ...")

    def _activate(tags):
        return bool(set(tags) & set([baca.tags.FERMATA_MEASURE]))

    # activate fermata measure bar line adjustment tags ...
    text = _activate_tags(text, _activate, "bar line adjustment", messages)
    # ... then deactivate non-EOL tags
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        eol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

        def _deactivate(tags):
            if baca.tags.FERMATA_MEASURE in tags:
                if not bool(set(tags) & set(eol_measure_numbers)):
                    return True
            return False

        text = _deactivate_tags(text, _deactivate, "EOL fermata bar line", messages)
    messages.append("")
    return text


def _handle_mol_tags(
    text: str,
    messages: list[str],
    bol_measure_numbers: list | None,
    final_measure_number: int | None,
) -> str:
    messages.append("Handling MOL tags ...")

    # activate all middle-of-line tags ...
    def _activate(tags):
        tags_ = set([baca.tags.NOT_MOL, baca.tags.ONLY_MOL])
        return bool(set(tags) & tags_)

    text = _activate_tags(text, _activate, "MOL", messages)
    # ... then deactivate conflicting middle-of-line tags
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        if final_measure_number is not None:
            nonmol_measure_numbers.append(final_measure_number + 1)
        nonmol_measure_numbers = [
            abjad.Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
        ]

        def _deactivate(tags):
            if baca.tags.NOT_MOL in tags:
                if not bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            if baca.tags.ONLY_MOL in tags:
                if bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            return False

        text = _deactivate_tags(text, _deactivate, "conflicting MOL", messages)
    messages.append("")
    return text


def _handle_section_tags(section_directory):
    assert section_directory.is_dir()
    print_file_handling("Writing section tag files ...")
    music_ly = section_directory / "music.ly"
    text = music_ly.read_text()
    text = abjad.tag.left_shift_tags(text)
    music_ly.write_text(text)
    for name in ("layout.ily", "music.ily", "music.ly"):
        path = music_ly.with_name(name)
        if not path.exists():
            continue
        bol_measure_numbers = baca.path.get_metadata(section_directory).get(
            "bol_measure_numbers"
        )
        final_measure_number = baca.path.get_metadata(section_directory).get(
            "final_measure_number"
        )
        _tags_file = music_ly.with_name(f".{name}.tags")
        messages = []
        text = path.read_text()
        text = _handle_edition_tags(text, messages, "SECTION", "SECTION")
        text = _handle_fermata_bar_lines(
            text, messages, bol_measure_numbers, final_measure_number
        )
        text = _handle_shifted_clefs(text, messages, bol_measure_numbers)
        text = _handle_mol_tags(
            text, messages, bol_measure_numbers, final_measure_number
        )
        path.write_text(text)
        print_file_handling(
            f"Appending {baca.path.trim(_tags_file)} ...", log_only=True
        )
        text = "\n".join(messages) + "\n"
        with _tags_file.open("a") as pointer:
            pointer.write(text)


def _handle_shifted_clefs(
    text: str, messages: list[str], bol_measure_numbers: list | None
) -> str:
    messages.append("Handling shifted clefs ...")

    def _activate(tags):
        return baca.tags.SHIFTED_CLEF in tags

    # set X-extent to false and left-shift measure-initial clefs ...
    text = _activate_tags(text, _activate, "shifted clef", messages)
    # ... then unshift clefs at beginning-of-line
    if bol_measure_numbers:
        bol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

        def _deactivate(tags):
            if baca.tags.SHIFTED_CLEF not in tags:
                return False
            if any(_ in tags for _ in bol_measure_numbers):
                return True
            return False

        text = _deactivate_tags(text, _deactivate, "BOL clef", messages)
    messages.append("")
    return text


def _join_broken_spanners(text: str, messages: list[str]) -> str:
    messages.append("Joining broken spanners ...")

    def _activate(tags):
        tags_ = [baca.tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def _deactivate(tags):
        tags_ = [baca.tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    text = _activate_tags(text, _activate, "broken spanner expression", messages)
    text = _deactivate_tags(text, _deactivate, "broken spanner suppression", messages)
    messages.append("")
    return text


def _log_timing(section_directory, timing):
    if "trevor" not in str(section_directory):
        return
    _timing = section_directory / ".timing"
    parts = []
    for part in _timing.parts:
        if part == os.path.sep:
            pass
        elif part == "Scores":
            parts.extend(["Regression", "timing"])
        else:
            parts.append(part)
    _timing_repo = "/" + os.path.sep.join(parts)
    _timing_repo = pathlib.Path(_timing_repo)
    if not _timing_repo.parent.is_dir():
        _timing_repo.parent.mkdir(parents=True)
    print_file_handling(f"Writing {baca.path.trim(_timing_repo)} ...", log_only=True)
    with _timing_repo.open(mode="a") as pointer:
        pointer.write("\n")
        line = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        pointer.write(line)
        python_runtime = timing.make_score + timing.postprocess
        counter = abjad.string.pluralize("second", python_runtime)
        line = f"Python runtime: {python_runtime} {counter}\n"
        pointer.write(line)
        counter = abjad.string.pluralize("second", timing.make_score)
        line = f"  make_score(): {timing.make_score} {counter}\n"
        pointer.write(line)
        counter = abjad.string.pluralize("second", timing.postprocess)
        line = f"  postprocess(): {timing.postprocess} {counter}\n"
        pointer.write(line)
        if timing.lilypond == "SKIPPED":
            line = f"LilyPond runtime: {timing.lilypond}\n"
        else:
            counter = abjad.string.pluralize("second", timing.lilypond)
            line = f"LilyPond runtime: {timing.lilypond} {counter}\n"
        pointer.write(line)


def _make_section_clicktrack(lilypond_file, mtime, section_directory):
    metadata = baca.path.get_metadata(section_directory)
    if metadata.get("first_metronome_mark") is False:
        print_main_task("Skipping clicktrack ...")
        return
    print_main_task("Making clicktrack ...")
    clicktrack_file_name = "clicktrack.midi"
    clicktrack_path = section_directory / clicktrack_file_name
    if clicktrack_path.is_file():
        print_file_handling(
            f"Existing {baca.path.trim(clicktrack_path)} ...", log_only=True
        )
    global_skips = lilypond_file["Skips"]
    time_signatures = []
    for skip in global_skips[:-1]:
        time_signature = abjad.get.effective_indicator(skip, abjad.TimeSignature)
        time_signatures.append(time_signature)
    skips = abjad.select.leaves(global_skips)[:-1]
    metronome_marks = []
    for skip in skips:
        metronome_mark = abjad.get.effective_indicator(skip, abjad.MetronomeMark)
        metronome_marks.append(metronome_mark)
    if metronome_marks[0] is None:
        for metronome_mark in metronome_marks:
            if metronome_mark is not None:
                first_metronome_mark = metronome_mark
                break
        for i, metronome_mark in enumerate(metronome_marks[:]):
            if metronome_mark is None:
                metronome_marks[i] = first_metronome_mark
    staff = abjad.Staff(name="Clicktrack_Staff")
    abjad.setting(staff).midiInstrument = '#"drums"'
    score = abjad.Score([staff], name="Score", simultaneous=False)
    fermata_measure_numbers = []
    if "Rests" in lilypond_file:
        global_rests = lilypond_file["Rests"]
        for i, rest in enumerate(global_rests):
            if abjad.get.has_indicator(rest, baca.enums.FERMATA_MEASURE):
                measure_number = i + 1
                fermata_measure_numbers.append(measure_number)
    for i, time_signature in enumerate(time_signatures):
        measure_number = i + 1
        if measure_number in fermata_measure_numbers:
            metronome_mark = abjad.MetronomeMark(abjad.ValueDuration(1, 4), 60)
            time_signature = abjad.TimeSignature((3, 4))
            notes = [abjad.Rest("r2.")]
        else:
            metronome_mark = metronome_marks[i]
            units_per_minute = round(metronome_mark.units_per_minute)
            metronome_mark = dataclasses.replace(
                metronome_mark,
                # TOD: metronome mark no longer has `hide` property
                hide=False,
                units_per_minute=units_per_minute,
            )
            time_signature = dataclasses.replace(time_signature)
            numerator, denominator = time_signature.pair
            notes = []
            for _ in range(numerator):
                note = abjad.Note("fs,1", multiplier=(1, denominator))
                notes.append(note)
            notes[0].set_written_pitch(-23)
        abjad.attach(time_signature, notes[0])
        abjad.attach(metronome_mark, notes[0])
        measure = abjad.Container(notes)
        staff.append(measure)
    score_block = abjad.Block("score", [score, abjad.Block("midi")])
    lilypond_file = abjad.LilyPondFile([score_block])
    print_file_handling(f"Writing {baca.path.trim(clicktrack_path)} ...")
    abjad.persist.as_pdf(lilypond_file, clicktrack_file_name)
    ly_path = section_directory / "clicktrack.ly"
    if ly_path.exists():
        ly_path.unlink()
    if clicktrack_path.is_file():
        mtime_ = os.path.getmtime(clicktrack_path)
        if mtime is not None and mtime < mtime_:
            print_success(f"Modified {baca.path.trim(clicktrack_path)} ...")
        else:
            print_success(f"Found {baca.path.trim(clicktrack_path)} ...")
    else:
        print_error(f"Can not find {baca.path.trim(clicktrack_path)} ...")


def _make_section_midi(lilypond_file, mtime, section_directory):
    metadata = baca.path.get_metadata(section_directory)
    if metadata.get("first_metronome_mark") is False:
        print_main_task("Skipping MIDI ...")
        return
    print_main_task("Making MIDI ...")
    music_midi = section_directory / "music.midi"
    if music_midi.exists():
        print_file_handling(f"Existing {baca.path.trim(music_midi)} ...", log_only=True)
    score = lilypond_file["Score"]
    score_block = abjad.Block("score", [score, abjad.Block("midi")])
    lilypond_file = abjad.LilyPondFile([score_block])
    tmp_midi = section_directory / "tmp.midi"
    print_file_handling(f"Writing {baca.path.trim(music_midi)} ...")
    abjad.persist.as_pdf(lilypond_file, tmp_midi)
    if tmp_midi.is_file():
        shutil.move(tmp_midi, music_midi)
    tmp_ly = tmp_midi.with_suffix(".ly")
    if tmp_ly.exists():
        tmp_ly.unlink()
    if music_midi.is_file():
        mtime_ = os.path.getmtime(music_midi)
        if mtime is not None and mtime < mtime_:
            print_success(f"Modified {baca.path.trim(music_midi)} ...")
        else:
            print_success(f"Found {baca.path.trim(music_midi)} ...")
    else:
        print_error(f"Can not find {baca.path.trim(music_midi)} ...")


def _make_section_pdf(
    lilypond_file,
    music_pdf_mtime,
    section_directory,
    timing,
    *,
    also_untagged=False,
    do_not_call_lilypond=False,
    lilypond_timeout=0,
    log_timing=False,
    print_timing=False,
):
    print_main_task("Making PDF ...")
    music_ly = section_directory / "music.ly"
    music_pdf = section_directory / "music.pdf"
    music_ly_mtime = os.path.getmtime(music_ly) if music_ly.is_file() else 0
    abjad.persist.as_ly(lilypond_file, music_ly, tags=True)
    if music_ly.is_file() and music_ly_mtime < os.path.getmtime(music_ly):
        print_file_handling(f"Writing {baca.path.trim(music_ly)} ...")
    print_file_handling("Removing section tag files ...")
    _layout_ily_tags = music_ly.with_name(".layout.ily.tags")
    if _layout_ily_tags.exists():
        _layout_ily_tags.unlink()
    _music_ily_tags = music_ly.with_name(".music.ily.tags")
    if _music_ily_tags.exists():
        _music_ily_tags.unlink()
    _music_ly_tags = music_ly.with_name(".music.ly.tags")
    if _music_ly_tags.exists():
        _music_ly_tags.unlink()
    _externalize_music_ly_path(music_ly)
    _handle_section_tags(section_directory)
    contents_directory = baca.path.get_contents_directory(section_directory)
    metadata = baca.path.get_metadata(contents_directory)
    do_not_populate_remote_repos = metadata.get("do_not_populate_remote_repos")
    if not do_not_populate_remote_repos:
        _populate_verbose_repository(section_directory)
    _remove_site_comments(section_directory)
    _remove_function_name_comments(section_directory)
    if music_pdf.is_file():
        print_file_handling(f"Existing {baca.path.trim(music_pdf)} ...", log_only=True)
    if do_not_call_lilypond is True:
        timing.lilypond = "SKIPPED"
    else:
        timing.lilypond = _call_lilypond_on_music_ly_in_section(
            music_ly,
            music_pdf_mtime,
            lilypond_timeout=lilypond_timeout,
        )
    if print_timing:
        print_all_timing(timing)
    if log_timing:
        _log_timing(section_directory, timing)
    if also_untagged is True and not do_not_populate_remote_repos:
        _populate_untagged_repository(section_directory)


def _metronome_mark_color_suppression_tags():
    return [baca.tags.EXPLICIT_METRONOME_MARK, baca.tags.REDUNDANT_METRONOME_MARK]


def _music_annotation_tags():
    return [
        baca.tags.CLOCK_TIME,
        baca.tags.FIGURE_LABEL,
        baca.tags.INVISIBLE_MUSIC_COLORING,
        baca.tags.LOCAL_MEASURE_NUMBER,
        baca.tags.MATERIAL_ANNOTATION_MARKUP,
        baca.tags.MATERIAL_ANNOTATION_SPANNER,
        baca.tags.MOCK_COLORING,
        baca.tags.MOMENT_ANNOTATION_SPANNER,
        baca.tags.NOT_YET_PITCHED_COLORING,
        baca.tags.OCTAVE_COLORING,
        baca.tags.REPEAT_PITCH_CLASS_COLORING,
        baca.tags.SPACING,
        baca.tags.STAFF_HIGHLIGHT,
        baca.tags.STAGE_NUMBER,
    ]


def _not_topmost(text: str, messages: list[str]) -> str:
    messages.append(f"Deactivating {baca.tags.NOT_TOPMOST.string} ...")

    def _deactivate(tags):
        tags_ = [baca.tags.NOT_TOPMOST]
        return bool(set(tags) & set(tags_))

    text = _deactivate_tags(text, _deactivate, "not topmost", messages)
    messages.append("")
    return text


def _persistent_indicator_color_expression_tags(*, build=False):
    tags = []
    clef_color_tags = [
        baca.tags.EXPLICIT_CLEF_COLOR,
        baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF_COLOR,
        baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
        baca.tags.REDUNDANT_CLEF_COLOR,
        baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
    ]
    if build is True:
        clef_color_tags.append(baca.tags.REAPPLIED_CLEF)
    tags.extend(clef_color_tags)
    dynamic_color_tags = [
        baca.tags.EXPLICIT_DYNAMIC_COLOR,
        baca.tags.REAPPLIED_DYNAMIC,
        baca.tags.REAPPLIED_DYNAMIC_COLOR,
        baca.tags.REDUNDANT_DYNAMIC_COLOR,
    ]
    tags.extend(dynamic_color_tags)
    tags.extend(baca.section.instrument_color_tags())
    metronome_mark_color_expression_tags = [
        baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
        baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
        baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
    ]
    tags.extend(metronome_mark_color_expression_tags)
    ottava_color_tags = [
        baca.tags.EXPLICIT_OTTAVA_COLOR,
        baca.tags.REAPPLIED_OTTAVA,
        baca.tags.REAPPLIED_OTTAVA_COLOR,
        baca.tags.REDUNDANT_OTTAVA_COLOR,
    ]
    tags.extend(ottava_color_tags)
    tags.extend(baca.section.short_instrument_name_color_tags())
    staff_lines_color_tags = [
        baca.tags.EXPLICIT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES_COLOR,
        baca.tags.REDUNDANT_STAFF_LINES_COLOR,
    ]
    if build is True:
        staff_lines_color_tags.append(baca.tags.REAPPLIED_STAFF_LINES)
    tags.extend(staff_lines_color_tags)
    time_signature_color_tags = [
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
    ]
    if build is True:
        time_signature_color_tags.append(baca.tags.REAPPLIED_TIME_SIGNATURE)
    tags.extend(time_signature_color_tags)
    return tags


def _persistent_indicator_color_suppression_tags():
    tags = []
    tags.extend(_metronome_mark_color_suppression_tags())
    return tags


def _populate_verbose_repository(section_directory):
    if os.environ.get("GITHUB_WORKSPACE"):
        return
    print_main_task("Populating $REGRESSION/verbose repository ...")
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        with path.open() as pointer:
            lines = pointer.readlines()
        string = "".join(lines)
        parts = []
        for part in path.parts:
            if part == os.path.sep:
                pass
            elif part == "Scores":
                parts.extend(["Regression", "verbose"])
            else:
                parts.append(part)
        _untagged = "/" + os.path.sep.join(parts)
        _untagged = pathlib.Path(_untagged)
        if not _untagged.parent.is_dir():
            _untagged.parent.mkdir(parents=True)
        _untagged.write_text(string)


def _populate_untagged_repository(section_directory):
    if os.environ.get("GITHUB_WORKSPACE"):
        return
    print_main_task("Populating $REGRESSION/untagged repository ...")
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        with path.open() as pointer:
            lines = pointer.readlines()
        lines_ = []
        for line in lines:
            if line.strip().startswith("% "):
                if line.strip().endswith(":"):
                    continue
            lines_.append(line)
        lines = lines_
        string = "".join(lines)
        string = abjad.tag.remove_tags(string)
        parts = []
        for part in path.parts:
            if part == os.path.sep:
                pass
            elif part == "Scores":
                parts.extend(["Regression", "untagged"])
            else:
                parts.append(part)
        _untagged = "/" + os.path.sep.join(parts)
        _untagged = pathlib.Path(_untagged)
        if not _untagged.parent.is_dir():
            _untagged.parent.mkdir(parents=True)
        _untagged.write_text(string)
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        safekeeping = section_directory / f"{name}.original"
        shutil.copyfile(path, safekeeping)
        color_persistent_indicators(path, undo=True)
        show_annotations(path, undo=True)
    print_main_task("Populating $REGRESSION/bw repository ...")
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        with path.open() as pointer:
            lines = pointer.readlines()
        lines_ = []
        for line in lines:
            if line.strip().startswith("%! "):
                continue
            if line.strip().startswith("%%% "):
                continue
            if line.strip().startswith("%@% "):
                continue
            if line.strip().startswith("% ") and line.strip().endswith(":"):
                continue
            if line.endswith(" %@%\n"):
                line = line.replace(" %@%", "")
            lines_.append(line)
        lines = lines_
        string = "".join(lines)
        parts = []
        for part in path.parts:
            if part == os.path.sep:
                pass
            elif part == "Scores":
                parts.extend(["Regression", "bw"])
            else:
                parts.append(part)
        _bw = "/" + os.path.sep.join(parts)
        _bw = pathlib.Path(_bw)
        if not _bw.parent.is_dir():
            _bw.parent.mkdir(parents=True)
        _bw.write_text(string)
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        safekeeping = section_directory / f"{name}.original"
        shutil.move(safekeeping, path)


def _remove_function_name_comments(section_directory):
    print_file_handling("Removing function name comments ...")
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        with path.open() as pointer:
            lines = pointer.readlines()
        lines_ = []
        for line in lines:
            if line.strip().startswith("%! "):
                if line.strip().endswith(")"):
                    continue
            lines_.append(line)
        lines = lines_
        string = "".join(lines)
        path.write_text(string)


def _remove_lilypond_warnings(
    path,
    *,
    crescendo_too_small=None,
    decrescendo_too_small=None,
    overwriting_glissando=None,
):
    assert path.name.endswith(".log"), repr(path)
    lines = []
    skip = 0
    with open(path) as pointer:
        for line in pointer.readlines():
            if 0 < skip:
                skip -= 1
                continue
            if crescendo_too_small and "crescendo too small" in line:
                skip = 2
                continue
            if decrescendo_too_small and "decrescendo too small" in line:
                skip = 2
                continue
            if overwriting_glissando and "overwriting glissando" in line:
                skip = 1
                continue
            lines.append(line)
    text = "".join(lines)
    path.write_text(text)


def _remove_site_comments(section_directory):
    print_file_handling("Removing site comments ...")
    for name in ("music.ly", "music.ily", "layout.ily"):
        path = section_directory / name
        if not path.exists():
            continue
        remove_site_comments(path)


def _show_music_annotations(
    text: str, messages: list[str], *, undo: bool = False
) -> str:
    name = "music annotation"

    def match(tags):
        tags_ = _music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [baca.tags.INVISIBLE_MUSIC_COMMAND]
        return bool(set(tags) & set(tags_))

    if not undo:
        messages.append(f"Showing {name}s ...")
        text = _activate_tags(text, match, name, messages)
        text = _deactivate_tags(text, match_2, name, messages)
    else:
        messages.append(f"Hiding {name}s ...")
        text = _activate_tags(text, match_2, name, messages)
        text = _deactivate_tags(text, match, name, messages)
    messages.append("")
    return text


def _trim_music_ly(ly):
    assert ly.is_file()
    lines = []
    with ly.open() as file_pointer:
        found_score_context_open = False
        found_score_context_close = False
        for line in file_pointer.readlines():
            if r"\context Score" in line:
                found_score_context_open = True
            if line == "        >>\n":
                found_score_context_close = True
            if found_score_context_open:
                lines.append(line)
            if found_score_context_close:
                lines.append("\n")
                break
    if lines and lines[0].startswith("    "):
        lines = [_[8:] for _ in lines]
    if lines and lines[-1] == "\n":
        lines.pop()
    lines = "".join(lines)
    return lines


def _write_music_ly(lilypond_file, music_ly):
    abjad.persist.as_ly(lilypond_file, music_ly, tags=True)


def _make_empty_mapping_proxy():
    return types.MappingProxyType({})


@dataclasses.dataclass(slots=True, order=True, unsafe_hash=True)
class Timing:
    lilypond: int | None = None
    make_score: int | None = None
    postprocess: int | None = None


@dataclasses.dataclass(frozen=True, slots=True, order=True, unsafe_hash=True)
class BuildDirectoryEnvironment:
    build_directory: pathlib.Path
    fermata_measure_numbers: list[int]
    time_signatures: list[str]


def read_build_directory_environment(layout_py_path) -> BuildDirectoryEnvironment:
    build_directory = pathlib.Path(layout_py_path).parent
    sections_directory = baca.path.get_contents_directory(build_directory) / "sections"
    time_signatures = accumulate_time_signatures(sections_directory)
    fermata_measure_numbers = accumulate_fermata_measure_numbers(sections_directory)
    return baca.build.BuildDirectoryEnvironment(
        build_directory=build_directory,
        fermata_measure_numbers=fermata_measure_numbers,
        time_signatures=time_signatures,
    )


@dataclasses.dataclass(frozen=True, slots=True, order=True, unsafe_hash=True)
class Environment:
    arguments: tuple[str, ...] = dataclasses.field(default_factory=tuple)
    first_measure_number: int = 1
    metadata: types.MappingProxyType = dataclasses.field(
        default_factory=_make_empty_mapping_proxy
    )
    persist: types.MappingProxyType = dataclasses.field(
        default_factory=_make_empty_mapping_proxy
    )
    previous_metadata: types.MappingProxyType = dataclasses.field(
        default_factory=_make_empty_mapping_proxy
    )
    section_directory: pathlib.Path | None = None
    section_not_included_in_score: bool = False
    section_number: str | None = None
    timing: Timing | None = None

    def score(self):
        if self.arguments.clicktrack is True:
            return True
        if self.arguments.midi is True:
            return True
        if self.arguments.pdf is True:
            return True
        return False


Timer = abjad.contextmanagers.Timer


def accumulate_fermata_measure_numbers(sections_directory):
    assert sections_directory.name == "sections", repr(sections_directory)
    fermata_measure_numbers = []
    for section_directory in sorted(sections_directory.glob("*")):
        if not section_directory.is_dir():
            continue
        dictionary = baca.path.get_metadata(section_directory)
        fermata_measure_numbers_ = dictionary.get("fermata_measure_numbers", [])
        fermata_measure_numbers.extend(fermata_measure_numbers_)
    assert all(isinstance(_, int) for _ in fermata_measure_numbers)
    return fermata_measure_numbers


def accumulate_time_signatures(sections_directory):
    assert sections_directory.name == "sections", repr(sections_directory)
    time_signatures = []
    for section_directory in sorted(sections_directory.glob("*")):
        if not section_directory.is_dir():
            continue
        dictionary = baca.path.get_metadata(section_directory)
        time_signatures_ = dictionary.get("time_signatures", [])
        time_signatures.extend(time_signatures_)
    assert all(isinstance(_, str) for _ in time_signatures), repr(time_signatures)
    return time_signatures


# TODO: integrate argparse
def arguments(arguments):
    known_arguments = (
        "--also-untagged",
        "--clicktrack",
        "--do-not-call-lilypond",
        "--layout",
        "--log-timing",
        "--midi",
        "--pdf",
        "--print-timing",
    )
    namespace = types.SimpleNamespace()
    for argument in known_arguments:
        name = argument.removeprefix("--").replace("-", "_")
        value = False
        for string in arguments[1:]:
            if string.startswith(argument) and "=" in string:
                value = string.split("=")[-1]
            elif string.startswith(argument) and "=" not in string:
                value = True
        setattr(namespace, name, value)
    for string in arguments[1:]:
        name = argument.removeprefix("--").replace("-", "_")
        if not hasattr(namespace, name):
            if string.startswith("--"):
                role = "option"
            else:
                role = "argument"
            raise Exception(f"Unrecognized {role} {string} ...")
    if not any([namespace.clicktrack, namespace.layout, namespace.midi, namespace.pdf]):
        print_always("Missing --clicktrack, --layout, --midi, --pdf ...")
        sys.exit(1)
    return namespace


def argv():
    return list(sys.argv)


def build_part(part_directory, keep_temporary_files=False):
    assert part_directory.parent.name.endswith("-parts"), repr(part_directory)
    part_pdf = part_directory / "part.pdf"
    print_always(f"Building {baca.path.trim(part_pdf)} ...")
    layout_py = part_directory / "layout.py"
    # TODO: consider removing or hoisting to make
    os.system(f"python {layout_py}")
    interpret_build_music(part_directory, keep_temporary_files=keep_temporary_files)
    front_cover_tex = part_directory / "front-cover.tex"
    run_xelatex(front_cover_tex)
    preface_tex = part_directory / "preface.tex"
    run_xelatex(preface_tex)
    back_cover_tex = part_directory / "back-cover.tex"
    run_xelatex(back_cover_tex)
    part_tex = part_directory / "part.tex"
    run_xelatex(part_tex)


def build_score(score_directory, keep_temporary_files=False):
    assert score_directory.name.endswith("-score"), repr(score_directory)
    assert score_directory.parent.name == "builds", repr(score_directory)
    print_main_task("Building score ...")
    interpret_build_music(score_directory, keep_temporary_files=keep_temporary_files)
    for stem in (
        "front-cover",
        "blank",
        "inscription",
        "preface",
        "back-cover",
        "score",
    ):
        tex = score_directory / f"{stem}.tex"
        pdf = score_directory / f"{stem}.pdf"
        if tex.is_file():
            run_xelatex(tex)
        elif pdf.is_file():
            print_file_handling(f"Using existing {baca.path.trim(pdf)} ...")
    score_tex = score_directory / "score.tex"
    run_xelatex(score_tex)
    score_pdf = score_directory / "score.pdf"
    if not score_pdf.is_file():
        print_error(f"Can not find {baca.path.trim(score_pdf)} ...")
        print_error("PDF MISSING IN build_score()")
        os.system("cat .music.ly.log")
        sys.exit(1)


def collect_temporary_files(_sections_directory):
    contents_directory = baca.path.get_contents_directory(_sections_directory)
    sections_directory = contents_directory / "sections"
    section_lys = sorted(sections_directory.glob("**/music.ly"))
    if not section_lys:
        print_file_handling("Missing section lys ...")
        sys.exit(1)
    if _sections_directory.exists():
        print_file_remove(f"Removing {baca.path.trim(_sections_directory)} ...")
        shutil.rmtree(str(_sections_directory))
    _sections_directory.mkdir()
    targets = []
    for source_ly in section_lys:
        text = _trim_music_ly(source_ly)
        section_number = source_ly.parent.name
        target_ly = _sections_directory / f"{section_number}.ly"
        targets.append(f"{target_ly.name}")
        target_ly.write_text(text)
        name = source_ly.name.removesuffix(".ly")
        name += ".ily"
        source_ily = source_ly.parent / name
        if source_ily.is_file():
            target_ily = target_ly.with_suffix(".ily")
            targets.append(f"{target_ily.name}")
            shutil.copyfile(str(source_ily), str(target_ily))
    print_file_handling(f"Populating {baca.path.trim(_sections_directory)} ...")
    handle_build_tags(_sections_directory)


def color_persistent_indicators(file, *, undo=False):
    assert file.is_file(), repr(file)
    if "sections" not in file.parts:
        print_always("Must call on file in section directory ...")
        sys.exit(1)
    messages = []
    text = file.read_text()
    build = "builds" in file.parts
    text = _color_persistent_indicators(text, messages, build, undo=undo)
    file.write_text(text)
    return messages


def get_includes():
    strings = []
    abjad_contents = pathlib.Path(abjad.__file__).parent
    strings.append(f"--include={abjad_contents}/scm")
    baca_contents = pathlib.Path(baca.__file__).parent
    strings.append(f" --include={baca_contents}/scm")
    string = " ".join(strings)
    return string


def handle_build_tags(_sections_directory):
    print_file_handling("Writing build tag files ...")
    contents_directory = baca.path.get_contents_directory(_sections_directory)
    sections_directory = contents_directory / "sections"
    paths = sorted(sections_directory.glob("*"))
    section_directories = [_ for _ in paths if _.is_dir()]
    final_section_directory_name = section_directories[-1].name
    final_ily_name = f"{final_section_directory_name}.ily"

    # TODO: can't this be simplified to just baca.tags.LEFT_BROKEN?
    #       Because left-broken things should always deactivate?
    def match_left_broken_should_deactivate(tags):
        if baca.tags.LEFT_BROKEN in tags and baca.tags.SPANNER_START in tags:
            return True
        if (
            baca.tags.LEFT_BROKEN in tags
            and baca.tags.SPANNER_STOP in tags
            and baca.tags.EXPLICIT_DYNAMIC in tags
        ):
            return True
        return False

    def match_anchor_should_activate(tags):
        if baca.tags.ANCHOR_NOTE not in tags and baca.tags.ANCHOR_SKIP not in tags:
            return False
        if baca.tags.ONE_VOICE_COMMAND in tags:
            return True
        if baca.tags.SHOW_TO_JOIN_BROKEN_SPANNERS in tags:
            return True
        if baca.tags.SPANNER_STOP in tags:
            return True
        return False

    def match_anchor_should_deactivate(tags):
        if baca.tags.ANCHOR_NOTE not in tags and baca.tags.ANCHOR_SKIP not in tags:
            return False
        # TODO: can't this be simplified to just baca.tags.LEFT_BROKEN?
        #       Because left-broken things should always deactivate?
        if baca.tags.SPANNER_START in tags and baca.tags.LEFT_BROKEN in tags:
            return True
        # TODO: can't this be simplified to just baca.tags.RIGHT_BROKEN?
        #       Because right-broken things should always deactivate?
        if baca.tags.SPANNER_STOP in tags and baca.tags.RIGHT_BROKEN in tags:
            # return True
            # 2024-06-28 changed to false for wttc cello part;
            # TODO: maybe should stay this way permanently?
            return False
        if baca.tags.HIDE_TO_JOIN_BROKEN_SPANNERS in tags:
            return True
        return False

    build_directory = _sections_directory.parent
    if "score" in str(build_directory):
        assert build_directory.parent.name == "builds", repr(build_directory)
        build_identifier = abjad.string.to_shout_case(build_directory.name)
    else:
        assert "-parts" in str(build_directory)
        assert build_directory.parent.parent.name == "builds", repr(build_directory)
        build_identifier = build_directory.parent.name + "_" + build_directory.name
        build_identifier = abjad.string.to_shout_case(build_identifier)
    for file in sorted(_sections_directory.glob("*ly")):
        bol_measure_numbers = baca.path.get_metadata(build_directory).get(
            "bol_measure_numbers"
        )
        final_measure_number = baca.path.get_metadata(build_directory).get(
            "final_measure_number"
        )
        messages = []
        assert "sections" not in file.parts
        assert "builds" in file.parts
        if "-score" in str(file):
            build_type = "SCORE"
        else:
            assert "-parts" in str(file)
            build_type = "PARTS"
        text = file.read_text()
        text = _handle_edition_tags(text, messages, build_identifier, build_type)
        text = _handle_fermata_bar_lines(
            text, messages, bol_measure_numbers, final_measure_number
        )
        text = _handle_shifted_clefs(text, messages, bol_measure_numbers)
        text = _handle_mol_tags(
            text, messages, bol_measure_numbers, final_measure_number
        )
        build = "builds" in file.parts
        text = _color_persistent_indicators(text, messages, build, undo=True)
        text = _show_music_annotations(text, messages, undo=True)
        text = _join_broken_spanners(text, messages)
        text = show_tag(
            text,
            "left-broken-should-deactivate",
            messages,
            match=match_left_broken_should_deactivate,
            undo=True,
        )
        if file.name != final_ily_name:
            text = show_tag(text, baca.tags.ANCHOR_NOTE, messages)
            text = show_tag(text, baca.tags.ANCHOR_SKIP, messages)
            text = show_tag(
                text,
                baca.tags.ANCHOR_NOTE,
                messages,
                prepend_empty_chord=True,
                undo=True,
            )
            text = show_tag(
                text,
                baca.tags.ANCHOR_SKIP,
                messages,
                prepend_empty_chord=True,
                undo=True,
            )
            text = show_tag(
                text,
                "anchor-should-activate",
                messages,
                match=match_anchor_should_activate,
            )
            text = show_tag(
                text,
                "anchor-should-deactivate",
                messages,
                match=match_anchor_should_deactivate,
                undo=True,
            )
            text = show_tag(
                text,
                baca.tags.EOS_STOP_MM_SPANNER,
                messages,
            )
        text = show_tag(
            text,
            baca.tags.METRIC_MODULATION_IS_STRIPPED,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.METRIC_MODULATION_IS_SCALED,
            messages,
            undo=True,
        )
        file.write_text(text)
        _tags = _sections_directory / f".{file.name}.tags"
        print_file_handling(f"Writing {baca.path.trim(_tags)} ...", log_only=True)
        text = "\n".join(messages) + "\n"
        with _tags.open("a") as pointer:
            pointer.write(text)


def handle_part_tags(_sections_directory, part_identifier=None):
    if not _sections_directory.parent.parent.name.endswith("-parts"):
        print_always("Must call in part directory ...")
        sys.exit(1)
    for file in sorted(_sections_directory.glob("*ily")):
        messages = []
        text = file.read_text()
        text = show_tag(
            text,
            baca.tags.ONLY_PARTS,
            messages,
        )
        text = show_tag(
            text,
            baca.tags.NOT_PARTS,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.HIDE_IN_PARTS,
            messages,
            undo=True,
        )
        if part_identifier is not None:
            parts_directory = _sections_directory.parent
            parts_directory_name = abjad.string.to_shout_case(parts_directory.name)
            name = f"{parts_directory_name}_{part_identifier}"
            text = show_tag(
                text,
                f"+{name}",
                messages,
            )
            text = show_tag(
                text,
                f"-{name}",
                messages,
                undo=True,
            )
        text = show_tag(
            text,
            baca.tags.METRIC_MODULATION_IS_SCALED,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.METRIC_MODULATION_IS_NOT_SCALED,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.METRIC_MODULATION_IS_STRIPPED,
            messages,
        )
        # HACK TO HIDE ALL POST-FERMATA-MEASURE TRANSPARENT BAR LINES;
        # this only works if parts contain no EOL fermata measure:
        text = show_tag(
            text,
            baca.tags.FERMATA_MEASURE,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.NOT_TOPMOST,
            messages,
        )
        text = show_tag(
            text,
            baca.tags.FERMATA_MEASURE_EMPTY_BAR_EXTENT,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.FERMATA_MEASURE_NEXT_BAR_EXTENT,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.FERMATA_MEASURE_RESUME_BAR_EXTENT,
            messages,
            undo=True,
        )
        text = show_tag(
            text,
            baca.tags.EXPLICIT_BAR_EXTENT,
            messages,
            undo=True,
        )


def interpret_build_music(
    build_directory,
    *,
    keep_temporary_files=False,
    skip_temporary_files=False,
):
    build_type = None
    if build_directory.name.endswith("-score"):
        build_type = "SCORE"
    if build_directory.parent.name.endswith("-parts"):
        build_type = "PART"
    if build_type is None:
        print_always("Must call script in score directory or part directory ...")
        sys.exit(1)
    music_ly = build_directory / "music.ly"
    if not music_ly.is_file():
        raise Exception(f"Missing {baca.path.trim(music_ly)} ...")
    if build_type == "SCORE":
        _sections_directory = build_directory / "_sections"
    else:
        assert build_type == "PART"
        _sections_directory = build_directory / "_sections"
    if skip_temporary_files:
        print_file_handling("Skipping temporary files ...")
    else:
        collect_temporary_files(_sections_directory)
    if build_directory.parent.name.endswith("-parts"):
        if skip_temporary_files:
            print_tags("Skipping tag handling ...")
        else:
            # handle_part_tags(build_directory)
            handle_part_tags(_sections_directory)
    contents_directory = baca.path.get_contents_directory(build_directory)
    metadata = baca.path.get_metadata(contents_directory)
    do_not_populate_remote_repos = metadata.get("do_not_populate_remote_repos")
    if "trevor" in _sections_directory.parts and not do_not_populate_remote_repos:
        print_main_task("Populating $REGRESSION/scorebuilds repository ...")
        parts = list(_sections_directory.parts)
        assert parts[4] == "Scores"
        parts[4:5] = ["Regression", "scorebuilds"]
        _builds_sections_directory = os.sep + os.sep.join(parts[1:])
        shutil.copytree(
            _sections_directory, _builds_sections_directory, dirs_exist_ok=True
        )
    remove = None
    if _sections_directory.is_dir() and not keep_temporary_files:
        remove = _sections_directory
    music_pdf = music_ly.with_name("music.pdf")
    if music_pdf.is_file():
        print_file_handling(f"Existing {baca.path.trim(music_pdf)} ...", log_only=True)
    run_lilypond(music_ly, remove=remove)


def persist_as_ly(argument, ly_file_path):
    print_file_handling(f"Writing {baca.path.trim(ly_file_path)} ...")
    abjad.persist.as_ly(argument, ly_file_path)


def persist_build_layout_ily(
    directory: pathlib.Path, lilypond_file: abjad.LilyPondFile
) -> None:
    persist_section_layout_ily(directory, lilypond_file)
    layout_ily_path = directory / "layout.ily"
    _externalize_layout_ily_path(layout_ily_path)


def persist_section_layout_ily(
    directory: pathlib.Path,
    lilypond_file: abjad.LilyPondFile,
    *,
    file_name: str = "layout.ily",
    externalize: bool = False,
) -> None:
    layout_ily_path = directory / file_name
    print_file_handling(f"Persisting {baca.path.trim(layout_ily_path)} ...")
    assert len(lilypond_file.items) == 2
    block = lilypond_file.items.pop()
    score = block.items.pop()
    lilypond_file.items.append(score)
    string = abjad.lilypond(lilypond_file, tags=True) + "\n"
    lines = string.split("\n")
    assert "abjad.LilyPondFile._get_format_pieces()" in lines[0]
    assert "baca.lilypond._make_lilypond_file()" in lines[1]
    lines = lines[2:]
    string = "\n".join(lines)
    layout_ily_path.write_text(string)


def persist_lilypond_file(
    arguments: types.SimpleNamespace,
    section_directory: pathlib.Path,
    timing: Timing,
    lilypond_file: abjad.LilyPondFile,
    metadata: types.MappingProxyType,
    *,
    lilypond_timeout: int = 0,
):
    print_main_task("Persisting LilyPond file ...")
    assert isinstance(arguments, types.SimpleNamespace), repr(arguments)
    assert isinstance(section_directory, pathlib.PosixPath), repr(section_directory)
    assert isinstance(timing, Timing), repr(timing)
    assert isinstance(lilypond_file, abjad.LilyPondFile), repr(lilypond_file)
    assert isinstance(metadata, types.MappingProxyType), repr(metadata)
    dictionary = dict(metadata)
    baca.section.sort_dictionary(dictionary)
    metadata = types.MappingProxyType(dictionary)
    metadata_file = section_directory / ".metadata"
    print_file_handling(f"Writing {baca.path.trim(metadata_file)} ...")
    baca.path.write_metadata_py(section_directory, metadata)
    if arguments.clicktrack:
        path = section_directory / "clicktrack.midi"
        mtime = os.path.getmtime(path) if path.is_file() else None
        _make_section_clicktrack(lilypond_file, mtime, section_directory)
    if arguments.midi:
        path = section_directory / "music.midi"
        mtime = os.path.getmtime(path) if path.is_file() else None
        _make_section_midi(lilypond_file, mtime, section_directory)
    if arguments.pdf:
        path = section_directory / "music.pdf"
        mtime = os.path.getmtime(path) if path.is_file() else None
        _make_section_pdf(
            lilypond_file,
            mtime,
            section_directory,
            timing,
            also_untagged=arguments.also_untagged,
            do_not_call_lilypond=arguments.do_not_call_lilypond,
            lilypond_timeout=lilypond_timeout,
            log_timing=arguments.log_timing,
            print_timing=arguments.print_timing,
        )


def print_all_timing(timing):
    if hasattr(timing, "make_score"):
        python_runtime = timing.make_score + timing.postprocess
        print_timing("Python runtime", python_runtime)
    if timing.lilypond == "SKIPPED":
        lilypond_runtime = "SKIPPED"
    else:
        lilypond_runtime = int(timing.lilypond)
    print_timing("LilyPond runtime", lilypond_runtime)


def print_always(string=""):
    print(string)


def print_error(string):
    print(baca.colors.red + string + baca.colors.end)


def print_file_handling(string, log_only=False):
    if not log_only:
        print(baca.colors.yellow + string + baca.colors.end)


def print_file_remove(string):
    print(baca.colors.cyan + string + baca.colors.end)


def print_layout(string):
    print(baca.colors.magenta + string + baca.colors.end)


def print_main_task(string):
    print(baca.colors.blue + string + baca.colors.end)


def print_success(string):
    print(baca.colors.green_bold + string + baca.colors.end)


def print_tags(string):
    print(baca.colors.cyan + string + baca.colors.end)


def print_timing(title, timer):
    if isinstance(timer, int | str):
        count = timer
    else:
        count = int(timer.elapsed_time)
    counter = abjad.string.pluralize("second", count)
    string = f"{title} {count} {counter} ..."
    print_success(string)


def read_environment(
    music_py_path_name, sys_argv, *, section_not_included_in_score=False
) -> Environment:
    arguments_ = arguments(sys_argv)
    section_directory = pathlib.Path(music_py_path_name).parent
    metadata = baca.path.get_metadata(section_directory)
    persist = baca.path.get_metadata(section_directory)
    previous_metadata = baca.path.previous_metadata(pathlib.Path(music_py_path_name))
    if previous_metadata and not section_not_included_in_score:
        string = "final_measure_number"
        if string in previous_metadata:
            first_measure_number = previous_metadata[string] + 1
        else:
            first_measure_number = None
    else:
        first_measure_number = 1
    environment = Environment(
        arguments=arguments_,
        first_measure_number=first_measure_number,
        metadata=metadata,
        persist=persist,
        previous_metadata=previous_metadata,
        section_directory=section_directory,
        section_not_included_in_score=section_not_included_in_score,
        section_number=section_directory.name,
        timing=Timing(),
    )
    return environment


def remove_site_comments(path: pathlib.Path) -> None:
    with path.open() as pointer:
        lines = pointer.readlines()
    string = "".join(lines)
    string = abjad.format.remove_site_comments(string)
    path.write_text(string)


def run_lilypond(
    ly_file_path: pathlib.Path,
    *,
    lilypond_timeout: int = 0,
    pdf_mtime: float | None = None,
    remove: pathlib.Path | None = None,
):
    assert isinstance(ly_file_path, pathlib.Path), repr(ly_file_path)
    assert ly_file_path.exists(), repr(ly_file_path)
    if pdf_mtime is not None:
        assert isinstance(pdf_mtime, float), repr(pdf_mtime)
    if remove is not None:
        assert isinstance(remove, pathlib.Path), repr(remove)
    string = f"Calling LilyPond (with includes) on {baca.path.trim(ly_file_path)} ..."
    print_file_handling(string)
    directory = ly_file_path.parent
    pdf = ly_file_path.with_suffix(".pdf")
    lilypond_log_file_name = "." + ly_file_path.name + ".log"
    lilypond_log_file_path = directory / lilypond_log_file_name
    exit_code = 0
    with abjad.contextmanagers.temporary_directory_change(directory=directory):
        flags = get_includes()
        try:
            signal.alarm(lilypond_timeout)
            exit_code = abjad.io.run_lilypond(
                str(ly_file_path),
                flags=flags,
                lilypond_log_file_path=lilypond_log_file_path,
            )
            signal.alarm(0)
        except TimeoutException as e:
            print(e)
        _remove_lilypond_warnings(
            lilypond_log_file_path,
            crescendo_too_small=True,
            decrescendo_too_small=True,
            overwriting_glissando=True,
        )
        _display_lilypond_log_errors(lilypond_log_file_path)
        if remove is not None:
            print_file_remove(f"Removing {baca.path.trim(remove)} ...")
            shutil.rmtree(str(remove))
        if exit_code == 0 and pdf.is_file():
            if pdf_mtime is not None and pdf_mtime < os.path.getmtime(pdf):
                print_success(f"Modified {baca.path.trim(pdf)} ...")
            else:
                print_success(f"Found {baca.path.trim(pdf)} ...")
        assert lilypond_log_file_path.exists()
    return exit_code


def run_xelatex(tex_file_path):
    if not tex_file_path.is_file():
        print_error(f"Can not find {baca.path.trim(tex_file_path)} ...")
        return
    executables = abjad.io.find_executable("xelatex")
    executables = [pathlib.Path(_) for _ in executables]
    if not executables:
        executable_name = "pdflatex"
    else:
        executable_name = "xelatex"
    print_file_handling(
        f"Calling {executable_name} on {baca.path.trim(tex_file_path)} ..."
    )
    command = f" {executable_name} -halt-on-error"
    command += " -interaction=nonstopmode"
    command += f" --jobname={tex_file_path.stem}"
    command += f" -output-directory={tex_file_path.parent} {tex_file_path}"
    command += f" 1>{tex_file_path.stem}.log 2>&1"
    command_called_twice = f"{command}; {command}"
    with abjad.contextmanagers.temporary_directory_change(
        directory=tex_file_path.parent
    ):
        abjad.io.spawn_subprocess(command_called_twice)
        source = tex_file_path.with_suffix(".log")
        name = "." + tex_file_path.stem + ".tex_file_path.log"
        target = tex_file_path.parent / name
        shutil.move(str(source), str(target))
        for path in sorted(tex_file_path.parent.glob("*.aux")):
            path.unlink()
    pdf = tex_file_path.with_suffix(".pdf")
    if pdf.is_file():
        print_success(f"Found {baca.path.trim(pdf)} ...")
    else:
        print_error(f"Can not produce {baca.path.trim(pdf)} ...")
        sys.exit(1)


def show_annotations(file, *, undo=False):
    assert file.is_file(), repr(file)
    if "sections" not in file.parts:
        print_always("Must call on file in section directory ...")
        sys.exit(1)
    messages = []

    def _annotation_spanners(tags):
        tags_ = (
            baca.tags.MATERIAL_ANNOTATION_SPANNER,
            baca.tags.MOMENT_ANNOTATION_SPANNER,
            baca.tags.STAFF_HIGHLIGHT,
        )
        return bool(set(tags) & set(tags_))

    text = file.read_text()
    text = show_tag(
        text,
        "annotation spanners",
        messages,
        match=_annotation_spanners,
        undo=undo,
    )

    def _spacing(tags):
        tags_ = (baca.tags.SPACING,)
        return bool(set(tags) & set(tags_))

    text = show_tag(text, baca.tags.CLOCK_TIME, messages, undo=undo)
    text = show_tag(text, baca.tags.FIGURE_LABEL, messages, undo=undo)
    text = show_tag(text, baca.tags.INVISIBLE_MUSIC_COMMAND, messages, undo=not undo)
    text = show_tag(text, baca.tags.INVISIBLE_MUSIC_COLORING, messages, undo=undo)
    text = show_tag(text, baca.tags.LOCAL_MEASURE_NUMBER, messages, undo=undo)
    text = show_tag(text, baca.tags.MEASURE_NUMBER, messages, undo=undo)
    text = show_tag(text, baca.tags.MOCK_COLORING, messages, undo=undo)
    text = text = _show_music_annotations(text, messages, undo=undo)
    text = show_tag(text, baca.tags.NOT_YET_PITCHED_COLORING, messages, undo=undo)
    text = show_tag(text, "spacing", messages, match=_spacing, undo=undo)
    text = show_tag(text, baca.tags.STAGE_NUMBER, messages, undo=undo)
    file.write_text(text)
    return messages


def show_tag(
    text: str,
    tag: abjad.Tag | str,
    messages: list[str],
    *,
    match: typing.Callable | None = None,
    prepend_empty_chord: bool = False,
    undo: bool = False,
) -> str:
    if match is not None:
        assert callable(match)
    if isinstance(tag, str):
        assert match is not None, repr(match)
        name = tag
    else:
        assert isinstance(tag, abjad.Tag), repr(tag)
        name = tag.string

    if match is None:

        def match(tags):
            tags_ = [tag]
            return bool(set(tags) & set(tags_))

    if not undo:
        messages.append(f"Showing {name} tags ...")
        text = _activate_tags(text, match, name, messages)
    else:
        messages.append(f"Hiding {name} tags ...")
        text = _deactivate_tags(
            text,
            match,
            name,
            messages,
            prepend_empty_chord=prepend_empty_chord,
        )
    messages.append("")
    return text


def timed(timing_attribute):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*arguments, **keywords):
            timing = None
            if "environment" in keywords:
                timing = keywords["environment"].timing
            elif "timing" in keywords:
                timing = keywords.pop("timing")
            elif isinstance(arguments[-1], Timing):
                timing = arguments[-1]
                arguments = arguments[:-1]
            else:
                for argument in arguments:
                    if isinstance(argument, Environment):
                        timing = argument.timing
            with abjad.contextmanagers.Timer() as timer:
                result = function(*arguments, **keywords)
            if timing is not None:
                setattr(timing, timing_attribute, int(timer.elapsed_time()))
            return result

        return wrapper

    return decorator


def write_bol_metadata(directory, bol_measure_numbers):
    _metadata_path = directory / ".metadata"
    message = f"Writing {baca.path.trim(_metadata_path)} BOL measure numbers ..."
    print_file_handling(message)
    baca.path.add_metadatum(directory, "bol_measure_numbers", bol_measure_numbers)
