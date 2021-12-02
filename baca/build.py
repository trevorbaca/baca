"""
Build.
"""
import os
import pathlib
import pprint
import shutil
import sys
import time
import types
from inspect import currentframe as _frame

import abjad
import baca

from . import scoping as _scoping

_colors = baca.const.colors


__also_untagged = "--also-untagged" in sys.argv
__clicktrack = "--clicktrack" in sys.argv
__debug_segments = "--debug-segments" in sys.argv
__log_timing = "--log-timing" in sys.argv
__midi = "--midi" in sys.argv
__pdf = "--pdf" in sys.argv
__print_file_handling = "--print-file-handling" in sys.argv or "--verbose" in sys.argv
__print_layout = "--print-layout" in sys.argv or "--verbose" in sys.argv
__print_tags = "--print-tags" in sys.argv or "--verbose" in sys.argv
__print_tex = "--print-tex" in sys.argv or "--verbose" in sys.argv
__print_timing = "--print-timing" in sys.argv or "--verbose" in sys.argv
__redo_layout = "--redo-layout" in sys.argv
__verbose = "--verbose" in sys.argv


# TODO: replace with segment-specific stylesheets
def _add_nonfirst_segment_preamble(lilypond_file, segment_directory):
    if segment_directory.name == "01":
        return
    layout_ly = segment_directory / "layout.ly"
    if not layout_ly.is_file():
        return
    result = _get_preamble_page_count_overview(layout_ly)
    if result is None:
        return
    first_page_number, _, _ = result
    line = r"\paper { first-page-number = #"
    line += str(first_page_number)
    line += " }"
    lines = abjad.tag.double_tag([line], _scoping.site(_frame()))
    lines.append("")
    lilypond_file.items[-1:-1] = lines


def _also_untagged(segment_directory):
    if not __also_untagged:
        return
    if os.environ.get("GITHUB_WORKSPACE"):
        return
    for name in ("music.ly", "music.ily", "layout.ly"):
        tagged = segment_directory / name
        if not tagged.exists():
            continue
        with tagged.open() as pointer:
            lines = []
            for line in pointer.readlines():
                if "%@%" not in line:
                    lines.append(line)
        string = "".join(lines)
        string = abjad.lilypondformat.remove_tags(string)
        parts = []
        for part in tagged.parts:
            if part == os.path.sep:
                pass
            elif part == "Scores":
                parts.append("untagged")
            else:
                parts.append(part)
        untagged = "/" + os.path.sep.join(parts)
        untagged = pathlib.Path(untagged)
        if not untagged.parent.is_dir():
            untagged.parent.mkdir(parents=True)
        _print_file_handling(f"Writing {untagged} ...")
        untagged.write_text(string)


def _call_lilypond_on_music_ly_in_segment(music_ly, music_pdf_mtime):
    lilypond_log_file_name = "." + music_ly.name + ".log"
    lilypond_log_file_path = music_ly.parent / lilypond_log_file_name
    music_pdf = music_ly.with_name("music.pdf")
    with abjad.Timer() as timer:
        run_lilypond(music_ly)
        music_ly_pdf = music_ly.parent / "music.ly.pdf"
        if music_ly_pdf.is_file():
            shutil.move(str(music_ly_pdf), str(music_pdf))
    _remove_lilypond_warnings(
        lilypond_log_file_path,
        crescendo_too_small=True,
        decrescendo_too_small=True,
        overwriting_glissando=True,
    )
    if music_pdf.is_file() and music_pdf_mtime < os.path.getmtime(music_pdf):
        _print_file_handling(f"Modified {baca.path.trim(music_pdf)} ...")
    _print_timing("LilyPond runtime", int(timer.elapsed_time))
    return int(timer.elapsed_time)


def _check_layout_time_signatures_in_build(music_ly):
    _print_layout("Checking layout time signatures ...")
    build_directory = music_ly.parent
    layout_ly_file_path = build_directory / "layout.ly"
    if not layout_ly_file_path.is_file():
        _print_layout(f"No {baca.path.trim(layout_ly_file_path)} found ...")
        return
    _print_file_handling(f"Found {baca.path.trim(layout_ly_file_path)} ...")
    metadata_time_signatures = []
    segments_directory = build_directory / "segments"
    for segment_directory in sorted(segments_directory.glob("*")):
        time_signatures = baca.path.get_metadatum(segment_directory, "time_signatures")
        metadata_time_signatures.extend(time_signatures)
    if metadata_time_signatures:
        _print_file_handling("Found time signature metadata ...")
    layout_time_signatures = _get_preamble_time_signatures(layout_ly_file_path)
    if layout_time_signatures == metadata_time_signatures:
        message = "Layout time signatures"
        message += f" ({len(layout_time_signatures)})"
        message += " match metadata time signatures"
        message += f" ({len(metadata_time_signatures)}) ..."
        _print_layout(message)
        return
    message = "Layout time signatures"
    message += f" ({len(layout_time_signatures)})"
    message += " do not match metadata time signatures"
    message += f" ({len(metadata_time_signatures)}) ..."
    _print_layout(message)
    _print_layout(f"Remaking {baca.path.trim(layout_ly_file_path)} ...")
    layout_py = layout_ly_file_path.with_suffix(".py")
    # TODO: consider removing
    os.system(f"python {layout_py}")
    layout_time_signatures = _get_preamble_time_signatures(layout_ly_file_path)
    if layout_time_signatures == metadata_time_signatures:
        message = "Layout time signatures"
        message += f" ({len(layout_time_signatures)})"
        message += " match metadata time signatures"
        message += f" ({len(metadata_time_signatures)}) ..."
    else:
        message = "Layout time signatures"
        message += f" ({len(layout_time_signatures)})"
        message += " still do not match metadata time signatures"
        message += f" ({len(metadata_time_signatures)}) ..."
    _print_layout(message)


