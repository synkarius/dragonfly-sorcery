#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Notepad++

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class NPPRule(MergeRule):
    pronunciation = "notepad plus plus"

    mapping = {
        "stylize <n2>":
            R(Mouse("right") + Key("down:6/5, right") +
              (Key("down")*Repeat(extra="n2")) + Key("enter"),
              rdescript="Notepad++: Stylize"),
        "remove style":
            R(Mouse("right") + Key("down:6/5, right/5, down:5/5, enter"),
              rdescript="Notepad++: Remove Style"),
        "preview in browser":
            R(Key("cas-r"), rdescript="Notepad++: Preview In Browser"),

        # requires function list plug-in:
        "function list":
            R(Key("cas-l"), rdescript="Notepad++: Function List"),
        "open":
            R(Key("c-o"), rdescript="Notepad++: Open"),
        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter"),
              rdescript="Notepad++: Go to Line #"),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("n2", 1, 10),
    ]
    defaults = {"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="notepad++")
grammar = Grammar("Notepad++", context=context)

if settings.SETTINGS["apps"]["notepadplusplus"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(NPPRule())
    else:
        rule = NPPRule(name="notepad plus plus")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
