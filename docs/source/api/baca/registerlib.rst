.. _baca--registerlib:

registerlib
===========

.. automodule:: baca.registerlib

.. currentmodule:: baca.registerlib

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.registerlib

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: section-header

.. autosummary::
   :nosignatures:

   ~RegisterCommand
   ~RegisterInterpolationCommand
   ~RegisterToOctaveCommand

.. autoclass:: RegisterCommand

   .. autosummary::
      :nosignatures:

      registration

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RegisterCommand.__call__

   .. container:: inherited

      .. automethod:: RegisterCommand.__format__

   .. container:: inherited

      .. automethod:: RegisterCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RegisterCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterCommand.runtime

   .. container:: inherited

      .. autoattribute:: RegisterCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterCommand.deactivate

   .. autoattribute:: RegisterCommand.registration

   .. container:: inherited

      .. autoattribute:: RegisterCommand.selector

   .. container:: inherited

      .. autoattribute:: RegisterCommand.tag

   .. container:: inherited

      .. autoattribute:: RegisterCommand.tags

.. autoclass:: RegisterInterpolationCommand

   .. autosummary::
      :nosignatures:

      selector
      start_pitch
      stop_pitch

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RegisterInterpolationCommand.__call__

   .. container:: inherited

      .. automethod:: RegisterInterpolationCommand.__format__

   .. container:: inherited

      .. automethod:: RegisterInterpolationCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RegisterInterpolationCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.runtime

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.deactivate

   .. autoattribute:: RegisterInterpolationCommand.selector

   .. autoattribute:: RegisterInterpolationCommand.start_pitch

   .. autoattribute:: RegisterInterpolationCommand.stop_pitch

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.tag

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.tags

.. autoclass:: RegisterToOctaveCommand

   .. autosummary::
      :nosignatures:

      anchor
      octave_number

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RegisterToOctaveCommand.__call__

   .. container:: inherited

      .. automethod:: RegisterToOctaveCommand.__format__

   .. container:: inherited

      .. automethod:: RegisterToOctaveCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RegisterToOctaveCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.runtime

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RegisterToOctaveCommand.anchor

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.deactivate

   .. autoattribute:: RegisterToOctaveCommand.octave_number

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.selector

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.tag

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.tags

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Registration
   ~RegistrationComponent

.. autoclass:: Registration

   .. autosummary::
      :nosignatures:

      components

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Registration.__call__

   .. container:: inherited

      .. automethod:: Registration.__copy__

   .. container:: inherited

      .. automethod:: Registration.__eq__

   .. container:: inherited

      .. automethod:: Registration.__format__

   .. container:: inherited

      .. automethod:: Registration.__hash__

   .. container:: inherited

      .. automethod:: Registration.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Registration.components

.. autoclass:: RegistrationComponent

   .. autosummary::
      :nosignatures:

      source_pitch_range
      target_octave_start_pitch

   .. autosummary::
      :nosignatures:

      __eq__
      __format__
      __hash__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RegistrationComponent.__copy__

   .. automethod:: RegistrationComponent.__eq__

   .. automethod:: RegistrationComponent.__format__

   .. automethod:: RegistrationComponent.__hash__

   .. container:: inherited

      .. automethod:: RegistrationComponent.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RegistrationComponent.source_pitch_range

   .. autoattribute:: RegistrationComponent.target_octave_start_pitch

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~bass_to_octave
   ~center_to_octave
   ~register
   ~soprano_to_octave

.. autofunction:: bass_to_octave

.. autofunction:: center_to_octave

.. autofunction:: register

.. autofunction:: soprano_to_octave