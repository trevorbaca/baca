import abjad


class PitchArrayList(abjad.TypedList):
    r'''Pitch array list.

    ..  container:: example

        A pitch array list:

        >>> array_1 = baca.PitchArray([
        ...   [1, (2, 1), ([-2, -1.5], 2)],
        ...   [(7, 2), (6, 1), 1]])

        >>> array_2 = baca.PitchArray([
        ...   [1, 1, 1],
        ...   [1, 1, 1]])

        >>> arrays = [array_1, array_2]
        >>> arrays = baca.PitchArrayList(arrays)

        >>> abjad.f(arrays)
        baca.PitchArrayList(
            [
                baca.PitchArray(
                    rows=(
                        baca.PitchArrayRow(
                            cells=(
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    pitches=[
                                        abjad.NamedPitch("d'"),
                                        ],
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    pitches=[
                                        abjad.NamedPitch('bf'),
                                        abjad.NamedPitch('bqf'),
                                        ],
                                    width=2,
                                    ),
                                ),
                            ),
                        baca.PitchArrayRow(
                            cells=(
                                baca.PitchArrayCell(
                                    pitches=[
                                        abjad.NamedPitch("g'"),
                                        ],
                                    width=2,
                                    ),
                                baca.PitchArrayCell(
                                    pitches=[
                                        abjad.NamedPitch("fs'"),
                                        ],
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                ),
                            ),
                        ),
                    ),
                baca.PitchArray(
                    rows=(
                        baca.PitchArrayRow(
                            cells=(
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                ),
                            ),
                        baca.PitchArrayRow(
                            cells=(
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                baca.PitchArrayCell(
                                    width=1,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ]
            )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    _publish_storage_format = True

    ### PUBLIC METHODS ###

    def to_score(self):
        r'''Makes score from pitch arrays.

        ..  container:: example

            >>> array_1 = baca.PitchArray([
            ...   [1, (2, 1), ([-2, -1.5], 2)],
            ...   [(7, 2), (6, 1), 1]])

            >>> array_2 = baca.PitchArray([
            ...   [1, 1, 1],
            ...   [1, 1, 1]])

            >>> arrays = [array_1, array_2]
            >>> arrays = baca.PitchArrayList(arrays)

            >>> score = arrays.to_score()
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score <<
                    \new StaffGroup <<
                        \new Staff {
                            {
                                \time 4/8
                                r8
                                d'8
                                <bf bqf>4
                            }
                            {
                                \time 3/8
                                r8
                                r8
                                r8
                            }
                        }
                        \new Staff {
                            {
                                \time 4/8
                                g'4
                                fs'8
                                r8
                            }
                            {
                                \time 3/8
                                r8
                                r8
                                r8
                            }
                        }
                    >>
                >>

        Creates one staff per pitch-array row.

        Returns score.
        '''
        score = abjad.Score([])
        staff_group = abjad.StaffGroup([])
        score.append(staff_group)
        number_staves = self[0].depth
        staves = number_staves * abjad.Staff([])
        staff_group.extend(staves)
        for pitch_array in self:
            measures = pitch_array.to_measures()
            for staff, measure in zip(staves, measures):
                staff.append(measure)
        return score
