# -*- coding: utf-8 -*-


def change(expr, visitor):
    r'''Changes `expr` with `visitor`.

    Returns `expr`.
    '''
    if isinstance(expr, list):
        for x in expr[:]:
            expr[expr.index(x)] = change(x, visitor)
        return expr
    elif hasattr(expr, 'music'):
        for m in expr.music[:]:
            expr.music[expr.music.index(m)] = change(m, visitor)
        return expr
    else:
        return visitor.visit(expr)