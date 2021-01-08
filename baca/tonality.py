import re
import typing

import abjad


class ScaleDegree:
    """
    Scale degree.

    ..  container:: example

        >>> baca.tonality.ScaleDegree('#4')
        ScaleDegree('#4')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_accidental", "_number")

    _acceptable_numbers = tuple(range(1, 16))

    _numeral_to_number_name = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
    }

    _roman_numeral_string_to_scale_degree_number = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
    }

    _scale_degree_number_to_roman_numeral_string = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
        7: "VII",
    }

    _scale_degree_number_to_scale_degree_name = {
        1: "tonic",
        2: "superdominant",
        3: "mediant",
        4: "subdominant",
        5: "dominant",
        6: "submediant",
        7: "leading tone",
    }

    _string_regex = re.compile(r"([#|b]*)([i|I|v|V|\d]+)")

    ### INITIALIZER ###

    def __init__(self, string=1):
        assert isinstance(string, (str, int, type(self))), repr(string)
        string = str(string)
        match = self._string_regex.match(string)
        if match is None:
            raise Exception(repr(string))
        groups = match.groups()
        accidental, roman_numeral = groups
        accidental = abjad.Accidental(accidental)
        roman_numeral = roman_numeral.upper()
        try:
            number = self._roman_numeral_string_to_scale_degree_number[roman_numeral]
        except KeyError:
            number = int(roman_numeral)
        self._accidental = accidental
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a scale degree with number and
        accidental equal to those of this scale degree.

        ..  container:: example

            >>> degree_1 = baca.tonality.ScaleDegree('#4')
            >>> degree_2 = baca.tonality.ScaleDegree('#4')
            >>> degree_3 = baca.tonality.ScaleDegree(5)

            >>> degree_1 == degree_1
            True
            >>> degree_1 == degree_2
            True
            >>> degree_1 == degree_3
            False

            >>> degree_2 == degree_1
            True
            >>> degree_2 == degree_2
            True
            >>> degree_2 == degree_3
            False

            >>> degree_3 == degree_1
            False
            >>> degree_3 == degree_2
            False
            >>> degree_3 == degree_3
            True

        Returns true or false.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes scale degree.

        Returns integer.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of scale degree.

        ..  container:: example

            >>> str(baca.tonality.ScaleDegree('#4'))
            '#4'

        Returns string.
        """
        return f"{self.accidental.symbol}{self.number}"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.string]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def from_accidental_and_number(accidental, number):
        """
        Makes scale degree from ``accidental`` and ``number``.

        ..  container:: example

            >>> class_ = baca.tonality.ScaleDegree
            >>> class_.from_accidental_and_number('sharp', 4)
            ScaleDegree('#4')

        Returns new scale degree.
        """
        accidental = abjad.Accidental(accidental)
        string = f"{accidental.symbol}{number}"
        return ScaleDegree(string=string)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> baca.tonality.ScaleDegree('#4').accidental
            Accidental('sharp')

        Returns accidental.
        """
        return self._accidental

    @property
    def name(self):
        """
        Gets name.

        ..  container:: example

            >>> baca.tonality.ScaleDegree(1).name
            'tonic'
            >>> baca.tonality.ScaleDegree(2).name
            'superdominant'
            >>> baca.tonality.ScaleDegree(3).name
            'mediant'
            >>> baca.tonality.ScaleDegree(4).name
            'subdominant'
            >>> baca.tonality.ScaleDegree(5).name
            'dominant'
            >>> baca.tonality.ScaleDegree(6).name
            'submediant'
            >>> baca.tonality.ScaleDegree(7).name
            'leading tone'

        Returns string.
        """
        if self.accidental.semitones == 0:
            return self._scale_degree_number_to_scale_degree_name[self.number]
        else:
            raise NotImplementedError

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> baca.tonality.ScaleDegree('#4').number
            4

        Returns integer from 1 to 7, inclusive.
        """
        return self._number

    @property
    def roman_numeral_string(self):
        """
        Gets Roman numeral string.

        ..  container:: example

            >>> degree = baca.tonality.ScaleDegree('#4')
            >>> degree.roman_numeral_string
            'IV'

        Returns string.
        """
        string = self._scale_degree_number_to_roman_numeral_string[self.number]
        return string

    @property
    def string(self):
        """
        Gets string.

        ..  container:: example

            >>> baca.tonality.ScaleDegree('b4').string
            'b4'

            >>> baca.tonality.ScaleDegree('4').string
            '4'

            >>> baca.tonality.ScaleDegree('#4').string
            '#4'

        Returns string.
        """
        return f"{self.accidental.symbol}{self.number}"

    @property
    def title_string(self):
        """
        Gets title string.

        ..  container:: example

            >>> baca.tonality.ScaleDegree('b4').title_string
            'FlatFour'

            >>> baca.tonality.ScaleDegree('4').title_string
            'Four'

            >>> baca.tonality.ScaleDegree('#4').title_string
            'SharpFour'

        Returns string.
        """
        if not self.accidental.name == "natural":
            accidental = self.accidental.name
        else:
            accidental = ""
        number = self._numeral_to_number_name[self.number]
        return f"{accidental.title()}{number.title()}"


