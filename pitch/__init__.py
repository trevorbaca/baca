# these imports populate the namespace of the pitch module explicitly
# and therefore avoiding polluting the namespace of the pitch module
# with temp variables, imported helper functions and the like.
from baca.pitch.pitch import C
from baca.pitch.pitch import D

# this clean-up line causes the namespace of pitch to contain
# only C and D and NOT a reference to the pitch module itself
del pitch
