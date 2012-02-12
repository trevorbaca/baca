from abjad.tools.durationtools import Duration
from baca.scf import UserInputWrapper
import baca


def test_SargassoMeasureMaterialPackageMaker_01():

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')

    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', None),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_02():

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')

    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', True),
            ('measures_are_split', True),
            ('measures_are_shuffled', True)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_03():

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')

    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uil uic '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', None),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_04():
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso 3 16 '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', 16),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_05():
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso 3 16 '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', 16),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_06():
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uip 5 '
            'Duration(11, 2) False True True 4 [2, 2, 2, 2, 1, 1, 4, 4] 16 [1, 1, 2, 3, 4] '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', False),
            ('measures_are_split', True),
            ('measures_are_shuffled', True)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')


def test_SargassoMeasureMaterialPackageMaker_07():
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testsargasso')
    try:
        studio.run(user_input=
            'materials maker sargasso testsargasso default '
            'testsargasso uip 1 '
            '4 [2, 2, 3, 3] 16 [1, 1, 1, 1, 6, 6] b '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'baca.materials.testsargasso')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 3, 3]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 1, 1, 6, 6]),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testsargasso del remove default q')
        assert not studio.package_exists('baca.materials.testsargasso')
