% Aaron Hill (list)
% 2019-06-27

\include "english.ly"
\version "2.19.83"

% Aaron's clef example

\new Staff
{
    \clef "bass"
    \repeat unfold 10
    {
         g2. g4 |
    }
    \break
    % problem: override always affects both clefs:
    %\once \override Staff.Clef #'X-extent = #'(-2 . 2)
    %\once \override Staff.Clef.color = #red

    \once \override Staff.Clef.before-line-breaking = #(lambda (grob)
    (and (eq? LEFT (ly:item-break-dir grob))
        (set! (ly:grob-property grob 'X-extent) '(-2 . 2))))

    \once \override Staff.Clef.color = #(lambda (grob)
    (and (eq? RIGHT (ly:item-break-dir grob))
        (set! (ly:grob-property grob 'color) red )))

    \clef "tenor"
    \repeat unfold 7
    {
         g8 g g2.
    }
}

% Modification for bar lines:

\new Staff
{
    c'4 c'4 c'4 c'4
    c'4 c'4 c'4 c'4
    \bar ".|:"                                                                 %! baca.bar_line():baca.IndicatorCommand._call()
    % problem: override always affects both clefs:
    %\once \override Staff.BarLine.color = #red
    \once \override Staff.BarLine.color = #(lambda (grob)
    (and (eq? RIGHT (ly:item-break-dir grob))
        (set! (ly:grob-property grob 'color) red )))
    \break
    c'4 c'4 c'4 c'4
    c'4 c'4 c'4 c'4
}