class Scale(abjad.PitchClassSegment):
    """
    Scale.

    ..  container:: example

        Initializes from pair:

        >>> baca.tonality.Scale(('c', 'minor'))
        Scale("c d ef f g af bf")

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_key_signature",)

    ### INITIALIZER ###

    def __init__(self, key_signature=None):
        if key_signature is None:
            key_signature = abjad.KeySignature("c", "major")
        elif isinstance(key_signature, tuple):
            key_signature = abjad.KeySignature(*key_signature)
        elif isinstance(key_signature, type(self)):
            key_signature = key_signature.key_signature
        if not isinstance(key_signature, abjad.KeySignature):
            raise Exception(key_signature)
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.named_interval_segment[:-1]:
            named_pitch_class = npcs[-1] + mdi
            npcs.append(named_pitch_class)
        abjad.PitchClassSegment.__init__(
            self, items=npcs, item_class=abjad.NamedPitchClass
        )
        self._key_signature = key_signature

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets item in scale.

        Returns pitch-class segment.
        """
        segment = abjad.PitchClassSegment(self)
        return segment.__getitem__(argument)

    ### PRIVATE PROPERTIES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return f"{letter}{mode}"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[
                str(self.key_signature.tonic),
                self.key_signature.mode.mode_name,
            ],
        )

    def _set_ascending_named_diatonic_pitches_on_logical_ties(self, argument):
        dicg = self.named_interval_class_segment
        length = len(dicg)
        octave_number = 4
        pitch = abjad.NamedPitch((self[0].name, octave_number))
        for i, logical_tie in enumerate(abjad.Selection(argument).logical_ties()):
            if hasattr(logical_tie[0], "written_pitch"):
                for note in logical_tie:
                    note.written_pitch = pitch
            elif hasattr(logical_tie[0], "written_pitches"):
                for chord in logical_tie:
                    chord.written_pitches = [pitch]
            else:
                pass
            dic = dicg[i % length]
            ascending_mdi = abjad.NamedInterval((dic.quality, dic.number))
            pitch += ascending_mdi

    ### PUBLIC PROPERTIES ###

    @property
    def dominant(self):
        """
        Gets dominant.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).dominant
            NamedPitchClass('g')

        Return pitch-class.
        """
        return self[4]

    @property
    def key_signature(self):
        """
        Gets key signature.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).key_signature
            KeySignature(NamedPitchClass('c'), Mode('minor'))

        Returns key signature.
        """
        return self._key_signature

    @property
    def leading_tone(self):
        """
        Gets leading tone.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).leading_tone
            NamedPitchClass('bf')

        Returns pitch-class.
        """
        return self[-1]

    @property
    def mediant(self):
        """
        Gets mediant.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).mediant
            NamedPitchClass('ef')

        Returns pitch-class.
        """
        return self[2]

    @property
    def named_interval_class_segment(self):
        """
        Gets named interval class segment.

        ..  container:: example

            >>> scale = baca.tonality.Scale(('c', 'minor'))
            >>> str(scale.named_interval_class_segment)
            '<+M2, +m2, +M2, +M2, +m2, +M2, +M2>'

            >>> scale = baca.tonality.Scale(('d', 'dorian'))
            >>> str(scale.named_interval_class_segment)
            '<+M2, +m2, +M2, +M2, +M2, +m2, +M2>'

        Returns interval-class segment.
        """
        dics = []
        for left, right in abjad.Sequence(self).nwise(wrapped=True):
            dic = left - right
            dics.append(dic)
        dicg = abjad.IntervalClassSegment(
            items=dics, item_class=abjad.NamedInversionEquivalentIntervalClass
        )
        return dicg

    @property
    def subdominant(self):
        """
        Gets subdominant.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).subdominant
            NamedPitchClass('f')

        Returns pitch-class.
        """
        return self[3]

    @property
    def submediant(self):
        """
        Submediate of scale.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).submediant
            NamedPitchClass('af')

        Returns pitch-class.
        """
        return self[5]

    @property
    def superdominant(self):
        """
        Gets superdominant.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).superdominant
            NamedPitchClass('d')

        Returns pitch-class.
        """
        return self[1]

    @property
    def tonic(self):
        """
        Gets tonic.

        ..  container:: example

            >>> baca.tonality.Scale(('c', 'minor')).tonic
            NamedPitchClass('c')

        Returns pitch-class.
        """
        return self[0]

    ### PUBLIC METHODS ###

    def create_named_pitch_set_in_pitch_range(self, pitch_range):
        """
        Creates named pitch-set in ``pitch_range``.

        Returns pitch-set.
        """
        if not isinstance(pitch_range, abjad.PitchRange):
            pitch_range = abjad.PitchRange(
                float(abjad.NamedPitch(pitch_range[0])),
                float(abjad.NamedPitch(pitch_range[1])),
            )
        low = pitch_range.start_pitch.octave.number
        high = pitch_range.stop_pitch.octave.number
        pitches = []
        octave = low
        while octave <= high:
            for x in self:
                pitch = abjad.NamedPitch((x.name, octave))
                if pitch_range.start_pitch <= pitch and pitch <= pitch_range.stop_pitch:
                    pitches.append(pitch)
            octave += 1
        return abjad.PitchSet(items=pitches, item_class=abjad.NamedPitch)

    @classmethod
    def from_selection(class_, selection, item_class=None, name=None):
        """
        Makes scale from ``selection``.

        Returns new scale.
        """
        raise NotImplementedError

    def named_pitch_class_to_scale_degree(self, pitch_class):
        """
        Changes named ``pitch_class`` to scale degree.

        ..  container:: example

            >>> scale = baca.tonality.Scale(('c', 'major'))
            >>> scale.named_pitch_class_to_scale_degree('c')
            ScaleDegree('1')
            >>> scale.named_pitch_class_to_scale_degree('d')
            ScaleDegree('2')
            >>> scale.named_pitch_class_to_scale_degree('e')
            ScaleDegree('3')
            >>> scale.named_pitch_class_to_scale_degree('f')
            ScaleDegree('4')
            >>> scale.named_pitch_class_to_scale_degree('g')
            ScaleDegree('5')
            >>> scale.named_pitch_class_to_scale_degree('a')
            ScaleDegree('6')
            >>> scale.named_pitch_class_to_scale_degree('b')
            ScaleDegree('7')

            >>> scale.named_pitch_class_to_scale_degree('df')
            ScaleDegree('b2')

        Returns scale degree.
        """
        foreign_pitch_class = abjad.NamedPitchClass(pitch_class)
        letter = foreign_pitch_class._get_diatonic_pc_name()
        for i, pc in enumerate(self):
            if pc._get_diatonic_pc_name() == letter:
                native_pitch_class = pc
                scale_degree_index = i
                number = scale_degree_index + 1
                break
        native_pitch = abjad.NamedPitch((native_pitch_class.name, 4))
        foreign_pitch = abjad.NamedPitch((foreign_pitch_class.name, 4))
        accidental = foreign_pitch.accidental - native_pitch.accidental
        scale_degree = ScaleDegree.from_accidental_and_number(accidental, number)
        return scale_degree

    def scale_degree_to_named_pitch_class(self, scale_degree):
        """
        Changes scale degree to named pitch-class.

        ..  container:: example

            >>> scale = baca.tonality.Scale(('c', 'major'))
            >>> scale.scale_degree_to_named_pitch_class('1')
            NamedPitchClass('c')
            >>> scale.scale_degree_to_named_pitch_class('2')
            NamedPitchClass('d')
            >>> scale.scale_degree_to_named_pitch_class('3')
            NamedPitchClass('e')
            >>> scale.scale_degree_to_named_pitch_class('4')
            NamedPitchClass('f')
            >>> scale.scale_degree_to_named_pitch_class('5')
            NamedPitchClass('g')
            >>> scale.scale_degree_to_named_pitch_class('6')
            NamedPitchClass('a')
            >>> scale.scale_degree_to_named_pitch_class('7')
            NamedPitchClass('b')

            >>> scale.scale_degree_to_named_pitch_class('b2')
            NamedPitchClass('df')

        Returns named pitch-class.
        """
        scale_degree = ScaleDegree(scale_degree)
        scale_index = (scale_degree.number - 1) % 7
        pitch_class = self[scale_index]
        pitch_class = scale_degree.accidental(pitch_class)
        return pitch_class

    def voice_scale_degrees_in_open_position(self, scale_degrees):
        r"""
        Voices ``scale_degrees`` in open position.

        ..  container:: example

            >>> scale = baca.tonality.Scale(('c', 'major'))
            >>> scale_degrees = [1, 3, 'b5', 7, '#9']
            >>> segment = scale.voice_scale_degrees_in_open_position(scale_degrees)
            >>> segment
            PitchSegment("c' e' gf' b' ds''")

        Return pitch segment.
        """
        scale_degrees = [ScaleDegree(x) for x in scale_degrees]
        pitch_classes = [
            self.scale_degree_to_named_pitch_class(x) for x in scale_degrees
        ]
        pitches = [abjad.NamedPitch(pitch_classes[0])]
        for pitch_class in pitch_classes[1:]:
            pitch = abjad.NamedPitch(pitch_class)
            while pitch < pitches[-1]:
                pitch += 12
            pitches.append(pitch)
        pitches = abjad.PitchSegment(pitches)
        return pitches


class ChordExtent:
    """
    Chord extent.

    ..  container:: example

        Initializes from number:

        >>> baca.tonality.ChordExtent(7)
        ChordExtent(7)

    ..  container:: example

        Initializes from other chord extent:

        >>> extent = baca.tonality.ChordExtent(7)
        >>> baca.tonality.ChordExtent(extent)
        ChordExtent(7)

    Defined equal to outer interval of any root-position chord.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    _acceptable_number = (5, 7, 9)

    _extent_number_to_extent_name = {5: "triad", 7: "seventh", 9: "ninth"}

    ### INITIALIZER ###

    def __init__(self, number=5):
        if isinstance(number, int):
            if number not in self._acceptable_number:
                raise ValueError(f"can not initialize extent: {number}.")
            number = number
        elif isinstance(number, type(self)):
            number = number.number
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a chord extent with number equal to that
        of this chord extent.

        ..  container:: example

            >>> extent_1 = baca.tonality.ChordExtent(5)
            >>> extent_2 = baca.tonality.ChordExtent(5)
            >>> extent_3 = baca.tonality.ChordExtent(7)

            >>> extent_1 == extent_1
            True
            >>> extent_1 == extent_2
            True
            >>> extent_1 == extent_3
            False

            >>> extent_2 == extent_1
            True
            >>> extent_2 == extent_2
            True
            >>> extent_2 == extent_3
            False

            >>> extent_3 == extent_1
            False
            >>> extent_3 == extent_2
            False
            >>> extent_3 == extent_3
            True

        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes chord extent.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.number]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self) -> str:
        """
        Gets name.

        ..  container:: example

            >>> baca.tonality.ChordExtent(5).name
            'triad'

            >>> baca.tonality.ChordExtent(7).name
            'seventh'

        """
        return self._extent_number_to_extent_name[self.number]

    @property
    def number(self) -> int:
        """
        Gets number.

        ..  container:: example

            >>> baca.tonality.ChordExtent(7).number
            7

        """
        return self._number


class ChordInversion:
    """
    Chord inversion.

    ..  container:: example

        >>> baca.tonality.ChordInversion(1)
        ChordInversion(1)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    _inversion_name_to_inversion_number = {
        "root": 0,
        "root position": 0,
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
    }

    _inversion_number_to_inversion_name = {
        0: "root position",
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
    }

    _seventh_chord_inversion_to_figured_bass_string = {
        0: "7",
        1: "6/5",
        2: "4/3",
        3: "4/2",
    }

    _triadic_inversion_to_figured_bass_string = {0: "", 1: "6", 2: "6/4"}

    ### INITIALIZER ###

    def __init__(self, number=0):
        argument = number
        if isinstance(argument, int):
            number = argument
        elif isinstance(argument, str):
            number = self._inversion_name_to_inversion_number[argument]
        else:
            raise ValueError("can not initialize chord inversion.")
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a chord inversion with number equal to
        that of this chord inversion.

        ..  container:: example

            >>> inversion_1 = baca.tonality.ChordInversion(0)
            >>> inversion_2 = baca.tonality.ChordInversion(0)
            >>> inversion_3 = baca.tonality.ChordInversion(1)

            >>> inversion_1 == inversion_1
            True
            >>> inversion_1 == inversion_2
            True
            >>> inversion_1 == inversion_3
            False

            >>> inversion_2 == inversion_1
            True
            >>> inversion_2 == inversion_2
            True
            >>> inversion_2 == inversion_3
            False

            >>> inversion_3 == inversion_1
            False
            >>> inversion_3 == inversion_2
            False
            >>> inversion_3 == inversion_3
            True

        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes chord inversion.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.number]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    ### PUBLIC METHODS ###

    def extent_to_figured_bass_string(self, extent) -> str:
        """
        Changes ``extent`` to figured bass string.

        ..  container:: example

            >>> inversion = baca.tonality.ChordInversion(0)
            >>> inversion.extent_to_figured_bass_string(5)
            ''
            >>> inversion.extent_to_figured_bass_string(7)
            '7'

            >>> inversion = baca.tonality.ChordInversion(1)
            >>> inversion.extent_to_figured_bass_string(5)
            '6'
            >>> inversion.extent_to_figured_bass_string(7)
            '6/5'

            >>> inversion = baca.tonality.ChordInversion(2)
            >>> inversion.extent_to_figured_bass_string(5)
            '6/4'
            >>> inversion.extent_to_figured_bass_string(7)
            '4/3'

            >>> inversion = baca.tonality.ChordInversion(3)
            >>> inversion.extent_to_figured_bass_string(7)
            '4/2'

        """
        if extent == 5:
            return self._triadic_inversion_to_figured_bass_string[self.number]
        elif extent == 7:
            return self._seventh_chord_inversion_to_figured_bass_string[self.number]
        else:
            raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def name(self) -> str:
        """
        Gets name.

        ..  container:: example

            >>> baca.tonality.ChordInversion(0).name
            'root position'

            >>> baca.tonality.ChordInversion(1).name
            'first'

            >>> baca.tonality.ChordInversion(2).name
            'second'

        """
        return self._inversion_number_to_inversion_name[self.number]

    @property
    def number(self) -> int:
        """
        Number of chord inversion.

        ..  container:: example

            >>> baca.tonality.ChordInversion(0).number
            0

            >>> baca.tonality.ChordInversion(1).number
            1

            >>> baca.tonality.ChordInversion(2).number
            2

        """
        return self._number

    @property
    def title(self) -> str:
        """
        Title of chord inversion.

        ..  container:: example

            >>> baca.tonality.ChordInversion(0).title
            'RootPosition'

            >>> baca.tonality.ChordInversion(1).title
            'FirstInversion'

            >>> baca.tonality.ChordInversion(2).title
            'SecondInversion'

        """
        name = self._inversion_number_to_inversion_name[self.number]
        if name == "root position":
            return "RootPosition"
        return f"{name.title()}Inversion"


