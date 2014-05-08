# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


view_inventory=datastructuretools.TypedOrderedDict(
    [
        (
            'cary & sekka',
            iotools.View(
                ['\xc4\x8c\xc3\xa1ry (2006)', 'Sekka (2007)']
                ),
            ),
        (
            'examples',
            iotools.View(
                ['.*Example']
                ),
            ),
        ]
    )