.. _baca--classes:

classes
=======

.. automodule:: baca.classes

.. currentmodule:: baca.classes

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.classes

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Counter
   ~Cursor
   ~Expression
   ~PaddedTuple
   ~SchemeManifest
   ~Selection
   ~Sequence
   ~Tree

.. autoclass:: Counter

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      current
      start

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Counter.__call__

   .. automethod:: Counter.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Counter.current

   .. autoattribute:: Counter.start

.. autoclass:: Cursor

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __getitem__
      __hash__
      __iter__
      __len__
      __repr__
      cyclic
      from_pitch_class_segments
      is_exhausted
      next
      position
      reset
      singletons
      source
      suppress_exception

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Cursor.__eq__

   .. automethod:: Cursor.__getitem__

   .. automethod:: Cursor.__hash__

   .. automethod:: Cursor.__iter__

   .. automethod:: Cursor.__len__

   .. automethod:: Cursor.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Cursor.next

   .. automethod:: Cursor.reset

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Cursor.from_pitch_class_segments

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Cursor.cyclic

   .. autoattribute:: Cursor.is_exhausted

   .. autoattribute:: Cursor.position

   .. autoattribute:: Cursor.singletons

   .. autoattribute:: Cursor.source

   .. autoattribute:: Cursor.suppress_exception

.. autoclass:: Expression

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      division_sequence
      pitch_class_segment
      pitch_class_segments
      select

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Expression.__add__

   .. container:: inherited

      .. automethod:: Expression.__call__

   .. container:: inherited

      .. automethod:: Expression.__eq__

   .. container:: inherited

      .. automethod:: Expression.__format__

   .. container:: inherited

      .. automethod:: Expression.__getattr__

   .. container:: inherited

      .. automethod:: Expression.__getitem__

   .. container:: inherited

      .. automethod:: Expression.__hash__

   .. container:: inherited

      .. automethod:: Expression.__iadd__

   .. container:: inherited

      .. automethod:: Expression.__radd__

   .. container:: inherited

      .. automethod:: Expression.__repr__

   .. container:: inherited

      .. automethod:: Expression.__setitem__

   .. container:: inherited

      .. automethod:: Expression.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Expression.append_callback

   .. container:: inherited

      .. automethod:: Expression.color

   .. automethod:: Expression.division_sequence

   .. container:: inherited

      .. automethod:: Expression.establish_equivalence

   .. container:: inherited

      .. automethod:: Expression.get_markup

   .. container:: inherited

      .. automethod:: Expression.get_string

   .. container:: inherited

      .. automethod:: Expression.label

   .. automethod:: Expression.pitch_class_segment

   .. automethod:: Expression.pitch_class_segments

   .. container:: inherited

      .. automethod:: Expression.pitch_set

   .. container:: inherited

      .. automethod:: Expression.print

   .. automethod:: Expression.select

   .. container:: inherited

      .. automethod:: Expression.sequence

   .. container:: inherited

      .. automethod:: Expression.wrap_in_list

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Expression.make_callback

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Expression.argument_values

   .. container:: inherited

      .. autoattribute:: Expression.callbacks

   .. container:: inherited

      .. autoattribute:: Expression.evaluation_template

   .. container:: inherited

      .. autoattribute:: Expression.force_return

   .. container:: inherited

      .. autoattribute:: Expression.has_parentheses

   .. container:: inherited

      .. autoattribute:: Expression.is_composite

   .. container:: inherited

      .. autoattribute:: Expression.is_initializer

   .. container:: inherited

      .. autoattribute:: Expression.is_postfix

   .. container:: inherited

      .. autoattribute:: Expression.is_selector

   .. container:: inherited

      .. autoattribute:: Expression.keywords

   .. container:: inherited

      .. autoattribute:: Expression.lone

   .. container:: inherited

      .. autoattribute:: Expression.map_operand

   .. container:: inherited

      .. autoattribute:: Expression.markup_maker_callback

   .. container:: inherited

      .. autoattribute:: Expression.module_names

   .. container:: inherited

      .. autoattribute:: Expression.name

   .. container:: inherited

      .. autoattribute:: Expression.next_name

   .. container:: inherited

      .. autoattribute:: Expression.precedence

   .. container:: inherited

      .. autoattribute:: Expression.proxy_class

   .. container:: inherited

      .. autoattribute:: Expression.qualified_method_name

   .. container:: inherited

      .. autoattribute:: Expression.string_template

   .. container:: inherited

      .. autoattribute:: Expression.subclass_hook

   .. container:: inherited

      .. autoattribute:: Expression.subexpressions

   .. container:: inherited

      .. autoattribute:: Expression.template

