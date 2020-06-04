from typing import List

TCL_ERROR = False
TCL_OK = True
from python import example_defaults


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

    # Tcl_Obj defined in C macro in example.h 
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
        if self.parsed_s is []:
            return TCL_ERROR
        while self.parsed_s < len(self.shift) and not self.shift[self.parsed_s].isdigit():
            self.parsed_s += 1
        parsed_list.append(int(self.shift[self.parsed_s]))
        return TCL_OK


def initEvent(V: Event, E: Example):
    S = E.set
    V.example = E
    V.examplemaxTime = example_defaults.DEF_V_maxTime
    V.minTime = example_defaults.DEF_V_minTime
    V.graceTime = example_defaults.DEF_V_graceTime
    V.defaultInput = S.defaultInput
    V.__class__activeInput = S.activeInput
    V.defaultTarget = S.defaultTarget
    V.activeTarget = S.activeTarget
    # initEventExtension(V)  function is used to free memory


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
    E = Example(S)
    i, v = 0, 0
    totalFreq, scale, sum = 0.0, 0.0, 0.0
    junk = Tcl_CmdInfo()
    # Tcl Cmd info is a C library function Return information about the state of the Tcl interpreter

    # Count the number of examples and events
    S.numExamples, S.numEvents = 0, 0
    E = S.firstExample
    while E:
        S.numEvents += E.numEvents

        E = E.next
        S.numExamples += 1

    # Build the example and permuted arrays */

    if S.numExamples:
        # allocate memory for S.example
        # allocate memory for S.permuted
        pass

    # Fill the arrays and call the user-defined init procedures on each example and event

    i = 0
    E = S.firstExample
    while E:
        # original line: S->example[i] = S->permuted[i] = E;
        S.example[i], S.permuted = E, E
        E.num = i
        totalFreq += E.frequency
        E = E.next
        i = i + 1

    # /* Should this be done on the pipe example? */
    # replacemenet for interp? 
    if Tcl_GetCommandInfo(Interp, ".initExample", junk):
        E = S.firstExample
        while E:
            eval("catch {.initExample root.set(%d).example(%d)}", S.num, E.num)
            E = E.next

    if Tcl_GetCommandInfo(Interp, ".initEvent", junk):
        E = S.firstExample
        while E:
            for v in range(E.numEvents):
                eval("catch {.initEvent root.set(%d).example(%d).event(%d)}", S.num, E.num, v)
            E = E.next

    # Determine the event probabilities for probabilistic choosing.
    if S.numExamples:
        scale = 1.0 / totalFreq
        sum = 0.0
        for i in range(S.numExamples):
            sum += S.example[i].frequency * scale
            S.example[i].probability = sum
        S.example[S.numExamples - 1].probability = 1.0

    S.currentExample = None
    S.currentExampleNum = -1


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


# TODO

