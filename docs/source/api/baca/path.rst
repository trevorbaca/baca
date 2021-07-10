.. _baca--path:

path
====

.. automodule:: baca.path

.. currentmodule:: baca.path

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.path

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Path

.. autoclass:: Path

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      activate
      add_buildspace_metadatum
      add_metadatum
      build
      builds
      contents
      count
      deactivate
      distribution
      etc
      extern
      get_asset_type
      get_files_ending_with
      get_identifier
      get_metadata
      get_metadatum
      get_next_package
      get_next_score
      get_previous_package
      get_previous_score
      get_title
      is__assets
      is__segments
      is_build
      is_builds
      is_buildspace
      is_contents
      is_definitionspace
      is_distribution
      is_etc
      is_external
      is_part
      is_parts
      is_score_build
      is_score_package_path
      is_scores
      is_segment
      is_segments
      is_stylesheets
      is_wrapper
      list_paths
      list_secondary_paths
      remove
      remove_metadatum
      scores
      segments
      sort_segment_names
      stylesheets
      trim
      with_name
      wrapper
      write_metadata_py

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Path.__bytes__

   .. container:: inherited

      .. automethod:: Path.__class_getitem__

   .. container:: inherited

      .. automethod:: Path.__enter__

   .. container:: inherited

      .. automethod:: Path.__eq__

   .. container:: inherited

      .. automethod:: Path.__exit__

   .. container:: inherited

      .. automethod:: Path.__fspath__

   .. container:: inherited

      .. automethod:: Path.__ge__

   .. container:: inherited

      .. automethod:: Path.__gt__

   .. container:: inherited

      .. automethod:: Path.__hash__

   .. container:: inherited

      .. automethod:: Path.__le__

   .. container:: inherited

      .. automethod:: Path.__lt__

   .. container:: inherited

      .. automethod:: Path.__new__

   .. automethod:: Path.__repr__

   .. container:: inherited

      .. automethod:: Path.__rtruediv__

   .. container:: inherited

      .. automethod:: Path.__str__

   .. container:: inherited

      .. automethod:: Path.__truediv__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Path.absolute

   .. automethod:: Path.activate

   .. automethod:: Path.add_buildspace_metadatum

   .. automethod:: Path.add_metadatum

   .. container:: inherited

      .. automethod:: Path.as_posix

   .. container:: inherited

      .. automethod:: Path.as_uri

   .. container:: inherited

      .. automethod:: Path.chmod

   .. automethod:: Path.count

   .. automethod:: Path.deactivate

   .. container:: inherited

      .. automethod:: Path.exists

   .. container:: inherited

      .. automethod:: Path.expanduser

   .. automethod:: Path.extern

   .. automethod:: Path.get_asset_type

   .. automethod:: Path.get_files_ending_with

   .. automethod:: Path.get_identifier

   .. automethod:: Path.get_metadata

   .. automethod:: Path.get_metadatum

   .. automethod:: Path.get_next_package

   .. automethod:: Path.get_next_score

   .. automethod:: Path.get_previous_package

   .. automethod:: Path.get_previous_score

   .. automethod:: Path.get_title

   .. container:: inherited

      .. automethod:: Path.glob

   .. container:: inherited

      .. automethod:: Path.group

   .. automethod:: Path.is__assets

   .. automethod:: Path.is__segments

   .. container:: inherited

      .. automethod:: Path.is_absolute

   .. container:: inherited

      .. automethod:: Path.is_block_device

   .. automethod:: Path.is_build

   .. automethod:: Path.is_builds

   .. automethod:: Path.is_buildspace

   .. container:: inherited

      .. automethod:: Path.is_char_device

   .. automethod:: Path.is_contents

   .. automethod:: Path.is_definitionspace

   .. container:: inherited

      .. automethod:: Path.is_dir

   .. automethod:: Path.is_distribution

   .. automethod:: Path.is_etc

   .. automethod:: Path.is_external

   .. container:: inherited

      .. automethod:: Path.is_fifo

   .. container:: inherited

      .. automethod:: Path.is_file

   .. container:: inherited

      .. automethod:: Path.is_mount

   .. automethod:: Path.is_part

   .. automethod:: Path.is_parts

   .. container:: inherited

      .. automethod:: Path.is_relative_to

   .. container:: inherited

      .. automethod:: Path.is_reserved

   .. automethod:: Path.is_score_build

   .. automethod:: Path.is_score_package_path

   .. automethod:: Path.is_scores

   .. automethod:: Path.is_segment

   .. automethod:: Path.is_segments

   .. container:: inherited

      .. automethod:: Path.is_socket

   .. automethod:: Path.is_stylesheets

   .. container:: inherited

      .. automethod:: Path.is_symlink

   .. automethod:: Path.is_wrapper

   .. container:: inherited

      .. automethod:: Path.iterdir

   .. container:: inherited

      .. automethod:: Path.joinpath

   .. container:: inherited

      .. automethod:: Path.lchmod

   .. container:: inherited

      .. automethod:: Path.link_to

   .. automethod:: Path.list_paths

   .. automethod:: Path.list_secondary_paths

   .. container:: inherited

      .. automethod:: Path.lstat

   .. container:: inherited

      .. automethod:: Path.match

   .. container:: inherited

      .. automethod:: Path.mkdir

   .. container:: inherited

      .. automethod:: Path.open

   .. container:: inherited

      .. automethod:: Path.owner

   .. container:: inherited

      .. automethod:: Path.read_bytes

   .. container:: inherited

      .. automethod:: Path.read_text

   .. container:: inherited

      .. automethod:: Path.readlink

   .. container:: inherited

      .. automethod:: Path.relative_to

   .. automethod:: Path.remove

   .. automethod:: Path.remove_metadatum

   .. container:: inherited

      .. automethod:: Path.rename

   .. container:: inherited

      .. automethod:: Path.replace

   .. container:: inherited

      .. automethod:: Path.resolve

   .. container:: inherited

      .. automethod:: Path.rglob

   .. container:: inherited

      .. automethod:: Path.rmdir

   .. container:: inherited

      .. automethod:: Path.samefile

   .. container:: inherited

      .. automethod:: Path.stat

   .. container:: inherited

      .. automethod:: Path.symlink_to

   .. container:: inherited

      .. automethod:: Path.touch

   .. automethod:: Path.trim

   .. container:: inherited

      .. automethod:: Path.unlink

   .. automethod:: Path.with_name

   .. container:: inherited

      .. automethod:: Path.with_stem

   .. container:: inherited

      .. automethod:: Path.with_suffix

   .. container:: inherited

      .. automethod:: Path.write_bytes

   .. automethod:: Path.write_metadata_py

   .. container:: inherited

      .. automethod:: Path.write_text

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Path.cwd

   .. container:: inherited

      .. automethod:: Path.home

   .. automethod:: Path.sort_segment_names

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Path.anchor

   .. autoattribute:: Path.build

   .. autoattribute:: Path.builds

   .. autoattribute:: Path.contents

   .. autoattribute:: Path.distribution

   .. container:: inherited

      .. autoattribute:: Path.drive

   .. autoattribute:: Path.etc

   .. container:: inherited

      .. autoattribute:: Path.name

   .. container:: inherited

      .. autoattribute:: Path.parent

   .. container:: inherited

      .. autoattribute:: Path.parents

   .. container:: inherited

      .. autoattribute:: Path.parts

   .. container:: inherited

      .. autoattribute:: Path.root

   .. autoattribute:: Path.scores

   .. autoattribute:: Path.segments

   .. container:: inherited

      .. autoattribute:: Path.stem

   .. autoattribute:: Path.stylesheets

   .. container:: inherited

      .. autoattribute:: Path.suffix

   .. container:: inherited

      .. autoattribute:: Path.suffixes

   .. autoattribute:: Path.wrapper

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~get_measure_profile_metadata

.. autofunction:: get_measure_profile_metadata