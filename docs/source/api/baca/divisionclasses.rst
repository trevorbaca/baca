.. _baca--divisionclasses:

divisionclasses
===============

.. automodule:: baca.divisionclasses

.. currentmodule:: baca.divisionclasses

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.divisionclasses

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Division
   ~DivisionSequence

.. autoclass:: Division

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __add__
      __copy__
      __deepcopy__
      __new__
      __str__
      __sub__
      duration
      find_equivalent_durations
      start_offset
      stop_offset
      timespan
      yield_durations
      yield_nonreduced_fractions

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Division.__abs__

   .. automethod:: Division.__add__

   .. container:: inherited

      .. automethod:: Division.__bool__

   .. container:: inherited

      .. automethod:: Division.__ceil__

   .. container:: inherited

      .. automethod:: Division.__complex__

   .. automethod:: Division.__copy__

   .. automethod:: Division.__deepcopy__

   .. container:: inherited

      .. automethod:: Division.__div__

   .. container:: inherited

      .. automethod:: Division.__divmod__

   .. container:: inherited

      .. automethod:: Division.__eq__

   .. container:: inherited

      .. automethod:: Division.__float__

   .. container:: inherited

      .. automethod:: Division.__floor__

   .. container:: inherited

      .. automethod:: Division.__floordiv__

   .. container:: inherited

      .. automethod:: Division.__format__

   .. container:: inherited

      .. automethod:: Division.__ge__

   .. container:: inherited

      .. automethod:: Division.__gt__

   .. container:: inherited

      .. automethod:: Division.__hash__

   .. container:: inherited

      .. automethod:: Division.__le__

   .. container:: inherited

      .. automethod:: Division.__lt__

   .. container:: inherited

      .. automethod:: Division.__mod__

   .. container:: inherited

      .. automethod:: Division.__mul__

   .. container:: inherited

      .. automethod:: Division.__neg__

   .. automethod:: Division.__new__

   .. container:: inherited

      .. automethod:: Division.__pos__

   .. container:: inherited

      .. automethod:: Division.__pow__

   .. container:: inherited

      .. automethod:: Division.__radd__

   .. container:: inherited

      .. automethod:: Division.__rdiv__

   .. container:: inherited

      .. automethod:: Division.__rdivmod__

   .. container:: inherited

      .. automethod:: Division.__repr__

   .. container:: inherited

      .. automethod:: Division.__rfloordiv__

   .. container:: inherited

      .. automethod:: Division.__rmod__

   .. container:: inherited

      .. automethod:: Division.__rmul__

   .. container:: inherited

      .. automethod:: Division.__round__

   .. container:: inherited

      .. automethod:: Division.__rpow__

   .. container:: inherited

      .. automethod:: Division.__rsub__

   .. container:: inherited

      .. automethod:: Division.__rtruediv__

   .. automethod:: Division.__str__

   .. automethod:: Division.__sub__

   .. container:: inherited

      .. automethod:: Division.__truediv__

   .. container:: inherited

      .. automethod:: Division.__trunc__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Division.conjugate

   .. automethod:: Division.find_equivalent_durations

   .. container:: inherited

      .. automethod:: Division.limit_denominator

   .. container:: inherited

      .. automethod:: Division.multiply

   .. container:: inherited

      .. automethod:: Division.multiply_with_cross_cancelation

   .. container:: inherited

      .. automethod:: Division.multiply_without_reducing

   .. container:: inherited

      .. automethod:: Division.reduce

   .. container:: inherited

      .. automethod:: Division.with_denominator

   .. container:: inherited

      .. automethod:: Division.with_multiple_of_denominator

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Division.from_decimal

   .. container:: inherited

      .. automethod:: Division.from_float

   .. automethod:: Division.yield_durations

   .. automethod:: Division.yield_nonreduced_fractions

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Division.denominator

   .. autoattribute:: Division.duration

   .. container:: inherited

      .. autoattribute:: Division.imag

   .. container:: inherited

      .. autoattribute:: Division.numerator

   .. container:: inherited

      .. autoattribute:: Division.pair

   .. container:: inherited

      .. autoattribute:: Division.real

   .. autoattribute:: Division.start_offset

   .. autoattribute:: Division.stop_offset

   .. autoattribute:: Division.timespan

