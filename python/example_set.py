from typing import List
import re
from python.example import Example
from python.event import Event
from python.example_iterator import ExampleIterator

"""/* EXAMPLE SET FIELDS */"""
DEF_S_mode = bool(1 << 0)
DEF_S_pipeLoop = True
DEF_S_maxTime = 1.0
DEF_S_minTime = 0.0
DEF_S_graceTime = 0.0
DEF_S_defaultInput = 0.0
DEF_S_activeInput = 1.0
DEF_S_defaultTarget = 0.0
DEF_S_activeTarget = 1.0


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
    :param example_sel: list of examples but sorted by current selection mode
    :type example_sel: List[Example]
    :param example_sorted: List of indexes from self.examples sorted by current selection mode
    :type example_sorted: List[int]
    :param selfent_example_num:
    :type selfent_example_num: int
    :param selfent_example:
    :type selfent_example: Example
    :param current_example: Current example used by the iterator
    :type current_example: Example
    :param curr_ex_index: Index of the current example in the list example_sorted
    :type curr_ex_index: int
    :param cycle_num: the number of cycles through the list of examples
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
    example_iterator: ExampleIterator
    example_index = []
    current_example = None
    curr_ex_index = 0
    cycle_num = 0
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
    DEF_S_default_input: int
    DEF_S_active_input: int
    DEF_S_default_target: int
    DEF_S_active_target: int
    file_name: str
    proc = None  # a code which needs to be implemented before loading in values
    input_group = None  # List[Group]
    target_group = None  # List[Group]

    def __init__(self, name: str, file_name: str, input_groups, target_groups, default_input: int, active_input: int,
                 default_target: int,
                 active_target: int, def_s_pipe_loop=DEF_S_pipeLoop,
                 def_s_max_time=DEF_S_maxTime, def_s_min_time=DEF_S_minTime,
                 def_s_grace_time=DEF_S_graceTime):
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
        self.example_index = []
        self.example = []
        self.file_name = file_name
        self.input_group = input_groups
        self.target_group = target_groups
        self.proc = None
        self.sort_mode = "ORDERED"

    def iterate_example(self):
        return self.example_iterator.iterate_example()

    def set_sort_mode(self, sort_mode: str):
        """ Manually change sort mode to sort_mode
        :param sort_mode: new sort mode
        :type sort_mode: str
        """
        self.sort_mode = sort_mode
        self.example_iterator.reset_example_list()

    def get_first_example(self):
        """ Returns first example
        """
        return self.example_iterator.first_example()

    def get_last_example(self):
        """ Returns last example
        """
        return self.example_iterator.last_example()

    def get_current_example(self):
        """ Returns current example
        """
        return self.example_iterator.current_example()

    def get_prev_example(self):
        """Returns the previous example"""
        return self.example_iterator.prev_example()

    def get_next_example(self):
        """ Returns next example
        """
        return self.example_iterator.next_example()

    def read_in_file(self, name: str):
        """ Return a list of strings separated by ";" from name .ex file and then
        fills S object with information from the file by calling read_example
        :param name: path of the example set file
        :type name: str
        """
        # open file as string f
        f = open(name)
        # split file by ";"
        file_str = f.read()
        split_list = ignore_commented_lines(file_str).split(";")
        example_list = []
        for e in split_list:
            example_list.append(e.strip())
        return self.read_example(example_list)

    def read_example(self, example_list: List[str]):
        """ Read the example_list from the .ex file, fill attributes of S and
        registers the example (represented by example_list) in S by calling register_example(.)
        :param example_list: a substring of the .ex file representing an example. example_files are separated by
               semicolon ; .
        :type example_list: List[str]
        """
        example_list.pop()
        header_string = example_list[0]
        example_list[0] = self.parse_example_set_header_string(header_string)
        if example_list[0].strip() == '':
            example_list.pop(0)

        # if header is empty then remove header
        self.num_examples = len(example_list)
        for j in range(self.num_examples):
            E = Example(self)
            self.register_example(E)
            res = E.parse_example_arguments(example_list[j])
            if res is False:
                return False
            else:
                example_list[j] = res
            E.parse_example_string(example_list[j])
            if E.events_data != [] and E.events_data[0] == "":
                E.events_data.pop(0)
            for _ in range(E.num_events):
                new_event = Event(E)
                E.event.append(new_event)
            if E.num_events == 1:
                if E.event[0].parse_event_list(example_list[j]) is False:
                    return False
            else:
                for i in range(E.num_events):
                    if E.event[i].parse_event_header_string(E.event_headers[i]) is False:
                        return False
                    if E.event[i].parse_event_list(E.events_data[i]) is False:
                        return False
            if self.example:
                self.current_example = self.example[0]
                self.curr_ex_index = 0
            else:
                self.current_example = None
                self.curr_ex_index = None

        self.set_example_name()

        self.example_iterator = ExampleIterator(self)
        if self.example_iterator.reset_example_list() is False:
            return False
        return True

    def set_example_name(self):
        for ex in self.example:
            if ex.name is None:
                ex.name = self.example.index(ex)

    def register_example(self, E: Example, new=True):
        """ Add Example E to ExampleSet S and update the attributes of S

        :param E: The Example that is to be added to S
        :type E: Example
        """
        E.next = None
        if not self.first_example:
            self.first_example = E
            self.last_example = E
        else:
            self.last_example.next = E
            self.last_example = E
        if new:
            self.example.append(E)

    def parse_example_set_header_string(self, example_header: str):
        """ Parse through example_header substring and assign the values to S using lookup_list
         :param example_header: substring of the example set file representing an example set header
         :type example_header: str
         :return:
         """
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
                    if self.assign_field_values(lookup_string, value) is False:
                        return False
                    example_header = example_header.replace(example_header[index: find_newline + 1], '')
        return example_header

    def assign_field_values(self, lookup_string: str, value: str):
        """ Set the field value value of type proc, min, max, grace, defI, defT, actI, actT to their
        respective instance attributes in Event S; if Event is None then assign to ExampleSet S

        :param lookup_string: could be proc, min, max, grace, defI, defT, actI, actT
        :type lookup_string: str
        :param value:
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
                return self.parseError("missing value after \"min:\" in ExampleSet header")
        elif lookup_string == "max:":
            if p.match(value):
                self.max_time = float(value)
            elif value == "-":
                self.max_time = None
            else:
                return self.parseError("missing value after \"max:\" in ExampleSet header")
        elif lookup_string == "grace:":
            if p.match(value):
                self.grace_time = float(value)
            elif value == "-":
                self.grace_time = None
            else:
                return self.parseError("missing value after \"grace:\" in ExampleSet header")
        elif lookup_string == "defI:":
            if p.match(value):
                self.default_input = float(value)
            elif value == "-":
                self.default_input = None
            else:
                return self.parseError("missing value after \"defI:\" in ExampleSet header")
        elif lookup_string == "defT:":
            if p.match(value):
                self.default_target = float(value)
            elif value == "-":
                self.default_target = None
            else:
                return self.parseError("missing value after \"defT:\" in ExampleSet header")
        elif lookup_string == "actI:":
            if p.match(value):
                self.active_input = float(value)
            elif value == "-":
                self.active_input = None
            else:
                return self.parseError("missing value after \"actI:\" in ExampleSet header")
        elif lookup_string == "actT:":
            if p.match(value):
                self.active_target = float(value)
            elif value == "-":
                self.active_target = None
            else:
                return self.parseError("missing value after \"actT:\" in ExampleSet header")
        return True

    def print_out_example_set(self):
        """ Prints out the instance variables of an ExampleSet and of its example_files.
        This function is a work in progress for testing purposes.
        Each new layer of composition is indicated by indent.
        """

        s = ""
        s += "ExampleSet " + self.name + ": "
        L = [("fileName", self.file_name), ("numEvents", self.num_events), ("defI", self.default_input)]
        L.extend([("actI", self.active_input), ("defT", self.default_target), ("actT", self.active_target)])
        s += format_object_line(L)
        for example_num in range(len(self.example)):
            ex = self.example[example_num]
            s += ex.print_out_example(False, 1)
        print(s)

    def print_out_examples(self):
        """ Prints out the list of examples in the currently sorted order
        """
        self.example_iterator.print_out_examples()

    def parseError(self, fmt: str) -> bool:
        """ Prints error message fmt regarding ExampleSet S and return False
        """
        print("loadExample: " + fmt + " of file " + self.file_name)
        return False

    def print_out(self):
        self.print_out_example_set()

    def write_example_set_to_file(self, file_name):
        """ Writes text file representation of this example set to file_name file
        :param file_name: string of the file to write to.
        :type file_name: str
        """
        s = "hello world\noof"
        f = open(file_name, "w")
        f.write(s)

    def write_example_set_header(self):
        return


def ignore_commented_lines(example_array: str):
    """
    Returns new example_array where all text between "#" and the next new line are removed
    :param example_array:
    :return:
    """
    while '#' in example_array:
        index = example_array.find("#")
        find_newline = example_array[index:].find("\n") + index
        example_array = example_array.replace(example_array[index: find_newline + 1], '\n')
    return example_array


# These are helper functions for the self.print_out functions.
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
    E = ExampleSet("xor_dense.ex", "xor_dense.ex", [], [], 0, 1, 0, 1)
    E.read_in_file(E.file_name)
    E.first_example.print_out()
    # E.write_example_set_to_file("testing.txt")

    E.set_sort_mode("PERMUTED")
    # E.print_out_examples()
    for i in range(8):
        print(E.iterate_example())
