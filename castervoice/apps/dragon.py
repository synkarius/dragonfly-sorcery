
from dragonfly import (Grammar, Playback, Key, Text, Dictation, Function, Choice, Mimic, WaitWindow, Pause, Repeat, AppContext)
from castervoice.lib import control
from castervoice.lib import utilities, settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
_NEXUS = control.nexus()


def fix_dragon_double(nexus):
    try:
        lr = nexus.history[len(nexus.history) - 1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del").execute()
    except Exception:
        utilities.simple_log(False)

def cap_dictation(dictation):
    input_list = str(dictation).split(" ")
    output_list = []
    for i in range(len(input_list)):
        if input_list[i] == "cap":
            input_list[i+1] = input_list[i+1].title()
        else:
            output_list.append(input_list[i])
    Text(" ".join(output_list)).execute()

# extras are common to both classes in this file
extras_for_whole_file = [
        Dictation("text"),
        IntegerRefST("n10", 1, 10),
        Choice("first_second_third", {
            "first": 0,
            "second": 1,
            "third": 2,
            "fourth": 3,
            "fifth": 4,
            "six": 5,
            "seventh": 6
        }),
        
    ]
defaults_for_whole_file = {"n10": 1, "text": "",}

class DragonRule(MergeRule):
    pronunciation = "dragon"

    mapping = {
        "format <text>": Function(cap_dictation, extra={"text"}),
        '(lock Dragon | deactivate)':
            R(Playback([(["go", "to", "sleep"], 0.0)]), rdescript="Dragon: Go To Sleep"),
        '(number|numbers) mode':
            R(Playback([(["numbers", "mode", "on"], 0.0)]),
              rdescript="Dragon: Number Mode"),
        'spell mode':
            R(Playback([(["spell", "mode", "on"], 0.0)]), rdescript="Dragon: Spell Mode"),
        'dictation mode':
            R(Playback([(["dictation", "mode", "on"], 0.0)]),
              rdescript="Dragon: Dictation Mode"),
        'normal mode':
            R(Playback([(["normal", "mode", "on"], 0.0)]),
              rdescript="Dragon: Normal Mode"),
        'com on':
            R(Playback([(["command", "mode", "on"], 0.0)]),
              rdescript="Dragon: Command Mode (On)"),
        'com off':
            R(Playback([(["command", "mode", "off"], 0.0)]),
              rdescript="Dragon: Command Mode (Off)"),
        "reboot dragon":
            R(Function(utilities.reboot), rdescript="Reboot Dragon Naturallyspeaking"),
        "fix dragon double":
            R(Function(fix_dragon_double, nexus=_NEXUS),
              rdescript="Fix Dragon Double Letter"),
        "left point":
            R(Playback([(["MouseGrid"], 0.1), (["four", "four"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Left Point"),
        "right point":
            R(Playback([(["MouseGrid"], 0.1), (["six", "six"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Right Point"),
        "center point":
            R(Playback([(["MouseGrid"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Center Point"),
        
        
        "show windows": R(Mimic("list", "all", "windows"),  
            rdescript="Dragon: emulate Dragon command for listing windows"),
        "cory <text>": 
            R(Mimic("correct", extra="text") + WaitWindow(title="spelling window") + Mimic("choose", "one"),
                rdescript="Dragon: brings up the correction menu for the phrase spoken in the command and chooses the 1st choice"),
        "cory that": 
            R(Mimic("correct", "that") + WaitWindow(title="spelling window") + Mimic("choose", "one"), 
                rdescript="Dragon: brings up the correction menu for the previously spoken phrase and chooses the first choice"),

        "make that <text>": R(Mimic("scratch", "that") + Mimic(extra="text"), 
             rdescript="Dragon: deletes the dictation generated by the previous utterance and replaces it with what you say next"),
        'scratch [<n10>]': R(Playback([(["scratch", "that"], 0.03)]), 
            rdescript="Dragon: delete dictation from previous n utterances") * Repeat(extra="n10"),
             
        "train word": R(Mimic("train", "that") + Key("a-r/200, s"),
             rdescript="Dragon: quickly train word when you have it selected in a Dragon friendly text field"),
        "(add train | train from add word)": R(Key("a-a/2, enter/300, a-s"),
            rdescript="Dragon: quickly train word from the add word dialogbox"),
        "(train from vocab | cab train)": R(Key("a-t/50, enter/50, a-r/250, s"), 
            rdescript="Dragon: quickly train word from Vocabulary Editor"),
        
        "recognition history": 
            R(Playback([(["view", "recognition", "history"], 0.03)]),
             rdescript="Dragon: open Dragon recognition history"),
        "peak [recognition] history": 
            R(Playback([(["view", "recognition", "history"], 0.03)])
                + Pause("300") + Key("escape"), 
                    rdescript="Dragon: open Dragon recognition history then close it"),
        "[dictation] sources": R(Mimic("manage", "dictation", "sources"), 
            rdescript="Dragon: manage dictation sources"),
        
        # A Natlink Command
        "clear caster log": R(Function(utilities.clear_log), rdescript="Core: Clear Caster Log"),

        
    }
    # see above
    extras = extras_for_whole_file
    defaults = defaults_for_whole_file
class SpellingWindowRule(MergeRule):
    mapping = {
         # todo: make these CCR
         "<first_second_third> word": 
            R(Key("home, c-right:%(first_second_third)d, cs-right"), 
            rdescript="Dragon: select the first second or third etc. word"),
         "last [word]": R(Key("right, cs-left"), rdescript="Dragon: select the last word"),
         "second [to] last word": R(Key("right, c-left:1, cs-left"), rdescript="Dragon: select the second to last word"), 
         "<n10>": R(Mimic("choose", extra="n10"), rdescript="Dragon: e.g. instead of having to say 'choose two' you can just say 'two'"),
            # consider making the above command global so that it works when you say something like 
            # "insert before 'hello'" where there are multiple instances of 'hello'
            # personally I think it's better just to have the setting where Dragon choose is the closest instance
    }

    # see above
    extras = extras_for_whole_file
    defaults = defaults_for_whole_file

    

# #---------------------------------------------------------------------------
grammar1 = Grammar("Dragon Naturallyspeaking")
spelling_window_and_windows_list_context = AppContext(executable="natspeak")
grammar2 = Grammar("Spelling Window", context= spelling_window_and_windows_list_context)
if settings.SETTINGS["apps"]["dragon"] and not settings.WSR:
    rule_1 = DragonRule(name="dragon")
    rule_2 = SpellingWindowRule(name="spelling_window")
    gfilter.run_on(rule_1)
    gfilter.run_on(rule_2)
    grammar1.add_rule(rule_1)
    grammar2.add_rule(rule_2)
    grammar1.load()
    grammar2.load()
