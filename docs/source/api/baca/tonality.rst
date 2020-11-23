.. _baca--tonality:

tonality
========

.. automodule:: baca.tonality

.. currentmodule:: baca.tonality

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.tonality

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~ChordExtent
   ~ChordInversion
   ~ChordQuality
   ~ChordSuspension
   ~RomanNumeral
   ~RootedChordClass
   ~RootlessChordClass

.. autoclass:: ChordExtent

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      name
      number

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ChordExtent.__eq__

   .. automethod:: ChordExtent.__hash__

   .. automethod:: ChordExtent.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ChordExtent.name

   .. autoattribute:: ChordExtent.number

.. autoclass:: ChordInversion

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      extent_to_figured_bass_string
      name
      number
      title

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ChordInversion.__eq__

   .. automethod:: ChordInversion.__hash__

   .. automethod:: ChordInversion.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: ChordInversion.extent_to_figured_bass_string

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ChordInversion.name

   .. autoattribute:: ChordInversion.number

   .. autoattribute:: ChordInversion.title

.. autoclass:: ChordQuality

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      __str__
      is_uppercase
      quality_string

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ChordQuality.__eq__

   .. automethod:: ChordQuality.__hash__

   .. automethod:: ChordQuality.__repr__

   .. automethod:: ChordQuality.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ChordQuality.is_uppercase

   .. autoattribute:: ChordQuality.quality_string

.. autoclass:: ChordSuspension

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      __str__
      chord_name
      figured_bass_pair
      figured_bass_string
      start
      stop
      title_string

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ChordSuspension.__eq__

   .. automethod:: ChordSuspension.__hash__

   .. automethod:: ChordSuspension.__repr__

   .. automethod:: ChordSuspension.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ChordSuspension.chord_name

   .. autoattribute:: ChordSuspension.figured_bass_pair

   .. autoattribute:: ChordSuspension.figured_bass_string

   .. autoattribute:: ChordSuspension.start

   .. autoattribute:: ChordSuspension.stop

   .. autoattribute:: ChordSuspension.title_string

.. autoclass:: RomanNumeral

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      bass_scale_degree
      extent
      figured_bass_string
      from_scale_degree_quality_extent_and_inversion
      inversion
      markup
      quality
      root_scale_degree
      suspension
      symbol

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RomanNumeral.__eq__

   .. automethod:: RomanNumeral.__hash__

   .. automethod:: RomanNumeral.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: RomanNumeral.from_scale_degree_quality_extent_and_inversion

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RomanNumeral.bass_scale_degree

   .. autoattribute:: RomanNumeral.extent

   .. autoattribute:: RomanNumeral.figured_bass_string

   .. autoattribute:: RomanNumeral.inversion

   .. autoattribute:: RomanNumeral.markup

   .. autoattribute:: RomanNumeral.quality

   .. autoattribute:: RomanNumeral.root_scale_degree

   .. autoattribute:: RomanNumeral.suspension

   .. autoattribute:: RomanNumeral.symbol

