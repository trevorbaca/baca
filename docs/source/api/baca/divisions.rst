.. _baca--divisions:

divisions
=========

.. automodule:: baca.divisions

.. currentmodule:: baca.divisions

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.divisions

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Division
   ~DivisionSequence
   ~DivisionSequenceExpression
   ~FuseByCountsDivisionCallback
   ~SplitByDurationsDivisionCallback
   ~SplitByRoundedRatiosDivisionCallback

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
      payload
      start_offset
      stop_offset
      yield_durations
      yield_equivalent_durations
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

   .. automethod:: Division.yield_equivalent_durations

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

   .. autoattribute:: Division.payload

   .. container:: inherited

      .. autoattribute:: Division.real

   .. autoattribute:: Division.start_offset

   .. autoattribute:: Division.stop_offset

.. autoclass:: DivisionSequence

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      rotate
      show
      split_by_durations
      split_by_rounded_ratios

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

   .. container:: inherited

      .. automethod:: DivisionSequence.split

   .. automethod:: DivisionSequence.split_by_durations

   .. automethod:: DivisionSequence.split_by_rounded_ratios

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

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: DivisionSequence.show

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: DivisionSequence.items

.. autoclass:: DivisionSequenceExpression

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __add__
      __getitem__
      __radd__
      division_sequence
      split_by_durations
      split_by_rounded_ratios

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: DivisionSequenceExpression.__add__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__call__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__eq__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__format__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__getattr__

   .. automethod:: DivisionSequenceExpression.__getitem__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__hash__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__iadd__

   .. automethod:: DivisionSequenceExpression.__radd__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__repr__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__setitem__

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.append_callback

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.color

   .. automethod:: DivisionSequenceExpression.division_sequence

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.establish_equivalence

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.get_markup

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.get_string

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.label

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.pitch_class_segment

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.pitch_set

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.print

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.select

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.sequence

   .. automethod:: DivisionSequenceExpression.split_by_durations

   .. automethod:: DivisionSequenceExpression.split_by_rounded_ratios

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.wrap_in_list

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DivisionSequenceExpression.make_callback

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.argument_values

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.callbacks

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.evaluation_template

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.force_return

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.has_parentheses

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.is_composite

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.is_initializer

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.is_postfix

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.is_selector

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.keywords

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.lone

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.map_operand

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.markup_maker_callback

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.module_names

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.name

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.next_name

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.precedence

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.proxy_class

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.qualified_method_name

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.string_template

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.subclass_hook

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.subexpressions

   .. container:: inherited

      .. autoattribute:: DivisionSequenceExpression.template

.. autoclass:: FuseByCountsDivisionCallback

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      counts
      cyclic

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: FuseByCountsDivisionCallback.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: FuseByCountsDivisionCallback.counts

   .. autoattribute:: FuseByCountsDivisionCallback.cyclic

.. autoclass:: SplitByDurationsDivisionCallback

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      compound_meter_multiplier
      cyclic
      durations
      pattern_rotation_index
      remainder
      remainder_fuse_threshold

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SplitByDurationsDivisionCallback.__call__

   .. automethod:: SplitByDurationsDivisionCallback.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SplitByDurationsDivisionCallback.compound_meter_multiplier

   .. autoattribute:: SplitByDurationsDivisionCallback.cyclic

   .. autoattribute:: SplitByDurationsDivisionCallback.durations

   .. autoattribute:: SplitByDurationsDivisionCallback.pattern_rotation_index

   .. autoattribute:: SplitByDurationsDivisionCallback.remainder

   .. autoattribute:: SplitByDurationsDivisionCallback.remainder_fuse_threshold

.. autoclass:: SplitByRoundedRatiosDivisionCallback

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      ratios

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SplitByRoundedRatiosDivisionCallback.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SplitByRoundedRatiosDivisionCallback.ratios

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~compound_quarter_divisions
   ~fuse_compound_quarter_divisions
   ~split_by_durations
   ~split_by_rounded_ratios
   ~strict_quarter_divisions

.. autofunction:: compound_quarter_divisions

.. autofunction:: fuse_compound_quarter_divisions

.. autofunction:: split_by_durations

.. autofunction:: split_by_rounded_ratios

.. autofunction:: strict_quarter_divisions