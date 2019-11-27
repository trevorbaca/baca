% Harm and Andrew Bernard on the LilyPond list (2019-03-11)
% only works when Bača definition of Solomon's flared hairpin is removed:

{
    \alterBroken stencil
      #(list
        ly:hairpin::print
        ly:hairpin::print
        (elbowed-hairpin '((0 . 0.3333) (0.95 . 0.4) (1.0 . 1.0)) #t))
      Hairpin
    c'1\< \break c' \break s c'\!
}
