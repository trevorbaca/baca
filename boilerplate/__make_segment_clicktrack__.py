#! /usr/bin/env python
import os
import pathlib
import sys
import traceback

import abjad
import baca

if __name__ == "__main__":

    try:
        from definition import maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __metadata__ import metadata as metadata
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __persist__ import persist as persist
    except ModuleNotFoundError:
        persist = None

    try:
        {previous_segment_persist_import_statement}
    except ModuleNotFoundError:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment_directory = baca.Path(os.path.realpath(__file__)).parent
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                metadata=metadata,
                midi=True,
                persist=persist,
                previous_metadata=previous_metadata,
                previous_persist=previous_persist,
                segment_directory=segment_directory,
            )
        count = int(timer.elapsed_time)
        counter = abjad.String("second").pluralize(count)
        message = f"Abjad runtime {{count}} {{counter}} ..."
        print(message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    time_signatures = maker.time_signatures
    assert maker.validate_measure_count == len(time_signatures)

    global_skips = lilypond_file["Global_Skips"]
    skips = abjad.select(global_skips).leaves()[:-1]
    assert maker.validate_measure_count == len(skips)

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

    try:
        segment_directory = baca.Path(__file__).parent
        score_directory = segment_directory.contents
        stem = f"{{score_directory.name}}-{{segment_directory.name}}-clicktrack"
        midi = stem + ".midi"
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            abjad.persist.as_midi(lilypond_file, midi, remove_ly=True)
        count = int(timer.elapsed_time)
        counter = abjad.String("second").pluralize(count)
        message = f"LilyPond runtime {{count}} {{counter}} ..."
        print(message)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
