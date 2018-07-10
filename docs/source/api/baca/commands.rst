.. _baca--commands:

commands
========

.. automodule:: baca.commands

.. currentmodule:: baca.commands

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.commands

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~BCPCommand
   ~ColorCommand
   ~ContainerCommand
   ~GlobalFermataCommand
   ~IndicatorCommand
   ~InstrumentChangeCommand
   ~LabelCommand
   ~MetronomeMarkCommand
   ~PartAssignmentCommand
   ~VoltaCommand

.. autoclass:: BCPCommand

   .. autosummary::
      :nosignatures:

      bow_contact_points
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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: BCPCommand.map

   .. container:: inherited

      .. autoattribute:: BCPCommand.measures

   .. container:: inherited

      .. autoattribute:: BCPCommand.runtime

   .. container:: inherited

      .. autoattribute:: BCPCommand.scope

   .. container:: inherited

      .. autoattribute:: BCPCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: BCPCommand.bow_contact_points

   .. container:: inherited

      .. autoattribute:: BCPCommand.deactivate

   .. autoattribute:: BCPCommand.final_spanner

   .. autoattribute:: BCPCommand.helper

   .. container:: inherited

      .. autoattribute:: BCPCommand.selector

   .. autoattribute:: BCPCommand.start_command

   .. autoattribute:: BCPCommand.stop_command

   .. autoattribute:: BCPCommand.tag

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ColorCommand.map

   .. container:: inherited

      .. autoattribute:: ColorCommand.measures

   .. container:: inherited

      .. autoattribute:: ColorCommand.runtime

   .. container:: inherited

      .. autoattribute:: ColorCommand.scope

   .. container:: inherited

      .. autoattribute:: ColorCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ColorCommand.deactivate

   .. container:: inherited

      .. autoattribute:: ColorCommand.selector

   .. container:: inherited

      .. autoattribute:: ColorCommand.tag

   .. container:: inherited

      .. autoattribute:: ColorCommand.tags

.. autoclass:: ContainerCommand

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ContainerCommand.map

   .. container:: inherited

      .. autoattribute:: ContainerCommand.measures

   .. container:: inherited

      .. autoattribute:: ContainerCommand.runtime

   .. container:: inherited

      .. autoattribute:: ContainerCommand.scope

   .. container:: inherited

      .. autoattribute:: ContainerCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ContainerCommand.deactivate

   .. autoattribute:: ContainerCommand.identifier

   .. container:: inherited

      .. autoattribute:: ContainerCommand.selector

   .. container:: inherited

      .. autoattribute:: ContainerCommand.tag

   .. container:: inherited

      .. autoattribute:: ContainerCommand.tags

.. autoclass:: GlobalFermataCommand

   .. autosummary::
      :nosignatures:

      description_to_command

   .. autosummary::
      :nosignatures:

      description

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.map

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.measures

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.runtime

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.scope

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.deactivate

   .. autoattribute:: GlobalFermataCommand.description

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.selector

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.tag

   .. container:: inherited

      .. autoattribute:: GlobalFermataCommand.tags

.. autoclass:: IndicatorCommand

   .. autosummary::
      :nosignatures:

      context
      indicators
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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.map

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.measures

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.runtime

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.scope

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: IndicatorCommand.context

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.deactivate

   .. autoattribute:: IndicatorCommand.indicators

   .. autoattribute:: IndicatorCommand.redundant

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.selector

   .. container:: inherited

      .. autoattribute:: IndicatorCommand.tag

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.map

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.measures

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.runtime

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.scope

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.context

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.deactivate

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.indicators

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.redundant

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.selector

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tag

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tags

   .. container:: inherited

      .. autoattribute:: InstrumentChangeCommand.tweaks

.. autoclass:: LabelCommand

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: LabelCommand.map

   .. container:: inherited

      .. autoattribute:: LabelCommand.measures

   .. container:: inherited

      .. autoattribute:: LabelCommand.runtime

   .. container:: inherited

      .. autoattribute:: LabelCommand.scope

   .. container:: inherited

      .. autoattribute:: LabelCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: LabelCommand.deactivate

   .. autoattribute:: LabelCommand.expression

   .. container:: inherited

      .. autoattribute:: LabelCommand.selector

   .. container:: inherited

      .. autoattribute:: LabelCommand.tag

   .. container:: inherited

      .. autoattribute:: LabelCommand.tags

.. autoclass:: MetronomeMarkCommand

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.map

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.measures

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.runtime

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.scope

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.deactivate

   .. autoattribute:: MetronomeMarkCommand.key

   .. autoattribute:: MetronomeMarkCommand.redundant

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.selector

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.tag

   .. container:: inherited

      .. autoattribute:: MetronomeMarkCommand.tags

.. autoclass:: PartAssignmentCommand

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.map

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.measures

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.runtime

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.scope

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.deactivate

   .. autoattribute:: PartAssignmentCommand.part_assignment

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.selector

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.tag

   .. container:: inherited

      .. autoattribute:: PartAssignmentCommand.tags

.. autoclass:: VoltaCommand

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: VoltaCommand.__call__

   .. container:: inherited

      .. automethod:: VoltaCommand.__format__

   .. container:: inherited

      .. automethod:: VoltaCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: VoltaCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: VoltaCommand.map

   .. container:: inherited

      .. autoattribute:: VoltaCommand.measures

   .. container:: inherited

      .. autoattribute:: VoltaCommand.runtime

   .. container:: inherited

      .. autoattribute:: VoltaCommand.scope

   .. container:: inherited

      .. autoattribute:: VoltaCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: VoltaCommand.deactivate

   .. container:: inherited

      .. autoattribute:: VoltaCommand.selector

   .. container:: inherited

      .. autoattribute:: VoltaCommand.tag

   .. container:: inherited

      .. autoattribute:: VoltaCommand.tags

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~allow_octaves
   ~bar_extent_persistent
   ~bcps
   ~color
   ~container
   ~cross_staff
   ~dynamic_down
   ~dynamic_up
   ~edition
   ~global_fermata
   ~instrument
   ~label
   ~markup
   ~metronome_mark
   ~one_voice
   ~parts
   ~previous_metadata
   ~voice_four
   ~voice_one
   ~voice_three
   ~voice_two
   ~volta

.. autofunction:: allow_octaves

.. autofunction:: bar_extent_persistent

.. autofunction:: bcps

.. autofunction:: color

.. autofunction:: container

.. autofunction:: cross_staff

.. autofunction:: dynamic_down

.. autofunction:: dynamic_up

.. autofunction:: edition

.. autofunction:: global_fermata

.. autofunction:: instrument

.. autofunction:: label

.. autofunction:: markup

.. autofunction:: metronome_mark

.. autofunction:: one_voice

.. autofunction:: parts

.. autofunction:: previous_metadata

.. autofunction:: voice_four

.. autofunction:: voice_one

.. autofunction:: voice_three

.. autofunction:: voice_two

.. autofunction:: volta