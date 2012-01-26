% Abjad revision 4973M
% 2012-01-27 14:45

\version "2.15.24"
\include "english.ly"
\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

\header {
	tagline = \markup { "" }
	title = \markup { red notes }
}

\score {
	\new Score <<
		\new PianoStaff <<
			\context Staff = "treble" {
				\clef "treble"
				d'16
				e'8
				f'16
				d'8
				e'16
				f'8
				d'16
				e'8
				f'16
				d'8
				e'16
				f'8
				d'16
				e'8
				f'16
				d'8
				e'16
				f'8
			}
			\context Staff = "bass" {
				\clef "bass"
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
				r16
				r8
			}
		>>
	>>
}