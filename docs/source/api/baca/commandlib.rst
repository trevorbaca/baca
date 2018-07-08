.. _baca--commandlib:

commandlib
==========

.. automodule:: baca.commandlib

.. currentmodule:: baca.commandlib

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.commandlib

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Command
   ~CommandWrapper

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

.. autoclass:: CommandWrapper

   .. autosummary::
      :nosignatures:

      command
      scope

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: CommandWrapper.__format__

   .. container:: inherited

      .. automethod:: CommandWrapper.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: CommandWrapper.command

   .. autoattribute:: CommandWrapper.scope

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: section-header

.. autosummary::
   :nosignatures:

   ~MeasureWrapper
   ~Scope
   ~TimelineScope

.. autoclass:: MeasureWrapper

   .. autosummary::
      :nosignatures:

      command
      measures

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: MeasureWrapper.__format__

   .. container:: inherited

      .. automethod:: MeasureWrapper.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: MeasureWrapper.command

   .. autoattribute:: MeasureWrapper.measures

.. autoclass:: Scope

   .. autosummary::
      :nosignatures:

      stages
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Scope.__format__

   .. container:: inherited

      .. automethod:: Scope.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Scope.stages

   .. autoattribute:: Scope.voice_name

.. autoclass:: TimelineScope

   .. autosummary::
      :nosignatures:

      scopes
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: TimelineScope.__format__

   .. container:: inherited

      .. automethod:: TimelineScope.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: TimelineScope.scopes

   .. autoattribute:: TimelineScope.voice_name

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

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~map
   ~measures
   ~not_parts
   ~not_score
   ~not_segment
   ~only_parts
   ~only_score
   ~only_segment
   ~pick
   ~scope
   ~suite
   ~tag
   ~timeline

.. autofunction:: map

.. autofunction:: measures

.. autofunction:: not_parts

.. autofunction:: not_score

.. autofunction:: not_segment

.. autofunction:: only_parts

.. autofunction:: only_score

.. autofunction:: only_segment

.. autofunction:: pick

.. autofunction:: scope

.. autofunction:: suite

.. autofunction:: tag

.. autofunction:: timeline