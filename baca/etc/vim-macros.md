Vim macros
==========

To renumber lists:

    @i:     qigg/^\d<return>cw1<esc>"nyw/\.<return>dwi.<tab><esc>q
    @j:     qj/^\d<return>cw<ctrl>rn<esc><ctrl>a0"nyw/\.<return>dwi.<tab><esc>q
    @r:     q@i:g/^\d/ normal @j<return>ggq

Macro @i sets the first left-edge-adjacent number to 1.

Macro @j increments the next left-edge-adjacent number.

Macro @r ("renumber") calls @j recursively and then returns to top-of-file.
