from abjad.tools import mathtools
from abjad.tools import sequencetools
from baca.rhythm.kaleids._PartForcedObjectWithPatternedTokens import _PartForcedObjectWithPatternedTokens


class PartForcedPatternedTokens(_PartForcedObjectWithPatternedTokens):
    '''Part-forced pattern-filled tokens.
    '''

    ### PRIVATE METHODS ###

    def _force_token_parts(self, tokens, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        lefts_index, rights_index = 0, 0
        forced_tokens = []
        for token_index, token in enumerate(tokens):
            left_length = left_lengths[token_index]
            left = lefts[lefts_index:lefts_index+left_length]
            lefts_index += left_length
            right_length = right_lengths[token_index]
            right = rights[rights_index:rights_index+right_length]
            rights_index += right_length
            available_left_length = len(token)
            left_length = min([left_length, available_left_length])
            available_right_length = len(token) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(token) - left_length - right_length

            left = left[:left_length]
            middle = middle_length * [middles[token_index]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_once_by_counts_without_overhang(
                token, [left_length, middle_length, right_length])
            left_part = self._force_token_part(left_part, left)
            middle_part = self._force_token_part(middle_part, middle)
            right_part = self._force_token_part(right_part, right)
            forced_token = left_part + middle_part + right_part
            forced_tokens.append(forced_token)
        unforced_weights = [mathtools.weight(x) for x in tokens]
        forced_weights = [mathtools.weight(x) for x in forced_tokens]
        assert forced_weights == unforced_weights
        return forced_tokens
