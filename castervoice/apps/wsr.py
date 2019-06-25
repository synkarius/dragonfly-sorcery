from castervoice.lib.imports import *

class WindowsSpeechRecognitionRule(MergeRule):

    mapping = {
        "reboot windows speech recognition":
            R(Function(utilities.reboot, wsr=True),
              rdescript="Reboot Windows Speech Recognition"),
    }
    extras = []
    defaults = {}


if settings.WSR:
    control.non_ccr_app_rule(WindowsSpeechRecognitionRule())