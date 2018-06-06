\include "flared-hairpin-for-trevor.ily"


\relative c' {

    \override Score.Hairpin.stencil = #flared-hairpin-old
    a\< b c d |
    e\f a a a |
    a\< b c d |
    a b c d |
    a b c d |
    a b c d |
    e\f a a a |
    \break

    \override Score.Hairpin.stencil = #flared-hairpin-new
    a\< b c d |
    e\f a a a |
    a\< b c d |
    a b c d |
    a b c d |
    a b c d |
    e\f a a a |

}
