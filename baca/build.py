import importlib
import os
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
        print(f"No {layout_ly_file_path.trim()} found ...")
        return
    print(f"Found {layout_ly_file_path.trim()} ...")
    partial_score = baca.segments.get_preamble_partial_score(layout_ly_file_path)
    if partial_score:
        print(f"Found {layout_ly_file_path.trim()} partial score comment ...")
        print("Aborting layout time signature check ...")
        return
    metadata_time_signatures = []
    segments_directory = build_directory / "segments"
    for segment_directory in sorted(segments_directory.glob("*")):
        time_signatures = segment_directory.get_metadatum("time_signatures")
        metadata_time_signatures.extend(time_signatures)
    if metadata_time_signatures:
        print("Found time signature metadata ...")
    layout_time_signatures = baca.segments.get_preamble_time_signatures(
        layout_ly_file_path
    )
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
    print(f"Remaking {layout_ly_file_path.trim()} ...")
    layout_py = layout_ly_file_path.with_suffix(".py")
    os.system(f"make-layout-ly {layout_py}")
    layout_time_signatures = baca.segments.get_preamble_time_signatures(
        layout_ly_file_path
    )
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
    lilypond_log_file_path = baca.Path(lilypond_log_file_path)
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


def _import_definition_and_run_segment_maker(segment_directory, midi=False):
    assert segment_directory.parent.name == "segments", repr(segment_directory)
    definition = segment_directory / "definition.py"
    if not definition.is_file():
        raise Exception(f"Can not find {definition.trim()} ...")
    if str(segment_directory) not in sys.path:
        sys.path.append(str(segment_directory))
    definition = importlib.import_module("definition")
    metadata = segment_directory.get_metadata()
    persist = segment_directory.get_metadata(file_name="__persist__")
    if not midi:
        ly = segment_directory / "illustration.ly"
        if ly.exists():
            print(f"Removing {ly.trim()} ...")
            ly.unlink()
        pdf = segment_directory / "illustration.pdf"
        if pdf.exists():
            print(f"Removing {pdf.trim()} ...")
            pdf.unlink()
    if segment_directory.name == "01":
        previous_metadata = None
        previous_persist = None
    else:
        previous_segment = str(int(segment_directory.name) - 1).zfill(2)
        previous_segment = segment_directory.parent / previous_segment
        path = previous_segment / "__metadata__"
        file = baca.Path(path)
        if file.is_file():
            string = file.read_text()
            previous_metadata = eval(string)
        else:
            previous_metadata = None
        path = previous_segment / "__persist__"
        file = baca.Path(path)
        if file.is_file():
            lines = file.read_text()
            previous_persist = eval(lines)
        else:
            previous_persist = None
    print("Running segment-maker ...")
    with abjad.Timer() as timer:
        lilypond_file = definition.maker.run(
            metadata=metadata,
            midi=midi,
            persist=persist,
            previous_metadata=previous_metadata,
            previous_persist=previous_persist,
            segment_directory=segment_directory,
        )
    segment_maker_runtime = int(timer.elapsed_time)
    count = segment_maker_runtime
    counter = abjad.String("second").pluralize(count)
    message = f"Segment-maker runtime {count} {counter} ..."
    print(message)
    runtime = (count, counter)
    return definition, metadata, persist, lilypond_file, runtime


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


def _trim_illustration_ly(ly):
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
    part = baca.segments.part_directory_to_part(part_directory)
    dashed_part_name = abjad.String(part.name).to_dash_case()
    part_pdf = part_directory / f"{dashed_part_name}.pdf"
    print(f"Building {part_pdf.trim()} ...")
    snake_part_name = abjad.String(part.name).to_snake_case()
    layout_py = part_directory / f"{snake_part_name}_layout.py"
    os.system(f"make-layout-ly {layout_py}")
    print()
    os.system("interpret-build-music")
    print()
    front_cover_tex = part_directory / f"{dashed_part_name}-front-cover.tex"
    interpret_tex_file(front_cover_tex)
    print()
    preface_tex = part_directory / f"{dashed_part_name}-preface.tex"
    interpret_tex_file(preface_tex)
    print()
    back_cover_tex = part_directory / f"{dashed_part_name}-back-cover.tex"
    interpret_tex_file(back_cover_tex)
    print()
    part_tex = part_directory / f"{dashed_part_name}-part.tex"
    interpret_tex_file(part_tex)


