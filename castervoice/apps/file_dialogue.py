from castervoice.lib.imports import *

class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
        "up [<n>]":
            R(Key("a-up"), rdescript="File Dialogue: Navigate up")*Repeat(extra="n"),
        "back [<n>]":
            R(Key("a-left"), rdescript="File Dialogue: Navigate back")*Repeat(extra="n"),
        "forward [<n>]":
            R(Key("a-right"), rdescript="File Dialogue: Navigate forward")*
            Repeat(extra="n"),
        "(files | file list)":
            R(Key("a-d, f6:3"), rdescript="File Dialogue: Files list"),
        "navigation [pane]":
            R(Key("a-d, f6:2"), rdescript="File Dialogue: Navigation pane"),
        "[file] name":
            R(Key("a-d, f6:5"), rdescript="File Dialogue: File name"),
    }
    extras = [IntegerRefST("n", 1, 10)]
    defaults = {
        "n": 1,
    }


dialogue_names = [
    "open",
    "save",
    "select",
]
context = AppContext(title=dialogue_names)
control.non_ccr_app_rule(FileDialogueRule(), context=context)
