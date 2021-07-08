import io
import os
import shutil
import subprocess
import sys

import abjad
import baca

abjad_configuration = abjad.Configuration()


# lilypond.org/doc/v2.19/Documentation/notation/predefined-paper-sizes
paper_size_to_paper_dimensions = {
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
}


def _collect_segment_lys(directory):
    paths = directory.segments.list_paths()
    names = [_.name for _ in paths]
    sources, targets = [], []
    for name in names:
        source = directory.segments / name / "illustration.ly"
        if not source.is_file():
            continue
        target = "segment-" + name.replace("_", "-") + ".ly"
        target = directory._segments / target
        sources.append(source)
        targets.append(target)
    if not directory.builds.is_dir():
        directory.builds.mkdir()
    return zip(sources, targets)


def _copy_boilerplate(directory, source_name, target_name=None, values=None):
    target_name = target_name or source_name
    target = directory / target_name
    if target.exists():
        print(f"Removing {target.trim()} ...")
    print(f"Writing {target.trim()} ...")
    values = values or {}
    boilerplate = baca.Path(baca.__file__).parent.parent / "boilerplate"
    source = boilerplate / source_name
    target_name = target_name or source_name
    target = directory / target_name
    shutil.copyfile(str(source), str(target))
    if not values:
        return
    template = target.read_text()
    template = template.format(**values)
    target.write_text(template)


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


def _generate_part_music_ly(
    path,
    dashed_part_name=None,
    forces_tagline=None,
    keep_with_tag=None,
    part=None,
    part_subtitle=None,
):
    assert path.build.exists(), repr(path)
    print(f"Generating {path.trim()} ...")
    if path.exists():
        print(f"Removing {path.trim()} ...")
        path.remove()
    segments = path.segments.list_paths()
    if not segments:
        print("No segments found ...")
    for segment in segments:
        if not segment.is_segment():
            continue
        message = f"examining {segment.trim()} ..."
        print(message)
    names = [_.stem.replace("_", "-") for _ in segments]
    boilerplate = "part-music.ly"
    _copy_boilerplate(path.build, boilerplate, target_name=path.name)
    lines, ily_lines = [], []
    for i, name in enumerate(names):
        name = "segment-" + name + ".ly"
        ly = path.build._segments / name
        if ly.is_file():
            line = rf'\include "../_segments/{name}"'
        else:
            line = rf'%\include "../_segments/{name}"'
        ily_lines.append(line.replace(".ly", ".ily"))
        if 0 < i:
            line = 8 * " " + line
        lines.append(line)
    if lines:
        segment_ily_include_statements = "\n".join(ily_lines)
    else:
        segment_ily_include_statements = ""
    language_token = abjad.LilyPondLanguageToken()
    lilypond_language_directive = abjad.lilypond(language_token)
    version_token = abjad.LilyPondVersionToken()
    lilypond_version_directive = abjad.lilypond(version_token)
    annotated_title = path.contents.get_title(year=True)
    if annotated_title:
        score_title = annotated_title
    else:
        score_title = path.contents.get_title(year=False)
    score_title_without_year = path.contents.get_title(year=False)
    if forces_tagline is None:
        string = "forces_tagline"
        forces_tagline = path.contents.get_metadatum(string, "")
    if forces_tagline:
        forces_tagline = forces_tagline.replace("\\", "")
    assert path.is_file(), repr(path)
    template = path.read_text()
    if path.parent.is_part():
        identifiers = baca.segments.global_skip_identifiers(path)
        identifiers = ["\\" + _ for _ in identifiers]
        newline = "\n" + 24 * " "
        global_skip_identifiers = newline.join(identifiers)
        dictionary = _make_container_to_part_assignment(path)
        identifiers = baca.segments.part_to_identifiers(path, part, dictionary)
        if isinstance(identifiers, str):
            print(identifiers + " ...")
            message = f"removing {path.trim()} ..."
            print(message)
            path.remove()
            return
        identifiers = ["\\" + _ for _ in identifiers]
        newline = "\n" + 24 * " "
        segment_ly_include_statements = newline.join(identifiers)
        template = template.format(
            dashed_part_name=dashed_part_name,
            forces_tagline=forces_tagline,
            global_skip_identifiers=global_skip_identifiers,
            lilypond_language_directive=lilypond_language_directive,
            lilypond_version_directive=lilypond_version_directive,
            part_identifier=repr(part.identifier),
            part_subtitle=part_subtitle,
            score_title=score_title,
            score_title_without_year=score_title_without_year,
            segment_ily_include_statements=segment_ily_include_statements,
            segment_ly_include_statements=segment_ly_include_statements,
        )
    path.write_text(template)


