import os
import shutil
import sys

import abjad
import baca

abjad_configuration = abjad.Configuration()


def _display_lilypond_log_errors(lilypond_log_file_path=None):
    if lilypond_log_file_path is None:
        lilypond_log_file_path = abjad_configuration.lilypond_log_file_path
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


def _make_container_to_part_assignment(directory):
    pairs = collect_segment_lys(directory.build)
    if not pairs:
        print("... no segment lys found.")
        return
    container_to_part_assignment = abjad.OrderedDict()
    for source, target in pairs:
        segment = source.parent
        value = segment.get_metadatum(
            "container_to_part_assignment", file_name="__persist__"
        )
        if value:
            container_to_part_assignment[segment.name] = value
    return container_to_part_assignment


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


def collect_segment_lys(directory):
    segments_directory = directory.contents / "segments"
    paths = sorted(segments_directory.glob("*"))
    names = [_.name for _ in paths]
    sources, targets = [], []
    for name in names:
        source = segments_directory / name / "illustration.ly"
        if not source.is_file():
            continue
        target = "segment-" + name.replace("_", "-") + ".ly"
        target = directory / "_segments" / target
        sources.append(source)
        targets.append(target)
    builds_directory = directory / "builds"
    if not builds_directory.is_dir():
        builds_directory.mkdir()
    return zip(sources, targets)


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


def handle_build_tags(directory):
    directory = baca.Path(directory)
    assert directory.is_build() or directory.name == "_segments"
    print("Handling build tags ...")
    pairs = baca.build.collect_segment_lys(directory.build)
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

    _segments = directory / "_segments"
    for job in [
        baca.jobs.handle_edition_tags(_segments),
        baca.jobs.handle_fermata_bar_lines(directory),
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
    if not directory.is_part():
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
            print(" " + message)

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

    music_ly = directory / "music.ly"
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
        target = tex.with_name(name)
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


def part_subtitle(part_name, parentheses=False):
    words = abjad.String(part_name).delimit_words()
    number = None
    try:
        number = int(words[-1])
    except ValueError:
        pass
    if number is not None:
        if parentheses:
            words[-1] = f"({number})"
        else:
            words[-1] = str(number)
    words = [_.lower() for _ in words]
    part_subtitle = " ".join(words)
    return part_subtitle


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
        _display_lilypond_log_errors(lilypond_log_file_path=lilypond_log_file_path)
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


def to_paper_dimensions(paper_size, orientation="portrait"):
    orientations = ("landscape", "portrait", None)
    assert orientation in orientations, repr(orientation)
    # lilypond.org/doc/v2.19/Documentation/notation/predefined-paper-sizes
    paper_dimensions = {
        "a3": "297 x 420 mm",
        "a4": "210 x 297 mm",
        "arch a": "9 x 12 in",
        "arch b": "12 x 18 in",
        "arch c": "18 x 24 in",
        "arch d": "24 x 36 in",
        "arch e": "36 x 48 in",
        "legal": "8.5 x 14 in",
        "ledger": "17 x 11 in",
        "letter": "8.5 x 11 in",
        "tabloid": "11 x 17 in",
    }[paper_size]
    paper_dimensions = paper_dimensions.replace(" x ", " ")
    width, height, unit = paper_dimensions.split()
    if orientation == "landscape":
        height_ = width
        width_ = height
        height = height_
        width = width_
    return width, height, unit
