.. _baca--pitchclasses:

pitchclasses
============

.. automodule:: baca.pitchclasses

.. currentmodule:: baca.pitchclasses

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.pitchclasses

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: section-header

.. autosummary::
   :nosignatures:

   ~PitchTree

.. autoclass:: PitchTree

   .. autosummary::
      :nosignatures:

      has_repeats
      invert
      retrograde
      rotate
      transpose

   .. autosummary::
      :nosignatures:

      __illustrate__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchTree.__contains__

   .. container:: inherited

      .. automethod:: PitchTree.__eq__

   .. container:: inherited

      .. automethod:: PitchTree.__format__

   .. container:: inherited

      .. automethod:: PitchTree.__getitem__

   .. container:: inherited

      .. automethod:: PitchTree.__hash__

   .. automethod:: PitchTree.__illustrate__

   .. container:: inherited

      .. automethod:: PitchTree.__len__

   .. container:: inherited

      .. automethod:: PitchTree.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchTree.get_payload

   .. automethod:: PitchTree.has_repeats

   .. automethod:: PitchTree.invert

   .. container:: inherited

      .. automethod:: PitchTree.iterate

   .. automethod:: PitchTree.retrograde

   .. automethod:: PitchTree.rotate

   .. automethod:: PitchTree.transpose

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchTree.item_class

   .. container:: inherited

      .. autoattribute:: PitchTree.items

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~ArpeggiationSpacingSpecifier
   ~ChordalSpacingSpecifier
   ~CollectionList
   ~Constellation
   ~ConstellationCircuit
   ~DesignMaker
   ~HarmonicSeries
   ~Partial
   ~PitchClassSegment
   ~PitchClassSet
   ~PitchSegment
   ~PitchSet
   ~PitchTreeSpanner
   ~ZaggedPitchClassMaker

.. autoclass:: ArpeggiationSpacingSpecifier

   .. autosummary::
      :nosignatures:

      direction
      pattern

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ArpeggiationSpacingSpecifier.__call__

   .. container:: inherited

      .. automethod:: ArpeggiationSpacingSpecifier.__copy__

   .. container:: inherited

      .. automethod:: ArpeggiationSpacingSpecifier.__eq__

   .. container:: inherited

      .. automethod:: ArpeggiationSpacingSpecifier.__format__

   .. container:: inherited

      .. automethod:: ArpeggiationSpacingSpecifier.__hash__

   .. container:: inherited

      .. automethod:: ArpeggiationSpacingSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ArpeggiationSpacingSpecifier.direction

   .. autoattribute:: ArpeggiationSpacingSpecifier.pattern

.. autoclass:: ChordalSpacingSpecifier

   .. autosummary::
      :nosignatures:

      bass
      direction
      minimum_semitones
      pattern
      soprano

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ChordalSpacingSpecifier.__call__

   .. container:: inherited

      .. automethod:: ChordalSpacingSpecifier.__copy__

   .. container:: inherited

      .. automethod:: ChordalSpacingSpecifier.__eq__

   .. container:: inherited

      .. automethod:: ChordalSpacingSpecifier.__format__

   .. container:: inherited

      .. automethod:: ChordalSpacingSpecifier.__hash__

   .. container:: inherited

      .. automethod:: ChordalSpacingSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ChordalSpacingSpecifier.bass

   .. autoattribute:: ChordalSpacingSpecifier.direction

   .. autoattribute:: ChordalSpacingSpecifier.minimum_semitones

   .. autoattribute:: ChordalSpacingSpecifier.pattern

   .. autoattribute:: ChordalSpacingSpecifier.soprano

