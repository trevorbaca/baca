.. _baca--commandclasses:

commandclasses
==============

.. automodule:: baca.commandclasses

.. currentmodule:: baca.commandclasses

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.commandclasses

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~BCPCommand
   ~ColorCommand
   ~ContainerCommand
   ~DetachCommand
   ~GlissandoCommand
   ~GlobalFermataCommand
   ~IndicatorCommand
   ~InstrumentChangeCommand
   ~LabelCommand
   ~MetronomeMarkCommand
   ~PartAssignmentCommand

.. autoclass:: BCPCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      bcps
      bow_change_tweaks
      final_spanner
      helper
      start_command
      stop_command
      tag
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: BCPCommand.__call__

   .. container:: inherited

      .. automethod:: BCPCommand.__format__

   .. container:: inherited

      .. automethod:: BCPCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: BCPCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: BCPCommand.bcps

   .. autoattribute:: BCPCommand.bow_change_tweaks

   .. container:: inherited

      .. autoattribute:: BCPCommand.deactivate

   .. autoattribute:: BCPCommand.final_spanner

   .. autoattribute:: BCPCommand.helper

   .. container:: inherited

      .. autoattribute:: BCPCommand.map

   .. container:: inherited

      .. autoattribute:: BCPCommand.match

   .. container:: inherited

      .. autoattribute:: BCPCommand.measures

   .. container:: inherited

      .. autoattribute:: BCPCommand.runtime

   .. container:: inherited

      .. autoattribute:: BCPCommand.scope

   .. container:: inherited

      .. autoattribute:: BCPCommand.selector

   .. autoattribute:: BCPCommand.start_command

   .. autoattribute:: BCPCommand.stop_command

   .. autoattribute:: BCPCommand.tag

   .. container:: inherited

      .. autoattribute:: BCPCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: BCPCommand.tags

   .. autoattribute:: BCPCommand.tweaks

.. autoclass:: ColorCommand

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ColorCommand.__call__

   .. container:: inherited

      .. automethod:: ColorCommand.__format__

   .. container:: inherited

      .. automethod:: ColorCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ColorCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ColorCommand.deactivate

   .. container:: inherited

      .. autoattribute:: ColorCommand.map

   .. container:: inherited

      .. autoattribute:: ColorCommand.match

   .. container:: inherited

      .. autoattribute:: ColorCommand.measures

   .. container:: inherited

      .. autoattribute:: ColorCommand.runtime

   .. container:: inherited

      .. autoattribute:: ColorCommand.scope

   .. container:: inherited

      .. autoattribute:: ColorCommand.selector

   .. container:: inherited

      .. autoattribute:: ColorCommand.tag

   .. container:: inherited

      .. autoattribute:: ColorCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: ColorCommand.tags

.. autoclass:: ContainerCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      identifier

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ContainerCommand.__call__

   .. container:: inherited

      .. automethod:: ContainerCommand.__format__

   .. container:: inherited

      .. automethod:: ContainerCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ContainerCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ContainerCommand.deactivate

   .. autoattribute:: ContainerCommand.identifier

   .. container:: inherited

      .. autoattribute:: ContainerCommand.map

   .. container:: inherited

      .. autoattribute:: ContainerCommand.match

   .. container:: inherited

      .. autoattribute:: ContainerCommand.measures

   .. container:: inherited

      .. autoattribute:: ContainerCommand.runtime

   .. container:: inherited

      .. autoattribute:: ContainerCommand.scope

   .. container:: inherited

      .. autoattribute:: ContainerCommand.selector

   .. container:: inherited

      .. autoattribute:: ContainerCommand.tag

   .. container:: inherited

      .. autoattribute:: ContainerCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: ContainerCommand.tags

.. autoclass:: DetachCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      arguments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DetachCommand.__call__

   .. container:: inherited

      .. automethod:: DetachCommand.__format__

   .. container:: inherited

      .. automethod:: DetachCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DetachCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: DetachCommand.arguments

   .. container:: inherited

      .. autoattribute:: DetachCommand.deactivate

   .. container:: inherited

      .. autoattribute:: DetachCommand.map

   .. container:: inherited

      .. autoattribute:: DetachCommand.match

   .. container:: inherited

      .. autoattribute:: DetachCommand.measures

   .. container:: inherited

      .. autoattribute:: DetachCommand.runtime

   .. container:: inherited

      .. autoattribute:: DetachCommand.scope

   .. container:: inherited

      .. autoattribute:: DetachCommand.selector

   .. container:: inherited

      .. autoattribute:: DetachCommand.tag

   .. container:: inherited

      .. autoattribute:: DetachCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: DetachCommand.tags

