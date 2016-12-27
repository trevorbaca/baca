# -*- coding: utf-8 -*-
import abjad
import baca


def test_pitchtools_PitchArray_to_measures_01():

    array = baca.tools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    measures = array.to_measures()
    score = abjad.Score(abjad.Staff([]) * 2)
    score[0].append(measures[0])
    score[1].append(measures[1])

    r'''
    \new Score <<
        \new Staff {
            {
                \time 4/8
                r8
                d'8
                <bf bqf>4
            }
        }
        \new Staff {
            {
                \time 4/8
                g'4
                fs'8
                r8
            }
        }
    >>
    '''

    assert abjad.inspect_(score).is_well_formed()
    assert format(score) == abjad.stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                {
                    \time 4/8
                    r8
                    d'8
                    <bf bqf>4
                }
            }
            \new Staff {
                {
                    \time 4/8
                    g'4
                    fs'8
                    r8
                }
            }
        >>
        '''
        )
