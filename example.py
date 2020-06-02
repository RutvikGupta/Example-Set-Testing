from typing import List, Dict, Tuple

TCL_ERROR = False
TCL_OK = True
import example_defaults



class ExampleSet:
    """ set of examples linked list
    """
    name: str
    num: int
    # need python mask
    mode: int  # mask
    numExamples: int
    numEvents: int
    ext = None  #: ExSetExt
    # where is ExSetExt defined?? 

    example = None  #: Example
    permuted = None  #: Example
    currentExampleNum: int
    currentExample = None  #: Example
    firstExample = None  #: Example
    lastExample = None  #: Example
    pipeExample = None  #: Example
    pipeParser = None  # ParseRec

    pipeLoop: bool  # flag
    # whats python eq for flag? 
    pipeExampleNum: int

    # Tcl_Obj defined as C macro in example.h
    proc: Tcl_Obj
    chooseExample: Tcl_Obj
    maxTime: float
    minTime: float
    graceTime: float
    defaultInput: float
    activeInput: float
    defaultTarget: float
    activeTarget: float
    # int replaces short
    numGroupNames: int  # hidden
    maxGroupNames: int  # hidden
    groupName: list  # hidden

    # what are flags and how to translate?

    # flag     (*loadEvent)(Event V);
    # flag     (*loadExample)(Example E);
    # flag     (*nextExample)(ExampleSet S);

    def __init__(self, name: str):
        self.name = name
        self.pipeLoop = example_defaults.DEF_S_pipeLoop
        self.maxTime = example_defaults.DEF_S_maxTime
        self.minTime = example_defaults.DEF_S_minTime
        self.graceTime = example_defaults.DEF_S_graceTime
        self.defaultInput = example_defaults.DEF_S_defaultInput
        self.activeInput = example_defaults.DEF_S_activeInput
        self.defaultTarget = example_defaults.DEF_S_defaultTarget
        self.activeTarget = example_defaults.DEF_S_activeTarget
        self.loadEvent = standardLoadEvent
        self.loadExample = standardLoadExample
        self.numGroupNames = 0
        self.maxGroupNames = 0
        self.groupName = []


class Root:
    """
    class consisting of list of initialized exampleSet
    """
    num_example_set = 0
    set: List[ExampleSet]

    def __init__(self):
        self.set = []

    """/ *returns the root that contains name * /
    / *what is Root? * / """
    def lookupExampleSet(self, name: str):
        for s in range(self.num_example_set):
            if self.set[s].name == name:
                return self.set[s]
        return None

    """/ *Stores a link to the set in the Root set table. Assumes set with same name is not there already * /
    """
    def registerExampleSet(self, S: ExampleSet):
        self.num_example_set += 1
        S.num = self.num_example_set - 1
        self.set[S.num] = S
        # eval("catch {.initExSet root.set(%d)}", S->num);
        # signalSetListsChanged();


class Example:
    """ example
    """

    name = None  #: str
    num = 0  # : int
    numEvents = 0  #: int
    event = None  #: Event
    set = None  #: ExampleSet
    next = None  #: Example
    ext = None  #: ExampleExt

    # float replaces real
    frequency: float
    probability = 0.0  #: float

    proc: Tcl_Obj

    # proc function is defined in the C macros

    def __init__(self, S: ExampleSet):
        self.frequency = example_defaults.DEF_E_frequency
        self.set = S

        # initExampleExtension(E)


class Event:
    """ event! 
    """

    input = None  #: Range
    sharedInputs: bool  # flag
    target: range
    sharedTargets: bool  # flag

    # float = real
    maxTime: float
    minTime: float
    graceTime: float
    defaultInput: float
    activeInput: float
    defaultTarget: float
    activeTarget: float

    proc: Tcl_Obj
    example: Example
    ext = None  #: EventExt

    def __init__(self, E: Example):
        S = E.set
        self.example = E
        self.maxTime = example_defaults.DEF_V_maxTime
        self.minTime = example_defaults.DEF_V_minTime
        self.graceTime = example_defaults.DEF_V_graceTime
        self.defaultInput = S.defaultInput
        self.activeInput = S.activeInput
        self.defaultTarget = S.defaultTarget
        self.activeTarget = S.activeTarget
        # initEventExtension(V)


class Range:
    """range"""

    groupName: str  # If null, unit offsets are for the net
    numUnits: int
    firstUnit: int  # Only used for dense encodings
    # float replaces real
    val: float  # Only used for dense encodings

    value: float  # Only used for sparse encodings
    unit: int  # Only used for sparse encodings

    def __init__(self, V: Event, doing_inputs: bool, L=None):
        if doing_inputs:
            self.value = V.activeInput
        else:
            self.value = V.activeTarget
        if L:
            L.next = self
        else:
            if doing_inputs:
                V.input = self
            else:
                V.target = self


class ParseRec:
    channel: None  # Tcl_Channel: channel;
    fileName: str
    cookie: str
    cookiePos: int
    line: int
    buf: str
    s: str
    shift: list  # length of s
    parsed_s: int

    def __init__(self):
        self.shift = list(self.s)
        self.parsed_s = 0

    def readInt(self, parsed_list: list):
        if self.shift is []:
            return TCL_ERROR
        while self.parsed_s < len(self.shift) and not self.shift[self.parsed_s].isdigit():
            self.parsed_s += 1
        parsed_list.append(int(self.shift[self.parsed_s]))
        return TCL_OK


def register_example(E: Example, S: ExampleSet):
    E.next = None
    if not S.firstExample:
        S.firstExample = E
        S.lastExample = E
    else:
        S.lastExample.next = E
        S.lastExample = E
    S.numExamples += 1
    E.set = S