def _check_layout_time_signatures_in_segment(
    segment_directory,
    nonphantom_time_signatures,
):
    measure_count = len(nonphantom_time_signatures)
    layout_py = segment_directory / "layout.py"
    music_ly = segment_directory / "music.ly"
    if not layout_py.exists():
        _print_layout(f"No {baca.path.trim(layout_py)} found ...")
        return
    layout_ly = segment_directory / "layout.ly"
    layout_time_signatures = _get_preamble_time_signatures(layout_ly)
    if layout_time_signatures is not None:
        assert isinstance(layout_time_signatures, list)
        layout_measure_count = len(layout_time_signatures)
        counter = abjad.String("measure").pluralize(layout_measure_count)
        message = f"Found {layout_measure_count} {counter}"
        message += f" in {baca.path.trim(layout_ly)} ..."
        _print_layout(message)
        if layout_time_signatures == nonphantom_time_signatures:
            _print_layout("Music time signatures match layout time signatures ...")
        # TODO: consider removing
        else:
            message = "Music time signatures do not match layout time signatures ..."
            _print_layout(message)
            _print_layout(f"Remaking {baca.path.trim(layout_ly)} ...")
            os.system(f"python {layout_py}")
            counter = abjad.String("measure").pluralize(measure_count)
            message = f"Found {measure_count} {counter}"
            message += f" in {baca.path.trim(music_ly)} ..."
            _print_layout(message)
            layout_time_signatures = _get_preamble_time_signatures(layout_ly)
            layout_measure_count = len(layout_time_signatures)
            counter = abjad.String("measure").pluralize(layout_measure_count)
            message = f"Found {layout_measure_count} {counter}"
            message += f" in {baca.path.trim(layout_ly)} ..."
            _print_layout(message)
            if layout_time_signatures != nonphantom_time_signatures:
                message = "Music time signatures still do not match"
                message += " layout time signatures ..."
                _print_layout(message)


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
            _print_always("ERROR IN LILYPOND LOG FILE ...")
            error = True
            break
    if error:
        for line in lines[:10]:
            _print_always(line)


def _externalize_music_ly(music_ly):
    music_ily = music_ly.with_name("music.ily")
    baca.path.extern(music_ly, music_ily)
    assert music_ily.is_file()
    not_topmost = baca.jobs.Job(
        deactivate=(baca.tags.NOT_TOPMOST, "not topmost"),
        path=music_ly.parent,
        title=f"Deactivating {str(baca.tags.NOT_TOPMOST)} ...",
    )
    for message in not_topmost():
        _print_tags(message)


def _get_lilypond_include_string():
    abjad_repo = pathlib.Path(abjad.__file__).parent.parent
    baca_repo = pathlib.Path(baca.__file__).parent.parent
    string = f"--include={abjad_repo}/docs/source/_stylesheets"
    string += f" --include={baca_repo}/lilypond"
    return string


def _get_nonphantom_time_signatures(lilypond_file):
    global_skips = lilypond_file["Global_Skips"]
    time_signatures = []
    for skip in global_skips:
        time_signature = abjad.get.effective(skip, abjad.TimeSignature)
        assert isinstance(time_signature, abjad.TimeSignature), repr(time_signature)
        time_signatures.append(str(time_signature))
    # for phantom measure at end
    if 0 < len(time_signatures):
        time_signatures.pop()
    return time_signatures


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


def _get_previous_metadata(segment_directory):
    if segment_directory.name == "01":
        previous_metadata = None
        previous_persist = None
    else:
        previous_segment = str(int(segment_directory.name) - 1).zfill(2)
        previous_segment = segment_directory.parent / previous_segment
        path = previous_segment / "__metadata__"
        file = pathlib.Path(path)
        if file.is_file():
            string = file.read_text()
            previous_metadata = eval(string)
        else:
            previous_metadata = None
        path = previous_segment / "__persist__"
        file = pathlib.Path(path)
        if file.is_file():
            lines = file.read_text()
            previous_persist = eval(lines)
        else:
            previous_persist = None
    return previous_metadata, previous_persist


def _handle_music_ly_tags_in_segment(music_ly):
    text = music_ly.read_text()
    text = abjad.lilypondformat.left_shift_tags(text)
    music_ly.write_text(text)
    for job in (
        baca.jobs.handle_edition_tags(music_ly),
        baca.jobs.handle_fermata_bar_lines(music_ly.parent),
        baca.jobs.handle_shifted_clefs(music_ly.parent),
        baca.jobs.handle_mol_tags(music_ly.parent),
    ):
        for message in job():
            _print_tags(message)


