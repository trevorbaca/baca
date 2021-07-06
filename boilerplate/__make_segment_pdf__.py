#! /usr/bin/env python
import os
import sys
import time
import traceback

import abjad
import baca

if __name__ == "__main__":

    try:
        from definition import maker

        {previous_segment_metadata_import_statement}

        from __metadata__ import metadata as metadata

    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment_directory = baca.Path(os.path.realpath(__file__)).parent
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        {previous_segment_persist_import_statement}
    except ModuleNotFoundError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __persist__ import persist as persist
    except ModuleNotFoundError:
        segment_directory.write_metadata_py(
            None,
            file_name="__persist__.py",
            variable_name="persist",
        )
        persist = None

    try:
        scores_directory = segment_directory.parent.parent.parent.parent
        segment_directory = baca.Path(segment_directory)
        assert segment_directory.is_score_package_path(), repr(segment_directory)
        illustration_ly = segment_directory / "illustration.ly"
        print(" Running segment-maker ...")
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                persist=persist,
                previous_metadata=previous_metadata,
                previous_persist=previous_persist,
                segment_directory=segment_directory,
            )
        segment_maker_runtime = int(timer.elapsed_time)
        count = segment_maker_runtime
        counter = abjad.String("second").pluralize(count)
        message = f" Segment-maker runtime {{count}} {{counter}} ..."
        print(message)
        segment_maker_runtime = (count, counter)
        print(" Writing __metadata__.py ...")
        segment_directory.write_metadata_py(maker.metadata)
        os.system("black --target-version=py38 __metadata__.py")
        print(" Writing __persist__.py ...")
        segment_directory.write_metadata_py(
            maker.persist,
            file_name="__persist__.py",
            variable_name="persist",
        )
        os.system("black --target-version=py38 __persist__.py")
        first_segment = segment_directory.segments.get_next_package()
        if segment_directory.name != first_segment.name:
            layout_ly = segment_directory / "layout.ly"
            if not layout_ly.is_file():
                message = f"{{layout_ly.trim()}} does not exit."
                raise Exception(message)
            result = baca.segments.get_preamble_page_count_overview(layout_ly)
            if result is not None:
                first_page_number, _, _ = result
                line = r"\paper {{ first-page-number = #"
                line += str(first_page_number)
                line += " }}"
                lines = abjad.tag.double_tag([line], "__make_segment_pdf__")
                lines.append("")
                lilypond_file.items[-1:-1] = lines
        result = abjad.persist.as_ly(lilypond_file, illustration_ly)
        abjad_format_time = int(result[1])
        count = abjad_format_time
        counter = abjad.String("second").pluralize(count)
        message = f" Abjad format time {{count}} {{counter}} ..."
        print(message)
        abjad_format_time = (count, counter)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        if "Global_Skips" in lilypond_file:
            context = lilypond_file["Global_Skips"]
            measure_count = len(context)
            counter = abjad.String("measure").pluralize(measure_count)
            message = f" Wrote {{measure_count}} {{counter}}"
            message += f" to {{illustration_ly.trim()}} ..."
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
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
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
                print(" " + message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        layout_py = segment_directory / "layout.py"
        if not layout_py.exists():
            print(" Writing stub layout.py ...")
            layout_py.write_text("")
        layout_ly = segment_directory / "layout.ly"
        if not layout_ly.exists():
            print(" Writing stub layout.ly ...")
            layout_ly.write_text("")
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        if layout_py.read_text() == "":
            empty_layout = True
        else:
            empty_layout = False
        if empty_layout:
            print(f" Ignoring empty {{layout_py.trim()}} ...")
        else:
            layout_time_signatures = baca.segments.get_preamble_time_signatures(
                layout_ly
            )
            if layout_time_signatures is not None:
                assert isinstance(layout_time_signatures, list)
                layout_measure_count = len(layout_time_signatures)
                counter = abjad.String("measure").pluralize(layout_measure_count)
                message = f" Found {{layout_measure_count}} {{counter}}"
                message += f" in {{layout_ly.trim()}} ..."
                print(message)
                if layout_time_signatures == time_signatures:
                    message = " Music time signatures match"
                    message += " layout time signatures ..."
                    print(message)
                else:
                    message = "Music time signatures do not match"
                    message += " layout time signatures ..."
                    print(message)
                    print(f" Remaking {{layout_ly.trim()}} ...")
                    os.system(f"make_layout_ly --layout-py={{layout_py}}")
                    counter = abjad.String("measure").pluralize(measure_count)
                    message = f" Found {{measure_count}} {{counter}}"
                    message += f" in {{illustration_ly.trim()}} ..."
                    print(message)
                    layout_time_signatures = baca.segments.get_preamble_time_signatures(
                        layout_ly
                    )
                    layout_measure_count = len(layout_time_signatures)
                    counter = abjad.String("measure").pluralize(layout_measure_count)
                    message = f" Found {{layout_measure_count}} {{counter}}"
                    message += f" in {{layout_ly.trim()}} ..."
                    print(message)
                    if layout_time_signatures != time_signatures:
                        message = " Music time signatures still do not match"
                        message += " layout time signatures ..."
                        print(message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        if getattr(maker, "do_not_externalize", False) is not True:
            illustration_ly.extern()
            illustration_ily = illustration_ly.with_suffix(".ily")
            assert illustration_ily.is_file()
            not_topmost = baca.Job(
                deactivate=(abjad.Tag("NOT_TOPMOST"), "not topmost"),
                path=segment_directory,
                title="deactivating NOT_TOPMOST ...",
            )
            for message in not_topmost():
                print(" " + message)
        lilypond_log_file_path = illustration_ily.parent / ".log"
        with abjad.Timer() as timer:
            print(" Running LilyPond ...")
            baca_repo_path = os.getenv("BACA")
            flags = f"--include={{baca_repo_path}}/lilypond"
            abjad_repo_path = os.getenv("ABJAD")
            flags += f" --include={{abjad_repo_path}}/docs/source/_stylesheets"
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
        message = f" LilyPond runtime {{count}} {{counter}} ..."
        print(message)
        lilypond_runtime = (count, counter)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        for name in ["illustration.ly", "illustration.ily", "layout.ly"]:
            tagged = segment_directory / name
            if not tagged.exists():
                continue
            with tagged.open() as pointer:
                lines = []
                for line in pointer.readlines():
                    if '%@%' not in line:
                        lines.append(line)
            string = "".join(lines)
            string = abjad.format.remove_tags(string)
            base, extension = name.split(".")
            untagged = segment_directory / f"{{base}}.untagged.{{extension}}"
            untagged.write_text(string)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        timing = segment_directory / ".timing"
        with timing.open(mode="a") as pointer:
            pointer.write("\n")
            line = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
            pointer.write(line)
            count, counter = segment_maker_runtime
            line = f" Segment-maker runtime: {{count}} {{counter}}\n"
            pointer.write(line)
            count, counter = abjad_format_time
            line = f" Abjad format time: {{count}} {{counter}}\n"
            pointer.write(line)
            count, counter = lilypond_runtime
            line = f" LilyPond runtime: {{count}} {{counter}}\n"
            pointer.write(line)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
