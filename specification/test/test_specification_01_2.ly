\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 2/8
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					r4
				}
				{
					r4
				}
			}
		}
		\context RhythmicStaff = "Staff 2" {
			\context Voice = "Voice 2" {
				{
					r4
				}
				{
					r4
				}
			}
		}
		\context RhythmicStaff = "Staff 3" {
			\context Voice = "Voice 3" {
				{
					r4
				}
				{
					r4
				}
			}
		}
		\context RhythmicStaff = "Staff 4" {
			\context Voice = "Voice 4" {
				{
					r4
				}
				{
					r4
				}
			}
		}
	>>
>>