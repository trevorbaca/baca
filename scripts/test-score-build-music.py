#! /usr/bin/env python
import os
import pathlib
import sys

import baca


def _make_fail_string(string):
    return f"{baca.colors.red}FAIL: {string} ...{baca.colors.end}"


def _make_file_handling_string(string):
    return f"{baca.colors.yellow}{string} ...{baca.colors.end}"


def _make_pass_string(string):
    return f"{baca.colors.green_bold}PASS: {string} ...{baca.colors.end}"


def _get_builds():
    builds_directory = pathlib.Path(os.getcwd())
    if not builds_directory.name == "builds":
        raise Exception("Must run from builds directory.")
    builds = []
    if builds_directory.exists():
        for path in sorted(builds_directory.iterdir()):
            if path.is_dir() and path.name.endswith("-score"):
                builds.append(path)
    return builds


def _test_build(build):
    os.chdir(build)
    baca.build.print_main_task(f"Building {build} ...")
    messages, diffs, result = [], [], 0
    music_ly = build / "music.ly"
    if music_ly.exists():
        layout_py = build / "layout.py"
        if layout_py.exists():
            os.system("python layout.py")
        os.system("interpret-build-music.py")
        if layout_py.exists():
            layout_ily = build / "layout.ily"
            if layout_ily.exists():
                message = _make_pass_string(f"{baca.path.trim(layout_ily)} found")
            else:
                message = _make_fail_string(f"{baca.path.trim(layout_ily)} missing")
                result = 99
            messages.append(message)
            if layout_ily.exists():
                tmp = build / "tmp"
                os.system(f"git diff --color=always {layout_ily} > {tmp} 2>&1")
                with open(tmp) as pointer:
                    lines = pointer.readlines()
                tmp.unlink()
                if not lines:
                    message = _make_pass_string(f"{baca.path.trim(layout_ily)} same")
                else:
                    diffs.append(lines[:30])
                    message = _make_fail_string(
                        f"{baca.path.trim(layout_ily)} different"
                    )
                    result = 99
                messages.append(message)
        music_pdf = build / "music.pdf"
        if music_pdf.exists():
            message = _make_pass_string(f"{baca.path.trim(music_pdf)} found")
        else:
            message = _make_fail_string(f"{baca.path.trim(music_pdf)} missing")
            result = 99
        messages.append(message)
    else:
        message = _make_file_handling_string(f"Missing {baca.path.trim(music_ly)}")
        messages.append(message)
    return messages, diffs, result


def main():
    builds = _get_builds()
    messages, diffs, result = [], [], 0
    for i, build in enumerate(builds):
        messages_, diffs_, result_ = _test_build(build)
        messages.extend(messages_)
        diffs.extend(diffs_)
        result = result or result_
    messages.append("")
    for diff in diffs:
        string = "".join(diff)
        print(string)
    for message in messages:
        print(message)


if __name__ == "__main__":
    result = main()
    sys.exit(result)
