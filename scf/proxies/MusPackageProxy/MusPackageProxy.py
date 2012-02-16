from baca.scf.proxies.PackageProxy import PackageProxy


class MusPackageProxy(PackageProxy):

    def __init__(self, score_package_short_name, session=None):
        PackageProxy.__init__(self, '{}.mus'.format(score_package_short_name), session=session)
