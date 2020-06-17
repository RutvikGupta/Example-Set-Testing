from typing import List
from python import example_defaults
import re
import numpy as np


class ExampleSet:
    """ExampleSet Object. Stores a set of examples with similar properties
    on which the neural network will be trained on.
    Each .ex file contains information used to construct one ExampleSet.

    ======================================================================

    :param name: name of this ExampleSet
    :type name: str
    :param num:
    :type num: str
    :param mode:
    :type mode: int
    :param num_examples: number of examples
    :type num_examples: int
    :param num_events: number of events
    :type num_events: int
    :param example: list of examples in this set
    :type example: List[Example]
    :param permuted:
    :type permuted: List[Example]
    :param selfent_example_num:
    :type selfent_example_num: int
    :param selfent_example:
    :type selfent_example: Example
    :param first_example: first example
    :type first_example: Example
    :param last_example: last example
    :type last_example: Example
    :param max_time:
    :type max_time: float
    :param grace_time:
    :type grace_time: float
    :param default_input:
    :type default_input: float
    :param active_input:
    :type active_input: float
    :param default_target:
    :type default_target: float
    :param active_target:
    :type active_target: float
    :param max_group_names:
    :type max_group_names: float
    :param group_name:
    :type group_name: List
    :param DEF_S_default_input:
    :type DEF_S_default_input: int
    :param DEF_S_active_input:
    :type DEF_S_active_input: int
    :param DEF_S_default_target:
    :type DEF_S_default_target: int
    :param DEF_S_active_target:
    :type DEF_S_active_target: int
    :param file_name:
    :type file_name: str
    :param file_str: string representation of the raw file
    :type file_str: str
    """
    name: str
    num: int
    # need python mask
    mode: int  # mask
    num_examples: int
    num_events: int

    example = []  #: List[Example]  list of examples
    permuted = []  #: List[Example]
    selfent_example_num: int
    selfent_example = None  #: Example
    first_example = None  #: Example
    last_example = None  #: Example
    # Tcl_Obj defined in C macro in example.h
    # proc: Tcl_Obj
    # chooseExample: Tcl_Obj
    max_time: float
    min_time: float
    grace_time: float
    default_input: float
    active_input: float
    default_target: float
    active_target: float
    # int replaces short
    num_group_names: int  # hidden
    max_group_names: int  # hidden
    group_name: list  # hidden
    DEF_S_default_input: int
    DEF_S_active_input: int
    DEF_S_default_target: int
    DEF_S_active_target: int
    file_name: str

    def __init__(self, name: str, file_name: str, default_input: int, active_input: int, default_target: int,
                 active_target: int, def_s_pipe_loop=example_defaults.DEF_S_pipeLoop,
                 def_s_max_time=example_defaults.DEF_S_maxTime, def_s_min_time=example_defaults.DEF_S_minTime,
                 def_s_grace_time=example_defaults.DEF_S_graceTime):
        self.name = name
        self.pipeLoop = def_s_pipe_loop
        self.max_time = def_s_max_time
        self.min_time = def_s_min_time
        self.grace_time = def_s_grace_time
        self.default_input = default_input
        self.active_input = active_input
        self.default_target = default_target
        self.active_target = active_target

        self.num_group_names = 0
        self.max_group_names = 0
        self.group_name = []
        self.num_examples = 0
        self.num_events = 0
        self.example = []
        self.file_name = file_name
        # read_in_file(self, file_name)

    def print_out(self):
        print_out_example_set(self)


class Example:
    """ Example class. The object which stores information related to one example of the
    ExampleSet and has a list of events which will be executed by the neural network

    :param name: name of Example
    :type name: str
    :param: num:
    :type num: int
    :param num_events:
    :type num_events: int
    :param event: list of Events in this example
    :type event: List[Event]
    :param set: the ExampleSet in which this example belows to
    :type set: ExampleSet
    :param next: next example
    :type next: Example
    """

    name = None  #: str
    num = 0  # : int
    num_events = 0  #: int
    event = []  #: List[Event]
    set = None  #: ExampleSet
    next = None  #: Example
    # float replaces real
    frequency: float
    probability = 0.0  #: float
    events_data = []
    event_headers = []
    proc = None

    # proc function is defined in the C macros

    def __init__(self, S: ExampleSet, frequency=example_defaults.DEF_E_frequency):
        self.frequency = frequency
        self.set = S
        self.event = []
        self.events_data = []
        self.event_headers = []

        # initExampleExtension(E)

    def print_out(self):
        print_out_example(self)


