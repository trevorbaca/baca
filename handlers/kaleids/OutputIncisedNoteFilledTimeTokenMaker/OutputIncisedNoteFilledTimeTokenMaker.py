from abjad.tools.timetokentools.OutputIncisedTimeTokenMaker import OutputIncisedTimeTokenMaker


class OutputIncisedNoteFilledTimeTokenMaker(OutputIncisedTimeTokenMaker):
    '''Signal-affixed chunks with rest-filled tokens.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (middle, )
        else:
            return ()