def _log_timing(segment_directory, timing):
    if not __log_timing:
        return
    _timing = segment_directory / ".timing"
    with _timing.open(mode="a") as pointer:
        pointer.write("\n")
        line = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        pointer.write(line)
        counter = abjad.String("second").pluralize(timing.runtime)
        line = f"Segment interpretation time: {timing.runtime} {counter}\n"
        pointer.write(line)
        counter = abjad.String("second").pluralize(timing.abjad_format_time)
        line = f"Abjad format time: {timing.abjad_format_time} {counter}\n"
        pointer.write(line)
        counter = abjad.String("second").pluralize(timing.lilypond_runtime)
        line = f"LilyPond runtime: {timing.lilypond_runtime} {counter}\n"
        pointer.write(line)


def _make_annotation_jobs(directory, *, undo=False):
    def _annotation_spanners(tags):
        tags_ = (
            baca.tags.MATERIAL_ANNOTATION_SPANNER,
            baca.tags.PITCH_ANNOTATION_SPANNER,
            baca.tags.RHYTHM_ANNOTATION_SPANNER,
        )
        return bool(set(tags) & set(tags_))

    annotation_spanners = baca.jobs.show_tag(
        directory,
        "annotation spanners",
        match=_annotation_spanners,
        undo=undo,
    )

    def _spacing(tags):
        tags_ = (
            baca.tags.SPACING,
            baca.tags.SPACING_OVERRIDE,
        )
        return bool(set(tags) & set(tags_))

    spacing = baca.jobs.show_tag(directory, "spacing", match=_spacing, undo=undo)

    jobs = [
        annotation_spanners,
        baca.jobs.show_tag(directory, baca.tags.CLOCK_TIME, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.FIGURE_NAME, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.INVISIBLE_MUSIC_COMMAND, undo=not undo),
        baca.jobs.show_tag(directory, baca.tags.INVISIBLE_MUSIC_COLORING, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.LOCAL_MEASURE_NUMBER, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.MEASURE_NUMBER, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.MOCK_COLORING, undo=undo),
        baca.jobs.show_music_annotations(directory, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.NOT_YET_PITCHED_COLORING, undo=undo),
        baca.jobs.show_tag(directory, baca.tags.RHYTHM_ANNOTATION_SPANNER, undo=undo),
        spacing,
        baca.jobs.show_tag(directory, baca.tags.STAGE_NUMBER, undo=undo),
    ]

    return jobs


def _make_segment_clicktrack(lilypond_file):
    segment_directory = pathlib.Path(os.getcwd())
    _print_main_task(f"Making clicktrack for segment {segment_directory.name} ...")
    global_skips = lilypond_file["Global_Skips"]
    time_signatures = []
    for skip in global_skips[:-1]:
        time_signature = abjad.get.effective(skip, abjad.TimeSignature)
        time_signatures.append(time_signature)
    skips = abjad.select(global_skips).leaves()[:-1]
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
    if "Global_Rests" in lilypond_file:
        global_rests = lilypond_file["Global_Rests"]
        for i, rest in enumerate(global_rests):
            if abjad.get.has_indicator(rest, baca.const.FERMATA_MEASURE):
                measure_number = i + 1
                fermata_measure_numbers.append(measure_number)
    for i, time_signature in enumerate(time_signatures):
        measure_number = i + 1
        if measure_number in fermata_measure_numbers:
            metronome_mark = abjad.MetronomeMark((1, 4), 60)
            time_signature = abjad.TimeSignature((3, 4))
            notes = [abjad.Rest("r2.")]
        else:
            metronome_mark = metronome_marks[i]
            units_per_minute = round(metronome_mark.units_per_minute)
            metronome_mark = abjad.new(
                metronome_mark,
                hide=False,
                units_per_minute=units_per_minute,
            )
            time_signature = abjad.new(time_signature)
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
    clicktrack_file_name = "clicktrack.midi"
    _print_file_handling("Persisting LilyPond file as MIDI ...")
    abjad.persist.as_midi(lilypond_file, clicktrack_file_name, remove_ly=True)
    clicktrack_path = segment_directory / clicktrack_file_name
    if clicktrack_path.is_file():
        _print_success(f"Found {baca.path.trim(clicktrack_path)} ...")
    else:
        _print_error(f"Can not find {baca.path.trim(clicktrack_path)} ...")


def _make_segment_midi(lilypond_file):
    segment_directory = pathlib.Path(os.getcwd())
    _print_main_task(f"Making MIDI for segment {segment_directory.name} ...")
    music_midi = segment_directory / "music.midi"
    if music_midi.exists():
        _print_file_handling(f"Removing {baca.path.trim(music_midi)} ...")
        music_midi.unlink()
    score = lilypond_file["Score"]
    score_block = abjad.Block("score", [score, abjad.Block("midi")])
    lilypond_file = abjad.LilyPondFile([score_block])
    tmp_midi = segment_directory / "tmp.midi"
    abjad.persist.as_midi(lilypond_file, tmp_midi)
    if tmp_midi.is_file():
        shutil.move(tmp_midi, music_midi)
    tmp_ly = tmp_midi.with_suffix(".ly")
    if tmp_ly.exists():
        tmp_ly.unlink()
    if music_midi.is_file():
        _print_success(f"Found {baca.path.trim(music_midi)} ...")
    else:
        _print_error(f"Can not find {baca.path.trim(music_midi)} ...")