.. autoclass:: CollectionList

   .. autosummary::
      :nosignatures:

      accumulate
      arpeggiate_down
      arpeggiate_up
      bass_to_octave
      center_to_octave
      chords
      cursor
      flatten
      has_duplicate_pitch_classes
      has_duplicates
      has_repeat_pitch_classes
      has_repeats
      helianthate
      join
      partition
      read
      remove
      remove_duplicate_pitch_classes
      remove_duplicates
      remove_repeat_pitch_classes
      remove_repeats
      repeat
      retain
      soprano_to_octave
      space_down
      space_up
      to_pitch_classes
      to_pitches
      transpose

   .. autosummary::
      :nosignatures:

      collections
      item_class

   .. autosummary::
      :nosignatures:

      __add__
      __eq__
      __format__
      __getitem__
      __illustrate__
      __len__
      __repr__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: CollectionList.__add__

   .. container:: inherited

      .. automethod:: CollectionList.__contains__

   .. container:: inherited

      .. automethod:: CollectionList.__copy__

   .. automethod:: CollectionList.__eq__

   .. automethod:: CollectionList.__format__

   .. automethod:: CollectionList.__getitem__

   .. automethod:: CollectionList.__illustrate__

   .. container:: inherited

      .. automethod:: CollectionList.__iter__

   .. automethod:: CollectionList.__len__

   .. automethod:: CollectionList.__repr__

   .. container:: inherited

      .. automethod:: CollectionList.__reversed__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: CollectionList.accumulate

   .. automethod:: CollectionList.arpeggiate_down

   .. automethod:: CollectionList.arpeggiate_up

   .. automethod:: CollectionList.bass_to_octave

   .. automethod:: CollectionList.center_to_octave

   .. automethod:: CollectionList.chords

   .. container:: inherited

      .. automethod:: CollectionList.count

   .. automethod:: CollectionList.cursor

   .. automethod:: CollectionList.flatten

   .. automethod:: CollectionList.has_duplicate_pitch_classes

   .. automethod:: CollectionList.has_duplicates

   .. automethod:: CollectionList.has_repeat_pitch_classes

   .. automethod:: CollectionList.has_repeats

   .. automethod:: CollectionList.helianthate

   .. container:: inherited

      .. automethod:: CollectionList.index

   .. automethod:: CollectionList.join

   .. automethod:: CollectionList.partition

   .. automethod:: CollectionList.read

   .. automethod:: CollectionList.remove

   .. automethod:: CollectionList.remove_duplicate_pitch_classes

   .. automethod:: CollectionList.remove_duplicates

   .. automethod:: CollectionList.remove_repeat_pitch_classes

   .. automethod:: CollectionList.remove_repeats

   .. automethod:: CollectionList.repeat

   .. automethod:: CollectionList.retain

   .. automethod:: CollectionList.soprano_to_octave

   .. automethod:: CollectionList.space_down

   .. automethod:: CollectionList.space_up

   .. automethod:: CollectionList.to_pitch_classes

   .. automethod:: CollectionList.to_pitches

   .. automethod:: CollectionList.transpose

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: CollectionList.collections

   .. autoattribute:: CollectionList.item_class

.. autoclass:: Constellation

   .. autosummary::
      :nosignatures:

      get_chord
      get_number_of_chord
      make_chords
      make_labeled_chords
      make_labeled_colored_chords
      show_colored_generator_chord
      show_colored_generator_chord_and_pivot_chord
      show_generator_chord
      show_generator_chord_and_pivot_chord
      show_pivot_chord

   .. autosummary::
      :nosignatures:

      constellation_number
      generator_chord
      partitioned_generator_pitch_numbers
      pitch_range
      pivot_chord

   .. autosummary::
      :nosignatures:

      __contains__
      __getitem__
      __len__
      __repr__

   .. autosummary::
      :nosignatures:

      constellate

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Constellation.__contains__

   .. container:: inherited

      .. automethod:: Constellation.__format__

   .. automethod:: Constellation.__getitem__

   .. automethod:: Constellation.__len__

   .. automethod:: Constellation.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Constellation.get_chord

   .. automethod:: Constellation.get_number_of_chord

   .. automethod:: Constellation.make_chords

   .. automethod:: Constellation.make_labeled_chords

   .. automethod:: Constellation.make_labeled_colored_chords

   .. automethod:: Constellation.show_colored_generator_chord

   .. automethod:: Constellation.show_colored_generator_chord_and_pivot_chord

   .. automethod:: Constellation.show_generator_chord

   .. automethod:: Constellation.show_generator_chord_and_pivot_chord

   .. automethod:: Constellation.show_pivot_chord

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Constellation.constellate

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Constellation.constellation_number

   .. autoattribute:: Constellation.generator_chord

   .. autoattribute:: Constellation.partitioned_generator_pitch_numbers

   .. autoattribute:: Constellation.pitch_range

   .. autoattribute:: Constellation.pivot_chord

