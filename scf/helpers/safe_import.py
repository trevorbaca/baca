def safe_import(target_namespace, source_module_short_name, source_attribute_name,
    source_parent_module_importable_name=None):

    if source_parent_module_importable_name is None:
        source_parent_module_importable_name = target_namespace['__name__']

    source_module_importable_name = '{}.{}'.format(source_parent_module_importable_name, source_module_short_name)

    try:
        source_module = __import__(source_module_importable_name, fromlist=['*'])
    except SyntaxError:
        message = 'Syntax error in {!r}.'.format(source_module_importable_name)
        print message
        return

    try:
        source_attribute_value = source_module.__dict__[source_attribute_name]
    except:
        message = 'Can not import {!r} from {!r}.'.format(source_attribute_name, source_module_importable_name)
        print message
        return

    target_namespace[source_attribute_name] = source_attribute_value
    return source_attribute_value