class Event:
    """Event class. Consist of information related to one event of the Example object
    and has UnitGroup object as inputs and targets

    =================================================================================

    :param shared_inputs:
    :type shared_inputs: bool
    :param shared_targets:
    :type shared_targets: bool
    :param max_time:
    :type max_time: float
    :param grace_time:
    :type grace_time: float
    :param default_input:
    :type default_input: float
    :param active_input:
    :type active_input: float
    :param default_target:
    :type default_target: float
    :param active_target:
    :type active_target: float
    :param input_group: list of numpy array of UnitGroups containing the Event inputs
    :type input_group: List[np]
    :param target_group: list of numpy array of UnitGroups containing the Event targets
    :type target_group: List[np]
    :param example: the example in which this Event belongs to
    :type example: Example
    :param ext:
    :type ext: EventExt
    """
    shared_inputs: bool  # flag
    shared_targets: bool  # flag
    max_time: float
    min_time: float
    grace_time: float
    default_input: float
    active_input: float
    default_target: float
    active_target: float
    input_group = []  # List[np]
    target_group = []  # List[np]
    example: Example
    ext = None  #: EventExt

    def __init__(self, E: Example):
        S = E.set
        self.example = E
        # E.event.append(self)
        self.max_time = example_defaults.DEF_V_maxTime
        self.min_time = example_defaults.DEF_V_minTime
        self.grace_time = example_defaults.DEF_V_graceTime
        self.default_input = S.default_input
        self.active_input = S.active_input
        self.default_target = S.default_target
        self.active_target = S.active_target
        self.input_group = []
        self.target_group = []
        # initEventExtension(V)

    def print_out(self):
        print_out_event(self)


class UnitGroup:
    """It stores information related to the inputs and targets of event of event class.
    It can be target OR input based on the variable doing_inputs.
    Used to be called Range class.

    ===================================================================================

    :param group_name:
    :type group_name: str
    :param num_units:
    :type num_units: int
    :param first_unit:
    :type first_unit: np
    :param group:
    :type group: np
    :param value:
    :type value: float
    :param unit:
    :type unit: int
    :param event: the Event in which this UnitGroup belongs to
    :type event: Event
    """

    group_name: str  # If null, unit offsets are for the net
    num_units: int
    first_unit: np  # Only used for dense encodings
    # float replaces real
    group: np  # Only used for dense encodings
    # numpy array containing all units in this group

    value: float  # Only used for sparse encodings
    unit: int  # Only used for sparse encodings
    event: Event

    def __init__(self, V: Event, doing_inputs: bool, num_units: int, group_name=None):
        self.event = V
        self.group_name = group_name
        self.group = np.array([])
        self.num_units = num_units

    def add_units(self, doing_inputs: bool, unit_value=None):
        """ Add unit_value to the group. If unit_value is not given, then a default value
        will be added instead: adds default_input if doing_inputs is true, or else
        adds default_target.

        :param doing_inputs: true if this UnitGroup object is the input of an Event; false otherwise
        :type doing_inputs: bool
        :param unit_value: value of the unit to be added to group
        :type unit_value: int
        """
        if unit_value is not None:  # if value is not given, use default
            self.group = np.append(self.group, [unit_value])
        else:
            if doing_inputs:  # if the Range is an input
                self.group = np.append(self.group, [self.event.default_input])
            else:
                self.group = np.append(self.group, [self.event.default_target])

    def check_units_size(self, doing_inputs: bool) -> bool:
        """ Return True if self.group size is the correct number of units. Otherwise, fills self.group
        with default values until it reaches the correct number of units and return False.

        :param doing_inputs: true if this UnitGroup object is the input of an Event; false otherwise
        :type doing_inputs: bool
        :return: true if self.group size is the correct number of unit.
        :rtype: bool
        """
        if self.group.size > self.num_units:
            return False
        elif self.group.size < self.num_units:
            if doing_inputs:
                while self.group.size != self.num_units:
                    self.group = np.append(self.group, [self.event.default_input])
            else:
                while self.group.size != self.num_units:
                    self.group = np.append(self.group, [self.event.default_target])
        if doing_inputs:
            self.event.input_group.append(self.group)
        else:
            self.event.target_group.append(self.group)
        return True


