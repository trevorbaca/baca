SEGMENTING LILYPOND SCORE FILES
===============================

The `music.ly` in each build directory will look something like this:
```
    % Score (2016) for guitar

    \version "2.19.52"
    \language "english"

    #(ly:set-option 'relative-includes #t)
    \include "stylesheet.ily"

    \score {
        {
        \include "../_segments/segment--introduction.ly"
        \include "../_segments/segment-a.ly"
        \include "../_segments/segment-b.ly"
        \include "../_segments/segment-c.ly"
        \include "../_segments/segment-d.ly"
        \include "../_segments/segment-e.ly"
        \include "../_segments/segment-f.ly"
        \include "../_segments/segment-g.ly"
        \include "../_segments/segment-h.ly"
        \include "../_segments/segment-i.ly"
        \include "../_segments/segment-j.ly"
        \include "../_segments/segment-k.ly"
        \include "../_segments/segment-l.ly"
        \include "../_segments/segment-m.ly"
        }
    }
```
There is an important LilyPond gotcha in the way each segment file must be
constructed.

This example with the LilyPond `\new` command does NOT work:
```
    \score {
        \context Score = "Score" <<
            \new PianoStaff <<
                ...
            >>
        >>
    }
```

But this example with only the LilyPond `\context` command DOES work:
```
    \score {
        \context Score = "Score" <<
            \context PianoStaff = "Piano Staff" <<
                ...
            >>
        >>
    }
```

IMPORTANT: segment files must *NOT* start any contexts with the Lilypond `\new`
command.

IMPORTANT: all contexts must be named.
