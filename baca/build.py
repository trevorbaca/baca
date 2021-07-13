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


def collect_segment_lys(directory):
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


def copy_boilerplate(directory, source_name, target_name=None, values=None):
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
    target.write_text(template + "\n")


def interpret_tex_file(tex, open_after=False):
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