class ChordQuality:
    """
    Chord quality.

    ..  container:: example

        Initializes from string:

        >>> baca.tonality.ChordQuality("major")
        ChordQuality('major')

    ..  container:: example

        Initializes from other chord quality:

        >>> quality = baca.tonality.ChordQuality("major")
        >>> baca.tonality.ChordQuality(quality)
        ChordQuality('major')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_quality_string",)

    _acceptable_quality_strings = (
        "augmented",
        "diminished",
        "dominant",
        "half diminished",
        "major",
        "minor",
    )

    _uppercase_quality_strings = ("augmented", "dominant", "major")

    ### INITIALIZER ###

    def __init__(self, quality_string="major"):
        quality_string = str(quality_string)
        if quality_string not in self._acceptable_quality_strings:
            raise ValueError(f"can not initialize chord quality: {quality_string!r}.")
        self._quality_string = quality_string

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a chord quality with quality string
        equal to that of this chord quality.

        ..  container:: example

            >>> quality_1 = baca.tonality.ChordQuality("major")
            >>> quality_2 = baca.tonality.ChordQuality("major")
            >>> quality_3 = baca.tonality.ChordQuality("dominant")

            >>> quality_1 == quality_1
            True
            >>> quality_1 == quality_2
            True
            >>> quality_1 == quality_3
            False

            >>> quality_2 == quality_1
            True
            >>> quality_2 == quality_2
            True
            >>> quality_2 == quality_3
            False

            >>> quality_3 == quality_1
            False
            >>> quality_3 == quality_2
            False
            >>> quality_3 == quality_3
            True

        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes chord quality.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        """
        Gets string representation of chord quality.

        ..  container:: example

            >>> quality = baca.tonality.ChordQuality("major")
            >>> str(quality)
            'major'

        """
        return self.quality_string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.quality_string]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def is_uppercase(self) -> bool:
        """
        Is true when chord quality is uppercase.

        ..  container:: example

            >>> baca.tonality.ChordQuality("major").is_uppercase
            True

            >>> baca.tonality.ChordQuality("minor").is_uppercase
            False

        """
        return self.quality_string in self._uppercase_quality_strings

    @property
    def quality_string(self) -> str:
        """
        Gets quality string.

        ..  container:: example

            >>> baca.tonality.ChordQuality("major").quality_string
            'major'

            >>> baca.tonality.ChordQuality("minor").quality_string
            'minor'

        """
        return self._quality_string


class ChordSuspension:
    """
    Chord suspension.

    ..  container:: example

        Initializes from numbers:

        >>> baca.tonality.ChordSuspension("4-b3")
        ChordSuspension('4-b3')

    ..  container:: example

        Initializes from other suspension:

        >>> suspension = baca.tonality.ChordSuspension("4-3")
        >>> baca.tonality.ChordSuspension(suspension)
        ChordSuspension('4-3')

    9-8, 7-6, 4-3, 2-1 and other types of suspension typical of, for example,
    the Bach chorales.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_start", "_stop")

    _symbol_regex = re.compile(r"([#|b]?\d+)-([#|b]?\d+)")

    ### INITIALIZER ###

    def __init__(self, figured_bass_string="4-3"):
        if isinstance(figured_bass_string, type(self)):
            figured_bass_string = figured_bass_string.figured_bass_string
        start, stop = self._initialize_by_symbol(figured_bass_string)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a chord suspension when start and stop
        equal to those of this chord suspension.

        ..  container:: example

            >>> suspension_1 = baca.tonality.ChordSuspension("4-3")
            >>> suspension_2 = baca.tonality.ChordSuspension("4-3")
            >>> suspension_3 = baca.tonality.ChordSuspension("2-1")

            >>> suspension_1 == suspension_1
            True
            >>> suspension_1 == suspension_2
            True
            >>> suspension_1 == suspension_3
            False


            >>> suspension_2 == suspension_1
            True
            >>> suspension_2 == suspension_2
            True
            >>> suspension_2 == suspension_3
            False


            >>> suspension_3 == suspension_1
            False
            >>> suspension_3 == suspension_2
            False
            >>> suspension_3 == suspension_3
            True

        Returns true or false.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes chord suspension.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        """
        Gets string representation of chord suspension.
        """
        if self.start is not None and self.stop is not None:
            return f"{self.start!s}-{self.stop!s}"
        else:
            return ""

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.figured_bass_string]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    def _initialize_by_pair(self, pair):
        start, stop = pair
        return self._initialize_by_start_and_stop(start, stop)

    def _initialize_by_reference(self, chord_suspension):
        start, stop = chord_suspension.start, chord_suspension.stop
        return self._initialize_by_start_and_stop(start, stop)

    def _initialize_by_start_and_stop(self, start, stop):
        start = ScaleDegree(start)
        stop = ScaleDegree(stop)
        return start, stop

    def _initialize_by_symbol(self, symbol):
        groups = self._symbol_regex.match(symbol).groups()
        start, stop = groups
        start = ScaleDegree(start)
        stop = ScaleDegree(stop)
        return start, stop

    def _initialize_empty(self):
        return None, None

    ### PUBLIC PROPERTIES ###

    @property
    def chord_name(self) -> str:
        """
        Gets chord name.

        ..  container:: example

            >>> baca.tonality.ChordSuspension("4-b3").chord_name
            'sus4'

            >>> baca.tonality.ChordSuspension("b2-1").chord_name
            'susb2'

        """
        return f"sus{self.start!s}"

    @property
    def figured_bass_pair(self) -> typing.Tuple[str, str]:
        """
        Gets figured bass pair.

        ..  container:: example

            >>> baca.tonality.ChordSuspension("4-b3").figured_bass_pair
            ('4', 'b3')

            >>> baca.tonality.ChordSuspension("b2-1").figured_bass_pair
            ('b2', '1')

        """
        return str(self.start), str(self.stop)

    @property
    def figured_bass_string(self) -> str:
        """
        Gets figured bass string.

        ..  container:: example

            >>> baca.tonality.ChordSuspension("4-b3").figured_bass_string
            '4-b3'

            >>> baca.tonality.ChordSuspension("b2-1").figured_bass_string
            'b2-1'

        """
        return f"{self.start!s}-{self.stop!s}"

    @property
    def start(self) -> ScaleDegree:
        """
        Gets start.


            >>> baca.tonality.ChordSuspension("4-b3").start
            ScaleDegree('4')

            >>> baca.tonality.ChordSuspension("b2-1").start
            ScaleDegree('b2')

        """
        return self._start

    @property
    def stop(self) -> ScaleDegree:
        """
        Gets stop.

        ..  container:: example

            >>> baca.tonality.ChordSuspension("4-b3").stop
            ScaleDegree('b3')

            >>> baca.tonality.ChordSuspension("b2-1").stop
            ScaleDegree('1')

        """
        return self._stop

    @property
    def title_string(self) -> str:
        """
        Gets title string.

        ..  container:: example

            >>> baca.tonality.ChordSuspension("4-b3").title_string
            'FourFlatThreeSuspension'

            >>> baca.tonality.ChordSuspension("b2-1").title_string
            'FlatTwoOneSuspension'

        """
        start = self.start.title_string
        stop = self.stop.title_string
        return f"{start}{stop!s}Suspension"


