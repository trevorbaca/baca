#! /usr/bin/env python
import doctest
import io
import os
import pathlib
import sys

import abjad
import abjadext
import baca
from abjadext import rmakers

try:
    from abjadext import nauert
except ImportError:
    nauert = None


def _doctest_files(current_directory, files, globals_, report_only_first_failure=False):
    if report_only_first_failure:
        optionflags = (
            doctest.ELLIPSIS
            | doctest.NORMALIZE_WHITESPACE
            | doctest.REPORT_ONLY_FIRST_FAILURE
        )
    else:
        optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    failed_file_paths, error_messages = [], []
    failure_count, test_count = 0, 0
    for file_ in files:
        assert file_.is_file(), repr(file_)
        parent_directory = str(file_.parent)
        sys.path.insert(0, parent_directory)
        string_buffer = io.StringIO()
        with abjad.RedirectedStreams(stdout=string_buffer):
            failure_count_, test_count_ = doctest.testfile(
                file_,
                module_relative=False,
                globs=globals_,
                optionflags=optionflags,
            )
            failure_count += failure_count_
            test_count += test_count_
            doctest_output = string_buffer.getvalue()
        assert sys.path[0] == parent_directory
        del sys.path[0]
        if failure_count_:
            failed_file_paths.append(os.path.relpath(file_))
            error_messages.append(doctest_output)
            strings = (baca.colors.red, "FAILED", baca.colors.end)
            result_code = "".join(strings)
        else:
            strings = (baca.colors.blue, "OK", baca.colors.end)
            result_code = "".join(strings)
        relative_path = os.path.relpath(file_)
        print(f"{relative_path} {result_code}")
    if failed_file_paths:
        print()
        for error_message in error_messages:
            print(error_message)
    for file_ in failed_file_paths:
        print(f"FAILED: {file_}")
    print()
    test_identifier = abjad.string.pluralize("test", test_count)
    module_identifier = abjad.string.pluralize("module", len(names))
    success_count = test_count - failure_count
    string = (
        f"{success_count} passed, {failure_count} failed out of "
        f"{test_count} {test_identifier} "
        f"in {len(names)} {module_identifier}."
    )
    print(string)
    if failed_file_paths:
        return -1
    return 0


def _get_globals():
    globals_ = {}
    globals_["abjad"] = abjad
    globals_["abjadext"] = abjadext
    globals_["baca"] = baca
    if nauert is not None:
        globals_["nauert"] = nauert
    globals_["rmakers"] = rmakers
    return globals_


def main(current_directory, globals_, names, report_only_first_failure):
    files = []
    for name in names:
        path = current_directory / name
        if path.is_file():
            files.append(path)
            continue
        if path.is_dir():
            for path_ in sorted(path.glob("**/*.py")):
                if path_.is_file():
                    files.append(path_)
        else:
            files.append(path)
    files.sort()
    exit_code = _doctest_files(
        current_directory,
        files,
        globals_,
        report_only_first_failure=report_only_first_failure,
    )
    return exit_code


if __name__ == "__main__":
    current_directory = pathlib.Path(os.getcwd())
    names, report_only_first_failure = [], False
    for input_ in sys.argv[1:]:
        if input_ == "--report-only-first-failure":
            report_only_first_failure = True
        else:
            names.append(input_)
    assert names, repr(names)
    globals_ = _get_globals()
    exit_code = main(current_directory, globals_, names, report_only_first_failure)
    sys.exit(exit_code)
