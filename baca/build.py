import os
import pathlib
import pprint
import shutil
import sys
import time

import abjad
import baca


def _check_layout_time_signatures(music_ly):
    print("Checking layout time signatures ...")
    build_directory = music_ly.parent
    layout_ly_file_path = build_directory / "layout.ly"
    if not layout_ly_file_path.is_file():
        print(f"No {baca.path.trim(layout_ly_file_path)} found ...")
        return
    print(f"Found {baca.path.trim(layout_ly_file_path)} ...")
    partial_score = _get_preamble_partial_score(layout_ly_file_path)
    if partial_score:
        print(f"Found {baca.path.trim(layout_ly_file_path)} partial score comment ...")
        print("Aborting layout time signature check ...")
        return
    metadata_time_signatures = []
    segments_directory = build_directory / "segments"
    for segment_directory in sorted(segments_directory.glob("*")):
        time_signatures = baca.path.get_metadatum(segment_directory, "time_signatures")
        metadata_time_signatures.extend(time_signatures)
    if metadata_time_signatures:
        print("Found time signature metadata ...")
    layout_time_signatures = _get_preamble_time_signatures(layout_ly_file_path)
    if layout_time_signatures == metadata_time_signatures:
        message = "Layout time signatures"
        message += f" ({len(layout_time_signatures)})"
        message += " match metadata time signatures"
        message += f" ({len(metadata_time_signatures)}) ..."
        print(message)
        return
    message = "Layout time signatures"
    message += f" ({len(layout_time_signatures)})"
    message += " do not match metadata time signatures"
    message += f" ({len(metadata_time_signatures)}) ..."
    print(message)
    print(f"Remaking {baca.path.trim(layout_ly_file_path)} ...")
    layout_py = layout_ly_file_path.with_suffix(".py")
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
    print(message)


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
            print("ERROR IN LILYPOND LOG FILE ...")
            error = True
            break
    if error:
        for line in lines[:10]:
            print(line)


def _get_preamble_page_count_overview(path):
    """
    Gets preamble page count overview.
    """
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


def _get_preamble_partial_score(path):
    """
    Gets preamble time signatures.
    """
    assert path.is_file(), repr(path)
    prefix = "% partial_score ="
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith(prefix):
                line = line[len(prefix) :]
                partial_score = eval(line)
                return partial_score
    return False


def _get_preamble_time_signatures(path):
    """
    Gets preamble time signatures.
    """
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


def _make_annotation_jobs(directory, undo=False):
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


def _make_segment_clicktrack(maker):
    segment_directory = pathlib.Path(os.getcwd())
    print(f"Making clicktrack for segment {segment_directory.name} ...")
    result = _run_segment_maker(maker, midi=True)
    metadata, persist, lilypond_file, runtime = result
    print("Configuring LilyPond file ...")
    time_signatures = maker.time_signatures
    global_skips = lilypond_file["Global_Skips"]
    skips = abjad.select(global_skips).leaves()[:-1]
    metronome_marks = []
    for skip in skips:
        metronome_mark = abjad.get.effective(skip, abjad.MetronomeMark)
        metronome_marks.append(metronome_mark)
    staff = abjad.Staff()
    abjad.setting(staff).midiInstrument = '#"drums"'
    score = abjad.Score([staff], simultaneous=False)
    fermata_measure_numbers = maker.fermata_measure_empty_overrides or []
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
                note = abjad.Note.from_pitch_and_duration(-18, (1, denominator))
                notes.append(note)
            notes[0].written_pitch = -23
        abjad.attach(time_signature, notes[0])
        abjad.attach(metronome_mark, notes[0])
        measure = abjad.Container(notes)
        staff.append(measure)
    score_block = abjad.Block(name="score")
    score_block.items.append(score)
    midi_block = abjad.Block(name="midi")
    score_block.items.append(midi_block)
    lilypond_file = abjad.LilyPondFile(items=[score_block])
    clicktrack_file_name = "clicktrack.midi"
    print("Persisting LilyPond file ...")
    with abjad.Timer() as timer:
        abjad.persist.as_midi(lilypond_file, clicktrack_file_name, remove_ly=True)
    count = int(timer.elapsed_time)
    counter = abjad.String("second").pluralize(count)
    print(f"LilyPond runtime {count} {counter} ...")
    clicktrack_path = segment_directory / clicktrack_file_name
    if clicktrack_path.is_file():
        print(f"Found {baca.path.trim(clicktrack_path)} ...")
    else:
        print(f"Could not make {baca.path.trim(clicktrack_path)} ...")


