.. _baca--Selection:

Selection
=========

.. automodule:: baca.Selection

.. currentmodule:: baca.Selection

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.Selection

.. autoclass:: Selection

   .. autosummary::
      :nosignatures:

      chead
      cheads
      enchain
      group
      lleak
      lleaves
      lt
      ltqrun
      ltqruns
      ltrun
      ltruns
      lts
      ntruns
      phead
      pheads
      pleaf
      pleaves
      plt
      plts
      ptail
      ptails
      ptlt
      ptlts
      qrun
      qruns
      rleak
      rleaves
      rrun
      rruns
      skip
      skips
      tleaves
      wleaves

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Selection.__add__

   .. container:: inherited

      .. automethod:: Selection.__contains__

   .. container:: inherited

      .. automethod:: Selection.__copy__

   .. container:: inherited

      .. automethod:: Selection.__eq__

   .. container:: inherited

      .. automethod:: Selection.__format__

   .. container:: inherited

      .. automethod:: Selection.__getitem__

   .. container:: inherited

      .. automethod:: Selection.__hash__

   .. container:: inherited

      .. automethod:: Selection.__illustrate__

   .. container:: inherited

      .. automethod:: Selection.__iter__

   .. container:: inherited

      .. automethod:: Selection.__len__

   .. container:: inherited

      .. automethod:: Selection.__radd__

   .. container:: inherited

      .. automethod:: Selection.__repr__

   .. container:: inherited

      .. automethod:: Selection.__reversed__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Selection.are_contiguous_logical_voice

   .. container:: inherited

      .. automethod:: Selection.are_contiguous_same_parent

   .. container:: inherited

      .. automethod:: Selection.are_leaves

   .. container:: inherited

      .. automethod:: Selection.are_logical_voice

   .. automethod:: Selection.chead

   .. automethod:: Selection.cheads

   .. container:: inherited

      .. automethod:: Selection.chord

   .. container:: inherited

      .. automethod:: Selection.chords

   .. container:: inherited

      .. automethod:: Selection.components

   .. container:: inherited

      .. automethod:: Selection.count

   .. automethod:: Selection.enchain

   .. container:: inherited

      .. automethod:: Selection.filter

   .. container:: inherited

      .. automethod:: Selection.filter_duration

   .. container:: inherited

      .. automethod:: Selection.filter_length

   .. container:: inherited

      .. automethod:: Selection.filter_pitches

   .. container:: inherited

      .. automethod:: Selection.filter_preprolated

   .. container:: inherited

      .. automethod:: Selection.flatten

   .. automethod:: Selection.group

   .. container:: inherited

      .. automethod:: Selection.group_by

   .. container:: inherited

      .. automethod:: Selection.group_by_contiguity

   .. container:: inherited

      .. automethod:: Selection.group_by_duration

   .. container:: inherited

      .. automethod:: Selection.group_by_length

   .. container:: inherited

      .. automethod:: Selection.group_by_measure

   .. container:: inherited

      .. automethod:: Selection.group_by_pitch

   .. container:: inherited

      .. automethod:: Selection.index

   .. container:: inherited

      .. automethod:: Selection.leaf

   .. container:: inherited

      .. automethod:: Selection.leaves

   .. automethod:: Selection.lleak

   .. automethod:: Selection.lleaves

   .. container:: inherited

      .. automethod:: Selection.logical_ties

   .. automethod:: Selection.lt

   .. automethod:: Selection.ltqrun

   .. automethod:: Selection.ltqruns

   .. automethod:: Selection.ltrun

   .. automethod:: Selection.ltruns

   .. automethod:: Selection.lts

   .. container:: inherited

      .. automethod:: Selection.map

   .. container:: inherited

      .. automethod:: Selection.nontrivial

   .. container:: inherited

      .. automethod:: Selection.note

   .. container:: inherited

      .. automethod:: Selection.notes

   .. automethod:: Selection.ntruns

   .. container:: inherited

      .. automethod:: Selection.partition_by_counts

   .. container:: inherited

      .. automethod:: Selection.partition_by_durations

   .. container:: inherited

      .. automethod:: Selection.partition_by_ratio

   .. automethod:: Selection.phead

   .. automethod:: Selection.pheads

   .. automethod:: Selection.pleaf

   .. automethod:: Selection.pleaves

   .. automethod:: Selection.plt

   .. automethod:: Selection.plts

   .. automethod:: Selection.ptail

   .. automethod:: Selection.ptails

   .. automethod:: Selection.ptlt

   .. automethod:: Selection.ptlts

   .. automethod:: Selection.qrun

   .. automethod:: Selection.qruns

   .. container:: inherited

      .. automethod:: Selection.rest

   .. container:: inherited

      .. automethod:: Selection.rests

   .. automethod:: Selection.rleak

   .. automethod:: Selection.rleaves

   .. automethod:: Selection.rrun

   .. automethod:: Selection.rruns

   .. container:: inherited

      .. automethod:: Selection.run

   .. container:: inherited

      .. automethod:: Selection.runs

   .. automethod:: Selection.skip

   .. automethod:: Selection.skips

   .. automethod:: Selection.tleaves

   .. container:: inherited

      .. automethod:: Selection.top

   .. container:: inherited

      .. automethod:: Selection.tuplet

   .. container:: inherited

      .. automethod:: Selection.tuplets

   .. container:: inherited

      .. automethod:: Selection.with_next_leaf

   .. container:: inherited

      .. automethod:: Selection.with_previous_leaf

   .. automethod:: Selection.wleaves

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Selection.items