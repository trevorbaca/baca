from abjad import *


t = Note(0, (1, 4))
t.notehead.style = 'cross'
t.notehead.color = 'red'
t.stem.color = 'red'
t.articulations.append('staccato')
t.articulations.append('tenuto')
t.markup.down.append(r'\italic { ben. marcato }')
t.comments.before.append('textual information before')
t.comments.after.append('textual information after')