def _make_segment_midi(maker):
    segment_directory = pathlib.Path(os.getcwd())
    print(f"Making MIDI for segment {segment_directory.name} ...")
    music_midi = segment_directory / "music.midi"
    if music_midi.exists():
        print(f"Removing {baca.path.trim(music_midi)} ...")
        music_midi.unlink()
    result = _run_segment_maker(maker, midi=True)
    metadata, persist, lilypond_file, runtime = result
    with abjad.Timer() as timer:
        tmp_midi = segment_directory / "tmp.midi"
        abjad.persist.as_midi(lilypond_file, tmp_midi)
        if tmp_midi.is_file():
            shutil.move(tmp_midi, music_midi)
        tmp_ly = tmp_midi.with_suffix(".ly")
        if tmp_ly.exists():
            tmp_ly.unlink()
    count = int(timer.elapsed_time)
    counter = abjad.String("second").pluralize(count)
    print(f"LilyPond runtime {count} {counter} ...")
    if music_midi.is_file():
        print(f"Found {baca.path.trim(music_midi)} ...")
    else:
        print(f"Could not produce {baca.path.trim(music_midi)} ...")


def _remove_lilypond_warnings(
    path,
    crescendo_too_small=None,
    decrescendo_too_small=None,
    overwriting_glissando=None,
):
    """
    Removes LilyPond warnings from ``.log``.
    """
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


def _run_segment_maker(maker, first_segment=False, midi=False):
    segment_directory = pathlib.Path(os.getcwd())
    metadata = baca.path.get_metadata(segment_directory)
    persist = baca.path.get_metadata(segment_directory, file_name="__persist__")
    if not midi:
        ly = segment_directory / "music.ly.tagged"
        if ly.exists():
            print(f"Removing {baca.path.trim(ly)} ...")
            ly.unlink()
        pdf = segment_directory / "music.pdf"
        if pdf.exists():
            print(f"Removing {baca.path.trim(pdf)} ...")
            pdf.unlink()
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
    if first_segment is True:
        pass
    else:
        first_segment = segment_directory.name == "01"
    with abjad.Timer() as timer:
        lilypond_file = maker.run(
            first_segment=first_segment,
            metadata=metadata,
            midi=midi,
            persist=persist,
            previous_metadata=previous_metadata,
            previous_persist=previous_persist,
            segment_name=segment_directory.name,
        )
    segment_maker_runtime = int(timer.elapsed_time)
    count = segment_maker_runtime
    counter = abjad.String("second").pluralize(count)
    print(f"Segment-maker runtime {count} {counter} ...")
    runtime = (count, counter)
    return metadata, persist, lilypond_file, runtime


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


def build_part(part_directory):
    assert part_directory.parent.name.endswith("-parts"), repr(part_directory)
    part_pdf = part_directory / "part.pdf"
    print(f"Building {baca.path.trim(part_pdf)} ...")
    layout_py = part_directory / "layout.py"
    os.system(f"python {layout_py}")
    print()
    interpret_build_music(part_directory)
    print()
    front_cover_tex = part_directory / "front-cover.tex"
    interpret_tex_file(front_cover_tex)
    print()
    preface_tex = part_directory / "preface.tex"
    interpret_tex_file(preface_tex)
    print()
    back_cover_tex = part_directory / "back-cover.tex"
    interpret_tex_file(back_cover_tex)
    print()
    part_tex = part_directory / "part.tex"
    interpret_tex_file(part_tex)


def build_score(score_directory):
    assert score_directory.name.endswith("-score"), repr(score_directory)
    assert score_directory.parent.name == "builds", repr(score_directory)
    print("Building score ...")
    interpret_build_music(score_directory)
    print()
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
            print()
        elif pdf.is_file():
            print(f"Using existing {baca.path.trim(pdf)} ...")
            print()
    score_tex = score_directory / "score.tex"
    interpret_tex_file(score_tex)
    score_pdf = score_directory / "score.pdf"
    if not score_pdf.is_file():
        print(f"Could not produce {baca.path.trim(score_pdf)} ...")
        sys.exit(1)


