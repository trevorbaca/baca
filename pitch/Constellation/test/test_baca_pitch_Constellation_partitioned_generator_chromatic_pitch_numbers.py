import baca


def test_baca_pitch_Constellation_partitioned_generator_chromatic_pitch_numbers_01():

    CC = baca.pitch.CC

    assert CC[0].partitioned_generator_chromatic_pitch_numbers == [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    assert CC[1].partitioned_generator_chromatic_pitch_numbers == [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
    assert CC[2].partitioned_generator_chromatic_pitch_numbers == [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
    assert CC[3].partitioned_generator_chromatic_pitch_numbers == [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    assert CC[4].partitioned_generator_chromatic_pitch_numbers == [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
    assert CC[5].partitioned_generator_chromatic_pitch_numbers == [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
    assert CC[6].partitioned_generator_chromatic_pitch_numbers == [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
    assert CC[7].partitioned_generator_chromatic_pitch_numbers == [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]