class RootlessChordClass(abjad.IntervalSegment):
    """
    Rootless chord class.

    ..  container:: example

        Major triad in root position:

        >>> baca.tonality.RootlessChordClass("major")
        MajorTriadInRootPosition('P1', '+M3', '+P5')

    ..  container:: example

        Dominant seventh in root position:

        >>> baca.tonality.RootlessChordClass("dominant", 7)
        DominantSeventhInRootPosition('P1', '+M3', '+P5', '+m7')

    ..  container:: example

        German augmented sixth in root position:

        >>> baca.tonality.RootlessChordClass("German", "augmented sixth")
        GermanAugmentedSixthInRootPosition('P1', '+M3', '+m3', '+A2')

    """

    ### CLASS VARIABLES ###

    _segment_to_quality_and_extent = {
        "<+m3, +m3>": ("diminished", 5),
        "<+m3, +M3>": ("minor", 5),
        "<+M3, +m3>": ("major", 5),
        "<+M3, +M3>": ("augmented", 5),
        "<+M3, M2, +M3>": ("augmented French", 6),
        "<+M3, +m3, +2>": ("augmented German", 6),
        "<+M3, P1, +4>": ("augmented Italian", 6),
        "<+M3, +2, +m3>": ("augmented Swiss", 6),
        "<+m3, +m3, +m3>": ("diminished", 7),
        "<+m3, +m3, +M3>": ("half diminished", 7),
        "<+m3, +M3, +m3>": ("minor", 7),
        "<+M3, +m3, +m3>": ("dominant", 7),
        "<+M3, +m3, +M3>": ("major", 7),
        "<+M3, +m3, +m3, +M3>": ("dominant", 9),
    }

    __slots__ = ("_quality_string", "_rotation")

    ### INITIALIZER ###

    def __init__(self, quality_string="major", extent="triad", inversion="root"):
        if extent in ("triad", 5):
            intervals = self._initialize_triad(quality_string)
        elif extent in ("seventh", 7):
            intervals = self._initialize_seventh(quality_string)
        elif extent in ("ninth", 9):
            intervals = self._initialize_ninth(quality_string)
        elif extent in ("augmented sixth", 6):
            intervals = self._initialize_augmented_sixth(quality_string)
        else:
            message = "unknown chord quality arguments."
            raise ValueError(message)
        intervals, rotation = self._invert_chord_quality(intervals, inversion)
        abjad.IntervalSegment.__init__(
            self, items=intervals, item_class=abjad.NamedInterval
        )
        self._quality_string = quality_string
        self._rotation = rotation

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation of rootless chord-class.
        """
        parts = []
        if self.item_class.__name__.startswith("Named"):
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        string = ", ".join(parts)
        return f"{self._title_case_name}({string})"

    ### PRIVATE METHODS ###

    @staticmethod
    def _initialize_augmented_sixth(quality_string):
        if quality_string == "French":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("M2"),
                abjad.NamedInterval("M3"),
            ]
        elif quality_string == "German":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("m3"),
                abjad.NamedInterval("aug2"),
            ]
        elif quality_string == "Italian":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("P1"),
                abjad.NamedInterval("aug4"),
            ]
        elif quality_string == "Swiss":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("aug2"),
                abjad.NamedInterval("m3"),
            ]
        else:
            message = "unaccpetable quality string."
            raise ValueError(message)
        intervals.insert(0, abjad.NamedInterval("P1"))
        return intervals

    @staticmethod
    def _initialize_ninth(quality_string):
        if quality_string == "dominant":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("P5"),
                abjad.NamedInterval("m7"),
                abjad.NamedInterval("M9"),
            ]
        else:
            message = "unacceptable quality string."
            raise ValueError(message)
        intervals.insert(0, abjad.NamedInterval("P1"))
        return intervals

    @staticmethod
    def _initialize_seventh(quality_string):
        if quality_string == "dominant":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("P5"),
                abjad.NamedInterval("m7"),
            ]
        elif quality_string == "major":
            intervals = [
                abjad.NamedInterval("M3"),
                abjad.NamedInterval("P5"),
                abjad.NamedInterval("M7"),
            ]
        elif quality_string == "minor":
            intervals = [
                abjad.NamedInterval("m3"),
                abjad.NamedInterval("P5"),
                abjad.NamedInterval("m7"),
            ]
        elif quality_string in ("diminished", "fully diminished"):
            intervals = [
                abjad.NamedInterval("m3"),
                abjad.NamedInterval("dim5"),
                abjad.NamedInterval("dim7"),
            ]
        elif quality_string == "half diminished":
            intervals = [
                abjad.NamedInterval("m3"),
                abjad.NamedInterval("P5"),
                abjad.NamedInterval("dim7"),
            ]
        else:
            message = "unacceptable quality string."
            raise ValueError(message)
        intervals.insert(0, abjad.NamedInterval("P1"))
        return intervals

    @staticmethod
    def _initialize_triad(quality_string):
        if quality_string == "major":
            intervals = [abjad.NamedInterval("M3"), abjad.NamedInterval("P5")]
        elif quality_string == "minor":
            intervals = [abjad.NamedInterval("m3"), abjad.NamedInterval("P5")]
        elif quality_string == "diminished":
            intervals = [abjad.NamedInterval("m3"), abjad.NamedInterval("dim5")]
        elif quality_string == "augmented":
            intervals = [abjad.NamedInterval("M3"), abjad.NamedInterval("aug5")]
        else:
            raise ValueError(f"unacceptable quality string: {quality_string!r}.")
        intervals.insert(0, abjad.NamedInterval("P1"))
        return intervals

    @staticmethod
    def _invert_chord_quality(intervals, inversion):
        if isinstance(inversion, int):
            intervals = abjad.sequence(intervals).rotate(n=-inversion)
            rotation = -inversion
        elif inversion == "root":
            rotation = 0
        elif inversion == "first":
            intervals = abjad.sequence(intervals).rotate(n=-1)
            rotation = -1
        elif inversion == "second":
            intervals = abjad.sequence(intervals).rotate(n=-2)
            rotation = -2
        elif inversion == "third":
            intervals = abjad.sequence(intervals).rotate(n=-3)
            rotation = -3
        elif inversion == "fourth":
            intervals = abjad.sequence(intervals).rotate(n=-4)
            rotation = -4
        else:
            raise ValueError(f"unknown chord inversion: {inversion!r}.")
        return intervals, rotation

    ### PUBLIC METHODS ###

    @staticmethod
    def from_interval_class_segment(segment) -> "RootlessChordClass":
        """
        Makes new rootless chord-class from ``segment``.

        ..  container:: example

            >>> segment = abjad.IntervalClassSegment([
            ...     abjad.NamedInversionEquivalentIntervalClass("m3"),
            ...     abjad.NamedInversionEquivalentIntervalClass("m3"),
            ... ])
            >>> class_ = baca.tonality.RootlessChordClass
            >>> class_.from_interval_class_segment(segment)
            DiminishedTriadInRootPosition('P1', '+m3', '+d5')

        ..  container:: example

            >>> segment = abjad.IntervalClassSegment([
            ...     abjad.NamedInversionEquivalentIntervalClass("m3"),
            ...     abjad.NamedInversionEquivalentIntervalClass("M3"),
            ... ])
            >>> class_ = baca.tonality.RootlessChordClass
            >>> class_.from_interval_class_segment(segment)
            MinorTriadInRootPosition('P1', '+m3', '+P5')

        ..  container:: example

            >>> segment = abjad.IntervalClassSegment([
            ...     abjad.NamedInversionEquivalentIntervalClass("M3"),
            ...     abjad.NamedInversionEquivalentIntervalClass("m3"),
            ... ])
            >>> class_ = baca.tonality.RootlessChordClass
            >>> class_.from_interval_class_segment(segment)
            MajorTriadInRootPosition('P1', '+M3', '+P5')

        """
        quality, extent = RootlessChordClass._segment_to_quality_and_extent[
            str(segment)
        ]
        return RootlessChordClass(quality, extent=extent)

    ### PRIVATE PROPERTIES ###

    @property
    def _acceptable_augmented_sixth_qualities(self):
        return ("french", "german", "italian", "swiss")

    @property
    def _acceptable_ninth_qualities(self):
        return ("dominant",)

    @property
    def _acceptable_seventh_qualities(self):
        return ("dominant", "major", "minor", "fully diminshed", "half diminished")

    @property
    def _acceptable_triad_qualities(self):
        return ("major", "minor", "diminished", "augmented")

    @property
    def _title_case_name(self):
        return "{}{}In{}".format(
            abjad.String(self.quality_string).to_upper_camel_case(),
            abjad.String(self.extent_name).to_upper_camel_case(),
            abjad.String(self.position).to_upper_camel_case(),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self) -> int:
        """
        Gets cardinality.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).cardinality
            4

        """
        return len(self)

    @property
    def extent(self) -> int:
        """
        Gets extent.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).extent
            7

        """
        return RootedChordClass.cardinality_to_extent(self.cardinality)

    @property
    def extent_name(self) -> str:
        """
        Gets extent name.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).extent_name
            'seventh'

        """
        if self._quality_string.lower() in self._acceptable_augmented_sixth_qualities:
            return "augmented sixth"
        return RootedChordClass.extent_to_extent_name(self.extent)

    @property
    def inversion(self) -> int:
        """
        Gets inversion.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).inversion
            0

        """
        return abs(self.rotation)

    @property
    def position(self) -> str:
        """
        Gets position.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).position
            'root position'

        """
        if self.rotation == 0:
            return "root position"
        elif self.rotation == -1:
            return "first inversion"
        elif self.rotation == -2:
            return "second inversion"
        elif self.rotation == -3:
            return "third inversion"
        elif self.rotation == -4:
            return "fourth inversion"
        else:
            raise ValueError(f"unknown chord position: {self!r}.")

    @property
    def quality_string(self) -> str:
        """
        Gets quality string.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).quality_string
            'dominant'

        """
        return self._quality_string

    @property
    def rotation(self) -> int:
        """
        Gets rotation.

        ..  container:: example

            >>> baca.tonality.RootlessChordClass("dominant", 7).rotation
            0

        """
        return self._rotation


class RootedChordClass(abjad.PitchClassSet):
    """
    Rooted chord class.

    ..  container:: example

        Initializes from pair:

        >>> baca.tonality.RootedChordClass("g", "major")
        GMajorTriadInRootPosition

    ..  container:: example

        Initializes from triple:

        >>> baca.tonality.RootedChordClass("g", "dominant", 7)
        GDominantSeventhInRootPosition

    G dominant seventh represents a class of chords because there are many
    different spacings of a G dominant seventh.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_bass", "_chord_quality", "_root")

    _cardinality_to_extent = {3: 5, 4: 7, 5: 9, 6: 11, 7: 13}

    _extent_to_cardinality = {5: 3, 7: 4, 9: 5, 11: 6, 13: 7}

    _extent_to_extent_name = {
        5: "triad",
        7: "seventh",
        9: "ninth",
        11: "eleventh",
        13: "thirteenth",
    }

    ### INITIALIZER ###

    def __init__(
        self, root=None, quality_string="major", extent="triad", inversion="root"
    ):
        root = root or "c"
        root = abjad.NamedPitchClass(root)
        chord_quality = RootlessChordClass(
            quality_string=quality_string, extent=extent, inversion=inversion
        )
        npcs = []
        for hdi in chord_quality:
            mdi = abjad.NamedInterval(hdi)
            npc = root + mdi
            npcs.append(npc)
        bass = npcs[0]
        abjad.PitchClassSet.__init__(self, items=npcs, item_class=abjad.NamedPitchClass)
        self._root = root
        self._chord_quality = chord_quality
        self._bass = bass

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a rooted chord-class with root, chord
        quality and inversion equal to those of this rooted chord-class.
        """
        return super(RootedChordClass, self).__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes rooted chord-class.
        """
        return super(RootedChordClass, self).__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation of rooted chord-class.
        """
        root = str(self.root).title()
        quality = self.chord_quality._title_case_name
        return root + quality

    ### PRIVATE PROPERTIES ###

    @property
    def _markup_root(self):
        if self.chord_quality._quality_string in ("major", "augmented", "dominant"):
            root = str(self.root).upper()
        else:
            root = str(self.root).lower()
        if len(root) == 2:
            adjustment = r"\hspace #-0.5 \raise #1 \fontsize #-3"
            if root[-1].lower() == "s":
                root = root[0] + rf"{adjustment} \sharp"
            elif root[-1].lower() == "f":
                root = root[0] + rf"{adjustment} \flat"
            else:
                raise ValueError(f"unknown note name: {root}")
        return root

    @property
    def _markup_symbol(self):
        circle = r"\draw-circle #0.35 #0 ##f"
        if self.chord_quality._quality_string == "augmented":
            return "+"
        elif self.chord_quality._quality_string == "diminished":
            return circle
        elif self.chord_quality._quality_string == "half diminished":
            line = r"\draw-line #'(1 . 1)"
            markup = rf"\concat {{ {circle} \hspace #-0.85 \raise #-0.5 {line} }}"
            return markup
        elif self.chord_quality._quality_string == "major" and 5 < self.extent.number:
            return "M"
        elif self.chord_quality._quality_string == "minor" and 5 < self.extent.number:
            return "m"
        else:
            return ""

    ### PUBLIC PROPERTIES ###

    @property
    def bass(self) -> abjad.NamedPitchClass:
        """
        Gets bass.

        ..  container:: example

            >>> baca.tonality.RootedChordClass("g", "major").bass
            NamedPitchClass('g')

        """
        return self._bass

    @property
    def cardinality(self) -> int:
        """
        Gets cardinality.

        ..  container:: example

            >>> baca.tonality.RootedChordClass("g", "dominant", 7).cardinality
            4

        """
        return len(self)

    @property
    def chord_quality(self) -> RootlessChordClass:
        """
        Gets chord quality.

        ..  container:: example

            >>> baca.tonality.RootedChordClass("g", "dominant", 7).chord_quality
            DominantSeventhInRootPosition('P1', '+M3', '+P5', '+m7')

        """
        return self._chord_quality

    @property
    def extent(self) -> ChordExtent:
        """
        Gets extent.

        ..  container:: example

            >>> baca.tonality.RootedChordClass("g", "dominant", 7).extent
            ChordExtent(7)

        """
        extent = self.cardinality_to_extent(self.cardinality)
        return ChordExtent(extent)

    @property
    def figured_bass(self) -> str:
        """
        Gets figured bass.

        ..  container:: example

            >>> baca.tonality.RootedChordClass("g", "dominant", 7).extent
            ChordExtent(7)

        """
        extent, inversion = self.extent, self.inversion
        if extent.number == 5:
            if inversion == 0:
                return ""
            elif inversion == 1:
                return "6/3"
            elif inversion == 2:
                return "6/4"
        elif extent.number == 7:
            if inversion == 0:
                return "7"
            elif inversion == 1:
                return "6/5"
            elif inversion == 2:
                return "4/3"
            elif inversion == 3:
                return "4/2"
        elif extent.number == 9:
            if inversion == 0:
                return ""
            elif inversion == 1:
                raise NotImplementedError
            elif inversion == 2:
                raise NotImplementedError
            elif inversion == 3:
                raise NotImplementedError
            elif inversion == 4:
                raise NotImplementedError
        raise Exception

    @property
    def inversion(self) -> int:
        """
        Gets inversion.

        ..  container:: example

            >>> baca.tonality.RootedChordClass("g", "dominant", 7).inversion
            0

        """
        return self._chord_quality.inversion

    @property
    def markup(self) -> abjad.Markup:
        r"""
        Markup of rooted chord-class.

        ..  container:: example

            >>> chord_class = baca.tonality.RootedChordClass("g", "dominant", 7)
            >>> markup = chord_class.markup
            >>> markup = abjad.new(markup, direction=None)
            >>> lilypond_file = abjad.LilyPondFile()
            >>> lilypond_file.items.append(markup)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \fontsize
                        #1
                        G
                    \hspace
                        #-0.5
                    \raise
                        #1
                        \fontsize
                            #-3
                            \override
                                #'(baseline-skip . 1.5)
                                \column
                                    {
                                        7
                                    }
                    }

        """
        markups = [self._markup_root, self._markup_symbol, self.figured_bass]
        markup = "".join(markups)
        markup = rf"\fontsize #1 {self._markup_root} \hspace #-0.5"
        symbol = self._markup_symbol
        if symbol:
            markup += rf" \hspace #0.5 \raise #1 \fontsize #-3 {symbol}"
            if "circle" in symbol:
                if "sharp" in self._markup_root:
                    markup += r" \hspace #0"
                else:
                    markup += r" \hspace #-1.2"
        inversion = self.figured_bass
        if inversion:
            inv = r" \raise #1 \fontsize #-3 \override #'(baseline-skip . 1.5)"
            string = " ".join(inversion.split("/"))
            inv += rf" \column {{ {string} }}"
            markup += inv
        return abjad.Markup(markup, direction=abjad.Down)

    @property
    def quality_pair(self) -> typing.Tuple[str, str]:
        """
        Gets quality pair.

        ..  container:: example

            >>> chord_class = baca.tonality.RootedChordClass(
            ...     "c",
            ...     "major",
            ...     "triad",
            ...     "root",
            ...     )
            >>> chord_class.quality_pair
            ('major', 'triad')

            >>> chord_class = baca.tonality.RootedChordClass(
            ...     "g",
            ...     "dominant",
            ...     7,
            ...     "second",
            ...     )
            >>> chord_class.quality_pair
            ('dominant', 'seventh')

        """
        chord_quality = self.chord_quality
        return chord_quality.quality_string, chord_quality.extent_name

    @property
    def root(self) -> abjad.NamedPitchClass:
        """
        Gets root.

        ..  container:: example

            >>> chord_class = baca.tonality.RootedChordClass(
            ...     "c",
            ...     "major",
            ...     "triad",
            ...     "root",
            ...     )
            >>> chord_class.root
            NamedPitchClass('c')

            >>> chord_class = baca.tonality.RootedChordClass(
            ...     "g",
            ...     "dominant",
            ...     7,
            ...     "second",
            ...     )
            >>> chord_class.root
            NamedPitchClass('g')

        """
        return self._root

    @property
    def root_string(self) -> str:
        """
        Gets root string.

        ..  container:: example

            >>> chord_class = baca.tonality.RootedChordClass(
            ...     "c",
            ...     "major",
            ...     "triad",
            ...     "root",
            ...     )
            >>> chord_class.root_string
            'C'

            >>> chord_class = baca.tonality.RootedChordClass(
            ...     "g",
            ...     "dominant",
            ...     7,
            ...     "second",
            ...     )
            >>> chord_class.root_string
            'G'

        """
        capitalized_qualities = ("major", "dominant", "augmented")
        name = self.root.pitch_class_label
        letter, accidental = name[0], name[1:]
        if self.chord_quality.quality_string in capitalized_qualities:
            letter = letter.upper()
        else:
            letter = letter.lower()
        return letter + accidental

    ### PUBLIC METHODS ###

    @staticmethod
    def cardinality_to_extent(cardinality) -> int:
        """
        Change ``cardinality`` to extent.

        ..  container:: example

            >>> baca.tonality.RootedChordClass.cardinality_to_extent(3)
            5
            >>> baca.tonality.RootedChordClass.cardinality_to_extent(4)
            7
            >>> baca.tonality.RootedChordClass.cardinality_to_extent(5)
            9
            >>> baca.tonality.RootedChordClass.cardinality_to_extent(6)
            11
            >>> baca.tonality.RootedChordClass.cardinality_to_extent(7)
            13

        """
        return RootedChordClass._cardinality_to_extent[cardinality]

    @staticmethod
    def extent_to_cardinality(extent) -> int:
        """
        Changes ``extent`` to cardinality.

        ..  container:: example

            >>> baca.tonality.RootedChordClass.extent_to_cardinality(5)
            3
            >>> baca.tonality.RootedChordClass.extent_to_cardinality(7)
            4
            >>> baca.tonality.RootedChordClass.extent_to_cardinality(9)
            5
            >>> baca.tonality.RootedChordClass.extent_to_cardinality(11)
            6
            >>> baca.tonality.RootedChordClass.extent_to_cardinality(13)
            7

        """
        return RootedChordClass._extent_to_cardinality[extent]

    @staticmethod
    def extent_to_extent_name(extent) -> str:
        """
        Changes ``extent`` to extent name.

        ..  container:: example

            >>> baca.tonality.RootedChordClass.extent_to_extent_name(5)
            'triad'
            >>> baca.tonality.RootedChordClass.extent_to_extent_name(7)
            'seventh'
            >>> baca.tonality.RootedChordClass.extent_to_extent_name(9)
            'ninth'
            >>> baca.tonality.RootedChordClass.extent_to_extent_name(11)
            'eleventh'
            >>> baca.tonality.RootedChordClass.extent_to_extent_name(13)
            'thirteenth'

        """
        return RootedChordClass._extent_to_extent_name[extent]


class RomanNumeral:
    """
    Roman numeral.

    ..  container:: example

        Initializes from string:

        >>> baca.tonality.RomanNumeral("bII6/4")
        RomanNumeral('bII6/4')

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_extent",
        "_inversion",
        "_quality",
        "_root_scale_degree",
        "_suspension",
    )

    _figured_bass_string_to_extent = {
        "": 5,
        "6": 5,
        "6/4": 5,
        "7": 7,
        "6/5": 7,
        "4/3": 7,
        "4/2": 7,
    }

    _figured_bass_string_to_inversion = {
        "": 0,
        "6": 1,
        "6/4": 2,
        "7": 0,
        "6/5": 1,
        "4/3": 2,
        "4/2": 3,
    }

    _symbol_regex = re.compile(r"([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(.*)")

    ### INITIALIZER ###

    def __init__(self, symbol="V7"):
        groups = self._symbol_regex.match(symbol).groups()
        accidental, roman_numeral, quality, figured_bass = groups
        scale_degree = accidental + roman_numeral
        scale_degree = ScaleDegree(scale_degree)
        figured_bass_parts = figured_bass.split("/")
        naive_figured_bass = [x for x in figured_bass_parts if "-" not in x]
        naive_figured_bass = "/".join(naive_figured_bass)
        extent = self._figured_bass_string_to_extent[naive_figured_bass]
        extent = ChordExtent(extent)
        uppercase = roman_numeral == roman_numeral.upper()
        quality = self._get_quality_name(uppercase, quality, extent.number)
        quality = ChordQuality(quality)
        inversion = self._figured_bass_string_to_inversion[naive_figured_bass]
        inversion = ChordInversion(inversion)
        suspension = [x for x in figured_bass_parts if "-" in x]
        if not suspension:
            suspension = None
        elif 1 < len(suspension):
            raise NotImplementedError("no multiple suspensions yet.")
        else:
            suspension = ChordSuspension(suspension[0])
        self._root_scale_degree = scale_degree
        self._quality = quality
        self._extent = extent
        self._inversion = inversion
        if suspension is not None and suspension.start is None:
            suspension = None
        self._suspension = suspension

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a Roman numeral with scale degree,
        quality, extent, inversion and suspension equal to those of this Roman
        numeral.

        ..  container:: example

            >>> roman_numeral_1 = baca.tonality.RomanNumeral('I')
            >>> roman_numeral_2 = baca.tonality.RomanNumeral('I')
            >>> roman_numeral_3 = baca.tonality.RomanNumeral('V7')

            >>> roman_numeral_1 == roman_numeral_1
            True
            >>> roman_numeral_1 == roman_numeral_2
            True
            >>> roman_numeral_1 == roman_numeral_3
            False


            >>> roman_numeral_2 == roman_numeral_1
            True
            >>> roman_numeral_2 == roman_numeral_2
            True
            >>> roman_numeral_2 == roman_numeral_3
            False

            >>> roman_numeral_3 == roman_numeral_1
            False
            >>> roman_numeral_3 == roman_numeral_2
            False
            >>> roman_numeral_3 == roman_numeral_3
            True

        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Roman numeral.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_accidental_name(self):
        accidental = self.root_scale_degree.accidental
        if accidental.semitones != 0:
            return accidental.name.title()
        return ""

    def _get_figured_bass_digits(self):
        characters = self._get_figured_bass_string()
        if characters:
            characters = characters.split("/")
            digits = [int(x) for x in characters]
            return tuple(digits)
        return ()

    def _get_figured_bass_string(self):
        return self.inversion.extent_to_figured_bass_string(self.extent.number)

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            storage_format_is_indented=False,
            storage_format_args_values=[self.symbol],
        )

    def _get_quality_name(self, uppercase, quality_string, extent):
        if quality_string == "o":
            return "diminished"
        elif quality_string == "@":
            return "half diminished"
        elif quality_string == "+":
            return "augmented"
        elif quality_string == "M":
            return "major"
        elif quality_string == "m":
            return "minor"
        elif extent == 5:
            if quality_string == "" and uppercase:
                return "major"
            elif quality_string == "" and not uppercase:
                return "minor"
            else:
                raise ValueError(f"unknown quality string: {quality_string!r}.")
        elif extent == 7:
            if quality_string == "" and uppercase:
                return "dominant"
            elif quality_string == "" and not uppercase:
                return "minor"
            else:
                raise ValueError(f"unknown quality string: {quality_string!r}.")
        else:
            raise ValueError(f"unknown extent: {extent!r}.")

    def _get_quality_symbol(self):
        if self.extent == ChordExtent(5):
            if self.quality == ChordQuality("diminished"):
                return "o"
            elif self.quality == ChordQuality("augmented"):
                return "+"
            else:
                return ""
        elif self.extent == ChordExtent(7):
            if self.quality == ChordQuality("dominant"):
                return ""
            elif self.quality == ChordQuality("major"):
                return "M"
            elif self.quality == ChordQuality("diminished"):
                return "o"
            elif self.quality == ChordQuality("half diminished"):
                return "@"
            elif self.quality == ChordQuality("augmented"):
                return "+"
            else:
                return ""
        else:
            raise NotImplementedError

    def _get_roman_numeral_string(self):
        roman_numeral_string = self.root_scale_degree.roman_numeral_string
        if not self.quality.is_uppercase:
            roman_numeral_string = roman_numeral_string.lower()
        return roman_numeral_string

    ### PUBLIC PROPERTIES ###

    @property
    def bass_scale_degree(self) -> ScaleDegree:
        """
        Gets bass scale degree.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII6/4").bass_scale_degree
            ScaleDegree('6')

            >>> baca.tonality.RomanNumeral("V7").bass_scale_degree
            ScaleDegree('5')

        """
        root_scale_degree = self.root_scale_degree.number
        bass_scale_degree = root_scale_degree - 1
        bass_scale_degree += 2 * self.inversion.number
        bass_scale_degree %= 7
        bass_scale_degree += 1
        bass_scale_degree = ScaleDegree(bass_scale_degree)
        return bass_scale_degree

    @property
    def extent(self) -> ChordExtent:
        """
        Gets extent.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII").extent
            ChordExtent(5)

        """
        return self._extent

    @property
    def figured_bass_string(self) -> str:
        """
        Gets figured bass string.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("II6/5").figured_bass_string
            '6/5'

        """
        digits = self._get_figured_bass_digits()
        if self.suspension is None:
            return "/".join([str(_) for _ in digits])
        suspension_pair = self.suspension.figured_bass_pair
        figured_bass_list = []
        for n in range(9, 1, -1):
            if n == suspension_pair[0]:
                figured_bass_list.append(str(self.suspension))
            elif n == suspension_pair[1]:
                pass
            elif n in digits:
                figured_bass_list.append(str(n))
        figured_bass_string = "/".join(figured_bass_list)
        return figured_bass_string

    @property
    def inversion(self) -> ChordInversion:
        """
        Gets inversion.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII").inversion
            ChordInversion(0)

        """
        return self._inversion

    @property
    def markup(self) -> abjad.Markup:
        r"""
        Gets markup.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII").markup
            Markup(contents=['bII'], direction=Down)

        """
        symbol = self.symbol
        symbol = symbol.replace("#", r"\sharp ")
        return abjad.Markup(symbol, direction=abjad.Down)

    @property
    def quality(self) -> ChordQuality:
        """
        Gets quality.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII").quality
            ChordQuality('major')

        """
        return self._quality

    @property
    def root_scale_degree(self) -> ScaleDegree:
        """
        Gets root scale degree.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII").root_scale_degree
            ScaleDegree('b2')

            >>> baca.tonality.RomanNumeral("bII6/4").root_scale_degree
            ScaleDegree('b2')

        """
        return self._root_scale_degree

    @property
    def suspension(self) -> typing.Optional[ChordSuspension]:
        """
        Gets suspension.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII6/4").suspension is None
            True

            >>> baca.tonality.RomanNumeral("V7").suspension is None
            True

        """
        return self._suspension

    @property
    def symbol(self) -> str:
        """
        Gets symbolc of Roman numeral.

        ..  container:: example

            >>> baca.tonality.RomanNumeral("bII6/4").symbol
            'bII6/4'

            >>> baca.tonality.RomanNumeral("V7").symbol
            'V7'

        """
        result = ""
        result += self.root_scale_degree.accidental.symbol
        result += self._get_roman_numeral_string()
        result += self._get_quality_symbol()
        result += self.figured_bass_string
        return result

    ### PUBLIC METHODS ###

    @staticmethod
    def from_scale_degree_quality_extent_and_inversion(
        scale_degree, quality, extent, inversion
    ) -> "RomanNumeral":
        """
        Makes Roman numeral from ``scale_degree``, ``quality``, ``extent`` and
        ``inversion``.
        """
        scale_degree = ScaleDegree(scale_degree)
        quality = ChordQuality(quality)
        extent = ChordExtent(extent)
        inversion = ChordInversion(inversion)
        roman_numeral = RomanNumeral()
        roman_numeral._root_scale_degree = scale_degree
        roman_numeral._quality = quality
        roman_numeral._extent = extent
        roman_numeral._inversion = inversion
        return roman_numeral