def parse_event_list(event: Event, event_list: str):
    """ Parse through event_list and populates attributes in event Event object
    in the same way as LENS. Return if an error is found.

    :param event: the event object that is to be populated
    :type event: Event
    :param event_list: a substring of the .ex file containing information about the event
    :type event_list: str
    :return: false if an error is found
    "rtype: optional, false
    """
    event_string = event_list.strip()
    inp_tar_lst = re.split("[IT]:", event_string)
    inp_tar_lst.pop(0)
    # separates by letter (dense only) and removes the first value
    # because it's the description and does not contain data
    # event_dict is a set of key-value pairs with letter keys and list of numbers value
    if "I" and "T" in event_string:
        event_dict = {"I": inp_tar_lst[0].split(), "T": inp_tar_lst[1].split()}
    elif "I" in event_string:
        event_dict = {"I": inp_tar_lst[0].split()}
    else:
        event_dict = {"T": inp_tar_lst[0].split()}

    if "I" in event_dict:
        Input_group = UnitGroup(event, True, len(event_dict["I"]), "Input")
        for i in range(len(event_dict["I"])):
            Input_group.add_units(True, int(event_dict["I"][i]))
        if Input_group.check_units_size(True) is False:
            return parseError(event.example.set, "Too many units")
    if "T" in event_dict:
        Target_group = UnitGroup(event, False, len(event_dict["T"]), "Target")
        for i in range(len(event_dict["T"])):
            Target_group.add_units(False, int(event_dict["T"][i]))

        if Target_group.check_units_size(False) is False:
            return parseError(event.example.set, "Too many units")


def assign_field_values(lookup_string: str, S: ExampleSet, value: str, obj_type: str, event=None):
    if (event is not None) and (type(event) is Event):
        obj = event
    else:
        obj = S
    # p = re.compile("([0-9]+\.[0-9]+)|[0-9]+")
    p = re.compile("([0-9]+\.[0-9]+)")
    print(value)
    if lookup_string == "proc:":
        obj.proc = value
    elif lookup_string == "min:":
        if p.match(value):
            obj.min_time = float(value[0:-1])
            # remove the last piece, which is space or "]"
        elif value == "-":
            obj.min_time = None
        else:
            return parseError(S, "missing value after \"min:\" in " + obj_type + " header")
    elif lookup_string == "max:":
        if p.match(value):
            obj.max_time = float(value)
        elif value == "-":
            obj.max_time = None
        else:
            return parseError(S, "missing value after \"max:\" in " + obj_type + " header")
    elif lookup_string == "grace:":
        if p.match(value):
            obj.grace_time = float(value)
        elif value == "-":
            obj.grace_time = None
        else:
            return parseError(S, "missing value after \"grace:\" in " + obj_type + " header")
    elif lookup_string == "defI:":
        if p.match(value):
            obj.default_input = float(value)
        elif value == "-":
            obj.default_input = None
        else:
            return parseError(S, "missing value after \"defI:\" in " + obj_type + " header")
    elif lookup_string == "defT:":
        if p.match(value):
            obj.default_target = float(value)
        elif value == "-":
            obj.default_target = None
        else:
            return parseError(S, "missing value after \"defT:\" in " + obj_type + " header")
    elif lookup_string == "actI:":
        if p.match(value):
            obj.active_input = float(value)
        elif value == "-":
            obj.active_input = None
        else:
            return parseError(S, "missing value after \"actI:\" in " + obj_type + " header")
    elif lookup_string == "actT:":
        if p.match(value):
            obj.active_target = float(value)
        elif value == "-":
            obj.active_target = None
        else:
            return parseError(S, "missing value after \"actT:\" in " + obj_type + " header")


def parse_example_set_header_string(S: ExampleSet, example_header: str):
    square_index = float("inf")
    if "[" in example_header:
        square_index = example_header.find("[")
    example_header += "\n"
    lookup_list = ["proc:", "min:", "max:", "grace:", "defI:", "defT:", "actT:", "actI:"]
    for lookup_string in lookup_list:
        if lookup_string in example_header:
            index = example_header.find(lookup_string)
            if index < square_index:
                find_newline = example_header[index:].find("\n") + index
                value = example_header[index + len(lookup_string): find_newline].strip()
                assign_field_values(lookup_string, S, value, "Example Set")
                example_header = example_header.replace(example_header[index: find_newline + 1], '')
    return example_header


