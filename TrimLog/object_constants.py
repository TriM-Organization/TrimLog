import builtins
import rich.console


class ObjectStateConstant(builtins.object):
    def __init__(self):
        self.debugging = True
        self.project_name = ""
        self.version = "v0.0.1"
        self.version_tuple = (0, 0, 1)
        self.ParameterSelection = "default=self"

        self.isLoggingUsing = True

        self.isRelease = False

        self.console = None

    def get_console(self, in_console: rich.console.Console) -> None:
        self.console: rich.console.Console = in_console

    def get_is_debug(self):
        return self.debugging

    def get_versions(self):
        return [self.version, self.version_tuple]

    def debugging_print(self, anything):
        if self.debugging:
            if self.console is not None:
                self.console.print(anything)
            else:
                print(anything)

    def dp(self, anything):
        if self.debugging:
            if self.console is not None:
                self.console.print(anything)
            else:
                print(anything)
