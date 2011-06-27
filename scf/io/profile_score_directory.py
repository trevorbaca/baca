import os


def profile_score_directory(score_package_name):

   exec('from %s.mus.cfg import score_title' % score_package_name)

   print 'Score title: %s' % score_title
   print ''
