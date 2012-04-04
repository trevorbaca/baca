from abjad import *


class TwoStaffPianoScoreTemplate(object):
    '''Duplicates Abjad implementation.
    '''

    ### SPECIAL METHODS ###

    def __call__(self):

        # make treble staff
        treble_staff = Staff([])
        treble_staff.name = 'treble'
        contexttools.ClefMark('treble')(treble_staff)

        # make bass staff
        bass_staff = Staff([])
        bass_staff.name = 'bass'
        contexttools.ClefMark('bass')(bass_staff)

        # make piano staff and score
        piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])
        score = Score([])
        score.append(piano_staff)

        # return score
        return score
