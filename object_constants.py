import builtins


class ObjectStateConstant(builtins.object):
    def __init__(self):
        self.debugging = True
        self.version = "v0.0.1"
        self.version_tuple = (0, 0, 1)
        self.ParameterSelection = "default=self"

        self.isLoggingUsing = True

        self.isRelease = False

    def get_is_debug(self):
        return self.debugging

    def get_versions(self):
        return [self.version, self.version_tuple]

    def debugging_print(self, anything):
        if self.debugging:
            print(anything)

    def dp(self, anything):
        if self.debugging:
            print(anything)