.. autoclass:: GlissandoCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      allow_repeats
      allow_ties
      hide_middle_note_heads
      hide_middle_stems
      hide_stem_selector
      left_broken
      parenthesize_repeats
      right_broken
      right_broken_show_next
      tweaks
      zero_padding

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: GlissandoCommand.__call__

   .. container:: inherited

      .. automethod:: GlissandoCommand.__format__

   .. container:: inherited

      .. automethod:: GlissandoCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: GlissandoCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: GlissandoCommand.allow_repeats

   .. autoattribute:: GlissandoCommand.allow_ties

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.deactivate

   .. autoattribute:: GlissandoCommand.hide_middle_note_heads

   .. autoattribute:: GlissandoCommand.hide_middle_stems

   .. autoattribute:: GlissandoCommand.hide_stem_selector

   .. autoattribute:: GlissandoCommand.left_broken

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.map

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.match

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.measures

   .. autoattribute:: GlissandoCommand.parenthesize_repeats

   .. autoattribute:: GlissandoCommand.right_broken

   .. autoattribute:: GlissandoCommand.right_broken_show_next

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.runtime

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.scope

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.selector

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.tag

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: GlissandoCommand.tags

   .. autoattribute:: GlissandoCommand.tweaks

   .. autoattribute:: GlissandoCommand.zero_padding

.. autoclass:: GlobalFermataCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      description
      description_to_command

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: GlobalFermataCommand.__call__

   .. container:: inherited

      .. automethod:: GlobalFermataCommand.__format__

   .. container:: inherited

      .. automethod:: GlobalFermataCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: GlobalFermataCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.deactivate

   .. autoattribute:: GlobalFermataCommand.description

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.map

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.match

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.measures

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.runtime

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.scope

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.selector

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.tag

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.tags

.. autoclass:: IndicatorCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      context
      do_not_test
      indicators
      predicate
      redundant
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: IndicatorCommand.__call__

   .. container:: inherited

      .. automethod:: IndicatorCommand.__format__

   .. container:: inherited

      .. automethod:: IndicatorCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: IndicatorCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: IndicatorCommand.context

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.deactivate

   .. autoattribute:: IndicatorCommand.do_not_test

   .. autoattribute:: IndicatorCommand.indicators

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.map

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.match

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.measures

   .. autoattribute:: IndicatorCommand.predicate

   .. autoattribute:: IndicatorCommand.redundant

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.runtime

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.scope

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.selector

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.tag

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.tags

   .. autoattribute:: IndicatorCommand.tweaks

.. autoclass:: InstrumentChangeCommand

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: InstrumentChangeCommand.__call__

   .. container:: inherited

      .. automethod:: InstrumentChangeCommand.__format__

   .. container:: inherited

      .. automethod:: InstrumentChangeCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: InstrumentChangeCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.context

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.deactivate

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.do_not_test

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.indicators

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.map

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.match

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.measures

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.predicate

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.redundant

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.runtime

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.scope

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.selector

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tag

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tags

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tweaks

.. autoclass:: LabelCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      expression

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: LabelCommand.__call__

   .. container:: inherited

      .. automethod:: LabelCommand.__format__

   .. container:: inherited

      .. automethod:: LabelCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: LabelCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: LabelCommand.deactivate

   .. autoattribute:: LabelCommand.expression

   .. container:: inherited

      .. autoattribute:: LabelCommand.map

   .. container:: inherited

      .. autoattribute:: LabelCommand.match

   .. container:: inherited

      .. autoattribute:: LabelCommand.measures

   .. container:: inherited

      .. autoattribute:: LabelCommand.runtime

   .. container:: inherited

      .. autoattribute:: LabelCommand.scope

   .. container:: inherited

      .. autoattribute:: LabelCommand.selector

   .. container:: inherited

      .. autoattribute:: LabelCommand.tag

   .. container:: inherited

      .. autoattribute:: LabelCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: LabelCommand.tags

.. autoclass:: MetronomeMarkCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      key
      redundant

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: MetronomeMarkCommand.__call__

   .. container:: inherited

      .. automethod:: MetronomeMarkCommand.__format__

   .. container:: inherited

      .. automethod:: MetronomeMarkCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: MetronomeMarkCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.deactivate

   .. autoattribute:: MetronomeMarkCommand.key

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.map

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.match

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.measures

   .. autoattribute:: MetronomeMarkCommand.redundant

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.runtime

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.scope

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.selector

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.tag

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.tags

.. autoclass:: PartAssignmentCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      part_assignment

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PartAssignmentCommand.__call__

   .. container:: inherited

      .. automethod:: PartAssignmentCommand.__format__

   .. container:: inherited

      .. automethod:: PartAssignmentCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PartAssignmentCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.deactivate

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.map

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.match

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.measures

   .. autoattribute:: PartAssignmentCommand.part_assignment

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.runtime

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.scope

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.selector

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.tag

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.tags