from abjad import *
import baca


def test_UserInputGetter_append_values_01():

    getter = baca.scf.menuing.UserInputGetter()
    getter.append_integer('attribute')
    assert getter.run(user_input='foo -99') == -99

    getter = baca.scf.menuing.UserInputGetter()
    getter.append_integer_in_closed_range('attribute', 1, 10)
    assert getter.run(user_input='foo -99 99 7') == 7

    getter = baca.scf.menuing.UserInputGetter()
    argument_list = ['apple', 'banana', 'cherry', 'durian', 'endive', 'fennel']
    getter.append_argument_range('attribute', argument_list)
    assert getter.run(user_input='fen-dur, app, che') == [6, 5, 4, 1, 3]

    getter = baca.scf.menuing.UserInputGetter()
    getter.append_markup('attribute')
    assert getter.run(user_input='foo') == markuptools.Markup('foo')

    getter = baca.scf.menuing.UserInputGetter()
    getter.append_named_chromatic_pitch('attribute')
    assert getter.run(user_input="cs'") == pitchtools.NamedChromaticPitch("cs'")

    getter = baca.scf.menuing.UserInputGetter()
    getter.append_string('attribute')
    assert getter.run(user_input='None -99 99 1-4 foo') == 'foo'

    getter = baca.scf.menuing.UserInputGetter()
    getter.append_string_or_none('attribute')
    assert getter.run(user_input='-99 99 1-4 None') is None