def parse_event_header_string(event: Event, event_header: str):
    delimiters = re.findall(r'[0-9]\s', event_header)
    event_header_list = re.split(r'[0-9]\s', event_header)
    for i in range(len(delimiters)):
        event_header_list[i] += delimiters[i].strip()

    lookup_list = ["proc:", "min:", "max:", "grace:", "defI:", "defT:", "actT:", "actI:"]
    for lookup_string in lookup_list:
        for element in event_header_list:
            if lookup_string in element:
                colon_index = element.find(":")
                if " " in element:
                    value = element[colon_index + 2:].strip()
                else:
                    value = element[colon_index + 1:].strip()
                assign_field_values(lookup_string, event.example.set, value, "Event", event)
                break
    return True


def ignore_commented_lines(example_array: str):
    while '#' in example_array:
        index = example_array.find("#")
        find_newline = example_array[index:].find("\n") + index
        example_array = example_array.replace(example_array[index: find_newline + 1], '\n')
    return example_array


def parse_example_string(E: Example, example_array: str):
    E.event_headers = re.findall(r'\[(.+)\]', example_array)
    if len(E.event_headers) == 0:
        E.num_events = 1
    else:
        E.num_events = len(E.event_headers)
        E.events_data = re.split(r'\[.+\]', example_array)


def parse_example_arguments(E: Example, example_array: str):
    if "name:" in example_array:
        index = example_array.find("name:")
        find_newline = example_array[index:].find("\n") + index
        example_name = example_array[index + len("name:"): find_newline]
        E.name = example_name
        example_array = example_array.replace(example_array[index: find_newline + 1], '')

    if "freq:" in example_array:
        index = example_array.find("freq:")
        find_newline = example_array[index:].find("\n") + index
        example_freq = example_array[index + len("freq:"): find_newline]
        p = re.compile("([0-9]+\.[0-9]+)|[0-9]+")
        if p.match(example_freq):
            E.frequency = float(example_freq)
            example_array = example_array.replace(example_array[index: find_newline + 1], '')

    if "proc:" in example_array:
        index = example_array.find("proc:")
        find_newline = example_array[index:].find("\n") + index
        example_proc = example_array[index + len("proc:"): find_newline]
        E.proc = example_proc
        example_array = example_array.replace(example_array[index: find_newline + 1], '')

    regex = re.compile("(^|\\n)[0-9]+(\\n|$)")
    matched = regex.search(example_array)
    if matched is not None:
        start = matched.start()
        end = matched.end()
        num = example_array[start: end].strip()
        if num.isdigit():
            E.num_events = int(num)
            example_array = example_array.replace(example_array[start: end], '')

    return example_array


def read_example(S: ExampleSet, example_list: List[str]):
    """ Read the example_list from the .ex file, fill attributes of S and
    registers the example (represented by example_list) in S by calling register_example(.)

    :param S: the ExampleSet where we add the example
    :type S: ExampleSet
    :param example_list: a substring of the .ex file representing an example. Examples are separated by semicolon ; .
    :type example_list: List[str]
    """
    example_list.pop()
    header_string = example_list[0]
    example_list[0] = parse_example_set_header_string(S, header_string)
    if example_list[0].strip() == '':
        example_list.pop(0)

    # if header is empty then remove header
    S.num_examples = len(example_list)
    for j in range(S.num_examples):
        E = Example(S)
        register_example(E, S)
        # example_list[j] = ignore_commented_lines(example_list[j])
        example_list[j] = parse_example_arguments(E, example_list[j])
        parse_example_string(E, example_list[j])
        E.events_data.pop(0)

        for _ in range(E.num_events):
            new_event = Event(E)
            E.event.append(new_event)
        if E.num_events == 1:
            parse_event_list(E.event[0], example_list[j])
        else:
            for i in range(E.num_events):
                parse_event_header_string(E.event[i], E.event_headers[i])
                parse_event_list(E.event[i], E.events_data[i])


def register_example(E: Example, S: ExampleSet):
    """ Add Example E to ExampleSet S and update the attributes of S

    :param E: The Example that is to be added to S
    :type E: Example
    :param S: The ExampleSet where E will be added
    :type S: ExampleSet
    """
    E.next = None
    if not S.first_example:
        S.first_example = E
        S.last_example = E
    else:
        S.last_example.next = E
        S.last_example = E
    S.example.append(E)
    E.set = S


