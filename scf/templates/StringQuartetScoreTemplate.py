from abjad import *


class StringQuartetScoreTemplate(object):
    
    ### SPECIAL METHODS ###

    def __call__(self):

        # make first violin staff
        first_violin_staff = Staff(name='violin 1')
        contexttools.ClefMark('treble')(first_violin_staff)

        # make second violin staff
        second_violin_staff = Staff(name='violin 2')
        contexttools.ClefMark('treble')(second_violin_staff)

        # make viola staff
        viola_staff = Staff(name='viola')
        contexttools.ClefMark('alto')(viola_staff)

        # make cello staff
        cello_staff = Staff(name='cello')
        contexttools.ClefMark('bass')(cello_staff)

        # make staff group
        staff_group = scoretools.StaffGroup([
            first_violin_staff, 
            second_violin_staff,
            viola_staff,
            cello_staff,
            ])

        # make score
        score = Score([staff_group])

        # return score
        return score
