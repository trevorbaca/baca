from abjad import *
from scf import specifiers
import py
import scf


def test_MusicContributionSpecifierEditor_run_01():
    py.test.skip('errors on empty breadcrumb stack.')

    editor = scf.editors.MusicContributionSpecifierEditor()
    editor.run(user_input='name blue~violin~pizzicati add instrument instrument violin done done')

    specifier = specifiers.MusicContributionSpecifier([
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.Violin()
            )
        ])

    assert editor.target == specifier
