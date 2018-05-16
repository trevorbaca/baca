.. _baca--tools--PitchArray:

PitchArray
==========

.. automodule:: baca.tools.PitchArray

.. currentmodule:: baca.tools.PitchArray

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.tools.PitchArray

.. autoclass:: PitchArray

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchArray.__add__

   .. automethod:: PitchArray.__contains__

   .. automethod:: PitchArray.__copy__

   .. automethod:: PitchArray.__eq__

   .. automethod:: PitchArray.__format__

   .. automethod:: PitchArray.__getitem__

   .. automethod:: PitchArray.__hash__

   .. automethod:: PitchArray.__iadd__

   .. automethod:: PitchArray.__ne__

   .. automethod:: PitchArray.__repr__

   .. automethod:: PitchArray.__setitem__

   .. automethod:: PitchArray.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchArray.append_column

   .. automethod:: PitchArray.append_row

   .. automethod:: PitchArray.apply_pitches_by_row

   .. automethod:: PitchArray.copy_subarray

   .. automethod:: PitchArray.has_spanning_cell_over_index

   .. automethod:: PitchArray.list_nonspanning_subarrays

   .. automethod:: PitchArray.pad_to_depth

   .. automethod:: PitchArray.pad_to_width

   .. automethod:: PitchArray.pop_column

   .. automethod:: PitchArray.pop_row

   .. automethod:: PitchArray.remove_row

   .. automethod:: PitchArray.to_measures

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: PitchArray.from_counts

   .. automethod:: PitchArray.from_score

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchArray.cell_tokens_by_row

   .. autoattribute:: PitchArray.cell_widths_by_row

   .. autoattribute:: PitchArray.cells

   .. autoattribute:: PitchArray.columns

   .. autoattribute:: PitchArray.depth

   .. autoattribute:: PitchArray.dimensions

   .. autoattribute:: PitchArray.has_voice_crossing

   .. autoattribute:: PitchArray.is_rectangular

   .. autoattribute:: PitchArray.pitches

   .. autoattribute:: PitchArray.pitches_by_row

   .. autoattribute:: PitchArray.rows

   .. autoattribute:: PitchArray.size

   .. autoattribute:: PitchArray.voice_crossing_count

   .. autoattribute:: PitchArray.weight

   .. autoattribute:: PitchArray.width