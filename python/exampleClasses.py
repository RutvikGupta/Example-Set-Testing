from typing import List

TCL_ERROR = False
TCL_OK = True



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
