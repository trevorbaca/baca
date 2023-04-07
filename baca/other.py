"""
Other functions.
"""


def call(argument):
    if callable(argument):
        argument()
    else:

        def composite(function):
            function(argument)

        return composite
