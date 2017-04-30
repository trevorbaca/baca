# -*- coding: utf-8 -*-
from __future__ import print_function
import abjad
import ide
import shutil
import os
import subprocess


configuration = ide.tools.idetools.AbjadIDEConfiguration()
boilerplate_path = configuration.abjad_ide_boilerplate_directory
boilerplate_path = os.path.join(boilerplate_path, '__illustrate_segment__.py')

def illustrate_segment(segment_path):
    local_boilerplate_path = os.path.join(
        segment_path,
        '__illustrate_segment__.py',
        )
    illustration_ly_path = os.path.join(
        segment_path,
        'illustration.ly',
        )
    illustration_pdf_path = os.path.join(
        segment_path,
        'illustration.pdf',
        )
    illustration_candidate_ly_path = os.path.join(
        segment_path,
        'illustration.candidate.ly',
        )
    illustration_candidate_pdf_path = os.path.join(
        segment_path,
        'illustration.candidate.pdf',
        )
    if os.path.exists(local_boilerplate_path):
        os.remove(local_boilerplate_path)
    with abjad.systemtools.FilesystemState(
        keep=[illustration_ly_path, illustration_pdf_path],
        remove=[local_boilerplate_path],
        ):
        shutil.copyfile(boilerplate_path, local_boilerplate_path)
        ide.tools.idetools.AbjadIDE._replace_in_file(
            local_boilerplate_path,
            '{previous_segment_metadata_import_statement}',
            'previous_segment_metadata = None',
            )
        ide.tools.idetools.AbjadIDE._replace_in_file(
            local_boilerplate_path,
            '{{}}',
            '{}',
            )
        assert os.path.exists(local_boilerplate_path)
        assert not os.path.exists(illustration_candidate_ly_path)
        assert not os.path.exists(illustration_candidate_pdf_path)
        command = 'python {}'.format(local_boilerplate_path)
        exit_status = abjad.systemtools.IOManager.spawn_subprocess(command)
        assert exit_status == 0
        assert os.path.exists(illustration_candidate_ly_path)
        assert os.path.exists(illustration_candidate_pdf_path)
        shutil.move(illustration_candidate_ly_path, illustration_ly_path)
        shutil.move(illustration_candidate_pdf_path, illustration_pdf_path)


if __name__ == '__main__':
    this_file = os.path.abspath(__file__)
    test_directory = os.path.dirname(this_file)
    inner_score_directory = os.path.dirname(test_directory)
    segments_directory = os.path.join(
        inner_score_directory,
        'segments',
        )
    names = os.listdir(segments_directory)
    names.sort()
    for name in names:
        segment_directory = os.path.join(
            segments_directory,
            name,
            )
        definition_file = os.path.join(
            segments_directory,
            name,
            'definition.py',
            )
        if not os.path.isfile(definition_file):
            continue
        with abjad.systemtools.Timer() as timer:
            message = 'Illustrating {} ... '
            message = message.format(definition_file)
            print(message)
            illustrate_segment(segment_directory)
