"""
Build.
"""

import dataclasses
import functools
import os
import pathlib
import pprint
import shutil
import sys
import time
import types
import typing

import abjad
import baca


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


def _call_lilypond_on_music_ly_in_section(music_ly, music_pdf_mtime):
    music_pdf = music_ly.with_name("music.pdf")
    with abjad.Timer() as timer:
        run_lilypond(music_ly, pdf_mtime=music_pdf_mtime)
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
    return int(timer.elapsed_time)


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


def _display_lilypond_log_errors(lilypond_log_file_path):
    lilypond_log_file_path = pathlib.Path(lilypond_log_file_path)
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
        for line in lines[:10]:
            print_always(line)


def _externalize_music_ly(music_ly):
    music_ily = music_ly.with_name("music.ily")
    print_file_handling(f"Externalizing {baca.path.trim(music_ly)} ...")
    baca.path.extern(music_ly, music_ily)
    assert music_ily.is_file()
    assert music_ily.parent.parent.name == "sections"
    for file in (music_ly, music_ily):
        text = file.read_text()
        messages = []
        text = _not_topmost(text, messages)
        file.write_text(text)
        if messages:
            messages = "\n".join(messages) + "\n"
            print_file_handling(
                "Appending not-topmost tags messages ...", log_only=True
            )
            _tags_file = file.with_name(f".{file.name}.tags")
            with _tags_file.open("a") as pointer:
                pointer.write(messages)


def _get_preamble_page_count_overview(path):
    assert path.is_file(), repr(path)
    first_page_number, page_count = 1, None
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith("% first_page_number = "):
                line = line.strip("% first_page_number = ")
                first_page_number = eval(line)
            if line.startswith("% page_count = "):
                line = line.strip("% page_count = ")
                page_count = eval(line)
    if isinstance(page_count, int):
        final_page_number = first_page_number + page_count - 1
        return first_page_number, page_count, final_page_number
    return None


def _get_preamble_time_signatures(path):
    assert path.is_file(), repr(path)
    start_line = "% time_signatures = ["
    stop_line = "%  ]"
    lines = []
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith(stop_line):
                lines.append("]")
                break
            if lines:
                lines.append(line.strip("%").strip("\n"))
            elif line.startswith(start_line):
                lines.append("[")
        string = "".join(lines)
        try:
            time_signatures = eval(string)
        except Exception:
            return []
        return time_signatures
    return None


