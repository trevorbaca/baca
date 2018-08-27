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
   ~Scope
   ~Suite
   ~TimelineScope

.. autoclass:: Command

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      deactivate
      get_tag
      map
      match
      measures
      runtime
      scope
      selector
      tag
      tag_measure_number
      tags

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

   .. autoattribute:: Command.map

   .. autoattribute:: Command.match

   .. autoattribute:: Command.measures

   .. autoattribute:: Command.scope

   .. autoattribute:: Command.selector

   .. autoattribute:: Command.tag

   .. autoattribute:: Command.tags

.. autoclass:: Scope

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      measures
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

   .. autoattribute:: Scope.measures

   .. autoattribute:: Scope.voice_name

.. autoclass:: Suite

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __iter__
      commands
      runtime

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Suite.__call__

   .. container:: inherited

      .. automethod:: Suite.__format__

   .. automethod:: Suite.__iter__

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

.. autoclass:: TimelineScope

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

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

   ~compare_persistent_indicators
   ~new
   ~not_parts
   ~not_score
   ~not_segment
   ~only_parts
   ~only_score
   ~only_segment
   ~suite
   ~tag
   ~timeline

.. autofunction:: compare_persistent_indicators

.. autofunction:: new

.. autofunction:: not_parts

.. autofunction:: not_score

.. autofunction:: not_segment

.. autofunction:: only_parts

.. autofunction:: only_score

.. autofunction:: only_segment

.. autofunction:: suite

.. autofunction:: tag

.. autofunction:: timeline