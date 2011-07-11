def get_score_title(score_package_name):

   command = 'from %s.mus.cfg import score_title' % score_package_name
   exec(command)
   return score_title
