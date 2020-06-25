
import copy
from typing import List, Optional
import re
import random
from python.example import Example
from python.event import Event

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
    example_sel = []
    example_sorted = []
    current_example = None
    curr_ex_index = 0
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
        self.example = []
        self.file_name = file_name
        self.input_group = input_groups
        self.target_group = target_groups
        self.proc = None
        self.sort_mode = "ORDERED"

    def sort_examples_by_mode(self, mode="ORDERED"):
        """ Fills self.example_sorted, which is the list of indexes in self.examples
        but sorted by mode.

        In ORDERED mode, which is the default, examples will be presented in the order in
        which they were found in the example file.

        In RANDOMIZED mode, examples will be selected at random with replacement,
        each having the same probability of selection. Note that this differs from
        PERMUTED because it uses replacement. It differs from PROBABILISTIC because it
        ignores the example frequency.

        In PERMUTED mode, examples will be selected at random without replacement,
        each having the same probability of selection. A different order will be
        computed for each pass through the set.

        In PROBABILISTIC mode, examples are selected based on their given frequency.
        Specified frequency values will be normalized over all examples and this
        distribution used for selection. If example sets are concatenated, the distribution
        will be recalculated based on the specified frequencies. An example with no
        frequency specified is given a value of 1.0.

        PIPE mode is used for example sets that are reading from a pipe. The next example
        will be read from the pipe and stored temporarily in the example set's pipeExample
        field. This mode can only be used with example sets for which a pipe was opened
        with "loadExamples ... -m PIPE". If the pipe is exhausted and the example set's
        pipeLoop flag is set to TRUE, which is the default, the pipe will be re-opened
        automatically. If an example set contains both stored examples and an open pipe,
        you can switch between them by changing from PIPE mode to another mode.

        CUSTOM mode allows you to write a procedure that generates the index of the next example. When it's time to
        choose the next example, the example set's chooseExample procedure will be called. This should return an integer
         between 0 and one less than the number of examples, inclusive.
        :param mode:
        :return:
        """
        mode = mode.upper()
        self.sort_mode = mode
        self.example_sorted = []
        self.example_sel = []

        if mode == "ORDERED":
            for i in range(self.num_examples):
                self.example_sorted.append(i)
                self.example_sel.append(self.example[i])
        elif mode == "RANDOMIZED":
            for _ in range(self.num_examples):
                random_index = random.randint(0, self.num_examples - 1)
                self.example_sorted.append(random_index)
                self.example_sel.append(self.example[random_index])
        elif mode == "PERMUTED":
            for i in range(self.num_examples):
                self.example_sorted.append(i)
            random.shuffle(self.example_sorted)
            self.example_sel = copy.copy(self.example)
            random.shuffle(self.example_sel)

        elif mode == "PROBABILISTIC":
            total_freq = 0.0
            freq_cum = [0.0]
            # cumulative frequency of all previous examples parsed. the greater the frequency
            # of an example, the greater the increment over the previous value.
            for e in self.example:
                if isinstance(e.frequency, float):
                    total_freq += e.frequency
                else:
                    return self.parseError("error reading frequency")
                freq_cum.append(total_freq)
            for _ in range(self.num_examples):
                random_choice = random.random() * total_freq
                example_index = 0
                while freq_cum[example_index + 1] < random_choice:
                    example_index += 1
                self.example_sorted.append(example_index)
                self.example_sel.append(self.example[example_index])

        elif mode == "PIPE":
            # TODO
            pass
        elif mode == "CUSTOM":
            # TODO
            pass
        else:
            return self.parseError("invalid example selection mode")

    def iterate_example(self) -> Optional[Example]:
        """ Returns the example at index self.curr_ex_index and increments self.curr_ex_index
        of self.example_sorted. If the index is the last index of the list, re-sort the list.
        :return: next example
        :rtype: Example
        """

        # TODO
        # Note: the current linked list implementation only works when new sorted
        # examples list do not have duplicate examples i.e. permutated

        # TODO for now, please don't use example.next ... instead, get the next index
        original_examples_list_index = self.example_sorted[self.curr_ex_index]
        if self.curr_ex_index == self.num_examples - 1:
            self.reset_example_list(self.sort_mode)
        else:
            self.curr_ex_index += 1
        return self.example[original_examples_list_index]

        # if self.current_example is None:
        #     return None
        # if self.current_example.next is None or self.current_example is self.last_example:
        #     self.reset_example_list()
        # self.current_example = self.current_example.next
        # return self.current_example

    def get_current_example(self):
        """ Returns current example
        """
        return self.example[self.example_sorted[self.curr_ex_index]]

    def reset_example_list(self, mode="ORDERED"):
        """ Re-sort the example list according to mode and updates first_example,
        last_example and each example.next accordingly.
        :param mode: mode to sort example
        :type mode: str
        """
        if not self.example:
            return
        self.example_sorted = []
        self.sort_examples_by_mode(mode)
        self.first_example = self.example[self.example_sorted[0]]
        self.current_example = self.first_example
        self.curr_ex_index = 0
        self.last_example = self.example[self.example_sorted[-1]]
        self.last_example.next = None
        # TODO
        # Note: the current linked list implementation only works when new sorted
        # examples list do not have duplicate examples i.e. permutated
        for e in range(self.num_examples - 1):
            this_example = self.example[self.example_sorted[e]]
            next_example = self.example[self.example_sorted[e + 1]]
            this_example.next = next_example

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

        self.sort_examples_by_mode()
        return True

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
        E.set = self

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
        s = ""
        for e in self.example_sorted:
            s += " -> "
            s += self.example[e].name + " i=" + str(e)
        print(s)

    def parseError(self, fmt: str) -> bool:
        """ Prints error message fmt regarding ExampleSet S and return False
        """
        print("loadExample: " + fmt + " of file " + self.file_name)
        return False

    def print_out(self):
        self.print_out_example_set()


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
    E = ExampleSet("train4.ex", "train4.ex", [], [], 0, 1, 0, 1)
    E.reset_example_list("ORDERED")
    E.print_out_examples()
    E.reset_example_list("PERMUTED")
    E.print_out_examples()
    E.reset_example_list("PROBABILISTIC")
    E.print_out_examples()
    E.reset_example_list("ORDERED")
    E.print_out_examples()
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
    print(E.iterate_example().name)
