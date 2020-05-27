class ExampleSet:
    """ set of examples linked list
    """
    name: str
    num: int
    # need python mask
    mode: int # mask
    numExamples: int
    numEvents: int
    ext = None #: ExSetExt
    # where is ExSetExt defined?? 

    example = None #: Example
    permuted = None #: Example
    currentExampleNum: int
    currentExample = None #: Example
    firstExample = None #: Example
    lastExample = None #: Example
    pipeExample = None #: Example
    pipeParser: ParseRec 
    # whats that ^^

    pipeLoop: bool # flag
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
    numGroupNames: short #hidden
    maxGroupNames: short #hidden
    groupName: str #hidden

    #what are flags and how to translate? 

    # flag     (*loadEvent)(Event V);
    # flag     (*loadExample)(Example E);
    # flag     (*nextExample)(ExampleSet S);

    def __init__(self, name: str):
        self.name = name
        self.pipeLoop = DEF_S_pipeLoop
        self.maxTime = DEF_S_maxTime
        self.minTime = DEF_S_minTime
        self.graceTime = DEF_S_graceTime
        self.defaultInput = DEF_S_defaultInput
        self.activeInput = DEF_S_activeInput
        self.defaultTarget = DEF_S_defaultTarget
        self.activeTarget = DEF_S_activeTarget
        self.loadEvent = standardLoadEvent
        self.loadExample = standardLoadExample
        self.numGroupNames = 0
        self.maxGroupNames = 0
        self.groupName = NULL


class Example:
    """ example
    """

    name = None #: str
    num = 0 # : int
    numEvents = 0 #: int
    event = None  #: Event
    set = None  #: ExampleSet
    next = None  #: Example
    ext = None  #: ExampleExt

    # float replaces real
    frequency: float
    probability = 0.0 #: float

    proc: Tcl_Obj

    # proc function is defined in the C macros

    def __init__(self, S: ExampleSet):
        self.frequency = DEF_E_frequency
        self.set = S

        # initExampleExtension(E)


class Event:
    """ event! 
    """

    input = None #: Range
    sharedInputs: bool # flag
    target: range
    sharedTargets: bool # flag
    
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
    ext = None #: EventExt

    def __init__(self, E: Example):
        S = E.set
        self.example = E
        self.maxTime = DEF_V_maxTime
        self.minTime = DEF_V_minTime
        self.graceTime = DEF_V_graceTime
        self.defaultInput = S.defaultInput
        self.activeInput = S.activeInput
        self.defaultTarget = S.defaultTarget
        self.activeTarget = S.activeTarget
        # initEventExtension(V)


class Range:
    """range"""

    groupName: str          # If null, unit offsets are for the net
    numUnits: int
    firstUnit: int          # Only used for dense encodings
    # float replaces real
    val: float              # Only used for dense encodings

    value: float            # Only used for sparse encodings
    unit: int               # Only used for sparse encodings

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
    E.frequency = DEF_E_frequency
    E.probability = 0.0
    E.proc = None

# This is used when writing an example file 
def normalEvent(V: Event, S: ExampleSet) -> bool:
    if V.proc is None:
        return False
    elif not V.maxTime is DEF_V_maxTime:
        return False
    elif not V.minTime is DEF_V_minTime:
        return False
    elif not V.graceTime is DEF_V_graceTime:
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

# def parseError(R: ParseRec, fmt: str, ...) -> bool:

# static flag parseError(ParseRec R, char *fmt, ...) {
#   char message[256];
#   va_list args;
#   if (fmt[0]) {
#     va_start(args, fmt);
#     vsprintf(message, fmt, args);
#     va_end(args);
#     error("loadExamples: %s on %s %d of file \"%s\"",
# 	  message, (R->binary) ? "example" : "line", R->line, R->fileName);
#   }
#   if (R->channel) closeChannel(R->channel);
#   R->channel = NULL;
#   FREE(R->fileName);
#   freeString(R->buf);
#   R->buf = NULL;

#   return TCL_ERROR;
# }

# do we need custom memory management? 
def freeExampleSet(S: ExampleSet):
    E, N = Example(), Example()
    if not S:
        return
    # free S.name
    E = S.firstExample
    while E:
        N = E.next
        # freeExample(E)
        E = N
    #free S.example
    #free S.permuted
    if S.proc:
        #Tcl_DecrRefCount(S->proc)
    if S.pipeParser:
        # parseError(S->pipeParser, "");
        # free(S->pipeParser);
    # FREE(S->groupName);

    # freeExSetExtension(S);
    # free(S);

# This puts all the examples in arrays and does some other calculations 
def compileExampleSet(S: ExampleSet):
    E = Example()
    i, v = 0, 0

    # what is Tcl Cmd info? 

# This parses a list of event numbers 
# this function copy pasted C function calls; will need to reimplement some of them 
# used bool for flag; true replaces Tcl_Ok
def parseEventList(R: ParseRec, eventActive: List[str], num: int) -> bool:
    empty = True
    v, w = 0, 0
    # bzero((void *) eventActive, num)

    # skipBlank(R)
    while R.s[0].isdigit() or R.s[0] == "*":
        empty = False
        if stringMatch(R, "*"): # ! C function
            for v in range(num):
                eventActive[v] = True
        else:
            if readInt(R, &v)): # ! C functions
                return parseError(R, "error reading event list")
            if v < 0 or v >= num:
                return parseError(R, "event (%d) out of range", v)
            if stringMatch(R, "-"):
                if readInt(R, &w):
                    return parseError(R, "error reading event range")
                if w <= v or w >= num:
                    return parseError(R, "event (%d) out of range", w)
            else:
                w = v
            while v <= w:
                eventActive[v] = True
                v += 1
        # skipBlank(R)
    if empty:
        for v in range(num):
            eventActive[v] = True
    return True
        
def tidyUpRange(L: Range, unit: int, val: float, sparseMode: bool):
    i = 1
    if !L: 
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


def registerGroupName(name: str, S: ExampleSet) -> str:
    i = 0
    while i < S.numGroupNames and S.groupName[i] == name:
        i += 1
    if i == S.numGroupNames:
        if S.maxGroupNames == 0:
            S.maxGroupNames = 16
            S.groupName = "registerGroupName"
        elif i == S.maxGroupNames:
            S.maxGroupNames *= 2
            S.groupName = "registerGroupName"
      
        S.numGroupNames += 1
        # S.groupName[S.numGroupNames] = copyString(name)    
    return S.groupName[i]
    