.. autoclass:: RootedChordClass

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      bass
      cardinality
      cardinality_to_extent
      chord_quality
      extent
      extent_to_cardinality
      extent_to_extent_name
      figured_bass
      inversion
      markup
      quality_pair
      root
      root_string

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RootedChordClass.__and__

   .. container:: inherited

      .. automethod:: RootedChordClass.__class_getitem__

   .. container:: inherited

      .. automethod:: RootedChordClass.__contains__

   .. automethod:: RootedChordClass.__eq__

   .. container:: inherited

      .. automethod:: RootedChordClass.__ge__

   .. container:: inherited

      .. automethod:: RootedChordClass.__gt__

   .. automethod:: RootedChordClass.__hash__

   .. container:: inherited

      .. automethod:: RootedChordClass.__iter__

   .. container:: inherited

      .. automethod:: RootedChordClass.__le__

   .. container:: inherited

      .. automethod:: RootedChordClass.__len__

   .. container:: inherited

      .. automethod:: RootedChordClass.__lt__

   .. container:: inherited

      .. automethod:: RootedChordClass.__or__

   .. container:: inherited

      .. automethod:: RootedChordClass.__rand__

   .. automethod:: RootedChordClass.__repr__

   .. container:: inherited

      .. automethod:: RootedChordClass.__ror__

   .. container:: inherited

      .. automethod:: RootedChordClass.__rsub__

   .. container:: inherited

      .. automethod:: RootedChordClass.__rxor__

   .. container:: inherited

      .. automethod:: RootedChordClass.__str__

   .. container:: inherited

      .. automethod:: RootedChordClass.__sub__

   .. container:: inherited

      .. automethod:: RootedChordClass.__xor__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RootedChordClass.copy

   .. container:: inherited

      .. automethod:: RootedChordClass.difference

   .. container:: inherited

      .. automethod:: RootedChordClass.get_normal_order

   .. container:: inherited

      .. automethod:: RootedChordClass.get_prime_form

   .. container:: inherited

      .. automethod:: RootedChordClass.intersection

   .. container:: inherited

      .. automethod:: RootedChordClass.invert

   .. container:: inherited

      .. automethod:: RootedChordClass.is_transposed_subset

   .. container:: inherited

      .. automethod:: RootedChordClass.is_transposed_superset

   .. container:: inherited

      .. automethod:: RootedChordClass.isdisjoint

   .. container:: inherited

      .. automethod:: RootedChordClass.issubset

   .. container:: inherited

      .. automethod:: RootedChordClass.issuperset

   .. container:: inherited

      .. automethod:: RootedChordClass.multiply

   .. container:: inherited

      .. automethod:: RootedChordClass.order_by

   .. container:: inherited

      .. automethod:: RootedChordClass.symmetric_difference

   .. container:: inherited

      .. automethod:: RootedChordClass.transpose

   .. container:: inherited

      .. automethod:: RootedChordClass.union

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: RootedChordClass.cardinality_to_extent

   .. automethod:: RootedChordClass.extent_to_cardinality

   .. automethod:: RootedChordClass.extent_to_extent_name

   .. container:: inherited

      .. automethod:: RootedChordClass.from_selection

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RootedChordClass.bass

   .. autoattribute:: RootedChordClass.cardinality

   .. autoattribute:: RootedChordClass.chord_quality

   .. autoattribute:: RootedChordClass.extent

   .. autoattribute:: RootedChordClass.figured_bass

   .. autoattribute:: RootedChordClass.inversion

   .. container:: inherited

      .. autoattribute:: RootedChordClass.item_class

   .. container:: inherited

      .. autoattribute:: RootedChordClass.items

   .. autoattribute:: RootedChordClass.markup

   .. autoattribute:: RootedChordClass.quality_pair

   .. autoattribute:: RootedChordClass.root

   .. autoattribute:: RootedChordClass.root_string

.. autoclass:: RootlessChordClass

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      cardinality
      extent
      extent_name
      from_interval_class_segment
      inversion
      position
      quality_string
      rotation

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RootlessChordClass.__add__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__class_getitem__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__contains__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__eq__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__getitem__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__hash__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__iter__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__len__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__mul__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__radd__

   .. automethod:: RootlessChordClass.__repr__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__reversed__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__rmul__

   .. container:: inherited

      .. automethod:: RootlessChordClass.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RootlessChordClass.count

   .. container:: inherited

      .. automethod:: RootlessChordClass.has_duplicates

   .. container:: inherited

      .. automethod:: RootlessChordClass.index

   .. container:: inherited

      .. automethod:: RootlessChordClass.rotate

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: RootlessChordClass.from_interval_class_segment

   .. container:: inherited

      .. automethod:: RootlessChordClass.from_selection

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RootlessChordClass.cardinality

   .. autoattribute:: RootlessChordClass.extent

   .. autoattribute:: RootlessChordClass.extent_name

   .. autoattribute:: RootlessChordClass.inversion

   .. container:: inherited

      .. autoattribute:: RootlessChordClass.item_class

   .. container:: inherited

      .. autoattribute:: RootlessChordClass.items

   .. autoattribute:: RootlessChordClass.position

   .. autoattribute:: RootlessChordClass.quality_string

   .. autoattribute:: RootlessChordClass.rotation

   .. container:: inherited

      .. autoattribute:: RootlessChordClass.slope

   .. container:: inherited

      .. autoattribute:: RootlessChordClass.spread

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~analyze_chords
   ~analyze_incomplete_chords
   ~analyze_incomplete_tonal_functions
   ~analyze_neighbor_notes
   ~analyze_passing_tones
   ~analyze_tonal_functions
   ~are_scalar_notes
   ~are_stepwise_ascending_notes
   ~are_stepwise_descending_notes
   ~are_stepwise_notes

.. autofunction:: analyze_chords

.. autofunction:: analyze_incomplete_chords

.. autofunction:: analyze_incomplete_tonal_functions

.. autofunction:: analyze_neighbor_notes

.. autofunction:: analyze_passing_tones

.. autofunction:: analyze_tonal_functions

.. autofunction:: are_scalar_notes

.. autofunction:: are_stepwise_ascending_notes

.. autofunction:: are_stepwise_descending_notes

.. autofunction:: are_stepwise_notes