def _make_segment_pdf(lilypond_file, metadata, persist, timing):
    segment_directory = pathlib.Path(os.getcwd())
    _print_main_task(f"Making PDF for segment {segment_directory.name} ...")
    music_pdf = segment_directory / "music.pdf"
    music_ly = segment_directory / "music.ly"
    music_pdf_mtime = os.path.getmtime(music_pdf) if music_pdf.is_file() else 0
    music_ly_mtime = os.path.getmtime(music_ly) if music_ly.is_file() else 0
    nonphantom_time_signatures = _get_nonphantom_time_signatures(lilypond_file)
    _write_metadata(metadata, persist, segment_directory)
    _add_nonfirst_segment_preamble(lilypond_file, segment_directory)
    timing.abjad_format_time = _write_music_ly(lilypond_file, music_ly)
    _message_music_ly_timing(
        timing.abjad_format_time, music_ly, music_ly_mtime, nonphantom_time_signatures
    )
    _handle_music_ly_tags_in_segment(music_ly)
    _check_layout_time_signatures_in_segment(
        segment_directory,
        nonphantom_time_signatures,
    )
    _externalize_music_ly(music_ly)
    timing.lilypond_runtime = _call_lilypond_on_music_ly_in_segment(
        music_ly,
        music_pdf_mtime,
    )
    _also_untagged(segment_directory)
    _log_timing(segment_directory, timing)


def _message_music_ly_timing(
    abjad_format_time, music_ly, music_ly_mtime, nonphantom_time_signatures
):
    if music_ly.is_file() and music_ly_mtime < os.path.getmtime(music_ly):
        count = len(nonphantom_time_signatures)
        message = f"Wrote {baca.path.trim(music_ly)} with {count} + 1 measures ..."
        _print_file_handling(message)
        _print_timing("Abjad format time", abjad_format_time)


def _print_always(string):
    print(string)


def _print_error(string):
    print(_colors.red + string + _colors.end)


def _print_file_handling(string):
    if __print_file_handling:
        print(_colors.yellow + string + _colors.end)


def _print_layout(string):
    if __print_layout:
        print(_colors.cyan + string + _colors.end)


def _print_main_task(string):
    print(_colors.blue + string + _colors.end)


def _print_success(string):
    print(_colors.green_bold + string + _colors.end)


def _print_tags(string):
    if __print_tags:
        print(_colors.blue + string + _colors.end)


def _print_tex(string):
    if __print_tags:
        print(_colors.magenta + string + _colors.end)


def _print_timing(title, timer):
    if not __print_timing:
        return
    if isinstance(timer, int):
        count = timer
    else:
        count = int(timer.elapsed_time)
    counter = abjad.String("second").pluralize(count)
    count = str(count)
    string = f"{_colors.cyan}{title} {count} {counter} ...{_colors.end}"
    print(string)


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


def _write_metadata(metadata, persist, segment_directory):
    metadata_file = segment_directory / "__metadata__"
    _print_file_handling(f"Writing {baca.path.trim(metadata_file)} ...")
    baca.path.write_metadata_py(segment_directory, metadata)
    # TODO: import black here instead
    os.system("black --target-version=py38 __metadata__ 1>/dev/null 2>&1")
    persist_file = segment_directory / "__persist__"
    _print_file_handling(f"Writing {baca.path.trim(persist_file)} ...")
    baca.path.write_metadata_py(
        segment_directory,
        persist,
        file_name="__persist__",
        variable_name="persist",
    )
    # TODO: import black here instead
    os.system("black --target-version=py38 __persist__ 1>/dev/null 2>&1")


def _write_music_ly(lilypond_file, music_ly):
    result = abjad.persist.as_ly(lilypond_file, music_ly, tags=True)
    abjad_format_time = int(result[1])
    return abjad_format_time


def build_part(part_directory):
    assert part_directory.parent.name.endswith("-parts"), repr(part_directory)
    part_pdf = part_directory / "part.pdf"
    _print_always(f"Building {baca.path.trim(part_pdf)} ...")
    layout_py = part_directory / "layout.py"
    # TODO: consider removing or hoisting to make
    os.system(f"python {layout_py}")
    _print_always()
    interpret_build_music(part_directory)
    _print_always()
    front_cover_tex = part_directory / "front-cover.tex"
    interpret_tex_file(front_cover_tex)
    _print_always()
    preface_tex = part_directory / "preface.tex"
    interpret_tex_file(preface_tex)
    _print_always()
    back_cover_tex = part_directory / "back-cover.tex"
    interpret_tex_file(back_cover_tex)
    _print_always()
    part_tex = part_directory / "part.tex"
    interpret_tex_file(part_tex)


