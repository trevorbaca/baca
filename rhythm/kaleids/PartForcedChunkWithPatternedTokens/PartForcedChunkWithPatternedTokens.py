from abjad.tools import mathtools
from abjad.tools import sequencetools
from baca.rhythm.kaleids._PartForcedObjectWithPatternedTokens import _PartForcedObjectWithPatternedTokens


class PartForcedChunkWithPatternedTokens(_PartForcedObjectWithPatternedTokens):
    '''Part-forced chunk with pattern-filled tokens.
    '''

    ### PRIVATE METHODS ###

    def _force_token_parts(self, tokens, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        forced_tokens = []
        left_length = left_lengths[0]
        left = lefts[:left_length]
        right_length = right_lengths[0]
        right = rights[:right_length]
        if len(tokens) == 1:
            available_left_length = len(tokens[0])
            left_length = min([left_length, available_left_length])
            available_right_length = len(tokens[0]) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(tokens[0]) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_once_by_counts_without_overhang(
                tokens[0], [left_length, middle_length, right_length])
            left_part = self._force_token_part(left_part, left)
            middle_part = self._force_token_part(middle_part, middle)
            right_part = self._force_token_part(right_part, right)
            forced_token = left_part + middle_part + right_part
            forced_tokens.append(forced_token)
        else:
            ## first token
            available_left_length = len(tokens[0])
            left_length = min([left_length, available_left_length])
            middle_length = len(tokens[0]) - left_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            left_part, middle_part = \
                sequencetools.partition_sequence_once_by_counts_without_overhang(
                tokens[0], [left_length, middle_length])
            left_part = self._force_token_part(left_part, left)
            middle_part = self._force_token_part(middle_part, middle)
            forced_token = left_part + middle_part
            forced_tokens.append(forced_token)
            ## middle tokens
            for token in tokens[1:-1]:
                middle_part = token
                middle = len(token) * [middles[0]]
                middle_part = self._force_token_part(middle_part, middle)
                forced_token = middle_part
                forced_tokens.append(forced_token)
            ## last token:
            available_right_length = len(tokens[-1])
            right_length = min([right_length, available_right_length])
            middle_length = len(tokens[-1]) - right_length
            right = right[:right_length]
            middle = middle_length * [middles[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_once_by_counts_without_overhang(
                tokens[-1], [middle_length, right_length])
            middle_part = self._force_token_part(middle_part, middle)
            right_part = self._force_token_part(right_part, right)
            forced_token = middle_part + right_part
            forced_tokens.append(forced_token)
        unforced_weights = [mathtools.weight(x) for x in tokens]
        forced_weights = [mathtools.weight(x) for x in forced_tokens]
        assert forced_weights == unforced_weights
        return forced_tokens