.. autoclass:: DivisionSequence

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      duration
      fuse
      quarters
      ratios_each
      rotate
      split
      split_each
      start_offset
      stop_offset
      timespan

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DivisionSequence.__add__

   .. container:: inherited

      .. automethod:: DivisionSequence.__contains__

   .. container:: inherited

      .. automethod:: DivisionSequence.__eq__

   .. container:: inherited

      .. automethod:: DivisionSequence.__format__

   .. container:: inherited

      .. automethod:: DivisionSequence.__getitem__

   .. container:: inherited

      .. automethod:: DivisionSequence.__hash__

   .. container:: inherited

      .. automethod:: DivisionSequence.__iter__

   .. container:: inherited

      .. automethod:: DivisionSequence.__len__

   .. container:: inherited

      .. automethod:: DivisionSequence.__radd__

   .. container:: inherited

      .. automethod:: DivisionSequence.__repr__

   .. container:: inherited

      .. automethod:: DivisionSequence.__reversed__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DivisionSequence.count

   .. container:: inherited

      .. automethod:: DivisionSequence.filter

   .. container:: inherited

      .. automethod:: DivisionSequence.flatten

   .. automethod:: DivisionSequence.fuse

   .. container:: inherited

      .. automethod:: DivisionSequence.group_by

   .. container:: inherited

      .. automethod:: DivisionSequence.index

   .. container:: inherited

      .. automethod:: DivisionSequence.is_decreasing

   .. container:: inherited

      .. automethod:: DivisionSequence.is_increasing

   .. container:: inherited

      .. automethod:: DivisionSequence.is_permutation

   .. container:: inherited

      .. automethod:: DivisionSequence.is_repetition_free

   .. container:: inherited

      .. automethod:: DivisionSequence.join

   .. container:: inherited

      .. automethod:: DivisionSequence.map

   .. container:: inherited

      .. automethod:: DivisionSequence.nwise

   .. container:: inherited

      .. automethod:: DivisionSequence.partition_by_counts

   .. container:: inherited

      .. automethod:: DivisionSequence.partition_by_ratio_of_lengths

   .. container:: inherited

      .. automethod:: DivisionSequence.partition_by_ratio_of_weights

   .. container:: inherited

      .. automethod:: DivisionSequence.partition_by_weights

   .. container:: inherited

      .. automethod:: DivisionSequence.permute

   .. automethod:: DivisionSequence.quarters

   .. automethod:: DivisionSequence.ratios_each

   .. container:: inherited

      .. automethod:: DivisionSequence.remove

   .. container:: inherited

      .. automethod:: DivisionSequence.remove_repeats

   .. container:: inherited

      .. automethod:: DivisionSequence.repeat

   .. container:: inherited

      .. automethod:: DivisionSequence.repeat_to_length

   .. container:: inherited

      .. automethod:: DivisionSequence.repeat_to_weight

   .. container:: inherited

      .. automethod:: DivisionSequence.replace

   .. container:: inherited

      .. automethod:: DivisionSequence.replace_at

   .. container:: inherited

      .. automethod:: DivisionSequence.retain

   .. container:: inherited

      .. automethod:: DivisionSequence.retain_pattern

   .. container:: inherited

      .. automethod:: DivisionSequence.reverse

   .. automethod:: DivisionSequence.rotate

   .. container:: inherited

      .. automethod:: DivisionSequence.select

   .. container:: inherited

      .. automethod:: DivisionSequence.sort

   .. automethod:: DivisionSequence.split

   .. automethod:: DivisionSequence.split_each

   .. container:: inherited

      .. automethod:: DivisionSequence.sum

   .. container:: inherited

      .. automethod:: DivisionSequence.sum_by_sign

   .. container:: inherited

      .. automethod:: DivisionSequence.truncate

   .. container:: inherited

      .. automethod:: DivisionSequence.weight

   .. container:: inherited

      .. automethod:: DivisionSequence.zip

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: DivisionSequence.duration

   .. container:: inherited

      .. autoattribute:: DivisionSequence.items

   .. autoattribute:: DivisionSequence.start_offset

   .. autoattribute:: DivisionSequence.stop_offset

   .. autoattribute:: DivisionSequence.timespan