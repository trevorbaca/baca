.. _baca--pitchcommands:

pitchcommands
=============

.. automodule:: baca.pitchcommands

.. currentmodule:: baca.pitchcommands

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.pitchcommands

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~AccidentalAdjustmentCommand
   ~ClusterCommand
   ~ColorFingeringCommand
   ~DiatonicClusterCommand
   ~Loop
   ~MicrotoneDeviationCommand
   ~OctaveDisplacementCommand
   ~PitchCommand
   ~RegisterCommand
   ~RegisterInterpolationCommand
   ~RegisterToOctaveCommand
   ~StaffPositionCommand
   ~StaffPositionInterpolationCommand

.. autoclass:: AccidentalAdjustmentCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      cautionary
      forced
      parenthesized

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: AccidentalAdjustmentCommand.__call__

   .. container:: inherited

      .. automethod:: AccidentalAdjustmentCommand.__format__

   .. container:: inherited

      .. automethod:: AccidentalAdjustmentCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: AccidentalAdjustmentCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: AccidentalAdjustmentCommand.cautionary

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.deactivate

   .. autoattribute:: AccidentalAdjustmentCommand.forced

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.map

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.match

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.measures

   .. autoattribute:: AccidentalAdjustmentCommand.parenthesized

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.runtime

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.scope

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.selector

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.tag

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: AccidentalAdjustmentCommand.tags

.. autoclass:: ClusterCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      hide_flat_markup
      selector
      start_pitch
      widths

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ClusterCommand.__call__

   .. container:: inherited

      .. automethod:: ClusterCommand.__format__

   .. container:: inherited

      .. automethod:: ClusterCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ClusterCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ClusterCommand.deactivate

   .. autoattribute:: ClusterCommand.hide_flat_markup

   .. container:: inherited

      .. autoattribute:: ClusterCommand.map

   .. container:: inherited

      .. autoattribute:: ClusterCommand.match

   .. container:: inherited

      .. autoattribute:: ClusterCommand.measures

   .. container:: inherited

      .. autoattribute:: ClusterCommand.runtime

   .. container:: inherited

      .. autoattribute:: ClusterCommand.scope

   .. autoattribute:: ClusterCommand.selector

   .. autoattribute:: ClusterCommand.start_pitch

   .. container:: inherited

      .. autoattribute:: ClusterCommand.tag

   .. container:: inherited

      .. autoattribute:: ClusterCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: ClusterCommand.tags

   .. autoattribute:: ClusterCommand.widths

.. autoclass:: ColorFingeringCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      numbers
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ColorFingeringCommand.__call__

   .. container:: inherited

      .. automethod:: ColorFingeringCommand.__format__

   .. container:: inherited

      .. automethod:: ColorFingeringCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ColorFingeringCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.deactivate

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.map

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.match

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.measures

   .. autoattribute:: ColorFingeringCommand.numbers

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.runtime

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.scope

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.selector

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.tag

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: ColorFingeringCommand.tags

   .. autoattribute:: ColorFingeringCommand.tweaks

.. autoclass:: DiatonicClusterCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      widths

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DiatonicClusterCommand.__call__

   .. container:: inherited

      .. automethod:: DiatonicClusterCommand.__format__

   .. container:: inherited

      .. automethod:: DiatonicClusterCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DiatonicClusterCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.deactivate

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.map

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.match

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.measures

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.runtime

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.scope

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.selector

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.tag

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: DiatonicClusterCommand.tags

   .. autoattribute:: DiatonicClusterCommand.widths

.. autoclass:: Loop

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __getitem__
      intervals
      items

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Loop.__contains__

   .. container:: inherited

      .. automethod:: Loop.__eq__

   .. container:: inherited

      .. automethod:: Loop.__format__

   .. automethod:: Loop.__getitem__

   .. container:: inherited

      .. automethod:: Loop.__hash__

   .. container:: inherited

      .. automethod:: Loop.__iter__

   .. container:: inherited

      .. automethod:: Loop.__len__

   .. container:: inherited

      .. automethod:: Loop.__repr__

   .. container:: inherited

      .. automethod:: Loop.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Loop.intervals

   .. autoattribute:: Loop.items

.. autoclass:: MicrotoneDeviationCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      deviations

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: MicrotoneDeviationCommand.__call__

   .. container:: inherited

      .. automethod:: MicrotoneDeviationCommand.__format__

   .. container:: inherited

      .. automethod:: MicrotoneDeviationCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: MicrotoneDeviationCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.deactivate

   .. autoattribute:: MicrotoneDeviationCommand.deviations

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.map

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.match

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.measures

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.runtime

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.scope

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.selector

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.tag

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: MicrotoneDeviationCommand.tags

.. autoclass:: OctaveDisplacementCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      displacements

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: OctaveDisplacementCommand.__call__

   .. container:: inherited

      .. automethod:: OctaveDisplacementCommand.__format__

   .. container:: inherited

      .. automethod:: OctaveDisplacementCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: OctaveDisplacementCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.deactivate

   .. autoattribute:: OctaveDisplacementCommand.displacements

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.map

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.match

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.measures

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.runtime

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.scope

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.selector

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.tag

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: OctaveDisplacementCommand.tags