def _handle_edition_tags(
    text: str, messages: list[str], directory_name: str, my_name: str
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

    """
    assert isinstance(text, str), repr(text)
    assert isinstance(directory_name, str), repr(directory_name)
    assert my_name in ("SECTION", "SCORE", "PARTS"), repr(my_name)
    messages.append("Handling edition tags ...")
    this_edition = abjad.Tag(f"+{my_name}")
    not_this_edition = abjad.Tag(f"-{my_name}")
    directory_name = abjad.string.to_shout_case(directory_name)
    this_directory = abjad.Tag(f"+{directory_name}")
    not_this_directory = abjad.Tag(f"-{directory_name}")

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
    for name in ("layout.ly", "music.ily", "music.ly"):
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
        text = _handle_edition_tags(text, messages, section_directory.name, "SECTION")
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
            parts.append("_timing")
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
        python_runtime = timing.make_score + timing.postprocess_score
        counter = abjad.string.pluralize("second", python_runtime)
        line = f"Python runtime: {python_runtime} {counter}\n"
        pointer.write(line)
        counter = abjad.string.pluralize("second", timing.make_score)
        line = f"  make_score(): {timing.make_score} {counter}\n"
        pointer.write(line)
        counter = abjad.string.pluralize("second", timing.postprocess_score)
        line = f"  postprocess_score(): {timing.postprocess_score} {counter}\n"
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
        time_signature = abjad.get.effective(skip, abjad.TimeSignature)
        time_signatures.append(time_signature)
    skips = abjad.select.leaves(global_skips)[:-1]
    metronome_marks = []
    for skip in skips:
        metronome_mark = abjad.get.effective(skip, abjad.MetronomeMark)
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
            metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            time_signature = abjad.TimeSignature((3, 4))
            notes = [abjad.Rest("r2.")]
        else:
            metronome_mark = metronome_marks[i]
            units_per_minute = round(metronome_mark.units_per_minute)
            metronome_mark = dataclasses.replace(
                metronome_mark,
                hide=False,
                units_per_minute=units_per_minute,
            )
            time_signature = dataclasses.replace(time_signature)
            numerator, denominator = time_signature.pair
            notes = []
            for _ in range(numerator):
                note = abjad.Note("fs,1", multiplier=(1, denominator))
                notes.append(note)
            notes[0].written_pitch = -23
        abjad.attach(time_signature, notes[0])
        abjad.attach(metronome_mark, notes[0])
        measure = abjad.Container(notes)
        staff.append(measure)
    score_block = abjad.Block("score", [score, abjad.Block("midi")])
    lilypond_file = abjad.LilyPondFile([score_block])
    print_file_handling(f"Writing {baca.path.trim(clicktrack_path)} ...")
    abjad.persist.as_midi(lilypond_file, clicktrack_file_name)
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
    abjad.persist.as_midi(lilypond_file, tmp_midi)
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
    _layout_ly_tags = music_ly.with_name(".layout.ly.tags")
    if _layout_ly_tags.exists():
        _layout_ly_tags.unlink()
    _music_ily_tags = music_ly.with_name(".music.ily.tags")
    if _music_ily_tags.exists():
        _music_ily_tags.unlink()
    _music_ly_tags = music_ly.with_name(".music.ly.tags")
    if _music_ly_tags.exists():
        _music_ly_tags.unlink()
    _externalize_music_ly(music_ly)
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
        baca.tags.SPACING_OVERRIDE,
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
    print_main_task("Populating _verbose repository ...")
    for name in ("music.ly", "music.ily", "layout.ly"):
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
                parts.append("_verbose")
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
    print_main_task("Populating _untagged repository ...")
    for name in ("music.ly", "music.ily", "layout.ly"):
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
                parts.append("_untagged")
            else:
                parts.append(part)
        _untagged = "/" + os.path.sep.join(parts)
        _untagged = pathlib.Path(_untagged)
        if not _untagged.parent.is_dir():
            _untagged.parent.mkdir(parents=True)
        _untagged.write_text(string)
    for name in ("music.ly", "music.ily", "layout.ly"):
        path = section_directory / name
        if not path.exists():
            continue
        safekeeping = section_directory / f"{name}.original"
        shutil.copyfile(path, safekeeping)
        color_persistent_indicators(path, undo=True)
        show_annotations(path, undo=True)
    print_main_task("Populating _bw repository ...")
    for name in ("music.ly", "music.ily", "layout.ly"):
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
                parts.append("_bw")
            else:
                parts.append(part)
        _bw = "/" + os.path.sep.join(parts)
        _bw = pathlib.Path(_bw)
        if not _bw.parent.is_dir():
            _bw.parent.mkdir(parents=True)
        _bw.write_text(string)
    for name in ("music.ly", "music.ily", "layout.ly"):
        path = section_directory / name
        if not path.exists():
            continue
        safekeeping = section_directory / f"{name}.original"
        shutil.move(safekeeping, path)


def _remove_function_name_comments(section_directory):
    print_file_handling("Removing function name comments ...")
    for name in ("music.ly", "music.ily", "layout.ly"):
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
    for name in ("music.ly", "music.ily", "layout.ly"):
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
    postprocess_score: int | None = None


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


Timer = abjad.Timer


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


def build_part(part_directory, debug_sections=False):
    assert part_directory.parent.name.endswith("-parts"), repr(part_directory)
    part_pdf = part_directory / "part.pdf"
    print_always(f"Building {baca.path.trim(part_pdf)} ...")
    layout_py = part_directory / "layout.py"
    # TODO: consider removing or hoisting to make
    os.system(f"python {layout_py}")
    interpret_build_music(part_directory, debug_sections=debug_sections)
    front_cover_tex = part_directory / "front-cover.tex"
    interpret_tex_file(front_cover_tex)
    preface_tex = part_directory / "preface.tex"
    interpret_tex_file(preface_tex)
    back_cover_tex = part_directory / "back-cover.tex"
    interpret_tex_file(back_cover_tex)
    part_tex = part_directory / "part.tex"
    interpret_tex_file(part_tex)


def build_score(score_directory, debug_sections=False):
    assert score_directory.name.endswith("-score"), repr(score_directory)
    assert score_directory.parent.name == "builds", repr(score_directory)
    print_main_task("Building score ...")
    interpret_build_music(score_directory, debug_sections=debug_sections)
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
            interpret_tex_file(tex)
        elif pdf.is_file():
            print_file_handling(f"Using existing {baca.path.trim(pdf)} ...")
    score_tex = score_directory / "score.tex"
    interpret_tex_file(score_tex)
    score_pdf = score_directory / "score.pdf"
    if not score_pdf.is_file():
        print_error(f"Can not find {baca.path.trim(score_pdf)} ...")
        print_error("PDF MISSING IN build_score()")
        os.system("cat .music.ly.log")
        sys.exit(1)


def collect_section_lys(_sections_directory):
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
            return True
        if baca.tags.HIDE_TO_JOIN_BROKEN_SPANNERS in tags:
            return True
        return False

    build_directory = _sections_directory.parent
    assert build_directory.parent.name == "builds", repr(build_directory)
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
            my_name = "SCORE"
        else:
            assert "-parts" in str(file)
            my_name = "PARTS"
        text = file.read_text()
        text = _handle_edition_tags(text, messages, "_sections", my_name)
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


def handle_part_tags(directory):
    directory = pathlib.Path(directory)
    if not directory.parent.name.endswith("-parts"):
        print_always("Must call script in part directory ...")
        sys.exit(1)
    parts_directory = directory.parent

    def _activate(
        path,
        tag,
        *,
        deactivate=False,
        name=None,
    ):
        if isinstance(tag, str):
            tag_ = abjad.Tag(tag)
        else:
            assert callable(tag)
            tag_ = tag
        assert isinstance(tag_, abjad.Tag) or callable(tag_)
        if deactivate:
            result = baca.path.deactivate(path, tag_, name=name)
            assert result is not None
            count, skipped, messages = result
        else:
            result = baca.path.activate(path, tag_, name=name)
            assert result is not None
            count, skipped, messages = result
        for message in messages:
            print_tags(message)

    def _deactivate(
        path,
        tag,
        *,
        name=None,
    ):
        _activate(
            path,
            tag,
            name=name,
            deactivate=True,
        )

    def _parse_part_identifier(path):
        if path.suffix == ".ly":
            part_identifier = None
            with path.open("r") as pointer:
                for line in pointer.readlines():
                    if line.startswith("% part_identifier = "):
                        line = line.strip("% part_identifier = ")
                        part_identifier = eval(line)
                        return part_identifier
        elif path.name.endswith("layout.py"):
            part_identifier = None
            with path.open("r") as pointer:
                for line in pointer.readlines():
                    if line.startswith("part_identifier = "):
                        line = line.strip("part_identifier = ")
                        part_identifier = eval(line)
                        return part_identifier
        else:
            raise TypeError(path)

    music_ly = list(directory.glob("*music.ly"))[0]
    _activate(
        parts_directory,
        "+PARTS",
    )
    _deactivate(
        parts_directory,
        "-PARTS",
    )
    _deactivate(
        parts_directory,
        "HIDE_IN_PARTS",
    )
    part_identifier = _parse_part_identifier(music_ly)
    if part_identifier is None:
        message = f"No part identifier found in {baca.path.trim(music_ly)} ..."
        print_file_handling(message)
        sys.exit()
    parts_directory_name = abjad.string.to_shout_case(parts_directory.name)
    name = f"{parts_directory_name}_{part_identifier}"
    _activate(
        parts_directory,
        f"+{name}",
    )
    _deactivate(
        parts_directory,
        f"-{name}",
    )
    _deactivate(
        parts_directory,
        str(baca.tags.METRIC_MODULATION_IS_SCALED),
    )
    _deactivate(
        parts_directory,
        str(baca.tags.METRIC_MODULATION_IS_NOT_SCALED),
    )
    _activate(
        parts_directory,
        str(baca.tags.METRIC_MODULATION_IS_STRIPPED),
    )
    # HACK TO HIDE ALL POST-FERMATA-MEASURE TRANSPARENT BAR LINES;
    # this only works if parts contain no EOL fermata measure:
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE),
    )
    _activate(
        parts_directory,
        str(baca.tags.NOT_TOPMOST),
    )
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE_EMPTY_BAR_EXTENT),
    )
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE_NEXT_BAR_EXTENT),
    )
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE_RESUME_BAR_EXTENT),
    )
    _deactivate(
        parts_directory,
        str(baca.tags.EXPLICIT_BAR_EXTENT),
    )


def interpret_build_music(
    build_directory,
    *,
    debug_sections=False,
    skip_section_collection=False,
):
    """
    Interprets music.ly file in build directory.

    Collects sections and handles tags.
    """
    build_type = None
    if build_directory.name.endswith("-score"):
        build_type = "score"
    if build_directory.parent.name.endswith("-parts"):
        build_type = "part"
    if build_type is None:
        print_always("Must call script in score directory or part directory ...")
        sys.exit(1)
    music_ly = build_directory / "music.ly"
    if not music_ly.is_file():
        raise Exception(f"Missing {baca.path.trim(music_ly)} ...")
    if build_type == "score":
        _sections_directory = build_directory / "_sections"
    else:
        assert build_type == "part"
        _sections_directory = build_directory.parent / "_sections"
    if skip_section_collection:
        print_file_handling("Skipping section collection ...")
    else:
        collect_section_lys(_sections_directory)
    if build_directory.parent.name.endswith("-parts"):
        if skip_section_collection:
            print_tags("Skipping tag handling ...")
        else:
            handle_part_tags(build_directory)
    contents_directory = baca.path.get_contents_directory(build_directory)
    metadata = baca.path.get_metadata(contents_directory)
    do_not_populate_remote_repos = metadata.get("do_not_populate_remote_repos")
    if "trevor" in _sections_directory.parts and not do_not_populate_remote_repos:
        print_main_task("Populating _builds repository ...")
        parts = list(_sections_directory.parts)
        assert parts[3] == "Scores"
        parts[3] = "_builds"
        _builds_sections_directory = os.sep + os.sep.join(parts[1:])
        shutil.copytree(
            _sections_directory, _builds_sections_directory, dirs_exist_ok=True
        )
    remove = None
    if _sections_directory.is_dir() and not debug_sections:
        remove = _sections_directory
    music_pdf = music_ly.with_name("music.pdf")
    if music_pdf.is_file():
        print_file_handling(f"Existing {baca.path.trim(music_pdf)} ...", log_only=True)
    run_lilypond(music_ly, remove=remove)


def interpret_tex_file(tex):
    if not tex.is_file():
        print_error(f"Can not find {baca.path.trim(tex)} ...")
        return
    executables = abjad.io.find_executable("xelatex")
    executables = [pathlib.Path(_) for _ in executables]
    if not executables:
        executable_name = "pdflatex"
    else:
        executable_name = "xelatex"
    print_file_handling(f"Calling {executable_name} on {baca.path.trim(tex)} ...")
    command = f" {executable_name} -halt-on-error"
    command += " -interaction=nonstopmode"
    command += f" --jobname={tex.stem}"
    command += f" -output-directory={tex.parent} {tex}"
    command += f" 1>{tex.stem}.log 2>&1"
    command_called_twice = f"{command}; {command}"
    with abjad.TemporaryDirectoryChange(directory=tex.parent):
        abjad.io.spawn_subprocess(command_called_twice)
        source = tex.with_suffix(".log")
        name = "." + tex.stem + ".tex.log"
        target = tex.parent / name
        shutil.move(str(source), str(target))
        for path in sorted(tex.parent.glob("*.aux")):
            path.unlink()
    pdf = tex.with_suffix(".pdf")
    if pdf.is_file():
        print_success(f"Found {baca.path.trim(pdf)} ...")
    else:
        print_error(f"Can not produce {baca.path.trim(pdf)} ...")
        sys.exit(1)


def persist_as_ly(argument, ly_file_path):
    print_file_handling(f"Writing {baca.path.trim(ly_file_path)} ...")
    abjad.persist.as_ly(argument, ly_file_path)


def persist_lilypond_file(
    arguments: types.SimpleNamespace,
    section_directory: pathlib.Path,
    timing: Timing,
    lilypond_file: abjad.LilyPondFile,
    metadata: types.MappingProxyType,
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
            log_timing=arguments.log_timing,
            print_timing=arguments.print_timing,
        )


def print_all_timing(timing):
    if hasattr(timing, "make_score"):
        python_runtime = timing.make_score + timing.postprocess_score
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


def run_lilypond(ly_file_path, *, pdf_mtime=None, remove=None):
    assert ly_file_path.exists(), repr(ly_file_path)
    string = f"Calling LilyPond (with includes) on {baca.path.trim(ly_file_path)} ..."
    print_file_handling(string)
    directory = ly_file_path.parent
    pdf = ly_file_path.with_suffix(".pdf")
    lilypond_log_file_name = "." + ly_file_path.name + ".log"
    lilypond_log_file_path = directory / lilypond_log_file_name
    with abjad.TemporaryDirectoryChange(directory=directory):
        flags = get_includes()
        abjad.io.run_lilypond(
            str(ly_file_path),
            flags=flags,
            lilypond_log_file_path=(lilypond_log_file_path),
        )
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
        if pdf.is_file():
            if pdf_mtime is not None and pdf_mtime < os.path.getmtime(pdf):
                print_success(f"Modified {baca.path.trim(pdf)} ...")
            else:
                print_success(f"Found {baca.path.trim(pdf)} ...")
        else:
            print_error(f"Can not find {baca.path.trim(pdf)} ...")
            print_error("PDF MISSING IN run_lilypond()")
            os.system("cat .music.ly.log")
        assert lilypond_log_file_path.exists()


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
        tags_ = (
            baca.tags.SPACING,
            baca.tags.SPACING_OVERRIDE,
        )
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
            with abjad.Timer() as timer:
                result = function(*arguments, **keywords)
            if timing is not None:
                setattr(timing, timing_attribute, int(timer.elapsed_time))
            return result

        return wrapper

    return decorator


def write_layout_ly(
    breaks,
    spacing=None,
    *,
    curtail_measure_count=None,
    do_not_write_metadata=False,
    file_name="layout.ly",
    page_layout_context_only=False,
    time_signatures=None,
):
    layout_directory = pathlib.Path(os.getcwd())
    print_main_task("Making layout ...")
    assert isinstance(breaks, baca.layout.Breaks), repr(breaks)
    if spacing is not None:
        assert isinstance(spacing, baca.layout.Spacing), repr(spacing)
    layout_py = layout_directory / "layout.py"
    layout_ly = layout_directory / file_name
    if spacing is not None and spacing.spacing_overrides is not None:
        assert spacing.default_spacing is not None
    if spacing is not None and spacing.default_spacing is None:
        eol_measure_numbers = None
        fermata_measure_numbers = None
        measure_count = None
    else:
        tuple_ = baca.path.get_measure_profile_metadata(layout_py)
        first_measure_number = tuple_[0]
        measure_count = tuple_[1]
        fermata_measure_numbers = tuple_[2] or []
        first_measure_number = first_measure_number or 1
        fermata_measure_numbers = [
            _ - (first_measure_number - 1) for _ in fermata_measure_numbers
        ]
        eol_measure_numbers = []
        for bol_measure_number in breaks.bol_measure_numbers[1:]:
            eol_measure_number = bol_measure_number - 1
            eol_measure_numbers.append(eol_measure_number)
    # TODO: use dataclass:
    page_layout_profile = {
        "eol_measure_numbers": eol_measure_numbers,
        "fermata_measure_numbers": fermata_measure_numbers,
        "measure_count": measure_count,
    }
    # TODO: do not read from environment; pass into function instead:
    has_anchor_skip = baca.path.get_metadata(layout_directory).get("has_anchor_skip")
    document_name = abjad.string.to_shout_case(layout_directory.name)
    if time_signatures is not None:
        first_measure_number = 1
    elif layout_directory.parent.name == "sections":
        string = "first_measure_number"
        first_measure_number = baca.path.get_metadata(layout_directory).get(string, 1)
        if not bool(first_measure_number):
            print_file_handling("Can not find first measure number ...")
            first_measure_number = False
        assert isinstance(first_measure_number, int)
        time_signatures = baca.path.get_metadata(layout_directory).get(
            "time_signatures"
        )
    else:
        first_measure_number = 1
        time_signatures = []
        contents_directory = baca.path.get_contents_directory(layout_directory)
        sections_directory = contents_directory / "sections"
        for section_directory in sorted(sections_directory.glob("*")):
            if not section_directory.is_dir():
                continue
            time_signatures_ = baca.path.get_metadata(section_directory).get(
                "time_signatures",
            )
            time_signatures.extend(time_signatures_)
    if first_measure_number is False:
        raise Exception("first_measure_number should not be false")
        print_file_handling(f"Skipping {baca.path.trim(layout_py)} ...")
        sys.exit(1)
    assert abjad.string.is_shout_case(document_name)
    score = baca.docs.make_empty_score(1, do_not_move_global_context=True)
    time_signatures_ = [abjad.TimeSignature.from_string(_) for _ in time_signatures]
    baca.section.set_up_score(
        score,
        time_signatures_,
        append_anchor_skip=has_anchor_skip,
        layout=True,
    )
    if spacing is not None:
        spacing(score, page_layout_profile, has_anchor_skip=has_anchor_skip)
    breaks(score)
    offset_to_measure_number = baca.section._populate_offset_to_measure_number(
        first_measure_number,
        score["Skips"],
    )
    baca.section._comment_measure_numbers(
        first_measure_number, offset_to_measure_number, score
    )
    baca.section._whitespace_leaves(score)
    baca.section._add_container_identifiers(score, None)
    baca.section.style_anchor_skip(score)
    baca.section._remove_layout_tags(score)
    lilypond_file = baca.lilypond.file(score)
    context = lilypond_file["Skips"]
    if curtail_measure_count is not None:
        del context[curtail_measure_count:]
    context.lilypond_type = "PageLayout"
    context.name = "PageLayout"
    skips = baca.select.skips(context)
    for skip in skips:
        abjad.detach(abjad.TimeSignature, skip)
    score = lilypond_file["Score"]
    del score["MusicContext"]
    score = lilypond_file["Score"]
    if page_layout_context_only:
        context = score["PageLayout"]
    else:
        context = score
    for component in abjad.iterate.components(context):
        component.tag = component.tag.retain_shoutcase()
        for wrapper in abjad.get.wrappers(component):
            wrapper.tag = wrapper.tag.retain_shoutcase()
    text = abjad.lilypond(context, tags=True)
    text = text.replace("Skips", "PageLayout")
    text = text.replace("GlobalSkips", "PageLayout")
    text = abjad.tag.left_shift_tags(text)
    layout_ly = layout_directory / file_name
    lines = []
    # TODO: remove first_page_number embedding
    if layout_directory.parent.name == "sections":
        if layout_directory.name != "01":
            previous_section_number = str(int(layout_directory.name) - 1).zfill(2)
            previous_section_directory = (
                layout_directory.parent / previous_section_number
            )
            previous_layout_ly = previous_section_directory / "layout.ly"
            if previous_layout_ly.is_file():
                result = _get_preamble_page_count_overview(previous_layout_ly)
                if result is not None:
                    _, _, final_page_number = result
                    first_page_number = final_page_number + 1
                    line = f"% first_page_number = {first_page_number}"
                    lines.append(line)
    page_count = breaks.page_count
    lines.append(f"% page_count = {page_count}")
    time_signatures = [str(_) for _ in time_signatures]
    measure_count = len(time_signatures)
    if has_anchor_skip:
        lines.append(f"% measure_count = {measure_count} + 1")
    else:
        lines.append(f"% measure_count = {measure_count}")
    string = pprint.pformat(time_signatures, compact=True, width=80 - 3)
    lines_ = string.split("\n")
    lines_ = [_.strip("[").strip("]") for _ in lines_]
    lines_ = ["% " + _ for _ in lines_]
    lines_.insert(0, "% time_signatures = [")
    lines_.append("%  ]")
    lines.extend(lines_)
    header = "\n".join(lines) + "\n\n"
    layout_ly.write_text(header + text + "\n")
    counter = abjad.string.pluralize("measure", measure_count)
    message = f"Writing {measure_count} + 1 {counter} to"
    message += f" {baca.path.trim(layout_ly)} ..."
    print_file_handling(message)
    bol_measure_numbers = []
    skips = abjad.iterate.leaves(score["PageLayout"], abjad.Skip)
    for i, skip in enumerate(skips):
        for literal in abjad.get.indicators(skip, abjad.LilyPondLiteral):
            if literal.argument in (r"\break", r"\pageBreak"):
                measure_number = first_measure_number + i
                bol_measure_numbers.append(measure_number)
                continue
    count = len(bol_measure_numbers)
    numbers = abjad.string.pluralize("number", count)
    if not do_not_write_metadata:
        metadata = layout_directory / ".metadata"
        string = baca.path.trim(metadata)
        message = f"Writing BOL measure {numbers} to {string} ..."
        print_file_handling(message)
        if layout_directory.name.endswith("-parts"):
            if document_name is not None:
                part_dictionary = baca.path.get_metadata(layout_directory).get(
                    document_name,
                    {},
                )
            else:
                part_dictionary = {}
            part_dictionary["bol_measure_numbers"] = bol_measure_numbers
            assert abjad.string.is_shout_case(document_name)
            baca.path.add_metadatum(layout_directory, document_name, part_dictionary)
        else:
            baca.path.add_metadatum(
                layout_directory,
                "bol_measure_numbers",
                bol_measure_numbers,
            )