.. autoclass:: PaddedTuple

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __contains__
      __eq__
      __getitem__
      __hash__
      __iter__
      __len__
      __repr__
      items
      pad

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PaddedTuple.__contains__

   .. automethod:: PaddedTuple.__eq__

   .. automethod:: PaddedTuple.__getitem__

   .. automethod:: PaddedTuple.__hash__

   .. automethod:: PaddedTuple.__iter__

   .. automethod:: PaddedTuple.__len__

   .. automethod:: PaddedTuple.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PaddedTuple.items

   .. autoattribute:: PaddedTuple.pad

.. autoclass:: SchemeManifest

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      dynamic_to_steady_state
      dynamics

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: SchemeManifest.dynamic_to_steady_state

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SchemeManifest.dynamics

.. autoclass:: Selection

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      chead
      cheads
      clparts
      cmgroups
      enchain
      grace
      graces
      hleaf
      hleaves
      lleaf
      lleak
      lleaves
      lparts
      lt
      ltleaf
      ltleaves
      ltqrun
      ltqruns
      ltrun
      ltruns
      lts
      mgroups
      mleaves
      mmrest
      mmrests
      ntrun
      ntruns
      omgroups
      ompltgroups
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
      rleaf
      rleak
      rleaves
      rmleaves
      rrun
      rruns
      skip
      skips
      tleaf
      tleaves
      wleaf
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

   .. automethod:: Selection.clparts

   .. automethod:: Selection.cmgroups

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

   .. automethod:: Selection.grace

   .. automethod:: Selection.graces

   .. container:: inherited

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

   .. automethod:: Selection.hleaf

   .. automethod:: Selection.hleaves

   .. container:: inherited

      .. automethod:: Selection.index

   .. container:: inherited

      .. automethod:: Selection.leaf

   .. container:: inherited

      .. automethod:: Selection.leaves

   .. automethod:: Selection.lleaf

   .. automethod:: Selection.lleak

   .. automethod:: Selection.lleaves

   .. container:: inherited

      .. automethod:: Selection.logical_ties

   .. automethod:: Selection.lparts

   .. automethod:: Selection.lt

   .. automethod:: Selection.ltleaf

   .. automethod:: Selection.ltleaves

   .. automethod:: Selection.ltqrun

   .. automethod:: Selection.ltqruns

   .. automethod:: Selection.ltrun

   .. automethod:: Selection.ltruns

   .. automethod:: Selection.lts

   .. container:: inherited

      .. automethod:: Selection.map

   .. automethod:: Selection.mgroups

   .. automethod:: Selection.mleaves

   .. automethod:: Selection.mmrest

   .. automethod:: Selection.mmrests

   .. container:: inherited

      .. automethod:: Selection.nontrivial

   .. container:: inherited

      .. automethod:: Selection.note

   .. container:: inherited

      .. automethod:: Selection.notes

   .. automethod:: Selection.ntrun

   .. automethod:: Selection.ntruns

   .. automethod:: Selection.omgroups

   .. automethod:: Selection.ompltgroups

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

   .. automethod:: Selection.rleaf

   .. automethod:: Selection.rleak

   .. automethod:: Selection.rleaves

   .. automethod:: Selection.rmleaves

   .. automethod:: Selection.rrun

   .. automethod:: Selection.rruns

   .. container:: inherited

      .. automethod:: Selection.run

   .. container:: inherited

      .. automethod:: Selection.runs

   .. automethod:: Selection.skip

   .. automethod:: Selection.skips

   .. automethod:: Selection.tleaf

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

   .. automethod:: Selection.wleaf

   .. automethod:: Selection.wleaves

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Selection.items