def build_score(score_directory):
    assert score_directory.name.endswith("-score"), repr(score_directory)
    assert score_directory.parent.name == "builds", repr(score_directory)
    print("Building score ...")
    os.system("interpret-build-music")
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
            print(f"Using existing {pdf.trim()} ...")
            print()
    score_tex = score_directory / "score.tex"
    interpret_tex_file(score_tex)
    score_pdf = score_directory / "score.pdf"
    if not score_pdf.is_file():
        print(f"Could not produce {score_pdf.trim()} ...")
        sys.exit(-1)


def collect_segment_lys(_segments):
    assert _segments.name == "_segments", repr(_segments)
    segments_directory = _segments.contents / "segments"
    paths = sorted(segments_directory.glob("*"))
    names = [_.name for _ in paths]
    sources, targets = [], []
    for name in names:
        source = segments_directory / name / "illustration.ly"
        if not source.is_file():
            continue
        target = "segment-" + name.replace("_", "-") + ".ly"
        target = _segments / target
        sources.append(source)
        targets.append(target)
    return zip(sources, targets)


def collect_segment_lys_CLEAN(directory):
    segments_directory = directory.contents / "segments"
    paths = sorted(segments_directory.glob("**/illustration.ly"))
    return paths


def color_persistent_indicators(directory, undo=False):
    directory = baca.Path(directory)
    if directory.parent.name != "segments":
        print("Must call in segment directory ...")
        sys.exit(-1)
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


def handle_build_tags(_segments):
    print(f"Handling {_segments.trim()} build tags ...")
    pairs = baca.build.collect_segment_lys(_segments)
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

    # _segments = directory / "_segments"
    for job in [
        baca.jobs.handle_edition_tags(_segments),
        # baca.jobs.handle_fermata_bar_lines(directory),
        baca.jobs.handle_fermata_bar_lines(_segments),
        baca.jobs.handle_shifted_clefs(_segments),
        baca.jobs.handle_mol_tags(_segments),
        baca.jobs.color_persistent_indicators(_segments, undo=True),
        baca.jobs.show_music_annotations(_segments, undo=True),
        baca.jobs.join_broken_spanners(_segments),
        baca.jobs.show_tag(
            _segments,
            "left-broken-should-deactivate",
            match=match_left_broken_should_deactivate,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments, baca.tags.PHANTOM, skip_file_name=final_file_name
        ),
        baca.jobs.show_tag(
            _segments,
            baca.tags.PHANTOM,
            prepend_empty_chord=True,
            skip_file_name=final_file_name,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments,
            "phantom-should-activate",
            match=match_phantom_should_activate,
            skip_file_name=final_file_name,
        ),
        baca.jobs.show_tag(
            _segments,
            "phantom-should-deactivate",
            match=match_phantom_should_deactivate,
            skip_file_name=final_file_name,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments,
            baca.tags.EOS_STOP_MM_SPANNER,
            skip_file_name=final_file_name,
        ),
        baca.jobs.show_tag(
            _segments,
            baca.tags.METRIC_MODULATION_IS_STRIPPED,
            undo=True,
        ),
        baca.jobs.show_tag(
            _segments,
            baca.tags.METRIC_MODULATION_IS_SCALED,
            undo=True,
        ),
    ]:
        _run(job, quiet=False)