def build_score(score_directory):
    assert score_directory.name.endswith("-score"), repr(score_directory)
    assert score_directory.parent.name == "builds", repr(score_directory)
    _print_always("Building score ...")
    interpret_build_music(score_directory)
    _print_always()
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
            _print_file_handling()
        elif pdf.is_file():
            _print_file_handling(f"Using existing {baca.path.trim(pdf)} ...")
            _print_file_handling()
    score_tex = score_directory / "score.tex"
    interpret_tex_file(score_tex)
    score_pdf = score_directory / "score.pdf"
    if not score_pdf.is_file():
        _print_error(f"Can not find {baca.path.trim(score_pdf)} ...")
        sys.exit(1)


def collect_segment_lys(_segments_directory):
    _print_file_handling("Collecting segment lys ...")
    contents_directory = baca.path.get_contents_directory(_segments_directory)
    segments_directory = contents_directory / "segments"
    segment_lys = sorted(segments_directory.glob("**/music.ly"))
    if not segment_lys:
        _print_file_handling("Missing segment lys ...")
        sys.exit(1)
    if _segments_directory.exists():
        _print_file_handling(f"Removing {baca.path.trim(_segments_directory)} ...")
        shutil.rmtree(str(_segments_directory))
    _segments_directory.mkdir()
    targets = []
    for source_ly in segment_lys:
        text = _trim_music_ly(source_ly)
        segment_number = source_ly.parent.name
        target_ly = _segments_directory / f"{segment_number}.ly"
        targets.append(f"{target_ly.name}")
        target_ly.write_text(text)
        name = source_ly.name.removesuffix(".ly")
        name += ".ily"
        source_ily = source_ly.parent / name
        if source_ily.is_file():
            target_ily = target_ly.with_suffix(".ily")
            targets.append(f"{target_ily.name}")
            shutil.copyfile(str(source_ily), str(target_ily))
    targets = ", ".join(targets)
    message = f"Writing {baca.path.trim(_segments_directory)}/{targets} ..."
    _print_file_handling(message)
    handle_build_tags(_segments_directory)


def color_persistent_indicators(directory, *, undo=False):
    directory = pathlib.Path(directory)
    if directory.parent.name != "segments":
        _print_always("Must call in segment directory ...")
        sys.exit(1)
    for job in (
        baca.jobs.color_clefs,
        baca.jobs.color_dynamics,
        baca.jobs.color_instruments,
        baca.jobs.color_margin_markup,
        baca.jobs.color_metronome_marks,
        baca.jobs.color_persistent_indicators,
        baca.jobs.color_staff_lines,
        baca.jobs.color_time_signatures,
    ):
        job = job(directory, undo=undo)
        job = abjad.new(job, message_zero=True)
        for message in job():
            _print_tags(message)


def handle_build_tags(_segments_directory):
    _print_tags(f"Handling {baca.path.trim(_segments_directory)} build tags ...")
    contents_directory = baca.path.get_contents_directory(_segments_directory)
    segments_directory = contents_directory / "segments"
    paths = sorted(segments_directory.glob("*"))
    segment_directories = [_ for _ in paths if _.is_dir()]
    final_segment_directory_name = segment_directories[-1].name
    final_ily_name = f"{final_segment_directory_name}.ily"

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

    def match_phantom_should_activate(tags):
        if baca.tags.PHANTOM not in tags:
            return False
        if baca.tags.ONE_VOICE_COMMAND in tags:
            return True
        if baca.tags.SHOW_TO_JOIN_BROKEN_SPANNERS in tags:
            return True
        if baca.tags.SPANNER_STOP in tags:
            return True
        return False

    def match_phantom_should_deactivate(tags):
        if baca.tags.PHANTOM not in tags:
            return False
        if baca.tags.SPANNER_START in tags and baca.tags.LEFT_BROKEN in tags:
            return True
        if baca.tags.SPANNER_STOP in tags and baca.tags.RIGHT_BROKEN in tags:
            return True
        if baca.tags.HIDE_TO_JOIN_BROKEN_SPANNERS in tags:
            return True
        return False

    def _run(job, *, quiet=False):
        message_zero = not bool(quiet)
        job = abjad.new(job, message_zero=message_zero)
        messages = job()
        for message in messages:
            _print_tags(message)

    for job in (
        baca.jobs.handle_edition_tags(_segments_directory),
        baca.jobs.handle_fermata_bar_lines(_segments_directory),
        baca.jobs.handle_shifted_clefs(_segments_directory),
        baca.jobs.handle_mol_tags(_segments_directory),
        baca.jobs.color_persistent_indicators(_segments_directory, undo=True),
        baca.jobs.show_music_annotations(_segments_directory, undo=True),
        baca.jobs.join_broken_spanners(_segments_directory),
        baca.jobs.show_tag(
            _segments_directory,
            "left-broken-should-deactivate",
            match=match_left_broken_should_deactivate,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments_directory, baca.tags.PHANTOM, skip_file_name=final_ily_name
        ),
        baca.jobs.show_tag(
            _segments_directory,
            baca.tags.PHANTOM,
            prepend_empty_chord=True,
            skip_file_name=final_ily_name,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            "phantom-should-activate",
            match=match_phantom_should_activate,
            skip_file_name=final_ily_name,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            "phantom-should-deactivate",
            match=match_phantom_should_deactivate,
            skip_file_name=final_ily_name,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            baca.tags.EOS_STOP_MM_SPANNER,
            skip_file_name=final_ily_name,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            baca.tags.METRIC_MODULATION_IS_STRIPPED,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            baca.tags.METRIC_MODULATION_IS_SCALED,
            undo=True,
        ),
    ):
        _run(job, quiet=False)


