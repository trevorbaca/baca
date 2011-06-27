from score_package_dictionary import score_package_dictionary


def score_package_number_to_score_package_name(score_package_number):

   score_package_name, score_title = score_package_dictionary[score_package_number]

   return score_package_name
