% Abjad revision 4952M
% 2012-01-10 19:31

\version "2.15.17"
\include "english.ly"
\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

\include "/Users/trevorbaca/Documents/other/baca/materials/demo_material/stylesheet.ly"

\header {
	tagline = \markup { "" }
	title = \markup { demo material }
}

\score {
	\new Score <<
		\new PianoStaff <<
			\context Staff = "treble" {
				\clef "treble"
				d'16
				e'8
				f'8
				g'16
				a'8
				d'8
				e'16
				f'8
				g'8
				a'16
				d'8
				e'8
				f'16
				g'8
				a'8
				d'16
				e'8
				f'8
				g'16
				a'8
				d'8
				e'16
				f'8
				g'8
				a'16
				d'8
				e'8
				f'16
				g'8
				a'8
			}
			\context Staff = "bass" {
				\clef "bass"
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
				r16
				r8
				r8
			}
		>>
	>>
}