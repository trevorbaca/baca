Vim macros
==========

To renumber lists:

    @i:     qigg/^\d<return>cw1<esc>"nyw/\.<return>dwi.<tab><esc>q
    @j:     qj/^\d<return>cw<ctrl>rn<esc><ctrl>a0"nyw/\.<return>dwi.<tab><esc>q
    @r:     q@i:g/^\d/ normal @j<return>ggq

Macro @i sets the first left-edge-adjacent number to 1.

Macro @j increments the next left-edge-adjacent number.

Macro @r ("renumber") calls @j recursively and then returns to top-of-file.

Doctest trim script:

    import pathlib
    path = pathlib.Path('/Users/trevorbaca/Desktop/out')
    keep = []
    found_got = False
    for line in path.open('r'):
        if line.startswith('File') and 'line' in line:
            print(line)
        if found_got:
            if line.startswith('*********'):
                break
            keep.append(line)
        if line == 'Got:\n':
            found_got = True
    text = ''.join(keep)
    trimmed = pathlib.Path('trimmed')
    trimmed.write_text(text)

Read into register x:

    :let @x = join(readfile("/Users/trevorbaca/Desktop/trimmed"), "\n")  