def handle_part_tags(directory):
    directory = pathlib.Path(directory)
    if not directory.parent.name.endswith("-parts"):
        _print_always("Must call script in part directory ...")
        sys.exit(1)
    parts_directory = directory.parent
    _print_tags("Handling part tags ...")

    def _activate(
        path,
        tag,
        *,
        deactivate=False,
        message_zero=False,
        name=None,
    ):
        if isinstance(tag, str):
            tag_ = abjad.Tag(tag)
        else:
            assert callable(tag)
            tag_ = tag
        assert isinstance(tag_, abjad.Tag) or callable(tag_)
        if deactivate:
            result = baca.path.deactivate(
                path, tag_, message_zero=message_zero, name=name
            )
            assert result is not None
            count, skipped, messages = result
        else:
            result = baca.path.activate(
                path, tag_, message_zero=message_zero, name=name
            )
            assert result is not None
            count, skipped, messages = result
        for message in messages:
            _print_tags(message)

    def _deactivate(
        path,
        tag,
        *,
        message_zero=False,
        name=None,
    ):
        _activate(
            path,
            tag,
            name=name,
            deactivate=True,
            message_zero=message_zero,
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
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        "-PARTS",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        "HIDE_IN_PARTS",
        message_zero=True,
    )
    part_identifier = _parse_part_identifier(music_ly)
    if part_identifier is None:
        message = f"No part identifier found in {baca.path.trim(music_ly)} ..."
        _print_file_handling(message)
        sys.exit()
    parts_directory_name = abjad.String(parts_directory.name)
    parts_directory_name = parts_directory_name.to_shout_case()
    name = f"{parts_directory_name}_{part_identifier}"
    _activate(
        parts_directory,
        f"+{name}",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        f"-{name}",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.METRIC_MODULATION_IS_SCALED),
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.METRIC_MODULATION_IS_NOT_SCALED),
        message_zero=True,
    )
    _activate(
        parts_directory,
        str(baca.tags.METRIC_MODULATION_IS_STRIPPED),
        message_zero=True,
    )
    # HACK TO HIDE ALL POST-FERMATA-MEASURE TRANSPARENT BAR LINES;
    # this only works if parts contain no EOL fermata measure:
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE),
        message_zero=True,
    )
    _activate(
        parts_directory,
        str(baca.tags.NOT_TOPMOST),
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE_EMPTY_BAR_EXTENT),
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE_NEXT_BAR_EXTENT),
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.FERMATA_MEASURE_RESUME_BAR_EXTENT),
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.EXPLICIT_BAR_EXTENT),
        message_zero=True,
    )


def interpret_build_music(build_directory, *, skip_segment_collection=False):
    """
    Interprets music.ly file in build directory.

    Collects segments and handles tags.

    Skips segment collection when skip_segment_collection=True.
    """
    build_type = None
    if build_directory.name.endswith("-score"):
        build_type = "score"
    if build_directory.parent.name.endswith("-parts"):
        build_type = "part"
    if build_type is None:
        _print_always("Must call script in score directory or part directory ...")
        sys.exit(1)
    music_ly = build_directory / "music.ly"
    if not music_ly.is_file():
        raise Exception(f"Missing {baca.path.trim(music_ly)} ...")
    if build_type == "score":
        _segments_directory = build_directory / "_segments"
    else:
        assert build_type == "part"
        _segments_directory = build_directory.parent / "_segments"
    if skip_segment_collection:
        _print_file_handling("Skipping segment collection ...")
    else:
        collect_segment_lys(_segments_directory)
    if build_directory.parent.name.endswith("-parts"):
        if skip_segment_collection:
            _print_tags("Skipping tag handling ...")
        else:
            handle_part_tags(build_directory)
    _check_layout_time_signatures_in_build(music_ly)
    run_lilypond(music_ly)
    if _segments_directory.is_dir() and not __debug_segments:
        _print_file_handling(f"Removing {baca.path.trim(_segments_directory)} ...")
        shutil.rmtree(str(_segments_directory))


