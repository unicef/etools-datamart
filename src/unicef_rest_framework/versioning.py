from rest_framework.versioning import URLPathVersioning


class URFVersioning(URLPathVersioning):
    # allowed_versions = ['v1', 'v2', 'latest']
    allowed_versions = []
    # def is_allowed_version(self, version):
    #     if not self.allowed_versions:
    #         return True
    #     return ((version is not None and version == self.default_version) or
    #             (version in self.allowed_versions))


#
