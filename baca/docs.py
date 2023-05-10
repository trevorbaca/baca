"""
Docs.
"""
from inspect import currentframe as _frame

import abjad

from . import score as _score
from . import tags as _tags

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


def _move_global_context(score):
    global_skips = score["Skips"]
    global_skips.lilypond_type = "Voice"
    music_context = score["MusicContext"]
    for component in abjad.iterate.components(music_context):
        if isinstance(component, abjad.Staff):
            first_music_staff = component
            break
    first_music_staff.simultaneous = True
    first_music_staff.insert(0, global_skips)
    score["GlobalContext"][:] = []
    del score["GlobalContext"]
    assert len(score) == 1, repr(score)
    score[:] = music_context[:]
    if len(score) == 1:
        score.simultaneous = False


def attach_time_signature(voice: abjad.Voice) -> None:
    assert isinstance(voice, abjad.Voice), repr(voice)
    duration = abjad.get.duration(voice)
    time_signature = abjad.TimeSignature(duration.pair)
    leaf = abjad.select.leaf(voice, 0)
    abjad.detach(abjad.TimeSignature, leaf)
    abjad.attach(time_signature, leaf)


def global_context_string():
    """
    Makes global context string.
    """
    return _global_context_string


def lilypond_file(score, *, includes=None):
    lilypond_file = abjad.LilyPondFile()
    for name in includes or []:
        lilypond_file.items.append(rf'\include "{name}"')
    lilypond_file.items.append("")
    lilypond_file.items.append(score)
    return lilypond_file


def make_empty_score(*counts, do_not_move_global_context=False, no_skips=False):
    r"""
    Makes empty score for doc examples.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                }
                \context Voice = "Music"
                {
                }
            >>
        }

    ..  container:: example

        >>> score = baca.docs.make_empty_score(4)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                }
                \context Voice = "Music.1"
                {
                }
                \context Voice = "Music.2"
                {
                }
                \context Voice = "Music.3"
                {
                }
                \context Voice = "Music.4"
                {
                }
            >>
        }

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1, 1, 1, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context StaffGroup = "StaffGroup"
            <<
                \context Staff = "Staff.1"
                <<
                    \context Voice = "Skips"
                    {
                    }
                    \context Voice = "Music.1"
                    {
                    }
                >>
                \context Staff = "Staff.2"
                {
                    \context Voice = "Music.2"
                    {
                    }
                }
                \context Staff = "Staff.3"
                {
                    \context Voice = "Music.3"
                    {
                    }
                }
                \context Staff = "Staff.4"
                {
                    \context Voice = "Music.4"
                    {
                    }
                }
            >>
        }

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1, 2, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context StaffGroup = "StaffGroup"
            <<
                \context Staff = "Staff.1"
                <<
                    \context Voice = "Skips"
                    {
                    }
                    \context Voice = "Music.1"
                    {
                    }
                >>
                \context Staff = "Staff.2"
                <<
                    \context Voice = "Music.2"
                    {
                    }
                    \context Voice = "Music.3"
                    {
                    }
                >>
                \context Staff = "Staff.3"
                {
                    \context Voice = "Music.4"
                    {
                    }
                }
            >>
        }

    """
    tag = _tags.function_name(_frame())
    global_context = _score.make_global_context()
    single_staff = len(counts) == 1
    single_voice = single_staff and counts[0] == 1
    staves, voice_number = [], 1
    for staff_index, voice_count in enumerate(counts):
        if single_staff:
            name = "Staff"
        else:
            staff_number = staff_index + 1
            name = f"Staff.{staff_number}"
        simultaneous = 1 < voice_count
        staff = abjad.Staff(name=name, simultaneous=simultaneous, tag=tag)
        voices = []
        for voice_index in range(voice_count):
            if single_voice:
                name = "Music"
            else:
                name = f"Music.{voice_number}"
            voice = abjad.Voice(name=name, tag=tag)
            voices.append(voice)
            voice_number += 1
        staff.extend(voices)
        staves.append(staff)
    if len(staves) == 1:
        music = staves
        simultaneous = False
    else:
        music = [abjad.StaffGroup(staves, name="StaffGroup")]
        simultaneous = True
    music_context = abjad.Context(
        music,
        lilypond_type="MusicContext",
        simultaneous=simultaneous,
        name="MusicContext",
        tag=tag,
    )
    score = abjad.Score([global_context, music_context], name="Score", tag=tag)
    if not do_not_move_global_context:
        _move_global_context(score)
    if no_skips is True:
        del score["Skips"]
    for context in abjad.select.components(score, abjad.Context):
        if len(context) == 1:
            context.simultaneous = False
    return score


def make_single_staff_score(components):
    voice = abjad.Voice(components, name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    score = abjad.Score([staff], name="Score", simultaneous=False)
    duration = abjad.get.duration(components)
    time_signature = abjad.TimeSignature(duration.pair)
    leaf = abjad.select.leaf(components, 0)
    abjad.attach(time_signature, leaf)
    return score


def remove_deactivated_wrappers(score):
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if wrapper.tag is None:
                continue
            if wrapper.deactivate:
                abjad.detach(wrapper, leaf)