def handle_part_tags(directory):
    directory = baca.Path(directory)
    if not directory.parent.name.endswith("-parts"):
        print("Must call script in part directory ...")
        sys.exit(-1)
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
            result = path.deactivate(tag_, message_zero=message_zero, name=name)
            assert result is not None
            count, skipped, messages = result
        else:
            result = path.activate(tag_, message_zero=message_zero, name=name)
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

    # music_ly = directory / "music.ly"
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
        message = f"No part identifier found in {music_ly.trim()} ..."
        print(message)
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
    Interprets music.ly file in (score or part) build directory.

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
        sys.exit(-1)
    music_ly = list(build_directory.glob("*music.ly"))[0]
    if build_type == "score":
        _segments = build_directory / "_segments"
    elif build_type == "part":
        _segments = build_directory.parent / "_segments"
    else:
        raise Exception(build_type)
    if skip_segment_collection:
        print("Skipping segment collection ...")
    else:
        print("Collecting segment lys ...")
        segment_lys = collect_segment_lys_CLEAN(build_directory)
        if not segment_lys:
            print("Missing segment lys ...")
            sys.exit(1)
        if _segments.exists():
            print(f"Removing {_segments.trim()} ...")
            shutil.rmtree(str(_segments))
        print(f"Making {_segments.trim()} ...")
        _segments.mkdir()
        print("Writing", end=" ")
        for source_ly in segment_lys:
            text = _trim_illustration_ly(source_ly)
            segment_number = source_ly.parent.name
            target_ly = _segments / f"segment-{segment_number}.ly"
            print(f"{target_ly.name.split('-')[-1]}", end=" ")
            target_ly.write_text(text)
            source_ily = source_ly.with_suffix(".ily")
            if source_ily.is_file():
                target_ily = target_ly.with_suffix(".ily")
                print(f"{target_ily.name.split('-')[-1]}", end=" ")
                shutil.copyfile(str(source_ily), str(target_ily))
        print("...")
        handle_build_tags(_segments)
    if build_directory.parent.name.endswith("-parts"):
        if skip_segment_collection:
            print("Skipping tag handling ...")
        else:
            os.system("handle-part-tags")
    _check_layout_time_signatures(music_ly)
    run_lilypond(music_ly)
    if _segments.is_dir():
        print(f"Removing {_segments.trim()} ...")
        shutil.rmtree(str(_segments))


def interpret_tex_file(tex, open_after=False):
    if not tex.is_file():
        print(f"Can not find {tex.trim()} ...")
        return
    pdf = tex.with_suffix(".pdf")
    if pdf.exists():
        print(f"Removing {pdf.trim()} ...")
        pdf.unlink()
    print(f"Interpreting {tex.trim()} ...")
    if not tex.is_file():
        return
    executables = abjad.io.find_executable("xelatex")
    executables = [baca.Path(_) for _ in executables]
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
        print(f"Logging to {target.trim()} ...")
        for path in sorted(tex.parent.glob("*.aux")):
            path.unlink()
    if pdf.is_file():
        print(f"Found {pdf.trim()} ...")
        if open_after:
            os.system(f"open {pdf}")
    else:
        print(f"Can not produce {pdf.trim()} ...")
        sys.exit(-1)


