from typing import List
from python import example_defaults
import re

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

    example = []  #: List[Example]  list of examples
    permuted = []  #: List[Example]
    currentExampleNum: int
    currentExample = None  #: Example
    firstExample = None  #: Example
    lastExample = None  #: Example
    # Tcl_Obj defined in C macro in example.h
    # proc: Tcl_Obj
    # chooseExample: Tcl_Obj
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
        # self.loadEvent = standardLoadEvent
        # self.loadExample = standardLoadExample
        self.numGroupNames = 0
        self.maxGroupNames = 0
        self.groupName = []
        self.numExamples = 0
        self.example = []



class Example:
    """ example
    """

    name = None  #: str
    num = 0  # : int
    numEvents = 0  #: int
    event = []  #: List[Event]
    set = None  #: ExampleSet
    next = None  #: Example
    ext = None  #: ExampleExt

    # float replaces real
    frequency: float
    probability = 0.0  #: float

    # proc: Tcl_Obj

    # proc function is defined in the C macros

    def __init__(self, S: ExampleSet):
        self.frequency = example_defaults.DEF_E_frequency
        self.set = S
        S.numExamples += 1

        # initExampleExtension(E)


class Event:
    """ event!
    """

    input = None  #: Range
    sharedInputs: bool  # flag
    target = None  #: range
    sharedTargets: bool  # flag
    # float = real
    maxTime: float
    minTime: float
    graceTime: float
    defaultInput: float
    activeInput: float
    defaultTarget: float
    activeTarget: float

    # proc: Tcl_Obj
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
    next = None # Range

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


def parse_event_list(event: Event, event_list: str):
    inp_tar_lst = re.split("[A-Z]:", event_list)
    inp_tar_lst.pop(0)
    event_dict = {"I": inp_tar_lst[0].split(), "T": inp_tar_lst[1].split()}
    for i in range(len(event_dict["I"])):
        if i == 0:
            R = Range(event, True)

        else:
            R = Range(event, True, event.input)
        R.val = int(event_dict["I"][i])
        R.firstUnit = R.val
        R.numUnits = len(event_dict["I"])

    for i in range(len(event_dict["T"])):
        if i == 0:
            R = Range(event, False)

        else:
            R = Range(event, False, event.input)
        R.val = int(event_dict["T"][i])
        R.firstUnit = R.val
        R.numUnits = len(event_dict["T"])


def read_example(S: ExampleSet, example_list: List[str]):
    E = Example(S)

    # add to list of examples
    S.example.append(E)

    example_list.pop()
    header_string = example_list[0]

    E.numEvents = len(example_list) - 1
    E.event = []
    for _ in range(E.numEvents):
        new_event = Event(E)
        E.event.append(new_event)
    for i in range(E.numEvents):
        parse_event_list(E.event[i], example_list[i + 1])


def read_in_xor_file(S: ExampleSet, name: str):
    f = open(name, "r")
    xor_example_list = f.read().split(";")
    read_example(S, xor_example_list)


if __name__ == "__main__":
    S = ExampleSet("Logic")
    read_in_xor_file(S, "scratch.txt")

    print("S.example:")
    print(S.example)

    


