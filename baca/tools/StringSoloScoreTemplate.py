# -*- coding: utf-8 -*-
from abjad import *


class StringSoloScoreTemplate(abctools.AbjadValueObject):
    r'''String solo score template.
    '''

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls string solo score template.

        Returns score.
        '''

        # make time signature context
        time_signature_context = scoretools.Context(
            name='TimeSignatureContext',
            context_name='TimeSignatureContext',
            )

        # make bow tablature voices and staff
        bow_tablature_rhythm_voice = Voice(
            context_name='BowTablatureRhythmVoice', 
            name='Rhythm Voice',
            )
        bow_tablature_bow_voice = Voice(
            context_name='BowTablatureBowVoice', 
            name='Bow Voice',
            )
        bow_tablature_bow_position_voice = Voice(
            context_name='BowTablatureBowPositionVoice',
            name='Bow Position Voice',
            )
        bow_tablature_dynamics_voice = Voice(
            context_name='BowTablatureDynamicsVoice', 
            name='Dynamics Voice',
            )
        bow_tablature_staff = Staff(
            context_name='BowTablatureStaff', 
            name='Bow Tablature Staff',
            )
        bow_tablature_staff.is_simultaneous = True
        bow_tablature_staff.append(bow_tablature_rhythm_voice)
        bow_tablature_staff.append(bow_tablature_bow_voice)
        bow_tablature_staff.append(bow_tablature_bow_position_voice)
        bow_tablature_staff.append(bow_tablature_dynamics_voice)

        # make lh voices and staff
        lh_voice = Voice(
            context_name='LHVoice', 
            name='LH Voice',
            )
        lh_staff = Staff(
            context_name='LHStaff', 
            name='LH Staff',
            )
        lh_staff.is_simultaneous = True
        lh_staff.append(lh_voice)
        indicatortools.Clef('bass')(lh_staff)

        # make staff group
        staff_group = scoretools.PianoStaff(
            [
            bow_tablature_staff,
            lh_staff,
            ],
            name='Traiettorie Staff Group',
            )
        
        # make score
        score = Score(
            [
            time_signature_context,
            staff_group,
            ],
            name='Traiettorie Score',
            )

        # return score
        return score