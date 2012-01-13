def check_illustration_builder_commandline(argv, usage_string = None):
    '''Function exists to encapsulate logic used in scripts like Manifolds
    show_horizontal_pitch_fields.py and show_segmented_pitch_fields.py.'''

    if len(argv) == 1:
        write = False
    elif len(argv) == 2:
        option = argv[1]
        if option == '--nowrite':
            write = False
        elif option == '--write':
            write = True
        else:
            raise SystemExit(usage_string)
    else:
        raise SystemExit(usage_string)

    return write
