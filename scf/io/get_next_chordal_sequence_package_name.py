from get_verified_user_input import get_verified_user_input
from list_chordal_sequences import list_chordal_sequences


def get_next_chordal_sequence_package_name(score_package_name):

    chordal_sequences = list_chordal_sequences(score_package_name)
    total_chordal_sequences = len(chordal_sequences)

    next_number = total_chordal_sequences + 1
    next_number = str(next_number)
    next_number = next_number.zfill(2)

    package_name = '%s_chordal_sequence_%s' % (score_package_name, next_number)

    print "Default package name is '%s'." % package_name
    print ''
    input = raw_input('Use default package name? ')
    print ''

    if input.lower() in ('2', 'n', 'no'):
        package_name = get_verified_user_input('Enter new package name> ')

    return package_name
