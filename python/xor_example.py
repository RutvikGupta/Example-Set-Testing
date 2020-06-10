from copy import deepcopy
from typing import List
from python import example_defaults
import re
import numpy as np

TCL_ERROR = False
TCL_OK = True


class ExampleSet:
    """ ExampleSet Object. Stores a set of examples with similar properties on which the neural network will be
        trained on.
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
    selfentExampleNum: int
    selfentExample = None  #: Example
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
    DEF_S_defaultInput: int
    DEF_S_activeInput: int
    DEF_S_defaultTarget: int
    DEF_S_activeTarget: int
    filename: str

    def __init__(self, name: str, filename: str, defaultInput: int, activeInput: int, defaultTarget: int,
                 activeTarget: int):
        self.name = name
        self.pipeLoop = example_defaults.DEF_S_pipeLoop
        self.maxTime = example_defaults.DEF_S_maxTime
        self.minTime = example_defaults.DEF_S_minTime
        self.graceTime = example_defaults.DEF_S_graceTime
        self.defaultInput = defaultInput
        self.activeInput = activeInput
        self.defaultTarget = defaultTarget
        self.activeTarget = activeTarget
        # self.loadEvent = standardLoadEvent
        # self.loadExample = standardLoadExample
        self.numGroupNames = 0
        self.maxGroupNames = 0
        self.groupName = []
        self.numExamples = 0
        self.example = []
        self.filename = filename


class Example:
    """ Example class. The object which stores information related to one example of the ExampleSet and has a list of
        event which will be executed by the neural network
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
    """ Event class. Consist of information related to one event of the Example object and has Range object as inputs
        and targets
    """
    sharedInputs: bool  # flag
    sharedTargets: bool  # flag
    # float = real
    maxTime: float
    minTime: float
    graceTime: float
    defaultInput: float
    activeInput: float
    defaultTarget: float
    activeTarget: float
    inputGroup = []  # List[np]
    targetGroup = []  # List[np]

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
        self.inputGroup = []
        self.targetGroup = []
        # initEventExtension(V)


class UnitGroup:
    """Range class. It stores information related to the inputs and targets of event of event class.
       It can be target OR input based on the variable doing_inputs"""

    groupName: str  # If null, unit offsets are for the net
    numUnits: int
    firstUnit: np  # Only used for dense encodings
    # float replaces real
    group: np  # Only used for dense encodings

    value: float  # Only used for sparse encodings
    unit: int  # Only used for sparse encodings
    event: Event

    def __init__(self, V: Event, doing_inputs: bool, num_units: int, groupname=None):
        self.event = V
        self.groupName = groupname
        self.group = np.array([])
        if doing_inputs:
            self.event.inputGroup.append(self.group)
        else:
            self.event.targetGroup.append(self.group)
        self.numUnits = num_units

    def add_units(self, doing_inputs: bool, unitValue, ):
        if doing_inputs:  # if the Range is an input
            if unitValue:
                self.group = np.append(self.group, [unitValue])
            else:
                self.group = np.append(self.group, [self.event.defaultInput])
        else:
            if unitValue:
                self.group = np.append(self.group, [unitValue])
            else:
                self.group = np.append(self.group, [self.event.defaultTarget])

    def check_units_size(self, doing_inputs: bool):
        if self.group.size > self.numUnits:
            return False
        elif self.group.size < self.numUnits:
            if doing_inputs:
                while self.group.size != self.numUnits:
                    self.group = np.append(self.group, [self.event.defaultInput])
            else:
                while self.group.size != self.numUnits:
                    self.group = np.append(self.group, [self.event.defaultTarget])
        return True


def parse_event_list(event: Event, event_list: str):
    """parse through the list of items and populates Event object
    events in the example file are separated by semicolons. text
    in between two semicolons represent an event."""

    inp_tar_lst = re.split("[A-Z]:", event_list)
    # separates by letter (dense only) and removes the first value
    # because it's the description and does not contain data
    inp_tar_lst.pop(0)
    # event_dict is a set of key-value pairs with letter keys and list of numbers value
    event_dict = {"I": inp_tar_lst[0].split(), "T": inp_tar_lst[1].split()}

    Input_group = UnitGroup(event, True, 2, "Input")
    Target_group = UnitGroup(event, False, 1, "Target")

    for i in range(len(event_dict["I"])):
        Input_group.add_units(True, event_dict["I"][i])

    if Input_group.check_units_size(True) is False:
        return parseError(event.example.set, "Too many units")

    for i in range(len(event_dict["T"])):
        Target_group.add_units(False, event_dict["T"][i])

    if Target_group.check_units_size(False) is False:
        return parseError(event.example.set, "Too many units")


def read_example(S: ExampleSet, example_list: List[str]):
    """reads the example_list string from the example file,
    creates the example and adds it to ExampleSet"""
    # example_list is the example file but in a list of
    # substrings separated by semicolon ;
    example_list.pop()
    header_string = example_list[0]
    S.numExamples = len(example_list) - 1
    for j in range(S.numExamples):
        E = Example(S)
        register_example(E, S)
        E.numEvents = 1
        E.event = []
        for _ in range(E.numEvents):
            new_event = Event(E)
            E.event.append(new_event)
        for i in range(E.numEvents):
            parse_event_list(E.event[i], example_list[j + 1])


def register_example(E: Example, S: ExampleSet):
    """keep track of examples by updating first, last examples"""
    E.next = None
    if not S.firstExample:
        S.firstExample = E
        S.lastExample = E
    else:
        S.lastExample.next = E
        S.lastExample = E
    S.numExamples += 1
    S.example.append(E)
    E.set = S


def read_in_xor_file(S: ExampleSet, name: str):
    """ the ExampleSet contains Examples, which contain Events, which contain
    input and target, both of which are Range objects.
    """
    f = open(name, "r")
    xor_example_list = f.read().split(";")
    read_example(S, xor_example_list)


def parseError(S: ExampleSet, fmt: str) -> bool:
    print("loadExample: " + fmt + " of file " + S.filename)
    return TCL_ERROR


# def print_out_example_set(ES: ExampleSet):
#     """
#     this function just prints out the layers of an ExampleSet
#     so it's easier to visualize. incomplete.
#
#     """
#     S = deepcopy(ES)
#     s = S.name
#     for example_num in range(len(S.example)):
#         s += ": example at list index " + str(example_num) + ', '
#         s += "located in ExampleSet " + S.name + "\n"
#         example = S.example[example_num]
#         for event_num in range(len(example.event)):
#             s += "    " + "event at list index " + str(example_num) + ' : \n'
#             event = example.event[event_num]
#             s += "    " * 2 + "input Range: " + str(event.input) + '\n'
#             list_of_vals = ""
#             while event.input.next is not None:
#                 list_of_vals += str(event.input.val) + ", "
#                 event.input = event.input.next
#
#             s += "    " * 3 + "val: " + list_of_vals + '\n'
#             s += "    " * 2 + "target Range: " + str(event.target) + '\n'
#             s += "    " * 3 + "val: " + str(event.target.val) + '\n'
#     print(s)


if __name__ == "__main__":
    S = ExampleSet("XOR", "xor.ex", 0, 1, 0, 1)
    read_in_xor_file(S, "scratch.txt")
    # print_out_example_set(S)
