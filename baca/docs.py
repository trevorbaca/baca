import abjad

from . import score as _score

_global_context_string = r"""\layout
{
    \context
    {
        \name GlobalSkips
        \type Engraver_group
        \consists Staff_symbol_engraver
        \override StaffSymbol.stencil = ##f
    }
    \context
    {
        \name GlobalContext
        \type Engraver_group
        \consists Axis_group_engraver
        \consists Mark_engraver
        \consists Metronome_mark_engraver
        \consists Time_signature_engraver
        \accepts GlobalSkips
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.break-align-symbol = #'left-edge
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.space-alist.clef = #'(extra-space . 0.5)
    }
    \context { \Staff \remove Time_signature_engraver }
    \context
    {
        \name MusicContext
        \type Engraver_group
        \consists System_start_delimiter_engraver
        \accepts StaffGroup
    }
    \context
    {
        \Score
        \accepts GlobalContext
        \accepts MusicContext
        \remove Bar_number_engraver
        \remove Mark_engraver
        \remove Metronome_mark_engraver
        \remove System_start_delimiter_engraver
    }
}
"""


def global_context_string():
    """
    Makes global context string.
    """
    return _global_context_string


def make_empty_score(*counts):
    r"""
    Makes empty score for doc examples.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            {
                \context Staff = "Music_Staff"
                {
                    \context Voice = "Music_Voice"
                    {
                    }
                }
            }
        >>

    ..  container:: example

        >>> score = baca.docs.make_empty_score(4)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Music_Voice_1"
                    {
                    }
                    \context Voice = "Music_Voice_2"
                    {
                    }
                    \context Voice = "Music_Voice_3"
                    {
                    }
                    \context Voice = "Music_Voice_4"
                    {
                    }
                >>
            }
        >>

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1, 1, 1, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            <<
                \context StaffGroup = "Music_Staff_Group"
                <<
                    \context Staff = "Music_Staff_1"
                    {
                        \context Voice = "Music_Voice_1"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_2"
                    {
                        \context Voice = "Music_Voice_2"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_3"
                    {
                        \context Voice = "Music_Voice_3"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_4"
                    {
                        \context Voice = "Music_Voice_4"
                        {
                        }
                    }
                >>
            >>
        >>

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1, 2, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "Global_Context"
            <<
                \context GlobalRests = "Global_Rests"
                {
                }
                \context GlobalSkips = "Global_Skips"
                {
                }
            >>
            \context MusicContext = "Music_Context"
            <<
                \context StaffGroup = "Music_Staff_Group"
                <<
                    \context Staff = "Music_Staff_1"
                    {
                        \context Voice = "Music_Voice_1"
                        {
                        }
                    }
                    \context Staff = "Music_Staff_2"
                    <<
                        \context Voice = "Music_Voice_2"
                        {
                        }
                        \context Voice = "Music_Voice_3"
                        {
                        }
                    >>
                    \context Staff = "Music_Staff_3"
                    {
                        \context Voice = "Music_Voice_4"
                        {
                        }
                    }
                >>
            >>
        >>

    """

    site = "baca.make_configuration_empty_score()"
    tag = abjad.Tag(site)
    global_context = _score.make_global_context()
    single_staff = len(counts) == 1
    single_voice = single_staff and counts[0] == 1
    staves, voice_number = [], 1
    for staff_index, voice_count in enumerate(counts):
        if single_staff:
            name = "Music_Staff"
        else:
            staff_number = staff_index + 1
            name = f"Music_Staff_{staff_number}"
        simultaneous = 1 < voice_count
        staff = abjad.Staff(name=name, simultaneous=simultaneous, tag=tag)
        voices = []
        for voice_index in range(voice_count):
            if single_voice:
                name = "Music_Voice"
            else:
                name = f"Music_Voice_{voice_number}"
            voice = abjad.Voice(name=name, tag=tag)
            voices.append(voice)
            voice_number += 1
        staff.extend(voices)
        staves.append(staff)

    if len(staves) == 1:
        music = staves
        simultaneous = False
    else:
        music = [abjad.StaffGroup(staves, name="Music_Staff_Group")]
        simultaneous = True

    music_context = abjad.Context(
        music,
        lilypond_type="MusicContext",
        simultaneous=simultaneous,
        name="Music_Context",
        tag=tag,
    )

    score = abjad.Score([global_context, music_context], name="Score", tag=tag)
    return score