def collect_segment_lys(_segments_directory):
    assert _segments_directory.name == "_segments", repr(_segments_directory)
    contents_directory = baca.path.get_contents_directory(_segments_directory)
    segments_directory = contents_directory / "segments"
    paths = sorted(segments_directory.glob("*"))
    names = [_.name for _ in paths]
    sources, targets = [], []
    for name in names:
        source = segments_directory / name / "music.ly"
        if not source.is_file():
            continue
        target = name + ".ly"
        target = _segments_directory / target
        sources.append(source)
        targets.append(target)
    return zip(sources, targets)


def collect_segment_lys_CLEAN(directory):
    contents_directory = baca.path.get_contents_directory(directory)
    segments_directory = contents_directory / "segments"
    paths = sorted(segments_directory.glob("**/music.ly.tagged"))
    return paths


def color_persistent_indicators(directory, undo=False):
    directory = pathlib.Path(directory)
    if directory.parent.name != "segments":
        print("Must call in segment directory ...")
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
        messages = job()
        for message in messages:
            print(message)


def handle_build_tags(_segments_directory):
    print(f"Handling {baca.path.trim(_segments_directory)} build tags ...")
    pairs = baca.build.collect_segment_lys(_segments_directory)
    final_source, final_target = list(pairs)[-1]
    final_file_name = final_target.with_suffix(".ily").name

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
            print(message)

    for job in [
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
            _segments_directory, baca.tags.PHANTOM, skip_file_name=final_file_name
        ),
        baca.jobs.show_tag(
            _segments_directory,
            baca.tags.PHANTOM,
            prepend_empty_chord=True,
            skip_file_name=final_file_name,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            "phantom-should-activate",
            match=match_phantom_should_activate,
            skip_file_name=final_file_name,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            "phantom-should-deactivate",
            match=match_phantom_should_deactivate,
            skip_file_name=final_file_name,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments_directory,
            baca.tags.EOS_STOP_MM_SPANNER,
            skip_file_name=final_file_name,
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
    ]:
        _run(job, quiet=False)


