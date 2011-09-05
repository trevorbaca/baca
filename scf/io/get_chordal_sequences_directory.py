import os


def get_chordal_sequences_directory(score_package_name):

    scores = os.environ.get('SCORES')
    return os.path.join(scores, score_package_name, 'mus', 'materials', 'chordal_sequences')