### PRIVATE FUNCTIONS ###


def _analyze_chord(argument):
    selection = abjad.select(argument)
    pitches = abjad.PitchSegment.from_selection(selection)
    npcset = abjad.PitchClassSet(pitches, item_class=abjad.NamedPitchClass)
    ordered_npcs = []
    letters = ("c", "e", "g", "b", "d", "f", "a")
    for letter in letters:
        for npc in npcset:
            if npc._get_diatonic_pc_name() == letter:
                ordered_npcs.append(npc)
    ordered_npcs = abjad.PitchClassSegment(
        ordered_npcs, item_class=abjad.NamedPitchClass
    )
    for x in range(len(ordered_npcs)):
        ordered_npcs = ordered_npcs.rotate(1)
        segment = abjad.IntervalClassSegment(
            items=abjad.math.difference_series(list(ordered_npcs)),
            item_class=abjad.NamedInversionEquivalentIntervalClass,
        )
        if segment.is_tertian:
            break
    else:
        return None
    root = ordered_npcs[0]
    class_ = RootlessChordClass
    rootless_chord_class = class_.from_interval_class_segment(segment)
    bass = min(pitches).pitch_class
    inversion = ordered_npcs.index(bass)
    return RootedChordClass(
        root,
        rootless_chord_class.quality_string,
        rootless_chord_class.extent,
        inversion,
    )


