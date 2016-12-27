# -*- coding: utf-8 -*-
import abjad


class PitchManager(abjad.abctools.AbjadObject):
    r'''Pitch manager.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### PUBLIC METHODS ###

    @staticmethod
    def get_matching_transforms(
        segment_1,
        segment_2,
        alpha=False,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        transposition=False,
        ):
        r'''Gets transforms of `segment_1` that match `segment_2`.

        ..  container:: example

            Example segments:

            ::

                >>> items = [-2, -1, 6, 7, -1, 7]
                >>> segment_1 = pitchtools.PitchClassSegment(items=items)
                >>> show(segment_1) # doctest: +SKIP

            ::

                >>> items = [9, 2, 1, 6, 2, 6]
                >>> segment_2 = pitchtools.PitchClassSegment(items=items)
                >>> show(segment_2) # doctest: +SKIP

        ..  container:: example

            Gets matching transforms:

            ::

                >>> transforms = baca.tools.PitchManager.get_matching_transforms(
                ...     segment_1,
                ...     segment_2,
                ...     alpha=True,
                ...     inversion=True,
                ...     multiplication=True,
                ...     retrograde=True,
                ...     rotation=False,
                ...     transposition=True,
                ...     )
                >>> for operator, transform in transforms:
                ...     print(str(operator), str(transform))
                ...
                M5T11 <9, 2, 1, 6, 2, 6>
                M7T1I <9, 2, 1, 6, 2, 6>

            ::

                >>> transforms = baca.tools.PitchManager.get_matching_transforms(
                ...     segment_2,
                ...     segment_1,
                ...     alpha=True,
                ...     inversion=True,
                ...     multiplication=True,
                ...     retrograde=True,
                ...     rotation=False,
                ...     transposition=True,
                ...     )
                >>> for operator, transform in transforms:
                ...     print(str(operator), str(transform))
                ...
                M5T5 <10, 11, 6, 7, 11, 7>
                M7T7I <10, 11, 6, 7, 11, 7>

        ..  container:: example

            No matching transforms. Segments of differing lengths never
            transform into each other:

            ::

                >>> segment_2 = pitchtools.PitchClassSegment(items=[0, 1, 2])
                >>> baca.tools.PitchManager.get_matching_transforms(
                ...     segment_2,
                ...     segment_1,
                ...     alpha=True,
                ...     inversion=True,
                ...     multiplication=True,
                ...     retrograde=True,
                ...     rotation=False,
                ...     transposition=True,
                ...     )
                []

        ..  container:: example

            Returns list of pairs:

            ::

                >>> isinstance(transforms, list)
                True

        '''
        result = []
        if not len(segment_1) == len(segment_2):
            return result
        transforms = PitchManager.get_transforms(
            segment_1,
            alpha=alpha,
            inversion=inversion,
            multiplication=multiplication,
            retrograde=retrograde,
            rotation=rotation,
            transposition=transposition,
            )
        for operator, transform in transforms:
            if transform == segment_2:
                result.append((operator, transform))
        return result

    @staticmethod
    def get_transforms(
        segment,
        alpha=False,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        show_identity_operators=False,
        transposition=False,
        ):
        r'''Gets transforms of `segment`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1, 6, 7, -1, 7]
                >>> J = pitchtools.PitchClassSegment(items=items)
                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Gets identity transform of segment:

            ::

                >>> transforms = baca.tools.PitchManager.get_transforms(J)

            ::

                >>> for operator, transform in transforms:
                ...     print(str(transform))
                <10, 11, 6, 7, 11, 7>

        ..  container:: example

            Gets transpositions of segment:

            ::

                >>> transforms = baca.tools.PitchManager.get_transforms(
                ...     J,
                ...     transposition=True,
                ...     )

            ::

                >>> for i, pair in enumerate(transforms):
                ...     rank = i + 1
                ...     operator, transform = pair
                ...     transform = transform._get_padded_string()
                ...     string = '{:3}:{!s:>4} J:  {!s}'
                ...     string = string.format(rank, operator, transform)
                ...     print(string)
                  1:     J:  <10, 11,  6,  7, 11,  7>
                  2:  T1 J:  <11,  0,  7,  8,  0,  8>
                  3:  T2 J:  < 0,  1,  8,  9,  1,  9>
                  4:  T3 J:  < 1,  2,  9, 10,  2, 10>
                  5:  T4 J:  < 2,  3, 10, 11,  3, 11>
                  6:  T5 J:  < 3,  4, 11,  0,  4,  0>
                  7:  T6 J:  < 4,  5,  0,  1,  5,  1>
                  8:  T7 J:  < 5,  6,  1,  2,  6,  2>
                  9:  T8 J:  < 6,  7,  2,  3,  7,  3>
                 10:  T9 J:  < 7,  8,  3,  4,  8,  4>
                 11: T10 J:  < 8,  9,  4,  5,  9,  5>
                 12: T11 J:  < 9, 10,  5,  6, 10,  6>

        ..  container:: example

            Gets all transforms of segment (without rotation):

            ::

                >>> transforms = baca.tools.PitchManager.get_transforms(
                ...     J,
                ...     alpha=True,
                ...     inversion=True,
                ...     multiplication=True,
                ...     retrograde=True,
                ...     transposition=True,
                ...     )

            ::

                >>> for i, pair in enumerate(transforms):
                ...     rank = i + 1
                ...     operator, transform = pair
                ...     transform = transform._get_padded_string()
                ...     string = '{:3}:{!s:>10} J:  {!s}'
                ...     string = string.format(rank, operator, transform)
                ...     print(string)
                  1:           J:  <10, 11,  6,  7, 11,  7>
                  2:         R J:  < 7, 11,  7,  6, 11, 10>
                  3:        T1 J:  <11,  0,  7,  8,  0,  8>
                  4:       RT1 J:  < 8,  0,  8,  7,  0, 11>
                  5:        T2 J:  < 0,  1,  8,  9,  1,  9>
                  6:       RT2 J:  < 9,  1,  9,  8,  1,  0>
                  7:        T3 J:  < 1,  2,  9, 10,  2, 10>
                  8:       RT3 J:  <10,  2, 10,  9,  2,  1>
                  9:        T4 J:  < 2,  3, 10, 11,  3, 11>
                 10:       RT4 J:  <11,  3, 11, 10,  3,  2>
                 11:        T5 J:  < 3,  4, 11,  0,  4,  0>
                 12:       RT5 J:  < 0,  4,  0, 11,  4,  3>
                 13:        T6 J:  < 4,  5,  0,  1,  5,  1>
                 14:       RT6 J:  < 1,  5,  1,  0,  5,  4>
                 15:        T7 J:  < 5,  6,  1,  2,  6,  2>
                 16:       RT7 J:  < 2,  6,  2,  1,  6,  5>
                 17:        T8 J:  < 6,  7,  2,  3,  7,  3>
                 18:       RT8 J:  < 3,  7,  3,  2,  7,  6>
                 19:        T9 J:  < 7,  8,  3,  4,  8,  4>
                 20:       RT9 J:  < 4,  8,  4,  3,  8,  7>
                 21:       T10 J:  < 8,  9,  4,  5,  9,  5>
                 22:      RT10 J:  < 5,  9,  5,  4,  9,  8>
                 23:       T11 J:  < 9, 10,  5,  6, 10,  6>
                 24:      RT11 J:  < 6, 10,  6,  5, 10,  9>
                 25:         I J:  < 2,  1,  6,  5,  1,  5>
                 26:        RI J:  < 5,  1,  5,  6,  1,  2>
                 27:       T1I J:  < 3,  2,  7,  6,  2,  6>
                 28:      RT1I J:  < 6,  2,  6,  7,  2,  3>
                 29:       T2I J:  < 4,  3,  8,  7,  3,  7>
                 30:      RT2I J:  < 7,  3,  7,  8,  3,  4>
                 31:       T3I J:  < 5,  4,  9,  8,  4,  8>
                 32:      RT3I J:  < 8,  4,  8,  9,  4,  5>
                 33:       T4I J:  < 6,  5, 10,  9,  5,  9>
                 34:      RT4I J:  < 9,  5,  9, 10,  5,  6>
                 35:       T5I J:  < 7,  6, 11, 10,  6, 10>
                 36:      RT5I J:  <10,  6, 10, 11,  6,  7>
                 37:       T6I J:  < 8,  7,  0, 11,  7, 11>
                 38:      RT6I J:  <11,  7, 11,  0,  7,  8>
                 39:       T7I J:  < 9,  8,  1,  0,  8,  0>
                 40:      RT7I J:  < 0,  8,  0,  1,  8,  9>
                 41:       T8I J:  <10,  9,  2,  1,  9,  1>
                 42:      RT8I J:  < 1,  9,  1,  2,  9, 10>
                 43:       T9I J:  <11, 10,  3,  2, 10,  2>
                 44:      RT9I J:  < 2, 10,  2,  3, 10, 11>
                 45:      T10I J:  < 0, 11,  4,  3, 11,  3>
                 46:     RT10I J:  < 3, 11,  3,  4, 11,  0>
                 47:      T11I J:  < 1,  0,  5,  4,  0,  4>
                 48:     RT11I J:  < 4,  0,  4,  5,  0,  1>
                 49:           J:  <10, 11,  6,  7, 11,  7>
                 50:         R J:  < 7, 11,  7,  6, 11, 10>
                 51:        T1 J:  <11,  0,  7,  8,  0,  8>
                 52:       RT1 J:  < 8,  0,  8,  7,  0, 11>
                 53:        T2 J:  < 0,  1,  8,  9,  1,  9>
                 54:       RT2 J:  < 9,  1,  9,  8,  1,  0>
                 55:        T3 J:  < 1,  2,  9, 10,  2, 10>
                 56:       RT3 J:  <10,  2, 10,  9,  2,  1>
                 57:        T4 J:  < 2,  3, 10, 11,  3, 11>
                 58:       RT4 J:  <11,  3, 11, 10,  3,  2>
                 59:        T5 J:  < 3,  4, 11,  0,  4,  0>
                 60:       RT5 J:  < 0,  4,  0, 11,  4,  3>
                 61:        T6 J:  < 4,  5,  0,  1,  5,  1>
                 62:       RT6 J:  < 1,  5,  1,  0,  5,  4>
                 63:        T7 J:  < 5,  6,  1,  2,  6,  2>
                 64:       RT7 J:  < 2,  6,  2,  1,  6,  5>
                 65:        T8 J:  < 6,  7,  2,  3,  7,  3>
                 66:       RT8 J:  < 3,  7,  3,  2,  7,  6>
                 67:        T9 J:  < 7,  8,  3,  4,  8,  4>
                 68:       RT9 J:  < 4,  8,  4,  3,  8,  7>
                 69:       T10 J:  < 8,  9,  4,  5,  9,  5>
                 70:      RT10 J:  < 5,  9,  5,  4,  9,  8>
                 71:       T11 J:  < 9, 10,  5,  6, 10,  6>
                 72:      RT11 J:  < 6, 10,  6,  5, 10,  9>
                 73:         I J:  < 2,  1,  6,  5,  1,  5>
                 74:        RI J:  < 5,  1,  5,  6,  1,  2>
                 75:       T1I J:  < 3,  2,  7,  6,  2,  6>
                 76:      RT1I J:  < 6,  2,  6,  7,  2,  3>
                 77:       T2I J:  < 4,  3,  8,  7,  3,  7>
                 78:      RT2I J:  < 7,  3,  7,  8,  3,  4>
                 79:       T3I J:  < 5,  4,  9,  8,  4,  8>
                 80:      RT3I J:  < 8,  4,  8,  9,  4,  5>
                 81:       T4I J:  < 6,  5, 10,  9,  5,  9>
                 82:      RT4I J:  < 9,  5,  9, 10,  5,  6>
                 83:       T5I J:  < 7,  6, 11, 10,  6, 10>
                 84:      RT5I J:  <10,  6, 10, 11,  6,  7>
                 85:       T6I J:  < 8,  7,  0, 11,  7, 11>
                 86:      RT6I J:  <11,  7, 11,  0,  7,  8>
                 87:       T7I J:  < 9,  8,  1,  0,  8,  0>
                 88:      RT7I J:  < 0,  8,  0,  1,  8,  9>
                 89:       T8I J:  <10,  9,  2,  1,  9,  1>
                 90:      RT8I J:  < 1,  9,  1,  2,  9, 10>
                 91:       T9I J:  <11, 10,  3,  2, 10,  2>
                 92:      RT9I J:  < 2, 10,  2,  3, 10, 11>
                 93:      T10I J:  < 0, 11,  4,  3, 11,  3>
                 94:     RT10I J:  < 3, 11,  3,  4, 11,  0>
                 95:      T11I J:  < 1,  0,  5,  4,  0,  4>
                 96:     RT11I J:  < 4,  0,  4,  5,  0,  1>
                 97:        M5 J:  < 2,  7,  6, 11,  7, 11>
                 98:       RM5 J:  <11,  7, 11,  6,  7,  2>
                 99:      M5T1 J:  < 7,  0, 11,  4,  0,  4>
                100:     RM5T1 J:  < 4,  0,  4, 11,  0,  7>
                101:      M5T2 J:  < 0,  5,  4,  9,  5,  9>
                102:     RM5T2 J:  < 9,  5,  9,  4,  5,  0>
                103:      M5T3 J:  < 5, 10,  9,  2, 10,  2>
                104:     RM5T3 J:  < 2, 10,  2,  9, 10,  5>
                105:      M5T4 J:  <10,  3,  2,  7,  3,  7>
                106:     RM5T4 J:  < 7,  3,  7,  2,  3, 10>
                107:      M5T5 J:  < 3,  8,  7,  0,  8,  0>
                108:     RM5T5 J:  < 0,  8,  0,  7,  8,  3>
                109:      M5T6 J:  < 8,  1,  0,  5,  1,  5>
                110:     RM5T6 J:  < 5,  1,  5,  0,  1,  8>
                111:      M5T7 J:  < 1,  6,  5, 10,  6, 10>
                112:     RM5T7 J:  <10,  6, 10,  5,  6,  1>
                113:      M5T8 J:  < 6, 11, 10,  3, 11,  3>
                114:     RM5T8 J:  < 3, 11,  3, 10, 11,  6>
                115:      M5T9 J:  <11,  4,  3,  8,  4,  8>
                116:     RM5T9 J:  < 8,  4,  8,  3,  4, 11>
                117:     M5T10 J:  < 4,  9,  8,  1,  9,  1>
                118:    RM5T10 J:  < 1,  9,  1,  8,  9,  4>
                119:     M5T11 J:  < 9,  2,  1,  6,  2,  6>
                120:    RM5T11 J:  < 6,  2,  6,  1,  2,  9>
                121:       M5I J:  <10,  5,  6,  1,  5,  1>
                122:      RM5I J:  < 1,  5,  1,  6,  5, 10>
                123:     M5T1I J:  < 3, 10, 11,  6, 10,  6>
                124:    RM5T1I J:  < 6, 10,  6, 11, 10,  3>
                125:     M5T2I J:  < 8,  3,  4, 11,  3, 11>
                126:    RM5T2I J:  <11,  3, 11,  4,  3,  8>
                127:     M5T3I J:  < 1,  8,  9,  4,  8,  4>
                128:    RM5T3I J:  < 4,  8,  4,  9,  8,  1>
                129:     M5T4I J:  < 6,  1,  2,  9,  1,  9>
                130:    RM5T4I J:  < 9,  1,  9,  2,  1,  6>
                131:     M5T5I J:  <11,  6,  7,  2,  6,  2>
                132:    RM5T5I J:  < 2,  6,  2,  7,  6, 11>
                133:     M5T6I J:  < 4, 11,  0,  7, 11,  7>
                134:    RM5T6I J:  < 7, 11,  7,  0, 11,  4>
                135:     M5T7I J:  < 9,  4,  5,  0,  4,  0>
                136:    RM5T7I J:  < 0,  4,  0,  5,  4,  9>
                137:     M5T8I J:  < 2,  9, 10,  5,  9,  5>
                138:    RM5T8I J:  < 5,  9,  5, 10,  9,  2>
                139:     M5T9I J:  < 7,  2,  3, 10,  2, 10>
                140:    RM5T9I J:  <10,  2, 10,  3,  2,  7>
                141:    M5T10I J:  < 0,  7,  8,  3,  7,  3>
                142:   RM5T10I J:  < 3,  7,  3,  8,  7,  0>
                143:    M5T11I J:  < 5,  0,  1,  8,  0,  8>
                144:   RM5T11I J:  < 8,  0,  8,  1,  0,  5>
                145:        M7 J:  <10,  5,  6,  1,  5,  1>
                146:       RM7 J:  < 1,  5,  1,  6,  5, 10>
                147:      M7T1 J:  < 5,  0,  1,  8,  0,  8>
                148:     RM7T1 J:  < 8,  0,  8,  1,  0,  5>
                149:      M7T2 J:  < 0,  7,  8,  3,  7,  3>
                150:     RM7T2 J:  < 3,  7,  3,  8,  7,  0>
                151:      M7T3 J:  < 7,  2,  3, 10,  2, 10>
                152:     RM7T3 J:  <10,  2, 10,  3,  2,  7>
                153:      M7T4 J:  < 2,  9, 10,  5,  9,  5>
                154:     RM7T4 J:  < 5,  9,  5, 10,  9,  2>
                155:      M7T5 J:  < 9,  4,  5,  0,  4,  0>
                156:     RM7T5 J:  < 0,  4,  0,  5,  4,  9>
                157:      M7T6 J:  < 4, 11,  0,  7, 11,  7>
                158:     RM7T6 J:  < 7, 11,  7,  0, 11,  4>
                159:      M7T7 J:  <11,  6,  7,  2,  6,  2>
                160:     RM7T7 J:  < 2,  6,  2,  7,  6, 11>
                161:      M7T8 J:  < 6,  1,  2,  9,  1,  9>
                162:     RM7T8 J:  < 9,  1,  9,  2,  1,  6>
                163:      M7T9 J:  < 1,  8,  9,  4,  8,  4>
                164:     RM7T9 J:  < 4,  8,  4,  9,  8,  1>
                165:     M7T10 J:  < 8,  3,  4, 11,  3, 11>
                166:    RM7T10 J:  <11,  3, 11,  4,  3,  8>
                167:     M7T11 J:  < 3, 10, 11,  6, 10,  6>
                168:    RM7T11 J:  < 6, 10,  6, 11, 10,  3>
                169:       M7I J:  < 2,  7,  6, 11,  7, 11>
                170:      RM7I J:  <11,  7, 11,  6,  7,  2>
                171:     M7T1I J:  < 9,  2,  1,  6,  2,  6>
                172:    RM7T1I J:  < 6,  2,  6,  1,  2,  9>
                173:     M7T2I J:  < 4,  9,  8,  1,  9,  1>
                174:    RM7T2I J:  < 1,  9,  1,  8,  9,  4>
                175:     M7T3I J:  <11,  4,  3,  8,  4,  8>
                176:    RM7T3I J:  < 8,  4,  8,  3,  4, 11>
                177:     M7T4I J:  < 6, 11, 10,  3, 11,  3>
                178:    RM7T4I J:  < 3, 11,  3, 10, 11,  6>
                179:     M7T5I J:  < 1,  6,  5, 10,  6, 10>
                180:    RM7T5I J:  <10,  6, 10,  5,  6,  1>
                181:     M7T6I J:  < 8,  1,  0,  5,  1,  5>
                182:    RM7T6I J:  < 5,  1,  5,  0,  1,  8>
                183:     M7T7I J:  < 3,  8,  7,  0,  8,  0>
                184:    RM7T7I J:  < 0,  8,  0,  7,  8,  3>
                185:     M7T8I J:  <10,  3,  2,  7,  3,  7>
                186:    RM7T8I J:  < 7,  3,  7,  2,  3, 10>
                187:     M7T9I J:  < 5, 10,  9,  2, 10,  2>
                188:    RM7T9I J:  < 2, 10,  2,  9, 10,  5>
                189:    M7T10I J:  < 0,  5,  4,  9,  5,  9>
                190:   RM7T10I J:  < 9,  5,  9,  4,  5,  0>
                191:    M7T11I J:  < 7,  0, 11,  4,  0,  4>
                192:   RM7T11I J:  < 4,  0,  4, 11,  0,  7>
                193:       M11 J:  < 2,  1,  6,  5,  1,  5>
                194:      RM11 J:  < 5,  1,  5,  6,  1,  2>
                195:     M11T1 J:  < 1,  0,  5,  4,  0,  4>
                196:    RM11T1 J:  < 4,  0,  4,  5,  0,  1>
                197:     M11T2 J:  < 0, 11,  4,  3, 11,  3>
                198:    RM11T2 J:  < 3, 11,  3,  4, 11,  0>
                199:     M11T3 J:  <11, 10,  3,  2, 10,  2>
                200:    RM11T3 J:  < 2, 10,  2,  3, 10, 11>
                201:     M11T4 J:  <10,  9,  2,  1,  9,  1>
                202:    RM11T4 J:  < 1,  9,  1,  2,  9, 10>
                203:     M11T5 J:  < 9,  8,  1,  0,  8,  0>
                204:    RM11T5 J:  < 0,  8,  0,  1,  8,  9>
                205:     M11T6 J:  < 8,  7,  0, 11,  7, 11>
                206:    RM11T6 J:  <11,  7, 11,  0,  7,  8>
                207:     M11T7 J:  < 7,  6, 11, 10,  6, 10>
                208:    RM11T7 J:  <10,  6, 10, 11,  6,  7>
                209:     M11T8 J:  < 6,  5, 10,  9,  5,  9>
                210:    RM11T8 J:  < 9,  5,  9, 10,  5,  6>
                211:     M11T9 J:  < 5,  4,  9,  8,  4,  8>
                212:    RM11T9 J:  < 8,  4,  8,  9,  4,  5>
                213:    M11T10 J:  < 4,  3,  8,  7,  3,  7>
                214:   RM11T10 J:  < 7,  3,  7,  8,  3,  4>
                215:    M11T11 J:  < 3,  2,  7,  6,  2,  6>
                216:   RM11T11 J:  < 6,  2,  6,  7,  2,  3>
                217:      M11I J:  <10, 11,  6,  7, 11,  7>
                218:     RM11I J:  < 7, 11,  7,  6, 11, 10>
                219:    M11T1I J:  < 9, 10,  5,  6, 10,  6>
                220:   RM11T1I J:  < 6, 10,  6,  5, 10,  9>
                221:    M11T2I J:  < 8,  9,  4,  5,  9,  5>
                222:   RM11T2I J:  < 5,  9,  5,  4,  9,  8>
                223:    M11T3I J:  < 7,  8,  3,  4,  8,  4>
                224:   RM11T3I J:  < 4,  8,  4,  3,  8,  7>
                225:    M11T4I J:  < 6,  7,  2,  3,  7,  3>
                226:   RM11T4I J:  < 3,  7,  3,  2,  7,  6>
                227:    M11T5I J:  < 5,  6,  1,  2,  6,  2>
                228:   RM11T5I J:  < 2,  6,  2,  1,  6,  5>
                229:    M11T6I J:  < 4,  5,  0,  1,  5,  1>
                230:   RM11T6I J:  < 1,  5,  1,  0,  5,  4>
                231:    M11T7I J:  < 3,  4, 11,  0,  4,  0>
                232:   RM11T7I J:  < 0,  4,  0, 11,  4,  3>
                233:    M11T8I J:  < 2,  3, 10, 11,  3, 11>
                234:   RM11T8I J:  <11,  3, 11, 10,  3,  2>
                235:    M11T9I J:  < 1,  2,  9, 10,  2, 10>
                236:   RM11T9I J:  <10,  2, 10,  9,  2,  1>
                237:   M11T10I J:  < 0,  1,  8,  9,  1,  9>
                238:  RM11T10I J:  < 9,  1,  9,  8,  1,  0>
                239:   M11T11I J:  <11,  0,  7,  8,  0,  8>
                240:  RM11T11I J:  < 8,  0,  8,  7,  0, 11>
                241:         A J:  <11, 10,  7,  6, 10,  6>
                242:        RA J:  < 6, 10,  6,  7, 10, 11>
                243:       AT1 J:  <10,  1,  6,  9,  1,  9>
                244:      RAT1 J:  < 9,  1,  9,  6,  1, 10>
                245:       AT2 J:  < 1,  0,  9,  8,  0,  8>
                246:      RAT2 J:  < 8,  0,  8,  9,  0,  1>
                247:       AT3 J:  < 0,  3,  8, 11,  3, 11>
                248:      RAT3 J:  <11,  3, 11,  8,  3,  0>
                249:       AT4 J:  < 3,  2, 11, 10,  2, 10>
                250:      RAT4 J:  <10,  2, 10, 11,  2,  3>
                251:       AT5 J:  < 2,  5, 10,  1,  5,  1>
                252:      RAT5 J:  < 1,  5,  1, 10,  5,  2>
                253:       AT6 J:  < 5,  4,  1,  0,  4,  0>
                254:      RAT6 J:  < 0,  4,  0,  1,  4,  5>
                255:       AT7 J:  < 4,  7,  0,  3,  7,  3>
                256:      RAT7 J:  < 3,  7,  3,  0,  7,  4>
                257:       AT8 J:  < 7,  6,  3,  2,  6,  2>
                258:      RAT8 J:  < 2,  6,  2,  3,  6,  7>
                259:       AT9 J:  < 6,  9,  2,  5,  9,  5>
                260:      RAT9 J:  < 5,  9,  5,  2,  9,  6>
                261:      AT10 J:  < 9,  8,  5,  4,  8,  4>
                262:     RAT10 J:  < 4,  8,  4,  5,  8,  9>
                263:      AT11 J:  < 8, 11,  4,  7, 11,  7>
                264:     RAT11 J:  < 7, 11,  7,  4, 11,  8>
                265:        AI J:  < 3,  0,  7,  4,  0,  4>
                266:       RAI J:  < 4,  0,  4,  7,  0,  3>
                267:      AT1I J:  < 2,  3,  6,  7,  3,  7>
                268:     RAT1I J:  < 7,  3,  7,  6,  3,  2>
                269:      AT2I J:  < 5,  2,  9,  6,  2,  6>
                270:     RAT2I J:  < 6,  2,  6,  9,  2,  5>
                271:      AT3I J:  < 4,  5,  8,  9,  5,  9>
                272:     RAT3I J:  < 9,  5,  9,  8,  5,  4>
                273:      AT4I J:  < 7,  4, 11,  8,  4,  8>
                274:     RAT4I J:  < 8,  4,  8, 11,  4,  7>
                275:      AT5I J:  < 6,  7, 10, 11,  7, 11>
                276:     RAT5I J:  <11,  7, 11, 10,  7,  6>
                277:      AT6I J:  < 9,  6,  1, 10,  6, 10>
                278:     RAT6I J:  <10,  6, 10,  1,  6,  9>
                279:      AT7I J:  < 8,  9,  0,  1,  9,  1>
                280:     RAT7I J:  < 1,  9,  1,  0,  9,  8>
                281:      AT8I J:  <11,  8,  3,  0,  8,  0>
                282:     RAT8I J:  < 0,  8,  0,  3,  8, 11>
                283:      AT9I J:  <10, 11,  2,  3, 11,  3>
                284:     RAT9I J:  < 3, 11,  3,  2, 11, 10>
                285:     AT10I J:  < 1, 10,  5,  2, 10,  2>
                286:    RAT10I J:  < 2, 10,  2,  5, 10,  1>
                287:     AT11I J:  < 0,  1,  4,  5,  1,  5>
                288:    RAT11I J:  < 5,  1,  5,  4,  1,  0>
                289:         A J:  <11, 10,  7,  6, 10,  6>
                290:        RA J:  < 6, 10,  6,  7, 10, 11>
                291:       AT1 J:  <10,  1,  6,  9,  1,  9>
                292:      RAT1 J:  < 9,  1,  9,  6,  1, 10>
                293:       AT2 J:  < 1,  0,  9,  8,  0,  8>
                294:      RAT2 J:  < 8,  0,  8,  9,  0,  1>
                295:       AT3 J:  < 0,  3,  8, 11,  3, 11>
                296:      RAT3 J:  <11,  3, 11,  8,  3,  0>
                297:       AT4 J:  < 3,  2, 11, 10,  2, 10>
                298:      RAT4 J:  <10,  2, 10, 11,  2,  3>
                299:       AT5 J:  < 2,  5, 10,  1,  5,  1>
                300:      RAT5 J:  < 1,  5,  1, 10,  5,  2>
                301:       AT6 J:  < 5,  4,  1,  0,  4,  0>
                302:      RAT6 J:  < 0,  4,  0,  1,  4,  5>
                303:       AT7 J:  < 4,  7,  0,  3,  7,  3>
                304:      RAT7 J:  < 3,  7,  3,  0,  7,  4>
                305:       AT8 J:  < 7,  6,  3,  2,  6,  2>
                306:      RAT8 J:  < 2,  6,  2,  3,  6,  7>
                307:       AT9 J:  < 6,  9,  2,  5,  9,  5>
                308:      RAT9 J:  < 5,  9,  5,  2,  9,  6>
                309:      AT10 J:  < 9,  8,  5,  4,  8,  4>
                310:     RAT10 J:  < 4,  8,  4,  5,  8,  9>
                311:      AT11 J:  < 8, 11,  4,  7, 11,  7>
                312:     RAT11 J:  < 7, 11,  7,  4, 11,  8>
                313:        AI J:  < 3,  0,  7,  4,  0,  4>
                314:       RAI J:  < 4,  0,  4,  7,  0,  3>
                315:      AT1I J:  < 2,  3,  6,  7,  3,  7>
                316:     RAT1I J:  < 7,  3,  7,  6,  3,  2>
                317:      AT2I J:  < 5,  2,  9,  6,  2,  6>
                318:     RAT2I J:  < 6,  2,  6,  9,  2,  5>
                319:      AT3I J:  < 4,  5,  8,  9,  5,  9>
                320:     RAT3I J:  < 9,  5,  9,  8,  5,  4>
                321:      AT4I J:  < 7,  4, 11,  8,  4,  8>
                322:     RAT4I J:  < 8,  4,  8, 11,  4,  7>
                323:      AT5I J:  < 6,  7, 10, 11,  7, 11>
                324:     RAT5I J:  <11,  7, 11, 10,  7,  6>
                325:      AT6I J:  < 9,  6,  1, 10,  6, 10>
                326:     RAT6I J:  <10,  6, 10,  1,  6,  9>
                327:      AT7I J:  < 8,  9,  0,  1,  9,  1>
                328:     RAT7I J:  < 1,  9,  1,  0,  9,  8>
                329:      AT8I J:  <11,  8,  3,  0,  8,  0>
                330:     RAT8I J:  < 0,  8,  0,  3,  8, 11>
                331:      AT9I J:  <10, 11,  2,  3, 11,  3>
                332:     RAT9I J:  < 3, 11,  3,  2, 11, 10>
                333:     AT10I J:  < 1, 10,  5,  2, 10,  2>
                334:    RAT10I J:  < 2, 10,  2,  5, 10,  1>
                335:     AT11I J:  < 0,  1,  4,  5,  1,  5>
                336:    RAT11I J:  < 5,  1,  5,  4,  1,  0>
                337:       AM5 J:  < 3,  6,  7, 10,  6, 10>
                338:      RAM5 J:  <10,  6, 10,  7,  6,  3>
                339:     AM5T1 J:  < 6,  1, 10,  5,  1,  5>
                340:    RAM5T1 J:  < 5,  1,  5, 10,  1,  6>
                341:     AM5T2 J:  < 1,  4,  5,  8,  4,  8>
                342:    RAM5T2 J:  < 8,  4,  8,  5,  4,  1>
                343:     AM5T3 J:  < 4, 11,  8,  3, 11,  3>
                344:    RAM5T3 J:  < 3, 11,  3,  8, 11,  4>
                345:     AM5T4 J:  <11,  2,  3,  6,  2,  6>
                346:    RAM5T4 J:  < 6,  2,  6,  3,  2, 11>
                347:     AM5T5 J:  < 2,  9,  6,  1,  9,  1>
                348:    RAM5T5 J:  < 1,  9,  1,  6,  9,  2>
                349:     AM5T6 J:  < 9,  0,  1,  4,  0,  4>
                350:    RAM5T6 J:  < 4,  0,  4,  1,  0,  9>
                351:     AM5T7 J:  < 0,  7,  4, 11,  7, 11>
                352:    RAM5T7 J:  <11,  7, 11,  4,  7,  0>
                353:     AM5T8 J:  < 7, 10, 11,  2, 10,  2>
                354:    RAM5T8 J:  < 2, 10,  2, 11, 10,  7>
                355:     AM5T9 J:  <10,  5,  2,  9,  5,  9>
                356:    RAM5T9 J:  < 9,  5,  9,  2,  5, 10>
                357:    AM5T10 J:  < 5,  8,  9,  0,  8,  0>
                358:   RAM5T10 J:  < 0,  8,  0,  9,  8,  5>
                359:    AM5T11 J:  < 8,  3,  0,  7,  3,  7>
                360:   RAM5T11 J:  < 7,  3,  7,  0,  3,  8>
                361:      AM5I J:  <11,  4,  7,  0,  4,  0>
                362:     RAM5I J:  < 0,  4,  0,  7,  4, 11>
                363:    AM5T1I J:  < 2, 11, 10,  7, 11,  7>
                364:   RAM5T1I J:  < 7, 11,  7, 10, 11,  2>
                365:    AM5T2I J:  < 9,  2,  5, 10,  2, 10>
                366:   RAM5T2I J:  <10,  2, 10,  5,  2,  9>
                367:    AM5T3I J:  < 0,  9,  8,  5,  9,  5>
                368:   RAM5T3I J:  < 5,  9,  5,  8,  9,  0>
                369:    AM5T4I J:  < 7,  0,  3,  8,  0,  8>
                370:   RAM5T4I J:  < 8,  0,  8,  3,  0,  7>
                371:    AM5T5I J:  <10,  7,  6,  3,  7,  3>
                372:   RAM5T5I J:  < 3,  7,  3,  6,  7, 10>
                373:    AM5T6I J:  < 5, 10,  1,  6, 10,  6>
                374:   RAM5T6I J:  < 6, 10,  6,  1, 10,  5>
                375:    AM5T7I J:  < 8,  5,  4,  1,  5,  1>
                376:   RAM5T7I J:  < 1,  5,  1,  4,  5,  8>
                377:    AM5T8I J:  < 3,  8, 11,  4,  8,  4>
                378:   RAM5T8I J:  < 4,  8,  4, 11,  8,  3>
                379:    AM5T9I J:  < 6,  3,  2, 11,  3, 11>
                380:   RAM5T9I J:  <11,  3, 11,  2,  3,  6>
                381:   AM5T10I J:  < 1,  6,  9,  2,  6,  2>
                382:  RAM5T10I J:  < 2,  6,  2,  9,  6,  1>
                383:   AM5T11I J:  < 4,  1,  0,  9,  1,  9>
                384:  RAM5T11I J:  < 9,  1,  9,  0,  1,  4>
                385:       AM7 J:  <11,  4,  7,  0,  4,  0>
                386:      RAM7 J:  < 0,  4,  0,  7,  4, 11>
                387:     AM7T1 J:  < 4,  1,  0,  9,  1,  9>
                388:    RAM7T1 J:  < 9,  1,  9,  0,  1,  4>
                389:     AM7T2 J:  < 1,  6,  9,  2,  6,  2>
                390:    RAM7T2 J:  < 2,  6,  2,  9,  6,  1>
                391:     AM7T3 J:  < 6,  3,  2, 11,  3, 11>
                392:    RAM7T3 J:  <11,  3, 11,  2,  3,  6>
                393:     AM7T4 J:  < 3,  8, 11,  4,  8,  4>
                394:    RAM7T4 J:  < 4,  8,  4, 11,  8,  3>
                395:     AM7T5 J:  < 8,  5,  4,  1,  5,  1>
                396:    RAM7T5 J:  < 1,  5,  1,  4,  5,  8>
                397:     AM7T6 J:  < 5, 10,  1,  6, 10,  6>
                398:    RAM7T6 J:  < 6, 10,  6,  1, 10,  5>
                399:     AM7T7 J:  <10,  7,  6,  3,  7,  3>
                400:    RAM7T7 J:  < 3,  7,  3,  6,  7, 10>
                401:     AM7T8 J:  < 7,  0,  3,  8,  0,  8>
                402:    RAM7T8 J:  < 8,  0,  8,  3,  0,  7>
                403:     AM7T9 J:  < 0,  9,  8,  5,  9,  5>
                404:    RAM7T9 J:  < 5,  9,  5,  8,  9,  0>
                405:    AM7T10 J:  < 9,  2,  5, 10,  2, 10>
                406:   RAM7T10 J:  <10,  2, 10,  5,  2,  9>
                407:    AM7T11 J:  < 2, 11, 10,  7, 11,  7>
                408:   RAM7T11 J:  < 7, 11,  7, 10, 11,  2>
                409:      AM7I J:  < 3,  6,  7, 10,  6, 10>
                410:     RAM7I J:  <10,  6, 10,  7,  6,  3>
                411:    AM7T1I J:  < 8,  3,  0,  7,  3,  7>
                412:   RAM7T1I J:  < 7,  3,  7,  0,  3,  8>
                413:    AM7T2I J:  < 5,  8,  9,  0,  8,  0>
                414:   RAM7T2I J:  < 0,  8,  0,  9,  8,  5>
                415:    AM7T3I J:  <10,  5,  2,  9,  5,  9>
                416:   RAM7T3I J:  < 9,  5,  9,  2,  5, 10>
                417:    AM7T4I J:  < 7, 10, 11,  2, 10,  2>
                418:   RAM7T4I J:  < 2, 10,  2, 11, 10,  7>
                419:    AM7T5I J:  < 0,  7,  4, 11,  7, 11>
                420:   RAM7T5I J:  <11,  7, 11,  4,  7,  0>
                421:    AM7T6I J:  < 9,  0,  1,  4,  0,  4>
                422:   RAM7T6I J:  < 4,  0,  4,  1,  0,  9>
                423:    AM7T7I J:  < 2,  9,  6,  1,  9,  1>
                424:   RAM7T7I J:  < 1,  9,  1,  6,  9,  2>
                425:    AM7T8I J:  <11,  2,  3,  6,  2,  6>
                426:   RAM7T8I J:  < 6,  2,  6,  3,  2, 11>
                427:    AM7T9I J:  < 4, 11,  8,  3, 11,  3>
                428:   RAM7T9I J:  < 3, 11,  3,  8, 11,  4>
                429:   AM7T10I J:  < 1,  4,  5,  8,  4,  8>
                430:  RAM7T10I J:  < 8,  4,  8,  5,  4,  1>
                431:   AM7T11I J:  < 6,  1, 10,  5,  1,  5>
                432:  RAM7T11I J:  < 5,  1,  5, 10,  1,  6>
                433:      AM11 J:  < 3,  0,  7,  4,  0,  4>
                434:     RAM11 J:  < 4,  0,  4,  7,  0,  3>
                435:    AM11T1 J:  < 0,  1,  4,  5,  1,  5>
                436:   RAM11T1 J:  < 5,  1,  5,  4,  1,  0>
                437:    AM11T2 J:  < 1, 10,  5,  2, 10,  2>
                438:   RAM11T2 J:  < 2, 10,  2,  5, 10,  1>
                439:    AM11T3 J:  <10, 11,  2,  3, 11,  3>
                440:   RAM11T3 J:  < 3, 11,  3,  2, 11, 10>
                441:    AM11T4 J:  <11,  8,  3,  0,  8,  0>
                442:   RAM11T4 J:  < 0,  8,  0,  3,  8, 11>
                443:    AM11T5 J:  < 8,  9,  0,  1,  9,  1>
                444:   RAM11T5 J:  < 1,  9,  1,  0,  9,  8>
                445:    AM11T6 J:  < 9,  6,  1, 10,  6, 10>
                446:   RAM11T6 J:  <10,  6, 10,  1,  6,  9>
                447:    AM11T7 J:  < 6,  7, 10, 11,  7, 11>
                448:   RAM11T7 J:  <11,  7, 11, 10,  7,  6>
                449:    AM11T8 J:  < 7,  4, 11,  8,  4,  8>
                450:   RAM11T8 J:  < 8,  4,  8, 11,  4,  7>
                451:    AM11T9 J:  < 4,  5,  8,  9,  5,  9>
                452:   RAM11T9 J:  < 9,  5,  9,  8,  5,  4>
                453:   AM11T10 J:  < 5,  2,  9,  6,  2,  6>
                454:  RAM11T10 J:  < 6,  2,  6,  9,  2,  5>
                455:   AM11T11 J:  < 2,  3,  6,  7,  3,  7>
                456:  RAM11T11 J:  < 7,  3,  7,  6,  3,  2>
                457:     AM11I J:  <11, 10,  7,  6, 10,  6>
                458:    RAM11I J:  < 6, 10,  6,  7, 10, 11>
                459:   AM11T1I J:  < 8, 11,  4,  7, 11,  7>
                460:  RAM11T1I J:  < 7, 11,  7,  4, 11,  8>
                461:   AM11T2I J:  < 9,  8,  5,  4,  8,  4>
                462:  RAM11T2I J:  < 4,  8,  4,  5,  8,  9>
                463:   AM11T3I J:  < 6,  9,  2,  5,  9,  5>
                464:  RAM11T3I J:  < 5,  9,  5,  2,  9,  6>
                465:   AM11T4I J:  < 7,  6,  3,  2,  6,  2>
                466:  RAM11T4I J:  < 2,  6,  2,  3,  6,  7>
                467:   AM11T5I J:  < 4,  7,  0,  3,  7,  3>
                468:  RAM11T5I J:  < 3,  7,  3,  0,  7,  4>
                469:   AM11T6I J:  < 5,  4,  1,  0,  4,  0>
                470:  RAM11T6I J:  < 0,  4,  0,  1,  4,  5>
                471:   AM11T7I J:  < 2,  5, 10,  1,  5,  1>
                472:  RAM11T7I J:  < 1,  5,  1, 10,  5,  2>
                473:   AM11T8I J:  < 3,  2, 11, 10,  2, 10>
                474:  RAM11T8I J:  <10,  2, 10, 11,  2,  3>
                475:   AM11T9I J:  < 0,  3,  8, 11,  3, 11>
                476:  RAM11T9I J:  <11,  3, 11,  8,  3,  0>
                477:  AM11T10I J:  < 1,  0,  9,  8,  0,  8>
                478: RAM11T10I J:  < 8,  0,  8,  9,  0,  1>
                479:  AM11T11I J:  <10,  1,  6,  9,  1,  9>
                480: RAM11T11I J:  < 9,  1,  9,  6,  1, 10>


        ..  container:: example

            Gets alpha rotations of segment:

            ::

                >>> transforms = baca.tools.PitchManager.get_transforms(
                ...     J,
                ...     alpha=True,
                ...     rotation=True,
                ...     )

            ::

                >>> for i, pair in enumerate(transforms):
                ...     rank = i + 1
                ...     operator, transform = pair
                ...     transform = transform._get_padded_string()
                ...     string = '{:3}:{!s:>4} J:  {!s}'
                ...     string = string.format(rank, operator, transform)
                ...     print(string)
                  1:     J:  <10, 11,  6,  7, 11,  7>
                  2:  r1 J:  < 7, 10, 11,  6,  7, 11>
                  3:  r2 J:  <11,  7, 10, 11,  6,  7>
                  4:  r3 J:  < 7, 11,  7, 10, 11,  6>
                  5:  r4 J:  < 6,  7, 11,  7, 10, 11>
                  6:  r5 J:  <11,  6,  7, 11,  7, 10>
                  7:   A J:  <11, 10,  7,  6, 10,  6>
                  8: r1A J:  < 6, 11, 10,  7,  6, 10>
                  9: r2A J:  <10,  6, 11, 10,  7,  6>
                 10: r3A J:  < 6, 10,  6, 11, 10,  7>
                 11: r4A J:  < 7,  6, 10,  6, 11, 10>
                 12: r5A J:  <10,  7,  6, 10,  6, 11>

        ..  container:: example

            Gets alpha left-rotations of segment:

            ::

                >>> transforms = baca.tools.PitchManager.get_transforms(
                ...     J,
                ...     alpha=True,
                ...     rotation=Left,
                ...     )

            ::

                >>> for i, pair in enumerate(transforms):
                ...     rank = i + 1
                ...     operator, transform = pair
                ...     transform = transform._get_padded_string()
                ...     string = '{:3}:{!s:>5} J:  {!s}'
                ...     string = string.format(rank, operator, transform)
                ...     print(string)
                  1:      J:  <10, 11,  6,  7, 11,  7>
                  2:  r-1 J:  <11,  6,  7, 11,  7, 10>
                  3:  r-2 J:  < 6,  7, 11,  7, 10, 11>
                  4:  r-3 J:  < 7, 11,  7, 10, 11,  6>
                  5:  r-4 J:  <11,  7, 10, 11,  6,  7>
                  6:  r-5 J:  < 7, 10, 11,  6,  7, 11>
                  7:    A J:  <11, 10,  7,  6, 10,  6>
                  8: r-1A J:  <10,  7,  6, 10,  6, 11>
                  9: r-2A J:  < 7,  6, 10,  6, 11, 10>
                 10: r-3A J:  < 6, 10,  6, 11, 10,  7>
                 11: r-4A J:  <10,  6, 11, 10,  7,  6>
                 12: r-5A J:  < 6, 11, 10,  7,  6, 10>

        ..  container:: example

            Returns list of pairs:

            ::

                >>> isinstance(transforms, list)
                True

        '''
        operators = []
        if transposition:
            for n in range(12):
                operator = abjad.pitchtools.CompoundOperator()
                operator = operator.transpose(n=n)
                operators.append(operator)
        else:
            operator = abjad.pitchtools.CompoundOperator()
            operator = operator.transpose()
            operators.append(operator)
        if inversion:
            operators_ = operators[:]
            for operator in operators:
                operator_ = abjad.pitchtools.CompoundOperator()
                operator_ = operator_.invert()
                foo = list(operator_._operators)
                foo.extend(operator.operators)
                operator_._operators = tuple(foo)
                operators_.append(operator_)
            operators = operators_
        if multiplication:
            operators_ = operators[:]
            for operator in operators:
                operator_ = operator.multiply(n=1)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=5)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=7)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=11)
                operators_.append(operator_)
            operators = operators_
        if alpha:
            operators_ = operators[:]
            for operator in operators:
                operator_ = operator.alpha()
                operators_.append(operator_)
            operators = operators_
        if retrograde:
            operators_ = []
            for operator in operators:
                operators_.append(operator)
                operator_ = operator.retrograde()
                operators_.append(operator_)
            operators = operators_
        if rotation:
            operators_ = []
            for operator in operators:
                for n in range(len(segment)):
                    if rotation is Left:
                        n *= -1
                    operator_ = operator.rotate(n=n)
                    operators_.append(operator_)
            operators = operators_
        result = []
        for operator in operators:
            transform = operator(segment)
            result.append((operator, transform))
        return result