def interpret_segment(
    score,
    commands,
    *,
    first_segment=False,
    interpreter=None,
    midi=False,
    **keywords,
):
    if not any([__clicktrack, __midi, __pdf]):
        _print_always("Missing --clicktrack, --midi, --pdf ...")
        sys.exit(1)
    _print_main_task("Interpreting commands ...")
    interpreter = interpreter or baca.interpret.interpreter
    segment_directory = pathlib.Path(os.getcwd())
    metadata = baca.path.get_metadata(segment_directory)
    persist = baca.path.get_metadata(segment_directory, file_name="__persist__")
    previous_metadata, previous_persist = _get_previous_metadata(segment_directory)
    first_segment = first_segment or segment_directory.name == "01"
    with abjad.Timer() as timer:
        metadata, persist = interpreter(
            score,
            commands.commands,
            commands.time_signatures,
            append_phantom_measure=commands.append_phantom_measure,
            instruments=commands.instruments,
            margin_markups=commands.margin_markups,
            metronome_marks=commands.metronome_marks,
            skips_instead_of_rests=commands.skips_instead_of_rests,
            **keywords,
            first_segment=first_segment,
            metadata=metadata,
            midi=midi,
            persist=persist,
            previous_metadata=previous_metadata,
            previous_persist=previous_persist,
            segment_number=segment_directory.name,
        )
    _print_timing("Command interpretation time", timer)
    timing = types.SimpleNamespace()
    timing.runtime = int(timer.elapsed_time)
    return metadata, persist, score, timing


def interpret_tex_file(tex):
    if not tex.is_file():
        _print_tex(f"Can not find {baca.path.trim(tex)} ...")
        return
    pdf = tex.with_suffix(".pdf")
    if pdf.exists():
        _print_tex(f"Removing {baca.path.trim(pdf)} ...")
        pdf.unlink()
    _print_tex(f"Interpreting {baca.path.trim(tex)} ...")
    if not tex.is_file():
        return
    executables = abjad.io.find_executable("xelatex")
    executables = [pathlib.Path(_) for _ in executables]
    if not executables:
        executable_name = "pdflatex"
    else:
        executable_name = "xelatex"
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
    if pdf.is_file():
        _print_success(f"Found {baca.path.trim(pdf)} ...")
    else:
        _print_error(f"Can not produce {baca.path.trim(pdf)} ...")
        sys.exit(1)