def _analyze_incomplete_chord(argument):
    selection = abjad.select(argument)
    pitches = abjad.PitchSegment.from_selection(selection)
    npcset = abjad.PitchClassSet(pitches, item_class=abjad.NamedPitchClass)
    dicv = abjad.IntervalClassVector(
        items=npcset, item_class=abjad.NamedInversionEquivalentIntervalClass
    )
    # TODO: eliminate code duplication #
    if dicv == _make_dicv("c", "ef"):
        model_npcs = ["c", "ef"]
        quality, extent = "minor", "triad"
    elif dicv == _make_dicv("c", "e"):
        model_npcs = ["c", "e"]
        quality, extent = "major", "triad"
    elif dicv == _make_dicv("c", "ef", "bff"):
        model_npcs = ["c", "ef", "bff"]
        quality, extent = "diminished", "seventh"
    elif dicv == _make_dicv("c", "ef", "bf"):
        model_npcs = ["c", "ef", "bf"]
        quality, extent = "minor", "seventh"
    elif dicv == _make_dicv("c", "e", "bf"):
        model_npcs = ["c", "e", "bf"]
        quality, extent = "dominant", "seventh"
    elif dicv == _make_dicv("c", "e", "b"):
        model_npcs = ["c", "e", "b"]
        quality, extent = "major", "seventh"
    else:
        raise Exception("can not identify incomplete tertian chord.")
    bass = min(pitches).pitch_class
    try:
        npcseg = npcset.order_by(
            abjad.PitchClassSegment(model_npcs, item_class=abjad.NamedPitchClass)
        )
    except ValueError:
        raise Exception("can not identify incomplete tertian chord.")
    inversion = npcseg.index(bass)
    root = npcseg[0]
    return RootedChordClass(root, quality, extent, inversion)


