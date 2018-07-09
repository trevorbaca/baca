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

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

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

      .. autoattribute:: BCPCommand.runtime

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

.. autoclass:: VoltaCommand

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

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

      .. autoattribute:: VoltaCommand.runtime

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

   ~bcps
   ~volta

.. autofunction:: bcps

.. autofunction:: volta