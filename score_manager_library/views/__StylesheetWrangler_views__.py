# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'flamingo',
            iotools.View(
                [
                    'gebiete-miscellaneous.ily (Gebiete)',
                    'meters.ily (Manifolds)',
                    'traiettorie-header.ily (Traiettorie inargentate)',
                    ]
                ),
            ),
        (
            'chocolate',
            iotools.View(
                [
                    'clean-letter-14.ily (Abjad)',
                    'clean-letter-16.ily (Abjad)',
                    ]
                ),
            ),
        ]
    )