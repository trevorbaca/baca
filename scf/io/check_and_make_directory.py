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
            input = raw_input('scf> ')
            print ''
            if input == '1':
                os.mkdir(path)
                print 'Diretory %s created.' % path
                print ''
                run_go_on_menu()
                break
            elif input == '2':
                print 'Returning to previous menu.'
                print ''
                run_go_on_menu()
                break