def readEventRanges(V: Event, S: ExampleSet, R: ParseRec,
                    doingInputs: bool, sparseMode: bool):
    #TODO buf = ???
    
    L = None
    done = False
    unit = []
    val = []
    maxUnits, maxvals = 2, 2

    while not done:
      if stringMatch(R, "{"):
        # function naming convention? 
        tidyUpRange(L, unit, val, sparseMode)
        L = newRange(V, L, doingInputs)
        while not stringMatch(R, "}"):
          if isNumber(R):
            if readReal(R, L.value):
              parseError(R, "couldn't read sparse active value")
              goto error
          else:
            if readBlock(R, buf):
              parseError(R, Tcl_GetStringResult(Interp))
              goto error
            if buf.s[0]:
              L.groupName = register_group_name(buf.s, S)
              if not L.groupName:
                parseError(R, "too many group names used")
                goto error
        sparseMode = True
      
      elif stringMatch(R, "("):
        tidy_up_range(L, unit, val, sparseMode)
        L = newRange(V, L, doingInputs)
        while not stringMatch(R, ")"):
          if isNumber(R):
            if readInt(R, L.firstUnit):
              parseError(R, "couldn't read dense first unit")
              goto error
          else:
            if readBlock(R, buf):
              parseError(R, Tcl_GetStringResult(Interp))
	            goto error
            if buf.s[0]:
              L.groupName = register_group_name(buf.s, S)
              if not L.groupName:
                parseError(R, "too many groups used")
                goto error
        sparseMode = False

      elif stringMatch(R, "*"):
        if not L:
          L = newRange(V, L, doingInputs)
        if not sparseMode or L.numUnits:
          parseError(R, "* may only be the first thing in a sparse range")
          goto error
        if L.numUnits >= maxUnits:
          maxUnits *= 2
          unit = []
        unit[L.numUnits] = -1
        L.numUnits += 1
      
      elif isNumber(R):
        if not L:
          L = newRange(V, L, doingInputs)
        if sparseMode:
          if L.numUnits and unit[0] < 0:
            parseError(R, "cannot have other units listed after *")
	          goto error;}
          if L.numUnits >= maxUnits:
            maxUnits *= 2
            unit = []
          if readInt(R, unit + L.numUnits):
            parseError(R, "error reading a sparse unit number")
            goto error
          
          #careful here...
          if unit[L.numUnits] < 0 and (L.numUnits == 0 or \
            0-unit[L.numUnits] < unit[L.numUnits - 1]):
            parseError(R, "invalid sparse unit range")
            goto error
          L.numUnits += 1
        else:
          if L.numUnits >= maxVals:
            maxVals *= 2
            val = []
          if readReal(R, val + L.numUnits)
            parseError(R, "couldn't read dense values")
            goto error
          L.numUnits += 1
      else: 
        done = True
    tidy_up_range(L, unit, val, sparseMode)
    return TCL_OK

    #TODO: reimplement jump to error block
    error: return TCL_ERROR

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
    inputsSeen, targetsSeen, done = True, True, True
    v, w, nextInputEvent, nextTargetEvent = 0, 0, 0, 0

    # read the example header
    if fileDone(R):
        return parseError(R, "file ended prematurely at start of an example")
    E.numEvents = 1

    done = False
    while not done:

        buf = R.buf

        if stringMatch(R, "name:"):
            if readBlock(R, buf):
                return parseError(R, "error reading example name")
            E.name = copyString(buf.s)
            done = False
        if stringMatch(R, "freq:"):
            if readReal(R, E.frequency):
                return parseError(R, "error reading example frequency")
            done = False
        if stringMatch(R, "proc:"):
            if readBlock(R, buf):
                return parseError(R, "error reading example proc")
            E.proc = Tcl_NewStringObj(buf.s, strlen(buf.s))
            Tcl_IncrRefCount(E.proc)
            done = False

        skipBlank(R)
        if R.s[0].isdigit():
            if readInt(R, E.numEvents):
                return parseError(R, "error reading num-events")
            if E.numEvents <= 0:
                return parseError(R, "num-events (%d) must be positive", E.numEvents)
            done = False

    # allocate memory
    E.event
    for v in range(E.numEvents):
        initEvent(E.event + v, E)

    # memory
    eventActive
    nextInputEvent, nextTargetEvent = 0, 0
    inputsSeen = targetsSeen = True

    while not stringMatch(R, ";"):
        if stringMatch(R, "[")
            # get the list of events
            if parseEventList(R, eventActive, E.numEvents):
                goto
                abort
            # This makes V the first active event, and v its index
            v, V = 0, None
            while v < E.numEvents and not V:
                if eventActive[v]:
                    V = E.event + v
                    v -= 1
            if not V:
                parseError(R, "no events specified")
                goto
                abort

            # parse the event headers
            while not stringMatch(R. "]"):
                if stringMatch(R, "proc:"):
                    if readBlock(R, buf):
                        return parseError(R, "error reading example proc")
                    w = v
                    while w < E.numEvents:
                        if eventActive[w]:
                            W = E.event + w
                            W.proc = Tcl_NewStringObj(buf.s, len(buf.s))
                            Tcl_IncrRefCount(W.proc)
                            w += 1
                elif stringMatch(R, "max:"):
                    if readReal(R, V.maxTime):
                        parseError(R, "missing value after \"max:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].maxTime = V.maxTime
                elif stringMatch(R, "min:"):
                    if readReal(R, V.minTime):
                        parseError(R, "missing value after \"min:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].minTime = V.minTime
                elif stringMatch(R, "grace:"):
                    if readReal(r, V.graceTime):
                        parseError(R, "missing value after \"grace:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].graceTime = V.graceTime
                elif stringMatch(R, "defI:"):
                    if readReal(r, V.defaultInput):
                        parseError(R, "missing value after \"defI:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].defaultInput = V.defaultInput
                elif stringMatch(R, "actI:"):
                    if readReal(r, V.activeInput):
                        parseError(R, "missing value after \"actI:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].activeInput = V.activeInput
                elif stringMatch(R, "defT:"):
                    if readReal(r, V.defaultTarget):
                        parseError(R, "missing value after \"defT:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].defaultTarget = V.defaultTarget
                elif stringMatch(R, "actT:"):
                    if readReal(r, V.activeTarget):
                        parseError(R, "missing value after \"actT:\" in event header")
                        goto
                        abort
                    for w in range(v + 1, E.numEvents):
                        if eventActive[w]:
                            E.event[w].activeTarget = V.activeTarget
                else:
                    parseError(R, "something unexpected (%s) in event header", R.s)
                    goto
                    abort
        elif stringPeek(R, "I:") or stringPeek(R, "i:") or stringPeek(R, "T:") or \
                stringPeek(R, "t:") or stringPeek(R "B:") or stringPeek(R, "b:"):
            sparseMode, doingInputs, doingTargets = False, False, False
            I, T = None

            case = R.s[0]

            if case == 'I':
                sparseMode, doingInputs, doingTargets = False, True, False
            if case == 'i':
                sparseMode, doingInputs, doingTargets = True, True, False
            if case == 'T':
                sparseMode, doingInputs, doingTargets = False, False, True
            if case == 't':
                sparseMode, doingInputs, doingTargets = True, False, True
            if case == 'B':
                sparseMode, doingInputs, doingTargets = False, True, True
            if case == 'b':
                sparseMode, doingInputs, doingTargets = True, True, True

            R.s += 2

            if doingInputs:
                if inputsSeen:
                    # /* Inputs have already been given since the last event list */
                    if nextInputEvent >= E.numEvents:
                        parseError(R, "attempted to specify inputs for event %d", nextInputEvent)
                        goto
                        abort
                    I = E.event + nextInputEvent
                    nextInputEvent += 1
                else:
                    #  /* This will apply to the active events */
                    for v in range(E.numEvents):
                        if eventActive[v]:
                            I = E.event
                            v -= 1
                    if not I:
                        parseError(R, "no events specified")
                        goto
                        abort
                    if I.input:
                        parseError(R, "multiple inputs given for event %d", v)
                        goto
                        abort
            if doingTargets:
                if targetsSeen:
                    #  /* Targets have already been given since the last event list */
                    if nextTargetEvent >= E.numEvents:
                        parseError(R, "attempted to specify targets for event %d", nextTargetEvent)
                        goto
                        abort
                    T = E.event + nextTargetEvent
                    nextTargetEvent += 1
            else:
                # /* This will apply to the active events */
                for v in range(E.numEvents):
                    if eventActive[v]:
                        T = E.event + v
                        v -= 1
                if not T:
                    parseError(R, "no events specified")
                    goto
                    abort
                if T.target:
                    parseError(R, "multiple targets given for event %d", v)
                    goto
                    abort

            # TODO
            # what does this syntax mean in C? replace this line
            V = (I) ? I: T

            if readEventRanges(V, S, R, V == I, sparseMode):
                goto
                abort
            if I and T:
                if T.target:
                    parseError(R, "multiple targets specified for event %d", \
                               (targetsSeen) ? nextTargetEvent - 1: v)
                    goto
                    abort
                T.target = I.input
                T.sharedTargets = True
            if doingInputs and not inputsSeen:
                for w in range(v + 1, E.numEvents):
                    if eventActive[w]:
                        W = E.event + w
                        if W.input:
                            parseError(R, "multiple inputs given for event %d", w)
                            goto
                            abort
                        W.input = I.input
                        W.sharedInputs = True

                for w in range(nextInputEvent, E.numEvents):
                    if eventActive[w]:
                        nextInputEvent = w + 1
                    inputsSeen = True
            if doingTargets and not targetsSeen:
                for w in range(v + 1, E.numEvents):
                    if eventActive[w]:
                        W = E.event + w
                        if W.target:
                            parseError(R, "multiple targets given for event %d", w)
                            goto
                            abort
                        W.target = T.target
                        W.sharedTargets = True
                for w in range(nextTargetEvent, E.numEvents):
                    if eventActive[w]:
                        nextTargetEvent = w + 1
                    targetsSeen = True

    # TODO: ifdef JUNK block


def readExampleSet(setName: str, fileName: str, Sp: ExampleSet, pipe: bool, maxExamples: int):
    S = Sp
    E = Example(Sp)
    val, examplesRead = 0, 0
    halted = False
    R = ParseRec()
    R.fileName = fileName
    R.buf = None
    R.s = None
    R.line = 0
    R.channel = readChannel(fileName)
    if not R.channel:
        return "readExampleSet: couldn't open the file " + fileName
    R.fileName = fileName
    R.buf = None
    R.s = None
    R.line = 0
    if startParser(R, HTONL(val)):
        return parseError(R, "couldn't read the header")
    R.readInt(val)
    R.readInt(val)
    if not S:
        S = ExampleSet(setName)
        Root.registerExampleSet(S)

    while not stringMatch(R, ";"):
        if stringMatch(R, "proc:"):
            if readBlock(R, buf):
                parseError(R, "error reading code segment")
                return abort
            # S->proc = Tcl_NewStringObj(buf->s, strlen(buf->s));
            # Tcl_IncrRefCount(S->proc);
            # if (Tcl_EvalObjEx(Interp, S->proc, TCL_EVAL_GLOBAL) != TCL_OK)
            # return TCL_ERROR;
        elif stringMatch(R, "max:"):
            if readReal(R, & (S->maxTime)):
                parseError(R, "missing value after \"max:\" in the set header")
                return abort(S, E)

        elif stringMatch(R, "min:"):
            if readReal(R, & (S->minTime)):
                parseError(R, "missing value after \"min:\" in the set header")
                return abort(S, E)

        elif (stringMatch(R, "grace:")):
            if (readReal(R, & (S->graceTime))):
                parseError(R, "missing value after \"grace:\" in the set header")
                return abort(S, E)

        elif (stringMatch(R, "defI:")):
            if (readReal(R, & (S->defaultInput))):
                parseError(R, "missing value after \"defI:\" in the set header")
                return abort(S, E)

        elif (stringMatch(R, "actI:")):
            if (readReal(R, & (S->activeInput))):
                parseError(R, "missing value after \"actI:\" in the set header")
                return abort(S, E)

        elif (stringMatch(R, "defT:")):
            if (readReal(R, & (S->defaultTarget))):
                parseError(R, "missing value after \"defT:\" in the set header")
                return abort(S, E)

        elif (stringMatch(R, "actT:")):
            if (readReal(R, & (S->activeTarget))):
                parseError(R, "missing value after \"actT:\" in the set header")
                return abort(S, E)
        else:
            break
    halted = False
    while (not fileDone(R)) and (not halted) and (not maxExamples or examplesRead < maxExamples):
        E = Example(S)
        if (readExample(E, R)):
            return abort(S, E)
        registerExample(E, S)

        halted = smartUpdate(FALSE)
    """/ *This is called to clean up the parser * /"""
    parseError(R, "")
    compileExampleSet(S)
    if (halted):
        return result("readExampleSet: halted prematurely");
    return TCL_OK;


"""/* A mode of 0 means do nothing if the set exists.
   1 means override the set
   2 means add to the set
   3 means use as a pipe */"""


def loadExamples(setName: str, fileName: str, mode: int, numExamples: int):
    R = Root()
    S = R.lookupExampleSet(setName)
    if S and mode == 1:
        # deleteExampleSet(S);
        S = None
    if not S or mode != 0:
        if readExampleSet(setName, fileName, S, mode, numExamples):
            # deleteExampleSet(S);
            return TCL_ERROR
    return  # result(setName)


"""/ *This puts all the examples in arrays and does some other calculations * /"""
def compileExampleSet(S: ExampleSet):
    E = Example(S)
    i, v = 0, 0
    totalFreq = 0.0
    scale, sum = 0.0, 0.0
    # struct Tcl_CmdInfo junk;
    # / *Count the number of examples and events * /
    S.numExamples = 0
    S.numEvents = 0
    E = S.firstExample
    while E:
        S.numEvents += E.numEvents
        E = E.next
        S.numExamples += 1

    # / * Build the example and permuted arrays * /
    S.example = []
    S.permuted = []
    # / * Fill the arrays and call the user-defined init procedures on each example and event * /
    i = 0
    E = S.firstExample
    while E:
        S.example[i], S.permuted[i] = E, E
        E.num = i
        totalFreq += E.frequency
        E = E.next
        i += 1