def read_in_file(S: ExampleSet, name: str):
    """ Return a list of strings separated by ";" from name .ex file and then
    fills S object with information from the file by calling read_example

    :param S: the ExampleSet for which information from name file will be filled
    :type S: ExampleSet
    :param name: path of the example set file
    :type name: str
    """
    # open file as string f
    f = open(name)
    # split file by ";"
    S.file_str = f.read()
    split_list = ignore_commented_lines(S.file_str).split(";")
    example_list = []
    for e in split_list:
        example_list.append(e.strip())
    read_example(S, example_list)


def parseError(S: ExampleSet, fmt: str) -> bool:
    """ Prints error message fmt regarding ExampleSet S and return False
    """
    print("loadExample: " + fmt + " of file " + S.file_name)
    return False


def print_out_example_set(S: ExampleSet):
    """ Prints out the instance variables of an ExampleSet and of its Examples.
    This function is a work in progress for testing purposes.
    Each new layer of composition is indicated by indent.

    :param S: the example set to be printed
    :type S: ExampleSet
    """

    s = ""
    s += "ExampleSet " + S.name + ": "
    L = [("fileName", S.file_name), ("numEvents", S.num_events), ("defI", S.default_input)]
    L.extend([("actI", S.active_input), ("defT", S.default_target), ("actT", S.active_target)])
    s += format_object_line(L)
    for example_num in range(len(S.example)):
        ex = S.example[example_num]
        s += print_out_example(ex, False, 1)
    print(s)


def print_out_example(E: Example, printing=True, tabs=0):
    """ Prints out the instance variables of an Example and of its Events
    This function is a work in progress for testing purposes.
    Each new layer of composition is indicated by indent.

    If calling this function directly, please leave
    printing=True and tabs=0 to their default values.

    :param E: the example to be printed
    :type E: Example
    """
    ex = E
    L = [("Obj", "Example"), ("name", ex.name), ("num", ex.num)]
    if ex.next is not None:
        next_name = ex.next.name
    else:
        next_name = None
    s = ""
    L.extend([("numEvents", ex.num_events), ("set.name", ex.set.name), ("next.name", next_name),
              ("frequency", ex.frequency), ("probability", ex.probability)])
    s += format_object_line(L, tabs)
    for event_num in range(len(ex.event)):
        ev = ex.event[event_num]
        s += print_out_event(ev, False, tabs + 1)
    if printing:
        print(s)
    return s


def print_out_event(E: Event, printing=True, tabs=0):
    """ Prints out the instance variables of an Event and of its input and target groups
    This function is a work in progress for testing purposes.
    Each new layer of composition is indicated by indent.

    If calling this function directly, please leave
    printing=True and tabs=0 to their default values.

    :param tabs: int
    :param printing: bool
    :param E: the example to be printed
    :type E: Example
    """
    ev = E
    L = [("Obj", "Event"), ("example.name", ev.example.name), ("maxTime", ev.max_time),
         ("minTime", ev.min_time), ("graceTime", ev.grace_time)]
    L.extend([("defI", ev.default_input), ("actI", ev.active_input), ("defT", ev.default_target),
              ("actT", ev.active_target)])

    s = ""
    s += format_object_line(L, tabs)
    for input_num in range(len(ev.input_group)):
        input = ev.input_group[input_num]
        L = [("input group", input)]
        s += format_object_line(L, tabs + 1)
    for target_num in range(len(ev.target_group)):
        target = ev.target_group[target_num]
        L = [("target group", target)]
        s += format_object_line(L, tabs + 1)
    if printing:
        print(s)
    return s


# These are helper functions for the printing functions.
def tab(n=1):
    return "     " * n


def format_object_line(L, num_tabs=0, row_size=10):
    s = tab(num_tabs)
    size = row_size
    for item in L:
        s += item[0] + " = " + str(item[1]) + ", "
        # if row_size == 0:
        #     s += "\n" + tab(num_tabs)
        #     row_size = size
        # row_size -= 1
    return s + "\n"


if __name__ == "__main__":
    S = ExampleSet("XOR", "train4.ex", 0, 1, 0, 1)
    read_in_file(S, "train4.ex")
    print_out_example_set(S)
    print_out_example(S.first_example)
    print_out_event(S.first_example.event[0])
