.. currentmodule:: baca.tools.PitchArray

PitchArray
==========

.. autoclass:: PitchArray

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject.AbjadObject`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~PitchArray.append_column
      ~PitchArray.append_row
      ~PitchArray.apply_pitches_by_row
      ~PitchArray.cell_tokens_by_row
      ~PitchArray.cell_widths_by_row
      ~PitchArray.cells
      ~PitchArray.columns
      ~PitchArray.copy_subarray
      ~PitchArray.depth
      ~PitchArray.dimensions
      ~PitchArray.from_counts
      ~PitchArray.from_score
      ~PitchArray.has_spanning_cell_over_index
      ~PitchArray.has_voice_crossing
      ~PitchArray.is_rectangular
      ~PitchArray.list_nonspanning_subarrays
      ~PitchArray.pad_to_depth
      ~PitchArray.pad_to_width
      ~PitchArray.pitches
      ~PitchArray.pitches_by_row
      ~PitchArray.pop_column
      ~PitchArray.pop_row
      ~PitchArray.remove_row
      ~PitchArray.rows
      ~PitchArray.size
      ~PitchArray.to_measures
      ~PitchArray.voice_crossing_count
      ~PitchArray.weight
      ~PitchArray.width
      ~PitchArray.__add__
      ~PitchArray.__contains__
      ~PitchArray.__copy__
      ~PitchArray.__eq__
      ~PitchArray.__format__
      ~PitchArray.__getitem__
      ~PitchArray.__hash__
      ~PitchArray.__iadd__
      ~PitchArray.__ne__
      ~PitchArray.__repr__
      ~PitchArray.__setitem__
      ~PitchArray.__str__

Read-only properties
--------------------

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

Methods
-------

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

Class & static methods
----------------------

.. automethod:: PitchArray.from_counts

.. automethod:: PitchArray.from_score

Special methods
---------------

.. automethod:: PitchArray.__add__

.. automethod:: PitchArray.__contains__

.. automethod:: PitchArray.__copy__

.. automethod:: PitchArray.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: PitchArray.__format__

.. automethod:: PitchArray.__getitem__

.. automethod:: PitchArray.__hash__

.. automethod:: PitchArray.__iadd__

.. automethod:: PitchArray.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: PitchArray.__repr__

.. automethod:: PitchArray.__setitem__

.. automethod:: PitchArray.__str__
