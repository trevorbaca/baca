\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    \with
    {
        autoBeaming = ##f
    }
    {
        {   % measure
            \time 2/8
            \tempo 4=60
            c'8
            d'8
        }   % measure
        {   % measure
            e'8
            f'8
        }   % measure
        {   % measure
            g'8
            a'8
        }   % measure
        {   % measure
            b'8
            c''8
        }   % measure
    }
}