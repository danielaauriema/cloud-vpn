from enum import Enum

def _log_message(level, message):
    print("[%-5s] %s" % (level.upper(), message))

class WgLogLevel(Enum):
    NONE = "none"
    INFO = "info"
    DEBUG = "debug"

    @staticmethod
    def get_log_level(args):
        if "debug" in args and args["debug"]:
            return WgLogLevel.DEBUG
        elif "log_level" in args:
            return  WgLogLevel(args["log_level"])
        else:
            return WgLogLevel.INFO

class WgLog:

    def __init__(self, log_level : WgLogLevel = WgLogLevel.INFO):
        self._log_level = log_level

    def set_log_level(self, log_level: WgLogLevel):
        self._log_level = log_level

    def set_log_level_from_args(self, args, prog = "pywg"):
        self._log_level = WgLogLevel.get_log_level(args)
        if self.is_debug_mode():
            self._debug_arguments(args, prog)

    def info(self, message):
        if self._log_level == WgLogLevel.NONE: return
        _log_message(WgLogLevel.INFO.value, message)

    def debug(self, message):
        if self._log_level == WgLogLevel.DEBUG:
            _log_message(WgLogLevel.DEBUG.value, message)

    def is_debug_mode(self):
        return self._log_level == WgLogLevel.DEBUG

    def _debug_arguments(self, args, prog):
        if not self.is_debug_mode(): return
        self.debug("Received arguments: %s" % prog)
        for key in args:
            self.debug("%s: %s" % (key, args[key]))
        self.debug("")

wg_log = WgLog()