def make_layout_ly(layout_py):
    if not layout_py.is_file():
        print(f"Skipping layout because no {layout_py.trim()} found ...")
        return
    layout_module_name = layout_py.with_suffix("").name
    if str(layout_py.parent) not in sys.path:
        sys.path.append(str(layout_py.parent))
    layout_module = importlib.import_module(layout_module_name)
    if "breaks" in dir(layout_module):
        breaks = layout_module.breaks
    else:
        print(f"No breaks in {layout_py.trim()} ...")
        sys.exit(-1)
    if "spacing" in dir(layout_module):
        spacing = layout_module.spacing
        prototype = baca.HorizontalSpacingSpecifier
        assert isinstance(spacing, prototype), repr(spacing)
    else:
        spacing = None
    buildspace_directory = layout_py.parent
    document_name = abjad.String(buildspace_directory.name).to_shout_case()
    if buildspace_directory.get_metadatum("parts_directory") is True:
        part_identifier = layout_module.part_identifier
        assert abjad.String(part_identifier).is_shout_case()
        document_name = f"{document_name}_{part_identifier}"
    if buildspace_directory.parent.name == "segments":
        string = "first_measure_number"
        first_measure_number = buildspace_directory.get_metadatum(string)
        if not bool(first_measure_number):
            print("Can not find first measure number ...")
            first_measure_number = False
        assert isinstance(first_measure_number, int)
    else:
        first_measure_number = 1
    if first_measure_number is False:
        print("Skipping layout ...")
        sys.exit(-1)
    assert abjad.String(document_name).is_shout_case()
    string = "first_measure_number"
    first_measure_number = buildspace_directory.get_metadatum(string, 1)
    if buildspace_directory.parent.name == "segments":
        time_signatures = buildspace_directory.get_metadatum("time_signatures")
    else:
        time_signatures = []
        segments_directory = buildspace_directory.contents / "segments"
        for segment_directory in sorted(segments_directory.glob("*")):
            time_signatures_ = segment_directory.get_metadatum("time_signatures")
            time_signatures.extend(time_signatures_)
    if breaks.partial_score is not None:
        time_signatures = time_signatures[: breaks.partial_score]
    maker = baca.SegmentMaker(
        breaks=breaks,
        do_not_check_persistence=True,
        do_not_include_layout_ly=True,
        first_measure_number=first_measure_number,
        score_template=baca.SingleStaffScoreTemplate(),
        spacing=spacing,
        time_signatures=time_signatures,
    )
    lilypond_file = maker.run(
        do_not_print_timing=True,
        environment="layout",
        remove=baca.tags.layout_removal_tags(),
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
    layout_ly = layout_module_name.replace("_", "-") + ".ly"
    layout_ly = buildspace_directory / layout_ly
    lines = []
    if breaks.partial_score is not None:
        lines.append("% partial_score = True")
    if buildspace_directory.parent.name == "segments":
        first_segment = buildspace_directory.parent / "01"
        if buildspace_directory.name != first_segment.name:
            previous_segment = str(int(buildspace_directory.name) - 1).zfill(2)
            previous_segment = buildspace_directory.parent / previous_segment
            previous_layout_ly = previous_segment / "layout.ly"
            if previous_layout_ly.is_file():
                result = baca.segments.get_preamble_page_count_overview(
                    previous_layout_ly
                )
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
    layout_ly.write_text(header + text + "\n")
    counter = abjad.String("measure").pluralize(measure_count)
    print(f"Writing {measure_count} + 1 {counter} to {layout_ly.trim()} ...")
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
    print(f"Writing BOL measure {numbers} {items} to metadata ...")
    buildspace_directory.add_buildspace_metadatum(
        "bol_measure_numbers",
        bol_measure_numbers,
        document_name=document_name,
    )


def make_segment_pdf(
    segment_directory,
    do_not_interpret_ly=False,
    layout=True,
    timing=False,
):
    assert segment_directory.parent.name == "segments"
    if layout is True:
        os.system(f"make-layout-ly {segment_directory / 'layout.py'}")
    print(f"Making segment {segment_directory.name} PDF ...")
    result = _import_definition_and_run_segment_maker(segment_directory)
    definition, metadata, persist, lilypond_file, runtime = result
    print("Writing __metadata__ ...")
    segment_directory.write_metadata_py(definition.maker.metadata)
    os.system("black --target-version=py38 __metadata__ 1>/dev/null 2>&1")
    print("Writing __persist__ ...")
    segment_directory.write_metadata_py(
        definition.maker.persist,
        file_name="__persist__",
        variable_name="persist",
    )
    os.system("black --target-version=py38 __persist__ 1>/dev/null 2>&1")
    first_segment = segment_directory.parent / "01"
    layout_ly = segment_directory / "layout.ly"
    if layout_ly.is_file() and segment_directory.name != first_segment.name:
        result = baca.segments.get_preamble_page_count_overview(layout_ly)
        if result is not None:
            first_page_number, _, _ = result
            line = r"\paper { first-page-number = #"
            line += str(first_page_number)
            line += " }"
            lines = abjad.tag.double_tag([line], "__make_segment_pdf__")
            lines.append("")
            lilypond_file.items[-1:-1] = lines
    illustration_ly = segment_directory / "illustration.ly"
    result = abjad.persist.as_ly(lilypond_file, illustration_ly)
    abjad_format_time = int(result[1])
    count = abjad_format_time
    counter = abjad.String("second").pluralize(count)
    message = f"Abjad format time {count} {counter} ..."
    print(message)
    abjad_format_time = (count, counter)
    if "Global_Skips" in lilypond_file:
        context = lilypond_file["Global_Skips"]
        measure_count = len(context)
        counter = abjad.String("measure").pluralize(measure_count)
        message = f"Wrote {measure_count} {counter}"
        message += f" to {illustration_ly.trim()} ..."
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
    text = illustration_ly.read_text()
    text = abjad.LilyPondFormatManager.left_shift_tags(text)
    illustration_ly.write_text(text)
    for job in [
        baca.jobs.handle_edition_tags(illustration_ly),
        baca.jobs.handle_fermata_bar_lines(segment_directory),
        baca.jobs.handle_shifted_clefs(segment_directory),
        baca.jobs.handle_mol_tags(segment_directory),
    ]:
        for message in job():
            print(message)
    layout_py = segment_directory / "layout.py"
    if not layout_py.exists():
        print(f"No {layout_py.trim()} found ...")
    else:
        layout_ly = segment_directory / "layout.ly"
        layout_time_signatures = baca.segments.get_preamble_time_signatures(layout_ly)
        if layout_time_signatures is not None:
            assert isinstance(layout_time_signatures, list)
            layout_measure_count = len(layout_time_signatures)
            counter = abjad.String("measure").pluralize(layout_measure_count)
            message = f"Found {layout_measure_count} {counter}"
            message += f" in {layout_ly.trim()} ..."
            print(message)
            if layout_time_signatures == time_signatures:
                message = "Music time signatures match"
                message += " layout time signatures ..."
                print(message)
            else:
                message = "Music time signatures do not match"
                message += " layout time signatures ..."
                print(message)
                print(f"Remaking {layout_ly.trim()} ...")
                os.system(f"make-layout-ly --layout-py={layout_py}")
                counter = abjad.String("measure").pluralize(measure_count)
                message = f"Found {measure_count} {counter}"
                message += f" in {illustration_ly.trim()} ..."
                print(message)
                layout_time_signatures = baca.segments.get_preamble_time_signatures(
                    layout_ly
                )
                layout_measure_count = len(layout_time_signatures)
                counter = abjad.String("measure").pluralize(layout_measure_count)
                message = f"Found {layout_measure_count} {counter}"
                message += f" in {layout_ly.trim()} ..."
                print(message)
                if layout_time_signatures != time_signatures:
                    message = "Music time signatures still do not match"
                    message += " layout time signatures ..."
                    print(message)
    if getattr(definition.maker, "do_not_externalize", False) is not True:
        illustration_ly.extern()
        illustration_ily = illustration_ly.with_suffix(".ily")
        assert illustration_ily.is_file()
        not_topmost = baca.Job(
            deactivate=(abjad.Tag("NOT_TOPMOST"), "not topmost"),
            path=segment_directory,
            title="deactivating NOT_TOPMOST ...",
        )
        for message in not_topmost():
            print(message)
    illustration_ly = segment_directory / "illustration.ly"
    if not do_not_interpret_ly:
        lilypond_log_file_path = illustration_ily.parent / ".log"
        with abjad.Timer() as timer:
            print("Running LilyPond ...")
            baca_repo_path = os.getenv("BACA")
            flags = f"--include={baca_repo_path}/lilypond"
            abjad_repo_path = os.getenv("ABJAD")
            flags += f" --include={abjad_repo_path}/docs/source/_stylesheets"
            abjad.io.run_lilypond(
                illustration_ly,
                flags=flags,
                lilypond_log_file_path=lilypond_log_file_path,
            )
        baca.segments.remove_lilypond_warnings(
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
    for name in ["illustration.ly", "illustration.ily", "layout.ly"]:
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
        base, extension = name.split(".")
        untagged = segment_directory / f"{base}.untagged.{extension}"
        untagged.write_text(string)
    if timing and not do_not_interpret_ly:
        timing = segment_directory / ".timing"
        with timing.open(mode="a") as pointer:
            print(f"Writing timing to {timing.trim()} ...")
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
    if illustration_ly.is_file():
        print(f"Found {illustration_ly.trim()} ...")
    illustration_pdf = segment_directory / "illustration.pdf"
    if not do_not_interpret_ly:
        if illustration_pdf.is_file():
            print(f"Found {illustration_pdf.trim()} ...")
    __pycache__ = segment_directory / "__pycache__"
    shutil.rmtree(str(__pycache__))


def run_lilypond(ly_file_path):
    assert ly_file_path.exists()
    if not abjad.io.find_executable("lilypond"):
        raise ValueError("cannot find LilyPond executable.")
    print(f"Running LilyPond on {ly_file_path.trim()} ...")
    directory = ly_file_path.parent
    pdf = ly_file_path.with_suffix(".pdf")
    backup_pdf = ly_file_path.with_suffix("._backup.pdf")
    lilypond_log_file_name = "." + ly_file_path.name + ".log"
    lilypond_log_file_path = directory / lilypond_log_file_name
    if backup_pdf.exists():
        backup_pdf.unlink()
    if pdf.exists():
        print(f"Removing {pdf.trim()} ...")
        pdf.unlink()
    assert not pdf.exists()
    with abjad.TemporaryDirectoryChange(directory=directory):
        print(f"Interpreting {ly_file_path.trim()} ...")
        print(f"Logging to {lilypond_log_file_path.trim()} ...")
        ABJAD = os.getenv("ABJAD")
        if ABJAD is None:
            print("Must set ABJAD environment variable to local copy of Abjad repo ...")
            sys.exit(-1)
        BACA = os.getenv("BACA")
        if BACA is None:
            print("Must set BACA environment variable to local copy of Bača repo ...")
            sys.exit(-1)
        flags = "--include=$ABJAD/docs/source/_stylesheets --include=$BACA/lilypond"
        abjad.io.run_lilypond(
            str(ly_file_path),
            flags=flags,
            lilypond_log_file_path=(lilypond_log_file_path),
        )
        baca.segments.remove_lilypond_warnings(
            lilypond_log_file_path,
            crescendo_too_small=True,
            decrescendo_too_small=True,
            overwriting_glissando=True,
        )
        _display_lilypond_log_errors(lilypond_log_file_path)
        if pdf.is_file():
            print(f"Found {pdf.trim()} ...")
        else:
            print(f"Can not produce {pdf.trim()} ...")
        assert lilypond_log_file_path.exists()


def show_annotations(directory, undo=False):
    directory = baca.Path(directory)
    if directory.parent.name != "segments":
        print("Must call in segment directory ...")
        sys.exit(-1)
    for job in _make_annotation_jobs(directory, undo=undo):
        job = abjad.new(job, message_zero=True)
        messages = job()
        for message in messages:
            print(message)


def show_tag(directory, tag, undo=False):
    directory = baca.Path(directory)
    tag = abjad.Tag(tag)
    job = baca.jobs.show_tag(directory, tag, undo=undo)
    job = abjad.new(job, message_zero=True)
    for message in job():
        print(message)
