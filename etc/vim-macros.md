Vim macros
==========

To renumber lists:

    @i:     qigg/^\d<return>cw1<esc>"nyw/\.<return>dwi.<tab><esc>q
    "i      gg/^\d^Mcw1^["nyw/\.^Mdwi.^I^[

    @j:     qj/^\d<return>cw<ctrl>rn<esc><ctrl>a0"nyw/\.<return>dwi.<tab><esc>q
    "j      /^\d^Mcw^Rn^[^A0"nyw/\.^Mdwi.^I^[

    @r:     qr@i:g/^\d/ normal @j<return>@iq
    "r      @i:g/^\d/ normal @j^M@i

    Macro @i sets the first left-edge-adjacent number to 1.
    Macro @j increments the next left-edge-adjacent number.
    Macro @r ("renumber") calls @j recursively and then returns to top-of-file.

To trim doctest output and replace in buffer:

    ajv doctest --external-modules=baca -x > ~/.tmp.doctest.out;
    cat ~/.tmp/doctest.out;
    trim-doctest

    @y:     qy:let @x = join(readfile("~/.tmp/doctest.trimmed"), "\n")q
    @b:     qbo<esc>jvipDo<esc>k@y<return>"xpvipo>><esc>kdd:w<return>q

    Macro @y reads doctest.trimmed into register x.
    Macro @b deletes block below, calls @y, pastes, indents, saves.
