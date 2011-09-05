from score_driver_template import score_driver_template
from get_next_letter_pair import get_next_letter_pair
import os


def make_score_workspace(parent_directory, workspace_name):

    ## extend workspace name
    workspace_name = '%s_score' % workspace_name

    ## build prefix
    verb = 'show'
    letter_pair = get_next_letter_pair(parent_directory)
    prefix = '%s_%s' % (letter_pair, verb)

    ## create workspace directory
    workspace_directory = '%s_%s' % (prefix, workspace_name)
    path = os.path.join(os.path.abspath(parent_directory), workspace_directory)
    print 'Creating score workspace %s ...' % path
    os.mkdir(path)

    ## build status message
    status_message = 'Making %s ...' % workspace_name.replace('_', ' ')

    ## build function name
    function_name = 'make_%s' % workspace_name

    ## build score name
    score_name = workspace_name

    ## make driver contents
    score_driver_contents = score_driver_template
    score_driver_contents %= (
        function_name, status_message, function_name, score_name)

    ## write driver
    driver_name = os.path.join(path, 'run.py')
    driver = file(driver_name, 'w')
    driver.write(score_driver_contents)
    driver.close()
    os.system('chmod 755 %s' % driver_name)

    ## make helpers directory
    helpers_directory = os.path.join(path, 'helpers')
    os.mkdir(helpers_directory)

    ## make helpers init contents
    helpers_init_contents = 'import baca\n'
    helpers_init_contents += '\n'
    helpers_init_contents += \
        'baca.util.import_public_functions(__file__, globals())\n'
    helpers_init_contents += 'del baca'

    ## write helpers init
    helpers_init = os.path.join(helpers_directory, '__init__.py')
    helpers_init =  file(helpers_init, 'w')
    helpers_init.write(helpers_init_contents)
    helpers_init.close()

    ## make helper contents
    helper_contents = '\n'
    helper_contents += '\n'
    helper_contents += 'def %s():\n' % function_name
    helper_contents += '\n'
    helper_contents += '    pass\n'

    ## make helper file
    helper_file = function_name + '.py'
    helper_file = os.path.join(helpers_directory, helper_file)
    helper_file = file(helper_file, 'w')
    helper_file.write(helper_contents)
    helper_file.close()

    ## create scores directory
    scores_directory = os.path.join(path, 'scores')
    os.mkdir(scores_directory)

    ## create templates directory
    templates_directory = os.path.join(path, 'templates')
    os.mkdir(templates_directory)
