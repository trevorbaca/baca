.. _baca--pitcharray:

pitcharray
==========

.. automodule:: baca.pitcharray

.. currentmodule:: baca.pitcharray

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.pitcharray

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~PitchArray
   ~PitchArrayCell
   ~PitchArrayColumn
   ~PitchArrayList
   ~PitchArrayRow

.. autoclass:: PitchArray

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __add__
      __contains__
      __copy__
      __eq__
      __getitem__
      __hash__
      __iadd__
      __ne__
      __repr__
      __setitem__
      __str__
      append_column
      append_row
      apply_pitches_by_row
      cell_tokens_by_row
      cell_widths_by_row
      cells
      columns
      copy_subarray
      depth
      dimensions
      from_counts
      from_score
      has_spanning_cell_over_index
      has_voice_crossing
      is_rectangular
      list_nonspanning_subarrays
      pad_to_depth
      pad_to_width
      pitches
      pitches_by_row
      pop_column
      pop_row
      remove_row
      rows
      size
      to_measures
      voice_crossing_count
      weight
      width

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchArray.__add__

   .. automethod:: PitchArray.__contains__

   .. automethod:: PitchArray.__copy__

   .. automethod:: PitchArray.__eq__

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

.. autoclass:: PitchArrayCell

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__
      append_pitch
      column_indices
      column_start_index
      column_stop_index
      indices
      is_final_in_row
      is_first_in_row
      item
      matches_cell
      next
      parent_array
      parent_column
      parent_row
      pitches
      previous
      row_index
      weight
      width

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchArrayCell.__repr__

   .. automethod:: PitchArrayCell.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchArrayCell.append_pitch

   .. automethod:: PitchArrayCell.matches_cell

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. autoattribute:: PitchArrayCell.pitches

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchArrayCell.column_indices

   .. autoattribute:: PitchArrayCell.column_start_index

   .. autoattribute:: PitchArrayCell.column_stop_index

   .. autoattribute:: PitchArrayCell.indices

   .. autoattribute:: PitchArrayCell.is_final_in_row

   .. autoattribute:: PitchArrayCell.is_first_in_row

   .. autoattribute:: PitchArrayCell.item

   .. autoattribute:: PitchArrayCell.next

   .. autoattribute:: PitchArrayCell.parent_array

   .. autoattribute:: PitchArrayCell.parent_column

   .. autoattribute:: PitchArrayCell.parent_row

   .. autoattribute:: PitchArrayCell.previous

   .. autoattribute:: PitchArrayCell.row_index

   .. autoattribute:: PitchArrayCell.weight

   .. autoattribute:: PitchArrayCell.width

.. autoclass:: PitchArrayColumn

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __getitem__
      __hash__
      __ne__
      __str__
      append
      cell_tokens
      cell_widths
      cells
      column_index
      depth
      dimensions
      extend
      has_voice_crossing
      is_defective
      parent_array
      pitches
      remove_pitches
      start_cells
      start_pitches
      stop_cells
      stop_pitches
      weight
      width

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchArrayColumn.__eq__

   .. automethod:: PitchArrayColumn.__getitem__

   .. automethod:: PitchArrayColumn.__hash__

   .. automethod:: PitchArrayColumn.__ne__

   .. automethod:: PitchArrayColumn.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchArrayColumn.append

   .. automethod:: PitchArrayColumn.extend

   .. automethod:: PitchArrayColumn.remove_pitches

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchArrayColumn.cell_tokens

   .. autoattribute:: PitchArrayColumn.cell_widths

   .. autoattribute:: PitchArrayColumn.cells

   .. autoattribute:: PitchArrayColumn.column_index

   .. autoattribute:: PitchArrayColumn.depth

   .. autoattribute:: PitchArrayColumn.dimensions

   .. autoattribute:: PitchArrayColumn.has_voice_crossing

   .. autoattribute:: PitchArrayColumn.is_defective

   .. autoattribute:: PitchArrayColumn.parent_array

   .. autoattribute:: PitchArrayColumn.pitches

   .. autoattribute:: PitchArrayColumn.start_cells

   .. autoattribute:: PitchArrayColumn.start_pitches

   .. autoattribute:: PitchArrayColumn.stop_cells

   .. autoattribute:: PitchArrayColumn.stop_pitches

   .. autoattribute:: PitchArrayColumn.weight

   .. autoattribute:: PitchArrayColumn.width

