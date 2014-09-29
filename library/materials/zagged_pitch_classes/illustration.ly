% 2014-07-09 13:23

\version "2.19.9"
\language "english"

\include "/Users/trevorbaca/Documents/abjad/abjad/stylesheets/rhythm-letter-16.ily"

\header {}

\layout {
	\accidentalStyle forget
}

\paper {}

\score {
	\new Score \with {
		\override BarLine #'stencil = ##f
		\override Flag #'stencil = ##f
		\override Stem #'stencil = ##f
		\override TextScript #'staff-padding = #3
		\override TimeSignature #'stencil = ##f
	} <<
		\new Staff {
			\new Voice \with {
				\consists Horizontal_bracket_engraver
			} {
				g'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								0
							}
						}
				cs'8
				ef'8
				e'8
				f'8
				b'8 \stopGroup \stopGroup
				ef'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								1
							}
						}
				f'8
				fs'8
				g'8 \stopGroup \stopGroup
				a'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								2
							}
						}
				bf'8
				c'8
				af'8 \stopGroup \stopGroup
				g'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								3
							}
						}
				ef'8
				f'8
				fs'8 \stopGroup
				af'8 \startGroup
				a'8
				bf'8
				c'8
				b'8
				g'8
				cs'8
				ef'8
				e'8
				f'8
				c'8
				af'8
				a'8
				bf'8 \stopGroup \stopGroup
				f'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								4
							}
						}
				b'8 \stopGroup
				g'8 \startGroup
				cs'8 \stopGroup
				ef'8 \startGroup
				e'8 \stopGroup \stopGroup
				fs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								5
							}
						}
				g'8
				ef'8 \stopGroup \stopGroup
				f'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								6
							}
						}
				e'8
				f'8
				b'8
				g'8 \stopGroup \stopGroup
				cs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								7
							}
						}
				ef'8 \stopGroup \stopGroup
				f'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								8
							}
						}
				fs'8
				g'8
				ef'8 \stopGroup
				bf'8 \startGroup
				c'8
				af'8
				a'8 \stopGroup \stopGroup
				ef'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								9
							}
						}
				f'8
				fs'8
				g'8
				a'8 \stopGroup
				bf'8 \startGroup
				c'8
				af'8
				ef'8
				e'8
				f'8 \stopGroup
				b'8 \startGroup
				g'8
				cs'8 \stopGroup \stopGroup
				af'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								10
							}
						}
				a'8
				bf'8
				c'8 \stopGroup \stopGroup
				cs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								11
							}
						}
				ef'8
				e'8
				f'8
				b'8
				g'8 \stopGroup \stopGroup
				g'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								12
							}
						}
				ef'8
				f'8
				fs'8
				g'8
				cs'8
				ef'8
				e'8
				f'8
				b'8 \stopGroup \stopGroup
				fs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								13
							}
						}
				g'8
				ef'8
				f'8
				c'8
				af'8
				a'8
				bf'8 \stopGroup
				f'8 \startGroup
				fs'8
				g'8
				ef'8 \stopGroup \stopGroup
				bf'8 \startGroup \stopGroup \startGroup
					^ \markup {
						\bold
							{
								14
							}
						}
				c'8 \startGroup
				af'8 \stopGroup
				a'8 \startGroup
				b'8
				g'8 \stopGroup \stopGroup
				cs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								15
							}
						}
				ef'8
				e'8
				f'8
				a'8
				bf'8
				c'8
				af'8 \stopGroup \stopGroup
				f'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								16
							}
						}
				b'8
				g'8
				cs'8
				ef'8
				e'8 \stopGroup \stopGroup
				ef'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								17
							}
						}
				f'8
				fs'8
				g'8 \stopGroup \stopGroup
				e'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								18
							}
						}
				f'8
				b'8
				g'8
				cs'8
				ef'8 \stopGroup
				g'8 \startGroup
				ef'8
				f'8 \stopGroup \stopGroup
				fs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								19
							}
						}
				af'8
				a'8
				bf'8 \stopGroup
				c'8 \startGroup \stopGroup
				fs'8 \startGroup
				g'8
				ef'8
				f'8 \stopGroup \stopGroup
				c'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								20
							}
						}
				af'8
				a'8
				bf'8 \stopGroup \stopGroup
				ef'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								21
							}
						}
				e'8
				f'8
				b'8
				g'8
				cs'8
				bf'8
				c'8
				af'8
				a'8 \stopGroup \stopGroup
				cs'8 \startGroup \startGroup
					^ \markup {
						\bold
							{
								22
							}
						}
				ef'8
				e'8
				f'8
				b'8
				g'8
				f'8
				fs'8
				g'8
				ef'8 \stopGroup \stopGroup
				\bar "|."
			}
		}
	>>
}