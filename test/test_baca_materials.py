# -*- encoding: utf-8 -*-
import ide
import os
import pytest
import shutil
import baca
from abjad.tools import systemtools


boilerplate_path = ide.idetools.Configuration().boilerplate_directory
boilerplate_path = os.path.join(boilerplate_path, '__output_material__.py')

materials_path = os.path.join(baca.__path__[0], 'materials')
abbreviations_path = os.path.join(materials_path, 'abbreviations.py')
miscellaneous_materials_path = os.path.join(materials_path, 'miscellaneous.py')

directory_names = os.listdir(materials_path)
directory_names = [_ for _ in directory_names if not _.startswith(('.', '_'))]

material_paths = [os.path.join(materials_path, _) for _ in directory_names]
material_paths = [_ for _ in material_paths if os.path.isdir(_)]


@pytest.mark.parametrize('material_path', material_paths)
def test_baca_materials_01(material_path):
    local_boilerplate_path = os.path.join(
        material_path,
        '__output_material__.py',
        )
    local_output_path = os.path.join(
        material_path,
        'output.py',
        )
    if os.path.exists(local_boilerplate_path):
        os.remove(local_boilerplate_path)
    with systemtools.FilesystemState(
        remove=[local_boilerplate_path],
        ):
        shutil.copyfile(boilerplate_path, local_boilerplate_path)
        if os.path.exists(local_output_path):
            os.remove(local_output_path)
        assert os.path.exists(local_boilerplate_path)
        assert not os.path.exists(local_output_path)
        command = 'python {}'.format(local_boilerplate_path)
        exit_status = systemtools.IOManager.spawn_subprocess(command)
        assert exit_status == 0
        assert os.path.exists(local_output_path)