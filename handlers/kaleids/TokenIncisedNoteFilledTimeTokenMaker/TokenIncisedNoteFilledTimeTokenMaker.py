from handlers.kaleids.TokenIncisedTimeTokenMaker import TokenIncisedTimeTokenMaker


class TokenIncisedNoteFilledTimeTokenMaker(TokenIncisedTimeTokenMaker):
    '''Signal-affixed note-filled tokens.
    '''

    ### PRIVATE METHODS ###

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (middle, )
        else:
            return ()
