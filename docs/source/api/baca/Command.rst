.. _baca--Command:

Command
=======

.. automodule:: baca.Command

.. currentmodule:: baca.Command

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.Command

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Command

.. autoclass:: Command

   .. autosummary::
      :nosignatures:

      get_tag

   .. autosummary::
      :nosignatures:

      deactivate
      selector
      tag
      tags

   .. autosummary::
      :nosignatures:

      manifests
      offset_to_measure_number
      previous_segment_voice_metadata
      score_template
      tag_measure_number

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Command.__call__

   .. container:: inherited

      .. automethod:: Command.__format__

   .. container:: inherited

      .. automethod:: Command.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Command.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. autoattribute:: Command.manifests

   .. autoattribute:: Command.offset_to_measure_number

   .. autoattribute:: Command.previous_segment_voice_metadata

   .. autoattribute:: Command.score_template

   .. autoattribute:: Command.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Command.deactivate

   .. autoattribute:: Command.selector

   .. autoattribute:: Command.tag

   .. autoattribute:: Command.tags

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Map
   ~Suite

.. autoclass:: Map

   .. autosummary::
      :nosignatures:

      commands
      selector

   .. autosummary::
      :nosignatures:

      manifests
      offset_to_measure_number
      previous_segment_voice_metadata
      score_template

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Map.__call__

   .. container:: inherited

      .. automethod:: Map.__format__

   .. container:: inherited

      .. automethod:: Map.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. autoattribute:: Map.manifests

   .. autoattribute:: Map.offset_to_measure_number

   .. autoattribute:: Map.previous_segment_voice_metadata

   .. autoattribute:: Map.score_template

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Map.commands

   .. autoattribute:: Map.selector

.. autoclass:: Suite

   .. autosummary::
      :nosignatures:

      commands

   .. autosummary::
      :nosignatures:

      manifests
      offset_to_measure_number
      previous_segment_voice_metadata
      score_template

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Suite.__call__

   .. container:: inherited

      .. automethod:: Suite.__format__

   .. container:: inherited

      .. automethod:: Suite.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. autoattribute:: Suite.manifests

   .. autoattribute:: Suite.offset_to_measure_number

   .. autoattribute:: Suite.previous_segment_voice_metadata

   .. autoattribute:: Suite.score_template

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Suite.commands