def _analyze_incomplete_tonal_function(argument, key_signature):
    if isinstance(argument, RootedChordClass):
        chord_class = argument
    else:
        selection = abjad.select(argument)
        chord_classes = analyze_incomplete_chords(selection)
        assert len(chord_classes) == 1
        chord_class = chord_classes[0]
    root = chord_class.root
    scale = Scale(key_signature)
    scale_degree = scale.named_pitch_class_to_scale_degree(root)
    quality = chord_class.chord_quality.quality_string
    extent = chord_class.extent
    inversion = chord_class.inversion
    class_ = RomanNumeral
    return class_.from_scale_degree_quality_extent_and_inversion(
        scale_degree, quality, extent, inversion
    )


def _analyze_tonal_function(argument, key_signature):
    if isinstance(argument, RootedChordClass):
        chord_class = argument
    else:
        selection = abjad.select(argument)
        chord_classes = analyze_chords(selection)
        assert len(chord_classes) == 1
        chord_class = chord_classes[0]
    if chord_class is None:
        return None
    root = chord_class.root
    scale = Scale(key_signature)
    scale_degree = scale.named_pitch_class_to_scale_degree(root)
    quality = chord_class.chord_quality.quality_string
    extent = chord_class.extent
    inversion = chord_class.inversion
    class_ = RomanNumeral
    return class_.from_scale_degree_quality_extent_and_inversion(
        scale_degree, quality, extent, inversion
    )


def _is_neighbor_note(note):
    if not isinstance(note, abjad.Note):
        raise TypeError(f"must be note: {note!r}.")
    previous_note = abjad.get.leaf(note, -1)
    next_note = abjad.get.leaf(note, 1)
    if previous_note is None:
        return False
    if next_note is None:
        return False
    notes = [previous_note, note, next_note]
    preceding_interval = note.written_pitch - previous_note.written_pitch
    preceding_interval_direction = abjad.math.sign(preceding_interval.direction_number)
    following_interval = next_note.written_pitch - note.written_pitch
    following_interval_direction = abjad.math.sign(following_interval.direction_number)
    if are_stepwise_notes(notes):
        if preceding_interval_direction != following_interval_direction:
            return True
    return False


def _is_passing_tone(note):
    if not isinstance(note, abjad.Note):
        raise TypeError(f"must be note: {note!r}.")
    previous_note = abjad.get.leaf(note, -1)
    next_note = abjad.get.leaf(note, 1)
    if previous_note is None or next_note is None:
        return False
    notes = [previous_note, note, next_note]
    return are_scalar_notes(notes)


def _make_dicv(*named_pitch_classes):
    pitch_set = abjad.PitchSet(named_pitch_classes)
    return abjad.IntervalClassVector(
        items=pitch_set, item_class=abjad.NamedInversionEquivalentIntervalClass
    )


### PUBLIC FUNCTIONS ###


def analyze_chords(selection) -> typing.Optional[typing.List[RootedChordClass]]:
    r"""
    Analyzes chords in selection.

    ..  container:: example

        >>> chords = [
        ...     abjad.Chord([0, 4, 7], (1, 4)),
        ...     abjad.Chord([4, 7, 12], (1, 4)),
        ...     abjad.Chord([7, 12, 16], (1, 4)),
        ...     ]
        >>> staff = abjad.Staff(chords)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c' e' g'>4
                <e' g' c''>4
                <g' c'' e''>4
            }

        >>> for chord in baca.tonality.analyze_chords(staff[:]):
        ...     chord
        ...
        CMajorTriadInRootPosition
        CMajorTriadInFirstInversion
        CMajorTriadInSecondInversion

    ..  container:: example

        The three inversions of an a minor triad:

        >>> chords = [
        ...     abjad.Chord([9, 12, 16], (1, 4)),
        ...     abjad.Chord([12, 16, 21], (1, 4)),
        ...     abjad.Chord([16, 21, 24], (1, 4)),
        ...     ]
        >>> staff = abjad.Staff(chords)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <a' c'' e''>4
                <c'' e'' a''>4
                <e'' a'' c'''>4
            }

        >>> for chord in baca.tonality.analyze_chords(staff[:]):
        ...     chord
        ...
        AMinorTriadInRootPosition
        AMinorTriadInFirstInversion
        AMinorTriadInSecondInversion

    ..  container:: example

        The four inversions of a C dominant seventh chord:

        >>> chords = [
        ...     abjad.Chord([0, 4, 7, 10], (1, 4)),
        ...     abjad.Chord([4, 7, 10, 12], (1, 4)),
        ...     abjad.Chord([7, 10, 12, 16], (1, 4)),
        ...     abjad.Chord([10, 12, 16, 19], (1, 4)),
        ...     ]
        >>> staff = abjad.Staff(chords)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c' e' g' bf'>4
                <e' g' bf' c''>4
                <g' bf' c'' e''>4
                <bf' c'' e'' g''>4
            }

        >>> for chord in baca.tonality.analyze_chords(staff[:]):
        ...     chord
        ...
        CDominantSeventhInRootPosition
        CDominantSeventhInFirstInversion
        CDominantSeventhInSecondInversion
        CDominantSeventhInThirdInversion

    ..  container:: example

        The five inversions of a C dominant ninth chord:

        >>> chords = [
        ...     abjad.Chord([0, 4, 7, 10, 14], (1, 4)),
        ...     abjad.Chord([4, 7, 10, 12, 14], (1, 4)),
        ...     abjad.Chord([7, 10, 12, 14, 16], (1, 4)),
        ...     abjad.Chord([10, 12, 14, 16, 19], (1, 4)),
        ...     abjad.Chord([2, 10, 12, 16, 19], (1, 4)),
        ...     ]
        >>> staff = abjad.Staff(chords)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c' e' g' bf' d''>4
                <e' g' bf' c'' d''>4
                <g' bf' c'' d'' e''>4
                <bf' c'' d'' e'' g''>4
                <d' bf' c'' e'' g''>4
            }

        >>> for chord in baca.tonality.analyze_chords(staff[:]):
        ...     chord
        ...
        CDominantNinthInRootPosition
        CDominantNinthInFirstInversion
        CDominantNinthInSecondInversion
        CDominantNinthInThirdInversion
        CDominantNinthInFourthInversion

    """
    result = []
    for component in selection:
        chord_class = _analyze_chord(component)
        result.append(chord_class)
    return result


