from baca.scf.PackageProxy import PackageProxy


class MusProxy(PackageProxy):

    def __init__(self, score_package_short_name, session=None):
        PackageProxy.__init__(self, '%s.mus' % score_package_short_name, session=session)
