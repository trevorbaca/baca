.. _baca--Expression:

Expression
==========

.. automodule:: baca.Expression

.. currentmodule:: baca.Expression

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.Expression

.. autoclass:: Expression

   .. autosummary::
      :nosignatures:

      pitch_class_segment
      pitch_class_segments
      select

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Expression.__add__

   .. container:: inherited

      .. automethod:: Expression.__call__

   .. container:: inherited

      .. automethod:: Expression.__copy__

   .. container:: inherited

      .. automethod:: Expression.__eq__

   .. container:: inherited

      .. automethod:: Expression.__format__

   .. container:: inherited

      .. automethod:: Expression.__getattr__

   .. container:: inherited

      .. automethod:: Expression.__getitem__

   .. container:: inherited

      .. automethod:: Expression.__hash__

   .. container:: inherited

      .. automethod:: Expression.__iadd__

   .. container:: inherited

      .. automethod:: Expression.__radd__

   .. container:: inherited

      .. automethod:: Expression.__repr__

   .. container:: inherited

      .. automethod:: Expression.__setitem__

   .. container:: inherited

      .. automethod:: Expression.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Expression.append_callback

   .. container:: inherited

      .. automethod:: Expression.color

   .. container:: inherited

      .. automethod:: Expression.establish_equivalence

   .. container:: inherited

      .. automethod:: Expression.get_markup

   .. container:: inherited

      .. automethod:: Expression.get_string

   .. container:: inherited

      .. automethod:: Expression.label

   .. automethod:: Expression.pitch_class_segment

   .. automethod:: Expression.pitch_class_segments

   .. container:: inherited

      .. automethod:: Expression.pitch_set

   .. container:: inherited

      .. automethod:: Expression.print

   .. automethod:: Expression.select

   .. container:: inherited

      .. automethod:: Expression.sequence

   .. container:: inherited

      .. automethod:: Expression.wrap_in_list

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Expression.make_callback

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Expression.argument_count

   .. container:: inherited

      .. autoattribute:: Expression.argument_values

   .. container:: inherited

      .. autoattribute:: Expression.callbacks

   .. container:: inherited

      .. autoattribute:: Expression.evaluation_template

   .. container:: inherited

      .. autoattribute:: Expression.force_return

   .. container:: inherited

      .. autoattribute:: Expression.has_parentheses

   .. container:: inherited

      .. autoattribute:: Expression.is_composite

   .. container:: inherited

      .. autoattribute:: Expression.is_initializer

   .. container:: inherited

      .. autoattribute:: Expression.is_postfix

   .. container:: inherited

      .. autoattribute:: Expression.is_selector

   .. container:: inherited

      .. autoattribute:: Expression.keywords

   .. container:: inherited

      .. autoattribute:: Expression.lone

   .. container:: inherited

      .. autoattribute:: Expression.map_operand

   .. container:: inherited

      .. autoattribute:: Expression.markup_maker_callback

   .. container:: inherited

      .. autoattribute:: Expression.module_names

   .. container:: inherited

      .. autoattribute:: Expression.name

   .. container:: inherited

      .. autoattribute:: Expression.next_name

   .. container:: inherited

      .. autoattribute:: Expression.precedence

   .. container:: inherited

      .. autoattribute:: Expression.proxy_class

   .. container:: inherited

      .. autoattribute:: Expression.qualified_method_name

   .. container:: inherited

      .. autoattribute:: Expression.string_template

   .. container:: inherited

      .. autoattribute:: Expression.subclass_hook

   .. container:: inherited

      .. autoattribute:: Expression.subexpressions

   .. container:: inherited

      .. autoattribute:: Expression.template