.. autoclass:: ConstellationCircuit

   .. autosummary::
      :nosignatures:

      make_constellation_circuit_1

   .. autosummary::
      :nosignatures:

      CC1

   .. autosummary::
      :nosignatures:

      get
      illustrate_colored_generator_chords
      illustrate_colored_generator_chords_and_pivot_chords
      illustrate_generator_chords
      illustrate_generator_chords_and_pivot_chords
      illustrate_pivot_chords

   .. autosummary::
      :nosignatures:

      generator_chords
      pitch_range
      pivot_chords

   .. autosummary::
      :nosignatures:

      __getitem__
      __len__
      __repr__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ConstellationCircuit.__format__

   .. automethod:: ConstellationCircuit.__getitem__

   .. automethod:: ConstellationCircuit.__len__

   .. automethod:: ConstellationCircuit.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: ConstellationCircuit.get

   .. automethod:: ConstellationCircuit.illustrate_colored_generator_chords

   .. automethod:: ConstellationCircuit.illustrate_colored_generator_chords_and_pivot_chords

   .. automethod:: ConstellationCircuit.illustrate_generator_chords

   .. automethod:: ConstellationCircuit.illustrate_generator_chords_and_pivot_chords

   .. automethod:: ConstellationCircuit.illustrate_pivot_chords

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: ConstellationCircuit.make_constellation_circuit_1

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ConstellationCircuit.generator_chords

   .. autoattribute:: ConstellationCircuit.pitch_range

   .. autoattribute:: ConstellationCircuit.pivot_chords

.. autoclass:: DesignMaker

   .. autosummary::
      :nosignatures:

      partition
      partition_cyclic

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: DesignMaker.__call__

   .. container:: inherited

      .. automethod:: DesignMaker.__format__

   .. container:: inherited

      .. automethod:: DesignMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: DesignMaker.partition

   .. automethod:: DesignMaker.partition_cyclic

.. autoclass:: HarmonicSeries

   .. autosummary::
      :nosignatures:

      partial

   .. autosummary::
      :nosignatures:

      fundamental

   .. autosummary::
      :nosignatures:

      __illustrate__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: HarmonicSeries.__format__

   .. automethod:: HarmonicSeries.__illustrate__

   .. container:: inherited

      .. automethod:: HarmonicSeries.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: HarmonicSeries.partial

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: HarmonicSeries.fundamental

.. autoclass:: Partial

   .. autosummary::
      :nosignatures:

      approximation
      deviation
      fundamental
      number

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Partial.__format__

   .. container:: inherited

      .. automethod:: Partial.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Partial.approximation

   .. autoattribute:: Partial.deviation

   .. autoattribute:: Partial.fundamental

   .. autoattribute:: Partial.number

