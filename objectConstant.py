import builtins


class ObjectStateConstant(builtins.object):
    def __init__(self):
        self.isDebugging = True
        self.versionStr = "v0.0.1"
        self.versionL = (0, 0, 1)
        self.ParameterSelection = "default=self"

        self.isLoggingUsing = True

        self.isRelease = False

    def get_is_debug(self):
        return self.isDebugging

    def programVersion(self):
        return [self.versionStr, self.versionL]

    def debuggingPrint(self, anything):
        if self.isDebugging:
            print(anything)

    def dp(self, anything):
        if self.isDebugging:
            print(anything)
