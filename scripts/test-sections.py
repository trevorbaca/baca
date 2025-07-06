#! /usr/bin/env python
import argparse
import os
import pathlib
import sys
import types

import abjad

import baca


def _capture_diff(path):
    if not path.is_file():
        return
    command = f"git ls-files --error-unmatch {path} 1>/dev/null 2>&1"
    if os.system(command) != 0:
        return
    _out = path.with_name(".out")
    if _out.exists():
        _out.unlink()
    with abjad.contextmanagers.FilesystemState(remove=[_out]):
        command = f'git diff --color=always -I"\version.*" {path.name} > .out'
        os.system(command)
        with open(_out) as pointer:
            lines = pointer.readlines()
            if lines:
                string = "".join(lines[:30])
                print(string)
                return False
    return True


def _make_result_strings(path, results):
    strings = []
    if results.exists is True:
        string = baca.colors.green_bold + f"{path.name} found" + baca.colors.end
    else:
        string = baca.colors.red_bold + f"{path.name} missing" + baca.colors.end
    strings.append(string)
    if results.same is True:
        string = baca.colors.green_bold + f"{path.name} same" + baca.colors.end
    elif results.same is False:
        string = baca.colors.red_bold + f"{path.name} changed ..." + baca.colors.end
    strings.append(string)
    return strings


def _print_results(path, results):
    if results.exists is True:
        baca.build.print_success(f"PASS: {path.name} found ...")
    else:
        baca.build.print_error(f"FAIL: {path.name} missing ...")
    if results.same is True:
        baca.build.print_success(f"PASS: {path.name} same ...")
    elif results.same is False:
        baca.build.print_error(f"FAIL: {path.name} changed ...")


def _test_section(section_directory, *, do_not_call_lilypond=False):
    assert section_directory.parent.name == "sections", repr(section_directory)
    metadata = baca.path.get_metadata(section_directory)
    names = ["music.ily", "music.ly", "music.pdf"]
    if metadata.get("first_metronome_mark") is not False:
        # names.extend(["clicktrack.midi", "music.midi"])
        pass
    names.sort()
    layout_ily = section_directory / "layout.ily"
    if layout_ily.exists():
        names.append("layout.ily")
    names.sort()
    path_to_results = {}
    for name in names:
        path = section_directory / name
        results = types.SimpleNamespace()
        path_to_results[path] = results
    music_ly = section_directory / "music.ly"
    if music_ly.exists():
        music_ly.unlink()
    music_ily = section_directory / "music.ily"
    if music_ily.exists():
        music_ily.unlink()
    # command = "python music.py --also-untagged --clicktrack --log-timing --midi --pdf"
    if do_not_call_lilypond is True:
        command = "python music.py --also-untagged --layout --log-timing --pdf"
        command += " --do-not-call-lilypond"
    else:
        command = "python music.py --also-untagged --layout --log-timing --pdf"
    os.system(command)
    for path, results in path_to_results.items():
        results.exists = path.is_file()
        results.same = _capture_diff(path)
    music_pdf = section_directory / "music.pdf"
    if not music_pdf.exists():
        _music_ly_log = section_directory / "_music_ly_log"
        if _music_ly_log.exists():
            with open(".music.ly.log") as pointer:
                lines = pointer.readlines()
                print("".join(lines))
    strings = []
    all_true, total_tests = True, 0
    for path, results in path_to_results.items():
        if results.exists is False or results.same is False:
            all_true = False
        total_tests += 2
    if all_true:
        baca.build.print_success(f"{total_tests}/{total_tests} tests passed ...")
    else:
        for path, results in path_to_results.items():
            _print_results(path, results)
            strings_ = _make_result_strings(path, results)
            strings.extend(strings_)
        for part in abjad.sequence.partition_by_counts(
            strings, [4], cyclic=True, overhang=True
        ):
            pass
            # print(", ".join(part))
    result = 0
    for results in path_to_results.values():
        if results.exists is False:
            result += 1
        if results.same is False:
            result += 1
    return result


def main(current_directory):
    parser = argparse.ArgumentParser(description="Test sections in score.")
    parser.add_argument(
        "--do-not-call-lilypond", help="Python only", action="store_true"
    )
    arguments = parser.parse_args()
    contents_directory = baca.path.get_contents_directory(current_directory)
    sections_directory = contents_directory / "sections"
    result = 0
    for path in sorted(sections_directory.glob("[0-9]*")):
        if not path.is_dir():
            continue
        os.chdir(path)
        result_ = _test_section(
            path, do_not_call_lilypond=arguments.do_not_call_lilypond
        )
        if result_ != 0:
            result = result_
        print()
    return result


if __name__ == "__main__":
    current_directory = pathlib.Path(os.getcwd())
    result = main(current_directory)
    sys.exit(result)
