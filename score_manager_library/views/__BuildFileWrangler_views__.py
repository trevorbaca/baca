# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'front cover',
            iotools.View(
                ['.*front-cover.pdf']
                ),
            ),
        ]
    )