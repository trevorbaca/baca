# -*- coding: utf-8 -*-


def replace_nested_elements_with_unary_subruns(l):
    '''Replaces positive integers in `l` with unary subruns.

    Works when `l` is a list of integers.

    Works when `l` is a list of integer lists.

    Ignores negative integers.

    ::

        >>> from baca import tools

    ::

        >>> l = [1, 2, 2, -4]
        >>> tools.replace_nested_elements_with_unary_subruns(l)
        [1, 1, 1, 1, 1, -4]

    ::

        >>> l = [[1, 3, -4], [1, 2, -2, -4]]
        >>> tools.replace_nested_elements_with_unary_subruns(l)
        [[1, 1, 1, 1, -4], [1, 1, 1, -2, -4]]

    Returns new list.
    '''
    result = []
    for element in l:
        if isinstance(element, list):
            new_sublist = []
            for x in element:
                if 0 < x:
                    new_sublist.extend(x * [1])
                else:
                    new_sublist.append(x)
            result.append(new_sublist)
        elif isinstance(element, int):
            if 0 < element:
                result.extend([1] * element)
            else:
                result.append(element)
        else:
            raise ValueError
    return result