.. autoclass:: PitchClassSegment

   .. autosummary::
      :nosignatures:

      alpha
      arpeggiate_down
      arpeggiate_up
      chord
      get_matching_transforms
      get_transforms
      has_duplicates
      has_repeats
      sequence
      space_down
      space_up

   .. autosummary::
      :nosignatures:

      __eq__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSegment.__add__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__contains__

   .. automethod:: PitchClassSegment.__eq__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__format__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__getitem__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__illustrate__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__iter__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__len__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__mul__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__radd__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__repr__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__reversed__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__rmul__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchClassSegment.alpha

   .. automethod:: PitchClassSegment.arpeggiate_down

   .. automethod:: PitchClassSegment.arpeggiate_up

   .. automethod:: PitchClassSegment.chord

   .. container:: inherited

      .. automethod:: PitchClassSegment.count

   .. automethod:: PitchClassSegment.get_matching_transforms

   .. automethod:: PitchClassSegment.get_transforms

   .. automethod:: PitchClassSegment.has_duplicates

   .. automethod:: PitchClassSegment.has_repeats

   .. container:: inherited

      .. automethod:: PitchClassSegment.index

   .. container:: inherited

      .. automethod:: PitchClassSegment.invert

   .. container:: inherited

      .. automethod:: PitchClassSegment.make_notes

   .. container:: inherited

      .. automethod:: PitchClassSegment.multiply

   .. container:: inherited

      .. automethod:: PitchClassSegment.permute

   .. container:: inherited

      .. automethod:: PitchClassSegment.retrograde

   .. container:: inherited

      .. automethod:: PitchClassSegment.rotate

   .. automethod:: PitchClassSegment.sequence

   .. automethod:: PitchClassSegment.space_down

   .. automethod:: PitchClassSegment.space_up

   .. container:: inherited

      .. automethod:: PitchClassSegment.to_pitch_classes

   .. container:: inherited

      .. automethod:: PitchClassSegment.to_pitches

   .. container:: inherited

      .. automethod:: PitchClassSegment.transpose

   .. container:: inherited

      .. automethod:: PitchClassSegment.voice_horizontally

   .. container:: inherited

      .. automethod:: PitchClassSegment.voice_vertically

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSegment.from_selection

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchClassSegment.item_class

   .. container:: inherited

      .. autoattribute:: PitchClassSegment.items

.. autoclass:: PitchClassSet

   .. autosummary::
      :nosignatures:

      to_pitch_classes
      to_pitches

   .. autosummary::
      :nosignatures:

      __eq__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSet.__and__

   .. container:: inherited

      .. automethod:: PitchClassSet.__contains__

   .. automethod:: PitchClassSet.__eq__

   .. container:: inherited

      .. automethod:: PitchClassSet.__format__

   .. container:: inherited

      .. automethod:: PitchClassSet.__ge__

   .. container:: inherited

      .. automethod:: PitchClassSet.__gt__

   .. container:: inherited

      .. automethod:: PitchClassSet.__illustrate__

   .. container:: inherited

      .. automethod:: PitchClassSet.__iter__

   .. container:: inherited

      .. automethod:: PitchClassSet.__le__

   .. container:: inherited

      .. automethod:: PitchClassSet.__len__

   .. container:: inherited

      .. automethod:: PitchClassSet.__lt__

   .. container:: inherited

      .. automethod:: PitchClassSet.__or__

   .. container:: inherited

      .. automethod:: PitchClassSet.__rand__

   .. container:: inherited

      .. automethod:: PitchClassSet.__repr__

   .. container:: inherited

      .. automethod:: PitchClassSet.__ror__

   .. container:: inherited

      .. automethod:: PitchClassSet.__rsub__

   .. container:: inherited

      .. automethod:: PitchClassSet.__rxor__

   .. container:: inherited

      .. automethod:: PitchClassSet.__str__

   .. container:: inherited

      .. automethod:: PitchClassSet.__sub__

   .. container:: inherited

      .. automethod:: PitchClassSet.__xor__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSet.copy

   .. container:: inherited

      .. automethod:: PitchClassSet.difference

   .. container:: inherited

      .. automethod:: PitchClassSet.get_normal_order

   .. container:: inherited

      .. automethod:: PitchClassSet.get_prime_form

   .. container:: inherited

      .. automethod:: PitchClassSet.intersection

   .. container:: inherited

      .. automethod:: PitchClassSet.invert

   .. container:: inherited

      .. automethod:: PitchClassSet.is_transposed_subset

   .. container:: inherited

      .. automethod:: PitchClassSet.is_transposed_superset

   .. container:: inherited

      .. automethod:: PitchClassSet.isdisjoint

   .. container:: inherited

      .. automethod:: PitchClassSet.issubset

   .. container:: inherited

      .. automethod:: PitchClassSet.issuperset

   .. container:: inherited

      .. automethod:: PitchClassSet.multiply

   .. container:: inherited

      .. automethod:: PitchClassSet.order_by

   .. container:: inherited

      .. automethod:: PitchClassSet.symmetric_difference

   .. automethod:: PitchClassSet.to_pitch_classes

   .. automethod:: PitchClassSet.to_pitches

   .. container:: inherited

      .. automethod:: PitchClassSet.transpose

   .. container:: inherited

      .. automethod:: PitchClassSet.union

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSet.from_selection

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchClassSet.cardinality

   .. container:: inherited

      .. autoattribute:: PitchClassSet.item_class

   .. container:: inherited

      .. autoattribute:: PitchClassSet.items

