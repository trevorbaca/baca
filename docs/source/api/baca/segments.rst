.. _baca--segments:

segments
========

.. automodule:: baca.segments

.. currentmodule:: baca.segments

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.segments

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Job
   ~Momento
   ~Part
   ~PartAssignment
   ~PartManifest
   ~PersistentOverride
   ~Section

.. autoclass:: Job

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      activate
      deactivate
      deactivate_first
      message_zero
      path
      prepend_empty_chord
      skip_file_name
      title

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Job.__call__

   .. automethod:: Job.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Job.activate

   .. autoattribute:: Job.deactivate

   .. autoattribute:: Job.deactivate_first

   .. autoattribute:: Job.message_zero

   .. autoattribute:: Job.path

   .. autoattribute:: Job.prepend_empty_chord

   .. autoattribute:: Job.skip_file_name

   .. autoattribute:: Job.title

.. autoclass:: Momento

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      context
      edition
      manifest
      prototype
      synthetic_offset
      value

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Momento.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Momento.context

   .. autoattribute:: Momento.edition

   .. autoattribute:: Momento.manifest

   .. autoattribute:: Momento.prototype

   .. autoattribute:: Momento.synthetic_offset

   .. autoattribute:: Momento.value

.. autoclass:: Part

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      identifier
      instrument
      member
      name
      number
      section
      section_abbreviation
      zfill

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Part.__eq__

   .. automethod:: Part.__hash__

   .. automethod:: Part.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Part.identifier

   .. autoattribute:: Part.instrument

   .. autoattribute:: Part.member

   .. autoattribute:: Part.name

   .. autoattribute:: Part.number

   .. autoattribute:: Part.section

   .. autoattribute:: Part.section_abbreviation

   .. autoattribute:: Part.zfill

.. autoclass:: PartAssignment

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __contains__
      __eq__
      __hash__
      __iter__
      __repr__
      members
      parts
      section
      token

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PartAssignment.__contains__

   .. automethod:: PartAssignment.__eq__

   .. automethod:: PartAssignment.__hash__

   .. automethod:: PartAssignment.__iter__

   .. automethod:: PartAssignment.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PartAssignment.members

   .. autoattribute:: PartAssignment.parts

   .. autoattribute:: PartAssignment.section

   .. autoattribute:: PartAssignment.token

.. autoclass:: PartManifest

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __iter__
      __len__
      __repr__
      expand
      parts
      sections

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PartManifest.__iter__

   .. automethod:: PartManifest.__len__

   .. automethod:: PartManifest.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PartManifest.expand

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PartManifest.parts

   .. autoattribute:: PartManifest.sections

.. autoclass:: PersistentOverride

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      after
      attribute
      context
      grob
      hide
      persistent
      value

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PersistentOverride.__eq__

   .. automethod:: PersistentOverride.__hash__

   .. automethod:: PersistentOverride.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PersistentOverride.after

   .. autoattribute:: PersistentOverride.attribute

   .. autoattribute:: PersistentOverride.context

   .. autoattribute:: PersistentOverride.grob

   .. autoattribute:: PersistentOverride.hide

   .. autoattribute:: PersistentOverride.persistent

   .. autoattribute:: PersistentOverride.value

.. autoclass:: Section

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      abbreviation
      count
      instrument
      name
      parts

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Section.__eq__

   .. automethod:: Section.__hash__

   .. automethod:: Section.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Section.abbreviation

   .. autoattribute:: Section.count

   .. autoattribute:: Section.instrument

   .. autoattribute:: Section.name

   .. autoattribute:: Section.parts

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~get_measure_profile_metadata
   ~get_part_identifier
   ~get_part_manifest
   ~get_preamble_page_count_overview
   ~get_preamble_partial_score
   ~get_preamble_time_signatures
   ~global_skip_identifiers
   ~part_to_identifiers
   ~path_to_part
   ~remove_lilypond_warnings
   ~score_skeleton

.. autofunction:: get_measure_profile_metadata

.. autofunction:: get_part_identifier

.. autofunction:: get_part_manifest

.. autofunction:: get_preamble_page_count_overview

.. autofunction:: get_preamble_partial_score

.. autofunction:: get_preamble_time_signatures

.. autofunction:: global_skip_identifiers

.. autofunction:: part_to_identifiers

.. autofunction:: path_to_part

.. autofunction:: remove_lilypond_warnings

.. autofunction:: score_skeleton