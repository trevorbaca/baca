from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import types


class _PartForcedObjectWithPatternedTokens(_RhythmicKaleid):
    '''Part-forced object with patterned tokens.
    '''

    def __init__(self, pattern, denominator, prolation_addenda = None,
        lefts = None, middles = None, rights = None, left_lengths = None, right_lengths = None,
        secondary_divisions = None,
        pattern_helper = None, prolation_addenda_helper = None,
        lefts_helper = None, middles_helper = None, rights_helper = None,
        left_lengths_helper = None, right_lengths_helper = None, secondary_divisions_helper = None):
        _RhythmicKaleid.__init__(self)
        prolation_addenda = self._none_to_new_list(prolation_addenda)
        lefts = self._none_to_new_list(lefts)
        middles = self._none_to_new_list(middles)
        rights = self._none_to_new_list(rights)
        left_lengths = self._none_to_new_list(left_lengths)
        right_lengths = self._none_to_new_list(right_lengths)
        secondary_divisions = self._none_to_new_list(secondary_divisions)
        pattern_helper = self._none_to_trivial_helper(pattern_helper)
        prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)
        lefts_helper = self._none_to_trivial_helper(lefts_helper)
        middles_helper = self._none_to_trivial_helper(middles_helper)
        rights_helper = self._none_to_trivial_helper(rights_helper)
        left_lengths_helper = self._none_to_trivial_helper(left_lengths_helper)
        right_lengths_helper = self._none_to_trivial_helper(right_lengths_helper)
        secondary_divisions_helper = self._none_to_trivial_helper(secondary_divisions_helper)
        assert sequencetools.all_are_integer_equivalent_numbers(pattern)
        assert mathtools.is_positive_integer_equivalent_number(denominator)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(prolation_addenda)
        assert all([x in (-1, 0, 1) for x in lefts])
        assert all([x in (-1, 0, 1) for x in middles])
        assert all([x in (-1, 0, 1) for x in rights])
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(left_lengths)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(right_lengths)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(secondary_divisions)
        assert isinstance(pattern_helper, (types.FunctionType, types.MethodType))
        assert isinstance(prolation_addenda_helper, (types.FunctionType, types.MethodType))
        assert isinstance(lefts_helper, (types.FunctionType, types.MethodType))
        assert isinstance(middles_helper, (types.FunctionType, types.MethodType))
        assert isinstance(rights_helper, (types.FunctionType, types.MethodType))
        assert isinstance(left_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(right_lengths_helper, (types.FunctionType, types.MethodType))
        self._pattern = pattern
        self._denominator = denominator
        self._prolation_addenda = prolation_addenda
        self._lefts = lefts
        self._middles = middles
        self._rights = rights
        self._left_lengths = left_lengths
        self._right_lengths = right_lengths
        self._secondary_divisions = secondary_divisions
        self._pattern_helper = pattern_helper
        self._prolation_addenda_helper = prolation_addenda_helper
        self._lefts_helper = lefts_helper
        self._middles_helper = middles_helper
        self._rights_helper = rights_helper
        self._left_lengths_helper = left_lengths_helper
        self._right_lengths_helper = right_lengths_helper
        self._secondary_divisions_helper = secondary_divisions_helper
        self._repr_signals.append(self._pattern)
        self._repr_signals.append(self._prolation_addenda)
        self._repr_signals.append(self._lefts)
        self._repr_signals.append(self._middles)
        self._repr_signals.append(self._rights)
        self._repr_signals.append(self._secondary_divisions)

    ### OVERLOADS ###

    def __call__(self, duration_tokens, seeds = None):
        duration_pairs, seeds = _RhythmicKaleid.__call__(self, duration_tokens, seeds)
        octuplet = self._prepare_input(seeds)
        pattern, prolation_addenda = octuplet[:2]
        secondary_divisions = octuplet[-1]
        signals = (pattern, prolation_addenda, secondary_divisions)
        result = self._scale_signals(duration_pairs, self._denominator, signals)
        duration_pairs, lcd, pattern, prolation_addenda, secondary_divisions = result
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        septuplet = (pattern, prolation_addenda) + octuplet[2:-1]
        #numeric_map = self._make_numeric_map(duration_pairs, septuplet)
        numeric_map = self._make_numeric_map(secondary_duration_pairs, septuplet)
        leaf_lists = self._make_leaf_lists(numeric_map, lcd)
        if not prolation_addenda:
            return leaf_lists
        else:
            #tuplets = self._make_tuplets(duration_pairs, leaf_lists)
            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
            return tuplets

    def __eq__(self, other):
        return all([
            isinstance(other, type(self)),
            self._pattern == other._pattern,
            self._denominator == other._denominator,
            self._prolation_addenda == other._prolation_addenda,
            self._lefts == other._lefts,
            self._middles == other._middles,
            self._rights == other._rights,
            self._left_lengths == other._left_lengths,
            self._right_lengths == other._right_lengths,
            self._secondary_divisions == other._secondary_divisions,
            #self._pattern_helper == other._pattern_helper,
            #self._prolation_addenda_helper == other._prolation_addenda_helper,
            #self._lefts_helper == other._lefts_helper,
            #self._middles_helper == other._middles_helper,
            #self._rights_helper == other._rights_helper,
            #self._left_lengths_helper == other._left_lengths_helper,
            #self._right_lengths_helper == other._right_lengths_helper,
            #self._secondary_divisons_helper == other._secondary_divisions_helper,
            ])    

    def __ne__(self, other):
        return self == other

    ### PRIVATE METHODS ###

    def _force_token_part(self, token_part, indicator):
        assert len(token_part) == len(indicator)
        new_token_part = []
        for number, i in zip(token_part, indicator):
            if i == -1:
                new_token_part.append(-abs(number))
            elif i == 0:
                new_token_part.append(number)
            elif i == 1:
                new_token_part.append(abs(number))
            else:
                raise ValueError
        new_token_part = type(token_part)(new_token_part)
        return new_token_part

    def _make_leaf_lists(self, numeric_map, denominator):
        leaf_lists = []
        for map_token in numeric_map:
            leaf_list = leaftools.make_leaves_from_note_value_signal(map_token, denominator)
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _make_numeric_map(self, duration_pairs, septuplet):
        pattern, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths = septuplet
        prolated_duration_pairs = self._make_prolated_duration_pairs(
            duration_pairs, prolation_addenda)
        prolated_numerators = [pair[0] for pair in prolated_duration_pairs]
        map_tokens = sequencetools.split_sequence_extended_to_weights_without_overhang(
            pattern, prolated_numerators)
        quintuplet = (lefts, middles, rights, left_lengths, right_lengths)
        forced_map_tokens = self._force_token_parts(map_tokens, quintuplet)
        numeric_map = forced_map_tokens
        return numeric_map

    def _make_prolated_duration_pairs(self, duration_pairs, prolation_addenda):
        prolated_duration_pairs = []
        for i, duration_pair in enumerate(duration_pairs):
            if not prolation_addenda:
                prolated_duration_pairs.append(duration_pair)
            else:
                prolation_addendum = prolation_addenda[i]
                prolation_addendum %= duration_pair[0]
                prolated_duration_pair = (duration_pair[0] + prolation_addendum, duration_pair[1])
                prolated_duration_pairs.append(prolated_duration_pair)
        return prolated_duration_pairs

    def _prepare_input(self, seeds):
        pattern = sequencetools.CyclicTuple(self._pattern_helper(self._pattern, seeds))
        prolation_addenda = self._prolation_addenda_helper(self._prolation_addenda, seeds)
        prolation_addenda = sequencetools.CyclicTuple(prolation_addenda)
        lefts = sequencetools.CyclicTuple(self._lefts_helper(self._lefts, seeds))
        middles = sequencetools.CyclicTuple(self._middles_helper(self._middles, seeds))
        rights = sequencetools.CyclicTuple(self._rights_helper(self._rights, seeds))
        left_lengths = sequencetools.CyclicTuple(self._left_lengths_helper(self._left_lengths, seeds))
        right_lengths = sequencetools.CyclicTuple(self._right_lengths_helper(self._right_lengths, seeds))
        secondary_divisions = self._secondary_divisions_helper(self._secondary_divisions, seeds)
        secondary_divisions = sequencetools.CyclicTuple(secondary_divisions)
        return pattern, prolation_addenda, \
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions
