# -*- coding: utf-8 -*-
from abjad.tools import sequencetools


def partition_nested_into_inward_pointing_parts(l, target='negative'):
    '''Partitions integers in `l` into inward-pointing parts.
    
        >>> from baca import tools

    ::

        >>> l = [[1, 1, 5]]
        >>> tools.partition_nested_into_inward_pointing_parts(l)
        [[1, 1, 5]]

    ::

        >>> l = [[1, 1, -5]]
        >>> tools.partition_nested_into_inward_pointing_parts(l)
        [[1, 1, 1, -4]]

    ::

        >>> l = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
        >>> tools.partition_nested_into_inward_pointing_parts(
        ...    l, target='positive')
        [[1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

    ::

        >>> l = [[1, 1, -5]]
        >>> tools.partition_nested_into_inward_pointing_parts(
        ...    l, target='positive')
        [[1, 1, -5]]

    '''
    result = []
    if target == 'negative':
        for element in l:
            # -5 at beginning
            if element[0] == -5:
                result.append([-4, 1] + element[1:])
            # -5 at end
            elif element[-1] == -5:
                result.append(element[:-1] + [1, -4])
            # -5 in middle
            elif -5 in element:
                new = []
                for x in element:
                    if x != -5:
                        new.append(x)
                    else:
                        new.append(-4)
                        new.append(1)
            # no -5
            else:
                result.append(element)
    if target == 'positive':
        for sublist in l:
            new = sublist
            # 5 at beginning
            if new[0] == 5:
                new = [4, 1] + new[1:]
            # 5 at end
            if new[-1] == 5:
                new = new[:-1] + [1, 4]
            # 5 in middle
            if 5 in new:
                new = [(4, 1) if element == 5 else element for element in new]
                new = sequencetools.flatten_sequence(new)
            result.append(new)
    return result