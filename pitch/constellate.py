from abjad import *


def constellate(pitch_number_lists, pitch_range, flatten=True):
    '''Return outer product of octave transpositions of 
    pitch_number_lists in pitch_range.
    '''

    if not isinstance(pitch_range, pitchtools.PitchRange):
        raise TypeError('must be pitch range.')

    transposition_list = []
    for pnl in pitch_number_lists:
        transpositions = pitch_range.list_octave_transpositions(pnl)
        transposition_list.append(transpositions)

    result = sequencetools.yield_outer_product_of_sequences(transposition_list)
    result = list(result)

    if flatten:
        for i, part in enumerate(result):
            result[i] = sequencetools.flatten_sequence(part)

    for pnl in result:
        pnl.sort()

    return result