# TODO: replace?
def _interpret_file(path):
    path = baca.Path(path)
    if not path.exists():
        print(f"Missing {path} ...")
    if path.suffix == ".py":
        command = f"python {path}"
    elif path.suffix == ".ly":
        command = f"lilypond -dno-point-and-click {path}"
    else:
        message = f"can not interpret {path}."
        raise Exception(message)
    directory = path.parent
    directory = abjad.TemporaryDirectoryChange(directory)
    string_buffer = io.StringIO()
    with directory, string_buffer:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for line in process.stdout:
            line = line.decode("utf-8")
            print(line, end="")
            string_buffer.write(line)
        process.wait()
        stdout_lines = string_buffer.getvalue().splitlines()
        stderr_lines = abjad.io._read_from_pipe(process.stderr)
        stderr_lines = stderr_lines.splitlines()
    exit_code = process.returncode
    if path.suffix == ".ly":
        lilypond_log_file_path = directory / ".log"
        _display_lilypond_log_errors(lilypond_log_file_path=lilypond_log_file_path)
    return stdout_lines, stderr_lines, exit_code


def _interpret_tex_file(tex, open_after=False):
    if not tex.is_file():
        print(f"Can not find {tex.trim()} ...")
        return
    pdf = tex.with_suffix(".pdf")
    if pdf.exists():
        print(f"Removing {pdf.trim()} ...")
        pdf.remove()
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
            path.remove()
    if pdf.is_file():
        print(f"Found {pdf.trim()} ...")
        if open_after:
            os.system(f"open {pdf}")
    else:
        print(f"Can not produce {pdf.trim()} ...")
        sys.exit(-1)


def _make_container_to_part_assignment(directory):
    pairs = _collect_segment_lys(directory.build)
    if not pairs:
        print("... no segment lys found.")
        return
    container_to_part_assignment = abjad.OrderedDict()
    for source, target in pairs:
        segment = source.parent
        value = segment.get_metadatum(
            "container_to_part_assignment", file_name="__persist__.py"
        )
        if value:
            container_to_part_assignment[segment.name] = value
    return container_to_part_assignment


def _make_layout_ly(path):
    assert path.suffix == ".py"
    maker = "__make_layout_ly__.py"
    maker = path.parent / maker
    with abjad.FilesystemState(remove=[maker]):
        _copy_boilerplate(
            path.parent,
            maker.name,
            values={"layout_module_name": path.stem},
        )
        print(f"Interpreting {maker.trim()} ...")
        result = _interpret_file(maker)
        print(f"Removing {maker.trim()} ...")
    stdout_lines, stderr_lines, exit_code = result
    if exit_code:
        for string in stderr_lines:
            print(string)
    pycache = path.parent / "__pycache__"
    pycache.remove()


def _part_subtitle(part_name, parentheses=False):
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


def _run_lilypond(ly_file_path):
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
        backup_pdf.remove()
    if pdf.exists():
        print(f"Removing {pdf.trim()} ...")
        pdf.remove()
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


def _to_paper_dimensions(paper_size, orientation="portrait"):
    orientations = ("landscape", "portrait", None)
    assert orientation in orientations, repr(orientation)
    paper_dimensions = paper_size_to_paper_dimensions[paper_size]
    paper_dimensions = paper_dimensions.replace(" x ", " ")
    width, height, unit = paper_dimensions.split()
    if orientation == "landscape":
        height_ = width
        width_ = height
        height = height_
        width = width_
    return width, height, unit