def handle_part_tags(directory):
    directory = pathlib.Path(directory)
    if not directory.parent.name.endswith("-parts"):
        print("Must call script in part directory ...")
        sys.exit(1)
    parts_directory = directory.parent
    print("Handling part tags ...")

    def _activate(
        path,
        tag,
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
            print(message)

    def _deactivate(
        path,
        tag,
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
        print(f"No part identifier found in {baca.path.trim(music_ly)} ...")
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
        "NOT_TOPMOST",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        "FERMATA_MEASURE_EMPTY_BAR_EXTENT",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        "FERMATA_MEASURE_NEXT_BAR_EXTENT",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        "FERMATA_MEASURE_RESUME_BAR_EXTENT",
        message_zero=True,
    )
    _deactivate(
        parts_directory,
        str(baca.tags.EXPLICIT_BAR_EXTENT),
        message_zero=True,
    )


def interpret_build_music(build_directory, skip_segment_collection=False):
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
        print("Must call script in score directory or part directory ...")
        sys.exit(1)
    music_ly = build_directory / "music.ly"
    if build_type == "score":
        _segments_directory = build_directory / "_segments"
    else:
        assert build_type == "part"
        _segments_directory = build_directory.parent / "_segments"
    if skip_segment_collection:
        print("Skipping segment collection ...")
    else:
        print("Collecting segment lys ...")
        segment_lys = collect_segment_lys_CLEAN(build_directory)
        if not segment_lys:
            print("Missing segment lys ...")
            sys.exit(1)
        if _segments_directory.exists():
            print(f"Removing {baca.path.trim(_segments_directory)} ...")
            shutil.rmtree(str(_segments_directory))
        _segments_directory.mkdir()
        print(f"Writing {baca.path.trim(_segments_directory)}/", end="")
        for source_ly in segment_lys:
            text = _trim_music_ly(source_ly)
            segment_number = source_ly.parent.name
            target_ly = _segments_directory / f"{segment_number}.ly"
            print(f"{target_ly.name}", end=", ")
            target_ly.write_text(text)
            name = source_ly.name.removesuffix(".tagged").removesuffix(".ly")
            name += ".ily.tagged"
            source_ily = source_ly.parent / name
            if source_ily.is_file():
                target_ily = target_ly.with_suffix(".ily")
                print(f"{target_ily.name}", end=", ")
                shutil.copyfile(str(source_ily), str(target_ily))
        print("...")
        handle_build_tags(_segments_directory)
    if build_directory.parent.name.endswith("-parts"):
        if skip_segment_collection:
            print("Skipping tag handling ...")
        else:
            handle_part_tags(build_directory)
    _check_layout_time_signatures(music_ly)
    run_lilypond(music_ly)
    if _segments_directory.is_dir():
        print(f"Removing {baca.path.trim(_segments_directory)} ...")
        shutil.rmtree(str(_segments_directory))


def interpret_tex_file(tex, open_after=False):
    if not tex.is_file():
        print(f"Can not find {baca.path.trim(tex)} ...")
        return
    pdf = tex.with_suffix(".pdf")
    if pdf.exists():
        print(f"Removing {baca.path.trim(pdf)} ...")
        pdf.unlink()
    print(f"Interpreting {baca.path.trim(tex)} ...")
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
        print(f"Logging to {baca.path.trim(target)} ...")
        for path in sorted(tex.parent.glob("*.aux")):
            path.unlink()
    if pdf.is_file():
        print(f"Found {baca.path.trim(pdf)} ...")
        if open_after:
            os.system(f"open {pdf}")
    else:
        print(f"Can not produce {baca.path.trim(pdf)} ...")
        sys.exit(1)


def make_layout_ly(layout_py, breaks, spacing=None, *, part_identifier=None):
    layout_py = pathlib.Path(layout_py)
    layout_module_name = layout_py.stem
    assert layout_module_name == "layout", repr(layout_module_name)
    layout_directory = layout_py.parent
    document_name = abjad.String(layout_directory.name).to_shout_case()
    if baca.path.get_metadatum(layout_directory, "parts_directory") is True:
        assert abjad.String(part_identifier).is_shout_case()
        document_name = f"{document_name}_{part_identifier}"
    if layout_directory.parent.name == "segments":
        string = "first_measure_number"
        first_measure_number = baca.path.get_metadatum(layout_directory, string)
        if not bool(first_measure_number):
            print("Can not find first measure number ...")
            first_measure_number = False
        assert isinstance(first_measure_number, int)
    else:
        first_measure_number = 1
    if first_measure_number is False:
        print(f"Skipping {baca.path.trim(layout_py)} ...")
        sys.exit(1)
    assert abjad.String(document_name).is_shout_case()
    string = "first_measure_number"
    first_measure_number = baca.path.get_metadatum(layout_directory, string, 1)
    if layout_directory.parent.name == "segments":
        time_signatures = baca.path.get_metadatum(layout_directory, "time_signatures")
    else:
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
    if breaks.partial_score is not None:
        time_signatures = time_signatures[: breaks.partial_score]
    maker = baca.SegmentMaker(
        breaks=breaks,
        do_not_check_persistence=True,
        do_not_include_layout_ly=True,
        first_measure_number=first_measure_number,
        remove=baca.tags.layout_removal_tags(),
        score_template=baca.SingleStaffScoreTemplate(),
        spacing=spacing,
        time_signatures=time_signatures,
    )
    # TODO: remove segment_name here because it's never necessary
    if layout_directory.parent.name == "segments":
        segment_name = layout_directory.name
    else:
        segment_name = None
    lilypond_file = maker.run(
        do_not_print_timing=True,
        environment="layout",
        first_segment=True,
        segment_name=segment_name,
    )
    context = lilypond_file["Global_Skips"]
    context.lilypond_type = "PageLayout"
    context.name = "Page_Layout"
    skips = baca.select(context).skips()
    for skip in skips:
        abjad.detach(abjad.TimeSignature, skip)
    score = lilypond_file["Score"]
    del score["Music_Context"]
    score = lilypond_file["Score"]
    text = abjad.lilypond(score, tags=True)
    text = text.replace("Global_Skips", "Page_Layout")
    text = abjad.LilyPondFormatManager.left_shift_tags(text)
    layout_ly_tagged = layout_directory / "layout.ly.tagged"
    lines = []
    if breaks.partial_score is not None:
        lines.append("% partial_score = True")
    if layout_directory.parent.name == "segments":
        first_segment = layout_directory.parent / "01"
        if layout_directory.name != first_segment.name:
            previous_segment = str(int(layout_directory.name) - 1).zfill(2)
            previous_segment = layout_directory.parent / previous_segment
            previous_layout_ly = previous_segment / "layout.ly.tagged"
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
    lines.append(f"% measure_count = {measure_count} + 1")
    string = pprint.pformat(time_signatures, compact=True, width=80 - 3)
    lines_ = string.split("\n")
    lines_ = [_.strip("[").strip("]") for _ in lines_]
    lines_ = ["% " + _ for _ in lines_]
    lines_.insert(0, "% time_signatures = [")
    lines_.append("%  ]")
    lines.extend(lines_)
    header = "\n".join(lines) + "\n\n"
    layout_ly_tagged.write_text(header + text + "\n")
    counter = abjad.String("measure").pluralize(measure_count)
    print(
        f"Writing {measure_count} + 1 {counter} to"
        f" {baca.path.trim(layout_ly_tagged)} ..."
    )
    bol_measure_numbers = []
    prototype = abjad.LilyPondLiteral
    skips = abjad.iterate(score["Page_Layout"]).leaves(abjad.Skip)
    for i, skip in enumerate(skips):
        for literal in abjad.get.indicators(skip, prototype):
            if literal.argument in (r"\break", r"\pageBreak"):
                measure_number = first_measure_number + i
                bol_measure_numbers.append(measure_number)
                continue
    bols = bol_measure_numbers
    count = len(bols)
    numbers = abjad.String("number").pluralize(count)
    items = ", ".join([str(_) for _ in bols])
    metadata = layout_directory / "__metadata__"
    print(f"Writing BOL measure {numbers} {items} to {baca.path.trim(metadata)} ...")
    if layout_directory.name.endswith("-parts"):
        if document_name is not None:
            part_dictionary = baca.path.get_metadatum(
                layout_directory,
                document_name,
                abjad.OrderedDict(),
            )
        else:
            part_dictionary = abjad.OrderedDict()
        part_dictionary["bol_measure_numbers"] = bol_measure_numbers
        assert abjad.String(document_name).is_shout_case()
        baca.path.add_metadatum(layout_directory, document_name, part_dictionary)
    else:
        baca.path.add_metadatum(
            layout_directory,
            "bol_measure_numbers",
            bol_measure_numbers,
        )


def make_segment_pdf(maker, first_segment=False):
    if "--clicktrack" in sys.argv:
        _make_segment_clicktrack(maker)
        return
    if "--midi" in sys.argv:
        _make_segment_midi(maker)
        return
    segment_directory = pathlib.Path(os.getcwd())
    timing = "--timing" in sys.argv[1:]
    layout_py = segment_directory / "layout.py"
    if "--no-layout" not in sys.argv[1:] and layout_py.is_file():
        os.system(f"python {layout_py}")
    result = _run_segment_maker(maker, first_segment=first_segment)
    metadata, persist, lilypond_file, runtime = result
    metadata_file = segment_directory / "__metadata__"
    print(f"Writing {baca.path.trim(metadata_file)} ...")
    baca.path.write_metadata_py(segment_directory, maker.metadata)
    os.system("black --target-version=py38 __metadata__ 1>/dev/null 2>&1")
    persist_file = segment_directory / "__persist__"
    print(f"Writing {baca.path.trim(persist_file)} ...")
    baca.path.write_metadata_py(
        segment_directory,
        maker.persist,
        file_name="__persist__",
        variable_name="persist",
    )
    os.system("black --target-version=py38 __persist__ 1>/dev/null 2>&1")
    first_segment = segment_directory.parent / "01"
    layout_ly_tagged = segment_directory / "layout.ly.tagged"
    if layout_ly_tagged.is_file() and segment_directory.name != first_segment.name:
        result = _get_preamble_page_count_overview(layout_ly_tagged)
        if result is not None:
            first_page_number, _, _ = result
            line = r"\paper { first-page-number = #"
            line += str(first_page_number)
            line += " }"
            lines = abjad.tag.double_tag([line], "__make_segment_pdf__")
            lines.append("")
            lilypond_file.items[-1:-1] = lines
    music_ly_tagged = segment_directory / "music.ly.tagged"
    result = abjad.persist.as_ly(lilypond_file, music_ly_tagged)
    abjad_format_time = int(result[1])
    count = abjad_format_time
    counter = abjad.String("second").pluralize(count)
    print(f"Abjad format time {count} {counter} ...")
    abjad_format_time = (count, counter)
    if "Global_Skips" in lilypond_file:
        context = lilypond_file["Global_Skips"]
        measure_count = len(context)
        counter = abjad.String("measure").pluralize(measure_count)
        message = f"Wrote {measure_count} {counter}"
        message += f" to {baca.path.trim(music_ly_tagged)} ..."
        print(message)
        time_signatures = []
        prototype = abjad.TimeSignature
        for skip in context:
            time_signature = abjad.get.effective(skip, prototype)
            assert isinstance(time_signature, prototype), repr(time_signature)
            time_signatures.append(str(time_signature))
        # for phantom measure at end
        if 0 < len(time_signatures):
            time_signatures.pop()
    else:
        measure_count = None
        time_signatures = None
    text = music_ly_tagged.read_text()
    text = abjad.LilyPondFormatManager.left_shift_tags(text)
    music_ly_tagged.write_text(text)
    for job in [
        baca.jobs.handle_edition_tags(music_ly_tagged),
        baca.jobs.handle_fermata_bar_lines(segment_directory),
        baca.jobs.handle_shifted_clefs(segment_directory),
        baca.jobs.handle_mol_tags(segment_directory),
    ]:
        for message in job():
            print(message)
    layout_py = segment_directory / "layout.py"
    if not layout_py.exists():
        print(f"No {baca.path.trim(layout_py)} found ...")
    else:
        layout_ly_tagged = segment_directory / "layout.ly.tagged"
        layout_time_signatures = _get_preamble_time_signatures(layout_ly_tagged)
        if layout_time_signatures is not None:
            assert isinstance(layout_time_signatures, list)
            layout_measure_count = len(layout_time_signatures)
            counter = abjad.String("measure").pluralize(layout_measure_count)
            message = f"Found {layout_measure_count} {counter}"
            message += f" in {baca.path.trim(layout_ly_tagged)} ..."
            print(message)
            if layout_time_signatures == time_signatures:
                print("Music time signatures match layout time signatures ...")
            else:
                print("Music time signatures do not match layout time signatures ...")
                print(f"Remaking {baca.path.trim(layout_ly_tagged)} ...")
                os.system(f"python {layout_py}")
                counter = abjad.String("measure").pluralize(measure_count)
                message = f"Found {measure_count} {counter}"
                message += f" in {baca.path.trim(music_ly_tagged)} ..."
                print(message)
                layout_time_signatures = _get_preamble_time_signatures(layout_ly_tagged)
                layout_measure_count = len(layout_time_signatures)
                counter = abjad.String("measure").pluralize(layout_measure_count)
                message = f"Found {layout_measure_count} {counter}"
                message += f" in {baca.path.trim(layout_ly_tagged)} ..."
                print(message)
                if layout_time_signatures != time_signatures:
                    message = "Music time signatures still do not match"
                    message += " layout time signatures ..."
                    print(message)
    if getattr(maker, "do_not_externalize", False) is not True:
        music_ily_tagged = segment_directory / "music.ily.tagged"
        baca.path.extern(music_ly_tagged, music_ily_tagged)
        assert music_ily_tagged.is_file()
        not_topmost = baca.jobs.Job(
            deactivate=(abjad.Tag("NOT_TOPMOST"), "not topmost"),
            path=segment_directory,
            title="deactivating NOT_TOPMOST ...",
        )
        for message in not_topmost():
            print(message)
    if "--no-pdf" not in sys.argv:
        log_file_name = "." + music_ly_tagged.name + ".log"
        lilypond_log_file_path = music_ly_tagged.parent / log_file_name
        with abjad.Timer() as timer:
            print(f"Calling LilyPond on {baca.path.trim(music_ly_tagged)} ...")
            baca_repo_path = pathlib.Path(baca.__file__).parent.parent
            flags = f"--include={baca_repo_path}/lilypond"
            abjad_repo_path = pathlib.Path(abjad.__file__).parent.parent
            flags += f" --include={abjad_repo_path}/docs/source/_stylesheets"
            abjad.io.run_lilypond(
                music_ly_tagged,
                flags=flags,
                lilypond_log_file_path=lilypond_log_file_path,
            )
            music_ly_pdf = segment_directory / "music.ly.pdf"
            if music_ly_pdf.is_file():
                music_pdf = segment_directory / "music.pdf"
                shutil.move(str(music_ly_pdf), str(music_pdf))
        _remove_lilypond_warnings(
            lilypond_log_file_path,
            crescendo_too_small=True,
            decrescendo_too_small=True,
            overwriting_glissando=True,
        )
        lilypond_runtime = int(timer.elapsed_time)
        count = lilypond_runtime
        counter = abjad.String("second").pluralize(count)
        print(f"LilyPond runtime {count} {counter} ...")
        lilypond_runtime = (count, counter)
    for name in ["music.ly.tagged", "music.ily.tagged", "layout.ly.tagged"]:
        tagged = segment_directory / name
        if not tagged.exists():
            continue
        with tagged.open() as pointer:
            lines = []
            for line in pointer.readlines():
                if "%@%" not in line:
                    lines.append(line)
        string = "".join(lines)
        string = abjad.format.remove_tags(string)
        untagged = segment_directory / name.removesuffix(".tagged")
        untagged.write_text(string)
    if "--timing" in sys.argv and "--no-pdf" not in sys.argv:
        timing = segment_directory / ".timing"
        with timing.open(mode="a") as pointer:
            print(f"Writing timing to {baca.path.trim(timing)} ...")
            pointer.write("\n")
            line = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
            pointer.write(line)
            count, counter = runtime
            line = f"Segment-maker runtime: {count} {counter}\n"
            pointer.write(line)
            count, counter = abjad_format_time
            line = f"Abjad format time: {count} {counter}\n"
            pointer.write(line)
            count, counter = lilypond_runtime
            line = f"LilyPond runtime: {count} {counter}\n"
            pointer.write(line)
    if music_ly_tagged.is_file():
        print(f"Found {baca.path.trim(music_ly_tagged)} ...")
    music_pdf = segment_directory / "music.pdf"
    if "--no-pdf" not in sys.argv and music_pdf.is_file():
        print(f"Found {baca.path.trim(music_pdf)} ...")


def run_lilypond(ly_file_path):
    assert ly_file_path.exists()
    if not abjad.io.find_executable("lilypond"):
        raise ValueError("cannot find LilyPond executable.")
    print(f"Running LilyPond on {baca.path.trim(ly_file_path)} ...")
    directory = ly_file_path.parent
    pdf = ly_file_path.with_suffix(".pdf")
    backup_pdf = ly_file_path.with_suffix("._backup.pdf")
    lilypond_log_file_name = "." + ly_file_path.name + ".log"
    lilypond_log_file_path = directory / lilypond_log_file_name
    if backup_pdf.exists():
        backup_pdf.unlink()
    if pdf.exists():
        print(f"Removing {baca.path.trim(pdf)} ...")
        pdf.unlink()
    assert not pdf.exists()
    with abjad.TemporaryDirectoryChange(directory=directory):
        print(f"Interpreting {baca.path.trim(ly_file_path)} ...")
        print(f"Logging to {baca.path.trim(lilypond_log_file_path)} ...")
        abjad_repo = pathlib.Path(abjad.__file__).parent.parent
        baca_repo = pathlib.Path(baca.__file__).parent.parent
        flags = f"--include={abjad_repo}/docs/source/_stylesheets"
        flags += f" --include={baca_repo}/lilypond"
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
            print(f"Found {baca.path.trim(pdf)} ...")
        else:
            print(f"Can not produce {baca.path.trim(pdf)} ...")
        assert lilypond_log_file_path.exists()


def show_annotations(directory, undo=False):
    directory = pathlib.Path(directory)
    if directory.parent.name != "segments":
        print("Must call in segment directory ...")
        sys.exit(1)
    for job in _make_annotation_jobs(directory, undo=undo):
        job = abjad.new(job, message_zero=True)
        messages = job()
        for message in messages:
            print(message)


def show_tag(directory, tag, undo=False):
    directory = pathlib.Path(directory)
    tag = abjad.Tag(tag)
    job = baca.jobs.show_tag(directory, tag, undo=undo)
    job = abjad.new(job, message_zero=True)
    for message in job():
        print(message)
