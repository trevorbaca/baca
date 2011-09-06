def get_verified_user_input(prompt = 'scf> '):

    while True:
        response = raw_input(prompt)
        print ''
        accept = raw_input('Ok? ')
        if accept.lower() in ('1', 'y', 'yes'):
            print ''
            return response
        else:
            print ''
