.. _baca--settinglib:

settinglib
==========

.. automodule:: baca.settinglib

.. currentmodule:: baca.settinglib

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.settinglib

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: section-header

.. autosummary::
   :nosignatures:

   ~SettingCommand

.. autoclass:: SettingCommand

   .. autosummary::
      :nosignatures:

      context
      setting
      value

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SettingCommand.__call__

   .. container:: inherited

      .. automethod:: SettingCommand.__format__

   .. container:: inherited

      .. automethod:: SettingCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SettingCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SettingCommand.runtime

   .. container:: inherited

      .. autoattribute:: SettingCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SettingCommand.context

   .. container:: inherited

      .. autoattribute:: SettingCommand.deactivate

   .. container:: inherited

      .. autoattribute:: SettingCommand.selector

   .. autoattribute:: SettingCommand.setting

   .. container:: inherited

      .. autoattribute:: SettingCommand.tag

   .. container:: inherited

      .. autoattribute:: SettingCommand.tags

   .. autoattribute:: SettingCommand.value