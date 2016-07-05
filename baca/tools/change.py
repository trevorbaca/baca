# -*- coding: utf-8 -*-
import abjad


def change(expr, visitor):
    r'''Changes `expr` with `visitor`.

    Returns `expr`.
    '''
    if isinstance(expr, list):
        for component in expr[:]:
            new_component = change(component, visitor)
            expr[expr.index(component)] = new_component
        return expr
    elif hasattr(expr, '_music'):
        for component in expr._music[:]:
            new_component = change(component, visitor)
            if new_component is not None:
                abjad.mutate(component).replace([new_component])
        return expr
    else:
        return visitor.visit(expr)