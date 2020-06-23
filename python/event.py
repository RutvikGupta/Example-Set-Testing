from typing import List
import re
from python import example_defaults
from python.unit_group import UnitGroup


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
    example = None
    ext = None  #: EventExt
    proc = None

    def __init__(self, E):
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
        self.proc = None
        # initEventExtension(V)

    def parse_event_header_string(self, event_header: str):
        """ Parse through event_header substring and assign the values to event using lookup_list

        :param event_header: substring of the example set file representing an event header
        :type event_header: str
        :return:
        """
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
                    self.assign_field_values(lookup_string, value)
                    break
        return True

    def parse_event_list(self, event_list: str):
        """ Parse through event_list and populates attributes in event Event object
        in the same way as LENS. Return if an error is found.
        :param event_list: a substring of the .ex file containing information about the event
        :type event_list: str
        :return: false if an error is found
        "rtype: optional, false
        """
        input_group_len = []
        input_group_name = []
        target_group_len = []
        target_group_name = []
        # was called event.example.set.input_group, but this caused error?
        for group in self.example.set.input_group:
            input_group_len.append(group.num_units)
            input_group_name.append(group.name)
        for group in self.example.set.target_group:
            target_group_len.append(group.num_units)
            target_group_name.append(group.name)
        event_string = event_list.strip()
        inp_tar_lst = re.split("[IT]:", event_string)
        inp_tar_lst.pop(0)
        # separates by letter (dense only) and removes the first value
        # because it's the description and does not contain data
        # event_dict is a set of key-value pairs with letter keys and list of numbers value
        event_dict = {}
        i = 0
        for unit_type in ["I", "T", "B"]:
            if unit_type in event_string:
                event_dict[unit_type] = inp_tar_lst[i].split()
                i += 1

        if "I" in event_dict:
            self.add_unit_groups(True, input_group_len, event_dict["I"], input_group_name)

        if "T" in event_dict:
            self.add_unit_groups(False, target_group_len, event_dict["T"], target_group_name)

        if "B" in event_dict:
            self.add_unit_groups(True, input_group_len, event_dict["I"], input_group_name)
            self.add_unit_groups(False, target_group_len, event_dict["T"], target_group_name)

    def add_unit_groups(self, doing_inputs: bool, group_len: List[int], units: List[str], unitNames: List[str]):
        counter = 0
        group_counter = 0
        while counter < len(units) and group_counter < len(group_len):
            unit_group = UnitGroup(self, group_len[group_counter], unitNames[group_counter])
            for _ in range(group_len[group_counter]):
                if counter < len(units):
                    unit_group.add_units(doing_inputs, int(units[counter]))
                    counter += 1
                else:
                    break
            if unit_group.check_units_size(doing_inputs) is False:
                return self.example.set.parseError("Too many units")
            group_counter += 1
        if group_counter < len(group_len):
            while group_counter < len(group_len):
                unit_group = UnitGroup(self, group_len[group_counter], unitNames[group_counter])
                if unit_group.check_units_size(doing_inputs) is False:
                    return self.example.set.parseError("Too many units")
                group_counter += 1

    def print_out_event(self, printing=True, tabs=0):
        """ Prints out the instance variables of an Event and of its input and target groups
        This function is a work in progress for testing purposes.
        Each new layer of composition is indicated by indent.

        If calling this function directly, please leave
        printing=True and tabs=0 to their default values.

        :param tabs: int
        :param printing: bool
        """
        L = [("Obj", "Event"), ("example.name", self.example.name), ("maxTime", self.max_time),
             ("minTime", self.min_time), ("graceTime", self.grace_time)]
        L.extend([("defI", self.default_input), ("actI", self.active_input), ("defT", self.default_target),
                  ("actT", self.active_target)])

        s = ""
        s += format_object_line(L, tabs)
        for input_num in range(len(self.input_group)):
            input_g = self.input_group[input_num]
            L = [("input group", input_g)]
            s += format_object_line(L, tabs + 1)
        for target_num in range(len(self.target_group)):
            target = self.target_group[target_num]
            L = [("target group", target)]
            s += format_object_line(L, tabs + 1)
        if printing:
            print(s)
        return s

    def print_out(self):
        self.print_out_event()

    def assign_field_values(self, lookup_string: str, value: str):
        """ Set the field value value of type proc, min, max, grace, defI, defT, actI, actT to their
        respective instance attributes in Event S; if Event is None then assign to ExampleSet S

        :param lookup_string: could be proc, min, max, grace, defI, defT, actI, actT
        :type lookup_string: str
        :type value: str
        :return: Optional error
        """
        # p = re.compile("([0-9]+\.[0-9]+)|[0-9]+")
        p = re.compile("([0-9]+\.[0-9]+)")
        print(value)
        if lookup_string == "proc:":
            self.proc = value
        elif lookup_string == "min:":
            if p.match(value):
                self.min_time = float(value)
                # remove the last piece, which is space or "]"
            elif value == "-":
                self.min_time = None
            else:
                return self.example.set.parseError("missing value after \"min:\" in Event header")
        elif lookup_string == "max:":
            if p.match(value):
                self.max_time = float(value)
            elif value == "-":
                self.max_time = None
            else:
                return self.example.set.parseError("missing value after \"max:\" in Event header")
        elif lookup_string == "grace:":
            if p.match(value):
                self.grace_time = float(value)
            elif value == "-":
                self.grace_time = None
            else:
                return self.example.set.parseError("missing value after \"grace:\" in Event header")
        elif lookup_string == "defI:":
            if p.match(value):
                self.default_input = float(value)
            elif value == "-":
                self.default_input = None
            else:
                return self.example.set.parseError("missing value after \"defI:\" in Event header")
        elif lookup_string == "defT:":
            if p.match(value):
                self.default_target = float(value)
            elif value == "-":
                self.default_target = None
            else:
                return self.example.set.parseError("missing value after \"defT:\" in Event header")
        elif lookup_string == "actI:":
            if p.match(value):
                self.active_input = float(value)
            elif value == "-":
                self.active_input = None
            else:
                return self.example.set.parseError("missing value after \"actI:\" in Event header")
        elif lookup_string == "actT:":
            if p.match(value):
                self.active_target = float(value)
            elif value == "-":
                self.active_target = None
            else:
                return self.example.set.parseError("missing value after \"actT:\" in Event header")


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
