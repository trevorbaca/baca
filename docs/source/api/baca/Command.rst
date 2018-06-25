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

      runtime
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

   .. autoattribute:: Command.runtime

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

      runtime

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

   .. autoattribute:: Map.runtime

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

      runtime

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

   .. autoattribute:: Suite.runtime

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Suite.commands