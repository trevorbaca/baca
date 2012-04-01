import scf


def test_make_two_staff_piano_score_01():

    score = scf.templates.make_two_staff_piano_score()

    r'''
    \new Score <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
            }
            \context Staff = "bass" {
                \clef "bass"
            }
        >>
    >>
    '''

    assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t}\n\t>>\n>>'
