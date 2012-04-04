import scf


def test_StringQuartetScoreTemplate___call___01():

    template = scf.templates.StringQuartetScoreTemplate()
    score = template()

    r'''
    \new Score <<
        \new StaffGroup <<
            \context Staff = "violin 1" {
                \clef "treble"
            }
            \context Staff = "violin 2" {
                \clef "treble"
            }
            \context Staff = "viola" {
                \clef "alto"
            }
            \context Staff = "cello" {
                \clef "bass"
            }
        >>
    >>
    '''

    assert score.format == '\\new Score <<\n\t\\new StaffGroup <<\n\t\t\\context Staff = "violin 1" {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\context Staff = "violin 2" {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\context Staff = "viola" {\n\t\t\t\\clef "alto"\n\t\t}\n\t\t\\context Staff = "cello" {\n\t\t\t\\clef "bass"\n\t\t}\n\t>>\n>>'