.. autoclass:: PitchArrayList

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      to_score

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchArrayList.__class_getitem__

   .. container:: inherited

      .. automethod:: PitchArrayList.__contains__

   .. container:: inherited

      .. automethod:: PitchArrayList.__delitem__

   .. container:: inherited

      .. automethod:: PitchArrayList.__eq__

   .. container:: inherited

      .. automethod:: PitchArrayList.__getitem__

   .. container:: inherited

      .. automethod:: PitchArrayList.__hash__

   .. container:: inherited

      .. automethod:: PitchArrayList.__iadd__

   .. container:: inherited

      .. automethod:: PitchArrayList.__iter__

   .. container:: inherited

      .. automethod:: PitchArrayList.__len__

   .. container:: inherited

      .. automethod:: PitchArrayList.__repr__

   .. container:: inherited

      .. automethod:: PitchArrayList.__reversed__

   .. container:: inherited

      .. automethod:: PitchArrayList.__setitem__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchArrayList.append

   .. container:: inherited

      .. automethod:: PitchArrayList.clear

   .. container:: inherited

      .. automethod:: PitchArrayList.count

   .. container:: inherited

      .. automethod:: PitchArrayList.extend

   .. container:: inherited

      .. automethod:: PitchArrayList.index

   .. container:: inherited

      .. automethod:: PitchArrayList.insert

   .. container:: inherited

      .. automethod:: PitchArrayList.pop

   .. container:: inherited

      .. automethod:: PitchArrayList.remove

   .. container:: inherited

      .. automethod:: PitchArrayList.reverse

   .. container:: inherited

      .. automethod:: PitchArrayList.sort

   .. automethod:: PitchArrayList.to_score

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchArrayList.keep_sorted

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchArrayList.item_class

   .. container:: inherited

      .. autoattribute:: PitchArrayList.items

.. autoclass:: PitchArrayRow

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __add__
      __copy__
      __eq__
      __getitem__
      __hash__
      __iadd__
      __iter__
      __len__
      __ne__
      __repr__
      __str__
      append
      apply_pitches
      cell_tokens
      cell_widths
      cells
      copy_subrow
      depth
      dimensions
      empty_pitches
      extend
      has_spanning_cell_over_index
      index
      is_defective
      is_in_range
      merge
      pad_to_width
      parent_array
      pitch_range
      pitches
      pop
      remove
      row_index
      to_measure
      weight
      width
      withdraw

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchArrayRow.__add__

   .. automethod:: PitchArrayRow.__copy__

   .. automethod:: PitchArrayRow.__eq__

   .. automethod:: PitchArrayRow.__getitem__

   .. automethod:: PitchArrayRow.__hash__

   .. automethod:: PitchArrayRow.__iadd__

   .. automethod:: PitchArrayRow.__iter__

   .. automethod:: PitchArrayRow.__len__

   .. automethod:: PitchArrayRow.__ne__

   .. automethod:: PitchArrayRow.__repr__

   .. automethod:: PitchArrayRow.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchArrayRow.append

   .. automethod:: PitchArrayRow.apply_pitches

   .. automethod:: PitchArrayRow.copy_subrow

   .. automethod:: PitchArrayRow.empty_pitches

   .. automethod:: PitchArrayRow.extend

   .. automethod:: PitchArrayRow.has_spanning_cell_over_index

   .. automethod:: PitchArrayRow.index

   .. automethod:: PitchArrayRow.merge

   .. automethod:: PitchArrayRow.pad_to_width

   .. automethod:: PitchArrayRow.pop

   .. automethod:: PitchArrayRow.remove

   .. automethod:: PitchArrayRow.to_measure

   .. automethod:: PitchArrayRow.withdraw

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. autoattribute:: PitchArrayRow.pitch_range

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchArrayRow.cell_tokens

   .. autoattribute:: PitchArrayRow.cell_widths

   .. autoattribute:: PitchArrayRow.cells

   .. autoattribute:: PitchArrayRow.depth

   .. autoattribute:: PitchArrayRow.dimensions

   .. autoattribute:: PitchArrayRow.is_defective

   .. autoattribute:: PitchArrayRow.is_in_range

   .. autoattribute:: PitchArrayRow.parent_array

   .. autoattribute:: PitchArrayRow.pitches

   .. autoattribute:: PitchArrayRow.row_index

   .. autoattribute:: PitchArrayRow.weight

   .. autoattribute:: PitchArrayRow.width