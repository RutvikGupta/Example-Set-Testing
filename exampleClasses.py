class ExampleSet:
    """ set of examples linked list
    """
    name: str
    num: int
    # need python mask
    mode: mask
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
    sharedInputs: bool # flag
    target: range
    sharedTargets: bool # flag
    
    # float = real
    maxTime: float
    minTime: float
    graceTime: float
    defaultInput: float
    DEF_S_activeInput: float
    defaultTarget: float
    activeTarget: float

    proc: Tcl_Obj
    example: Example
    ext: EventExt

    def __init__(self):
        pass

class Range:
    """range"""

    groupName: str          # If null, unit offsets are for the net
    numUnits: int
    firstUnit: int          # Only used for dense encodings
    #float replaces real
    val: float              # Only used for dense encodings

    value: float            # Only used for sparse encodings
    unit: int               # Only used for sparse encodings

    next: Range

    def __init__(self, V: Event, L: Range, doing_inputs: bool):
        pass
        # python flags?
        # Range newRange(Event V, Range L, flag doingInputs) {
        # Range N = (Range) safeCalloc(1, sizeof(struct range), "newRange:N");
        # N->value = (doingInputs) ? V->activeInput : V->activeTarget;
        # if (L) L->next = N;
        # else {
        #     if (doingInputs) V->input = N;
        #     else V->target = N;
        # }
        # return N;
        # }