def clean_example(E: Example):
    i = 0
    # V = Event()
    # N, L = Range(), Range()
    if not E:
        return
    if E.proc:
        Tcl_DecrRefCount(E.proc)  # ! function
    if E.event:
        for i in range(E.numEvents):
            V = E.event + i
            if not V.sharedInputs:
                L = V.input
                while L:
                    N = L.next
                    L = N
            if not V.sharedTargets:
                L = V.target
                while L:
                    N = L.next
                    L = N
            if V.proc:
                Tcl_DecrRefCount(V.proc)  # !
            freeEventExtension(V)  # !


def clearExample(E: Example):
    E.name = None
    E.num = 0
    E.numEvents = 0
    E.event = None
    E.next = None
    E.frequency = example_defaults.DEF_E_frequency
    E.probability = 0.0
    E.proc = None


# This is used when writing an example file
def normalEvent(V: Event, S: ExampleSet) -> bool:
    if V.proc is None:
        return False
    elif not V.maxTime is example_defaults.DEF_V_maxTime:
        return False
    elif not V.minTime is example_defaults.DEF_V_minTime:
        return False
    elif not V.graceTime is example_defaults.DEF_V_graceTime:
        return False
    elif not V.defaultInput is S.defaultInput:
        return False
    elif not V.activeInput is S.activeInput:
        return False
    elif not V.defaultTarget is S.defaultTarget:
        return False
    elif not V.activeTarget is S.activeTarget:
        return False
    else:
        return True


"""Prints an error message and returns TCL_ERROR"""
def parseError(R: ParseRec, fmt: str) -> bool:
    print("loadExample: " + fmt + "on " + "line " + str(R.line) + " of file " + R.fileName)
    return TCL_ERROR


"""Not sure but we dont need this code even """
# # do we need custom memory management?
# def freeExampleSet(S: ExampleSet):
#     # E, N = Example(), Example()
#     if not S:
#         return
#     # free S.name
#     E = S.firstExample
#     while E:
#         N = E.next
#         # freeExample(E)
#         E = N
#     #free S.example
#     #free S.permuted
#     if S.proc:
#         #Tcl_DecrRefCount(S->proc)
#     if S.pipeParser:
#         # parseError(S->pipeParser, "");
#         # free(S->pipeParser);
#     # FREE(S->groupName);
#
#     # freeExSetExtension(S);
#     # free(S);
#

"""This puts all the examples in arrays and does some other calculations"""


def compile_example_set(S: ExampleSet):
    E = Example()
    i, v = 0, 0

    # what is Tcl Cmd info?


"""This parses a list of event numbers 
# used bool for flag; true replaces Tcl_Ok"""


def parseEventList(R: ParseRec, eventActive: List[bool], num: int) -> bool:
    empty = True
    lst = []
    # bzero((void *) eventActive, num)
    # skipBlank(R)
    while R.s[0].isdigit() or R.s[0] == "*":
        empty = False
        if R.s == "*":
            for i in range(num):
                eventActive[i] = True
        else:
            if R.readInt(lst):  # ! C functions
                return parseError(R, "error reading event list")
            elif lst[-1] < 0 or lst[-1] >= num:
                return parseError(R, "event" + str(lst[-1]) + " out of range")
            elif R.s is "-":
                if R.readInt(lst):
                    return parseError(R, "error reading event range")
                if lst[-1] <= lst[-2] or lst[-1] >= num:
                    return parseError(R, "event" + str(lst[-1]) + " out of range")
            else:
                lst[-1] = lst[-2]
            while lst[-2] <= lst[-1]:
                eventActive[lst[-2]] = True
                lst[-1] += 1
        # skipBlank(R)
    if empty:
        for v in range(num):
            eventActive[v] = True
    return True


def tidy_up_range(L: Range, unit: int, val: float, sparseMode: bool):
    i = 1
    if not L:
        return
    if sparseMode:
        # intArray function call is used for memory allocation 
        # what does the name do - is it important? 
        L.unit = []
        for i in range(L.numUnits):
            L.unit[i] = unit[i]
            # "tidyUpRange:L->unit"
    else:
        L.val = []
        for i in range(L.numUnits):
            L.val[i] = val[i]
            # "tidyUpRange:L->val"


def register_group_name(name: str, S: ExampleSet) -> str:
    i = 0
    while i < S.numGroupNames and S.groupName[i] == name:
        i += 1
    if i == S.numGroupNames:
        if S.maxGroupNames == 0:
            S.maxGroupNames = 16
        elif i == S.maxGroupNames:
            S.maxGroupNames *= 2

        S.numGroupNames += 1
        S.groupName[S.numGroupNames] = name
    return S.groupName[i]


def readEventRanges(V: Event, S: ExampleSet, R: ParseRec,
                    doingInputs: bool, sparseMode: bool):
    L = None
    done = False

    maxUnits, maxvals = 2, 2
    units = 0
    val = 0.0
    # if stringMatch(R, "{":
    # tidyUpRange(L, unit, val, sparseMode);
    # L = newRange(V, L, doingInputs);
    # while (!stringMatch(R, "}")) {
    # if (isNumber(R)) {
    # if (readReal(R, & L->value)) {
    # parseError(R, "couldn't read sparse active value");

#     # the rest    do{}
#     # TODO

def abort(S: ExampleSet, E: Example):
    R = Root()
    # if S:
    #     if R.lookupExampleSet(S.name):
    #         compileExampleSet(S);
    # if E:
    #     freeExample(E)
    return TCL_ERROR


"""/* This parses a text example */
"""
def read_example(E: Example, R: ParseRec):
    eventActive = ""
    V = Event(E)
    W = Event(E)
    S = E.set
    inputsSeen, targetsSeen, done = True
    v, w, nextInputEvent, nextTargetEvent = 0