def analyze_incomplete_chords(
    selection,
) -> typing.Optional[typing.List[RootedChordClass]]:
    """
    Analyzes incomplete chords.

    ..  container:: example

        >>> chord = abjad.Chord("<g' b'>4")
        >>> baca.tonality.analyze_incomplete_chords([chord])
        [GMajorTriadInRootPosition]

        >>> chord = abjad.Chord("<g' bf'>4")
        >>> baca.tonality.analyze_incomplete_chords([chord])
        [GMinorTriadInRootPosition]

        >>> chord = abjad.Chord("<f g b>4")
        >>> baca.tonality.analyze_incomplete_chords([chord])
        [GDominantSeventhInSecondInversion]

        >>> chord = abjad.Chord("<fs g b>4")
        >>> baca.tonality.analyze_incomplete_chords([chord])
        [GMajorSeventhInSecondInversion]

    """
    result = []
    for component in selection:
        chord_class = _analyze_incomplete_chord(component)
        result.append(chord_class)
    return result


def analyze_incomplete_tonal_functions(
    selection, key_signature
) -> typing.Optional[typing.List[RomanNumeral]]:
    """
    Analyzes incomplete tonal functions of chords in client according to
    ``key_signature``.

    ..  container:: example

        >>> chord = abjad.Chord("<c' e'>4")
        >>> key_signature = abjad.KeySignature("g", "major")
        >>> baca.tonality.analyze_incomplete_tonal_functions([chord], key_signature)
        [RomanNumeral('IV')]

        >>> chord = abjad.Chord("<g' b'>4")
        >>> key_signature = abjad.KeySignature("c", "major")
        >>> baca.tonality.analyze_incomplete_tonal_functions([chord], key_signature)
        [RomanNumeral('V')]

        >>> chord = abjad.Chord("<g' bf'>4")
        >>> baca.tonality.analyze_incomplete_tonal_functions([chord], key_signature)
        [RomanNumeral('v')]

        >>> key_signature = abjad.KeySignature("c", "major")
        >>> chord = abjad.Chord("<f g b>4")
        >>> baca.tonality.analyze_incomplete_tonal_functions([chord], key_signature)
        [RomanNumeral('V4/3')]

        >>> chord = abjad.Chord("<fs g b>4")
        >>> baca.tonality.analyze_incomplete_tonal_functions([chord], key_signature)
        [RomanNumeral('VM4/3')]

    """
    result = []
    for component in selection:
        tonal_function = _analyze_incomplete_tonal_function(component, key_signature)
        result.append(tonal_function)
    return result


def analyze_neighbor_notes(selection) -> typing.List[bool]:
    r"""
    Is true when ``note`` in client is preceeded by a stepwise interval in one
    direction and followed by a stepwise interval in the other direction.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }

        >>> baca.tonality.analyze_neighbor_notes(staff[:])
        [False, False, False, False]

    """
    result = []
    for component in selection:
        tonal_function = _is_neighbor_note(component)
        result.append(tonal_function)
    return result


def analyze_passing_tones(selection) -> typing.List[bool]:
    r"""
    Is true when note in client is both preceeded and followed by scalewise notes.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }

        >>> baca.tonality.analyze_passing_tones(staff[:])
        [False, True, True, False]

    """
    result = []
    for component in selection:
        tonal_function = _is_passing_tone(component)
        result.append(tonal_function)
    return result


def analyze_tonal_functions(selection, key_signature) -> typing.List[RomanNumeral]:
    """
    Analyzes tonal function of chords in client according to ``key_signature``.

    ..  container:: example

        >>> chord = abjad.Chord('<ef g bf>4')
        >>> key_signature = abjad.KeySignature('c', 'major')
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('bIII')]

        >>> key_signature = abjad.KeySignature('c', 'major')
        >>> chord = abjad.Chord('<c e g>4')
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I')]

        >>> chord = abjad.Chord(['e', 'g', "c'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I6')]

        >>> chord = abjad.Chord(['g', "c'", "e'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I6/4')]

    ..  container:: example

        >>> key_signature = abjad.KeySignature('c', 'major')
        >>> chord = abjad.Chord(['c', 'ef', 'g'], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('i')]

        >>> chord = abjad.Chord(['ef', 'g', "c'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('i6')]

        >>> chord = abjad.Chord(['g', "c'", "ef'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('i6/4')]

    ..  container:: example

        >>> key_signature = abjad.KeySignature('c', 'major')
        >>> chord = abjad.Chord(['c', 'e', 'g', 'bf'], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I7')]

        >>> chord = abjad.Chord(['e', 'g', 'bf', "c'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I6/5')]

        >>> chord = abjad.Chord(['g', 'bf', "c'", "e'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I4/3')]

        >>> chord = abjad.Chord(['bf', "c'", "e'", "g'"], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [RomanNumeral('I4/2')]

    ..  container:: example

        >>> key_signature = abjad.KeySignature('c', 'major')
        >>> chord = abjad.Chord(['c', 'cs', 'd'], (1, 4))
        >>> baca.tonality.analyze_tonal_functions([chord], key_signature)
        [None]

    """
    result = []
    for component in selection:
        tonal_function = _analyze_tonal_function(component, key_signature)
        result.append(tonal_function)
    return result


def are_scalar_notes(selection) -> bool:
    """
    Is true when notes in client are scalar.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 cs'")
        >>> baca.tonality.are_scalar_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 d'")
        >>> baca.tonality.are_scalar_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 ds'")
        >>> baca.tonality.are_scalar_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 b")
        >>> baca.tonality.are_scalar_notes(staff[:])
        True

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'")
        >>> baca.tonality.are_scalar_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 e'")
        >>> baca.tonality.are_scalar_notes(staff[:])
        False

    """
    direction_number = None
    notes = abjad.iterate(selection).components(abjad.Note)
    for left, right in abjad.sequence(notes).nwise():
        try:
            assert not (left.written_pitch == right.written_pitch)
            mdi = abjad.NamedInterval.from_pitch_carriers(left, right)
            assert mdi.number <= 2
            if direction_number is None:
                direction_number = mdi.direction_number
            assert direction_number == mdi.direction_number
        except AssertionError:
            return False
    return True


def are_stepwise_ascending_notes(selection) -> bool:
    """
    Is true when notes in client are stepwise ascending.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 cs'")
        >>> baca.tonality.are_stepwise_ascending_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 d'")
        >>> baca.tonality.are_stepwise_ascending_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 ds'")
        >>> baca.tonality.are_stepwise_ascending_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 b")
        >>> baca.tonality.are_stepwise_ascending_notes(staff[:])
        False

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'")
        >>> baca.tonality.are_stepwise_ascending_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 e'")
        >>> baca.tonality.are_stepwise_ascending_notes(staff[:])
        False

    """
    notes = abjad.iterate(selection).components(abjad.Note)
    for left, right in abjad.sequence(notes).nwise():
        try:
            assert not (left.written_pitch == right.written_pitch)
            mdi = abjad.NamedInterval.from_pitch_carriers(left, right)
            assert mdi.number == 2
        except AssertionError:
            return False
    return True


def are_stepwise_descending_notes(selection) -> bool:
    """
    Is true when notes in client are stepwise descending.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 cs'")
        >>> baca.tonality.are_stepwise_descending_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 d'")
        >>> baca.tonality.are_stepwise_descending_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 ds'")
        >>> baca.tonality.are_stepwise_descending_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 b")
        >>> baca.tonality.are_stepwise_descending_notes(staff[:])
        True

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'")
        >>> baca.tonality.are_stepwise_descending_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 e'")
        >>> baca.tonality.are_stepwise_descending_notes(staff[:])
        False

    """
    notes = abjad.iterate(selection).components(abjad.Note)
    for left, right in abjad.sequence(notes).nwise():
        try:
            assert not (left.written_pitch == right.written_pitch)
            mdi = abjad.NamedInterval.from_pitch_carriers(left, right)
            assert mdi.number == -2
        except AssertionError:
            return False
    return True


def are_stepwise_notes(selection) -> bool:
    """
    Is true when notes in client are stepwise.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 cs'")
        >>> baca.tonality.are_stepwise_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 d'")
        >>> baca.tonality.are_stepwise_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 ds'")
        >>> baca.tonality.are_stepwise_notes(staff[:])
        True

        >>> staff = abjad.Staff("c'4 b")
        >>> baca.tonality.are_stepwise_notes(staff[:])
        True

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'")
        >>> baca.tonality.are_stepwise_notes(staff[:])
        False

        >>> staff = abjad.Staff("c'4 e'")
        >>> baca.tonality.are_stepwise_notes(staff[:])
        False

    """
    notes = abjad.iterate(selection).components(abjad.Note)
    for left, right in abjad.sequence(notes).nwise():
        try:
            assert not (left.written_pitch == right.written_pitch)
            hdi = abjad.NamedInterval.from_pitch_carriers(left, right)
            assert hdi.number <= 2
        except AssertionError:
            return False
    return True