.. autoclass:: PitchCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      allow_octaves
      allow_out_of_range
      allow_repeats
      allow_repitch
      approximate_pitch
      cyclic
      do_not_transpose
      ignore_incomplete
      parameter
      persist
      pitches
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchCommand.__call__

   .. container:: inherited

      .. automethod:: PitchCommand.__format__

   .. container:: inherited

      .. automethod:: PitchCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchCommand.allow_octaves

   .. autoattribute:: PitchCommand.allow_out_of_range

   .. autoattribute:: PitchCommand.allow_repeats

   .. autoattribute:: PitchCommand.allow_repitch

   .. autoattribute:: PitchCommand.approximate_pitch

   .. autoattribute:: PitchCommand.cyclic

   .. container:: inherited

      .. autoattribute:: PitchCommand.deactivate

   .. autoattribute:: PitchCommand.do_not_transpose

   .. autoattribute:: PitchCommand.ignore_incomplete

   .. container:: inherited

      .. autoattribute:: PitchCommand.map

   .. container:: inherited

      .. autoattribute:: PitchCommand.match

   .. container:: inherited

      .. autoattribute:: PitchCommand.measures

   .. autoattribute:: PitchCommand.parameter

   .. autoattribute:: PitchCommand.persist

   .. autoattribute:: PitchCommand.pitches

   .. container:: inherited

      .. autoattribute:: PitchCommand.runtime

   .. container:: inherited

      .. autoattribute:: PitchCommand.scope

   .. container:: inherited

      .. autoattribute:: PitchCommand.selector

   .. autoattribute:: PitchCommand.state

   .. container:: inherited

      .. autoattribute:: PitchCommand.tag

   .. container:: inherited

      .. autoattribute:: PitchCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: PitchCommand.tags

.. autoclass:: RegisterCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      registration

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

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

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterCommand.deactivate

   .. container:: inherited

      .. autoattribute:: RegisterCommand.map

   .. container:: inherited

      .. autoattribute:: RegisterCommand.match

   .. container:: inherited

      .. autoattribute:: RegisterCommand.measures

   .. autoattribute:: RegisterCommand.registration

   .. container:: inherited

      .. autoattribute:: RegisterCommand.runtime

   .. container:: inherited

      .. autoattribute:: RegisterCommand.scope

   .. container:: inherited

      .. autoattribute:: RegisterCommand.selector

   .. container:: inherited

      .. autoattribute:: RegisterCommand.tag

   .. container:: inherited

      .. autoattribute:: RegisterCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: RegisterCommand.tags

.. autoclass:: RegisterInterpolationCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      selector
      start_pitch
      stop_pitch

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

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

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.deactivate

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.map

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.match

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.measures

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.runtime

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.scope

   .. autoattribute:: RegisterInterpolationCommand.selector

   .. autoattribute:: RegisterInterpolationCommand.start_pitch

   .. autoattribute:: RegisterInterpolationCommand.stop_pitch

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.tag

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: RegisterInterpolationCommand.tags

.. autoclass:: RegisterToOctaveCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      anchor
      octave_number

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

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

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RegisterToOctaveCommand.anchor

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.deactivate

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.map

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.match

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.measures

   .. autoattribute:: RegisterToOctaveCommand.octave_number

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.runtime

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.scope

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.selector

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.tag

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: RegisterToOctaveCommand.tags

.. autoclass:: StaffPositionCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      allow_out_of_range
      allow_repeats
      approximate_pitch
      exact
      numbers
      set_chord_pitches_equal

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: StaffPositionCommand.__call__

   .. container:: inherited

      .. automethod:: StaffPositionCommand.__format__

   .. container:: inherited

      .. automethod:: StaffPositionCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: StaffPositionCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: StaffPositionCommand.allow_out_of_range

   .. autoattribute:: StaffPositionCommand.allow_repeats

   .. autoattribute:: StaffPositionCommand.approximate_pitch

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.deactivate

   .. autoattribute:: StaffPositionCommand.exact

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.map

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.match

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.measures

   .. autoattribute:: StaffPositionCommand.numbers

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.runtime

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.scope

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.selector

   .. autoattribute:: StaffPositionCommand.set_chord_pitches_equal

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.tag

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: StaffPositionCommand.tags

.. autoclass:: StaffPositionInterpolationCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      approximate_pitch
      start
      stop

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: StaffPositionInterpolationCommand.__call__

   .. container:: inherited

      .. automethod:: StaffPositionInterpolationCommand.__format__

   .. container:: inherited

      .. automethod:: StaffPositionInterpolationCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: StaffPositionInterpolationCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: StaffPositionInterpolationCommand.approximate_pitch

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.deactivate

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.map

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.match

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.measures

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.runtime

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.scope

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.selector

   .. autoattribute:: StaffPositionInterpolationCommand.start

   .. autoattribute:: StaffPositionInterpolationCommand.stop

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.tag

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: StaffPositionInterpolationCommand.tags

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~bass_to_octave
   ~center_to_octave
   ~clusters
   ~color_fingerings
   ~deviation
   ~diatonic_clusters
   ~displacement
   ~force_accidental
   ~interpolate_staff_positions
   ~loop
   ~natural_clusters
   ~pitch
   ~pitches
   ~register
   ~soprano_to_octave
   ~staff_position
   ~staff_positions

.. autofunction:: bass_to_octave

.. autofunction:: center_to_octave

.. autofunction:: clusters

.. autofunction:: color_fingerings

.. autofunction:: deviation

.. autofunction:: diatonic_clusters

.. autofunction:: displacement

.. autofunction:: force_accidental

.. autofunction:: interpolate_staff_positions

.. autofunction:: loop

.. autofunction:: natural_clusters

.. autofunction:: pitch

.. autofunction:: pitches

.. autofunction:: register

.. autofunction:: soprano_to_octave

.. autofunction:: staff_position

.. autofunction:: staff_positions