# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'flamingo',
            iotools.View(
                [
                    'gebiete-miscellaneous (Gebiete)',
                    'meters (Manifolds)',
                    'traiettorie-header (Traiettorie inargentate)',
                    ]
                ),
            ),
        ],
    item_class=iotools.View,
    )