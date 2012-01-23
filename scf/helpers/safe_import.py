def safe_import(namespace, module_short_name, attribute_name):

    parent_module_importable_name = namespace['__name__']
    module_importable_name = '{}.{}'.format(parent_module_importable_name, module_short_name)

    try:
        module = __import__(module_importable_name, fromlist=['*'])
    except SyntaxError:
        message = 'Syntax error in {!r}.'.format(module_importable_name)
        print message
        return

    try:
        attribute_value = module.__dict__[attribute_name]
    except:
        message = 'Can not import {!r} from {!r}.'.format(attribute_name, module_importable_name)
        print message
        return

    namespace[attribute_name] = attribute_value
