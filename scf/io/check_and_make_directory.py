import os
#from run_go_on_menu import run_go_on_menu


def check_and_make_directory(path):
    '''Return true or false.
    '''

    if os.path.exists(path):
        return True
    else:
        while True:
            print 'Directory %s does not exist.' % path
            print ''
            print 'Create it?'
            print ''
            print '  1: yes'
            print '  2: no'
            print ''
            response = raw_input('scf> ')
            print ''
            if response == '1':
                os.mkdir(path)
                print 'Diretory %s created.' % path
                print ''
                run_go_on_menu()
                break
            elif response == '2':
                print 'Returning to previous menu.'
                print ''
                run_go_on_menu()
                break
