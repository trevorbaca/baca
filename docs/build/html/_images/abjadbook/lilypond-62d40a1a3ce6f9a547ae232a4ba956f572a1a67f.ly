\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        <c' d' e' f'>4
        <d' e' f' g' a' b'>4
        <e' f' g' a'>4
        <f' g' a' b' c'' d''>4
    }
}