.. autoclass:: PitchSegment

   .. autosummary::
      :nosignatures:

      bass_to_octave
      center_to_octave
      chord
      soprano_to_octave
      space_down
      space_up
      split

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSegment.__add__

   .. container:: inherited

      .. automethod:: PitchSegment.__contains__

   .. container:: inherited

      .. automethod:: PitchSegment.__eq__

   .. container:: inherited

      .. automethod:: PitchSegment.__format__

   .. container:: inherited

      .. automethod:: PitchSegment.__getitem__

   .. container:: inherited

      .. automethod:: PitchSegment.__hash__

   .. container:: inherited

      .. automethod:: PitchSegment.__illustrate__

   .. container:: inherited

      .. automethod:: PitchSegment.__iter__

   .. container:: inherited

      .. automethod:: PitchSegment.__len__

   .. container:: inherited

      .. automethod:: PitchSegment.__mul__

   .. container:: inherited

      .. automethod:: PitchSegment.__radd__

   .. container:: inherited

      .. automethod:: PitchSegment.__repr__

   .. container:: inherited

      .. automethod:: PitchSegment.__reversed__

   .. container:: inherited

      .. automethod:: PitchSegment.__rmul__

   .. container:: inherited

      .. automethod:: PitchSegment.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchSegment.bass_to_octave

   .. automethod:: PitchSegment.center_to_octave

   .. automethod:: PitchSegment.chord

   .. container:: inherited

      .. automethod:: PitchSegment.count

   .. container:: inherited

      .. automethod:: PitchSegment.has_duplicates

   .. container:: inherited

      .. automethod:: PitchSegment.index

   .. container:: inherited

      .. automethod:: PitchSegment.invert

   .. container:: inherited

      .. automethod:: PitchSegment.make_notes

   .. container:: inherited

      .. automethod:: PitchSegment.multiply

   .. container:: inherited

      .. automethod:: PitchSegment.retrograde

   .. container:: inherited

      .. automethod:: PitchSegment.rotate

   .. automethod:: PitchSegment.soprano_to_octave

   .. automethod:: PitchSegment.space_down

   .. automethod:: PitchSegment.space_up

   .. automethod:: PitchSegment.split

   .. container:: inherited

      .. automethod:: PitchSegment.to_pitch_classes

   .. container:: inherited

      .. automethod:: PitchSegment.to_pitches

   .. container:: inherited

      .. automethod:: PitchSegment.transpose

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSegment.from_selection

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchSegment.hertz

   .. container:: inherited

      .. autoattribute:: PitchSegment.inflection_point_count

   .. container:: inherited

      .. autoattribute:: PitchSegment.item_class

   .. container:: inherited

      .. autoattribute:: PitchSegment.items

   .. container:: inherited

      .. autoattribute:: PitchSegment.local_maxima

   .. container:: inherited

      .. autoattribute:: PitchSegment.local_minima

