import io
import os
import shutil
import subprocess
import sys

import abjad
import baca

abjad_configuration = abjad.Configuration()


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


def _interpret_tex_file(tex):
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
        print(f"Logging {target.trim()} ...")
        for path in sorted(tex.parent.glob("*.aux")):
            path.remove()
    if pdf.is_file():
        print(f"Found {pdf.trim()} ...")
    else:
        print(f"Can not produce {pdf.trim()} ...")
        sys.exit(-1)


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


def _run_lilypond(ly_file_path, indent=0):
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
        print(f"Logging {lilypond_log_file_path.trim()} ...")
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
