.. _baca--scoping:

scoping
=======

.. automodule:: baca.scoping

.. currentmodule:: baca.scoping

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.scoping

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Command
   ~CommandWrapper
   ~Scope
   ~Suite
   ~TimelineScope

.. autoclass:: Command

   .. autosummary::
      :nosignatures:

      get_tag

   .. autosummary::
      :nosignatures:

      deactivate
      measures
      selector
      tag
      tags

   .. autosummary::
      :nosignatures:

      map
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

   .. autoattribute:: Command.map

   .. autoattribute:: Command.runtime

   .. autoattribute:: Command.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Command.deactivate

   .. autoattribute:: Command.measures

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

.. autoclass:: Suite

   .. autosummary::
      :nosignatures:

      commands
      measures

   .. autosummary::
      :nosignatures:

      map
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

   .. autoattribute:: Suite.map

   .. autoattribute:: Suite.runtime

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Suite.commands

   .. autoattribute:: Suite.measures

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

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~apply
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

.. autofunction:: apply

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