.. autoclass:: PitchSet

   .. autosummary::
      :nosignatures:

      space_down
      space_up
      to_pitch_classes

   .. autosummary::
      :nosignatures:

      __eq__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSet.__and__

   .. container:: inherited

      .. automethod:: PitchSet.__contains__

   .. automethod:: PitchSet.__eq__

   .. container:: inherited

      .. automethod:: PitchSet.__format__

   .. container:: inherited

      .. automethod:: PitchSet.__ge__

   .. container:: inherited

      .. automethod:: PitchSet.__gt__

   .. container:: inherited

      .. automethod:: PitchSet.__illustrate__

   .. container:: inherited

      .. automethod:: PitchSet.__iter__

   .. container:: inherited

      .. automethod:: PitchSet.__le__

   .. container:: inherited

      .. automethod:: PitchSet.__len__

   .. container:: inherited

      .. automethod:: PitchSet.__lt__

   .. container:: inherited

      .. automethod:: PitchSet.__or__

   .. container:: inherited

      .. automethod:: PitchSet.__rand__

   .. container:: inherited

      .. automethod:: PitchSet.__repr__

   .. container:: inherited

      .. automethod:: PitchSet.__ror__

   .. container:: inherited

      .. automethod:: PitchSet.__rsub__

   .. container:: inherited

      .. automethod:: PitchSet.__rxor__

   .. container:: inherited

      .. automethod:: PitchSet.__str__

   .. container:: inherited

      .. automethod:: PitchSet.__sub__

   .. container:: inherited

      .. automethod:: PitchSet.__xor__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSet.copy

   .. container:: inherited

      .. automethod:: PitchSet.difference

   .. container:: inherited

      .. automethod:: PitchSet.intersection

   .. container:: inherited

      .. automethod:: PitchSet.invert

   .. container:: inherited

      .. automethod:: PitchSet.isdisjoint

   .. container:: inherited

      .. automethod:: PitchSet.issubset

   .. container:: inherited

      .. automethod:: PitchSet.issuperset

   .. container:: inherited

      .. automethod:: PitchSet.register

   .. automethod:: PitchSet.space_down

   .. automethod:: PitchSet.space_up

   .. container:: inherited

      .. automethod:: PitchSet.symmetric_difference

   .. automethod:: PitchSet.to_pitch_classes

   .. container:: inherited

      .. automethod:: PitchSet.transpose

   .. container:: inherited

      .. automethod:: PitchSet.union

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSet.from_selection

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchSet.cardinality

   .. container:: inherited

      .. autoattribute:: PitchSet.duplicate_pitch_classes

   .. container:: inherited

      .. autoattribute:: PitchSet.hertz

   .. container:: inherited

      .. autoattribute:: PitchSet.is_pitch_class_unique

   .. container:: inherited

      .. autoattribute:: PitchSet.item_class

   .. container:: inherited

      .. autoattribute:: PitchSet.items

.. autoclass:: PitchTreeSpanner

   .. autosummary::
      :nosignatures:

      level

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__contains__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__copy__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__format__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__getitem__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__iter__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__len__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__lt__

   .. container:: inherited

      .. automethod:: PitchTreeSpanner.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchTreeSpanner.leaves

   .. autoattribute:: PitchTreeSpanner.level

   .. container:: inherited

      .. autoattribute:: PitchTreeSpanner.tweaks

.. autoclass:: ZaggedPitchClassMaker

   .. autosummary::
      :nosignatures:

      division_ratios
      grouping_counts
      pc_cells

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __hash__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ZaggedPitchClassMaker.__call__

   .. automethod:: ZaggedPitchClassMaker.__eq__

   .. container:: inherited

      .. automethod:: ZaggedPitchClassMaker.__format__

   .. automethod:: ZaggedPitchClassMaker.__hash__

   .. container:: inherited

      .. automethod:: ZaggedPitchClassMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ZaggedPitchClassMaker.division_ratios

   .. autoattribute:: ZaggedPitchClassMaker.grouping_counts

   .. autoattribute:: ZaggedPitchClassMaker.pc_cells