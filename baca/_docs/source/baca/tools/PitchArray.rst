.. currentmodule:: baca.tools

PitchArray
==========

.. autoclass:: PitchArray

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~baca.tools.PitchArray.PitchArray.append_column
      ~baca.tools.PitchArray.PitchArray.append_row
      ~baca.tools.PitchArray.PitchArray.apply_pitches_by_row
      ~baca.tools.PitchArray.PitchArray.cell_tokens_by_row
      ~baca.tools.PitchArray.PitchArray.cell_widths_by_row
      ~baca.tools.PitchArray.PitchArray.cells
      ~baca.tools.PitchArray.PitchArray.columns
      ~baca.tools.PitchArray.PitchArray.copy_subarray
      ~baca.tools.PitchArray.PitchArray.depth
      ~baca.tools.PitchArray.PitchArray.dimensions
      ~baca.tools.PitchArray.PitchArray.from_counts
      ~baca.tools.PitchArray.PitchArray.from_score
      ~baca.tools.PitchArray.PitchArray.has_spanning_cell_over_index
      ~baca.tools.PitchArray.PitchArray.has_voice_crossing
      ~baca.tools.PitchArray.PitchArray.is_rectangular
      ~baca.tools.PitchArray.PitchArray.list_nonspanning_subarrays
      ~baca.tools.PitchArray.PitchArray.pad_to_depth
      ~baca.tools.PitchArray.PitchArray.pad_to_width
      ~baca.tools.PitchArray.PitchArray.pitches
      ~baca.tools.PitchArray.PitchArray.pitches_by_row
      ~baca.tools.PitchArray.PitchArray.pop_column
      ~baca.tools.PitchArray.PitchArray.pop_row
      ~baca.tools.PitchArray.PitchArray.remove_row
      ~baca.tools.PitchArray.PitchArray.rows
      ~baca.tools.PitchArray.PitchArray.size
      ~baca.tools.PitchArray.PitchArray.to_measures
      ~baca.tools.PitchArray.PitchArray.voice_crossing_count
      ~baca.tools.PitchArray.PitchArray.weight
      ~baca.tools.PitchArray.PitchArray.width
      ~baca.tools.PitchArray.PitchArray.__add__
      ~baca.tools.PitchArray.PitchArray.__contains__
      ~baca.tools.PitchArray.PitchArray.__copy__
      ~baca.tools.PitchArray.PitchArray.__eq__
      ~baca.tools.PitchArray.PitchArray.__format__
      ~baca.tools.PitchArray.PitchArray.__getitem__
      ~baca.tools.PitchArray.PitchArray.__hash__
      ~baca.tools.PitchArray.PitchArray.__iadd__
      ~baca.tools.PitchArray.PitchArray.__ne__
      ~baca.tools.PitchArray.PitchArray.__repr__
      ~baca.tools.PitchArray.PitchArray.__setitem__
      ~baca.tools.PitchArray.PitchArray.__str__

Read-only properties
--------------------

.. autoattribute:: baca.tools.PitchArray.PitchArray.cell_tokens_by_row

.. autoattribute:: baca.tools.PitchArray.PitchArray.cell_widths_by_row

.. autoattribute:: baca.tools.PitchArray.PitchArray.cells

.. autoattribute:: baca.tools.PitchArray.PitchArray.columns

.. autoattribute:: baca.tools.PitchArray.PitchArray.depth

.. autoattribute:: baca.tools.PitchArray.PitchArray.dimensions

.. autoattribute:: baca.tools.PitchArray.PitchArray.has_voice_crossing

.. autoattribute:: baca.tools.PitchArray.PitchArray.is_rectangular

.. autoattribute:: baca.tools.PitchArray.PitchArray.pitches

.. autoattribute:: baca.tools.PitchArray.PitchArray.pitches_by_row

.. autoattribute:: baca.tools.PitchArray.PitchArray.rows

.. autoattribute:: baca.tools.PitchArray.PitchArray.size

.. autoattribute:: baca.tools.PitchArray.PitchArray.voice_crossing_count

.. autoattribute:: baca.tools.PitchArray.PitchArray.weight

.. autoattribute:: baca.tools.PitchArray.PitchArray.width

Methods
-------

.. automethod:: baca.tools.PitchArray.PitchArray.append_column

.. automethod:: baca.tools.PitchArray.PitchArray.append_row

.. automethod:: baca.tools.PitchArray.PitchArray.apply_pitches_by_row

.. automethod:: baca.tools.PitchArray.PitchArray.copy_subarray

.. automethod:: baca.tools.PitchArray.PitchArray.has_spanning_cell_over_index

.. automethod:: baca.tools.PitchArray.PitchArray.list_nonspanning_subarrays

.. automethod:: baca.tools.PitchArray.PitchArray.pad_to_depth

.. automethod:: baca.tools.PitchArray.PitchArray.pad_to_width

.. automethod:: baca.tools.PitchArray.PitchArray.pop_column

.. automethod:: baca.tools.PitchArray.PitchArray.pop_row

.. automethod:: baca.tools.PitchArray.PitchArray.remove_row

.. automethod:: baca.tools.PitchArray.PitchArray.to_measures

Class & static methods
----------------------

.. automethod:: baca.tools.PitchArray.PitchArray.from_counts

.. automethod:: baca.tools.PitchArray.PitchArray.from_score

Special methods
---------------

.. automethod:: baca.tools.PitchArray.PitchArray.__add__

.. automethod:: baca.tools.PitchArray.PitchArray.__contains__

.. automethod:: baca.tools.PitchArray.PitchArray.__copy__

.. automethod:: baca.tools.PitchArray.PitchArray.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.PitchArray.PitchArray.__format__

.. automethod:: baca.tools.PitchArray.PitchArray.__getitem__

.. automethod:: baca.tools.PitchArray.PitchArray.__hash__

.. automethod:: baca.tools.PitchArray.PitchArray.__iadd__

.. automethod:: baca.tools.PitchArray.PitchArray.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.PitchArray.PitchArray.__repr__

.. automethod:: baca.tools.PitchArray.PitchArray.__setitem__

.. automethod:: baca.tools.PitchArray.PitchArray.__str__