def make_layout_ly(
    spacing, *, curtail_measure_count=None, do_not_append_phantom_measure=False
):
    current_directory = pathlib.Path(os.getcwd())
    if "segments" in str(current_directory):
        _print_main_task(f"Making layout for segment {current_directory.name} ...")
    else:
        _print_main_task(f"Making layout for {current_directory.name} ...")
    assert isinstance(spacing, baca.SpacingSpecifier), repr(spacing)
    layout_directory = pathlib.Path(os.getcwd())
    layout_py = layout_directory / "layout.py"
    layout_ly = layout_directory / "layout.ly"
    if spacing.overrides is not None:
        assert spacing.fallback_duration is not None
    if spacing.fallback_duration is None:
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
        for bol_measure_number in spacing.breaks.bol_measure_numbers[1:]:
            eol_measure_number = bol_measure_number - 1
            eol_measure_numbers.append(eol_measure_number)
    page_layout_profile = {
        "eol_measure_numbers": eol_measure_numbers,
        "fermata_measure_numbers": fermata_measure_numbers,
        "measure_count": measure_count,
    }
    document_name = abjad.String(layout_directory.name).to_shout_case()
    if layout_directory.parent.name == "segments":
        string = "first_measure_number"
        first_measure_number = baca.path.get_metadatum(
            layout_directory, string, default=1
        )
        if not bool(first_measure_number):
            _print_file_handling("Can not find first measure number ...")
            first_measure_number = False
        assert isinstance(first_measure_number, int)
        time_signatures = baca.path.get_metadatum(layout_directory, "time_signatures")
    else:
        first_measure_number = 1
        time_signatures = []
        contents_directory = baca.path.get_contents_directory(layout_directory)
        segments_directory = contents_directory / "segments"
        for segment_directory in sorted(segments_directory.glob("*")):
            if not segment_directory.is_dir():
                continue
            time_signatures_ = baca.path.get_metadatum(
                segment_directory,
                "time_signatures",
            )
            time_signatures.extend(time_signatures_)
    if first_measure_number is False:
        raise Exception("first_measure_number should not be false")
        _print_file_handling(f"Skipping {baca.path.trim(layout_py)} ...")
        sys.exit(1)
    assert abjad.String(document_name).is_shout_case()
    score = baca.docs.make_empty_score(1)
    commands = baca.CommandAccumulator(
        append_phantom_measure=not (do_not_append_phantom_measure),
        time_signatures=time_signatures,
    )
    _, _ = baca.interpreter(
        score,
        commands.commands,
        commands.time_signatures,
        append_phantom_measure=commands.append_phantom_measure,
        add_container_identifiers=True,
        comment_measure_numbers=True,
        first_measure_number=first_measure_number,
        first_segment=True,
        page_layout_profile=page_layout_profile,
        remove_tags=baca.tags.layout_removal_tags(),
        spacing=spacing,
        whitespace_leaves=True,
    )
    lilypond_file = baca.make_lilypond_file(score)
    context = lilypond_file["Global_Skips"]
    if curtail_measure_count is not None:
        del context[curtail_measure_count:]
    context.lilypond_type = "PageLayout"
    context.name = "Page_Layout"
    skips = baca.Selection(context).skips()
    for skip in skips:
        abjad.detach(abjad.TimeSignature, skip)
    score = lilypond_file["Score"]
    del score["Music_Context"]
    score = lilypond_file["Score"]
    text = abjad.lilypond(score, tags=True)
    text = text.replace("Global_Skips", "Page_Layout")
    text = text.replace("Global.Skips", "Page.Layout")
    text = abjad.lilypondformat.left_shift_tags(text)
    layout_ly = layout_directory / "layout.ly"
    lines = []
    # TODO: remove first_page_number embedding
    if layout_directory.parent.name == "segments":
        if layout_directory.name != "01":
            previous_segment_number = str(int(layout_directory.name) - 1).zfill(2)
            previous_segment_directory = (
                layout_directory.parent / previous_segment_number
            )
            previous_layout_ly = previous_segment_directory / "layout.ly"
            if previous_layout_ly.is_file():
                result = _get_preamble_page_count_overview(previous_layout_ly)
                if result is not None:
                    _, _, final_page_number = result
                    first_page_number = final_page_number + 1
                    line = f"% first_page_number = {first_page_number}"
                    lines.append(line)
    page_count = spacing.breaks.page_count
    lines.append(f"% page_count = {page_count}")
    time_signatures = [str(_) for _ in time_signatures]
    measure_count = len(time_signatures)
    lines.append(f"% measure_count = {measure_count} + 1")
    string = pprint.pformat(time_signatures, compact=True, width=80 - 3)
    lines_ = string.split("\n")
    lines_ = [_.strip("[").strip("]") for _ in lines_]
    lines_ = ["% " + _ for _ in lines_]
    lines_.insert(0, "% time_signatures = [")
    lines_.append("%  ]")
    lines.extend(lines_)
    header = "\n".join(lines) + "\n\n"
    layout_ly.write_text(header + text + "\n")
    counter = abjad.String("measure").pluralize(measure_count)
    message = f"Writing {measure_count} + 1 {counter} to"
    message += f" {baca.path.trim(layout_ly)} ..."
    _print_file_handling(message)
    bol_measure_numbers = []
    skips = abjad.iterate.leaves(score["Page_Layout"], abjad.Skip)
    for i, skip in enumerate(skips):
        for literal in abjad.get.indicators(skip, abjad.LilyPondLiteral):
            if literal.argument in (r"\break", r"\pageBreak"):
                measure_number = first_measure_number + i
                bol_measure_numbers.append(measure_number)
                continue
    count = len(bol_measure_numbers)
    numbers = abjad.String("number").pluralize(count)
    items = ", ".join([str(_) for _ in bol_measure_numbers])
    metadata = layout_directory / "__metadata__"
    message = f"Writing BOL measure {numbers} {items} to {baca.path.trim(metadata)} ..."
    _print_file_handling(message)
    if layout_directory.name.endswith("-parts"):
        if document_name is not None:
            part_dictionary = baca.path.get_metadatum(
                layout_directory,
                document_name,
                {},
            )
        else:
            part_dictionary = {}
        part_dictionary["bol_measure_numbers"] = bol_measure_numbers
        assert abjad.String(document_name).is_shout_case()
        baca.path.add_metadatum(layout_directory, document_name, part_dictionary)
    else:
        baca.path.add_metadatum(
            layout_directory,
            "bol_measure_numbers",
            bol_measure_numbers,
        )


def make_segment_pdf(lilypond_file, metadata, persist, timing):
    if __clicktrack:
        _make_segment_clicktrack(lilypond_file)
    if __midi:
        _make_segment_midi(lilypond_file)
    if __pdf:
        _make_segment_pdf(lilypond_file, metadata, persist, timing)


def run_lilypond(ly_file_path):
    assert ly_file_path.exists(), repr(ly_file_path)
    string = f"Calling LilyPond (with includes) on {baca.path.trim(ly_file_path)} ..."
    _print_file_handling(string)
    directory = ly_file_path.parent
    pdf = ly_file_path.with_suffix(".pdf")
    lilypond_log_file_name = "." + ly_file_path.name + ".log"
    lilypond_log_file_path = directory / lilypond_log_file_name
    with abjad.TemporaryDirectoryChange(directory=directory):
        flags = _get_lilypond_include_string()
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
        if pdf.is_file():
            _print_success(f"Found {baca.path.trim(pdf)} ...")
        else:
            _print_error(f"Can not find {baca.path.trim(pdf)} ...")
        assert lilypond_log_file_path.exists()


def show_annotations(directory, *, undo=False):
    directory = pathlib.Path(directory)
    if directory.parent.name != "segments":
        _print_always("Must call in segment directory ...")
        sys.exit(1)
    for job in _make_annotation_jobs(directory, undo=undo):
        job = abjad.new(job, message_zero=True)
        for message in job():
            _print_tags(message)


def show_tag(directory, tag, *, undo=False):
    directory = pathlib.Path(directory)
    tag = abjad.Tag(tag)
    job = baca.jobs.show_tag(directory, tag, undo=undo)
    job = abjad.new(job, message_zero=True)
    for message in job():
        _print_tags(message)
