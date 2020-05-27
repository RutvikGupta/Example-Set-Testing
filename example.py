class ExampleSet:
    """ set of examples linked list
    """
    name: str
    num: int
    # need python mask
    mode: int  # mask
    numExamples: int
    numEvents: int
    ext: ExSetExt
    # where is ExSetExt defined?? 

    example: Example
    permuted: Example
    currentExampleNum: int
    currentExample: Example
    firstExample: Example
    lastExample: Example
    pipeExample: Example
    pipeParser: ParseRec
    # whats that ^^

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
    numGroupNames: short  # hidden
    maxGroupNames: short  # hidden
    groupName: str  # hidden

    # what are flags and how to translate?  EDIT: flags are just bool

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

    name: str
    num: int
    numEvents: int
    event: Event
    set: ExampleSet
    next: Example
    ext: ExampleExt

    # float replaces real
    frequency: float
    probability: float

    proc: Tcl_Obj

    # proc function is defined in the C macros

    def __init__(self, S: ExampleSet):
        self.frequency = DEF_E_frequency
        self.set = S

        # initExampleExtension(E)


class Event:
    """ event! 
    """

    input: Range
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
    ext: EventExt

    def __init__(self):
        pass


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


def initialize_event(V: Event, E: Example):
    S = E.set
    V.example = E
    V.maxTime = DEF_V_maxTime
    V.minTime = DEF_V_minTime
    V.graceTime = DEF_V_graceTime
    V.defaultInput = S.defaultInput
    V.activeInput = S.activeInput
    V.defaultTarget = S.defaultTarget
    V.activeTarget = S.activeTarget
    # initEventExtension(V)


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
    if not Event():
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


""" This is used when writing an example file """


def normal_event(V: Event, S: ExampleSet):
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