.. autoclass:: Sequence

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      accumulate
      boustrophedon
      degree_of_rotational_symmetry
      group_by_sign
      helianthate
      partition
      period_of_rotation
      repeat_by
      reveal

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Sequence.__add__

   .. container:: inherited

      .. automethod:: Sequence.__contains__

   .. container:: inherited

      .. automethod:: Sequence.__eq__

   .. container:: inherited

      .. automethod:: Sequence.__format__

   .. container:: inherited

      .. automethod:: Sequence.__getitem__

   .. container:: inherited

      .. automethod:: Sequence.__hash__

   .. container:: inherited

      .. automethod:: Sequence.__iter__

   .. container:: inherited

      .. automethod:: Sequence.__len__

   .. container:: inherited

      .. automethod:: Sequence.__radd__

   .. container:: inherited

      .. automethod:: Sequence.__repr__

   .. container:: inherited

      .. automethod:: Sequence.__reversed__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Sequence.accumulate

   .. automethod:: Sequence.boustrophedon

   .. container:: inherited

      .. automethod:: Sequence.count

   .. automethod:: Sequence.degree_of_rotational_symmetry

   .. container:: inherited

      .. automethod:: Sequence.filter

   .. container:: inherited

      .. automethod:: Sequence.flatten

   .. container:: inherited

      .. automethod:: Sequence.group_by

   .. automethod:: Sequence.group_by_sign

   .. automethod:: Sequence.helianthate

   .. container:: inherited

      .. automethod:: Sequence.index

   .. container:: inherited

      .. automethod:: Sequence.is_decreasing

   .. container:: inherited

      .. automethod:: Sequence.is_increasing

   .. container:: inherited

      .. automethod:: Sequence.is_permutation

   .. container:: inherited

      .. automethod:: Sequence.is_repetition_free

   .. container:: inherited

      .. automethod:: Sequence.join

   .. container:: inherited

      .. automethod:: Sequence.map

   .. container:: inherited

      .. automethod:: Sequence.nwise

   .. automethod:: Sequence.partition

   .. container:: inherited

      .. automethod:: Sequence.partition_by_counts

   .. container:: inherited

      .. automethod:: Sequence.partition_by_ratio_of_lengths

   .. container:: inherited

      .. automethod:: Sequence.partition_by_ratio_of_weights

   .. container:: inherited

      .. automethod:: Sequence.partition_by_weights

   .. automethod:: Sequence.period_of_rotation

   .. container:: inherited

      .. automethod:: Sequence.permute

   .. container:: inherited

      .. automethod:: Sequence.remove

   .. container:: inherited

      .. automethod:: Sequence.remove_repeats

   .. container:: inherited

      .. automethod:: Sequence.repeat

   .. automethod:: Sequence.repeat_by

   .. container:: inherited

      .. automethod:: Sequence.repeat_to_length

   .. container:: inherited

      .. automethod:: Sequence.repeat_to_weight

   .. container:: inherited

      .. automethod:: Sequence.replace

   .. container:: inherited

      .. automethod:: Sequence.replace_at

   .. container:: inherited

      .. automethod:: Sequence.retain

   .. container:: inherited

      .. automethod:: Sequence.retain_pattern

   .. automethod:: Sequence.reveal

   .. container:: inherited

      .. automethod:: Sequence.reverse

   .. container:: inherited

      .. automethod:: Sequence.rotate

   .. container:: inherited

      .. automethod:: Sequence.select

   .. container:: inherited

      .. automethod:: Sequence.sort

   .. container:: inherited

      .. automethod:: Sequence.split

   .. container:: inherited

      .. automethod:: Sequence.sum

   .. container:: inherited

      .. automethod:: Sequence.sum_by_sign

   .. container:: inherited

      .. automethod:: Sequence.truncate

   .. container:: inherited

      .. automethod:: Sequence.weight

   .. container:: inherited

      .. automethod:: Sequence.zip

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Sequence.items

.. autoclass:: Tree

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __contains__
      __eq__
      __format__
      __getitem__
      __hash__
      __len__
      __repr__
      get_payload
      item_class
      items
      iterate

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Tree.__contains__

   .. automethod:: Tree.__eq__

   .. automethod:: Tree.__format__

   .. automethod:: Tree.__getitem__

   .. automethod:: Tree.__hash__

   .. automethod:: Tree.__len__

   .. automethod:: Tree.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Tree.get_payload

   .. automethod:: Tree.iterate

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Tree.item_class

   .. autoattribute:: Tree.items

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~_select
   ~_sequence

.. autofunction:: _select

.. autofunction:: _sequence