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
      __format__
      __repr__
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

   .. automethod:: Command.__format__

   .. automethod:: Command.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Command.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Command.deactivate

   .. autoattribute:: Command.map

   .. autoattribute:: Command.match

   .. autoattribute:: Command.measures

   .. autoattribute:: Command.runtime

   .. autoattribute:: Command.scope

   .. autoattribute:: Command.selector

   .. autoattribute:: Command.tag

   .. autoattribute:: Command.tag_measure_number

   .. autoattribute:: Command.tags

.. autoclass:: Scope

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __format__
      __repr__
      measures
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Scope.__format__

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
      __format__
      __iter__
      __repr__
      commands

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Suite.__call__

   .. automethod:: Suite.__format__

   .. automethod:: Suite.__iter__

   .. automethod:: Suite.__repr__

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

      __format__
      __repr__
      scopes
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TimelineScope.__format__

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

   ~chunk
   ~compare_persistent_indicators
   ~new
   ~not_mol
   ~not_parts
   ~not_score
   ~not_segment
   ~only_mol
   ~only_parts
   ~only_score
   ~only_segment
   ~site
   ~suite
   ~tag
   ~timeline

.. autofunction:: chunk

.. autofunction:: compare_persistent_indicators

.. autofunction:: new

.. autofunction:: not_mol

.. autofunction:: not_parts

.. autofunction:: not_score

.. autofunction:: not_segment

.. autofunction:: only_mol

.. autofunction:: only_parts

.. autofunction:: only_score

.. autofunction:: only_segment

.. autofunction:: site

.. autofunction:: suite

.. autofunction:: tag

.. autofunction:: timeline