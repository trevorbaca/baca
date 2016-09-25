# -*- coding: utf-8 -*-
import abjad


def constellate(pitch_number_lists, pitch_range, flatten=True):
    '''Constellates `pitch_number_lists`.
    
    Returns outer product of octave transpositions of 
    `pitch_number_lists` in `pitch_range`.
    '''

    if not isinstance(pitch_range, abjad.pitchtools.PitchRange):
        message = 'must be pitch range: {!r}.'
        message = message.format(pitch_range)
        raise TypeError(message)

    transposition_list = []
    for list_ in pitch_number_lists:
        transpositions = pitch_range.list_octave_transpositions(list_)
        transposition_list.append(transpositions)

    result = abjad.sequencetools.yield_outer_product_of_sequences(
        transposition_list)
    result = list(result)

    if flatten:
        for i, part in enumerate(result):
            result[i] = abjad.sequencetools.flatten_sequence(part)

    for list_ in result:
        list_.sort()

    return result
